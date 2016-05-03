from collections import Counter, Iterable
from .stream_processor import StreamProcessor
from .stream_message import StreamMessage


class Subnet(StreamProcessor):
    def __init__(self, device_builder: callable):
        self._tick = Counter()
        self._devices = dict()
        self._device_builder = device_builder

    def process(self, msg: StreamMessage) -> Iterable:
        if msg.stream not in self._devices:
            self._devices[msg.stream] = Device(self._device_builder())

        if self._tick[msg.stream] > 0:
            for stream in self._devices:
                if self._tick[stream] == 0:
                    for effect in self._devices[stream].touch():
                        yield effect

            self._tick.clear()

        for effect in self._devices[msg.stream].process(msg):
            yield effect

        self._tick[msg.stream] += 1


class Device(StreamProcessor):
    def __init__(self, core: StreamProcessor):
        self._core = core
        self._state = None

    def process(self, msg: StreamMessage) -> Iterable:
        self._state = msg
        for effect in self._core(msg):
            yield effect

    def touch(self) -> Iterable:
        for effect in self._core(self._state):
            yield effect


