'''\
Supplemental support for json plugins
'''

import os.path, logging
import zope.component as capi
from zope.interface import implements, Interface
from interfaces import IJSONStreamWriteable

logger = logging.getLogger('kss.core')

def getJsonAddonFiles():
    'Gets the addon javascript files for json'
    files = []
    # Try adding the jsonserver files
    request = getattr(capi.getSiteManager(), 'REQUEST', None)

    if request is not None:
        try:
            # use the files already registered to that concat resource
            jsonrpc = capi.getAdapter(request, Interface, 'jsonrpc.js')
        except capi.ComponentLookupError:
            pass    # JSON not present.
        else:
            # JSON present.
            files.extend(jsonrpc.context.context.getPathList())
            # add the json kukit support file
            plugins_dir = os.path.split(globals()['__file__'])[0]
            files.append(os.path.join(plugins_dir, 'browser', 'jsonkukit.js'))
            logger.info('Lazy plugin construction: Installed support for JSON-RPC transport.')
    return files

class JsonCommandView(object):
    '''View of a command for JSON requests.
    
    We siply return the commands since they
    will be transparently rendered for JSON,
    via the writer adapter hooks.
    '''
    
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def render(self):
        return self.context

class KSSCommandWriter(object):
    'Writes a command to JSON'
    implements(IJSONStreamWriteable)

    def __init__(self, context, writer):
        self.context = context
        self.writer = writer
        
    def __jsonwrite__(self):
        writer = self.writer
        # All is written as a dict
        d = dict(self.context.__dict__)
        # params are converted to a dict from a list.
        # Also get rid of "none" params that were only a hack for xml
        d['params'] = dict([(param.name, param.content) for param in d['params'] if param.name != 'none'])
        writer.write_repr(d)
