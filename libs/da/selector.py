from collections import Iterable
from .stream_processor import StreamProcessor
from .stream_message import StreamMessage


class Selector(StreamProcessor):
    def __init__(self, stream):
        self._stream = stream

    def process(self, msg: StreamMessage) -> Iterable:
        if msg.stream in self._stream:
            yield msg
