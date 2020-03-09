import unittest

from test.loader import LoaderTestCase

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest([
        LoaderTestCase()
    ])
    unittest.TextTestRunner().run(suite)
