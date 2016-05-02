from collections import Counter, deque
from itertools import chain
from . import bits
from . import stats
from .i_stream_filter import IStreamFilter
from .stream_message import StreamMessage


class Separator(IStreamFilter):

    def __init__(self, stream: str):
        self._distribution = Counter()
        self._state = None
        self._chain = chain()
        self._stream = stream

    def __len__(self):
        return len(self._indexes())

    def read(self) -> iter:
        result = self._chain
        self._chain = chain()
        return result

    def write(self, msg: StreamMessage):
        if self._state is not None and self._state.size == msg.size:
            self._count_bits(bits.xor(
                msg.payload, self._state.payload, msg.size), msg.size)

        self._state = msg
        self._chain = chain(self._chain, self._reader())

    def _reader(self):
        start = 0

        for i, end in enumerate(self._indexes()):
            size = end - start
            payload = bits.read(self._state.payload, start, size)

            yield StreamMessage(
                self._stream + ':' + str(i), payload, size)

            start = end

    def _count_bits(self, frame: bytes, size: int):
        for i in range(8 * size):
            if bits.test(frame, i):
                self._distribution[i] += 1

    def _gaps(self) -> iter:
        gaps = deque()
        prev = None

        for x in range(self._state.size * 8, 0, -1):
            curr = self._distribution[x - 1]

            if prev is not None:
                if prev < curr:
                    gaps.appendleft(curr - prev)
                else:
                    gaps.appendleft(0)

            prev = curr

        return gaps

    def _indexes(self) -> iter:
        indexes = list()
        gaps = self._gaps()
        edge = stats.max_dx_edge(gaps)

        for i, x in enumerate(gaps):
            if x > edge:
                indexes.append(i + 1)

        indexes.append(self._state.size * 8)
        return indexes
