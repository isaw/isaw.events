from zope.i18nmessageid import MessageFactory
PloneMessageFactory = MessageFactory('plone')

from Products.CMFCore.permissions import setDefaultRoles
setDefaultRoles('plone.portlet.static: Add static portlet', ('Manager', 'Owner',))