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

class KSSUnicodeError(RuntimeError):
    pass

def force_unicode(value, encoding='ascii'):
    'Force value to be unicode - allow also value in a specific encoding (by default, ascii).'
    if isinstance(value, str):
        try:
            value = unicode(value, encoding)
        except UnicodeDecodeError, exc:
            raise KSSUnicodeError, 'Content must be unicode or ascii string, original exception: %s' % (exc, )
    else:
        assert isinstance(value, unicode)
    return value
