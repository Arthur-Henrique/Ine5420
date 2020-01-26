import unittest
from test.model import *

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest([
        ClippingTestCase(),
        RectangleTestCase()
    ])
    unittest.TextTestRunner().run(suite)
