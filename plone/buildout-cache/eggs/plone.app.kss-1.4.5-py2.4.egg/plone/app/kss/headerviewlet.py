from zope.interface import implements
from zope.component import getMultiAdapter
from zope.viewlet.interfaces import IViewlet

from Products.Five.browser import BrowserView

class KSSBaseUrlViewlet(BrowserView):
    """ Renders a link rel tag with the real url of the published object. """
    implements(IViewlet)

    def __init__(self, context, request, view, manager):
        super(KSSBaseUrlViewlet, self).__init__(context, request)
        self.__parent__ = view
        self.context = context
        self.request = request
        self.view = view
        self.manager = manager
        self.context_state = getMultiAdapter((context, request), name=u'plone_context_state')

    def update(self):
        pass

    def render(self):
        return u'<link rel="kss-base-url" href="%s" />' % self.context_state.object_url()
