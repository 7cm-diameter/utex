from enum import Enum as __Enum


class SessionMarker(__Enum):
    """Pre-defined events marker"""

    START = 0
    NEND = 1
    ABEND = -1


def elementwise_shuffle(x: list) -> list:
    from numpy.random import choice

    return list(choice(x, size=len(x), replace=False))


def blockwise_shuffle(x: list, blocksize: int) -> list:
    from numpy.random import choice

    length = len(x)
    if not length % blocksize == 0:
        raise ValueError("`x` must be dividable by `blocksize`")
    offsets = list(range(0, length + 1, blocksize))
    ret: list = []
    for i in range(length // blocksize):
        _x = x[offsets[i] : offsets[i + 1]]
        _x = choice(_x, size=len(_x), replace=False)
        ret.extend(_x)
    return ret


def mix(x: list, y: list, px: int, py: int):
    return x * px + y * py


def repeat(x, times: int = 0, each: int = 0) -> list:
    if each > 0:
        return [i for i in x for _ in range(each)]
    ret = [x for _ in range(times)]
    if type(ret[0]) == list:
        return sum(ret, [])
    return ret


class TrialIterator(object):
    from typing import Sequence

    def __init__(self, l: Sequence, *args: Sequence):
        ls = (l, *args)
        lnc = len(ls)
        lnr = len(l)
        self.__tuples: list[tuple] = list(
            map(lambda i: tuple(map(lambda j: ls[j][i], range(lnc))), range(lnr))
        )
        self.__n = lnr
        self.__idx = range(self.__n)
        self.__now = 0

    def __iter__(self):
        return self

    def __next__(self) -> tuple[int, ...]:
        if self.__now >= self.__n:
            raise StopIteration()
        vals = self.__now, *self.__tuples[self.__now]
        self.__now += 1
        return vals
