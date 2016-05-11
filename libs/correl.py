from collections import deque
from sys import stdin
from struct import unpack

from libs.utils import bits
from libs.stream.normalizer import Normalizer
from libs.stream.processor import Processor
from libs.stream.subnet import Subnet
from libs.stream.selector import Selector
from libs.stream.integrator import Integrator
from libs.stream.forced_sampler import ForcedSampler
from libs.stream.separator import Separator


class RawMessage:
    def __init__(self, fid, size, data):
        self._stream = int(fid)
        self._size = int(size)
        self._payload = bytes(data)

    def __bytes__(self):
        return self._payload

    def __len__(self):
        return self._size

    def __str__(self):
        return self._stream


class SeparatedMessage:

    @classmethod
    def builder(cls, raw, index, payload, size):
        return cls(str(raw) + '|' + str(index),
                   unpack('!I', bits.align(payload, size, 4))[0])

    def __init__(self, stream, value):
        self._stream = stream
        self._value = value

    def __float__(self):
        return float(self._value)

    def __str__(self):
        return self._stream


class FloatMessage:
    @classmethod
    def conv(cls, a, b):
        return cls(str(a) + '*' + str(b), float(a) * float(b))

    @classmethod
    def simple(cls, raw, value):
        return cls(str(raw), value)

    def __init__(self, stream, value):
        self._stream = stream
        self._value = value

    def __float__(self):
        return self._value

    def __str__(self):
        return self._stream


def same(x):
    return x
