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
""" Unit tests for ProfileMetadata.

$Id: test_profile_metadata.py 89451 2008-08-06 16:48:46Z tseaver $
"""
import unittest
import os

from Testing.ZopeTestCase import ZopeTestCase
from Testing.ZopeTestCase import installProduct

from Products.GenericSetup import profile_registry
from Products.GenericSetup.metadata import ProfileMetadata

desc = 'DESCRIPTION TEXT'
version = 'VERSION'
dep1 = 'DEPENDENCY 1'
dep2 = 'DEPENDENCY 2'

_METADATA_XML = """<?xml version="1.0"?>
<metadata>
  <description>%s</description>
  <version>%s</version>
  <dependencies>
    <dependency>%s</dependency>
    <dependency>%s</dependency>
  </dependencies>
</metadata>
""" % (desc, version, dep1, dep2)

_METADATA_MAP = {
    'description': desc,
    'version': version,
    'dependencies': (dep1, dep2),
    }

_METADATA_EMPTY_DEPENDENCIES_XML = """<?xml version="1.0"?>
<metadata>
  <description>%s</description>
  <version>%s</version>
  <dependencies></dependencies>
</metadata>
""" % (desc, version)

_METADATA_MAP_EMPTY_DEPENDENCIES = {
    'description': desc,
    'version': version,
    'dependencies': (),
    }

class ProfileMetadataTests( ZopeTestCase ):

    installProduct('GenericSetup')

    def test_parseXML(self):
        metadata = ProfileMetadata( '' )
        parsed = metadata.parseXML( _METADATA_XML )
        self.assertEqual(parsed, _METADATA_MAP)

    def test_versionFromProduct(self):
        import warnings
        warnings.filterwarnings('ignore')
        try:
            profile_id = 'dummy_profile'
            product_name = 'GenericSetup'
            directory = os.path.split(__file__)[0]
            path = os.path.join(directory, 'default_profile')
            profile_registry.registerProfile( profile_id,
                                              'Dummy Profile',
                                              'This is a dummy profile',
                                              path,
                                              product=product_name)
            profile_info = profile_registry.getProfileInfo(
                                '%s:%s' % (product_name, profile_id))
            product = getattr(self.app.Control_Panel.Products, product_name)
            self.assertEqual(profile_info['version'], product.version)
        finally:
            warnings.resetwarnings()

    def test_relativePath(self):
        profile_id = 'dummy_profile2'
        product_name = 'GenericSetup'
        profile_registry.registerProfile(
            profile_id, 'Dummy Profile', 'This is a dummy profile',
            'tests/metadata_profile', product=product_name)
        profile_info = profile_registry.getProfileInfo(
            '%s:%s' % (product_name, profile_id))
        self.assertEqual(profile_info['description'],
                         'Description from metadata')

    def test_parseXML_empty_dependencies(self):
        # https://bugs.launchpad.net/bugs/255301
        metadata = ProfileMetadata( '')
        parsed = metadata.parseXML(_METADATA_EMPTY_DEPENDENCIES_XML)
        self.assertEqual(parsed, _METADATA_MAP_EMPTY_DEPENDENCIES)

def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite( ProfileMetadataTests ),
        ))

if __name__ == '__main__':
    from Products.GenericSetup.testing import run
    run(test_suite())
