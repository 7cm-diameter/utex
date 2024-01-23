from enum import Enum
from time import perf_counter

from amas.agent import Agent, NotWorkingError
from amas.agent import Observer as _Observer
from pyno.ino import ArduinoLineReader


class AgentAddress(Enum):
    """Pre-defined agent addresses"""

    from amas.agent import OBSERVER as _OBSERVER

    OBSERVER = _OBSERVER
    READER = "READER"
    RECORDER = "RECORDER"
    CONTROLLER = "CONTROLLER"


async def _observe(agent: _Observer):
    from utex.scheduler import SessionMarker

    while agent.working():
        _, mess = await agent.recv()
        if mess in (SessionMarker.NEND, SessionMarker.ABEND):
            agent.send_all(mess)
            agent.finish()
            break
    return None


async def self_terminate(agent: Agent, **kwargs) -> None:
    from utex.scheduler import SessionMarker

    try:
        while agent.working():
            _, mess = await agent.recv_from_observer()
            if mess in (SessionMarker.NEND, SessionMarker.ABEND):
                agent.finish()
                break
    except NotWorkingError:
        pass
    return None


async def read(agent: Agent, ino: ArduinoLineReader):
    try:
        while agent.working():
            readline = await agent.call_async(ino.readline)
            if readline is None:
                continue
            readstr = readline.rstrip().decode("utf-8")
            agent.send_to(AgentAddress.RECORDER.value, readstr)
    except NotWorkingError:
        ino.connection.cancel_read()


async def record(agent: Agent, filename: str, timing: bool = False):
    try:
        with open(filename, "w") as f:
            if timing:
                while agent.working():
                    _, mess = await agent.recv()
                    t, e = mess
                    l = f"{t}, {e}"
                    print(l)
                    f.write(l+"\n")
            else:
                while agent.working():
                    _, mess = await agent.recv()
                    print(mess)
                    f.write(f"{mess}\n")
    except NotWorkingError:
        pass


class Observer(_Observer):
    def __init__(self):
        """docstring for __init__"""
        super().__init__()
        self.assign_task(_observe)


class Reader(Agent):
    def __init__(self, ino: ArduinoLineReader):
        super().__init__(AgentAddress.READER.value)
        self.assign_task(read, ino=ino).assign_task(self_terminate)


class Recorder(Agent):
    def __init__(self, filename: str, **kwargs):
        super().__init__(AgentAddress.RECORDER.value)
        self.assign_task(record, filename=filename, **kwargs).assign_task(
            self_terminate
        )
