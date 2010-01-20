from zope import component
from zope.component import getMultiAdapter
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from kss.core.interfaces import IKSSView

from plone.app.kss.portlets import attributesModified

@component.adapter(None, IKSSView, IObjectModifiedEvent)
def attributesTriggerPortalTabsReload(obj, view, event):
    triggeringAttributes = ('title', 'description')
    if attributesModified(triggeringAttributes, event):
        ksscore = view.getCommandSet('core')
        selector = ksscore.getHtmlIdSelector('portal-globalnav')
        zopecommands = view.getCommandSet('zope')
        zopecommands.refreshViewlet(selector,
                                    'plone.portalheader',
                                    'plone.global_sections')

@component.adapter(None, IKSSView, IObjectModifiedEvent)
def attributesTriggerDocumentBylineReload(obj, view, event):
    ksscore = view.getCommandSet('core')
    selector = ksscore.getHtmlIdSelector('plone-document-byline')
    zopecommands = view.getCommandSet('zope')
    zopecommands.refreshViewlet(selector,
                                'plone.belowcontenttitle',
                                'plone.belowcontenttitle.documentbyline')

@component.adapter(None, IKSSView, IObjectModifiedEvent)
def attributesTriggerBreadcrumbsReload(obj, view, event):
    triggeringAttributes = ('title', 'description')
    if attributesModified(triggeringAttributes, event):
        ksscore = view.getCommandSet('core')
        selector = ksscore.getHtmlIdSelector('portal-breadcrumbs')
        zopecommands = view.getCommandSet('zope')
        zopecommands.refreshViewlet(selector,
                                    'plone.portaltop',
                                    'plone.path_bar')

@component.adapter(None, IKSSView, IObjectModifiedEvent)
def attributesTriggerHeadTitleReload(obj, view, event):
    triggeringAttributes = ('title', )
    if attributesModified(triggeringAttributes, event):
        htmlhead = getMultiAdapter((obj, view.request, view), name=u'plone.htmlhead')
        headtitle = getMultiAdapter((obj, view.request, view, htmlhead), name=u'plone.htmlhead.title')
        headtitle.update()
        ksscore = view.getCommandSet('core')
        ksscore.replaceHTML(
            'head title',
            headtitle.render(),
            withKssSetup='False')

