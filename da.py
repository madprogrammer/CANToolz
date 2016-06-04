#!/usr/bin/env python
import sys

from libs.stream.msg import *
from libs.stream.separator import Separator
from libs.stream.std_in import StdIn
from libs.stream.subnet import Subnet
from libs.stream.anomaly import Anomaly
from libs.stream.derivative import Derivative
from libs.stream.nop import Nop

DETECTOR = {
    'nop': lambda _: Nop(),
    'd': lambda _: Derivative(numeric_msg),
    'anomaly': lambda _: Anomaly(),
    'anomaly/d': lambda _: Anomaly() * Derivative(numeric_msg),
}


def device(_):
    return Subnet(DETECTOR[sys.argv[1]]) * \
           Separator(numeric_msg)


def main():
    subnet = Subnet(device)
    stream = subnet * StdIn(dump_msg)

    for msg in stream():
        if float(msg) == float(msg):
            print(msg, float(msg))

    print(subnet.stats())


if __name__ == '__main__':
    main()

