import unittest

from testrepo.common.testfixtures.auth import IdentityFixture


class AuthConfigQuickCheck(IdentityFixture):

    @classmethod
    def setUpClass(cls):
        super(AuthConfigQuickCheck, cls).setUpClass()

    @unittest.skip('This is more of a tool than a test')
    def test_print_service_catalog(self):
        auth_data = self.client.authenticate()
        auth_data.print_auth_response()
        pass
