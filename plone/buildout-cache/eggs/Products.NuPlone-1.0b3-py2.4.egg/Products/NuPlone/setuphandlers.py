from StringIO import StringIO

from zope.component import getUtility
from zope.component import getMultiAdapter

from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from plone.app.portlets import portlets


def addSearchPortlet(portal, out):
    leftColumn = getUtility(IPortletManager, name=u'plone.leftcolumn', context=portal)
    left = getMultiAdapter((portal, leftColumn,), IPortletAssignmentMapping, context=portal)
    if u'portlets.Search' not in left:
        print >> out, "Adding search portlet to the left column"
        left[u'portlets.Search'] = portlets.search.Assignment()
        order = [left.keys()[-1]]+left.keys()[:-1]
        left.updateOrder(list(order))

def addLanguagePortlet(portal, out):
    leftColumn = getUtility(IPortletManager, name=u'plone.leftcolumn', context=portal)
    left = getMultiAdapter((portal, leftColumn,), IPortletAssignmentMapping, context=portal)
    if u'portlets.Language' not in left:
        print >> out, "Adding language portlet to the left column"
        left[u'portlets.Language'] = portlets.language.Assignment()
        order = [left.keys()[-1]]+left.keys()[:-1]
        left.updateOrder(list(order))


def importVarious(context):
    
    if context.readDataFile('nuplone_various.txt') is None:
        return
    
    site = context.getSite()
    out = StringIO()

    addSearchPortlet(site, out)
    addLanguagePortlet(site, out)
