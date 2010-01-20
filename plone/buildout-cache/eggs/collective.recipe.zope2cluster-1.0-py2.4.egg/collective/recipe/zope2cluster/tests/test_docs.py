# -*- coding: utf-8 -*-
"""
Doctest runner for 'collective.recipe.zope2cluster'.
"""
__docformat__ = 'restructuredtext'

import os
import re
import unittest
import zc.buildout.tests
import zc.buildout.testing

from zope.testing import doctest, renormalizing

optionflags =  (doctest.ELLIPSIS  |
                doctest.REPORT_ONLY_FIRST_FAILURE |
                doctest.REPORT_UDIFF)

current_dir = os.path.abspath(os.path.dirname(__file__))
recipe_location = current_dir
zope2_location = os.path.join(current_dir, 'zope2')

for i in range(5):
    recipe_location = os.path.split(recipe_location)[0]

def setUp(test):
    zc.buildout.testing.buildoutSetUp(test)

    # Install the recipe in develop mode
    zc.buildout.testing.install_develop('collective.recipe.zope2cluster', test)

    # Install any other recipes that should be available in the tests
    zc.buildout.testing.install('plone.recipe.zope2instance', test)

def test_suite():
    globs = globals()
    suite = unittest.TestSuite((
            doctest.DocFileSuite(
                '../README.txt',
                globs=globs,
                setUp=setUp,
                tearDown=zc.buildout.testing.buildoutTearDown,
                optionflags=optionflags,
                checker=renormalizing.RENormalizing([
                        # If want to clean up the doctest output you
                        # can register additional regexp normalizers
                        # here. The format is a two-tuple with the RE
                        # as the first item and the replacement as the
                        # second item, e.g.
                        # (re.compile('my-[rR]eg[eE]ps'), 'my-regexps')
                        zc.buildout.testing.normalize_path,
                        (re.compile(r'line \d+'), 'line NNN'),
                        (re.compile(r'py\(\d+\)'), 'py(NNN)'),
                        ]),
                ),
            ))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
