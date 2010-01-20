
from kss.base.plugin import Plugin
from kss.demo.resource import (
    KSSDemo,
    KSSSeleniumTestDirectory,
    )

class CoreSyntaxDemos(Plugin):

    zope_demos = (
        KSSDemo('', 'Core syntax', "kss_selector_param.html", "Kss selector parameters"),
        KSSDemo('', 'Core syntax', "kss_url_param.html", "Kss url parameters"),
        KSSDemo('', 'Core syntax', "kss_selector_param_multiprop.html", "Kss selector parameters, with multiproperties"),
        KSSDemo('', 'Core syntax', "kss_url_param_multiprop.html", "Kss url parameters, with multiproperties"),
        KSSDemo('', 'Core syntax', "kss_client_action_alias.html", "Client action aliases"),
        )

    # directories are relative from the location of this .py file
    zope_selenium_testsuites = (
        KSSSeleniumTestDirectory('selenium_tests'),
        )
