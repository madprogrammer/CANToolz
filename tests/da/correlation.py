import numpy
import math
import time
import struct
import collections

pack = numpy.vectorize(lambda i: struct.pack('!f', i))
expand = numpy.vectorize(lambda b: b + b)
sine = numpy.vectorize(lambda i: 10*math.sin(i))


def line() -> numpy.array:
    return numpy.arange(0, 100, 0.1)


def test_bit(array: bytearray, offset: int) -> int:
    byte = array[offset // 8]
    mask = 1 << (7 - offset % 8)

    return byte & mask > 0


def diff(curr: bytearray, prev: bytearray, size: int) -> bytearray:
    result = bytearray(size)

    for i in range(size):
        result[i] = curr[i] ^ prev[i]

    return result


def count_bits(cnt: collections.Counter, bits: bytearray, count: int):
    for i in range(8 * count):
        if test_bit(bits, i):
            cnt[i] += 1


fn = sine(line())
series = expand(pack(fn))
counter = collections.Counter()
last = None
last_size = 0

start = time.clock()

for x in numpy.nditer(series):
    payload = bytearray(x)
    size = len(payload)

    if last and size == last_size:
        count_bits(counter, diff(payload, last, size), size)

    last = payload
    last_size = size

print(fn)
for x in sorted(counter):
    print(x, counter[x])