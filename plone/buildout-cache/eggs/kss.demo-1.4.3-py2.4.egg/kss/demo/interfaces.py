from zope.interface import Interface
from zope.schema import (
    TextLine,
    List,
    )

class ISimpleContent(Interface):
    pass

# --
# Resources
# --

class IKSSDemo(Interface):
    """Represents an actual demo page"""

    plugin_namespace = TextLine(
        title=u"plugin_namespace",
        description=u'string with the name of the plugin.'
                    u'Or: "" when it is the core part.',
        required=False,
        )

    category = TextLine(
        title=u"component",
        description=u'text that will appear as the title of the'
                    u'category. "" if out of category.',
        required=False,
        )

    page_url = TextLine(
        title=u"page_url",
        description=u'(relative) url of the demo page. This should'
                    u'traverse on ISimpleContent.',
        required=True,
        )

    title = TextLine(
        title=u"title",
        description=u'Title of the demo. This also identifies it'
                    u'for removal.',
        required=True,
        )

class IKSSSeleniumTestDirectory(Interface):
    """Represents an actual selenium test directory"""

    test_directory = TextLine(
        title=u"test directory",
        description=u'Relative directory path, contains *.html selenium tests',
        required=False,
        )

# --
# Resource definition interfaces
# --

class IKSSDemoResource(Interface):
    """An utility that a demo needs to register"""

    # list of IKSSDemo
    demos = List(
        title=u"demos",
        description=u'The ordered list of demos contained in this plugin',
        required=True,
        )

class IKSSSeleniumTestResource(Interface):
    """An utility that a demo needs to register"""

    # list of IKSSSeleniumTestDir
    selenium_tests = List(
        title=u"selenium tests",
        description=u'The list of selenium test directories contained in this plugin',
        required=True,
        )

# --
# The registry itself
# --

class IKSSDemoRegistry(Interface):
    """Faciliates registration of demos.

    Implementations must look after the IKSSDemoResource
    adapters, and use their content to set up themselves.
    """

    def registerDemo(demo):
        """Register a demo

        It has the attributes specified in IKSSDemo:

        plugin_namespace - string with the name of the plugin.
                           Or: "" when it is the core part.

        category         - text that will appear as the title of the
                           category. "" if out of category.

        demo_page        - (relative) url of the demo page. This should
                           traverse on ISimpleContent.

        title            - Title of the demo. This also identifies it
                           for removal.
        """
 
    def unregisterDemo(demo):
        """Unregister the given demo."""

    def getSortedDemos():
        """Get the (sorted) list of demos"""

class IKSSSeleniumTestRegistry(Interface):
    """Faciliates registration of demos.

    Implementations must look after the IKSSSeleniumTestResource
    adapters, and use their content to set up themselves.
    """

    def registerSeleniumTestFile(test_filename):
        """Register a selenium test directory

        It test_dir has the "filename" attributes specified in IKSSSeleniumTest.
        """
    
    def unregisterSeleniumTestFile(test_filename):
        """Unregister the given test directory."""


# --
# Event that gets redispatched, for allowing
# the listeners to filter on component
# --

class IKSSDemoRegistrationEvent(Interface):
    """Redispatched event for registration of
    IKSSDemoRegistration utilities (resources).
    """

class IKSSDemoRegistryEvent(Interface):
    """Redispatched event for registration of
    IKSSDemoRegistry utilities.
    """
