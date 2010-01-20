# -*- coding: ISO-8859-15 -*-
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

import warnings, textwrap

def deprecated_warning(message):
    warnings.warn(message, DeprecationWarning, 2)

def deprecated(method, message):
    def deprecated_method(self, *args, **kw):
        warnings.warn(message, DeprecationWarning, 2)
        return method(self, *args, **kw)
    return deprecated_method

def deprecated_directive(method, directive, message):
    def deprecated_method(_context, *args, **kw):
        warnings.warn(message, DeprecationWarning, 2)
        warnings.warn(textwrap.dedent('''\


              %s
            The directive %s is deprecated and will be removed any time,
            %s
            '''
            % (_context.info, directive, message)),
        DeprecationWarning, 2)
        return method(_context, *args, **kw)
    return deprecated_method
