from abc import ABCMeta, abstractmethod

import numpy as np
from numpy import typing as npt


class SoundBase(metaclass=ABCMeta):
    @property
    @abstractmethod
    def wave(self) -> npt.NDArray[np.float_]:
        pass

    @property
    @abstractmethod
    def samplerate(self) -> int:
        pass


class WhiteNoise(SoundBase):
    def __init__(self, samplerate: int = 48000):
        self.__wave = np.random.uniform(-1, 1, samplerate)
        self.__samplerate = samplerate

    @property
    def wave(self) -> npt.NDArray[np.float_]:
        return self.__wave

    @property
    def samplerate(self) -> int:
        return self.__samplerate


class Speaker(object):
    def __init__(self, device_index: int):
        self.__dev_idx = device_index

    @staticmethod
    def check_availbale_device():
        from sounddevice import query_devices

        return query_devices()

    def play(self, tone: SoundBase, blocking=True, loop: bool = False) -> None:
        from sounddevice import play

        play(
            tone.wave,
            samplerate=tone.samplerate,
            blocking=blocking,
            loop=loop,
            device=self.__dev_idx,
        )
        return None

    def stop(self, ignore_errors: bool = True):
        from sounddevice import stop

        stop(ignore_errors=ignore_errors)
