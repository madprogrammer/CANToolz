#!/usr/bin/env python

from sys import stdin
from libs.da.stream_message import StreamMessage
from libs.da.aggregator import Aggregator
from libs.da.separator import Separator


def dump_message(line: str) -> StreamMessage:
    components = str.split(line[:-1], ':')
    return StreamMessage(components[0],
                         bytes.fromhex(components[2]),
                         int(components[1]))


def main():
    aggregator = Aggregator(lambda stream: Separator(stream))

    for line in stdin:
        aggregator(dump_message(line))

    for separator in aggregator:
        parts = len(aggregator[separator])
        if parts > 1:
            print(separator, parts)


if __name__ == '__main__':
    main()

