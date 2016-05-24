import unittest
import numpy

from libs.stream.anomaly import Anomaly


class DistributionTest(unittest.TestCase):

    def testProcess(self):
        distribution = Anomaly()

        for _ in range(0, 100000):
            list(distribution.process(numpy.random.normal()))

        self.assertLessEqual(round((distribution.quantile(0.75) +
                                    distribution.quantile(0.25)) * 100), 1)
