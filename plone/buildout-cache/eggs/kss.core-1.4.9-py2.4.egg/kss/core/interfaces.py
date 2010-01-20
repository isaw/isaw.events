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

from zope.interface import Interface, Attribute

class IKSSCommands(Interface):
    'KSS commands'

    def addCommand(self, name, selector=None):
        'Add a command'
   
    def render(self, request):
        'All methods must use this to return their command set'

    def getSelector(self, type, selector):
        'Return selector'

    # more helpers for the basic selectors

    def getCssSelector(self, selector):
        'Return selector'
            
    def getHtmlIdSelector(self, selector):
        'Return selector'

class IKSSCommand(Interface):
    'An KSS command'

    def addParam(self, name, content=''):
        'Add the param as is'

    #
    # Some helpers
    #

    def addUnicodeParam(self, name, content=''):
        'Add the param as unicode'

    def addStringParam(self, name, content='', encoding='utf'):
        'Add the param as an encoded string, by default UTF-8'

    def addHtmlParam(self, name, content=''):
        'Add the param as an HTML content.'

    def addXmlParam(self, name, content=''):
        'Add the param as XML content'

    def addCdataParam(self, name, content=''):
        'Add the param as a CDATA node'

    # --
    # Accessors, not sure if we need them
    # --

    def getName(self):
        ''

    def getSelector(self):
        ''

    def getSelectorType(self):
        ''

    def getParams(self):
        ''

class IKSSCommandView(Interface):
    'View of a command set'

    def render():
        'This renders the command set'


class IKSSParam(Interface):
    'An KSS parameter'
    
    def force_content_unicode(self):
        'Content must be str with ascii encoding, or unicode'

    def getName(self):
        ''

    def getContent(self):
        ''

class IKSSView(Interface):

    commands = Attribute('An IKSSCommands object that keeps track of '
                         'all commands that are sent to the browser')

    def render(self):
        """Return a string representation of all KSS commands issued
        so far."""

    def getCommandSet(name):
        """Return the commandset called ``name`` bound to the current
        view."""

# BBB deprecated
IAzaxView = IKSSView

class ICommandSet(Interface):
    'Methods of this class implement a command set'

    def getCommandSet(self, name):
        'Returns the command set for a given name'
