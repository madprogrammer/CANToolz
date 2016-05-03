#!/usr/bin/env python

from sys import stdin
from collections import deque
from libs.da.stream_message import StreamMessage
from libs.da.stream_processor import StreamProcessor
from libs.da.subnet import Subnet
from libs.da.separator import Separator
from libs.da.normalizer import Normalizer
from libs.da.combinations import Combinations
from libs.da.selector import Selector


class Convolution(StreamProcessor):
    def __init__(self, a: str, b: str, size: int):
        self._size = size
        self._a = a
        self._b = b
        self._a_slider = deque()
        self._b_slider = deque()

    def process(self, msg: StreamMessage):
        if msg.stream == self._a:
            self._a_slider.append(msg._int)

        if msg.stream == self._b:
            self._b_slider.append(msg._int)

        if len(self._b_slider) == len(self._a_slider) > self._size:
            corr = 0
            for a, b in zip(self._b_slider, self._a_slider):
                corr += a * b

            print(self._a, self._b, corr)

            self._a_slider.popleft()
            self._b_slider.popleft()

        if False:
            yield


def dump_source(source: iter) -> iter:
    for line in source:
        components = str.split(line[:-1], ':')
        yield StreamMessage.from_payload(
            components[0], bytes.fromhex(components[2]), int(components[1]))
        yield StreamMessage.from_payload(
            components[0] + '!', bytes.fromhex(components[2]), int(components[1]))


def main():
    separate = Subnet(lambda: Selector(['0x16f86250', '0x16f86250!']) * Separator())
    normalize = Subnet(lambda: Selector(['0x16f86250:0', '0x16f86250!:0']) * Normalizer(5))
    correlate = Combinations(2, lambda a, b: Convolution(a, b, 5))

    separated = separate(dump_source(stdin))

    for msg in correlate(normalize(separated)):
        print(msg.stream, msg._int)


if __name__ == '__main__':
    main()

