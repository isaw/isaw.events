from zope.interface import implements
from interfaces import (
    IKSSDemo,
    IKSSSeleniumTestDirectory,
    )

# --
# Reference implementations for the described elements
# They are designed to be passive
# --

class KSSDemo(object):
    """Represents a demo.
    """
    implements(IKSSDemo)
    def __init__(self, plugin_namespace, category, page_url, title, description=None, helpfile=None, packageName=None):
        self.plugin_namespace = plugin_namespace
        self.category = category
        self.page_url = page_url
        self.title = title
        self.description = description
        if not packageName:
            helpfile = None
        self.helpfile = helpfile
        self.packageName = packageName

    # convenience access for page templates
    __allow_access_to_unprotected_subobjects__ = 1
    def __getitem__(self, key):
        return getattr(self, key)

class KSSSeleniumTestDirectory(object):
    """Represents a selenium test directory.
    """
    implements(IKSSSeleniumTestDirectory)
    def __init__(self, test_directory):
        self.test_directory = test_directory

    # convenience access for page templates
    __allow_access_to_unprotected_subobjects__ = 1
    def __getitem__(self, key):
        return getattr(self, key)


