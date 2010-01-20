# Copyright (c) 2006-2007
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
from kss.core.interfaces import IKSSCommandView

class CommandInspectorView(object):
    '''Inspector view of a command.
    
    This enables debugging checks. Returns commands
    as a list of dicts.

    Look at the tests to see what checks this makes possible.
    '''
    implements(IKSSCommandView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

        # Force parameters content to be unicode
        for command in context:
            for param in command.getParams():
                param.force_content_unicode()
    
    def render(self):
        result = []
        for command in self.context:
            d = dict(command.__dict__)
            # params are converted to a dict from a list.
            # Also get rid of "none" params that were only a hack for xml
            d['params'] = dict([(param.name, param.content) for param in d['params'] if param.name != 'none'])
            result.append(d)
        return result
