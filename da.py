#!/usr/bin/env python

from libs.stream.msg import *
from libs.stream.separator import Separator
from libs.stream.std_in import StdIn
from libs.stream.subnet import Subnet
from libs.stream.anomaly import Anomaly
from libs.stream.derivative import Derivative
from libs.stream.nop import Nop
from bitstring import BitArray


def anomaly(_):
    return Anomaly()


def d_anomaly(_):
    return Anomaly() * Derivative(numeric_msg)


def nop(_):
    return Nop()


def d_nop(_):
    return Derivative(numeric_msg)


def device(_):
    return Subnet(anomaly) * \
           Separator(numeric_msg)


def main():
    subnet = Subnet(device) * \
             StdIn(dump_msg)

    for msg in subnet():
        if float(msg) == float(msg):
            print(msg, float(msg))


if __name__ == '__main__':
    main()

