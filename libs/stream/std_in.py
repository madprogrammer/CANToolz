import sys

from collections import Iterable
from libs.stream.processor import Processor
from libs.stream.msg import Heartbeat

class StdIn(Processor):

    def __init__(self, message_builder: callable):
        self._message_builder = message_builder

    def process(self, message) -> Iterable:
        yield from ()

    def flush(self) -> Iterable:
        for line in sys.stdin:
            yield self._message_builder(line)
            yield Heartbeat()
