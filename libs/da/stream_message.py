

class StreamMessage:
    def __init__(self, stream: str, payload: bytes, size: int):
        self.stream = stream
        self.payload = payload
        self.size = size

    def __str__(self):
        return self.stream + ':\t' + \
            '(' + str(self.size) + ')\t' + str(self.payload)
