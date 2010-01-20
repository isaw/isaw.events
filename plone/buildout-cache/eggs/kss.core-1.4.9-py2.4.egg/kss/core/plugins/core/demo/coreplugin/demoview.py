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
    def keyEvent(self, keycode):
        """XXX"""
        keycode = int(keycode)
        message = "Keycode: [%i]" % (keycode, )
        key = chr(keycode)
        if key.isalnum():
            message += ', Alpanumeric:"%s"' % (key, )
        core = self.getCommandSet('core')
        selector = core.getHtmlIdSelector('target')
        core.replaceInnerHTML(selector, message)
