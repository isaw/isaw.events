from zope.deprecation import deprecate
from zope.component import getMultiAdapter
from zope.interface import alsoProvides
from kss.core import CommandSet
from plone.app.layout.globals.interfaces import IViewView
from zope.contentprovider.interfaces import IContentProvider

# XXX: This is deprecated and will be removed in Plone 4.0. Use the 'plone'
# command set instead.
class KSSRefreshContentMenu(CommandSet):
    """
    Refresh a viewlet
    """

    @deprecate("The 'contentmenu' command set is deprecated and will be removed in Plone 4.0. "
              "Please use the 'plone' command set instead.")
    def refreshContentMenu(self, id, name):
        alsoProvides(self.view, IViewView)
        contentMenu = getMultiAdapter((self.context, self.request, self.view), 
                                      IContentProvider, name=name)
        renderer = contentMenu.__of__(self.context)
        renderer.update()
        result = renderer.render()
        ksscore = self.getCommandSet('core')
        ksscore.replaceHTML(ksscore.getHtmlIdSelector(id), result)


