from zope.interface import implements
from zope.component import getMultiAdapter

from zope.contentprovider.interfaces import IContentProvider
from zope.viewlet.interfaces import IViewletManager
from zope.viewlet.interfaces import IViewlet

from kss.core import CommandSet
from interfaces import IZopeCommands

class ZopeCommands(CommandSet):
    implements(IZopeCommands)
    
    def refreshProvider(self, selector, name):
        provider = getMultiAdapter((self.context, self.request, self.view),
                                    IContentProvider, name=name)
        renderer = provider.__of__(self.context)
        
        renderer.update()
        result = renderer.render()

        ksscore = self.getCommandSet('core')
        ksscore.replaceHTML(selector, result)
    
    def refreshViewlet(self, selector, manager, name):
        
        if isinstance(manager, basestring):
            manager = getMultiAdapter((self.context, self.request, self.view,),
                                      IViewletManager, name=manager)
        
        renderer = getMultiAdapter((self.context, self.request, self.view, manager),
                                   IViewlet, name=name)
        renderer = renderer.__of__(self.context)
        
        renderer.update()
        result = renderer.render()
        
        ksscore = self.getCommandSet('core')
        ksscore.replaceHTML(selector, result)