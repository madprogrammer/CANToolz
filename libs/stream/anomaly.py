import math

from collections import Iterable, Counter

from libs.stream.processor import Processor
from libs.stream.msg import Bailout


class Anomaly(Processor):

    def __init__(self):
        self._state = Counter()
        self._count = 0
        self._rate = 0

    def process(self, message) -> Iterable:
        point = float(message)

        if str(message) == Bailout.STREAM:
            self._state.clear()
            self._count = 0

            yield message
        else:
            self._state[point] += 1
            self._count += 1

            quantile, deviation = self._quantile(self._rate)

            if point > quantile:
                if self._rate > 0:
                    yield message

                self._rate = deviation * 1.1

    def _quantile(self, margin) -> (float, float):
        quantile = _Quantile(margin * self._count)

        for point in sorted(self._state):
            quantile += self._state[point]

            if bool(quantile):
                return float(point), quantile.acc() / self._count

        return float('nan'), 0


class _Quantile:
    def __init__(self, value: float):
        self._value = value
        self._acc = 0

    def __iadd__(self, other):
        self._acc += other
        return self

    def __bool__(self):
        return self._acc > self._value

    def acc(self):
        return self._acc
