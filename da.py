#!/usr/bin/env python

from libs.stream.msg import *
from libs.stream.separator import Separator
from libs.stream.std_in import StdIn
from libs.stream.subnet import Subnet
from libs.stream.anomaly import Anomaly
from libs.stream.nop import Nop
from bitstring import BitArray


def anomaly(_):
    return Anomaly()


def nop(_):
    return Nop()


def device(_):
    return Subnet(anomaly) * \
           Separator(numeric_msg)


def main():
    subnet = Subnet(device) * \
             StdIn(dump_msg)

    for msg in subnet():
        if float(msg) == float(msg):
            print(msg, BitArray(bytes(msg)).bin, float(msg))


if __name__ == '__main__':
    main()

