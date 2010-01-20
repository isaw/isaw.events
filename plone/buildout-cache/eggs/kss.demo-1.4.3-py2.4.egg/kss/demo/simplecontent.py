# -*- coding: utf-8 -*-
# Copyright (c) 2005-2006
# Authors:
#   Godefroid Chapelle <gotcha@bubblenet.be>
#   Tarek Ziadé <tz@nuxeo.com>
#   Balázs Reé <ree@greenfinity.hu>
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
#

"""Simple content implementation
"""
from OFS.SimpleItem import SimpleItem
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from helpers import add_and_edit
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from zope.interface import implements
from interfaces import ISimpleContent
from persistent.mapping import PersistentMapping

class SimpleContent(SimpleItem):
    implements(ISimpleContent)

    meta_type = 'KssDemo SimpleContent'
    security = ClassSecurityInfo()

    manage_options = (
        {'label':'Demos', 'action':''},
        ) + SimpleItem.manage_options
    
    def __init__(self, id, title):
        self.id = id
        self.title = title
        self.mapping = PersistentMapping()

    def getValue(self, name, default=None):
        result = self.mapping.get(name, default)
        if not result or result == default:
            result = default
            self.setValue(name, result)
        return result

    def setValue(self, name, value):
        self.mapping[name] = value

    security.declarePublic('direct')
    def direct(self):
        """Should be able to traverse directly to this as there is no view.
        """
        return "Direct traversal worked"

InitializeClass(SimpleContent)

manage_addSimpleContentForm = PageTemplateFile(
    "www/simpleContentAdd", globals(),
    __name__ = 'manage_addSimpleContentForm')

def manage_addSimpleContent(self, id, title, REQUEST=None):
    """Add the simple content."""
    id = self._setObject(id, SimpleContent(id, title))
    add_and_edit(self, id, REQUEST)
    return ''
