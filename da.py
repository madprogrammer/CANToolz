#!/usr/bin/env python

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
    def __init__(self, components: list):
        self._stream = components[0]
        self._size = int(components[1])
        self._payload = bytes.fromhex(components[2])

    def __bytes__(self):
        return self._payload

    def __len__(self):
        return self._size

    def __str__(self):
        return self._stream


class SeparatedMessage:

    @classmethod
    def builder(cls, raw: RawMessage, index: int, payload: bytes, size: int):
        return cls(str(raw) + '|' + str(index),
                   unpack('!I', bits.align(payload, size, 4))[0])

    def __init__(self, stream: str, value: int):
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
    def simple(cls, raw, value: float):
        return cls(str(raw), value)

    def __init__(self, stream: str, value: float):
        self._stream = stream
        self._value = value

    def __float__(self):
        return self._value

    def __str__(self):
        return self._stream


def input_reader(source):
    for line in source:
        yield RawMessage(str.split(line[:-1], ':'))


def same(x):
    return x


def main():
    dump = input_reader(stdin)
    align = ForcedSampler(1, same)
    subnet = Subnet(lambda stream: Separator(SeparatedMessage.builder))

    normalize = Subnet(lambda stream: Normalizer(10, FloatMessage.simple))

    conv = ForcedSampler(2, FloatMessage.conv)
    integrate = Integrator(10, FloatMessage.simple)

    for msg in integrate(conv(normalize(subnet(align(dump))))):
        if float(msg) > 1:
            print(msg, float(msg))


if __name__ == '__main__':
    main()

