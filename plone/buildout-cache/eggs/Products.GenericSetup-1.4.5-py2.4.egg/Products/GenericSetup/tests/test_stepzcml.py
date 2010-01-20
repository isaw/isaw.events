##############################################################################
#
# Copyright (c) 2007 Zope Corporation and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Unit tests for import/export step zcml module.

$Id: test_stepzcml.py 82385 2007-12-21 11:51:03Z yuppie $
"""

import unittest
from zope.testing.cleanup import cleanUp

import Products.GenericSetup
from Products.GenericSetup.registry import _import_step_registry
from Products.Five import zcml

EMPTY_ZCML = '''<configure xmlns:genericsetup="http://namespaces.zope.org/genericsetup">
</configure>'''

ONE_STEP_ZCML = '''<configure xmlns:genericsetup="http://namespaces.zope.org/genericsetup" i18n_domain="genericsetup">
<genericsetup:importStep
    name="Products.GenericSetup.teststep"
    title="step title"
    description="step description"
    handler="Products.GenericSetup.initialize"
    />
</configure>'''

class ImportStepTests(unittest.TestCase):

    def setUp(self):
        zcml.load_config('meta.zcml', Products.GenericSetup)

    def tearDown(self):
        cleanUp()

    def testEmptyImport(self):
        zcml.load_string(EMPTY_ZCML)
        self.assertEqual(_import_step_registry._registered, {})

    def testOneStepImport(self):
        zcml.load_string(ONE_STEP_ZCML)
        self.assertEqual(_import_step_registry._registered.keys(),
            [ u'Products.GenericSetup.teststep'  ])
        info = _import_step_registry._registered[ u'Products.GenericSetup.teststep' ]
        self.assertEqual( info['description'],
                u'step description' )
        self.assertEqual( info['title'],
                u'step title' )
        self.assertEqual( info['handler'],
                'Products.GenericSetup.initialize')
        self.assertEqual( info['id'],
                u'Products.GenericSetup.teststep' )


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(ImportStepTests),
        ))

if __name__ == '__main__':
    from Products.GenericSetup.testing import run
    run(test_suite())
