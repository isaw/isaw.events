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
#

import cgi, warnings

try:
    from Products.Five import BrowserView
except ImportError:
    from zope.app.publisher.browser import BrowserView
from zope.pagetemplate.pagetemplatefile import PageTemplateFile

class KSSBrowserView(BrowserView):

    # XML output gets rendered via a page template
    # XXX note: barefoot rendering, use python: only after zope2.9
    render_error = PageTemplateFile('browser/errorresponse.pt')

    def attach_error(self, err_type, err_value):
        'Attach the error payload on the response'
        message = '%s: %s' % (err_type, err_value)
        message = cgi.escape(message)
        payload = self.render_error(type='system', message=message)
        self.attach_payload(payload)

    def attach_payload(self, payload, header_name='X-KSSCOMMANDS'):
        'Attach the commands on the response'
        # get rid of newlines
        payload = payload.replace('\n', ' ')
        self.request.response.setHeader(header_name, payload)

# coherent naming KSS 
# deprecate Kss
class KssBrowserView(KSSBrowserView):
    def __init__(self, *args, **kw):
        message = "'KssBrowserView' is deprecated," \
            "use 'KSSBrowserView'- KSS uppercase instead."
        warnings.warn(message, DeprecationWarning, 2)
        KSSBrowserView.__init__(self, *args, **kw)

