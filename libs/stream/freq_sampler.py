from collections import Counter, Iterable

from libs.stream.processor import Processor
from libs.stream.msg import *


class FreqSampler(Processor):
    def __init__(self):
        self._ticks = Counter()
        self._beats = Counter()

    def process(self, message) -> Iterable:
        stream = str(message)

        if stream == Heartbeat.STREAM:
            for device in self._ticks:
                self._beats[device] += 1
        else:
            self._ticks[stream] += 1

            if self._beats[stream] >= 1:
                yield FloatMessage(
                    stream, self._beats[stream] * 1.0 / self._ticks[stream])

                self._ticks[stream] = \
                    self._beats[stream] = 0







