# -*- coding: UTF-8 -*-
from zope.interface import implements
from plonekssview import PloneKSSView

from kss.core import kssaction
from interfaces import IPloneKSSView

class ContentMenuView(PloneKSSView):

    # --
    # ContentMenu in-place refreshment
    # --

    implements(IPloneKSSView)

    @kssaction
    def contentMenuRefresh(self, id, menu):
        # XXX: We only know how to refresh the entire menu at this stage
        self.getCommandSet('plone').refreshContentMenu()

