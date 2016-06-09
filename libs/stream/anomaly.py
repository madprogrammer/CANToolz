import math

from collections import Iterable, Counter

from libs.stream.processor import Processor


class Anomaly(Processor):
    def __init__(self, rate=0.1):
        self._state = Counter()
        self._count = 0
        self._rate = rate
        self._stream = None

    def process(self, message) -> Iterable:
        point = float(message)

        if math.isnan(point):
            self._state = Counter()
            self._count = 0

            yield message
        else:
            self._state[point] += 1
            self._count += 1

            if point > self._quantile(1 - self._rate, point):
                #print(self._state, self._count)
                yield message

    def _quantile(self, margin, p) -> float:
        quantile = _Quantile(margin * self._count)

        for point in sorted(self._state):
            quantile += self._state[point]

            #print("-----", p, quantile._value, quantile._acc, point)

            if bool(quantile):
                return float(point)

        return float('nan')


class _Quantile:
    def __init__(self, value: float):
        self._value = value
        self._acc = 0

    def __iadd__(self, other):
        self._acc += other
        return self

    def __bool__(self):
        return self._acc >= self._value
