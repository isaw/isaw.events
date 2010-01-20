# -*- coding: latin-1 -*-
# Copyright (c) 2005-2007
# Authors: KSS Project Contributors (see docs/CREDITS.txt)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.

from textwrap import dedent

import warnings
from Testing.ZopeTestCase import ZopeTestCase, FunctionalTestCase

from zope import interface
from zope.publisher.interfaces.browser import IBrowserRequest
#from zope.app.testing import placelesssetup

import kss.core
from kss.core import KSSView

class KSSCoreLayer:
    @classmethod
    def setUp(cls):
        try:
            import Products.Five
        except ImportError:
            # probably zope 3
            pass
            # XXX TODO fix this?? --- never run yet on Z3
            from zope.configuration.xmlconfig import XMLConfig
            XMLConfig('tests/configure-unittest.zcml', kss.core)()
        else:
            from Products.Five.zcml import load_string, load_config
            load_config('meta.zcml', package=Products.Five)

            try:
                load_config('traversing.zcml', package=Products.Five)
            except IOError:
                # Let's try the Zope 2.9 way (zope.app.traversing is
                # moved in 2.10)
                load_string(dedent('''\
                <configure xmlns="http://namespaces.zope.org/zope"
                           xmlns:five="http://namespaces.zope.org/five">
                  <include package="zope.app.traversing" />
                  <adapter
                       for="*"
                       factory="Products.Five.traversable.FiveTraversable"
                       provides="zope.app.traversing.interfaces.ITraversable"
                       />
                   <adapter
                       for="*"
                       factory="zope.app.traversing.adapters.Traverser"
                       provides="zope.app.traversing.interfaces.ITraverser"
                       />
                </configure>'''))
            # Load the permissions config, if it's there
            try:
                load_config('permissions.zcml', package=Products.Five)
            except IOError:
                # Zope 2.10 / Five 1.3.6 does not have it
                pass
            load_config('configure-unittest.zcml', package=kss.core.tests)

    @classmethod
    def tearDown(cls):
        pass # placelesssetup.tearDown()
    

class KSSLayer(KSSCoreLayer):
    @classmethod
    def setUp(cls):
        try:
            from Products.Five.zcml import load_config
        except ImportError:
            raise ImportError("KSSLayer requires Five to be installed.")
        load_config('meta.zcml', package=kss.core)
        load_config('configure.zcml', package=kss.core)

# Test view
class TestView(KSSView):
    def testMethod(self):
        'Yes.'

# Debug request
# This has a modified render.

class IDebugRequest(IBrowserRequest):
    'The debug request'

class KSSViewTestCaseMixin:

    def loadCoreConfig(self, kss_core=True):
        warnings.warn(
            "KSS tests are now using layers.  Please do not use "
            "loadCoreConfig anymore.",
            DeprecationWarning)
    
    def createView(self):
        "Set up a fake view (with no content)"
        self.view = self.folder.restrictedTraverse('testMethod')
        return self.view

    def setDebugRequest(self):
        'commands will be rendered as test friendly data structures'
        request = self.folder.REQUEST
        interface.directlyProvides(
            request,
            interface.directlyProvidedBy(request) + IDebugRequest)

class KSSViewTestCase(ZopeTestCase, KSSViewTestCaseMixin):
    layer = KSSLayer

class KSSViewFunctionalTestCase(FunctionalTestCase, KSSViewTestCase):
    'Functional test base'

# backward compatibility
class AzaxViewTestCase(KSSViewTestCase):
    def __init__(self, *args, **kw):
        message = "'AzaxViewTestCase' is deprecated," \
            "use 'KSSViewTestCase'- KSS uppercase instead."
        warnings.warn(message, DeprecationWarning, 2)
        KSSViewTestCase.__init__(self, *args, **kw)

class KssViewTestCase(KSSViewTestCase):
    def __init__(self, *args, **kw):
        message = "'KssViewTestCase' is deprecated," \
            "use 'KSSViewTestCase'- KSS uppercase instead."
        warnings.warn(message, DeprecationWarning, 2)
        KSSViewTestCase.__init__(self, *args, **kw)

class KssViewFunctionalTestCase(KSSViewFunctionalTestCase):
    def __init__(self, *args, **kw):
        message = "'KssViewFunctionalTestCase' is deprecated," \
            "use 'KSSViewFunctionalTestCase'- KSS uppercase instead."
        warnings.warn(message, DeprecationWarning, 2)
        KSSViewFunctionalTestCase.__init__(self, *args, **kw)



