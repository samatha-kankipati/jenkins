from ccengine.common.decorators import attr
from ccengine.domain.types import NovaRackConnectAutomationStatusTypes
from ccengine.providers.rackconnect.rcc_api import RackconnectProvider
from testrepo.common.testfixtures.rackconnect import RackConnectBaseFixture


class TestRackConnectDataCenter(RackConnectBaseFixture):
    @classmethod
    def setUpClass(cls):
        super(TestRackConnectDataCenter, cls).setUpClass()
        cls.rackconnect_provider = RackconnectProvider(
            cls.config, cls.fixture_log)

    @classmethod
    def _create_server(cls, image_ref, flavor_ref):
        response = cls.servers_provider.create_active_server(
            name=cls.config.rackconnect.rackconnect_initials,
            image_ref=image_ref, flavor_ref=flavor_ref)
        server = response.entity
        cls.servers_to_delete.append(server.id)
        return server

    @attr('rackconnect', 'datacenter')
    def test_ubuntu_server_rackconnect_deployment_successful(self):
        image_ref = self.config.rackconnect.ubuntu_image_ref
        flavor_ref = self.config.rackconnect.default_flavor_ref
        self._verify_server_rackconnected(image_ref, flavor_ref)

    @attr('rackconnect', 'datacenter')
    def test_centos_server_rackconnect_deployment_successful(self):
        image_ref = self.config.rackconnect.centos_image_ref
        flavor_ref = self.config.rackconnect.default_flavor_ref
        self._verify_server_rackconnected(image_ref, flavor_ref)

    @attr('rackconnect', 'datacenter')
    def test_windows_server_rackconnect_deployment_successful(self):
        image_ref = self.config.rackconnect.windows_image_ref
        flavor_ref = self.config.rackconnect.windows_flavor_ref
        self._verify_server_rackconnected(image_ref, flavor_ref)

    def _verify_server_rackconnected(self, image_ref, flavor_ref):
        server = self._create_server(image_ref, flavor_ref)
        self.rackconnect_provider.wait_for_rackconnect_deployed_status(
            server_id=server.id,
            status_to_wait_for=NovaRackConnectAutomationStatusTypes.ACTIVE)