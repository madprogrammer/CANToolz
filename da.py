#!/usr/bin/env python
import sys

from libs.stream.msg import *
from libs.stream.separator import Separator
from libs.stream.std_in import StdIn
from libs.stream.subnet import Subnet
from libs.stream.anomaly import Anomaly
from libs.stream.derivative import Derivative
from libs.stream.nop import Nop
from libs.stream.heartbeat_sampler import HeartbeatSampler
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


# door - 0x12f(96)050 0x12f(85)050
# ??? - 0x12f84210


def main():
    histogram = Subnet(lambda _: Nop())
    stream = histogram * Subnet(detector) * \
             FreqSampler() * \
             HeartbeatSampler() * \
             StdIn(dump_msg)

    for msg in stream():
        print(msg, float(msg))

    stats = histogram.stats()
    print(len(stats), stats)


if __name__ == '__main__':
    main()
