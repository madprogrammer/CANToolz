from collections import Iterable
from .stream_message import StreamMessage


class StreamProcessor:
    def process(self, msg: StreamMessage) -> Iterable:
        pass

    def __mul__(self, other):
        return Composition(self, other)

    def __call__(self, source) -> Iterable:
        if type(source) is StreamMessage:
            for effect in self.process(source):
                yield effect
        else:
            for msg in source:
                for effect in self.process(msg):
                    yield effect


class Composition(StreamProcessor):
    def __init__(self, source: StreamProcessor, target: StreamProcessor):
        self._source = source
        self._target = target

    def process(self, msg: StreamMessage) -> Iterable:
        for effect in self._target(self._source(msg)):
            yield effect

