# -*- coding: UTF-8 -*-

from zope.interface import implements

from plonekssview import PloneKSSView
from interfaces import IPloneKSSView

class MacroView(PloneKSSView):

    # --
    # Macro replacement actions
    # --

    implements(IPloneKSSView)
    
    def replaceInnerByMacro(self, selector, macropath):
        content = self.macroContent(macropath)
        self.getCommandSet('core').replaceInnerHTML(selector, content)
        return self.render()

    def replaceByMacro(self, selector, macropath):
        content = self.macroContent(macropath)
        self.getCommandSet('core').replaceHTML(selector, content)
        return self.render()

    def replaceMacro(self, selector, macropath):
        import warnings, textwrap
        warnings.warn(textwrap.dedent('''\
            The usage of the server action replaceMacro is deprecated''' 
        ), DeprecationWarning, 2)
        return self.replaceInnerByMacro(selector, macropath)
