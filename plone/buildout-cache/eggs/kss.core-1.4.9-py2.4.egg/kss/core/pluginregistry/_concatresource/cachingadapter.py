from time import time
from interfaces import ICachedResource
from zope.interface import implements

try:
    from zope.datetime import rfc1123_date
except ImportError:
    # Zope < 2.10
    from zope.app.datetimeutils import rfc1123_date


class CachedResource(object):
    'Adapts a ContextFile to a cached resource'
    implements(ICachedResource)

    def __init__(self, context):
        self.context = context
        self.lmt_last_checked = 0
        self.data_last_fetched = 0
    
    def _fetchdata(self):
        try:
            result = self._contents
            ##print "*****Resource from cached"
        except AttributeError:
            result = self._contents = self.context.getContents()
            self.data_last_fetched = time()
            ##print "*****Resource kooked"
        return result

    def _deldata(self):
        del self._contents

    def purgeData(self):
        'Force file contents to be reloaded'
        ##print "***** PURGE", self.context.__name__
        try:
            self._deldata()
        except AttributeError:
            pass

    # Once fetched, data is cached in the object until
    # explicitely deleted.
    data = property(lambda self: self._fetchdata()['data'], None, _deldata)
    content_type = property(lambda self: self._fetchdata()['content_type'], None, _deldata)

    # Last modified time is calculated on demand
    # but never more often then lmt_check_period
    def _fetchlm(self):
        now = time()
        if now - self.lmt_last_checked > self.lmt_check_period:
            self.lmt_last_checked = now
            lmt = float(self.context.getLastMod()) or now
            lmh = rfc1123_date(lmt)
            d = self._last_mod = dict(lmt = lmt, lmh = lmh)
            ##print "***** LMT reread", d
        else:
            d = self._last_mod
        return d
            
    lmt = property(lambda self: self._fetchlm()['lmt'])
    lmh = property(lambda self: self._fetchlm()['lmh'])

    caching = property(lambda self: self.context.caching)
    lmt_check_period = property(lambda self: self.context.lmt_check_period)
