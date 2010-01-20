'''\
this is a fixture of zope app's fileresource

It correctly handles cache expiration headers and rereads
files when needed only.
'''

from zope.interface import implements
try:
    from zope.contenttype import guess_content_type
except ImportError: # BBB: Zope < 2.10
    try:
        # XXX ??? What zope version needs this?
        from zope.app.contenttypes import guess_content_type
    except ImportError:
        from zope.app.content_types import guess_content_type

import os
from interfaces import IContextFile

class File(object):
    implements(IContextFile)

    def __init__(self, path, name):
        self.path = path
        self.__name__ = name

    def getLastMod(self):
        return os.path.getmtime(self.path)

    def getContents(self):
        ##print "***** READ", self.path
        f = open(self.path, 'rb')
        data = f.read()
        f.close()
        content_type, enc = guess_content_type(self.path, data)
        return dict(data = data, content_type = content_type)

class Image(File):
    """Image objects stored in external files."""

    def getContents(self):
        d = super(Image, self).getContens()
        if d ['content_type'] in (None, 'application/octet-stream'):
            ext = os.path.splitext(self.path)[1]
            if ext:
                d['content_type'] = 'image/%s' % ext[1:]
        return d
