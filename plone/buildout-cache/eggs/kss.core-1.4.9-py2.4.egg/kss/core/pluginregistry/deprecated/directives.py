from zope.interface import Interface
from zope.schema import TextLine, Choice
from zope.configuration.fields import Path, Tokens, PythonIdentifier, \
        GlobalInterface

class IRegisterCommandDirective(Interface):
    'Register a KSS command plugin'
    
    name = TextLine(
         title=u"Name",
         description=u"The name of the command plugin.",
         required=True,
         )
    
    jsfile = Path(
         title=u"Javascript file",
         description=u"The path of the javascript file that defines the plugin",
         required=False,
         )
    
from kss.core.pluginregistry.directives import IRegisterEventTypeDirective, \
        IRegisterActionDirective, IRegisterSelectorTypeDirective, \
        IRegisterCommandSetDirective
