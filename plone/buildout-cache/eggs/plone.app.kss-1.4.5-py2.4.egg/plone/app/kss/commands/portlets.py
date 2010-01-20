from zope.deprecation import deprecate
from interfaces import IKSSPlonePortletCommands
from plone.portlets.interfaces import IPortletManager
from plone.app.portlets.portlets.classic import Assignment
from plone.portlets.interfaces import IPortletRenderer
from zope import component

from kss.core.kssview import CommandSet
from zope.interface import implements

# XXX: This is deprecated and will be removed in Plone 4.0. Use the 'plone'
# command set instead.
class KSSPortletCommands(CommandSet):
    implements(IKSSPlonePortletCommands)

    @deprecate("The 'plone-portlets' command set is deprecated and will be removed in Plone 4.0. "
               "Please use the 'plone' command set instead.")
    def reload_classic_portlet(self, css_selector, column,
                               template, portlet_macro='portlet'):
        context = self.context
        request = self.request
        view = self.view
        manager = component.getUtility(
            IPortletManager, name=column, context=context)
        assignment = Assignment(
            template=template, macro=portlet_macro)

        portlet = component.getMultiAdapter(
            (context, request, view, manager, assignment), IPortletRenderer)
        portlet = portlet.__of__(context)

        view.getCommandSet('core').replaceInnerHTML(css_selector, portlet.render())
