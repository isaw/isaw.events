from Products.PloneTestCase.layer import PloneSite

class PloneCustomerize(PloneSite):
    # Derived layers *must* have setUp and tearDown
    # methods, even when they are empty.

    @classmethod
    def setUp(cls):
        pass

    @classmethod
    def tearDown(cls):
        pass
