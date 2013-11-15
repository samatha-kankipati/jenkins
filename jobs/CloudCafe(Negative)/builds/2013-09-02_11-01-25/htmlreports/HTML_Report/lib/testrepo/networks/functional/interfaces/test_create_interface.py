from testrepo.common.testfixtures.networks import NetworksGatewayServerFixture
from ccengine.domain.types import NovaServerStatusTypes
from ccengine.common.decorators import attr


class TestCreateInterface(NetworksGatewayServerFixture):

    @attr('smoke', 'positive')
    def test_add_public_network_interface_with_isolated(self):
        '''Add public interface to server with only isolated network.'''
        public = self.networks_provider.get_public_network()
        networks = [{'uuid': self.shared_network.id}]
        r = self.servers_provider.create_active_server(networks=networks)
        server = r.entity
        self.servers_to_delete.append(server.id)
        r = self.networks_provider.client.create_virtual_interface(server.id,
                                                                   public.id)
        self.assertEquals(r.status_code, 200)
        new_interface = r.entity[0]
        server = self.servers_provider.servers_client.\
                                                get_server(server.id).entity
        self.helper.verify_interface(new_interface, server, public)
        r = self.networks_provider.client.list_virtual_interfaces(server.id)
        interface_list = r.entity
        self.assertEquals(len(interface_list), 2)
        self.helper.verify_interface_in_list(new_interface, interface_list,
                                             server, public)
        interface_details = self.networks_provider.get_interface(server.id,
                                                             public.id)
        self.helper.verify_interface(interface_details, server, public)

        if self.run_nvp:
            self.helper.verify_nvp_interface(interface_details, server, public)

    @attr('positive')
    def test_add_public_network_interface_with_private(self):
        '''Add public interface to server with only private network.'''
        public = self.networks_provider.get_public_network()
        private = self.networks_provider.get_private_network()
        networks = [{'uuid': private.id}]
        r = self.servers_provider.create_active_server(networks=networks)
        server = r.entity
        self.servers_to_delete.append(server.id)
        r = self.networks_provider.client.create_virtual_interface(server.id,
                                                                   public.id)
        self.assertEquals(r.status_code, 200)
        new_interface = r.entity[0]
        server = self.servers_provider.servers_client.\
                                                get_server(server.id).entity
        self.helper.verify_interface(new_interface, server, public)
        r = self.networks_provider.client.list_virtual_interfaces(server.id)
        interface_list = r.entity
        self.assertEquals(len(interface_list), 2)
        self.helper.verify_interface_in_list(new_interface, interface_list,
                                             server, public)
        interface_details = self.networks_provider.get_interface(server.id,
                                                             public.id)
        self.helper.verify_interface(interface_details, server, public)

        if self.run_nvp:
            self.helper.verify_nvp_interface(interface_details, server, public)

    @attr('smoke', 'positive')
    def test_add_private_network_interface_with_isolated(self):
        '''Add private interface to server with only isolated network.'''
        private = self.networks_provider.get_private_network()
        networks = [{'uuid': self.shared_network.id}]
        r = self.servers_provider.create_active_server(networks=networks)
        server = r.entity
        self.servers_to_delete.append(server.id)
        r = self.networks_provider.client.create_virtual_interface(server.id,
                                                                   private.id)
        self.assertEquals(r.status_code, 200)
        new_interface = r.entity[0]
        server = self.servers_provider.servers_client.\
                                                get_server(server.id).entity
        self.helper.verify_interface(new_interface, server, private)
        r = self.networks_provider.client.list_virtual_interfaces(server.id)
        interface_list = r.entity
        self.assertEquals(len(interface_list), 2)
        self.helper.verify_interface_in_list(new_interface, interface_list,
                                             server, private)
        interface_details = self.networks_provider.get_interface(server.id,
                                                             private.id)
        self.helper.verify_interface(interface_details, server, private)

        if self.run_nvp:
            self.helper.verify_nvp_interface(interface_details, server,
                                             private)

    @attr('positive')
    def test_add_private_network_interface_with_public(self):
        '''Add private interface to server with only public network.'''
        public = self.networks_provider.get_public_network()
        private = self.networks_provider.get_private_network()
        networks = [{'uuid': public.id}]
        r = self.servers_provider.create_active_server(networks=networks)
        server = r.entity
        self.servers_to_delete.append(server.id)
        r = self.networks_provider.client.create_virtual_interface(server.id,
                                                                   private.id)
        self.assertEquals(r.status_code, 200)
        new_interface = r.entity[0]
        server = self.servers_provider.servers_client.\
                                                get_server(server.id).entity
        self.helper.verify_interface(new_interface, server, private)
        r = self.networks_provider.client.list_virtual_interfaces(server.id)
        interface_list = r.entity
        self.assertEquals(len(interface_list), 2)
        self.helper.verify_interface_in_list(new_interface, interface_list,
                                             server, private)
        interface_details = self.networks_provider.get_interface(server.id,
                                                             private.id)
        self.helper.verify_interface(interface_details, server, private)

        if self.run_nvp:
            self.helper.verify_nvp_interface(interface_details, server,
                                             private)

    @attr('smoke', 'positive')
    def test_add_isolated_network_interface_with_public(self):
        '''Add isolated interface to server with only public network.'''
        public = self.networks_provider.get_public_network()
        networks = [{'uuid': public.id}]
        r = self.servers_provider.create_active_server(networks=networks)
        server = r.entity
        admin_pass = server.adminPass
        self.servers_to_delete.append(server.id)
        r = self.networks_provider.client.create_virtual_interface(server.id,
                                                        self.shared_network.id)
        self.assertEquals(r.status_code, 200)
        new_interface = r.entity[0]
        server = self.servers_provider.servers_client.\
                                                get_server(server.id).entity
        server.adminPass = admin_pass
        self.helper.verify_interface(new_interface, server,
                                     self.shared_network)
        r = self.networks_provider.client.list_virtual_interfaces(server.id)
        interface_list = r.entity
        self.assertEquals(len(interface_list), 2)
        self.helper.verify_interface_in_list(new_interface, interface_list,
                                             server, self.shared_network)

        interface_details = self.networks_provider.get_interface(server.id,
                                                        self.shared_network.id)
        self.helper.verify_interface(interface_details, server,
                                     self.shared_network)
        self.helper.verify_ifconfig(server, self.shared_network,
                                    self.gateway_server)
        if self.run_nvp:
            self.helper.verify_nvp_interface(interface_details, server,
                                             self.shared_network)

    @attr('positive')
    def test_add_isolated_network_interface_with_private(self):
        '''Add isolated interface to server with only private network.'''
        private = self.networks_provider.get_private_network()
        networks = [{'uuid': private.id}]
        r = self.servers_provider.create_active_server(networks=networks)
        server = r.entity
        self.servers_to_delete.append(server.id)
        r = self.networks_provider.client.create_virtual_interface(server.id,
                                                        self.shared_network.id)
        self.assertEquals(r.status_code, 200)
        new_interface = r.entity[0]
        server = self.servers_provider.servers_client.\
                                                get_server(server.id).entity
        self.helper.verify_interface(new_interface, server,
                                     self.shared_network)
        r = self.networks_provider.client.list_virtual_interfaces(server.id)
        interface_list = r.entity
        self.assertEquals(len(interface_list), 2)
        self.helper.verify_interface_in_list(new_interface, interface_list,
                                             server, self.shared_network)
        interface_details = self.networks_provider.get_interface(server.id,
                                                        self.shared_network.id)
        self.helper.verify_interface(interface_details, server,
                                     self.shared_network)

        if self.run_nvp:
            self.helper.verify_nvp_interface(interface_details, server,
                                             self.shared_network)

    @attr('smoke', 'positive')
    def test_add_isolated_network_interface_with_public_and_private(self):
        '''Add isolated interface to server with public and private network.'''
        r = self.servers_provider.create_active_server()
        server = r.entity
        self.servers_to_delete.append(server.id)
        r = self.networks_provider.client.create_virtual_interface(server.id,
                                                        self.shared_network.id)
        self.assertEquals(r.status_code, 200)
        new_interface = r.entity[0]
        server = self.servers_provider.servers_client.\
                                                get_server(server.id).entity
        self.helper.verify_interface(new_interface, server,
                                     self.shared_network)
        r = self.networks_provider.client.list_virtual_interfaces(server.id)
        interface_list = r.entity
        self.assertEquals(len(interface_list), 3)
        self.helper.verify_interface_in_list(new_interface, interface_list,
                                             server, self.shared_network)
        interface_details = self.networks_provider.get_interface(server.id,
                                                        self.shared_network.id)
        self.helper.verify_interface(interface_details, server,
                                     self.shared_network)
        if self.run_nvp:
            self.helper.verify_nvp_interface(interface_details, server,
                                             self.shared_network)

    @attr('positive')
    def test_add_public_network_interface_with_isolated_and_private(self):
        '''Add public interface to server with isolated and private network.'''
        public = self.networks_provider.get_public_network()
        private = self.networks_provider.get_private_network()
        networks = [{'uuid': self.shared_network.id}, {'uuid': private.id}]
        r = self.servers_provider.create_active_server(networks=networks)
        server = r.entity
        self.servers_to_delete.append(server.id)
        r = self.networks_provider.client.create_virtual_interface(server.id,
                                                                   public.id)
        self.assertEquals(r.status_code, 200)
        new_interface = r.entity[0]
        server = self.servers_provider.servers_client.\
                                                get_server(server.id).entity
        self.helper.verify_interface(new_interface, server, public)
        r = self.networks_provider.client.list_virtual_interfaces(server.id)
        interface_list = r.entity
        self.assertEquals(len(interface_list), 3)
        self.helper.verify_interface_in_list(new_interface, interface_list,
                                             server, public)
        interface_details = self.networks_provider.get_interface(server.id,
                                                             public.id)
        self.helper.verify_interface(interface_details, server, public)

        if self.run_nvp:
            self.helper.verify_nvp_interface(interface_details, server, public)

    @attr('positive')
    def test_add_private_network_interface_with_isolated_and_public(self):
        '''Add private interface to server with isolated and public network.'''
        public = self.networks_provider.get_public_network()
        private = self.networks_provider.get_private_network()
        networks = [{'uuid': public.id}, {'uuid': self.shared_network.id}]
        r = self.servers_provider.create_active_server(networks=networks)
        server = r.entity
        self.servers_to_delete.append(server.id)
        r = self.networks_provider.client.create_virtual_interface(server.id,
                                                                   private.id)
        self.assertEquals(r.status_code, 200)
        new_interface = r.entity[0]
        server = self.servers_provider.servers_client.\
                                                get_server(server.id).entity
        self.helper.verify_interface(new_interface, server, private)
        r = self.networks_provider.client.list_virtual_interfaces(server.id)
        interface_list = r.entity
        self.assertEquals(len(interface_list), 3)
        self.helper.verify_interface_in_list(new_interface, interface_list,
                                             server, private)
        interface_details = self.networks_provider.get_interface(server.id,
                                                             private.id)
        self.helper.verify_interface(interface_details, server, private)

        if self.run_nvp:
            self.helper.verify_nvp_interface(interface_details, server,
                                             private)

    @attr('positive')
    def test_add_isolated_network_interface_with_five_networks(self):
        '''Add interface to server with 5 networks, public, and private'''
        public = self.networks_provider.get_public_network()
        private = self.networks_provider.get_private_network()
        r = self.helper.create_server_with_n_networks(5,
                                                      [public.id,
                                                       private.id])[0]
        r = self.servers_provider.wait_for_server_status(r.entity.id,
                                                NovaServerStatusTypes.ACTIVE)
        self.assertEquals(r.status_code, 200)
        server = r.entity
        r = self.networks_provider.client.create_virtual_interface(server.id,
                                                        self.shared_network.id)
        self.assertEquals(r.status_code, 200)
        new_interface = r.entity[0]
        server = self.servers_provider.servers_client.\
                                                get_server(server.id).entity
        self.helper.verify_interface(new_interface, server,
                                     self.shared_network)
        r = self.networks_provider.client.list_virtual_interfaces(server.id)
        interface_list = r.entity
        self.assertEquals(len(interface_list), 8)
        self.helper.verify_interface_in_list(new_interface, interface_list,
                                             server, self.shared_network)
        interface_details = self.networks_provider.get_interface(server.id,
                                                        self.shared_network.id)
        self.helper.verify_interface(interface_details, server,
                                     self.shared_network)

        if self.run_nvp:
            self.helper.verify_nvp_interface(interface_details, server,
                                             self.shared_network)

    @attr('positive')
    def test_add_private_network_interface_with_six_networks(self):
        '''Add private interface to server with 6 networks and public'''
        public = self.networks_provider.get_public_network()
        private = self.networks_provider.get_private_network()
        r = self.helper.create_server_with_n_networks(6, [public.id])[0]
        r = self.servers_provider.wait_for_server_status(r.entity.id,
                                                NovaServerStatusTypes.ACTIVE)
        self.assertEquals(r.status_code, 200)
        server = r.entity
        r = self.networks_provider.client.create_virtual_interface(server.id,
                                                                   private.id)
        self.assertEquals(r.status_code, 200)
        new_interface = r.entity[0]
        server = self.servers_provider.servers_client.\
                                                get_server(server.id).entity
        self.helper.verify_interface(new_interface, server, private)
        r = self.networks_provider.client.list_virtual_interfaces(server.id)
        interface_list = r.entity
        self.assertEquals(len(interface_list), 8)
        self.helper.verify_interface_in_list(new_interface, interface_list,
                                             server, private)
        interface_details = self.networks_provider.get_interface(server.id,
                                                             private.id)
        self.helper.verify_interface(interface_details, server, private)

        if self.run_nvp:
            self.helper.verify_nvp_interface(interface_details, server,
                                             private)

    @attr('positive')
    def test_add_public_network_interface_with_six_networks(self):
        '''Add public interface to server with 6 networks and private'''
        public = self.networks_provider.get_public_network()
        private = self.networks_provider.get_private_network()
        r = self.helper.create_server_with_n_networks(6, [private.id])[0]
        r = self.servers_provider.wait_for_server_status(r.entity.id,
                                                NovaServerStatusTypes.ACTIVE)
        self.assertEquals(r.status_code, 200)
        server = r.entity
        r = self.networks_provider.client.create_virtual_interface(server.id,
                                                                   public.id)
        self.assertEquals(r.status_code, 200)
        new_interface = r.entity[0]
        server = self.servers_provider.servers_client.\
                                                get_server(server.id).entity
        self.helper.verify_interface(new_interface, server, public)
        r = self.networks_provider.client.list_virtual_interfaces(server.id)
        interface_list = r.entity
        self.assertEquals(len(interface_list), 8)
        self.helper.verify_interface_in_list(new_interface, interface_list,
                                             server, public)
        interface_details = self.networks_provider.get_interface(server.id,
                                                             public.id)
        self.helper.verify_interface(interface_details, server, public)

        if self.run_nvp:
            self.helper.verify_nvp_interface(interface_details, server, public)

    @attr('negative')
    def test_add_existing_interfaces(self):
        public = self.networks_provider.get_public_network()
        private = self.networks_provider.get_private_network()
        networks = [{'uuid': self.shared_network.id},
                    {'uuid': public.id},
                    {'uuid': private.id}]
        r = self.servers_provider.create_active_server(networks=networks)
        server = r.entity
        self.servers_to_delete.append(server.id)
        r = self.networks_provider.client.create_virtual_interface(server.id,
                                                                   public.id)
        self.assertEquals(r.status_code, 400,
                          'Existing public interface was allowed to be added')
        r = self.networks_provider.client.create_virtual_interface(server.id,
                                                                   private.id)
        self.assertEquals(r.status_code, 400,
                          'Existing private interface was allowed to be added')
        r = self.networks_provider.client.create_virtual_interface(server.id,
                                                        self.shared_network.id)
        self.assertEquals(r.status_code, 400,
                        'Existing isolated interface was allowed to be added')
