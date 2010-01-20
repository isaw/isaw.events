from zope.interface import Interface

class IScriptaculousEffectsCommands(Interface):
    '''effects commands'''
    def effect(selector, type):
        '''scriptaculous effect'''
