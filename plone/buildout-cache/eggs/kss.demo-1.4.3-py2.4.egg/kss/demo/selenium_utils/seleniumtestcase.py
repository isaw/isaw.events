import os
import unittest
import time

from selenium import selenium
try:
    browser = os.environ["SELENIUMBROWSER"]
except:
    browser = "*firefox"
try:
    target = os.environ["SELENIUMTARGET"]
except:
    target = "http://localhost:8080"


def trymanytimes(func):
    '''Decorate a test method with this to make it try for ten seconds'''
    def newfunc(*args, **kwargs):
        exc = None
        for i in range(10):
            try:
                func(*args, **kwargs)
            except Exception, e:
                exc = e
                time.sleep(1)
            else:
                return
        raise exc
    return newfunc

class SeleniumTestCase(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, browser, target)
        self.selenium.start()
        self.storedvars = {}

    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

    def __getattr__(self, name):
        try:
            return getattr(self.__dict__['selenium'], name)
        except KeyError:
            return super(SeleniumTestCase, self).__getattr__(name)

    def open(self, url):
        self.selenium.open(url)

    def click(self, target):
        self.selenium.click(target)

    @trymanytimes
    def waitForText(self, target, text):
        self.failUnless(text in self.selenium.get_text(target))

    @trymanytimes
    def waitForNotText(self, target, text):
        self.failIf(text in self.selenium.get_text(target))

    @trymanytimes
    def waitForTextPresent(self, text):
        self.failUnless(self.selenium.is_text_present(text))

    @trymanytimes
    def waitForElementNotPresent(self, target):
        self.failIf(self.selenium.is_element_present(target))

    @trymanytimes
    def waitForElementPresent(self, target):
        self.failUnless(self.selenium.is_element_present(target))

    @trymanytimes
    def waitForValue(self, target, value):
        self.failUnless(self.selenium.get_value(target))

    @trymanytimes
    def waitForAttribute(self, target, value):
        self.assertEqual(self.selenium.get_attribute(target), value)

    def assertText(self, target, text=''):
        self.assertEqual(self.selenium.get_text(target), text)

    def assertNotText(self, target, text=''):
        self.failIfEqual(self.selenium.get_text(target), text)

    def assertValue(self, target, value=''):
        self.assertEqual(self.selenium.get_value(target), value)

    def assertElementPresent(self, target):
        self.failUnless(self.selenium.is_element_present(target))

    def assertElementNotPresent(self, target):
        self.failIf(self.selenium.is_element_present(target))

    def pause(self, seconds):
        time.sleep(float(seconds)/1000)

    def assertTextPresent(self, text):
        self.failUnless(self.selenium.is_text_present(text))

    def assertTextNotPresent(self, text):
        self.failIf(self.selenium.is_text_present(text))
        
    def assertAttribute(self, target, value):
        self.assertEqual(self.selenium.get_attribute(target), value)

    def storeText(self, target, varname):
        self.storedvars[varname] = self.selenium.get_text(target)

    def getVar(self, varname):
        return self.storedvars[varname]
