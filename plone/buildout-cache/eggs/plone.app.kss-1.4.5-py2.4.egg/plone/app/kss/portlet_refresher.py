# -*- coding: UTF-8 -*-

from zope.interface import implements

from plonekssview import PloneKSSView
from interfaces import IPloneKSSView

class PortletView(PloneKSSView):

    # --
    # Portlet refresher actions
    # --

    implements(IPloneKSSView)
    
    def refreshPortlet(self, portlethash, nodeid=None):
        'Refresh portlet by name.'
        self.getCommandSet('plone').refreshPortlet(portlethash)
        return self.render()
