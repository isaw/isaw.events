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

import zope.component as capi
from interfaces import IKSSPlugin
from zope.interface import implements
# concatresource is an embedded product 
import _concatresource
from concatresource.interfaces import IConcatResourceAddon
from json import getJsonAddonFiles
import zope.component as capi

class KSSConcatResourceAddon(object):
    implements(IConcatResourceAddon)
    
    def getAddonFiles(self):
        try:
            files = self._addon_files
        except AttributeError:
            # Lazy setup of addon files
            self._addon_files = files = getJsonAddonFiles()
            # Lookup all utilities and add up the files from it
            plugins = capi.getAllUtilitiesRegisteredFor(IKSSPlugin)
            for plugin in plugins:
                if plugin.jsfile and plugin.jsfile not in files:
                    files.append(plugin.jsfile)
        return files

kssConcatResourceAddon = KSSConcatResourceAddon()
