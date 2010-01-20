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
""" GenericSetup profile metadata

$Id: metadata.py 89451 2008-08-06 16:48:46Z tseaver $
"""
import os

from utils import ImportConfiguratorBase, _getProductPath
from utils import CONVERTER, DEFAULT, KEY

METADATA_XML = 'metadata.xml'

class ProfileMetadata( ImportConfiguratorBase ):
    """ Extracts profile metadata from metadata.xml file.
    """

    def __init__( self, path, encoding=None, product=None ):

        # don't call the base class __init__ b/c we don't have (or need)
        # a site

        self._path = path
        if product is not None:
            # Handle relative paths
            try:
                product_path = _getProductPath(product)
            except ValueError:
                pass
            else:
                self._path = os.path.join(product_path, path)

        self._encoding = encoding

    def __call__( self ):
        
        full_path = os.path.join( self._path, METADATA_XML )
        if not os.path.exists( full_path ):
            return {}

        file = open( full_path, 'r' )
        return self.parseXML( file.read() )

    def _getImportMapping( self ):

        return {
            'metadata':
            {'description': { CONVERTER: self._convertToUnique },
             'version': { CONVERTER: self._convertToUnique },
             'dependencies': { CONVERTER: self._convertToUnique },
             },
            'description':
            { '#text': { KEY: None, DEFAULT: '' },
              },
            'version':
            { '#text': { KEY: None },
              },
            'dependencies':
            {'dependency': { KEY: None, DEFAULT: () },},
            'dependency':
            { '#text': { KEY: None },
              },
            }
