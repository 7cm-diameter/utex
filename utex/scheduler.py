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


def blockwise_shuffle2(x1: list, x2: list, blocksize: int) -> tuple[list, list]:
    from numpy.random import choice

    l1 = len(x1)
    l2 = len(x2)
    if l1 != l2:
        raise ValueError("`x1` and `x2` must be the same length")

    if not l1 % blocksize == 0:
        raise ValueError("`x` must be dividable by `blocksize`")

    offsets = list(range(0, l1 + 1, blocksize))
    ret1: list = []
    ret2: list = []
    for i in range(l1 // blocksize):
        onset = offsets[i]
        offset = offsets[i + 1]
        _x1 = x1[onset:offset]
        _x2 = x2[onset:offset]
        _sn = choice(len(_x1), size=len(_x1), replace=False)
        _x1 = [_x1[i] for i in _sn]
        _x2 = [_x2[i] for i in _sn]
        ret1.extend(_x1)
        ret2.extend(_x2)
    return ret1, ret2


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
