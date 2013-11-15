from ccengine.common.decorators import attr
from ccengine.domain.types import NovaServerStatusTypes as ServerStatus
from ccengine.common.constants.networks_constants import Constants
from testrepo.common.testfixtures.rackconnect import RackConnectNetworkFixture


class TestEnforcedNetworkPolicies(RackConnectNetworkFixture):
    @classmethod
    def setUpClass(cls):
        super(TestEnforcedNetworkPolicies, cls).setUpClass()
        cls.isolated_network = cls._create_isolated_network()
        cls.server = cls._create_server([cls.isolated_network])
        cls.interfaces = cls.list_virtual_interface(cls.server.id)

    @attr('rackconnect', 'network')
    def test_server_should_not_have_public_network(self):
        network = self._network(Constants.PUBLIC_NETWORK_ID,
                                Constants.PUBLIC_NETWORK_LABEL)
        self._verify_no_network(self.interfaces, network)

    @attr('rackconnect', 'network')
    def test_server_should_have_one_isolated_network(self):
        self._verify_network(self.interfaces, self.isolated_network, 1)

    @attr('rackconnect', 'network')
    def test_server_should_add_private_network(self):
        private_network = self._network(Constants.PRIVATE_NETWORK_ID,
                                        Constants.PRIVATE_NETWORK_LABEL)
        self._create_virtual_interface(private_network)
        interfaces = self.list_virtual_interface(self.server.id)
        self._verify_network(interfaces, private_network, 1)

    @attr('rackconnect', 'network')
    def test_server_should_not_allow_adding_public_network(self):
        public_network = self._network(Constants.PUBLIC_NETWORK_ID,
                                       Constants.PUBLIC_NETWORK_LABEL)
        response = self.networks_provider.client\
            .create_virtual_interface(self.server.id, public_network.id)
        self.assertEquals(response.status_code, 400)

    @attr('rackconnect', 'network')
    def test_server_should_not_have_more_than_one_isolated_network(self):
        network = self._create_isolated_network()
        response = self.networks_provider.client\
            .create_virtual_interface(self.server.id, network.id)
        self.assertEquals(response.status_code, 400)