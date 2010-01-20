
from kss.demo.interfaces import (
    IKSSDemoResource,
    IKSSSeleniumTestResource,
    )
from kss.demo import (
    KSSSeleniumTestSuite,
    KSSSeleniumTestDirectory,
    KSSSeleniumTestLayerBase,
    KSSSeleniumSandboxCreationTestCase,
    KSSSeleniumTestCase,
    KSSDemo,
    )
from zope.interface import implements



#
# XXX Important message to developers
#
# Dear Developer! Do _not_ use the setup you see below as an example
# for your own programs, or otherwise you will need to change
# it later. The test suite creation interface will change in
# the next kss.demo versions. The plugin class (PloneDemos) 
# will change in the next major KSS (and possibly Plone) version. 
# This configuration file will be kept up-to-date to these changes.
#
# It is safe, however, to fix existing tests or drop new
# tests in the directories set up below.
#


# Create a mesh of provided interfaces
# This is needed, because an utility must have a single interface.
class IResource(IKSSDemoResource, IKSSSeleniumTestResource):
    pass


class PloneSiteLayer(KSSSeleniumTestLayerBase):
    setup = KSSSeleniumSandboxCreationTestCase('@@kss_test_create_site')

class LoggedInManagerLayer(PloneSiteLayer):
    setup = KSSSeleniumTestCase('log-in-manager.html')
    teardown = KSSSeleniumTestCase('log-out.html')

class LoggedInUserLayer(PloneSiteLayer):
    setup = KSSSeleniumTestCase('log-in-user.html')
    teardown = KSSSeleniumTestCase('log-out.html')

class PloneDemos(object):
    implements(IResource)

    demos = (
        KSSDemo('plone.app.kss', '', "follow-link.html", "Follow link action"),
        )

    selenium_tests = (
        KSSSeleniumTestSuite(
            tests = KSSSeleniumTestDirectory('selenium_tests/run_as_anonymous'),
            layer = PloneSiteLayer,
            component = 'plone.app.kss',
            application = 'Plone',
            ),
        KSSSeleniumTestSuite(
            tests = KSSSeleniumTestDirectory('selenium_tests/run_as_testuser'),
            layer = LoggedInUserLayer,
            component = 'plone.app.kss',
            application = 'Plone',
            ),
        KSSSeleniumTestSuite(
            tests = KSSSeleniumTestDirectory('selenium_tests/run_as_testmanager'),
            layer = LoggedInManagerLayer,
            component = 'plone.app.kss',
            application = 'Plone',
            ),

        # these are the plugin tests
        # but for now we put them into the application suite
        KSSSeleniumTestSuite(
            tests = KSSSeleniumTestDirectory('selenium_tests/plugin'),
            component = 'plone.app.kss',
            application = 'Plone',
            ),
        )
