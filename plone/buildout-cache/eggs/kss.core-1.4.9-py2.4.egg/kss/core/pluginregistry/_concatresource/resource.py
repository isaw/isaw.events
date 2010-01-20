from zope.publisher.interfaces.browser import IBrowserPublisher
from zope.interface import implements
from concatfileresource import ConcatFiles
from interfaces import ICachedResource
import cachingadapter   # force adapter registration

try:
    from zope.publisher.browser import BrowserView
    from zope.datetime import time as timeFromDateTimeString
except ImportError:
    # Zope < 2.10
    from zope.app.publisher.browser import BrowserView
    from zope.app.datetimeutils import time as timeFromDateTimeString

try:
    import Products.Five
except ImportError:
    __five__ = False
    from zope.app.publisher.browser.resource import Resource
else:
    __five__ = True
    try:
        # Zope 2.8 / Five 1.0.2
        from Products.Five.resource import Resource
        __five_pre_1_3_ = True
    except ImportError:
        # Zope 2.9 / Five 1.3
        from Products.Five.browser.resource import Resource
        __five_pre_1_3__ = False

class GenericResource(BrowserView, Resource):
    """A publishable resource"""

    if __five__:
        #implements(IBrowserPublisher)

        def __browser_default__(self, request):
            return self, (request.REQUEST_METHOD,)

    else:
        implements(IBrowserPublisher)

        def publishTraverse(self, request, name):
            '''See interface IBrowserPublisher'''
            raise LookupError(name)

        def browserDefault(self, request):
            '''See interface IBrowserPublisher'''
            return getattr(self, request.method), ()

    # for unit tests
    def _testData(self):
        return self.context.data

    def chooseContext(self):
        """Choose the appropriate context"""
        return self.context

    def GET(self):
        """Default document"""

        file = self.chooseContext()
        request = self.request
        response = request.response

        # Control in-memory caching
        cache_in_memory = file.caching == 'memory'
        if cache_in_memory:
            last_mod = file.lmt
            if last_mod > file.data_last_fetched:
                # force delete file contents
                file.purgeData()

        # HTTP If-Modified-Since header handling. This is duplicated
        # from OFS.Image.Image - it really should be consolidated
        # somewhere...
        if __five__:
            header = request.get_header('If-Modified-Since')
        else:
            header = request.getHeader('If-Modified-Since', None)
        if header is not None:
            header = header.split(';')[0]
            # Some proxies seem to send invalid date strings for this
            # header. If the date string is not valid, we ignore it
            # rather than raise an error to be generally consistent
            # with common servers such as Apache (which can usually
            # understand the screwy date string as a lucky side effect
            # of the way they parse it).
            try:    mod_since=long(timeFromDateTimeString(header))
            except: mod_since=None
            if mod_since is not None:
                if not cache_in_memory:
                    last_mod = file.lmt
                if last_mod > 0 and int(last_mod) <= mod_since:
                    response.setStatus(304)
                    return ''

        response.setHeader('Content-Type', file.content_type)
        response.setHeader('Last-Modified', file.lmh)
        # Cache for one day
        response.setHeader('Cache-Control', 'public,max-age=86400')
        data = file.data

        if not cache_in_memory:
            # force delete file contents
            file.purgeData()

        return data

    def HEAD(self):
        file = self.chooseContext()
        response = self.request.response
        response.setHeader('Content-Type', file.content_type)
        response.setHeader('Last-Modified', file.lmh)
        # Cache for one day
        response.setHeader('Cache-Control', 'public,max-age=86400')
        return ''

class ResourceFactory(object):

    factory = None
    resource = None

    def __init__(self, path, name, compress_level, caching, lmt_check_period,
                resource_factory=None, checker=None):
        self.__name = name
        self.__path = path
        self.__compress_level = compress_level
        self.__caching = caching
        self.__lmt_check_period = lmt_check_period
        if resource_factory is not None:
            self.resource = resource_factory
        # z3 only
        self.__checker = checker

    def __call__(self, request):
        try:
            rsrc = self.__rsrc
        except AttributeError:
            # Delayed creation. That assures that registry is set up by this time.
            rsrc = self.__rsrc = ICachedResource(self.factory(self.__path, self.__name,
                    self.__compress_level, self.__caching, self.__lmt_check_period))
        resource = self.resource(rsrc, request)
        # z3 only
        resource.__name__ = self.__name
        if self.__checker is not None:
            # z3 only
            resource.__Security_checker__ = self.__checker
        return resource

class ConcatResourceFactory(ResourceFactory):
    """A factory for concat resources"""

    factory = ConcatFiles
    resource = GenericResource
