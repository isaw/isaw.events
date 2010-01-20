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
#
import unittest

import Products.Five
from Products.Five import zcml
from Testing.ZopeTestCase import FunctionalDocTestSuite

from zope import event, component
from zope.testing.cleanup import cleanUp
from zope.lifecycleevent import ObjectModifiedEvent
from zope.app.component.hooks import getSite, setHooks

from kss.core import KSSView

class TestKSSView(KSSView):

    def __call__(self):
        self.messages = []
        if getSite() == self:
            self.messages.append("I'm the current site.")
        if component.getSiteManager() == self.getSiteManager():
            self.messages.append("I have the current site manager.")
        event.notify(ObjectModifiedEvent(self.context))
        return "\n".join(self.messages)

@component.adapter(None, KSSView, ObjectModifiedEvent)
def objectModifiedThruKSSView(obj, view, event):
    view.messages.append("Event subscriber was here.")

def setUp(test=None):
    configure_zcml = '''\
    <configure
         xmlns="http://namespaces.zope.org/zope"
         xmlns:browser="http://namespaces.zope.org/browser"
         package="kss.core.tests.test_kssview_functional">
      <browser:page
          for="*"
          name="testkssview"
          class=".TestKSSView"
          permission="zope.Public"
          />
      <subscriber handler=".objectModifiedThruKSSView" />
    </configure>'''
    zcml.load_config('configure.zcml', Products.Five)
    zcml.load_string(configure_zcml)
    setHooks()

def tearDown(test=None):
    cleanUp()

def ftest_kssview():
    """
    Let's verify that a KSSView actually is the current site when it's
    being traversed to.  Also, let's make sure that if in the course
    of this view, an object event is fired, the view will dispatch to
    KSS-specific subscribers:
    
      >>> from Products.Five.testbrowser import Browser
      >>> browser = Browser('http://localhost:8080/testkssview')
      >>> print browser.contents
      I'm the current site.
      I have the current site manager.
      Event subscriber was here.
    """

def test_suite():
    return unittest.TestSuite([
        FunctionalDocTestSuite(setUp=setUp, tearDown=tearDown),
        ])
