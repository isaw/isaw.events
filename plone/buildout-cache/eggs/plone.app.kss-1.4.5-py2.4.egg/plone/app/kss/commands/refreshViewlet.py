from zope.deprecation import deprecate
from kss.core import CommandSet
from zope.viewlet.interfaces import IViewlet
from zope.component import getMultiAdapter

# XXX: This is deprecated and will be removed in Plone 4.0. Use the 'zope'
# command set instead.
class KSSRefreshViewlet(CommandSet):
    """
    Refresh a viewlet
    """

    @deprecate("The 'refreshviewlet' command set is deprecated and will be removed in Plone 4.0. "
               "Please use the 'zope' command set instead.")
    def refreshViewlet(self, id, manager, name):
        renderer = getMultiAdapter((self.context, self.request, self.view, manager),
                                  IViewlet,
                                  name=name)
        renderer = renderer.__of__(self.context)
        renderer.update()

        result = renderer.render()
        ksscore = self.getCommandSet('core')
        ksscore.replaceHTML(ksscore.getHtmlIdSelector(id), result)

