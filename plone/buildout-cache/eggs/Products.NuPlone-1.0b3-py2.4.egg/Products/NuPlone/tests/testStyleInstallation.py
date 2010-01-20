#
# Unit Tests for the style install and uninstall methods
#

import os, sys

from Products.PloneTestCase import PloneTestCase
from Products.CMFCore.utils import getToolByName

PloneTestCase.installProduct("NuPlone")
PloneTestCase.setupPloneSite(products=["NuPlone"])

class testInstall(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        """ Grab the skins, css and js tools """
        self.jstool = getToolByName(self.portal, 'portal_javascripts')
        self.csstool = getToolByName(self.portal, 'portal_css')
        self.skinstool = getToolByName(self.portal, 'portal_skins')

    def testSkinSelectionCreated(self):
        """ Check if the new skin is in portal_skins. """
        self.failUnless("NuPlone" in self.skinstool.getSkinSelections())
    
    def testSkinSelection(self):
        """ Check if the new skin has been set as the default. """
        self.assertEqual(self.skinstool.getDefaultSkin(), "NuPlone")

    def testCustomCSSAdded(self):
        """Check that a list of CSS files have been added"""
        cssfiles = ["nuplone.css"] # Examples are ["++resource++plonetheme.example/test.css"]
        for resource in self.csstool.getResources():
            try:
                cssfiles.remove(resource.getId())
            except ValueError:
                pass
        self.failUnless(len(cssfiles) == 0)
            
    def testRTLShouldHaveHigherPrecedence(self):
        installedStylesheetIds = self.csstool.getResourceIds()
        indexRTLStylesheet = self.csstool.getResourcePosition('RTL.css')
        comes_before = ['nuplone.css',]
        for cb in comes_before:
            self.failUnless(cb in installedStylesheetIds[:indexRTLStylesheet], cb)
        
    def testCustomJSAdded(self):
        """Check that a list of JS files have been added"""
        jsfiles = ["multi-resolution.js"] # Examples are ["++resource++plonetheme.example/test.css"]
        for resource in self.jstool.getResources():
            try:
                jsfiles.remove(resource.getId())
            except ValueError:
                pass
        self.failUnless(len(jsfiles) == 0)

class testUninstall(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        """ Grab the skins, css and js tools and uninstall NuPlone. """
        self.skinstool = getToolByName(self.portal, 'portal_skins')
        self.jstool = getToolByName(self.portal, 'portal_javascripts')
        self.csstool = getToolByName(self.portal, 'portal_css')
        self.qitool = getToolByName(self.portal, 'portal_quickinstaller')
        self.qitool.uninstallProducts(products=["NuPlone"])

    def testCustomCSSRemoved(self):
        """Check that a list of CSS files have been removed"""
        cssfiles = ["nuplone.css"] # Examples are ["++resource++plonetheme.example/test.css"]
        for resource in self.csstool.getResources():
            self.failIf(resource.getId() in cssfiles)

    def testCustomJSRemoved(self):
        """Check that a list of JS files have been removed"""
        jsfiles = ["multi-resolution.js"] # Examples are ["++resource++plonetheme.example/test.css"]
        for resource in self.jstool.getResources():
            self.failIf(resource.getId() in jsfiles)

    def testProductUninstalled(self):
        """Test if the product was uninstalled."""
        self.failIf(self.qitool.isProductInstalled("NuPlone"))

    def testSkinSelectionDeleted(self):
        """Test if the skin selection was removed from portal_skins."""
        skin_selections = self.skinstool.getSkinSelections()
        self.failIf("NuPlone" in skin_selections)
    
    def testNoPathsRemain(self):
        """Checks that all directory views in portal_skins do not depend on this product"""
        for directory in self.skinstool.objectValues():
            self.failIf(directory.getDirPath().startswith("Products.NuPlone:"))
        
    def testDefaultSkinChanged(self):
        """Test if default skin is no longer NuPlone"""
        default_skin = self.skinstool.getDefaultSkin()
        self.failUnless(default_skin != 'NuPlone')


if __name__ == '__main__':
    framework()
else:
    import unittest
    def test_suite():
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(testInstall))
        suite.addTest(unittest.makeSuite(testUninstall))
        return suite
