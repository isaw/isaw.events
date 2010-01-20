# -*- coding: UTF-8 -*-
from zope.interface import implements
from plonekssview import PloneKSSView
from kss.core import force_unicode, kssaction
from interfaces import IPloneKSSView

class KupuSaveView(PloneKSSView):

    # --
    # Calendar in-place refreshment
    # --

    implements(IPloneKSSView)

    @kssaction
    def save(self, text, fieldname):
        "In-place saving of kupu text area's."
        corecommands = self.getCommandSet('core')
        self.context.getField(fieldname).set(self.context, text, mimetype='text/html')
        
        selector = corecommands.getCssSelector('body')
        corecommands.insertHTMLAsLastChild(
            selector, '<div class="kupu-save-message">Document saved</div>')
