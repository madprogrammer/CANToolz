import numpy as np
import math
from collections import Iterable, deque
from .stream_processor import StreamProcessor
from .stream_message import StreamMessage


class Normalizer(StreamProcessor):
    def __init__(self, size: int):
        self._size = size
        self._queue = deque()

    def process(self, msg: StreamMessage) -> Iterable:
        if len(self._queue) == self._size:
            self._queue.popleft()

        self._queue.append(int(msg))

        array = np.array(self._queue)
        mean = array.mean()
        var = math.sqrt(array.var())

        if var != 0:
            yield StreamMessage.from_value(
                msg.stream, (int(msg) - mean) / var)
