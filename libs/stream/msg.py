import struct

class ByteMessage:

    @classmethod
    def dump(cls, line):
        return cls(str.split(line[:-1], ':'))

    def __init__(self, components: list):
        self._stream = components[0]
        self._size = int(components[1])
        self._payload = bytes.fromhex(components[2])

    def __bytes__(self):
        return self._payload

    def __len__(self):
        return self._size

    def __str__(self):
        return self._stream


class FloatMessage:
    @classmethod
    def conv(cls, a, b):
        return cls(str(a) + '*' + str(b), float(a) * float(b))

    @classmethod
    def builder(cls, stream, value):
        return cls(stream, float(value))

    def __init__(self, stream, value):
        self._stream = stream
        self._value = value

    def __float__(self):
        return self._value

    def __str__(self):
        return self._stream

    def __bytes__(self):
        return struct.pack('!I', int(self._value))


def numeric_msg(stream, value):
    return FloatMessage.builder(stream, value)


def dump_msg(line):
    return ByteMessage.dump(line)
