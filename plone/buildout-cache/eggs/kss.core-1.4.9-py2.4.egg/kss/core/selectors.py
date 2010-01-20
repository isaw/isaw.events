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

CSS_SELECTOR = 'css'
HTMLID_SELECTOR = 'htmlid' 
PARENTNODE_SELECTOR = 'parentnode' 
SAMENODE_SELECTOR = 'samenode' 

class SelectorBase(object):
    
    def __init__(self, selector):
        self.value = selector
        
class CssSelector(SelectorBase):
    type = CSS_SELECTOR
        
class HtmlIdSelector(SelectorBase):
    type = HTMLID_SELECTOR

class ParentNodeSelector(SelectorBase):
    type = PARENTNODE_SELECTOR

class SameNodeSelector(SelectorBase):
    def __init__(self):
        super(SameNodeSelector, self).__init__('')
    type = SAMENODE_SELECTOR

# A generic (pluggable) selector

class Selector(SelectorBase):

    def __init__(self, type, selector):
        self.type = type
        SelectorBase.__init__(self, selector)
