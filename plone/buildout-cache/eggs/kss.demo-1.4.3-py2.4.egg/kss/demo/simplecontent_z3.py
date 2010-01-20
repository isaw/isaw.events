# -*- coding: utf-8 -*-
# Copyright (c) 2005-2006
# Authors:
#   Godefroid Chapelle <gotcha@bubblenet.be>
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

'''\
Simple content implementation
'''

from persistent import Persistent
from zope.interface import implements
from interfaces import ISimpleContent

class SimpleContent(Persistent):
    implements(ISimpleContent)
