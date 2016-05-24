import unittest
import numpy

from libs.stream.distribution import Distribution


class DistributionTest(unittest.TestCase):

    def testProcess(self):
        distribution = Distribution()

        for _ in range(0, 100000):
            list(distribution.process(numpy.random.normal()))

        self.assertLessEqual(round((distribution.quantile(0.75) +
                                    distribution.quantile(0.25)) * 100), 1)
