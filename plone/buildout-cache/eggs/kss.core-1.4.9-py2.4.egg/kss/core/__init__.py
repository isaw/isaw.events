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

__all__ = ('force_unicode', 'KSSUnicodeError', 
           'KSSExplicitError', 'kssaction', 'KSSView',
           'CommandSet', 'ICommandSet',
#BBB
           'AzaxBaseView', 'KssExplicitError', 
        ) 

import mimetypes

mimetypes.types_map['.kkt'] = 'text/xml'    # BBB legacy!
mimetypes.types_map['.kukit'] = 'text/xml'

from kss.core.kssview import KSSView, CommandSet
from kss.core.actionwrapper import KSSExplicitError, kssaction 
from kss.core.unicode_quirks import force_unicode, KSSUnicodeError
from kss.core.interfaces import ICommandSet

# BBB
from kss.core.kssview import AzaxBaseView
from kss.core.actionwrapper import KssExplicitError
import sys, kssview
sys.modules['kss.core.azaxview'] = kssview

try:
    import Products.Five
except ImportError:
    pass
else:
    # Allow API to build commands from restricted code
    from AccessControl import allow_module
    allow_module('kss.core.ttwapi')

