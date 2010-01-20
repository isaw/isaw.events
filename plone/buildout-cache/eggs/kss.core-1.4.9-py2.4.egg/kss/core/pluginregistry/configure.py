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

from zope.component.zcml import adapter
from interfaces import IEventType, ISelectorType, IAction, IParamProvider
from event_type import EventType
from action import Action
from selector_type import SelectorType
from commandset import registerAndAllowCommandSet
from pprovider import ParamProvider
from plugin import registerPlugin

def registerEventType(_context, name, jsfile=None):
    'Directive that registers an event type' 
    
    # check to see if the file exists
    if jsfile is not None:
        file(jsfile, 'rb').close()

    _context.action(
        discriminator = ('registerKssEventType', name, jsfile),
        callable = registerPlugin,
        args = (EventType, IEventType, name, jsfile),
        )
 
def registerAction(_context, name, jsfile=None, command_factory='none',
        params_mandatory=[], params_optional=[], deprecated=None):
    'Directive that registers an action.' 
    
    # check to see if the file exists
    if jsfile is not None:
        file(jsfile, 'rb').close()

    _context.action(
        discriminator = ('registerKssAction', name, jsfile),
        callable = registerPlugin,
        args = (Action, IAction, name, jsfile, command_factory, params_mandatory, params_optional, deprecated),
        )

def registerSelectorType(_context, name, jsfile=None):
    'Directive that registers a selector type' 
    
    # check to see if the file exists
    if jsfile is not None:
        file(jsfile, 'rb').close()

    _context.action(
        discriminator = ('registerKssSelectorType', name, jsfile),
        callable = registerPlugin,
        args = (SelectorType, ISelectorType, name, jsfile),
        )

def registerCommandSet(_context, for_, class_, name, provides):
    'Directive that registers a command set' 
    
    adapter(_context, [class_], provides, [for_])
    _context.action(
        discriminator = ('registerKssCommandSet', name),
        callable = registerAndAllowCommandSet,
        args = (class_, name, provides),
        )

def registerParamProvider(_context, name, jsfile=None):
    'Directive that registers a parameter provider' 
    
    # check to see if the file exists
    if jsfile is not None:
        file(jsfile, 'rb').close()

    _context.action(
        discriminator = ('registerKssParamProvider', name),
        callable = registerPlugin,
        args = (ParamProvider, IParamProvider, name, jsfile),
        )
