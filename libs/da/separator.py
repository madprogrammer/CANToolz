from collections import Counter, deque
from . import bits
from . import stats
from .stream_processor import StreamProcessor
from .stream_message import StreamMessage


class Separator(StreamProcessor):
    def __init__(self):
        self._distribution = Counter()
        self._state = None

    def process(self, msg: StreamMessage):
        state_size = 0 if self._state is None else len(self._state)
        msg_size = len(msg)

        if self._state is not None and state_size == msg_size:
            self._count_bits(bits.xor(
                bytes(msg), bytes(self._state), msg_size), msg_size)

        self._state = msg

        start = 0

        for i, end in enumerate(self._indexes()):
            size, payload = bits.read(bytes(self._state), start, end - start)

            yield StreamMessage.from_payload(
                msg.stream + ':' + str(i), payload, size)

            start = end

    def _count_bits(self, frame: bytes, size: int):
        for i in range(8 * size):
            if bits.test(frame, i):
                self._distribution[i] += 1

    def _gaps(self) -> iter:
        gaps = deque()
        prev = None

        for x in range(len(self._state) * 8, 0, -1):
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

        indexes.append(len(self._state) * 8)
        return indexes
