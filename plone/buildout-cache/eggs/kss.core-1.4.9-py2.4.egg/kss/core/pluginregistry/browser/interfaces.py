

from zope.publisher.interfaces.browser import IBrowserPublisher

class IDevelView(IBrowserPublisher):

    def ison():
        '''Checks if running in development mode

        Two ways to induce development mode:

        - set the cookie on the request

        - switch portal_js tool into debug mode, this will
          select development mode without the cookie

        '''

    def isoff():
        'Check if running in production mode'

    def set():
        'Sets development mode cookie'

    def unset():
        'Unsets development mode cookie'

    def ui():
        'User interface for interactive switching'

    def ui_js():
        'Javascript needed for the ui'

    def ui_css():
        'CSS needed for the ui'

    def ui_kss():
        'KSS needed for the ui'


