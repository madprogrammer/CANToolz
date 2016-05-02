from .stream_message import StreamMessage


class IStreamFilter:
    def write(self, msg: StreamMessage):
        pass

    def read(self) -> list():
        pass

    def __call__(self, msg: StreamMessage = None):
        if msg is not None:
            self.write(msg)

        return self.read()
