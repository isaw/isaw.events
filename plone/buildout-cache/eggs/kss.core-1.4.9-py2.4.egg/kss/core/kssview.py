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

'''\
KSS Base view class

All the implementations should create a specialization
of this class when building their browser views.

The policy is that a method should build up a command
set on available methods and then return self.render().

The default command set is implemented in the base class
as well.
'''

import warnings

try:
    from Products.Five import BrowserView
except ImportError:
    from zope.publisher.browser import BrowserView

from kss.core.commands import KSSCommands
from kss.core.interfaces import IKSSView, ICommandSet
from kss.core.pluginregistry.commandset import getRegisteredCommandSet

from zope import component, interface, event
from zope.interface.adapter import VerifyingAdapterRegistry
from zope.component.globalregistry import BaseGlobalComponents
from zope.component.interfaces import IObjectEvent
from zope.app.component.interfaces import ISite
from zope.app.publication.zopepublication import BeforeTraverseEvent

HAS_FIVE_LSM = True
try:
    from five.localsitemanager import registry
    from zope.component.registry import UtilityRegistration
except ImportError:
    HAS_FIVE_LSM = False


class SiteViewComponents(BaseGlobalComponents):

    def _init_registries(self):
        # This is why this class is needed: we can't work with a
        # regular AdapterRegistry because it wants to do funny things
        # with __bases__.
        self.adapters = VerifyingAdapterRegistry()
        self.utilities = VerifyingAdapterRegistry()
        if HAS_FIVE_LSM:
            self.utilities.LookupClass = registry.FiveVerifyingAdapterLookup
            self.utilities._createLookup()
            self.utilities.__parent__ = self

    if HAS_FIVE_LSM:
        def registeredUtilities(self):
            for ((provided, name), (component, info)
                 ) in self._utility_registrations.iteritems():
                yield UtilityRegistration(self, provided, name,
                                          registry._wrap(component, self),
                                          info)

class SiteView(BrowserView):
    """A browser view that is its own site
    """
    interface.implements(ISite)

    def __init__(self, context, request):
        super(SiteView, self).__init__(context, request)

        next = component.getSiteManager()
        self._sitemanager = SiteViewComponents('siteview')
        self._sitemanager.__bases__ = (next, )
        if HAS_FIVE_LSM:
            self._sitemanager.__parent__ = self

        # On Five, we should wrap it in the acquisition context
        # see, if self has aq_parent, it is done obligatoraly
        try:
            self.context.aq_parent
        except AttributeError:
            # Zope3 - No problem.
            wrapped_view = self
        else:
            wrapped_view = self.__of__(self.context)

        # register object event handler
        self._sitemanager.registerHandler(wrapped_view._eventRedispatcher)

    # Zope 2.10 doesn't send BeforeTraverseEvents for all objects,
    # only the ones for which you explicitly enable a before traverse
    # hook available from Five.component.  Hence, this view won't
    # become the current site when it's traversed.  This is bad,
    # hopefully Zope 2.11 will fix this.  For now, we'll just take
    # care of it ourselves...
    def __before_publishing_traverse__(self, obj, request):
        event.notify(BeforeTraverseEvent(self, request))

    # ISite interface

    def getSiteManager(self):
        return self._sitemanager

    def setSiteManager(self, sm):
        raise TypeError("Site manager of SiteView can't be changed.")

    @component.adapter(IObjectEvent)
    def _eventRedispatcher(self, event):
        """This works similar to zope.component.event.objectEventNotify:
        It dispatches object events to subscribers that listen to
        (object, view, event)."""
        adapters = component.subscribers((event.object, self, event), None)
        for adapter in adapters:
            pass # getting them does the work

class KSSView(SiteView):
    """KSS view

    This allows setting up the content of the response, and then
    generate it out.
    """
    interface.implements(IKSSView)

    def __init__(self, context, request):
        super(KSSView, self).__init__(context, request)
        self._initcommands()

    def _initcommands(self):
        self.commands = KSSCommands()

    # XXX avoid weird acquisition behaviour in Zope 2... this should
    # go away when Five views aren't Acquisition objects anymore.
    def _set_context(self, context):
        self._context = [context]
    def _get_context(self):
        return self._context[0]
    context = property(_get_context, _set_context)

    def render(self):
        """Views can use this to return their command set."""
        return self.commands.render(self.request)

    def cancelRedirect(self):
        if self.request.response.getStatus() in (302, 303):
            # Try to not redirect if requested
            self.request.response.setStatus(200)

    def getCommands(self):
        return self.commands

    def getCommandSet(self, name):
        commandset = getRegisteredCommandSet(name)
        # return the adapted view
        return commandset.provides(self)

class CommandSet:
    interface.implements(ICommandSet)

    def __init__(self, view):
        self.view = view
        self.context = self.view.context
        self.request = self.view.request
        self.commands =  self.view.commands

    def getCommandSet(self, name):
        return self.view.getCommandSet(name)

# BBB deprecated
class AzaxBaseView(KSSView):
    def __init__(self, *args, **kw):
        message = "'AzaxBaseView' is deprecated," \
            "use 'KSSView' instead."
        warnings.warn(message, DeprecationWarning, 2)
        KSSView.__init__(self, *args, **kw)

class AzaxViewAdapter(CommandSet):
    def __init__(self, *args, **kw):
        message = "'AzaxViewAdapter' is deprecated," \
            "use 'CommandSet' instead."
        warnings.warn(message, DeprecationWarning, 2)
        CommandSet.__init__(self, *args, **kw)

