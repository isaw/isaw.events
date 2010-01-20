from zope.interface import Interface
from zope.configuration.fields import GlobalObject, Bool
from zope.schema import ASCII
from zope.app.publisher.browser.metadirectives import IBasicResourceInformation

class IConfigFeature(IBasicResourceInformation):
    """
    Defines a feature based on a python configuration
    """

    feature = ASCII(
        title = u"Feature",
        description = u"Name of the feature to define",
        required = True,
        )

    instance = GlobalObject(
        title = u'Object instance',
        description = u'Dotted name of the object that holds the attribute.',
        required = True,
        )

    attribute = ASCII(
        title = u"Attribute",
        description = u"Attribute name within the object.",
        required = True,
        )

    negate = Bool(
        title = u'Negate',
        description = u'If to negate the boolean value, default False',
        default = False,
        required = False,
        )
