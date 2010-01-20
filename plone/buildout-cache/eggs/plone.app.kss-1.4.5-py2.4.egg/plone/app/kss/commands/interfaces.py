from zope.interface import Interface

# Note: We have two basic command sets here - 'zope', for basic Zope 
# operations like refreshing viewlets and content providers, and 'plone'
# for core Plone functionality relating to status messages, portlets
# and the content menu.
# 
# Please be careful before dumping more things into these interfaces. It
# may be more appropriate to register a new command set for specific
# commands.

class IZopeCommands(Interface):
    """Commands for basic Zope-like operations.
    
    Registered as command set 'zope'
    """
    
    def refreshProvider(selector, name):
        """Refresh any IContentProvider named 'name' located in the page
        at 'selector'.
        
        This can be used to refresh an entire viewlet manager.
        """
    
    def refreshViewlet(selector, manager, name):
        """Refresh any IViewlet named 'name' inside the 
        IViewletManager 'manager', located in the page at
        'selector'.
        
        The 'manager' can be the name of a manager, in which case it's
        looked up, or an actual IViewletManager instance.
        """
        
class IPloneCommands(Interface):
    """Commands for basic Plone operations.
    
    Registered as command set 'plone'
    """
    
    def issuePortalMessage(message, msgtype='info'):
        """Issue a particular portal message. Type can be 'info', 'warn'
        or 'error'.
        """

    def refreshPortlet(portlethash, **kw):
        """Refresh a new-style portlet. The portlet hash is encoded in the
        standard view template as a KSS parameter. It can also be calculated
        using the functions in plone.portlets.utils. 
        
        Any keyword arguments are added as if they were form request
        parameters for the portlet to parse.
        """

    def refreshContentMenu():
        """Refresh the content menu
        """

class IPloneLegacyCommands(Interface):
    """Commands for legacy Plone operations.
    JS code done without KSS patterns

    registered as command set 'plone-legacy'
    """
    
    def createTableOfContents():
        """Parse the document body and add the TOC
        """

# Deprecated commands -- will be removed in Plone 4.0
# Do not use these.

class IIssuePortalMessageCommand(Interface):
    """Commands to issue portal status messages.
    
    Registered as command set 'portalmessage'
    """
    
    def issuePortalMessage(message, msgtype='info'):
        """Issue a particular portal message. Type can be any string, but
        'info', 'warning' and 'error' have default styles associated with them.
        """

class IRefreshPortletCommand(Interface):
    """Commands to refresh portlets
    
    Registered as command set 'refreshportlet'
    """
    
    def refreshPortlet(portlethash, **kw):
        """Refresh a new-style portlet. The portlet hash is encoded in the
        standard view template as a KSS parameter. It can also be calculated
        using the functions in plone.portlets.utils. 
        
        Any keyword arguments are added as if they were form request
        parameters for the portlet to parse.
        """

class IKSSRefreshViewlet(Interface):
    """Commands to refresh viewlets
    
    Registered as command set 'refreshviewlet'
    """
    
    def refreshViewlet(id, manager, name):
        """Refresh the viewlet at the given node id, found in the given
        IViewletManager, with the given name.
        
        To find a viewlet manager, you'll need to use getMultiAdapter()
        on a context, request and view, providing IViewletManager with a
        partcular name.
        """

class IRefreshProviderCommand(Interface):
    """Refresh a content provider (i.e. something given with a provider:
    expression).
    
    Registered as command set 'refreshprovider'
    """
    
    def refreshProvider(name, selector):
        """Refresh any IContentProvider named <name> located in the page
        at <selector> (css selector)
        """

class IReplaceContentMenuCommand(Interface):
    """Refresh the content menu (the green bar).
    
    Registered as command set 'replacecontentmenu'
    """
    
    def replaceMenu():
        """Refresh content menu
        """

class IKSSRefreshContentMenu(Interface):
    '''Utility command for refreshing a content menu
    '''

class IKSSPlonePortletCommands(Interface):
    '''These are utility commands for doing stuff with portlets'''

    def reload_classic_portlet(css_selector, column,
                               template, portlet_macro='portlet'):
        '''Reload an old-school portlet'''
