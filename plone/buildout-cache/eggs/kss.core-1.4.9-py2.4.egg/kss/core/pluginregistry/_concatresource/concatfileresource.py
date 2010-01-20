'''\

Support for concatenation and compression of resources

We concatenate first and compress afterwards, giving a better
chance for the compressor to optimize
'''

from zope.interface import implements
from interfaces import IContextFile
# we are aliased to Products, hence the following absolute import
from concatresource.interfaces import IConcatResourceAddon
from fileresource import File
from compression import compress
import time
import zope.component
try:
    from zope.component.interfaces import ComponentLookupError
except ImportError:
    # Zope < 2.10
    from zope.component.exceptions import ComponentLookupError

class ConcatFiles(object):
    '''A resource that concatenates files and compresses the result

    It is also possible to extend the statically given list via
    a utility.
    '''
    implements(IContextFile)

    def __init__(self, pathlist, name, compress_level, caching, lmt_check_period):
        # Path is now a list.
        assert isinstance(pathlist, (list, tuple))
        # check all files, just to raise error if don't exist
        for path in pathlist:
            file(path, 'rb').close()
        #
        self.pathlist_base = pathlist
        self.__name__ = name
        self.compress_level = compress_level
        self.caching = caching
        self.lmt_check_period = lmt_check_period
        # markers for pathlist modification
        self.pathlist = []
        self.fileslist_changed = None
        self.fileslist = []

    def getPathList(self):
        'Gets the extended pathlist'
        # we allow the list to be extended via an utility
        try:
            registry = zope.component.getUtility(IConcatResourceAddon, self.__name__)
        except ComponentLookupError:
            extend = []
        else:
            extend = registry.getAddonFiles()
        pathlist = self.pathlist_base + extend
        return pathlist

    def getFilesList(self):
        'Gets the list of files'
        ## # XXX We have two choices:
        ## # 1. We only calculate the list once, on startup
        ## # that is, we suppose that the file resource is
        ## # called up after the extension reg has been finished
        ## # and that it never changes later.
        ## # 2. but it also could be like this to allow changes later:
        pathlist = self.getPathList()
        if pathlist != self.pathlist:
        ##if not self.pathlist:
            ##pathlist = self.getPathList()
            # mark pathlist modification
            self.pathlist = pathlist
            self.fileslist_changed = time.time()
            fileslist = self.fileslist = [File(path, self.__name__) for path in pathlist]
        else:
            fileslist = self.fileslist
        return fileslist

    def getLastMod(self):
        # We take in consideration that the pathlist
        # itself could have changed too.
        return max([f.getLastMod() for f in self.getFilesList()] +
            [self.fileslist_changed])

    def getContents(self):
        fileslist = self.getFilesList()
        assert fileslist, 'Must contain at least one resource.'
        result = fileslist[0].getContents()
        content_type = result['content_type']
        data = [result['data']]
        for subres in fileslist[1:]:
            d = subres.getContents()
            # all elements must have the same content type.
            assert d['content_type'] == content_type
            data.append(d['data'])
        result['data'] = '\n'.join(data)
        result['compress_level'] = self.compress_level
        # Do compression on the result
        result['data'] = compress(**result)
        return result
