
import unittest, doctest

def test_suite():
    return unittest.TestSuite([
        doctest.DocTestSuite('archetypes.kss.events'),
        ])
