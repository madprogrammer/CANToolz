from struct import unpack, pack
from .bits import align


class StreamMessage:
    def __init__(self, stream: str, payload: bytes, size: int, value: int):
        self.stream = stream

        self._payload = payload
        self._size = size
        self._int = value

    @classmethod
    def from_value(cls, stream: str, value: int):
        return cls(stream, pack('!i', int(value)), 4, value)

    @classmethod
    def from_payload(cls, stream: str, payload: bytes, size: int):
        return cls(stream, payload, size,
                   unpack('!i', align(payload, size, 4))[0])

    def __int__(self):
        return self._int

    def __bytes__(self):
        return self._payload

    def __len__(self):
        return self._size

    def __str__(self):
        return str(self._size) + ':' + str(self._payload)

    def __eq__(self, other):
        if type(other) is StreamMessage:
            return other.stream == self.stream \
                   and len(other) == self._size \
                   and bytes(other) == self._payload

        return False

