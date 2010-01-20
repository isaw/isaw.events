
from zope.schema import Text
from zope.schema.interfaces import IFromUnicode
from zope.interface import implements
import os.path

class PathList(Text):

    implements(IFromUnicode)

    def fromUnicode(self, u):
        result = []
        for u in u.split():
            if os.path.isabs(u):
                path = os.path.normpath(u)
            else:
                path = self.context.path(u)
            result.append(path)
        return result
