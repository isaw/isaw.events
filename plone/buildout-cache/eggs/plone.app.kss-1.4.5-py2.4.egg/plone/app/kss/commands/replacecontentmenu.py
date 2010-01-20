from zope.deprecation import deprecate
from kss.core.kssview import CommandSet

# XXX: This is deprecated and will be removed in Plone 4.0. Use the 'plone'
# command set instead.
class ReplaceContentMenuCommand(CommandSet):
    """Mainly exists for backward compatibility with old hooks
    """
    
    @deprecate("The 'replacecontentmenu' command set is deprecated and will be removed in Plone 4.0. "
               "Please use the 'plone' command set instead.")
    def replaceMenu(self):
        self.getCommandSet('refreshprovider').refreshProvider('plone.contentmenu', '#portal-column-content div.contentActions')
