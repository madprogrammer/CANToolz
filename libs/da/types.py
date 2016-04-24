import struct


class Component:
    def __init__(self, payload, length):
        self.payload = payload
        self.length = length

    def __int__(self):
        return struct.unpack("!i", self.payload)[0]


class Frame:
    def __init__(self, components):
        self.components = components

