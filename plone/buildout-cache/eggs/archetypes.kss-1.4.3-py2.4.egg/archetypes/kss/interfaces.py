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
from zope.component.interfaces import IObjectEvent

# --
# Events
# --

class IVersionedFieldModifiedEvent(IObjectEvent):
    """A field has been modified, versioning needed"""


class IInlineEditingEnabled(Interface):
    """A view which just returns True or False on call to indicate
       whether inline editing should be enabled or not."""
