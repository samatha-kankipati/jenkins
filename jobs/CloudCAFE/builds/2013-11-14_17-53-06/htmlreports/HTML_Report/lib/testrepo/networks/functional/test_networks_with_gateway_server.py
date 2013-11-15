from testrepo.common.testfixtures.networks import NetworksGatewayServerFixture
from ccengine.domain.types import NovaServerStatusTypes
from ccengine.common.connectors.ssh import SSHConnector
from ccengine.common.decorators import attr
import re
import ccengine.common.tools.datagen as datagen
import os
import ccengine.common.tools.sshtools as sshtools


class TestNetworksGatewayServer(NetworksGatewayServerFixture):

    @attr('smoke', 'positive')
    def test_interfaces_created_correctly(self):
        '''Interfaces are created and network IP is correctly assigned.'''
        ssh = SSHConnector(self.gateway_ip, 'root',
                           self.gateway_server.adminPass, tcp_timeout=10)
        ssh.start_shell()
        output = ssh.exec_shell_command('ifconfig\n')[0]
        self.assertTrue(output.find('eth0') != -1)
        cidr = self.shared_network.cidr
        cidr = cidr[:cidr.rfind('.') + 1]
        regex = ''.join(['eth1.+inet addr:', cidr, '.+Bcast'])
        matches = re.search(regex, output, re.DOTALL)
        self.assertIsNotNone(matches)

    @attr('smoke', 'positive')
    def test_network_communication_between_servers(self):
        '''Servers on same network can communicate with each other.'''
        server1_name = datagen.random_string('net-comm-server1')
        server1_networks = [{'uuid':self.shared_network.id}]
        server2_name = datagen.random_string('net-comm-server2')
        server2_networks = [{'uuid':self.shared_network.id}]
        r = self.servers_provider.servers_client.create_server(
                                 name=server1_name,
                                 image_ref=self.config.compute_api.image_ref,
                                 flavor_ref=self.config.compute_api.flavor_ref,
                                 networks=server1_networks)
        server1 = r.entity
        r = self.servers_provider.servers_client.create_server(
                                 name=server2_name,
                                 image_ref=self.config.compute_api.image_ref,
                                 flavor_ref=self.config.compute_api.flavor_ref,
                                 networks=server2_networks)
        server2 = r.entity
        self.servers_to_delete.append(server1.id)
        self.servers_to_delete.append(server2.id)
        self.servers_provider.wait_for_server_status(server1.id,
                                              NovaServerStatusTypes.ACTIVE)
        self.servers_provider.wait_for_server_status(server2.id,
                                              NovaServerStatusTypes.ACTIVE)
        admin_pass1 = server1.adminPass
        admin_pass2 = server2.adminPass
        r = self.servers_provider.servers_client.get_server(server1.id)
        server1 = r.entity
        r = self.servers_provider.servers_client.get_server(server2.id)
        server2 = r.entity
        server1.adminPass = admin_pass1
        server2.adminPass = admin_pass2

        # Check the servers are on the same network
        msg = 'Server {0} did not get attached to network {1} correctly'
        self.assertIsNotNone(server1.addresses.get_by_name(
            self.shared_network.label), msg.format(server1.id,
                self.shared_network.label))
        self.assertIsNotNone(server2.addresses.get_by_name(
            self.shared_network.label), msg.format(server2.id,
                self.shared_network.label))
        server1.adminPass = admin_pass1
        server2.adminPass = admin_pass2

        # Check there is connectivity between servers on the same network
        self._remote_ssh(server1=server1, server2=server2,
            network1=self.shared_network, network2=self.shared_network,
            connection=True, retries=self.ssh_retries)

    @attr('smoke', 'positive')
    def test_network_communication_between_servers_on_diff_network(self):
        '''Servers on different network cannot communicate with each other.'''
        test_net = self.create_ipv4_network(
            name_starts_with='diff_net_comm_network', prefix='192.168.*.0')
        self.networks_to_delete.append(test_net.id)
        server1_name = datagen.random_string('diff-net-comm-server1')
        server1_networks = [{'uuid':self.shared_network.id}]
        server2_name = datagen.random_string('diff-net-comm-server2')
        server2_networks = [{'uuid':test_net.id}]
        r = self.servers_provider.servers_client.create_server(
                                 name=server1_name,
                                 image_ref=self.config.compute_api.image_ref,
                                 flavor_ref=self.config.compute_api.flavor_ref,
                                 networks=server1_networks)
        server1 = r.entity
        r = self.servers_provider.servers_client.create_server(
                                 name=server2_name,
                                 image_ref=self.config.compute_api.image_ref,
                                 flavor_ref=self.config.compute_api.flavor_ref,
                                 networks=server2_networks)
        server2 = r.entity
        self.servers_to_delete.append(server1.id)
        self.servers_to_delete.append(server2.id)
        self.servers_provider.wait_for_server_status(server1.id,
                                              NovaServerStatusTypes.ACTIVE)
        self.servers_provider.wait_for_server_status(server2.id,
                                              NovaServerStatusTypes.ACTIVE)
        admin_pass1 = server1.adminPass
        admin_pass2 = server2.adminPass
        r = self.servers_provider.servers_client.get_server(server1.id)
        server1 = r.entity
        r = self.servers_provider.servers_client.get_server(server2.id)
        server2 = r.entity

        server1.adminPass = admin_pass1
        server2.adminPass = admin_pass2

        # Check the servers have different networks
        msg = 'Server {0} did not get attached to network {1} correctly'
        self.assertIsNotNone(server1.addresses.get_by_name(
            self.shared_network.label), msg.format(server1.id,
                self.shared_network.label))
        self.assertIsNotNone(server2.addresses.get_by_name(test_net.label),
            msg.format(server2.id, test_net.label))

        # Check there is not connectivity between servers on different network
        self._remote_ssh(server1, server2, network1=self.shared_network,
            network2=test_net, connection=False, retries=self.ssh_retries)

    @attr('positive', 'again')
    def test_server_see_traffic_from_other_networks(self):
        '''Can a server attached to a network see traffic from other networks
        '''
        cidr = datagen.random_cidr(mask=24)
        label = datagen.random_string('traffic_other_network')
        r = self.networks_provider.client.create_network(cidr=cidr,
                                                         label=label)
        self.networks_to_delete.append(r.entity.id)
        other_net = r.entity
        server1_name = datagen.random_string('server1')
        server1_networks = [{'uuid':self.shared_network.id}]
        other_gw_name = datagen.random_string('traffic-gw-server')
        other_gw_networks = [{'uuid':other_net.id},
                    {'uuid':self.networks_provider.get_public_network().id}]
        other_server_name = datagen.random_string('traffic-server')
        other_server_networks = [{'uuid':other_net.id}]
        r = self.servers_provider.servers_client.create_server(
                                 name=server1_name,
                                 image_ref=self.config.compute_api.image_ref,
                                 flavor_ref=self.config.compute_api.flavor_ref,
                                 networks=server1_networks)
        self.servers_to_delete.append(r.entity.id)
        server1 = r.entity
        r = self.servers_provider.servers_client.create_server(
                                 name=other_gw_name,
                                 image_ref=self.config.compute_api.image_ref,
                                 flavor_ref=self.config.compute_api.flavor_ref,
                                 networks=other_gw_networks)
        self.servers_to_delete.append(r.entity.id)
        other_gateway_server = r.entity
        r = self.servers_provider.servers_client.create_server(
                                 name=other_server_name,
                                 image_ref=self.config.compute_api.image_ref,
                                 flavor_ref=self.config.compute_api.flavor_ref,
                                 networks=other_server_networks)
        self.servers_to_delete.append(r.entity.id)
        other_server = r.entity
        r = self.servers_provider.wait_for_server_status(server1.id,
                                                  NovaServerStatusTypes.ACTIVE)
        r.entity.adminPass = server1.adminPass
        server1 = r.entity
        r = self.servers_provider.wait_for_server_status(
                                                  other_gateway_server.id,
                                                  NovaServerStatusTypes.ACTIVE)
        r.entity.adminPass = other_gateway_server.adminPass
        other_gateway_server = r.entity
        r = self.servers_provider.wait_for_server_status(other_server.id,
                                                  NovaServerStatusTypes.ACTIVE)
        r.entity.adminPass = other_server.adminPass
        other_server = r.entity
        normal_ssh = SSHConnector(self.gateway_ip, 'root',
                                  self.gateway_server.adminPass, tcp_timeout=10)
        other_gw_ip = other_gateway_server.addresses.public.ipv4
        other_ssh = SSHConnector(other_gw_ip, 'root',
                                  other_gateway_server.adminPass, tcp_timeout=10)
        normal_ssh.start_shell()
        ip1 = server1.addresses.get_by_name(self.shared_network.label).ipv4
        output, prompt = normal_ssh.exec_shell_command(
                                                ' '.join(['ping', ip1, '\n']))
#        ip1_login = '@'.join(['root', ip1])
#        ip1_ssh_comm = ''.join(['ssh -o StrictHostKeyChecking=no ',
#                                ip1_login, '\n'])
#        normal_ssh.exec_shell_command(ip1_ssh_comm)
#        normal_ssh.exec_shell_command(''.join([server1.adminPass, '\n']))
        other_ssh.start_shell()
        other_ip = other_server.addresses.get_by_name(other_net.label).ipv4
        other_ip_login = '@'.join(['root', other_ip])
        other_ip_ssh_comm = ' '.join(['ssh -o StrictHostKeyChecking=no',
                                      other_ip_login, '\n'])
        other_ssh.exec_shell_command(other_ip_ssh_comm)
        other_ssh.exec_shell_command(''.join([other_server.adminPass, '\n']))

    @attr('positive')
    def test_network_change_by_another_user(self):
        '''Can a network be used or changed by another user.'''
        r = self.alt_networks_provider.client.get_network(
                                                        self.shared_network.id)
        self.assertEquals(r.status_code, 404)
        r = self.alt_networks_provider.client.delete_network(
                                                        self.shared_network.id)
        self.assertEquals(r.status_code, 404)
        network_ids = [{'uuid':self.shared_network.id}]
        r = self.alt_servers_provider.\
                                    create_active_server(networks=network_ids)
        self.alt_servers_to_delete.append(r.entity.id)
        self.assertEquals(r.entity.status, NovaServerStatusTypes.ERROR)
        self.assertIsNone(
                    r.entity.addresses.get_by_name(self.shared_network.label))
        r = self.alt_networks_provider.client.create_network(
                                                    self.shared_network.cidr,
                                                    self.shared_network.label)
        self.alt_networks_to_delete.append(r.entity.id)
        alt_shared_network = r.entity
        network_ids = [{'uuid':alt_shared_network.id},
                {'uuid':self.alt_networks_provider.get_public_network().id}]
        r = self.alt_servers_provider.\
                                    create_active_server(networks=network_ids)
        self.alt_servers_to_delete.append(r.entity.id)
        alt_server_adminPass = r.entity.adminPass
        r = self.alt_servers_provider.servers_client.get_server(r.entity.id)
        alt_server = r.entity
        alt_server_pub_ip = alt_server.addresses.public.ipv4
        ssh = SSHConnector(alt_server_pub_ip, 'root', alt_server_adminPass,
                        tcp_timeout=10)
        ssh.start_shell()
        private_gateway_ip = self.gateway_server.addresses.\
                             get_by_name(self.shared_network.label).ipv4
        ip1_login = '@'.join(['root', private_gateway_ip])
        ip1_ssh_comm = ''.join(['ssh -o StrictHostKeyChecking=no ',
                                ip1_login, '\n'])
        output, prompt = ssh.exec_shell_command(ip1_ssh_comm)
        self.assertTrue(prompt.find('password') != -1, ''.join(['SSH Failed: ',
                                                                output]))
        #should not be allowed to login because the adminPass accepted is for
        #the alt user's server, not the normal gateway server
        output, prompt = ssh.exec_shell_command(
                                ''.join([self.gateway_server.adminPass, '\n']))
        self.assertTrue(prompt.find(self.gateway_server.name) == -1,
                        ''.join(['SSH from from alt user into main users ',
                                 'server allowed.', output]))
        ssh.end_shell()

    @attr('positive', 'again')
    def test_public_interface_disabled(self):
        '''Disabling public interface ensures it cannot be accessed publicly.
        '''
        prompt_gws_name = self.gateway_server.name.replace('_', '-')
        pub_net = self.networks_provider.get_public_network()
        server1_name = datagen.random_string('disable-pub-interface-server1')
        server1_networks = [{'uuid':self.shared_network.id},
                            {'uuid':pub_net.id}]
        r = self.servers_provider.create_active_server(name=server1_name,
                                                    networks=server1_networks)
        server1 = r.entity
        admin_pass1 = server1.adminPass
        self.servers_to_delete.append(server1.id)
        self.assertEquals(r.status_code, 200)
        r = self.servers_provider.servers_client.get_server(server1.id)
        server1 = r.entity
        shared_ip1 = server1.addresses.\
                                get_by_name(self.shared_network.label).ipv4
        pub_ip1 = server1.addresses.public.ipv4
        ssh = SSHConnector(self.gateway_ip, 'root',
                           self.gateway_server.adminPass, tcp_timeout=10)
        ssh.start_shell()
        pub_ip_login = '@'.join(['root', pub_ip1])
        pub_ip_ssh_comm = ''.join(['ssh -o StrictHostKeyChecking=no ',
                                pub_ip_login, '\n'])
        output, prompt = ssh.exec_shell_command(pub_ip_ssh_comm)
        self.assertTrue(prompt.find('password') != -1, ''.join(['SSH Failed: ',
                                                                output]))
        output, prompt = ssh.exec_shell_command(''.join([admin_pass1, '\n']))
        self.assertTrue(prompt.find(server1.name) != -1, ''.join(['SSH from ',
                         'gateway server into first server through public ',
                         'network failed.', output + '\n' + prompt]))
        output, prompt = ssh.exec_shell_command('exit\n')
        self.assertTrue(prompt.find(prompt_gws_name) != -1,
                                    ''.join(['Error when closing connection ',
                                             'from server1.']))
        shared_ip_login = '@'.join(['root', shared_ip1])
        shared_ip_ssh_comm = ''.join(['ssh -o StrictHostKeyChecking=no ',
                                shared_ip_login, '\n'])
        output, prompt = ssh.exec_shell_command(shared_ip_ssh_comm)
        self.assertTrue(prompt.find('password') != -1, ''.join(['SSH Success ',
                                    ' when it should fail\n',
                                    output + '\n' + prompt]))
        output, prompt = ssh.exec_shell_command(''.join([admin_pass1, '\n']))
        self.assertTrue(prompt.find(server1.name) != -1, ''.join(['SSH from ',
                         'gateway server into first server through shared ',
                         'network failed.', output]))
        output, prompt = ssh.exec_shell_command('ifconfig eth0 down\n')
        output, prompt = ssh.exec_shell_command('exit\n')
        self.assertTrue(prompt.find(prompt_gws_name) != -1,
                                    ''.join(['Error when closing connection ',
                                             'from server1.']))
        output, prompt = ssh.exec_shell_command(pub_ip_ssh_comm)
        self.assertTrue(len(output) == 0 and len(prompt) == 0)
        ssh.end_shell()

    @attr('all_linux_images')
    def test_all_linux_images(self):
        r = self.servers_provider.images_client.list_images(image_type='BASE')
        images = r.entity
        linux_images = [image for image in images
                        if image.name.find('Windows') == -1]
        network_list = [{'uuid': self.shared_network.id}]
        result = {}
#        result['gateway'] = {}
#        result['gateway']['ip'] = self.gateway_server.addresses.public.ipv4
#        result['gateway']['password'] = self.gateway_server.adminPass
        servers_adminPass = {}
        servers = []
        for image in linux_images:
            name = datagen.rand_name(image.name)
            flavorRef = self.config.compute_api.flavor_ref
            r = self.servers_provider.servers_client.create_server(
                                                       name=name,
                                                       flavor_ref=flavorRef,
                                                       image_ref=image.id,
                                                       networks=network_list)
            servers_adminPass[r.entity.id] = r.entity.adminPass
            result[r.entity.id] = {'image_name': image.name,
                                   'server_status': 'BUILD',
                                   'ssh_connection': False}
            self.servers_to_delete.append(r.entity.id)
            servers.append(r.entity)
        for server in servers:
            r = self.servers_provider.wait_for_server_status(server.id,
                                                NovaServerStatusTypes.ACTIVE)
            result[server.id]['server_status'] = r.entity.status
        gw_ip = self.gateway_server.addresses.public.ipv4
        gw_pass = self.gateway_server.adminPass
        for server in servers:
            #try one last time to check if server is ACTIVE
            r = self.servers_provider.servers_client.get_server(server.id)
            server = r.entity
            result[server.id]['server_status'] = server.status
            if server.addresses is None or \
               server.addresses.get_by_name(self.shared_network.label) is None:
                continue
            s_ip = server.addresses.get_by_name(self.shared_network.label).ipv4
            s_pass = servers_adminPass[server.id]
#            result[server.id]['ip'] = s_ip
#            result[server.id]['password'] = s_pass
            success = sshtools.attempt_ssh_from_server_to_server(gw_ip,
                                                                 gw_pass,
                                                                 s_ip, s_pass)
            result[server.id]['ssh_connection'] = success

        str_write = '\nIMAGE RESULTS\n----------------------------------------'
        filename = 'results.results_out'
        for k in result.keys():
            str_write += "\nImage: %s, SSH Connected: %s, "\
                          + "Server Status, %s" % (
                                       result[k].get('image_name', 'null'),
                                       result[k].get('ssh_connection', 'null'),
                                       result[k].get('server_status', 'null'))
        str_write += "\n--------------------------------------------------"
        f = open('/'.join([os.getcwd(), filename]), 'wb')
        f.write(str_write)
        for k in result.keys():
            if result[k].get('server_status') == 'ACTIVE':
                self.assertTrue(result[k]['ssh_connection'], "%s: %s" % (k,
                                                                    result[k]))

    def _remote_ssh(self, server1, server2, network1, network2,
                    connection=True, retries=5):
        """
        @summary: ssh remote connection via Isolated Network from server 1
            to server 2, through a gateway server with Public Network
        @param server1: server for first SSH from gateway server
        @type: server entity instance
        @param network1: server 1 network
        @type: network entity instance
        @param network2: server 2 network
        @type: network entity instance
        @param server2: server for second SSH from server 1
        @type: server entity instance
        @param connection: if connection from server 1 to server 2 through
            isolated network should be available
        @type bool
        @param retries: number of times to retry the SSH connections
        @type: int
        """
        ip1 = server1.addresses.get_by_name(network1.label).ipv4
        ip2 = server2.addresses.get_by_name(network2.label).ipv4
        ssh = SSHConnector(self.gateway_ip, 'root',
                           self.gateway_server.adminPass, tcp_timeout=10)
        conn_msg = ('Unable to SSH into {0} server {1} with user: {2} and'
                    ' password: {3}. Output: {4}')
        self.assertTrue(ssh.test_connection_auth(), conn_msg.format('gateway',
            self.gateway_ip, 'root', self.gateway_server.adminPass, ''))

        count = 0
        ssh_msg_items = []
        result = False
        while count < self.ssh_retries:
            ssh.start_shell()
            ip1_login = 'root@{0}'.format(ip1)
            ip1_ssh_comm = 'ssh -o StrictHostKeyChecking=no {0}\n'.format(
                ip1_login)
            output, prompt = ssh.exec_shell_command(ip1_ssh_comm)
            ssh_msg_items = ['first', ip1, 'root', server1.adminPass, output]
            if prompt.find('password') != -1:
                output, prompt = ssh.exec_shell_command('{0}\n'.format(
                    server1.adminPass))
                ssh_msg_items = ['first', ip1, 'root', server1.adminPass,
                                 output]
                if prompt.find(server1.name) != -1:
                    ip2_login = 'root@{0}'.format(ip2)
                    ip2_ssh_comm = ('ssh -o StrictHostKeyChecking=no {0}'
                        '\n').format(ip2_login)
                    output, prompt = ssh.exec_shell_command(ip2_ssh_comm)
                    ssh_msg_items = ['second', ip2, 'root', server2.adminPass,
                                     output]
                    if prompt.find('password') != -1 and connection:
                        output, prompt = ssh.exec_shell_command(
                            '{0}\n'.format(server2.adminPass))
                        ssh_msg_items = ['second', ip2, 'root',
                                         server2.adminPass, output]
                        if prompt.find(server2.name) != -1:
                            result = True
                            ssh.end_shell()
                            break
                    elif prompt.find('password') == -1 and not connection:
                        result = True
                        ssh.end_shell()
                        break
                    elif prompt.find('password') != -1 and not connection:
                        output, prompt = ssh.exec_shell_command(
                            '{0}\n'.format(server2.adminPass))
                        if prompt.find(server2.name) != -1:
                            ssh_msg = ('Unexpected: Able to SSH into {0} '
                                'server {1} with user: {2} and password: {3} '
                                'Output: {4}').format('second', ip2, 'root',
                                    server2.adminPass2, output)
                            self.fail(ssh_msg)
            count += 1
        else:
            ssh.end_shell()

        # The result flag is set to True when the test passed as expected
        # and will be set to False when there was an unexpected SSH
        # connection with server1 or server2. The ssh_msg will give server info
        ssh_msg = conn_msg.format(*ssh_msg_items)
        self.assertTrue(result, ssh_msg)
