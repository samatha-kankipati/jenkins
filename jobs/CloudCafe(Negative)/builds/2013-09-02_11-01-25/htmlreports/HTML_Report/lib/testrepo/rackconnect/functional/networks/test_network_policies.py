from ccengine.common.decorators import attr
from ccengine.domain.types import NovaServerStatusTypes as ServerStatus
from ccengine.common.exceptions.compute import ItemNotFound
from ccengine.common.constants.networks_constants import Constants
from testrepo.common.testfixtures.rackconnect import BaseRackConnectFixture


class TestNetworkPolicies(BaseRackConnectFixture):
    @classmethod
    def setUpClass(cls):
        super(TestNetworkPolicies, cls).setUpClass()
        server_id = cls._create_server([])
        cls.interfaces = cls.list_virtual_interface(server_id)

    @attr('rackconnect', 'network', 'negative')
    def test_server_should_not_have_public_network(self):
        self._verify_no_network(self.interfaces,
                                Constants.PUBLIC_NETWORK_LABEL)

    @attr('rackconnect', 'network', 'negative')
    def test_server_should_have_private_network(self):
        self._verify_network(self.interfaces,
                             Constants.PRIVATE_NETWORK_LABEL, 1)