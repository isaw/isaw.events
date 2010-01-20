
from zope.interface import Interface
from zope.schema import Bytes, TextLine, Float

class IContextFile(Interface):

    def getLastMod(self):
        'Returns last modification time of the file'

    def getContents():
        'Reads the data and content type of the file'

class ICachedResource(Interface):
    
     data = Bytes(title = u'The content data of the file')

     content_type = TextLine(title = u'The mime content type of the file')

     lmt = Float(title = u'Last modification timestamp')
     
     lmh = Float(title = u'Last modification in human readable form')

     def purgeData(self):
         'Purges the cached data'

class IConcatResourceAddon(Interface):
    '''Utility to register addons

    This can be used to dynamically extend components for a given resource.
    We don't provide implementation for this here, but other
    components can implement this to provide dynamic add-ons.

    The name of the utility should be the name of the resource.
    '''

    def getAddonFiles(request):
        '''Returns a list of addon files.
        This will be concatenated to the end of the static list.
        '''
    
 
