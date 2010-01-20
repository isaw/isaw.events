# -*- coding: UTF-8 -*-

from urlparse import urlsplit

from kss.core import kssaction, KSSExplicitError
from kss.core.BeautifulSoup import BeautifulSoup

from plone.app.layout.globals.interfaces import IViewView
from plone.locking.interfaces import ILockable

from zope.interface import alsoProvides
from zope.interface import implements
from zope.component import getMultiAdapter

from Acquisition import aq_inner
from Acquisition import aq_parent
from Acquisition import Implicit
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

from interfaces import IPloneKSSView
from plonekssview import PloneKSSView


class Acquirer(Implicit):
    # XXX the next should be best to avoid - but I don't know how!
    __allow_access_to_unprotected_subobjects__ = 1
    main_template = ZopeTwoPageTemplateFile('browser/main_template_standalone.pt')

def acquirerFactory(context):
    return context.aq_chain[0].__of__(Acquirer().__of__(aq_parent(context)))

def getCurrentContext(context):
    """ Check if context is default page in folder and/or portal
    """
    # check if context is default page
    context = aq_inner(context)
    context_state = context.restrictedTraverse('@@plone_context_state')
    portal = getToolByName(context, 'portal_url').getPortalObject()
    if context_state.is_default_page() and context != portal:
        context = aq_parent(context)
    return context


class ContentView(Implicit, PloneKSSView):

    implements(IPloneKSSView)
    
    # --
    # Replacing content region
    # --

    # Override main template in this context
    main_template2 = ZopeTwoPageTemplateFile('browser/main_template_standalone.pt')

    #@staticmethod
    def _filter_action(actions, id, found=None):
        if found is not None:
            return found
        for action in actions:
            if action['id'] == id:
                return action
    _filter_action = staticmethod(_filter_action)    # for zope 2.8 / python 2.3

    @kssaction
    def replaceContentRegion(self, url, tabid=''):
        '''Replace content region by tab id

        Usage::
            ul.contentViews li a:click {
            evt-click-preventdefault: True;
            action-server: replaceContentRegion;
            replaceContentRegion-tabid: nodeAttr(id, true);
            replaceContentRegion-url: nodeAttr(href);
            }

        REMARK:

        We use the acquisition context hack to replace the main template
        with one that only renders the content region. This means that if
        the target template reuses main_template we win. Otherwise we loose
        and we get a full page of which we have to take out the required
        part with BeautifulSoup.

        Warning ("Do you want to...") when we leave the page is not implemented.

        '''
        # REMARK on error handling: 
        # If KSSExplicitError is raised, the control will be passed
        # to the error handler defined on the client. I.e. for this rule,
        # the static plone-followLink should be activated. This means that
        # if this method decides it cannot handle the situation, it
        # raises this exception and we fallback to the non-AJAX behaviour.
        #
        # XXX The next checks could be left out - but we won't be able to change the tabs.
        # This could be solved with not using the tabs or doing server side quirks.
        # This affect management screens, for example, that are not real actions.
        # and unlock XXX
        context = aq_inner(self.context)
        lock = getMultiAdapter((context,self.request), name='plone_lock_operations')
        lock.safe_unlock()

        if not tabid or tabid == 'content':
            raise KSSExplicitError, 'No tabid on the tab'
        if not tabid.startswith('contentview-'):
            raise RuntimeError, 'Not a valid contentview id "%s"' % tabid
        # Split the url into it's components
        (proto, host, path, query, anchor) = urlsplit(url)
        # if the url doesn't use http(s) or has a query string or anchor
        # specification, don't bother
        if query or anchor or proto not in ('http', 'https'):
            raise KSSExplicitError, 'Unhandled protocol on the tab'
        # make the wrapping for the context, to overwrite main_template
        # note we have to use aq_chain[0] *not* aq_base.
        # XXX however just context would be good too? Hmmm
        wrapping = acquirerFactory(context)
        # Figure out the template to render.
        # We need the physical path which we can obtain from the url
        path = list(self.request.physicalPathFromURL(url))
        obj_path = list(context.getPhysicalPath())
        if path == obj_path:
            # target is the default view of the method.
            # url is like: ['http:', '', 'localhost:9777', 'kukitportlets', 'prefs_users_overview']
            # physical path is like: ('', 'kukitportlets')
            # We lookup the default view for the object, which may be
            # another object, if so we give up, otherwise we use the
            # appropriate template
            utils = getToolByName(context, 'plone_utils')
            if utils.getDefaultPage(context) is not None:
                raise KSSExplicitError, 'no default page on the tab'
            viewobj, viewpath = utils.browserDefault(context)
            if len(viewpath) == 1:
                viewpath = viewpath[0]
            template = viewobj.restrictedTraverse(viewpath)
        else:
            # see if it is a method on the same context object...
            # url is like: ['http:', '', 'localhost:9777', 'kukitportlets', 'prefs_users_overview']
            # physical path is like: ('', 'kukitportlets')
            if path[:-1] != obj_path:
                raise KSSExplicitError, 'cannot reload since the tab visits a different context'
            method = path[-1]
            # Action method may be a method alias: Attempt to resolve to a template.
            try:
                method = context.getTypeInfo().queryMethodID(method, default=method)
            except AttributeError:
                # Don't raise if we don't have a CMF 1.5 FTI
                pass
            template = wrapping.restrictedTraverse(method)
        # We render it
        content = template()
        # Now. We take out the required node from it!
        # We need this in any way, as we don't know if the template
        # actually used main_template! In that case we would have
        # the *whole* html which is wrong.
        soup = BeautifulSoup(content)
        replace_id = 'region-content'
        tag = soup.find('div', id=replace_id)
        if tag is None:
            raise RuntimeError, 'Result content did not contain <div id="%s">' % replace_id
        # now we send it back to the client
        result = unicode(tag)
        ksscore = self.getCommandSet('core')
        ksscore.replaceHTML(ksscore.getHtmlIdSelector(replace_id), result)
        # to remove old tab highlight,...
        ksscore.setAttribute(ksscore.getCssSelector("ul.contentViews li"), name='class', value='plain');
        # ... and put the highlight to the newly selected tab
        ksscore.setAttribute(ksscore.getHtmlIdSelector(tabid), name='class', value='selected');
        # Update the content menu to show them only in the "view"
        if tabid.endswith('view'):
            alsoProvides(self, IViewView)
        self.getCommandSet('plone').refreshContentMenu()


class ContentMenuView(Implicit, PloneKSSView):

    implements(IPloneKSSView, IViewView)
    
    @kssaction
    def cutObject(self):
        context = getCurrentContext(self.context)
        context.object_cut()
        self.getCommandSet('plone').refreshContentMenu()
        self.issueAllPortalMessages()
        self.cancelRedirect()

    @kssaction
    def copyObject(self):
        context = getCurrentContext(self.context)
        context.object_copy()
        self.getCommandSet('plone').refreshContentMenu()
        self.issueAllPortalMessages()
        self.cancelRedirect()

    @kssaction
    def changeViewTemplate(self, url):
        '''Replace content region after selecting template from drop-down.
        
        Usage::
            dl#templateMenu dd a:click {
            evt-click-preventdefault: True;
            action-server: changeViewTemplate;
            changeViewTemplate-url: nodeAttr(href);
            }

        REMARK:

        Cheat at the moment: we render down the whole page
        but take out the required part only
        This will be optimized more to replace the main template
        for the context of the call

        Warning when we leave the page is not implemented.
        '''
        templateid = url.split('templateId=')[-1].split('&')[0]
        context = getCurrentContext(self.context)
        wrapping = acquirerFactory(context)
        # XXX I believe selectViewTemplate script will be replaced by an
        # adapter or a view in the new implementation of CMFDynamicFTI
        context.selectViewTemplate(templateid)
        # Figure out the template to render.
        template = wrapping.restrictedTraverse(templateid)
        # We render it
        content = template()
        # Now. We take out the required node from it!
        # We need this in any way, as we don't know if the template
        # actually used main_template! In that case we would have
        # the *whole* html which is wrong.

        soup = BeautifulSoup(content)
        replace_id = 'region-content'
        tag = soup.find('div', id=replace_id)
        if tag is None:
            raise RuntimeError, 'Result content did not contain <div id="%s">' % replace_id
        # now we send it back to the client
        result = unicode(tag)
        ksscore = self.getCommandSet('core')
        ksscore.replaceHTML(ksscore.getHtmlIdSelector(replace_id), result)

        self.getCommandSet('plone').refreshContentMenu()
        self.issueAllPortalMessages()
        self.cancelRedirect()
        # XXX We need to take care of the URL history here,
        # For instance if we come from the edit page and change the view we
        # stay on the edit URL but with a view page

    @kssaction
    def changeWorkflowState(self, url):
        context = aq_inner(self.context)
        ksscore = self.getCommandSet('core')
        zopecommands = self.getCommandSet('zope')
        plonecommands = self.getCommandSet('plone')
        
        locking = ILockable(context, None)
        if locking is not None and not locking.can_safely_unlock():
            selector = ksscore.getHtmlIdSelector('plone-lock-status')
            zopecommands.refreshViewlet(selector, 'plone.abovecontent', 'plone.lockinfo')
            plonecommands.refreshContentMenu()
            return self.render()

        (proto, host, path, query, anchor) = urlsplit(url)
        if not path.endswith('content_status_modify'):
            raise KSSExplicitError, 'content_status_modify is not handled'
        action = query.split("workflow_action=")[-1].split('&')[0]
        context.content_status_modify(action)
        selector = ksscore.getCssSelector('.contentViews')
        zopecommands.refreshViewlet(selector, 'plone.contentviews', 'plone.contentviews')
        plonecommands.refreshContentMenu()
        self.issueAllPortalMessages()
        self.cancelRedirect()
