
from kss.base.plugin import Plugin
from kss.demo.resource import (
    KSSDemo,
    KSSSeleniumTestDirectory,
    )

class ValueProviderDemos(Plugin):

    zope_demos = (
        KSSDemo('', 'Value providers', 'pf_forms.html', 'Forms'),
        KSSDemo('', 'Value providers', 'kss_form_submit_multiprop.html', 'Form submit, with multiproperties'),
        )

    # directories are relative from the location of this .py file
    zope_selenium_testsuites = (
        KSSSeleniumTestDirectory('selenium_tests'),
        )
