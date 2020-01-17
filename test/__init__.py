import unittest
from test.model import *
import core.core as core


if __name__ == "__main__":

    core.init()

    suite = unittest.TestSuite()
    suite.addTest([
        ClippingTestCase(),
        RectangleTestCase()
    ])
    unittest.TextTestRunner().run(suite)
