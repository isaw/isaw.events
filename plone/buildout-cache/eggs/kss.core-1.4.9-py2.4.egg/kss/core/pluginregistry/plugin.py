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

from interfaces import IKSSPlugin
import zope.component as capi
from zope.interface import implements

class KSSPluginError(Exception):
    pass
 
def registerPlugin(cls, interface, name, *arg, **kw):
    'Convenience method to help registration'
    plugin = cls(name, *arg, **kw)
    # check if it's registered: do not allow registration for the second name
    try:
        capi.getUtility(interface, name=name)
    except capi.ComponentLookupError:
        pass
    else:
        raise KSSPluginError, 'Duplicate registration attempt for plugin "%s" of type %s' % (plugin.name, interface)
    # provide the utility.
    capi.provideUtility(plugin, interface, name=name)

class KSSPlugin(object):
    'The base plugin class'

    implements(IKSSPlugin)

    def __init__(self, name, jsfile):
        self.name = name
        self.jsfile = jsfile
