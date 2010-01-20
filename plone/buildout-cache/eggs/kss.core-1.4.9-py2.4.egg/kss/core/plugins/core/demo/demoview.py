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

from kss.core import KSSView, force_unicode, KSSExplicitError, kssaction
import datetime
import time

class KSSDemoView(KSSView):

    def clearDivContent(self):
        """ clear div content """
        self.getCommandSet('core').clearChildNodes('div#demo')
        return self.render()

    def copyFromDivContent(self):
        """ copy div content """
        self.getCommandSet('core').copyChildNodesFrom('div#copy', 'demo')
        return self.render()

    def copyToDivContent(self):
        """ copy div content """
        self.getCommandSet('core').copyChildNodesTo('div#copy', 'demo')
        return self.render()

    def moveToDivContent(self):
        """ copy div content """
        self.getCommandSet('core').copyChildNodesTo('div#copy', 'demo')
        self.getCommandSet('core').clearChildNodes('div#copy')
        return self.render()

    def getDivContent(self):
        """ returns div content """
        self.getCommandSet('core').replaceInnerHTML('div#demo', '<h1>it worked</h1>')
        self.getCommandSet('core').replaceInnerHTML('div#demo', '<h1 id="workedagain">it worked&nbsp;again</h1>')
        return self.render()

    def getCorrespondingSelect(self, value):
        """ returns select content """
        mapping = {}
        mapping['']=[]
        mapping['animals']=['dog', 'cat', 'cow']
        mapping['machines']=['computer', 'car', 'airplane']
        # XXX Note that originally we just used replaceInnerHTML to just put
        # the options inside the select, however this is principally broken
        # on IE due to an IE bug. Microsoft has confirmed the bug but is not
        # giving information on whether it has or it will ever be fixed.
        # For further info, see http://support.microsoft.com/default.aspx?scid=kb;en-us;276228
        # The current solution, replace the outer node, works solidly.
        result = ['<select id="second">']
        result.extend(['<option>%s</option>' % item for item in mapping[value]])
        result.append('</select>')
        self.getCommandSet('core').replaceHTML('select#second', ' '.join(result))
        return self.render()

    def getAutoupdateMarkup(self):
        """ returns the current time """
        self.getCommandSet('core').replaceInnerHTML('div#update-wrapper', '<div id="update-area"></div>')
        return self.render()

    def getCurrentTime(self):
        """ returns the current time """
        self.getCommandSet('core').replaceInnerHTML('div#update-area', "<p>%s</p>" % str(datetime.datetime.now()))
        return self.render()

    def getInputField(self, value):
        'Inserts the value as entered into an input field'
        # We need to make unicode. But on Z2 we receive utf-8, on Z3 unicode
        value = force_unicode(value, 'utf')
        self.getCommandSet('core').replaceInnerHTML('div#text',
                            '<div><input type="text" name="value" value="'+value+'" /></div>' \
                            '<input type="button" value="save" id="save" />'
                           )
        return self.render()

    def saveText(self, value):
        'Inserts the value to display it on the page'
        # We need to make unicode. But on Z2 we receive utf-8, on Z3 unicode
        value = force_unicode(value, 'utf')
        self.getCommandSet('core').replaceInnerHTML('div#text', value+'<input type="hidden" name="value" value="'+value+'" />')
        return self.render()

    def expandSubTree(self, value, xvalue):
        'Expands given subtree'
        self.getCommandSet('core').replaceInnerHTML('#text', 'works, expand %s (xhtml attr: %s)' % (value, xvalue))
        return self.render()

    def collapseSubTree(self, value, xvalue):
        'Collapses given subtree'
        self.getCommandSet('core').replaceInnerHTML('#text', 'works, collapse %s (xhtml attr: %s)' % (value, xvalue))
        return self.render()

    def cancelSubmitSave(self, text_save):
        # We need to make unicode. But on Z2 we receive utf-8, on Z3 unicode
        text_save = force_unicode(text_save, 'utf')
        self.getCommandSet('core').replaceInnerHTML('div#async', 'Async saved %s' % text_save)
        return self.render()

    def removeNodeXpath(self):
        # XXX the xpath selector is now moved out of the core, see suppl, product "azaxslt"
        sel = self.getSelector('xpath', "//P[@id='xpath']/following-sibling::*[position()=1]")
        self.getCommandSet('core').deleteNode(sel)
        return self.render()

    def clickedButton(self, id):
        'Show status of the button clicked'
        self.getCommandSet('core').replaceInnerHTML('#update-status', "<p>Button <b>%s</b> clicked. <i>%s</i></p>" % (id, datetime.datetime.now()))
        return self.render()

    def updateSlaveSelector(self, masterid, value):
        """ returns select content """
        mapping = {}
        mapping['']=[]
        mapping['animals']=['dog', 'cat', 'cow']
        mapping['machines']=['computer', 'car', 'airplane']
        # calculate the slave id
        master, _dummy = masterid.split('-')
        slaveid = '%s-slave' % master
        # make the payload
        result = ['<select id="%s">' % slaveid]
        result.extend(['<option>%s</option>' % item for item in mapping[value]])
        result.append('</select>')
        # XXX See above remark why we need to replace the outer select.
        self.getCommandSet('core').replaceHTML('select#%s' % slaveid, ' '.join(result))
        return self.render()

    def formSubmitSave(self):
        result = ['<p>Async saved:</p><table><th>Name:</th><th>Value:</th>']
        for key, value in self.request.form.items():
            result.append('<tr><td>%s</td><td>%s</td></tr>' % (key, value))
        result.append('</table>')
        # We need to make unicode. But on Z2 we receive utf-8, on Z3 unicode
        retval = force_unicode(''.join(result), 'utf')
        self.getCommandSet('core').replaceInnerHTML('div#async', retval)
        return self.render()

    def reset(self):
        self.getCommandSet('effects').effect('.effects', 'appear')
        return self.render()

    @kssaction
    def errTest(self, id, act):
        if act == 'error':
            raise Exception, 'We have an error here.'
        elif act == 'explicit':
            raise KSSExplicitError, 'Explicit error raised.'
        elif act == 'empty':
            # Just do nothing, we want to return a response with no commands.
            # This is valid behaviour, should raise no error, however
            # gives a warning in the kukit log.
            pass
        elif act == 'timeout':
            # Wait longer then timeout, this is set by the stylesheet with
            # setActionServerTimeout client action
            time.sleep(2.0);
            # the next reply will never arrive.
            self.getCommandSet('core').replaceInnerHTML('#update-status', u'Not arrived')
        else:
            # act = noerror: standard response.
            self.getCommandSet('core').replaceInnerHTML('#update-status', u'Normal response, button %s clicked. %s' % (id, datetime.datetime.now()))
        return self.render()

    def htmlReplace(self):
        """html replace"""
        self.getCommandSet('core').replaceHTML('div#frame', '<div id="frame"><h1 id="core">KSS for a life.</h1></div>')
        return self.render()

    def htmlInsertBefore(self, text=''):
        """html insert"""
        self.getCommandSet('core').insertHTMLBefore('#frame', '<div class="type1">KSS for a life. %s</div>' % text)
        return self.render()

    def htmlInsertAfter(self, text=''):
        """html insert"""
        self.getCommandSet('core').insertHTMLAfter('#frame', '<div class="type1">KSS for a life. %s</div>' % text)
        return self.render()

    def htmlInsertAsFirstChild(self, text=''):
        """html insert"""
        self.getCommandSet('core').insertHTMLAsFirstChild('div#frame',
                                                          "first: %s " % text)
        return self.render()

    def htmlInsertAsLastChild(self, text=''):
        """html insert"""
        self.getCommandSet('core').insertHTMLAsLastChild('div#frame',
                                                         "last: %s" % text)
        return self.render()


    # protocol
    def protocolSmallDataset(self):
        self.getCommandSet('core').replaceInnerHTML(
            '#dataset-output', '<em>Worked</em>')
        return self.render()

    def protocolLargeDataset(self):
        text = 'really ' * 690
        self.getCommandSet('core').replaceInnerHTML(
            '#dataset-output', '<em>%s</em>' % (text + 'large text'))
        return self.render()

    def protocolAMP(self):
        self.getCommandSet('core').replaceInnerHTML(
            '#character-output', 'text & stuff')
        return self.render()

    def protocolLT(self):
        self.getCommandSet('core').replaceInnerHTML(
            '#character-output', 'text < stuff')
        return self.render()

    def protocolGT(self):
        self.getCommandSet('core').replaceInnerHTML(
            '#character-output', 'text > stuff')
        return self.render()

    def protocolENDCDATA(self):
        self.getCommandSet('core').replaceInnerHTML(
            '#character-output', 'before ]]> after')
        return self.render()


    def protocolSmallAttribute(self):
        self.getCommandSet('core').setAttribute(
            '#attribute-output', 'class', 'some smallattr')
        return self.render()

    def protocolLargeAttribute(self):
        classes = ' '.join(['h' + hex(i)[2:] * i for i in range(70)])
        self.getCommandSet('core').setAttribute(
            '#attribute-output', 'class', classes + ' largeattr')
        return self.render()

    def protocolAttributeAMP(self):
        self.getCommandSet('core').setAttribute(
            '#character-attr-output', 'title', 'text & stuff')
        return self.render()

    def protocolAttributeLT(self):
        self.getCommandSet('core').setAttribute(
            '#character-attr-output', 'title', 'text < stuff')
        return self.render()

    def protocolAttributeGT(self):
        self.getCommandSet('core').setAttribute(
            '#character-attr-output', 'title', 'text > stuff')
        return self.render()

    def protocolAttributeENDCDATA(self):
        self.getCommandSet('core').setAttribute(
            '#character-attr-output', 'title', 'before ]]> after')
        return self.render()
