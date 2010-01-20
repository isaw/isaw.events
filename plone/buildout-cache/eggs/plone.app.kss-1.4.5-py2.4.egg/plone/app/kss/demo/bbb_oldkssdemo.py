

# XXX future BBB
# Provide a way for the old kss.demo version, not to fail
# with import error - even if it cannot execute these tests.
# This enables that the package can contain application level
# test setup, but it still does not fail with the old version.
try:
    import kss.demo
    from kss.demo import (
        KSSSeleniumTestDirectory,
        KSSDemo,
        KSSSeleniumTestCase,
        KSSSeleniumTestSuite,
        KSSSeleniumTestLayerBase,
        KSSSeleniumSandboxCreationTestCase,
        )
except ImportError:
    # nonexistent constructs. They will not work, but
    # they will run without errors.
    class Fake(object):
        # test_directory is needed because the caller code
        # will treat us as a TestDirectory. So, we give a
        # directory that does not contain any *.html files.
        test_directory = '/'
        def __init__(self, *arg, **kw):
            pass
    #
    import kss.demo.resource
    # Provide the classes directly on kss.demo namespace
    kss.demo.KSSSeleniumTestDirectory = kss.demo.resource.KSSSeleniumTestDirectory
    kss.demo.KSSDemo = kss.demo.resource.KSSDemo
    kss.demo.KSSSeleniumTestCase = Fake
    kss.demo.KSSSeleniumTestSuite = Fake
    kss.demo.KSSSeleniumTestLayerBase = Fake
    kss.demo.KSSSeleniumSandboxCreationTestCase = Fake
