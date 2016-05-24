from collections import Iterable, Counter

from libs.stream.processor import Processor


class Distribution(Processor):
    def __init__(self):
        self._state = Counter()
        self._count = 0

    def process(self, message) -> Iterable:
        point = float(message)

        self._state[point] += 1
        self._count += 1

        yield from ()

    def quantile(self, margin) -> float:
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
