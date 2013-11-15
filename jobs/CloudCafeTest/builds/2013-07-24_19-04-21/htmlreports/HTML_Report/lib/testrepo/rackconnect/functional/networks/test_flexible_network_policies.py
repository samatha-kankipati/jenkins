from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute import ItemNotFound
from ccengine.common.tools import datagen
from ccengine.domain.types import NovaServerStatusTypes as ServerStatus
from ccengine.domain.networks.isolated_network import IsolatedNetwork
from ccengine.common.constants.networks_constants import Constants
from testrepo.common.testfixtures.rackconnect import BaseRackConnectFixture


class TestFlexibleNetworkPolicies(BaseRackConnectFixture):
    @classmethod
    def setUpClass(cls):
        super(TestFlexibleNetworkPolicies, cls).setUpClass()
        cls.isolated_network = cls._create_isolated_network()
        cls.public_network = cls._network(Constants.PUBLIC_NETWORK_ID,
                                          Constants.PUBLIC_NETWORK_LABEL)
        cls.private_network = cls._network(Constants.PRIVATE_NETWORK_ID,
                                           Constants.PRIVATE_NETWORK_LABEL)
        cls.server_id = cls._create_server([cls.isolated_network,
                                            cls.private_network,
                                            cls.public_network])
        cls.servers_to_delete.append(cls.server_id)
        cls.interfaces = cls.list_virtual_interface(cls.server_id)

    @attr('rackconnect', 'network')
    def test_server_allowed_to_have_public_network(self):
        self._verify_network(self.interfaces, self.public_network, 2)

    @attr('rackconnect', 'network')
    def test_server_should_add_private_network(self):
        self._verify_network(self.interfaces, self.private_network, 1)

    @attr('rackconnect', 'network')
    def test_server_can_have_more_than_one_isolated_network(self):
        self._verify_network(self.interfaces, self.isolated_network, 1)
        network = self._create_isolated_network()
        self._create_virtual_interface(network)
        interfaces = self.list_virtual_interface(self.server_id)
        self._verify_network(interfaces, network, 2)