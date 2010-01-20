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

from textwrap import dedent
from inspect import  formatargspec, getargspec, getargvalues, \
                     formatargvalues, currentframe
from zope.interface import implements

class KSSExplicitError(Exception):
    'Explicit error to be raised'

class kssaction(object):
    '''Descriptor to bundle kss server actions.

    - render() will be called automatically if there is no
      return value

    - if KSSExplicitError is raised, a normal response is returned,
      containing a single command:error KSS command.

    Let's say we have a class here - that is supposed to be a kss view.

        >>> from kss.core import kssaction, KSSExplicitError, KSSView

        >>> class MyView(KSSView):
        ...     def ok(self, a, b, c=0):
        ...         return 'OK %s %s %s' % (a, b, c)
        ...     def notok(self, a, b, c=0):
        ...         pass
        ...     def error(self, a, b, c=0):
        ...         raise KSSExplicitError, 'The error'
        ...     def exception(self, a, b, c=0):
        ...         raise Exception, 'Unknown exception'
         
    Now we try qualifying with kssaction. We overwrite render too, 
    just to enable sensible testing of the output:

        >>> class MyView(KSSView):
        ...     def render(self):
        ...         return 'Rendered'
        ...     @kssaction
        ...     def ok(self, a, b, c=3):
        ...         return 'OK %s %s %s' % (a, b, c)
        ...     @kssaction
        ...     def notok(self, a, b, c=3):
        ...         pass
        ...     @kssaction
        ...     def error(self, a, b, c=3):
        ...         raise KSSExplicitError, 'The error'
        ...     @kssaction
        ...     def exception(self, a, b, c=3):
        ...         raise Exception, 'Unknown exception'
 
    Instantiate a view.

        >>> view = MyView(None, None)

    Now, of course ok renders well.

        >>> view.ok(1, b=2)
        'OK 1 2 3'

    Not ok will have implicit rendering.

        >>> view.notok(1, b=2)
        'Rendered'

    The third type will return an error action. But it will render
    instead of an error.

        >>> view.error(1, b=2)
        'Rendered'

    The fourth type will be a real error.

        >>> view.exception(1, b=2)
        Traceback (most recent call last):
        ...
        Exception: Unknown exception

    Now for the sake of it, let's test the rendered kukit response.
    So, we don't overwrite render like as we did in the previous
    tests.

        >>> from zope.publisher.browser import TestRequest

        >>> class MyView(KSSView):
        ...     @kssaction
        ...     def error(self, a, b, c=3):
        ...         raise KSSExplicitError, 'The error'
        ...     @kssaction
        ...     def with_docstring(self, a, b, c=3):
        ...         "Docstring"
        ...         raise KSSExplicitError, 'The error'
 
        >>> request = TestRequest()
        >>> view = MyView(None, request)

    Set debug-mode command rendering so we can see the results in a
    more structured form.

        >>> from zope import interface as iapi
        >>> from kss.core.tests.base import IDebugRequest
        >>> iapi.directlyProvides(request, iapi.directlyProvidedBy(request) + IDebugRequest)

    See the results:

        >>> view.error(1, b=2)
        [{'selectorType': None, 'params': {'message': u'The error'}, 'name': 'error', 'selector': None}]

    Usage of the method wrapped in browser view
    -------------------------------------------

    Finally, let's check if the method appears if defined on a browser view.
    Since there could be a thousand reasons why Five's magic could fail,
    it's good to check this. (XXX Note that this must be adjusted to run on Zope3.)

        >>> try:
        ...     import Products.Five
        ... except ImportError:
        ...     # probably zope 3, not supported
        ...     raise 'Zope3 not supported in this test'
        ... else:
        ...     from Products.Five.zcml import load_string, load_config

        >>> import kss.core.tests
        >>> kss.core.tests.MyView = MyView

    We check for two basic types of declaration. The first one declares
    a view with different attributes. The second one declares a dedicated
    view with the method as the view default method. This is how we use
    it in several places.

        >>> load_string("""
        ...      <configure xmlns="http://namespaces.zope.org/zope"
        ...      xmlns:browser="http://namespaces.zope.org/browser"
        ...      xmlns:five="http://namespaces.zope.org/five"
        ...      xmlns:zcml="http://namespaces.zope.org/zcml"
        ...      >
        ...
        ...      <browser:page
        ...          for="*"
        ...          class="kss.core.tests.MyView"
        ...          allowed_attributes="error with_docstring"
        ...          name="my_view"
        ...          permission="zope.Public"
        ...          />
        ...
        ...      <browser:page
        ...          for="*"
        ...          class="kss.core.tests.MyView"
        ...          attribute="error"
        ...          name="my_view2"
        ...          permission="zope.Public"
        ...          />
        ...
        ...  </configure>""")

    Let's check it now:
    
        >>> self.folder.restrictedTraverse('/@@my_view/error')
        <bound method MyView.wrapper...

    It must also work as a default method of a view since that is
    main usage for us:
    
        >>> v = self.folder.restrictedTraverse('/my_view2')
        >>> isinstance(v, MyView)
        True
        >>> hasattr(v, 'error')
        True
        >>> v(1, b=2)
        [{'selectorType': None, 'params': {'message': u'The error'}, 'name': 'error', 'selector': None}]

    In addition, to be publishable, the docstring must exist. Let's
    see if the wrapper actually does this. If the method had a docstring,
    it will be reused, but a docstring is provided in any case.

        >>> v = self.folder.restrictedTraverse('/@@my_view')
        >>> bool(v.error.__doc__)
        True

        >>> v.with_docstring.__doc__
        'Docstring'

    '''
    def __init__(self, f):
        self.f = f
        # Now this is a solution I don't like, but we need the same
        # function signature, otherwise the ZPublisher won't marshall
        # the parameters. *arg, **kw would not suffice since no parameters
        # would be marshalled at all.
        argspec = getargspec(f)
        orig_args = formatargspec(*argspec)[1:-1]
        if argspec[3] is None:
            fixed_args_num = len(argspec[0])
        else:
            fixed_args_num = len(argspec[0]) - len(argspec[3])
        values_list = [v for v in argspec[0][:fixed_args_num]]
        values_list.extend(['%s=%s' % (v, v) for v in argspec[0][fixed_args_num:]])
        values_args = ', '.join(values_list)
        # provide a docstring in any case.
        if self.f.__doc__ is not None:
            docstring = repr(f.__doc__)
        else:
            docstring = '"XXX"'
        # orig_args: "a, b, c=2"
        # values_args: "a, b, c=c"
        code = dedent('''\n
                def wrapper(%s):
                    %s
                    return descr.apply(%s)
                ''' % (orig_args, docstring, values_args))
        self.wrapper_code = compile(code, '<wrapper>', 'exec')

    def __get__(self, obj, cls=None):
        d =  {'descr': self, 'self': obj}
        exec(self.wrapper_code, d)
        wrapper = d['wrapper'].__get__(obj, cls)
        return wrapper

    def apply(self, obj, *arg, **kw):
        try:
            result = self.f(obj, *arg, **kw)
        except KSSExplicitError, exc:
            # Clear all the commands, and emit an error command
            obj._initcommands()
            obj.commands.addCommand('error', message=str(exc))
            result = None
        if result is None:
            # render not returned - so we do it.
            result = obj.render()
        return result

# backward compatibility
class KssExplicitError(KSSExplicitError):
    def __init__(self, *args, **kw):
        message = "'KssExplicitError' is deprecated," \
            "use 'KSSExplicitError'- KSS uppercase instead."
        warnings.warn(message, DeprecationWarning, 2)
        KSSExplicitError.__init__(self, *args, **kw)

