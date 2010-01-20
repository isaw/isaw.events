from zope.component import adapter
from zope.component import getAllUtilitiesRegisteredFor

from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from plone.portlets.interfaces import IPortletManager
from plone.app.portlets.portlets.navigation import INavigationPortlet
from plone.app.portlets.portlets.recent import IRecentPortlet
from plone.app.portlets.interfaces import IDeferredPortletRenderer

from kss.core.interfaces import IKSSView

from Products.DCWorkflow.interfaces import IAfterTransitionEvent

@adapter(None, IKSSView, IObjectModifiedEvent)
def attributesTriggerNavigationPortletReload(obj, view, event):
    triggeringAttributes = ('title', 'description')
    if attributesModified(triggeringAttributes, event):
        portletReloader = PortletReloader(view)
        portletReloader.reloadPortletsByInterface(INavigationPortlet)

@adapter(None, IKSSView, IObjectModifiedEvent)
def attributesTriggerRecentPortletReload(obj, view, event):
    triggeringAttributes = ('title', 'description')
    if attributesModified(triggeringAttributes, event):
        portletReloader = PortletReloader(view)
        portletReloader.reloadPortletsByInterface(IRecentPortlet)

def attributesModified(triggeringAttributes, event):
    for description in event.descriptions:
        for attr in triggeringAttributes:
            if attr in description.attributes:
                return True
    return False

@adapter(None, IKSSView, IAfterTransitionEvent)
def workflowTriggersNavigationPortletReload(obj, view, event):
    if not (event.old_state is event.new_state):
        obj.reindexObject()
        portletReloader = PortletReloader(view)
        portletReloader.reloadPortletsByInterface(INavigationPortlet)

@adapter(None, IKSSView, IAfterTransitionEvent)
def workflowTriggersRecentPortletReload(obj, view, event):
    if not (event.old_state is event.new_state):
        obj.reindexObject()
        portletReloader = PortletReloader(view)
        portletReloader.reloadPortletsByInterface(IRecentPortlet)

class PortletReloader(object):
    def __init__(self, view):
        self.view = view
        self.context = view.context
        self.request = view.request

    def reloadPortletsByInterface(self, interface):
        for info in self.getPortletsByInterface(interface):
            self.reloadPortletByInfo(info)

    def getPortletsByInterface(self, interface):
        return [info for info in self.getAllPortletInfos() 
                if interface.providedBy(info['assignment'])]
    
    def reloadPortletByInfo(self, info):
        renderer = info['renderer']
        renderer.update()
        if IDeferredPortletRenderer.providedBy(renderer):
            # if this is a deferred load, prepare now the data
            renderer.deferred_update()
        result = renderer.render()
        portlethash = info['hash']
        wrapper_id = 'portletwrapper-%s' % portlethash
        ksscore = self.view.getCommandSet('core')
        ksscore.replaceInnerHTML(ksscore.getHtmlIdSelector(wrapper_id), result, withKssSetup='False')

    def getAllPortletInfos(self):
        portletInfos = []
        for manager in getAllUtilitiesRegisteredFor(IPortletManager):
            managerRenderer = manager(self.context, self.request, self.view)
            if managerRenderer.visible:
                portletInfos += managerRenderer.portletsToShow()
        return portletInfos
