#!/usr/bin/env python

from libs.stream.msg import *
from libs.stream.derivative import Derivative
from libs.stream.integrate import Integrate
from libs.stream.nop import Nop
from libs.stream.selector import Selector
from libs.stream.separator import Separator
from libs.stream.std_in import StdIn
from libs.stream.subnet import Subnet
from libs.stream.anomaly import Anomaly


def device(_):
    return Anomaly() * \
           (Derivative(numeric_msg) + Nop()) * \
           Separator(numeric_msg)


def main():
    subnet = Subnet(device) * StdIn(dump_msg)

    for msg in subnet():
        print(msg, int(float(msg)) >> 16, bytes(msg))


if __name__ == '__main__':
    main()

