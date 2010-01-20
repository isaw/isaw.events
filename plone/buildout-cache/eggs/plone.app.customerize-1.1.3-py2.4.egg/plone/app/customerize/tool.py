from five.customerize.interfaces import IViewTemplateContainer
from zope.interface import implements
from OFS.Folder import Folder


class ViewTemplateContainer(Folder):
    """ a local utility storing all ttw view templates provided
        by five.customerize in a folder """
    implements(IViewTemplateContainer)

    id  = 'portal_view_customizations'
    title = 'Manages view customizations'
    meta_type = 'Plone View Customizations'

    manage_options = (
        dict(label='Registrations', action='registrations.html'),
        ) + Folder.manage_options[0:1] + Folder.manage_options[2:]

    def addTemplate(self, id, template):
        """ add the given ttw view template to the container """
        self._setObject(id, template)
        return getattr(self, id)

