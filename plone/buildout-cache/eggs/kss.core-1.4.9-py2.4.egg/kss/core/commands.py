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

'''\
Marshal objects

These build up the response and get marshalled to the client
in the defined format
'''

from xml.sax.saxutils import escape as xml_escape
from zope.interface import implements
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from interfaces import IKSSCommands, IKSSCommand, IKSSParam, IKSSCommandView
from unicode_quirks import force_unicode
import zope.component
from parsers import XmlParser, HtmlParser
from pluginregistry import checkRegisteredCommand_old
from pluginregistry import checkRegisteredCommand, checkRegisteredSelector, \
        KSSPluginError

class KSSCommands(list):
    implements(IKSSCommands)

    def addCommand(self, command_name, selector=None, **kw):
        command = KSSCommand(command_name, selector=selector, **kw)
        self.append(command)
        return command

    def render(self, request):
        '''All methods must use this to return their command set
        '''
        adapter = zope.component.getMultiAdapter((self, request), IKSSCommandView)
        return adapter.render()

class KSSParam:
    implements(IKSSParam)

    def __init__(self, name, content=''):
        self.name = name
        self.content = content

    def force_content_unicode(self):
        # Content must be str with ascii encoding, or unicode!
        self.content = force_unicode(self.content)

    def getName(self):
        return self.name

    def getContent(self):
        return self.content

class KSSCommand:
    implements(IKSSCommand)

    def __init__(self, command_name, selector=None, **kw):
        try:
            checkRegisteredCommand_old(command_name)
        except KSSPluginError:
            # we expect this is not registered as command, anyway
            # so check it as an action.
            checkRegisteredCommand(command_name)
        else:
            # ok. XXX this will be deprecated
            # All registerCommand commands are obsolete, by default
            import warnings, textwrap
            warnings.warn(textwrap.dedent('''\
            The usage of the kss command "%s" is deprecated'''
                % (command_name, )), DeprecationWarning, 2)
        if selector is not None:
            if isinstance(selector, basestring):
                # the default selector - given just as a string
                self.selector = selector
                self.selectorType = ''
            else:
                checkRegisteredSelector(selector.type)
                self.selector = selector.value
                self.selectorType = selector.type
        else:
            self.selector = None
            self.selectorType = None
        self.name = command_name
        self.params = []
        # Add parameters passed in **kw
        for key, value in kw.iteritems():
            self.addParam(key, value)

    # --
    # Different parameter conversions
    # --

    # REMARK: with the jsonserver product present, you can
    # just send complex data types directly with AddParam

    def addParam(self, name, content=''):
        # Check for the size of the content. Larger than 4K will give
        # problems with Firefox (which splits text nodes). Therefore
        # we give this special treatment.
        if len(content) > 4096:
            return self.addCdataParam(name, content)
        else:
            # Escape all XML characters
            return self._addParam(name, content=xml_escape(content))

    def _addParam(self, name, content=''):
        'Add the param as is'
        param = KSSParam(name, content)
        self.params.append(param)
        return param

    #
    # Some helpers
    #

    def addUnicodeParam(self, name, content=u''):
        'Add the param as unicode'
        self.addParam(name, content)

    def addStringParam(self, name, content='', encoding='utf8'):
        'Add the param as an encoded string, by default UTF-8'
        content = unicode(content, encoding)
        self.addUnicodeParam(name, content=content)

    def addHtmlParam(self, name, content=''):
        'Add the param as an HTML content.'
        content = HtmlParser(content)().encode('ascii', 'xmlcharrefreplace')
        ##self.addParam(name, content=content)
        # add html as cdata!
        self.addCdataParam(name, content=content)

    def addXmlParam(self, name, content=''):
        'Add the param as XML content'
        content = XmlParser(content)().encode('ascii', 'xmlcharrefreplace')
        self._addParam(name, content=content)

    def addCdataParam(self, name, content=''):
        'Add the param as a CDATA node'
        # Replace `>` part of `]]>` with the entity ref so it won't
        # accidentally close the CDATA (required by the XML spec)
        content = '<![CDATA[%s]]>' % content.replace(']]>', ']]&gt;')
        self._addParam(name, content=content)


    # --
    # Accessors, not sure if we need them
    # --

    def getName(self):
        return self.name

    def getSelector(self):
        return self.selector

    def getSelectorType(self):
        return self.selectorType

    def getParams(self):
        return self.params

class CommandView(object):
    '''View of a command.

    The render method does actual marshalling
    of the commands to be sent to the client.
    '''
    implements(IKSSCommandView)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        # XXX From Zope2.9 we need this.
        # Note: We don't use proper views for Five. As our context object
        # is not even a proper Zope content. There would be a way to:
        #
        # - use ZopeTwoPageTemplateFile
        # - and, make the object to be proper zope content.
        #
        # This would be two much ado for nothing, so we just use barefoot
        # rendering but as a consequence no path expression, only python:
        # is available from the page template.
        if not hasattr(self.request, 'debug'):
            self.request.debug = None

        # Force parameters content to be unicode
        for command in context:
            for param in command.getParams():
                param.force_content_unicode()

    # XML output gets rendered via a page template
    # XXX note: barefoot rendering, use python: only after zope2.9
    # XXX we must have the content type set both here and below
    _render = ViewPageTemplateFile('browser/kukitresponse.pt', content_type='text/xml;charset=utf-8')

    def render(self):
        result = self._render()
        # Always output text/xml to make sure browsers but the data in the
        # responseXML instead of responseText attribute of the
        # XMLHttpRequestobject.
        self.request.response.setHeader('Content-type', 'text/xml;charset=utf-8')
        return result
