
try:
    from Products.Five import BrowserView
    BrowserView
except ImportError:
    from zope.publisher.browser import BrowserView

from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from interfaces import IDevelView
from zope.interface import implements
from zope.traversing.interfaces import ITraverser
from zope.publisher.interfaces import NotFound

COOKIE_DEVELMODE = '__kss_devel'
COOKIE_LOGLEVEL = '__kss_loglevel'

class DevelView(BrowserView):
    implements(IDevelView)

    # Zope3 requires the implementation of
    # IBrowserPublisher, in order for the methods
    # to be traversable.
    #
    # An alternative would be:
    # <browser:pages class="...">
    #   <page name="..." attribute="..." />
    #   <page name="..." attribute="..." />
    # </browser:pages>

    def publishTraverse(self, request, name):
        try:
            return getattr(self, name)
        except AttributeError:
            raise NotFound(self.context, name, request)

    def browserDefault(self, request):
        # make ui the default method
        return self, ('ui', )

    # --
    # Methods for handling development/production mode
    # --

    def ison(self):
        '''Checks if running in development mode

        Two ways to induce development mode:

        - set the cookie on the request

        - switch portal_js tool into debug mode, this will
          select development mode without the cookie

        '''
        ison = COOKIE_DEVELMODE in self.request.cookies

        if not ison:
            # Check from javascript tool
            # XXX this should not be done from here, but I don't want to
            # modify other components yet.
            try:
                from Products.CMFCore.utils import getToolByName
                js_tool = getToolByName(self.context.aq_inner, 'portal_javascripts')
                ison = js_tool.getDebugMode()
            except:
                pass

        result = bool(ison)
        return result

    def isoff(self, REQUEST=None):
        'Check if running in production mode'
        result = not(self.ison())
        if REQUEST is not None:
            result = str(result)
        return result

    def set(self):
        'Sets development mode cookie'
        self.request.response.setCookie(COOKIE_DEVELMODE, '1', path='/')

    def unset(self):
        'Unsets development mode cookie'
        self.request.response.expireCookie(COOKIE_DEVELMODE, path='/')

    # --
    # Methods for detecting some browser versions
    # --

    def needs_old_cssquery(self):
        user_agent = self.request.get_header('User-Agent', '')
        safari_3_1 = 'Version/3.1' in user_agent and 'Safari' in user_agent
        # on Safari 3_1 the current base2 is broken, this check makes
        # it possible to serve the old cssquery instead of base2
        # on this version.
        # """User-Agent: Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_2; en-us) AppleWebKit/525.13 (KHTML, like Gecko) Version/3.1 Safari/525.13"""
        return safari_3_1

    # --
    # Methods for handling loglevel
    # --

    def getLogLevel(self, REQUEST=None):
        'Gets current log level'
        loglevel = self.request.cookies.get(COOKIE_LOGLEVEL, 'DEBUG').upper()
        return loglevel

    def setLogLevel(self, loglevel):
        'Sets loglevel cookie'
        self.request.response.setCookie(COOKIE_LOGLEVEL, loglevel, path='/')

    # --
    # User interface
    # --

    _ui = ViewPageTemplateFile('develui.pt', content_type='text/html;charset=utf-8')

    def ui(self):
        'User interface for interactive switching'
        options = {}
        # Handle development/production mode
        if 'devel' in self.request.form:
            self.set()
            # setting it also to have immediate effect in the page
            options['devel_mode'] = True
        if 'prod' in self.request.form:
            self.unset()
            if COOKIE_DEVELMODE in self.request.cookies:
                # setting it also to have immediate effect in the page
                options['devel_mode'] = False
        # Handle loglevel
        if 'loglevel' in self.request.form:
            loglevel =  self.request.form['loglevel']
            self.setLogLevel(loglevel)
            # setting it also to have immediate effect in the page
            options['loglevel'] = loglevel
        # Return the rendered template
        return self._ui(**options)

    def ui_js(self):
        'Javascript needed for the ui'
        resource = ITraverser(self.context).traverse('++resource++kss_devel_ui.js', 
                request=self.request)
        cooked = resource.GET()
        return cooked

    def ui_css(self):
        'CSS needed for the ui'
        resource = ITraverser(self.context).traverse('++resource++kss_devel_ui.css', 
                request=self.request)
        cooked = resource.GET()
        return cooked

    def ui_kss(self):
        'KSS needed for the ui'
        resource = ITraverser(self.context).traverse('++resource++kss_devel_ui.kss', 
                request=self.request)
        cooked = resource.GET()
        return cooked
