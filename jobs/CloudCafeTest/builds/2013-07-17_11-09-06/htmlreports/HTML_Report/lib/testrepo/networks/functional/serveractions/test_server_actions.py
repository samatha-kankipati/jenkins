from testrepo.common.testfixtures.networks import NetworksServerActionsFixture
from ccengine.domain.types import NovaServerStatusTypes
import unittest2
from ccengine.common.decorators import attr


class TestServerActions(NetworksServerActionsFixture):

    @attr('positive')
    def test_net_config_build_server_from_snapshot(self):
        '''Snapshots do not include network configuration (BUILD).'''
        self._shared_server_sanity_check()
        r = self.servers_provider.create_active_server(
                                                image_ref=self.shared_image.id)
        self.servers_to_delete.append(r.entity.id)
        r = self.servers_provider.servers_client.get_server(r.entity.id)
        shared_net = r.entity.addresses.get_by_name(self.shared_network.label)
        self.assertIsNone(shared_net)

    @attr('positive')
    def test_net_config_rebuild_server_from_snapshot(self):
        '''Snapshots do not include networks configurations (REBUILD).'''
        self._shared_server_sanity_check()
        r = self.servers_provider.create_active_server()
        server1 = r.entity
        r = self.servers_provider.servers_client.rebuild(
                                     server1.id,
                                     name=server1.name,
                                     image_ref=self.shared_image.id,
                                     flavor_ref=server1.flavor.id,
                                     admin_pass=server1.adminPass)
        self.assertEquals(r.status_code, 202, 'Rebuild status code incorrect')
        r = self.servers_provider.wait_for_server_status(server1.id,
                                                  NovaServerStatusTypes.ACTIVE)
        shared_net = r.entity.addresses.get_by_name(self.shared_network.label)
        self.assertIsNone(shared_net)

    @attr('positive')
    def test_server_rebuild_network_configuration(self):
        '''Verify network configuration remains after server rebuild.'''
        self._shared_server_sanity_check()
        r = self.servers_provider.servers_client.rebuild(
                                 self.shared_server.id,
                                 name=self.shared_server.name,
                                 image_ref=self.shared_image.id,
                                 flavor_ref=self.shared_server.flavor.id,
                                 admin_pass=self.shared_server.adminPass)
        self.assertEquals(r.status_code, 204, 'Rebuild status code incorrect')
        r = self.servers_provider.wait_for_server_status(self.shared_server.id,
                                                NovaServerStatusTypes.ACTIVE)
        r.entity.adminPass = self.shared_server.adminPass
        self.shared_server = r.entity
        self.assertIsNotNone(self.shared_server.addresses.\
                             get_by_name(self.shared_network.label))
        self.assertIsNotNone(self.shared_server.addresses.public)
        self.assertIsNone(self.shared_server.addresses.private)

    @attr('positive')
    def test_server_resize_network_configuration(self):
        '''Verify network configuration remains after server resize.'''
        self._shared_server_sanity_check()
        new_flavor = self.config.compute_api.flavor_ref
        if new_flavor == '2':
            new_flavor = '3'
        else:
            new_flavor = '2'
        r = self.servers_provider.servers_client.resize(self.shared_server.id,
                                                        new_flavor)
        self.assertEquals(r.status_code, 202, 'Resize status code incorrect')
        r = self.servers_provider.wait_for_server_status(self.shared_server.id,
                                        NovaServerStatusTypes.VERIFY_RESIZE)
        r.entity.adminPass = self.shared_server.adminPass
        self.shared_server = r.entity
        self.assertIsNotNone(self.shared_server.addresses.\
                             get_by_name(self.shared_network.label))
        self.assertIsNotNone(self.shared_server.addresses.public)
        self.assertIsNone(self.shared_server.addresses.private)
        r = self.servers_provider.servers_client.confirm_resize(
                                                        self.shared_server.id)
        self.assertEquals(r.status_code, 202,
                          'Confirm resize status code incorrect.')
        r = self.servers_provider.wait_for_server_status(self.shared_server.id,
                                            NovaServerStatusTypes.ACTIVE)
        r.entity.adminPass = self.shared_server.adminPass
        self.shared_server = r.entity
        self.assertIsNotNone(self.shared_server.addresses.\
                             get_by_name(self.shared_network.label))
        self.assertIsNotNone(self.shared_server.addresses.public)
        self.assertIsNone(self.shared_server.addresses.private)

    @attr('positive')
    def test_rescue_server_maintains_network_connectivity(self):
        '''Verify network connectivity remains after server rescue.'''
        self._shared_server_sanity_check()
        r = self.servers_provider.servers_client.rescue(self.shared_server.id)
        self.assertEquals(r.status_code, 200, 'Rescue status code incorrect')
        r = self.servers_provider.wait_for_server_status(self.shared_server.id,
                                                NovaServerStatusTypes.RESCUE)
        temp_pass = self.shared_server.adminPass
        self.shared_server = r.entity
        self.shared_server.adminPass = temp_pass
        self.assertIsNotNone(self.shared_server.addresses.\
                             get_by_name(self.shared_network.label))
        self.assertIsNotNone(self.shared_server.addresses.public)
        self.assertIsNone(self.shared_server.addresses.private)
        r = self.servers_provider.servers_client.unrescue(
                                                        self.shared_server.id)
        self.assertEquals(r.status_code, 202, 'Unrescue status code incorrect')
        r = self.servers_provider.wait_for_server_status(self.shared_server.id,
                                                NovaServerStatusTypes.ACTIVE)
        temp_pass = self.shared_server.adminPass
        self.shared_server = r.entity
        self.shared_server.adminPass = temp_pass
        self.assertIsNotNone(self.shared_server.addresses.\
                             get_by_name(self.shared_network.label))
        self.assertIsNotNone(self.shared_server.addresses.public)
        self.assertIsNone(self.shared_server.addresses.private)

    @unittest2.skip('Need to find out how to suspend and pause a server.')
    @attr('positive', 'new')
    def test_suspend_pause_events_maintain_network_connectivity(self):
        '''Verify network connectivity remains after suspension and pause.'''
        pass

    def _shared_server_sanity_check(self):
        r = self.servers_provider.servers_client.get_server(
                                                        self.shared_server.id)
        if r.entity.status == NovaServerStatusTypes.ERROR:
            network_list = [{'uuid': self.shared_network.id},
                    {'uuid': self.networks_provider.get_public_network().id}]
            r = self.servers_provider.servers_client.create_active_server(
                                    name=r.entity.name, networks=network_list)
            self.shared_server.adminPass = r.entity.adminPass
        if (r.entity.status == NovaServerStatusTypes.BUILD or
            r.entity.status == NovaServerStatusTypes.REBUILD):
            r = self.servers_provider.wait_for_server_status(r.entity.id,
                                                  NovaServerStatusTypes.ACTIVE)
        if r.entity.status == NovaServerStatusTypes.PREP_RESCUE:
            r = self.servers_provider.wait_for_server_status(r.entity.id,
                                                  NovaServerStatusTypes.RESCUE)
        if r.entity.status == NovaServerStatusTypes.RESCUE:
            r = self.servers_provider.servers_client.unrescue(
                                                        self.shared_server.id)
            r = self.servers_provider.wait_for_server_status(r.entity.id,
                                                  NovaServerStatusTypes.ACTIVE)
        if r.entity.status == NovaServerStatusTypes.RESIZE:
            r = self.servers_provider.wait_for_server_status(r.entity.id,
                                        NovaServerStatusTypes.VERIFY_RESIZE)
        if r.entity.status == NovaServerStatusTypes.VERIFY_RESIZE:
            self.servers_provider.servers_client.confirm_resize(r.entity.id)
            r = self.servers_provider.wait_for_server_status(r.entity.id,
                                                NovaServerStatusTypes.ACTIVE)
        temp_pass = self.shared_server.adminPass
        self.shared_server = r.entity
        self.shared_server.adminPass = temp_pass
