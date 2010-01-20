
import os
from zope.security.checker import CheckerPublic, NamesChecker
from zope.configuration.exceptions import ConfigurationError
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.app.component.metaconfigure import handler
from zope.interface import Interface
from resource import ConcatResourceFactory

try:
    import Products.Five
except ImportError:
    __five__ = False
else:
    __five__ = True
    from Products.Five.metaclass import makeClass
    from Products.Five.security import getSecurityInfo, protectClass, protectName,\
        initializeClass

try:
    from zope.publisher.interfaces.browser import IDefaultBrowserLayer
    _layer = IDefaultBrowserLayer
    __pre_3_2__ = False
except ImportError:
    from zope.app.servicenames import Presentation
    _layer = 'default'
    __pre_3_2__ = True

try:
    from zope.component import zcml
    __pre_3_3__ = False
except:
    __pre_3_3__ = True

# z3 only
allowed_names = ('GET', 'HEAD', 'publishTraverse', 'browserDefault',
                 'request', '__call__')

# We keep this in order to allow an occasional merge to browser:resource
_factory_map = {
    'files': {
        'prefix': 'ConcatResource',
        'count': 0,
        'factory': ConcatResourceFactory
        },
    }

def concatresource(_context, name, files=None, compress_level='safe',
        caching='default', lmt_check_period=60.0,
        layer=_layer, permission='zope.Public'):

    if not files:
        raise ConfigurationError(
            "Must use a files"
            " attribute for concatresource directives, with at least"
            " one file contained."
            )

    res = files
    res_type = 'files'
    factory_info = _factory_map.get(res_type)
    factory_info['count'] += 1
    res_factory = factory_info['factory']

    if __five__:
        checker = None
        _class_name = '%s%s' % (factory_info['prefix'], factory_info['count'])
        new_class = makeClass(_class_name, (res_factory.resource,), {})

        _context.action(
            discriminator = ('five:protectClass', new_class),
            callable = protectClass,
            args = (new_class, permission)
            )
        _context.action(
            discriminator = ('five:initialize:class', new_class),
            callable = initializeClass,
            args = (new_class,)
            )

    else:
        new_class = res_factory.resource

        if permission == 'zope.Public':
            permission = CheckerPublic

        checker = NamesChecker(allowed_names, permission)

    factory = res_factory(res, name, compress_level, caching, lmt_check_period,
            resource_factory=new_class, checker=checker)

    if __pre_3_2__:
        _context.action(
            discriminator = ('resource', name, IBrowserRequest, layer),
            callable = handler,
            args = (Presentation, 'provideResource',
                    name, IBrowserRequest, factory, layer),
            )
    else:
        if __pre_3_3__:
            _context.action(
                discriminator = ('resource', name, IBrowserRequest, layer),
                callable = handler,
                args = ('provideAdapter',
                    (layer,), Interface, name, factory, _context.info),
                )
        else:
            _context.action(
                discriminator = ('resource', name, IBrowserRequest, layer),
                callable = handler,
                args = ('registerAdapter',
                    factory, (layer,), Interface, name, _context.info),
                )
