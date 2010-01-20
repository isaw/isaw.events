from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase import PloneTestCase as ptc
from kss.core.tests.base import KSSViewTestCaseMixin
import plone.app.kss.tests, kss.core.tests
from Products.Five.zcml import load_config

class KSSAndPloneLayer(PloneSite):
    '''Since Plone sets up all zcml needed for kss, we only
    need to set up the additional registration needed for
    some tests, and for the command request introspection.
    '''
    @classmethod
    def setUp(cls):
        load_config('configure-unittest.zcml', package=kss.core.tests)
        load_config('configure-part_reloading.zcml',
                    package=plone.app.kss.tests)

    @classmethod
    def tearDown(cls):
        # XXX: tear down whatever was set up in configure-part_reloading
        # XXX XXX - How? (RB)
        pass
       
class KSSAndPloneTestCase(ptc.PloneTestCase, KSSViewTestCaseMixin):
    layer = KSSAndPloneLayer
