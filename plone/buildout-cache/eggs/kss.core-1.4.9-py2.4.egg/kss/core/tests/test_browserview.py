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

import unittest
from base import KSSViewTestCase

class TestBrowserView(KSSViewTestCase):
    
    def test_attach_error(self):
        'Test if errors are attached properly'
        # just render any page
        context = self.folder
        view = context.restrictedTraverse('@@kss_view')
        self.assert_(view is not None)
        view.attach_error(err_type='TheError', err_value='the_<>message\n\n')
        response = view.request.response
        header = response.getHeader('x-ksscommands')
        self.assert_('the_&amp;lt;&amp;gt;message' in header)   # no < > in the message
        self.assert_('\n' not in header)   # no /n in the payload: would destroy the page
        self.assertEqual(header, '<?xml version="1.0"?> <kukit xmlns="http://www.kukit.org/commands/1.1"> <commands> \t<command name="error"> \t\t<param name="type">system</param> \t\t<param name="message">TheError: the_&amp;lt;&amp;gt;message  </param> \t</command> </commands> </kukit> ')

def test_suite():
    suites = []
    suites.append(unittest.makeSuite(TestBrowserView))
    return unittest.TestSuite(suites)
