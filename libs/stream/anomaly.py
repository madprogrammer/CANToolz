from collections import Iterable, Counter

from libs.stream.processor import Processor


class Anomaly(Processor):
    def __init__(self, rate=0.01):
        self._state = Counter()
        self._count = 0
        self._rate = rate

    def process(self, message) -> Iterable:
        point = float(message)

        self._state[point] += 1
        self._count += 1

        if point > self._quantile(1 - self._rate):
            yield message

    def _quantile(self, margin) -> float:
        quantile = _Quantile(margin * self._count)

        for point in sorted(self._state):
            quantile += self._state[point]

            if quantile:
                return point

        return 1 / 0


class _Quantile:
    def __init__(self, value: float):
        self._value = value
        self._acc = 0

    def __iadd__(self, other):
        self._acc += other
        return self

    def __bool__(self):
        return self._acc >= self._value
