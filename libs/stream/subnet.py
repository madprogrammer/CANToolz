from collections import Iterable, Counter

from libs.stream.processor import Processor


class Subnet(Processor):
    def __init__(self, device_builder: callable):
        self._devices = dict()
        self._device_builder = device_builder
        self._stats = Counter()

    def process(self, message) -> Iterable:
        stream = str(message)

        if stream not in self._devices:
            self._devices[stream] = self._device_builder(stream)

        self._stats[stream] += 1

        yield from self._devices[stream].process(message)

    def stats(self):
        return sorted(self._stats.items(), key=lambda kv: kv[1])
