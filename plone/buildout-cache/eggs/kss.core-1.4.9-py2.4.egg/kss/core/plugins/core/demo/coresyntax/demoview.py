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
#

from kss.core import KSSView, kssaction

class KSSDemoView(KSSView):

    @kssaction
    def urlMethod1(self):
        self.getCommandSet('core').replaceInnerHTML('div#target', 'Method 1 called')

    @kssaction
    def urlMethod2(self):
        self.getCommandSet('core').replaceInnerHTML('div#target', 'Method 2 called')

    @kssaction
    def urlMethod3(self):
        self.getCommandSet('core').replaceInnerHTML('div#target', 'Method 3 called')
