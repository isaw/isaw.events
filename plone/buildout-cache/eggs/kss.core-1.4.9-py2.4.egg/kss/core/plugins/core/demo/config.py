
from kss.base.plugin import Plugin
from kss.demo.resource import (
    KSSDemo,
    KSSSeleniumTestDirectory,
    )


##################
#
#
# THIS MODULE IS USED BY KSS.ZOPE DURING TRANSITION FROM KSS.CORE TO KSS.ZOPE
#
#
##################
class CoreDemos(Plugin):

    zope_demos = (
        ##disable address book because tbody problem needs to be fixed on IE
        ##KSSDemo('', 'Applications', "addressbook.html", "Addressbook"),
        KSSDemo('', 'Applications', "typewriter.html", "Typewriter"),
        KSSDemo('', 'Applications', "snake.html", "Snake"),
##      KSSDemo('', '',  "draganddrop.html", "Scriptaculous drag and drop"),
        KSSDemo('', 'Selectors', 'selectors.html', 'Parent node selector'),
        KSSDemo('', 'Core events', "kss_evt_preventbubbling.html", "Prevent bubbling KSS event parameter"),
        KSSDemo('', 'Core events', "kss_keyevents.html", "Key events"),
        KSSDemo('', 'Commands/Actions', "ca_focus.html", "Focus"),
        KSSDemo('', 'Commands/Actions', "ca_blur.html", "Blur"),
        KSSDemo('', 'Commands/Actions', "actions.html", "Class actions: toggle, add, remove"),
        KSSDemo('', 'Commands/Actions', "ca_cancel.html", "action-cancel"),
        KSSDemo('', 'Commands/Actions', "ca_kssattr.html", "setKssAttribute"),
        KSSDemo('', 'History', "basic_commands.html", "Change tag content"),
        KSSDemo('', 'History', "two_selects.html", "Two selects"),
        KSSDemo('', 'History', "autoupdate.html", "Auto update"),
        KSSDemo('', 'History', "inline_edit.html", "Inline edit"),
        KSSDemo('', 'History', "cancel_submit.html", "Cancel Submit Click"),
        KSSDemo('', 'History', "tree.html", "Tree"),
        KSSDemo('', 'History', "more_selectors.html", "More complex selectors"),
        KSSDemo('', 'History', "two_select_revisited.html", "Master-slave selects revisited"),
        KSSDemo('', 'History', "form_submit.html", "Form submit"),
        KSSDemo('', 'History', "effects.html", "Effects"),
        KSSDemo('', 'History', "error_handling.html", "Error handling"),
        KSSDemo('', 'History', "preventdefault.html", "Preventdefault (a.k.a. Safari workarounds)"),
        KSSDemo('', 'History', "html_inserts.html", "HTML insertions (Change tag content returns)"),
        KSSDemo('', 'History', "client-server-protocol", "Client server protocol"),
        # XXX this should go to the other plugin wuth all its stuff
        KSSDemo('Effects', '', "effects.html", "Effects"),
        )

    # directories are relative from the location of this .py file
    zope_selenium_testsuites = (
        KSSSeleniumTestDirectory('selenium_tests'),
        )
