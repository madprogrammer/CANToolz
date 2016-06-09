#!/usr/bin/env python
import sys

from libs.stream.msg import *
from libs.stream.separator import Separator
from libs.stream.selector import Selector
from libs.stream.std_in import StdIn
from libs.stream.subnet import Subnet
from libs.stream.anomaly import Anomaly
from libs.stream.derivative import Derivative
from libs.stream.nop import Nop
from libs.stream.freq_sampler import FreqSampler

DETECTOR = {
    'nop': lambda _: Nop(),
    'd': lambda _: Derivative(numeric_msg),
    'anomaly': lambda _: Anomaly(),
    'anomaly/d': lambda _: Anomaly() * Derivative(numeric_msg),
}


def detector(_):
    return DETECTOR[sys.argv[1]](_)


def separator(_):
    return Separator(numeric_msg)


def main():
    #stream = Subnet(detector) * Selector('0x12f84210') * FreqSampler() * StdIn(dump_msg)
    stream = Subnet(detector) * FreqSampler() * StdIn(dump_msg)
    #

    for msg in stream():
        if float(msg) == float(msg):
            print(msg, float(msg))


if __name__ == '__main__':
    main()

