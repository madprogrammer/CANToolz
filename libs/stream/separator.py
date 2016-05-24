from collections import Counter, deque, Iterable
from struct import unpack

from libs.stream.processor import Processor
from libs.utils import bits
from libs.utils import stats

xff = (1 << 16) - 1
x00 = xff << 16


class Separator(Processor):
    def __init__(self, message_builder: callable, fmt='!I', fmt_size=4):
        self._message_builder = message_builder
        self._distribution = Counter()
        self._state = None
        self._format = fmt
        self._format_size = fmt_size

    def process(self, message) -> Iterable:
        msg_size = len(message)

        if self._state is not None:
            self._count_bits(bits.xor(
                bytes(message), bytes(self._state), msg_size), msg_size)

        self._state = message

        start = 0

        for i, end in enumerate(self._indexes()):
            size, payload = bits.read(bytes(self._state), start, end - start)
            value = unpack(
                self._format, bits.align(payload, size, self._format_size))[0]

            if value & xff == xff:
                value >>= 16

            if value | x00 == value:
                value >>= 16

            yield self._message_builder(str(message) + '|' + str(i), value)

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
