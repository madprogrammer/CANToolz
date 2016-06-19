from collections import Iterable

from libs.stream.processor import Processor


class Derivative(Processor):
    def __init__(self, message_builder: callable):
        self._message_builder = message_builder
        self._prev = None

    def process(self, message) -> Iterable:
        value = float(message)

        if self._prev is not None:
            yield self._message_builder(str(message) + '|d', abs(value - self._prev))

        self._prev = value

