from collections import Iterable
from itertools import combinations
from .stream_processor import StreamProcessor
from .stream_message import StreamMessage


class Combinations(StreamProcessor):
    def __init__(self, power: int, builder: callable):
        self._streams = set()
        self._power = power
        self._builder = builder
        self._combinations = dict()

    def process(self, msg: StreamMessage) -> Iterable:
        if msg.stream not in self._streams:
            self._streams.add(msg.stream)

        for combination in combinations(self._streams, self._power):
            if combination not in self._combinations:
                self._combinations[combination] = self._builder(*combination)

            if msg.stream in combination:
                for effect in self._combinations[combination].process(msg):
                    yield effect
