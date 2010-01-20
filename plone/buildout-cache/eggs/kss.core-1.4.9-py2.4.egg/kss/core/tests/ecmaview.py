# Copyright (c) 2005-2007
# Authors: KSS Project Contributors (see docs/CREDITS.txt)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.

try:
    from Products.Five import BrowserView
except ImportError:
    from zope.app.publisher.browser import BrowserView

from zope.interface import Interface, implements
from zope.app import zapi
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
import os.path
from zope.publisher.interfaces.browser import IBrowserPublisher
from zope.publisher.interfaces import NotFound

# Oh well... file resource has different import locations in zope and five,
# the factories take different parameters order,
# plus these are not "entirely clean" as far as caching is concerned...
# Instead, use the resources implemented from concatresource:
# this is version free and has properly implemented cache control.
from kss.core.pluginregistry._concatresource.resource import ConcatResourceFactory

_marker = object()

# z3 only
from zope.security.checker import CheckerPublic, NamesChecker
allowed_names = ('GET', 'HEAD', 'publishTraverse', 'browserDefault',
                 'request', '__call__')
permission = CheckerPublic
checker = NamesChecker(allowed_names, permission)

class ViewFile(object):
    '''A wrapper for file resources that can be used in a view
    
    Similar to ViewPageTemplate in usage.
    (We only use the FileResource here, no distinction on content types
    like in the resourceDirectory code.)
    '''

    def __init__(self, name, path):
        # Create the resource with cache control most proper for debugging.
        self.resource_factory = ConcatResourceFactory([path], name, 
                compress_level='none', caching='memory', lmt_check_period=0.0,
                checker=checker)
        self.name = name

    def __get__(self, obj, cls=None):
        'The view wants a method only.'
        request = obj.request
        resource = self.resource_factory(request)
        resource.__parent__ = obj
        resource.__name__ = self.name
        return resource

def absolute_dir(path):
    here = os.path.split(globals()['__file__'])[0]
    return os.path.abspath(os.path.join(here, path))

class EcmaView(BrowserView):
    '''Kukit test view
    
    This allows the runner.html to be used on this view.

    This provides the tests run with the compiled kukit.js
    resource, in the same way as they would be run 
    in production with kss.
    '''

    implements(IBrowserPublisher)

    _testdir = absolute_dir('../kukit/tests')

    _runner = ViewPageTemplateFile('../kukit/tests/runner.html')
    
    # The next is only necessary on Zope (<=) 2.9,
    # provides a docstring to the method
    def _runner_proxy(self, *arg, **kw):
        'Publishable method'
        return self._runner(*arg, **kw)

    def publishTraverse(self, request, name):
        '''See interface IBrowserPublisher'''
        return self.get(name)

    def browserDefault(self, request):
        '''See interface IBrowserPublisher'''
        return self, ()

    def __getitem__(self, name):
        res = self.get(name, None)
        if res is None:
            raise KeyError(name)
        return res

    def get(self, name, default=_marker):
        # runner.html is compiled as a pagetemplate
        if name == 'runner.html':
            # XXX For Zope2.9 we need this.
            if not hasattr(self.request, 'debug'):
                self.request.debug = None
            # proxy is used to make it publishable, on Zope <= 2.9
            return self._runner_proxy

        # We store them on the view on demand.
        # Is it there yet?
        if name[0] != '_':
            try:
                return getattr(self, name)
            except AttributeError:
                pass

        # See the file we need
        path = os.path.join(self._testdir, name)
        if os.path.isfile(path):
            # Ok, this is a file. Cook it.
            resource = ViewFile(name, path)
            setattr(self.__class__, name, resource)
            # important: return accessed *from* the view.
            return getattr(self, name)

        # Not found.
        if default is _marker:
            raise NotFound(None, name)
        return default

    def __call__(self):
        'By default we redirect to runner.html.'
        # on Zope3, the url is of zope.publisher.http.URLGetter class, so we must stringify it
        return self.request.response.redirect(str(self.request.URL) + '/runner.html')
