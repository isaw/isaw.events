# -*- coding: UTF-8 -*-

from zope.interface import implements

from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

from Products.statusmessages import STATUSMESSAGEKEY
from Products.statusmessages.adapter import _decodeCookieValue

from kss.core import KSSView as base
from kss.core import force_unicode

from interfaces import IPloneKSSView

class PloneKSSView(base):
    '''The base view that contains helpers, to be imported
    be other plone products
    '''

    implements(IPloneKSSView)
    
    header_macros = ZopeTwoPageTemplateFile('browser/macro_wrapper.pt')

    def macroContent(self, macropath, **kw):
        'Renders a macro and returns its text'
        path = macropath.split('/')
        if len(path) < 2 or path[-2] != 'macros':
            raise RuntimeError, 'Path must end with macros/name_of_macro (%s)' % (repr(macropath), )
        # needs string, do not tolerate unicode (causes but at traverse)
        jointpath = '/'.join(path[:-2]).encode('ascii')
        macroobj = self.context.restrictedTraverse(jointpath)
        try:
            the_macro = macroobj.macros[path[-1]]
        except AttributeError, IndexError:
            raise RuntimeError, 'Macro not found'
        #  
        # put parameters on the request, by saving the original context
        self.request.form, orig_form = kw, self.request.form
        content = self.header_macros.__of__(macroobj.aq_parent)(the_macro=the_macro)
        self.request.form = orig_form
        # Always encoded as utf-8
        content = force_unicode(content, 'utf')
        return content

    def issueAllPortalMessages(self):
        if hasattr(self.request.RESPONSE, 'cookies'):
            cookie = self.request.RESPONSE.cookies.get(STATUSMESSAGEKEY)
            if cookie:
                encodedstatusmessages = cookie['value']
                statusmessages = _decodeCookieValue(encodedstatusmessages)
            else:
                statusmessages = []
            for msg in statusmessages:
                self.getCommandSet('plone').issuePortalMessage(msg)
            self.request.RESPONSE.expireCookie(STATUSMESSAGEKEY, path='/')
