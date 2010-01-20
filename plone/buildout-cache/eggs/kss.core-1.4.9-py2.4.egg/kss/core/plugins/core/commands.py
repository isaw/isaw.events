from kss.core.selectors import Selector, CssSelector, HtmlIdSelector
from kss.core.selectors import ParentNodeSelector, SameNodeSelector
from kss.core.kssview import CommandSet
from kss.core.deprecated import deprecated, deprecated_warning
from kss.core.plugins.core.interfaces import IKSSCoreCommands
from zope.interface import implements

class KSSCoreCommands(CommandSet):
    implements(IKSSCoreCommands)

    def getSelector(self, type, selector):
        'Get a selector of a given type'
        return Selector(type, selector)

    def getCssSelector(self, selector):
        return CssSelector(selector)
            
    def getHtmlIdSelector(self, selector):
        return HtmlIdSelector(selector)

    def getSameNodeSelector(self):
        return SameNodeSelector()

    def getParentNodeSelector(self, selector):
        return ParentNodeSelector(selector)

    # XXX the list is not full: maybe complete them?
    
    def replaceInnerHTML(self, selector, new_value, withKssSetup='True'):
        """ see interfaces.py """
        command = self.commands.addCommand('replaceInnerHTML', selector)
        data = command.addHtmlParam('html', new_value)
        data = command.addParam('withKssSetup', withKssSetup)

    def replaceHTML(self, selector, new_value, withKssSetup='True'):
        """ see interfaces.py """
        command = self.commands.addCommand('replaceHTML', selector)
        data = command.addHtmlParam('html', new_value)
        data = command.addParam('withKssSetup', withKssSetup)
    
    def setAttribute(self, selector, name, value):
        """ see interfaces.py """
        command = self.commands.addCommand('setAttribute', selector)
        data = command.addParam('name', name)
        data = command.addParam('value', value)

    def setKssAttribute(self, selector, name, value):
        """ see interfaces.py """
        command = self.commands.addCommand('setKssAttribute', selector)
        data = command.addParam('name', name)
        data = command.addParam('value', value)

    def setStyle(self, selector, name, value):
        """ see interfaces.py """
        command = self.commands.addCommand('setStyle', selector)
        data = command.addParam('name', name)
        data = command.addParam('value', value)
    
    def insertHTMLAfter(self, selector, new_value, withKssSetup='True'):
        """ see interfaces.py """
        command = self.commands.addCommand('insertHTMLAfter', selector)
        data = command.addHtmlParam('html', new_value)
        data = command.addParam('withKssSetup', withKssSetup)

    def insertHTMLAsFirstChild(self, selector, new_value, withKssSetup='True'):
        """ see interfaces.py """
        command = self.commands.addCommand('insertHTMLAsFirstChild', selector)
        data = command.addHtmlParam('html', new_value)
        data = command.addParam('withKssSetup', withKssSetup)

    def insertHTMLAsLastChild(self, selector, new_value, withKssSetup='True'):
        """ see interfaces.py """
        command = self.commands.addCommand('insertHTMLAsLastChild', selector)
        data = command.addHtmlParam('html', new_value)
        data = command.addParam('withKssSetup', withKssSetup)

    def insertHTMLBefore(self, selector, new_value, withKssSetup='True'):
        """ see interfaces.py """
        command = self.commands.addCommand('insertHTMLBefore', selector)
        data = command.addHtmlParam('html', new_value)
        data = command.addParam('withKssSetup', withKssSetup)

    def clearChildNodes(self, selector):
        """ see interfaces.py """
        command = self.commands.addCommand('clearChildNodes', selector)
    
    def deleteNode(self, selector):
        """ see interfaces.py """
        command = self.commands.addCommand('deleteNode', selector)

    def deleteNodeAfter(self, selector):
        """ see interfaces.py """
        command = self.commands.addCommand('deleteNodeAfter', selector)

    def deleteNodeBefore(self, selector):
        """ see interfaces.py """
        command = self.commands.addCommand('deleteNodeBefore', selector)

    def copyChildNodesFrom(self, selector, id):
        """ see interfaces.py """
        command = self.commands.addCommand('copyChildNodesFrom', selector)
        data = command.addParam('html_id', id)

    def moveNodeAfter(self, selector, id):
        """ see interfaces.py """
        command = self.commands.addCommand('moveNodeAfter', selector)
        data = command.addParam('html_id', id)

    def moveNodeBefore(self, selector, id):
        """ see interfaces.py """
        command = self.commands.addCommand('moveNodeBefore', selector)
        data = command.addParam('html_id', id)

    def copyChildNodesTo(self, selector, id):
        """ see interfaces.py """
        command = self.commands.addCommand('copyChildNodesTo', selector)
        data = command.addParam('html_id', id)

    def setStateVar(self, varname, value):
        """ see interfaces.py """
        command = self.commands.addCommand('setStateVar')
        command.addParam('varname', varname)
        command.addParam('value', value)

    def continueEvent(self, name, allnodes=False, **kw):
        """ see interfaces.py """
        command = self.commands.addCommand('continueEvent')
        command.addParam('name', name)
        command.addParam('allnodes', allnodes and 'true' or 'false')
        for key, value in kw.iteritems():
            command.addParam(key, value)

    def toggleClass(self, selector, *arg, **kw):
    ##def toggleClass(self, selector, value):
        """ see interfaces.py """
        # BBB 4 months, until 2007-10-18
        value = BBB_classParms('toggleClass', *arg, **kw)

        command = self.commands.addCommand('toggleClass', selector)
        data = command.addParam('value', value)

    def addClass(self, selector, *arg, **kw):
    ##def addClass(self, selector, name):
        """ see interfaces.py """
        # BBB 4 months, until 2007-10-18
        value = BBB_classParms('addClass', *arg, **kw)

        command = self.commands.addCommand('addClass', selector)
        data = command.addParam('value', value)

    def removeClass(self, selector, *arg, **kw):
    ##def removeClass(self, selector, name):
        """ see interfaces.py """
        # BBB 4 months, until 2007-10-18
        value = BBB_classParms('removeClass', *arg, **kw)

        command = self.commands.addCommand('removeClass', selector)
        data = command.addParam('value', value)

    def focus(self, selector):
        """ see interfaces.py """
        command = self.commands.addCommand('focus', selector)

    def blur(self, selector):
        """ see interfaces.py """
        command = self.commands.addCommand('blur', selector)

    # XXX Deprecated ones

    # BBB until 2007-10-18
    def moveChildrenTo(self, selector, id):
        """ see interfaces.py """
        self.copyChildrenTo(selector, id)
        self.clearChildren(selector)
    moveChildrenTo = deprecated(moveChildrenTo, 'No more supported, use a sequence of copyChildrenTo and clearChildren')

    # BBB until 2007-10-18
    setHtmlAsChild = deprecated(replaceInnerHTML, 'use replaceInnerHTML instead')
    addAfter = deprecated(insertHTMLAfter, 'use insertHTMLAfter instead')
    clearChildren = deprecated(clearChildNodes, 'use clearChildNodes instead')
    removeNode = deprecated(deleteNode, 'use deleteNode instead')
    removeNextSibling = deprecated(deleteNodeAfter, 'use deleteNodeAfter instead')
    removePreviousSibling = deprecated(deleteNodeBefore, 'use deleteNodeBefore instead')
    copyChildrenFrom = deprecated(copyChildNodesFrom, 'use copyChildNodesFrom instead')
    copyChildrenTo = deprecated(copyChildNodesTo, 'use copyChildNodesTo instead')
    setStatevar = deprecated(setStateVar, 'use setStateVar (capital V) instead')

    # BBB 4 month, until 2007-10-18
    addClassName = deprecated(addClass, 'use addClass instead')
    removeClassName = deprecated(removeClass, 'use removeClass instead')

# BBB 4 month, until 2007-10-18
def BBB_classParms(commandname, value=None, classname=None, name=None):
    if classname:
        deprecated_warning(('Deprecated the "classname" parameter in the "%s" command, ' +
                           'use "name" instead.') % (commandname ,))
        if not value:
            value = classname
    if name:
        deprecated_warning(('Deprecated the "name" parameter in the "%s" command, ' +
                           'use "name" instead.') % (commandname ,))
        if not value:
            value = name
    if not value:
        raise Exception, 'Parameter "value" is mandatory in command "%s"' % (commandname, )
    return value

    # end deprecated
