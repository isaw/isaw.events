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

from zope.interface import Interface

class IKSSPlugin(Interface):
    '''Base for KSS plugins
    
    this represents an entity implemented in a javascript file
    '''

class ICommand(IKSSPlugin):
    '''Command plugin'''

class IAction(IKSSPlugin):
    '''Action plugin'''

class IEventType(IKSSPlugin):
    '''Event type plugin'''

class ISelectorType(IKSSPlugin):
    '''Selector type plugin'''

class ICommandSet(Interface):
    '''Command set plugin'''

class IParamProvider(IKSSPlugin):
    '''Parameter provider plugin'''
