from Testing.ZopeTestCase import installPackage
from Products.Five import zcml
from Products.Five import fiveconfigure


class PTSLayer:
    """ test layer for PTS """

    @classmethod
    def setUp(cls):
        # load zcml
        fiveconfigure.debug_mode = True
        import Products.PlacelessTranslationService
        zcml.load_config('configure.zcml', Products.PlacelessTranslationService)
        fiveconfigure.debug_mode = False
        # install package, import profile...
        installPackage('Products.PlacelessTranslationService', quiet=True)

    @classmethod
    def tearDown(cls):
        pass
