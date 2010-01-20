
from kss.demo.interfaces import IKSSDemoRegistry
from zope.publisher.interfaces.browser import IBrowserPublisher
from zope.publisher.interfaces import NotFound
from zope.component import getUtility
from zope.interface import implements
from kss.demo.selenium_utils.builder import cookSeleniumTests
import os.path
try:
    from Products.Five import BrowserView
    BrowserView         # make pyflakes happy
except ImportError:
     from zope.publisher.browser import BrowserView

class KSSDemoRegistryView(BrowserView):

    def getSortedDemos(self):
        """Get demos"""
        registry = getUtility(IKSSDemoRegistry)
        return registry.getSortedDemos()

    def getDemoGroups(self):
        """Get demos groupped by plugin_namespace, category"""
        demo_groups = []
        prev_plugin_namespace, prev_category = None, None
        group = None
        for demo in self.getSortedDemos():
            plugin_namespace = demo['plugin_namespace']
            category =  demo['category']
            # Set a flag on first rows in group, 
            # since z3 seems not to  handle rpeeat(..).first()
            # These will be used for grouping
            if prev_plugin_namespace != plugin_namespace:
                is_first_plugin_namespace = True
                prev_plugin_namespace = plugin_namespace
            else:
                is_first_plugin_namespace = False
            if prev_category != category:
                is_first_category = True
                prev_category = category
            else:
                is_first_category = False
            # If plugin_namespace or category changed, time to
            # start a new group.
            if is_first_plugin_namespace or is_first_category:
                # Start a new group.
                group = []
                demo_groups.append(dict(
                    plugin_namespace = plugin_namespace,
                    category = category,
                    demos = group,
                    is_first_plugin_namespace = is_first_plugin_namespace,
                    is_first_category = is_first_category,
                    ))
            # In any case append our demo to the group
            group.append(demo)
        return demo_groups

    @staticmethod
    def _filename_to_title(filename):
        """Automatic conversion of filename to readable title"""
        if filename.lower().endswith('.html'):
            filename = filename[:-5]
        elif filename.lower().endswith('.htm'):
            filename = filename[:-4]
        words = os.path.basename(filename).split('_')
        # if the first word is a number: it is ignored in the title
        # This can be used to somelimited ordering, since filenames
        # are listed in alphabetical order, ie. 00_xxx.html will come first.
        if not words[0] or '0' <= words[0][0] <= '9':
            words = words[1:]
        # Compile the result.
        result = ' '.join([word.capitalize() for word in words])
        return result

    @staticmethod
    def _filename_to_href(filename):
        """Automatic conversion of filename to publication href"""
        return "@@resource?filename=%s" % (filename, )

    def getSeleniumTests(self):
        """Get selenium tests annotated with title and href."""
        return [dict(
                    href = self._filename_to_href(filename),
                    title=self._filename_to_title(filename),
                    )
                    for filename in self.selenium_test_filenames]

    @property
    def selenium_test_filenames(self):
        """A cached representation of all filenames."""
        try:
            return self._cooked_selenium_test_filenames
        except AttributeError:
            registry = getUtility(IKSSDemoRegistry)
            self._cooked_selenium_test_filenames =  filenames = \
                    registry.selenium_tests
            return filenames

    def getSeleniumTestResource(self, filename):
        """Return the html resource, whose absolute filename is given,"""
        # First of all, let's check if this is one of our file.
        # (Refuse otherwise - we don't want access to all files on the server.)
        if filename not in self.selenium_test_filenames:
            raise Exception, "Nonexistent resource"
        # Return the file's content.
        self.request.response.setHeader('Content-type', 'text/html;charset=utf-8')
        return file(filename).read()

    def getZuiteHomePage(self):
        """Redirects to the Zuite home page, Zuite object is found from path."""
        zuite = self.getZuite()
        html = "%s/core/TestRunner.html?test=%s/suite.html" % (zuite.absolute_url(), self.context.absolute_url())
        return self.request.response.redirect(html)

    def getZuite(self):
        """Finds a zuite in the same directory or under"""
        if not hasattr(self, 'zuites'):
            container = self.context.aq_inner.aq_parent
            self.zuites = self.context.ZopeFind(container, obj_metatypes=['Zuite'], search_sub=1)
        if self.zuites:
            return self.zuites[0][1]
        else:
            return None

class KSSDemoRegistryAdminView(BrowserView):
    """Things that only admin should do"""
    implements(IBrowserPublisher)

    # Zope3 requires the implementation of
    # IBrowserPublisher, in order for the methods
    # to be traversable.
    #
    # An alternative would be:
    # <browser:pages class="...">
    #   <page name="..." attribute="..." />
    #   <page name="..." attribute="..." />
    # </browser:pages>

    def publishTraverse(self, request, name):
        try:
            return getattr(self, name)
        except AttributeError:
            raise NotFound(self.context, name, request)

    def browserDefault(self, request):
        # make ui the default method
        return self, ('cookSeleniumTests', )

    # --
    # Accessable methods
    # --

    def cookSeleniumTests(self):
        """Cook selenium tests

        The *.html tests from each plugin are produced
        into the file seltest_all.pty in the directory
        of kss.demo.selenium_utils .
        """
        registry = getUtility(IKSSDemoRegistry)
        filenames = registry.selenium_tests
        # Cook them. This will create seltest_all.py. 
        cookSeleniumTests(filenames)
        # We are done.
        return "Selenium tests cooked OK. (%i)" % (len(filenames), )
