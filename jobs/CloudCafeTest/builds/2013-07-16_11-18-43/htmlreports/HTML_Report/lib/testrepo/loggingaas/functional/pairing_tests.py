from testrepo.common.testfixtures.loggingaas import PairingFixture


class PairingFunctionalTests(PairingFixture):
    @classmethod
    def setUpClass(cls):
        super(PairingFunctionalTests, cls).setUpClass()

    def setUp(self):
        super(PairingFunctionalTests, self).setUp()

    def tearDown(self):
        pass

    def test_creation_of_invalid_personality(self):
        """
        Tests Meniscus issue #122
        Should return a 400 when attempting to pair with an invalid personality
        """
        pair_resp = self.provider.pair_worker(personality='correlation')
        self.assertEquals(400, pair_resp.status_code,
                          msg="Creation should have failed")