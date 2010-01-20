# -*- coding: ISO-8859-15 -*-
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

'''\
Parser implementations

These assure that output is valid XML or HTML and fix the code or
raise an exception.

The wrapping makes it possible to change the parser transparently
if necessary.
'''

from unicode_quirks import force_unicode
import re, htmlentitydefs

class replace_html_named_entities(object):

    _entity_regexp = re.compile(r'&([A-Za-z]+);')

    def _entity_replacer(m):
        value = htmlentitydefs.name2codepoint.get(m.group(1))
        if value is None:
            return m.group(0)
        return "&#%i;" % value
    _entity_replacer = staticmethod(_entity_replacer)

    def _replace(cls, value):
        return cls._entity_regexp.sub(cls._entity_replacer, value)
    _replace = classmethod(_replace)

    def __new__(cls, value):
        return cls._replace(value)

class XmlParser(object):
    '''Custom XML parser

    wraps the parser implementation
    '''

    from BeautifulSoup import BeautifulStoneSoup
    
    def __init__(self, value):
        value = force_unicode(value)
        self.soup = self.BeautifulStoneSoup(value)

    def __call__(self):
        return unicode(self.soup)
        
class HtmlParser(object):
    '''Custom HTML parser

    wraps the parser implementation
    '''

    from BeautifulSoup import BeautifulSoup
    
    def __init__(self, value):
        value = force_unicode(value)
        self.soup = self.BeautifulSoup(value)
        #
        # XXX ree: I think these are not needed any more. See
        # kukit patches r25865, r25866 that IMO fix this on IE.
        #
        #for tag in self.soup.fetch(recursive=False):
        #    tag['xmlns'] = "http://www.w3.org/1999/xhtml"

    def __call__(self):
        value = unicode(self.soup)
        # Replace named HTML entitied in each case.
        # This is necessary for two reasons:
        # 1. Fixes an IE bug.
        # 2. Needed for the alternate transport mechanism to work.
        value = replace_html_named_entities(value)

        return value
