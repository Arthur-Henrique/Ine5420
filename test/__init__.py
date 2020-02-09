import unittest

from test.draft import DraftTestCase
from test.model import *

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest([
        DraftTestCase()
        # ClippingTestCase(),
        # RectangleTestCase()
    ])
    unittest.TextTestRunner().run(suite)
