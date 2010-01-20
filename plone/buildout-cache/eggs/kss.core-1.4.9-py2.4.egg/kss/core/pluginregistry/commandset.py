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

from zope.interface import implements
import zope.component as capi

from plugin import KSSPluginError
from plugin import registerPlugin
from interfaces import ICommandSet

def getRegisteredCommandSet(name):
    'Get the command set'
    try:
        commandset = capi.getUtility(ICommandSet, name)
    except capi.ComponentLookupError:
        raise KSSPluginError, '"%s" is not a registered kss command set' % (name, )
    return commandset

class CommandSet(object):
    '''The command set plugin

    registers the command adapter interface
    (like IKssCoreCommands), this makes possible
    to look them up by name instead of by interface
    '''

    implements(ICommandSet)

    def __init__(self, name, provides):
        self.name = name
        self.provides = provides

def registerAndAllowCommandSet(class_, name, provides, *arg, **kw):
    registerPlugin(CommandSet, ICommandSet, name, provides, *arg, **kw)
    try:
        import Products.Five
    except ImportError:
        pass
    else:
        # Allow TTW to use commandsets
        from AccessControl import allow_class
        allow_class(class_)
    
