from zope.deprecation import deprecate
from kss.core.kssview import CommandSet

from Products.statusmessages.message import Message

# XXX: This is deprecated and will be removed in Plone 4.0. Use the 'plone'
# command set instead.
class IssuePortalMessageCommand(CommandSet):

    __allow_access_to_unprotected_subobjects__ = 1

    @deprecate("The 'portalmessage' command set is deprecated and will be removed in Plone 4.0. "
               "Please use the 'plone' command set instead.")
    def issuePortalMessage(self, message, msgtype='info'):
        'Issue this portal message'
        if message is None:
            # allow message = None.
            message = ''

        if isinstance(message, Message):
            msgtype = message.type
            message = message.message

        # XXX The macro has to take in account that there might be more than
        # one status message.
        ksscore = self.getCommandSet('core')
        selector = ksscore.getHtmlIdSelector('kssPortalMessage')

        # We hide the standard Plone Portal Message
        standar_portal_message_selector = ksscore.getCssSelector('.portalMessage')
        ksscore.setStyle(standar_portal_message_selector, 'display','none')

        # Now there is always a portal message but it has to be
        # rendered visible or invisible, accordingly
        html = '<dt>%s</dt><dd>%s</dd>' % (msgtype, message)
        ksscore.replaceInnerHTML(selector, html)
        ksscore.setAttribute(selector, 'class', "portalMessage %s" % msgtype)
        ksscore.setStyle(selector, 'display', message and 'block' or 'none')
