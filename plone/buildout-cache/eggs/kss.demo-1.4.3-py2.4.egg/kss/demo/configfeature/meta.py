
from zope.configuration.exceptions import ConfigurationError

def configfeature(_context, feature, instance, attribute, negate=False):
    """Imports a python object and uses an attribute of it as a boolean value
    to declare a feature or not.

    Usage
    -----

    We can have an object with attributes,

    >>> class dictlike(object):
    ...     pass
    >>> conf1 = dictlike()
    >>> conf1.this = True
    >>> conf1.that = False

    and its attributes can defined a feature if they evaluate to True.
    The feature will not be defined if the value evaluates to False.

    >>> from zope.configuration.config import ConfigurationContext
    >>> c = ConfigurationContext()
    >>> configfeature(c, 'f1', conf1, 'this')
    >>> c.hasFeature('f1')
    True
    >>> configfeature(c, 'f2', conf1, 'that')
    >>> c.hasFeature('f2')
    False

    The boolean value can be negated, this allows it
    to overcome the shortage of negating possibilit of zcml:condition.

    >>> configfeature(c, 'f3', conf1, 'this', True)
    >>> c.hasFeature('f3')
    False
    >>> configfeature(c, 'f4', conf1, 'that', True)
    >>> c.hasFeature('f4')
    True

    Instead of an object with attributes, a dictionary can also be used:

    >>> dconf = {}
    >>> dconf['this'] = True
    >>> dconf['that'] = False

    >>> configfeature(c, 'f5', dconf, 'this')
    >>> c.hasFeature('f5')
    True
    >>> configfeature(c, 'f6', dconf, 'that')
    >>> c.hasFeature('f6')
    False


    Error handling
    --------------

    If there is an unexistent attribute, an error is reported.

    >>> configfeature(c, 'f7', conf1, 'nosuch')         #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    ConfigurationError: Object ... does not have attribute or key "nosuch"

    >>> configfeature(c, 'f8', dconf, 'nosuch')         #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    ConfigurationError: Object ... does not have attribute or key "nosuch"


    Finally, like with the "provides" directive normally:
    Spaces are not allowed in feature names (this is reserved for providing
    many features with a single directive in the futute).

    >>> configfeature(c, 'two words', conf1, 'this')
    Traceback (most recent call last):
    ...
    ValueError: Only one feature name allowed

    """

    try:
        value = getattr(instance, attribute)
    except AttributeError:
        # also try as dictionary value
        try:
            value = instance[attribute]
        except (TypeError, ValueError, KeyError):
            raise ConfigurationError, 'Object %s does not have attribute or key "%s"' % (instance, attribute)

    value = bool(value)
    if negate:
        value = not value

    if len(feature.split()) > 1:
        raise ValueError("Only one feature name allowed")

    if value:
        _context.provideFeature(feature)
