
import sys
import unittest
from zope.testing.doctestunit import DocTestSuite
from __parent__ import __parent__
configfeature = __parent__(__name__, 2)

def test_module_level():
    """
    Module level access.

    >>> import zope.configuration.tests
    >>> import zope.configuration.xmlconfig
    >>> context = zope.configuration.xmlconfig.file('metacore.zcml', configfeature)

    >>> import tempfile
    >>> fn = tempfile.mktemp('.zcml')
    >>> zcml = open(fn, 'w')
    >>> zcml.write('''
    ... <configure xmlns:meta="http://namespaces.zope.org/meta"
    ...            xmlns:five="http://namespaces.zope.org/five">
    ...     <five:configfeature
    ...         feature="conf1"
    ...         instance=".configtest"
    ...         attribute="conf1"
    ...     />
    ...     <five:configfeature
    ...         feature="conf2"
    ...         instance=".configtest"
    ...         attribute="conf2"
    ...     />
    ...     <five:configfeature
    ...         feature="conf2n"
    ...         instance=".configtest"
    ...         attribute="conf2"
    ...         negate="True"
    ...     />
    ... </configure>
    ... ''')
    >>> zcml.close()

    >>> context = zope.configuration.xmlconfig.file(fn, configfeature.tests, context)

    >>> context.hasFeature('conf1')
    True
    >>> context.hasFeature('conf2')
    False
    >>> context.hasFeature('conf2n')
    True

    """


def test_objectlevel():
    """
    Object level access.

    >>> import zope.configuration.tests
    >>> import zope.configuration.xmlconfig
    >>> context = zope.configuration.xmlconfig.file('metacore.zcml', configfeature)

    >>> import tempfile
    >>> fn = tempfile.mktemp('.zcml')
    >>> zcml = open(fn, 'w')
    >>> zcml.write('''
    ... <configure xmlns:meta="http://namespaces.zope.org/meta"
    ...            xmlns:five="http://namespaces.zope.org/five">
    ...     <five:configfeature
    ...         feature="conf3"
    ...         instance=".configtest.cobj"
    ...         attribute="conf3"
    ...     />
    ...     <five:configfeature
    ...         feature="conf4"
    ...         instance=".configtest.cobj"
    ...         attribute="conf4"
    ...     />
    ...     <five:configfeature
    ...         feature="conf4n"
    ...         instance=".configtest.cobj"
    ...         attribute="conf4"
    ...         negate="True"
    ...     />
    ... </configure>
    ... ''')
    >>> zcml.close()

    >>> context = zope.configuration.xmlconfig.file(fn, configfeature.tests, context)

    >>> context.hasFeature('conf3')
    True
    >>> context.hasFeature('conf4')
    False
    >>> context.hasFeature('conf4n')
    True

    """


def test_dict_level():
    """
    Dictionary level access.

    >>> import zope.configuration.tests
    >>> import zope.configuration.xmlconfig
    >>> context = zope.configuration.xmlconfig.file('metacore.zcml', configfeature)

    >>> import tempfile
    >>> fn = tempfile.mktemp('.zcml')
    >>> zcml = open(fn, 'w')
    >>> zcml.write('''
    ... <configure xmlns:meta="http://namespaces.zope.org/meta"
    ...            xmlns:five="http://namespaces.zope.org/five">
    ...     <five:configfeature
    ...         feature="conf5"
    ...         instance=".configtest.dobj"
    ...         attribute="conf5"
    ...     />
    ...     <five:configfeature
    ...         feature="conf6"
    ...         instance=".configtest.dobj"
    ...         attribute="conf6"
    ...     />
    ...     <five:configfeature
    ...         feature="conf6n"
    ...         instance=".configtest.dobj"
    ...         attribute="conf6"
    ...         negate="True"
    ...     />
    ... </configure>
    ... ''')
    >>> zcml.close()

    >>> context = zope.configuration.xmlconfig.file(fn, configfeature.tests, context)

    >>> context.hasFeature('conf5')
    True
    >>> context.hasFeature('conf6')
    False
    >>> context.hasFeature('conf6n')
    True

    """


def test_errors():
    """
    Testing errors.

    >>> import zope.configuration.tests
    >>> import zope.configuration.xmlconfig
    >>> context = zope.configuration.xmlconfig.file('metacore.zcml', configfeature)

    No such instance: raises an error.

    >>> import tempfile
    >>> fn = tempfile.mktemp('.zcml')
    >>> zcml = open(fn, 'w')
    >>> zcml.write('''
    ... <configure xmlns:meta="http://namespaces.zope.org/meta"
    ...            xmlns:five="http://namespaces.zope.org/five">
    ...     <five:configfeature
    ...         feature="conf1"
    ...         instance=".configtest.nosuch"
    ...         attribute="conf1"
    ...     />
    ... </configure>
    ... ''')
    >>> zcml.close()

    >>> context = zope.configuration.xmlconfig.file(fn, configfeature.tests, context) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    ZopeXMLConfigurationError: ...
        ConfigurationError: ...

    No such attribute: an error too

    >>> fn = tempfile.mktemp('.zcml')
    >>> zcml = open(fn, 'w')
    >>> zcml.write('''
    ... <configure xmlns:meta="http://namespaces.zope.org/meta"
    ...            xmlns:five="http://namespaces.zope.org/five">
    ...     <five:configfeature
    ...         feature="conf1"
    ...         instance=".configtest.cobj"
    ...         attribute="nosuch"
    ...     />
    ... </configure>
    ... ''')
    >>> zcml.close()

    >>> context = zope.configuration.xmlconfig.file(fn, configfeature.tests, context) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    ZopeXMLConfigurationError: ...
        ConfigurationError: Object ... does not have attribute or key "nosuch"

    No such key: an error too 

    >>> fn = tempfile.mktemp('.zcml')
    >>> zcml = open(fn, 'w')
    >>> zcml.write('''
    ... <configure xmlns:meta="http://namespaces.zope.org/meta"
    ...            xmlns:five="http://namespaces.zope.org/five">
    ...     <five:configfeature
    ...         feature="conf1"
    ...         instance=".configtest.dobj"
    ...         attribute="nosuch"
    ...     />
    ... </configure>
    ... ''')
    >>> zcml.close()

    >>> context = zope.configuration.xmlconfig.file(fn, configfeature.tests, context) #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    ZopeXMLConfigurationError: ...
        ConfigurationError: Object ... does not have attribute or key "nosuch"
    
    """


def test_suite():
    return unittest.TestSuite((
        DocTestSuite(configfeature.__name__ + '.meta'),
        DocTestSuite(),
        ))
