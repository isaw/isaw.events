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


from kss.core.plugins.core.demo.zopeconfig import KSSCoreDemos
from reStructuredText import HTML
from zope.dottedname.resolve import resolve
from kss.core import KSSView

class DemoRegistry(KSSView):

    def getDemo(self, viewname):
        kssdemos = KSSCoreDemos().demos
        for demo in kssdemos:
            if demo.page_url==viewname + '.html':
                return demo
        return None

    def getHTMLHelp(self, viewname):
        demo = self.getDemo(viewname)
        packagePath = self.getPackagePath(viewname)
        helpfile = demo.helpfile
        if not packagePath or not helpfile:
            return ''
        file = open(packagePath + '/' + helpfile)
        rtext = file.read()
        file.close()
        html = HTML(rtext)
        return html

    def getPackagePath(self, viewname):
        demo = self.getDemo(viewname)
        packageName = demo.packageName
        if not packageName:
            return None
        module = resolve(packageName)
        packagePath = '/'.join(module.__file__.split('/')[:-1])
        return packagePath

    def displayHelp(self, viewname):
        html = '<h1>Description</h1><div>%s</div>' % self.getHTMLHelp(viewname)
        self.getCommandSet('core').replaceInnerHTML('div#help', html)
        self.getCommandSet('core').addClass('a#displayHelp', 'hidden')
        self.getCommandSet('core').removeClass('a#hideHelp', 'hidden')
        return self.render()

    def hideHelp(self):
        self.getCommandSet('core').replaceInnerHTML('div#help', '')
        self.getCommandSet('core').removeClass('a#displayHelp', 'hidden')
        self.getCommandSet('core').addClass('a#hideHelp', 'hidden')
        return self.render()
