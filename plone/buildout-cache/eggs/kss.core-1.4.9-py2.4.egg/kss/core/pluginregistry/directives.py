from zope.interface import Interface
from zope.schema import TextLine, Choice
from zope.configuration.fields import Path, Tokens, PythonIdentifier, \
        GlobalInterface, GlobalObject

class IRegisterEventTypeDirective(Interface):
    'Register a KSS event type'
    
    name = TextLine(
         title=u"Name",
         description=u"The name of the event type plugin.",
         required=True,
         )
    
    jsfile = Path(
         title=u"Javascript file",
         description=u"The path of the javascript file that defines the plugin",
         required=False,
         )
    
class IRegisterActionDirective(Interface):
    'Register a KSS action'
    
    name = TextLine(
         title=u"Name",
         description=u"The name of the action plugin.",
         required=True,
         )
    
    jsfile = Path(
         title=u"Javascript file",
         description=u"The path of the javascript file that defines the plugin",
         required=False,
         )

    command_factory = Choice(
        title=u"Command factory type",
        description=u"Command factory type, by default 'none'.",
        values=(u'none', u'global', u'selector'),
        required=False,
        )

    params_mandatory = Tokens(
        title=u"Mandatory parameters",
        description=u"Space separated list of mandatory parameter names",
        value_type=PythonIdentifier(),
        required=False,
        )

    params_optional = Tokens(
        title=u"Optional parameters",
        description=u"Comma separated list of optional parameter names",
        value_type=PythonIdentifier(),
        required=False,
        )

    deprecated = TextLine(
         title=u"Deprecated",
         description=u"The hint that we should give as warning about deprecation",
         required=False,
         )
 
class IRegisterSelectorTypeDirective(Interface):
    'Register a KSS selector type'
    
    name = TextLine(
         title=u"Name",
         description=u"The name of the selector type plugin.",
         required=True,
         )
    
    jsfile = Path(
         title=u"Javascript file",
         description=u"The path of the javascript file that defines the plugin",
         required=False,
         )

class IRegisterCommandSetDirective(Interface):
    'Register a KSS command set'
    
    for_ = GlobalInterface(
         title=u"For",
         description=u"The interface of view that can be adapted to this commandset",
         required=True,
         )
    
    class_ = GlobalObject(
         title=u"Class",
         description=u"The class that implements the commandset",
         required=True,
         )

    name = TextLine(
         title=u"Name",
         description=u"The name of the command set component.",
         required=True,
         )

    provides = GlobalInterface(
         title=u"Provides",
         description=u"The interface that does the adaptation on the view for this set",
         required=True,
         )
 
class IRegisterParamProviderDirective(Interface):
    'Register a KSS parameter provider'
    
    name = TextLine(
         title=u"Name",
         description=u"The name of the parameter provider plugin.",
         required=True,
         )
    
    jsfile = Path(
         title=u"Javascript file",
         description=u"The path of the javascript file that defines the plugin",
         required=False,
         )
