from zope import schema
from zope.component import getMultiAdapter
from zope.component import queryUtility
from zope.formlib import form
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _

class IReviewPortlet(IPortletDataProvider):
    
    pass

class Assignment(base.Assignment):
    implements(IReviewPortlet)

    @property
    def title(self):
        return _(u"Review list")

class Renderer(base.Renderer):

    render = ViewPageTemplateFile('review.pt')

    @property
    def anonymous(self):
        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request),
                                       name=u'plone_portal_state')
        return portal_state.anonymous()

    @property
    def available(self):
        return not self.anonymous and len(self._data())

    def review_items(self):
        return self._data()

    def full_review_link(self):
        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request),
                                       name=u'plone_portal_state')
        return '%s/full_review_list' % portal_state.portal_url()

    @memoize
    def _data(self):
        if self.anonymous:
            return []
        context = aq_inner(self.context)
        workflow = getToolByName(context, 'portal_workflow')

        plone_view = getMultiAdapter((context, self.request), name=u'plone')
        getIcon = plone_view.getIcon
        toLocalizedTime = plone_view.toLocalizedTime

        idnormalizer = queryUtility(IIDNormalizer)
        norm = idnormalizer.normalize
        objects = workflow.getWorklistsResults()
        items = []
        for obj in objects:
            review_state = workflow.getInfoFor(obj, 'review_state')
            items.append(dict(
                path = obj.absolute_url(),
                title = obj.pretty_title_or_id(),
                description = obj.Description(),
                icon = getIcon(obj).html_tag(),
                creator = obj.Creator(),
                review_state = review_state,
                review_state_class = 'state-%s ' % norm(review_state),
                mod_date = toLocalizedTime(obj.ModificationDate()),
            ))
        return items


class AddForm(base.NullAddForm):
    form_fields = form.Fields(IReviewPortlet)
    label = _(u"Add Review Portlet")
    description = _(u"This portlet displays a queue of documents awaiting review.")

    def create(self):
        return Assignment()
