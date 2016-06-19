from collections import Counter, Iterable

from libs.stream.processor import Processor
from libs.stream.msg import *


class HeartbeatSampler(Processor):
    def __init__(self):
        self._ticks = Counter()

    def process(self, message) -> Iterable:
        stream = str(message)

        yield message

        self._ticks[stream] += 1
        if self._ticks[stream] > 1:
            self._ticks.clear()

            yield Heartbeat()

