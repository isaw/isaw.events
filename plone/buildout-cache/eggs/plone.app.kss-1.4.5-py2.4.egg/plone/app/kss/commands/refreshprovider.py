from zope.deprecation import deprecate
from kss.core.kssview import CommandSet
from zope.component import getMultiAdapter
from zope.contentprovider.interfaces import IContentProvider

# XXX: This is deprecated and will be removed in Plone 4.0. Use the 'zope'
# command set instead.
class RefreshProviderCommand(CommandSet):
    """Refreshes the selected provider (provides IContentProvider) named name and located
    at selector in the HTML"""

    @deprecate("The 'refreshprovider' command set is deprecated and will be removed in Plone 4.0. "
               "Please use the 'zope' command set instead.")
    def refreshProvider(self, name, selector):
        # Cleaned out all the old code pre-provider menus (supposed safe, we are in Plone 3.0)
        # Basically the code comes from jfroche's locking branch, where we get the provider
        # through adaptation and we render it. Right now a big refresh issue occurs on workflow
        # state changes
        contentMenuProvider = getMultiAdapter((self.context, self.request, self.view),
                                              IContentProvider,
                                              name=name)
        renderer = contentMenuProvider.__of__(self.context)
        renderer.update()
        result = renderer.render()
        # Command the replacement
        ksscore = self.getCommandSet('core')
        # Here we are using a replaceInner because we are binding to a selector to do that:
        # in case the provider does not want to be shown (and we have an example with the contentmenu
        # in edit tab) then the renderer might return a blank string, if we replace that normally then we
        # won't have selectors to get back!
        ksscore.replaceInnerHTML(ksscore.getCssSelector(selector), result)

