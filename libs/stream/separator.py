from collections import Counter, deque, Iterable
from struct import unpack

from libs.stream.processor import Processor
from libs.utils import bits
from libs.utils import stats
from libs.stream.msg import *
from bitstring import BitArray


class Separator(Processor):
    def __init__(self, message_builder: callable, fmt='!I', fmt_size=4):
        self._message_builder = message_builder
        self._distribution = Counter()
        self._state = None
        self._format = fmt
        self._format_size = fmt_size
        self._result = dict()

    def process(self, message) -> Iterable:
        if isinstance(message, Heartbeat):
            yield message
            return

        msg_size = len(message)

        if self._state is not None:
            self._count_bits(bits.xor(
                bytes(message), bytes(self._state), msg_size), msg_size)

        self._state = message

        left = 0
        data = bytes(self._state)

        for i, end in enumerate(self._indexes()):
            right = end
            for bit in range(end, left - 1, -1):
                if self._distribution[bit] == 0:
                    right = bit

            if right > left:
                size, payload = bits.read(data, left, right - left)

                value = unpack(self._format, bits.align(
                    payload, size, self._format_size))[0]

                stream = str(message) + '|' + str(i)

                if i in self._result and self._result[i] != (left, right):
                    self._result.clear()
                    yield Bailout()

                yield self._message_builder(stream, value)

                self._result[i] = (left, right)

            left = end

    def _count_bits(self, frame: bytes, size: int):
        for i in range(8 * size):
            if bits.test(frame, i):
                self._distribution[i] += 1

    def _gaps(self) -> iter:
        length = len(self._state) * 8
        gaps = [0] * length
        gap_power = 1

        prev = None
        for x in range(length, 0, -1):
            curr = self._distribution[x - 1]

            if prev is not None:
                gap_size = curr - prev
                gaps[x] = gap_size

                if gap_size > 0:
                    gaps[x] = gaps[x] * gap_power
                elif gap_size == 0:
                    gap_power += 1
                else:
                    gap_power = 1

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
