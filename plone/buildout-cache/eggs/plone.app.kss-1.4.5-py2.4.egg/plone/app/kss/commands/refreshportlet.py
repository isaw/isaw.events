from zope.deprecation import deprecate

from kss.core.BeautifulSoup import BeautifulSoup
from kss.core import CommandSet
from plone.app.portlets.utils import assignment_from_key
from plone.portlets.utils import unhashPortletInfo
from plone.portlets.interfaces import IPortletManager, IPortletRenderer
from plone.app.portlets.interfaces import IDeferredPortletRenderer
from zope.component import getMultiAdapter, getUtility

# XXX: This is deprecated and will be removed in Plone 4.0. Use the 'plone'
# command set instead.
class RefreshPortletCommand(CommandSet):
    
    @deprecate("The 'refreshportlet' command set is deprecated and will be removed in Plone 4.0. "
               "Please use the 'plone' command set instead.")
    def refreshPortletLegacy(self, name, nodeid=None, **kw):
        'Refresh portlet by name (old portlets)'
        if name.startswith('portlet-'):
            name = name[8:]
        if nodeid is None:
            nodeid = name
        # render it
        portlet_body = self.view.macroContent('portlet_%s/macros/portlet' % (name, ), **kw)
        # Good. Now, unfortunately we don't have any marker on the outside div.
        # So we just select the <dl> for insertion.
        # This could be spared with smarter templating.
        soup = BeautifulSoup(portlet_body)
        tag = soup.find('dl', id=nodeid)
        result = unicode(tag)
        # Command the replacement
        ksscore = self.getCommandSet('core')
        ksscore.replaceHTML(ksscore.getHtmlIdSelector(nodeid), result)

    @deprecate("The 'refreshportlet' command set is deprecated and will be removed in Plone 4.0. "
               "Please use the 'plone' command set instead.")
    def refreshPortlet(self, portlethash, **kw):
        'Refresh portlet by its hash (new portlets)'
        # put parameters on the request, by saving the original context
        self.request.form, orig_form = kw, self.request.form
        # Prepare the portlet and render the data
        info = unhashPortletInfo(portlethash) 
        manager = getUtility(IPortletManager, info['manager'])
        assignment = assignment_from_key(context = self.context, 
                                         manager_name = info['manager'], 
                                         category = info['category'],
                                         key = info['key'],
                                         name = info['name'])
        renderer = getMultiAdapter(
                (self.context, self.request, self.view, manager, assignment.data),
                IPortletRenderer
            )
        renderer = renderer.__of__(self.context)
        renderer.update()
        if IDeferredPortletRenderer.providedBy(renderer):
            # if this is a deferred load, prepare now the data
            renderer.deferred_update()
        result = renderer.render()
        # Revert the original request
        self.request.form = orig_form
        # Command the replacement
        wrapper_id = 'portletwrapper-%s' % portlethash
        ksscore = self.getCommandSet('core')
        ksscore.replaceInnerHTML(ksscore.getHtmlIdSelector(wrapper_id), result)
