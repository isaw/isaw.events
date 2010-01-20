# -*- coding: UTF-8 -*-
from zope.interface import implements
from plonekssview import PloneKSSView
from kss.core import kssaction
from interfaces import IPloneKSSView
from plone.locking.interfaces import ILockable
from Acquisition import aq_inner
from zope.component import queryAdapter

class LockView(PloneKSSView):
    """
    Lock informations/operation in kss
    """
    implements(IPloneKSSView)

    @kssaction
    def updateLockInfo(self):
        """Update the lock icon -
        Check if the object if really locked before showing the icon
        an xmlhttprequest might have just been sent on the object to
        unlock just a few moment ago. So we need to be really sure
        that the object wasn't locked, to be sure, we do one more
        """
        context = aq_inner(self.context)
        locking = queryAdapter(context, ILockable)
        if locking and not locking.locked():
            coreCmd = self.getCommandSet('core')
            selector = coreCmd.getHtmlIdSelector('lock-icon')
            coreCmd.deleteNode(selector)
