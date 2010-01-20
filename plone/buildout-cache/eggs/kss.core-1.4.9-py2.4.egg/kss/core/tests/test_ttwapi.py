import unittest

from Testing import ZopeTestCase
ZopeTestCase.installProduct('PythonScripts')

from AccessControl import allow_module
allow_module('kss.core.tests.help_ttwapi')

import Products.Five.component
from Products.Five import zcml

from zope import component
from zope.lifecycleevent import ObjectModifiedEvent
from zope.app.component.hooks import setHooks

from kss.core import KSSView
from kss.core.tests.base import KSSViewTestCase

class TTWTestCase(KSSViewTestCase):

    class layer(KSSViewTestCase.layer):
        @classmethod
        def setUp(cls):
            configure_zcml = '''\
            <configure
                 xmlns="http://namespaces.zope.org/zope"
                 xmlns:browser="http://namespaces.zope.org/browser"
                 package="kss.core.tests.test_ttwapi">
              <subscriber handler=".objectModifiedThruKSSView" />
            </configure>'''
            zcml.load_string(configure_zcml)

    def afterSetUp(self):
        KSSViewTestCase.afterSetUp(self)
        setHooks()
        self.app.manage_addProduct['PythonScripts'].manage_addPythonScript(
            'kss_test')
        self.setDebugRequest()

    def test_scriptWithCore(self):
        pythonScriptCode = '''
from kss.core.ttwapi import startKSSCommands
from kss.core.ttwapi import getKSSCommandSet
from kss.core.ttwapi import renderKSSCommands
startKSSCommands(context, context.REQUEST)
core = getKSSCommandSet('core')
core.replaceInnerHTML('#test', '<p>Done</p>')
return renderKSSCommands()
'''
        self.app.kss_test.ZPythonScript_edit('', pythonScriptCode)
        result = self.app.kss_test() 
        self.assertEquals(len(result), 1)
        command = result[0]
        self.assertEquals(command['selector'], '#test')
        self.assertEquals(command['name'], 'replaceInnerHTML')

    def test_scriptWithEffect(self):
        pythonScriptCode = '''
from kss.core.ttwapi import startKSSCommands
from kss.core.ttwapi import getKSSCommandSet
from kss.core.ttwapi import renderKSSCommands
startKSSCommands(context, context.REQUEST)
commandSet = getKSSCommandSet('effects')
commandSet.effect('#test', 'fade')
return renderKSSCommands()
'''
        self.app.kss_test.ZPythonScript_edit('', pythonScriptCode)
        result = self.app.kss_test() 
        self.assertEquals(len(result), 1)
        command = result[0]
        self.assertEquals(command['selector'], '#test')
        self.assertEquals(command['name'], 'effect')
        self.assertEquals(command['params']['type'], 'fade')

    def test_scriptWithEvents(self):
        pythonScriptCode = '''
from kss.core.ttwapi import startKSSCommands
from kss.core.ttwapi import getKSSCommandSet
from kss.core.ttwapi import renderKSSCommands
from kss.core.tests.help_ttwapi import objectModified
startKSSCommands(context, context.REQUEST)
core = getKSSCommandSet('core')
core.replaceInnerHTML('#test', '<p>Done</p>')
objectModified(context)
return renderKSSCommands()
'''
        self.app.kss_test.ZPythonScript_edit('', pythonScriptCode)
        result = self.app.kss_test()
        self.assertEquals(len(result), 2)
        command = result[0]
        self.assertEquals(command['selector'], '#test')
        self.assertEquals(command['name'], 'replaceInnerHTML')
        command = result[1]
        self.assertEquals(command['selector'], '#event')
        self.assertEquals(command['name'], 'replaceInnerHTML')

@component.adapter(None, KSSView, ObjectModifiedEvent)
def objectModifiedThruKSSView(obj, view, event):
    view.getCommandSet('core').replaceInnerHTML(
        "#event", "Event subscriber was here.")

def test_suite():
    suites = []
    suites.append(unittest.makeSuite(TTWTestCase))
    return unittest.TestSuite(suites)
