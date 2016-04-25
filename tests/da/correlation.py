import numpy
import math
import time
import struct
import collections
import functools

pack = numpy.vectorize(lambda i: struct.pack('!f', i))
expand = numpy.vectorize(lambda b: b + b + b)
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

distribution = collections.deque()
prev = None
for x in reversed(sorted(counter)):
    curr = counter[x]
    if prev is not None:
        if prev < curr:
            distribution.appendleft(curr - prev)
        else:
            distribution.appendleft(0)

    prev = curr


quantile_rate = list()
prev = None
for x in range(100, 0, -1):
    curr = numpy.percentile(distribution, x, interpolation='lower')
    if prev is not None:
        quantile_rate.append((prev - curr, curr))

    prev = curr


_, bottom = max(quantile_rate)

breaks = list()
for i, x in enumerate(distribution):
    if x > bottom:
        print(i)
