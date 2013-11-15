import unittest
import json
import pprint

from ccengine.providers.identity.identity_v2_0_api import IdentityAPIProvider
from testrepo.common.testfixtures.fixtures import BaseTestFixture


class IdentityConfigQuickCheck(BaseTestFixture):

    @classmethod
    def setUpClass(cls):
        super(IdentityConfigQuickCheck, cls).setUpClass()
        cls.identity_provider = IdentityAPIProvider(cls.config)

    def setUp(self):
        prov_resp = self.identity_provider.authenticate()
        assert prov_resp.entity is not None, \
                'Error deserializing identity authentication response, ' \
                'response entity object is none'
        self.response = prov_resp.response
        self.access = prov_resp.entity

    def test_identity_client(self):
        assert self.access.token is not None
        assert self.access.token.expires is not None
        assert self.access.token.id is not None

        assert self.access.user.id is not None
        assert self.access.user.name is not None
        assert self.access.user.roles is not None
        assert self.access.user.get_role(id='3') is not None
        assert self.access.user.get_role(name='identity:user-admin') \
                is not None
        assert self.access.user.get_role(id='3', name='identity:user-admin') \
                is not None
        assert self.access.serviceCatalog is not None

    @unittest.skip('Manual debug test')
    def test_print_identity_authentication_response(self):
        print '\nIdentity Authentication Response'
        data = json.loads(self.response.content)
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(data)
