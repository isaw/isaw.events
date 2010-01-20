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

from plugin import KSSPlugin, KSSPluginError
from interfaces import IAction
from zope.interface import implements
import zope.component as capi

def checkRegisteredCommand(name):
    'Check if it is a registered command.'
    try:
        command = capi.getUtility(IAction, name)
    except capi.ComponentLookupError:
        raise KSSPluginError, '"%s" is not a registered kss command' % (name, )
    # check if the action has a valid command factory
    if command.command_factory == 'none':
        raise KSSPluginError, '"%s" kss command has missing command_factory' % (name, )
    # issue deprecation warning, if necessary
    command.check_deprecation()

class Action(KSSPlugin):
    '''The action plugin

    '''

    implements(IAction)

    def __init__(self, name, jsfile, command_factory, 
            params_mandatory, params_optional, deprecated):
        KSSPlugin.__init__(self, name, jsfile)
        self.command_factory = command_factory
        self.params_mandatory = params_mandatory
        self.params_optional = params_optional
        self.deprecated = deprecated

    def check_deprecation(self):
        if self.deprecated:
            import warnings, textwrap
            warnings.warn(textwrap.dedent('''\
            The usage of the kss command "%s" is deprecated,
            %s''' % (self.name, self.deprecated)), DeprecationWarning, 2)
