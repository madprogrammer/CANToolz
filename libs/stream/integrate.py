import math
import numpy

from collections import Iterable, deque

from libs.stream.processor import Processor


class Integrate(Processor):
    def __init__(self, message_builder: callable):
        self._message_builder = message_builder
        self._sum = 0

    def process(self, message) -> Iterable:

        self._sum += float(message)

        yield self._message_builder(str(message) + '|i', self._sum)

