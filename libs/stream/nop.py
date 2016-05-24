from collections import Iterable
from libs.stream.processor import Processor


class Nop(Processor):

    def process(self, message) -> Iterable:
        yield message

    def flush(self) -> Iterable:
        yield from ()
