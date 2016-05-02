from .i_stream_filter import IStreamFilter
from .stream_message import StreamMessage


class Aggregator(IStreamFilter):
    def __init__(self, filter_builder: callable):
        self._filters = dict()
        self._filter_builder = filter_builder

    def write(self, msg: StreamMessage):
        if msg.stream not in self._filters:
            self._filters[msg.stream] = self._filter_builder(msg.stream)

        self._filters[msg.stream].write(msg)

    def read(self) -> list():
        for stream in self._filters:
            for msg in self._filters[stream].read():
                yield msg

    def __iter__(self):
        return iter(self._filters)

    def __getitem__(self, item):
        return self._filters[item]

    def __len__(self):
        return len(self._filters)
