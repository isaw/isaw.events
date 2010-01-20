from zope.interface import implements
from zope.component import getMultiAdapter, getUtility
from zope.i18n import translate
from zope.i18nmessageid.message import Message as i18nmessage

from Products.statusmessages.message import Message

from plone.portlets.interfaces import IPortletManager, IPortletRenderer
from plone.portlets.utils import unhashPortletInfo

from plone.app.portlets.interfaces import IDeferredPortletRenderer
from plone.app.portlets.utils import assignment_from_key

from kss.core import CommandSet
from interfaces import IPloneCommands

class PloneCommands(CommandSet):
    implements(IPloneCommands)
    
    def issuePortalMessage(self, message, msgtype='info'):
        if message is None:
            message = ''

        if isinstance(message, Message):
            msgtype = message.type
            # The translation domain of the message is not known.  We
            # can only assume that it is 'plone'.
            message = translate(message.message, domain='plone',
                                context=self.request)
        elif isinstance(message, i18nmessage):
            # Here the message has a domain itself, which is good.
            message = translate(message, context=self.request)

        # The 'dt' of the definition list we generate should contain
        # something like Info, Warning or Error.  Those messages are
        # available in the plone domain.
        msgtype_name = translate(msgtype.capitalize(), domain='plone',
                                 context=self.request)

        # XXX The macro has to take in account that there might be more than
        # one status message.
        ksscore = self.getCommandSet('core')
        selector = ksscore.getHtmlIdSelector('kssPortalMessage')

        # We hide the standard Plone Portal Message
        standard_portal_message_selector = ksscore.getCssSelector('.portalMessage')
        ksscore.setStyle(standard_portal_message_selector, 'display','none')

        # Now there is always a portal message but it has to be
        # rendered visible or invisible, accordingly
        html = '<dt>%s</dt><dd>%s</dd>' % (msgtype_name, message)
        ksscore.replaceInnerHTML(selector, html)
        ksscore.setAttribute(selector, 'class', "portalMessage %s" % msgtype)
        ksscore.setStyle(selector, 'display', message and 'block' or 'none')

    def refreshPortlet(self, portlethash, **kw):
        # put parameters on the request, by saving the original context
        self.request.form, orig_form = kw, self.request.form
        
        # Prepare the portlet and render the data
        info = unhashPortletInfo(portlethash) 
        manager = getUtility(IPortletManager, info['manager'])
        
        assignment = assignment_from_key(context = self.context, 
                                         manager_name = info['manager'], 
                                         category = info['category'],
                                         key = info['key'],
                                         name = info['name'])
        renderer = getMultiAdapter(
                (self.context, self.request, self.view, manager, assignment.data),
                IPortletRenderer
            )
        renderer = renderer.__of__(self.context)
        
        renderer.update()
        if IDeferredPortletRenderer.providedBy(renderer):
            # if this is a deferred load, prepare now the data
            renderer.deferred_update()
        result = renderer.render()
        
        # Revert the original request
        self.request.form = orig_form
        
        # Command the replacement
        wrapper_id = 'portletwrapper-%s' % portlethash
        ksscore = self.getCommandSet('core')
        ksscore.replaceInnerHTML(ksscore.getHtmlIdSelector(wrapper_id), result)

    def refreshContentMenu(self):
        ksscore = self.getCommandSet('core')
        selector = ksscore.getHtmlIdSelector('contentActionMenus')
        self.getCommandSet('zope').refreshProvider(selector, 'plone.contentmenu')
