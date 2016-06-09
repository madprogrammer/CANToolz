from collections import Counter, Iterable

from libs.stream.processor import Processor
from libs.stream.msg import *


class FreqSampler(Processor):

    def __init__(self):
        self._circles = 0.0
        self._tick = Counter()

    def process(self, message) -> Iterable:
        stream = str(message)

        if isinstance(message, Heartbeat):
            self._circles += 1
        elif isinstance(message, Bailout):
            self._circles = 0.0
            self._tick = Counter()
        elif self._circles > 0:
            if self._tick[stream] > 0:
                for s in self._tick:
                    yield FloatMessage(s, self._tick[s] / self._circles)

                self._tick.clear()
                self._circles = 0

            self._tick[stream] += 1






