
from kss.demo.interfaces import (
    IKSSDemoResource,
    IKSSSeleniumTestResource,
    )
from kss.demo.resource import (
    KSSDemo,
    KSSSeleniumTestDirectory,
    )
from zope.interface import implements

# Create a mesh of provided interfaces
# This is needed, because an utility must have a single interface.
class IResource(IKSSDemoResource, IKSSSeleniumTestResource):
    pass

class KSSCoreDemos(object):
    implements(IResource)

    demos = (
        ##disable address book because tbody problem needs to be fixed on IE
        ##KSSDemo('', 'Applications',         "addressbook.html",             "Addressbook",
        ##        description = 'Small Addressbook application'),
        KSSDemo('', 'Applications',         "typewriter.html",              "Typewriter",
                description = 'Typewriter application for learning typewriting',
                helpfile = 'typewriter.rst',
                packageName = 'kss.core.plugins.core.demo'),
        KSSDemo('', 'Applications', "snake.html", "Snake",
                description = 'A simple implementation of the infamous snake game',
                helpfile = 'snake.rst',
                packageName = 'kss.core.plugins.core.demo'),
##      KSSDemo('', '',  "draganddrop.html", "Scriptaculous drag and drop"),
        KSSDemo('', 'Parameter functions', 'pf_forms.html',                 'Forms'),
        KSSDemo('', 'Selectors',            'selectors.html',               'Parent node selector'),
        KSSDemo('', 'Core syntax',          "kss_selector_param.html",      "Kss selector parameters"),
        KSSDemo('', 'Core syntax',          "kss_url_param.html",           "Kss url parameters"),
        KSSDemo('', 'Core events',          "kss_evt_preventbubbling.html", "Prevent bubbling KSS event parameter"),
        KSSDemo('', 'Core events',          "kss_keyevents.html",           "Key events"),
        KSSDemo('', 'Commands/Actions',     "ca_focus.html",                "Focus"),
        KSSDemo('', 'Commands/Actions',     "ca_blur.html",                 "Blur"),
        KSSDemo('', 'Commands/Actions',     "ca_cancel.html",               "action-cancel"),
        KSSDemo('', 'Commands/Actions',     "ca_kssattr.html",              "setKssAttribute"),
        KSSDemo('', 'Commands/Actions',     "actions.html",                 "Class actions: toggle, add, remove"),
        KSSDemo('', 'History',              "basic_commands.html",          "Change tag content"),
        KSSDemo('', 'History',              "two_selects.html",             "Two selects"),
        KSSDemo('', 'History',              "autoupdate.html",              "Auto update"),
        KSSDemo('', 'History',              "inline_edit.html",             "Inline edit"),
        KSSDemo('', 'History',              "cancel_submit.html",           "Cancel Submit Click"),
        KSSDemo('', 'History',              "tree.html",                    "Tree"),
        KSSDemo('', 'History',              "more_selectors.html",          "More complex selectors"),
        KSSDemo('', 'History',              "two_select_revisited.html",    "Master-slave selects revisited"),
        KSSDemo('', 'History',              "form_submit.html",             "Form submit"),
        KSSDemo('', 'History',              "effects.html",                 "Effects"),
        KSSDemo('', 'History',              "error_handling.html",          "Error handling"),
        KSSDemo('', 'History',              "preventdefault.html",          "Preventdefault (a.k.a. Safari workarounds)"),
        KSSDemo('', 'History',              "html_inserts.html",            "HTML insertions (Change tag content returns)"),
        KSSDemo('', 'History',              "client-server-protocol",       "Client server protocol"),
        )

    # directories are relative from the location of this .py file
    selenium_tests = (
        KSSSeleniumTestDirectory('selenium_tests'),
        )
