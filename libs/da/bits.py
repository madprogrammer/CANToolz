

def xor(a: bytes, b: bytes, l: int) -> bytes:
    result = bytearray(l)

    for i in range(l):
        result[i] = a[i] ^ b[i]

    return result


def test(frame: bytes, offset: int) -> bool:
    byte = frame[offset // 8]
    mask = 1 << (7 - offset % 8)

    return byte & mask > 0


# assert slice_int(struct.pack('!I',
#   int('11110111111111111111111111111111', 2)), 0, 8) == int('11110111', 2)
def read(frame: bytes, offset: int, limit: int) -> bytes:
    result = 0
    size = len(frame)

    for i, x in enumerate(range(offset + limit, offset, -8)):
        l = x // 8
        h = l - 1
        bit = x % 8

        if l < size:
            byte = frame[h] << bit & 255 | frame[l] >> 8 - bit
        else:
            byte = frame[h] << bit & 255

        if x - 8 < offset:
            byte &= 255 >> offset - x + 8

        result |= byte << 8 * i

    return result



