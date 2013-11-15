from testrepo.common.testfixtures.networks import NetworksPerformanceFixture
from ccengine.domain.types import NovaServerStatusTypes
from ccengine.common.exceptions import compute as exceptions
import unittest2
from ccengine.common.decorators import attr
import time
import ccengine.common.tools.datagen as datagen
import ccengine.common.tools.sshtools as sshtools
import sys
import re
import math

class TestPerformance(NetworksPerformanceFixture):
#4ETE82udsYP4
    BW_TIME = 600

    CLIENT_COMMAND = 'nohup iperf -c %s -P 1 -i %s -p 5001 -f m -t %s > output.txt &'

    @unittest2.skip("Only run when you really want to.")
    @attr('performance', 'one_network_many_servers')
    def test_many_servers_on_one_network(self):
        '''Many servers on one network and measure performance.'''
        EXPECTED_SERVERS_ON_NETWORK = 64
        POSSIBLE_SERVERS_ON_NETWORK = 256

        SERVER_ITERATIONS = 1
        SERVERS_PER_ITERATION = 250

        cidr = '172.16.100.0/22'
        network_label = datagen.random_string('shared_network')
        r = self.networks_provider.client.create_network(cidr=cidr,
                                                        label=network_label)
        network1 = r.entity
        server_name = datagen.random_string('gateway_server')
        network_list = [{'uuid': network1.id},
                        {'uuid': self.networks_provider.get_public_network().id}]
        r = self.servers_provider.create_active_server(name=server_name,
                                                      image_ref=self.config.isolated_networks_api.performance_image_ref,
                                                      networks=network_list)
        gateway1 = r.entity
        admin_pass_gateway = gateway1.adminPass
        r = self.servers_provider.servers_client.get_server(gateway1.id)
        gateway1 = r.entity
        gateway1.adminPass = admin_pass_gateway
        servers = []
        for i in range(self.SERVER_ITERATIONS):
            new_servers = self._create_servers_and_wait_for_all_active(
                                                SERVERS_PER_ITERATION,
                                                network1)
            servers.extend(new_servers)
        self._do_commands(network1, gateway1, servers)
        time.sleep(self.BW_TIME)
        self._get_results(network1, gateway1, servers)

    @unittest2.skip("Only run when you really want to.")
    @attr('performance', 'one_server_many_networks')
    def test_many_networks_to_one_server(self):
        '''Many networks on one server and measure performance.'''
        pass

#    @unittest2.skip("Only run when you really want to.")
    @attr('performance', 'few_networks_many_servers')
    def test_few_networks_many_servers(self):
        '''Create networks and fill with servers.'''
        SERVERS_PER_NETWORK = 63
        NETWORK_ITERATIONS = 10
        NETWORKS_PER_ITERATION = 5

        NETWORKS_TO_TEST = 5
        SERVERS_TO_TEST = 3

        server_networks = []
        for i in range(NETWORK_ITERATIONS):
            networks = self._create_networks(i, NETWORKS_PER_ITERATION)
            new_server_networks = [self._create_servers_no_wait(i,
                                                      SERVERS_PER_NETWORK,
                                                      networks, True)]
            completed = self._wait_for_all_server_networks_active(
                                                           new_server_networks)
            server_networks.extend(completed)
            unable_to_ssh = 0
#            for server_network in server_networks:
#                servers = server_network['servers']
#                for network_counter in range(NETWORKS_TO_TEST):
#                    network = server_network['networks'][network_counter]
#                    ssh_servers = servers[:SERVERS_TO_TEST]
#                    unable_to_ssh += self._do_commands(network,
#                                                       servers[0],
#                                                       ssh_servers)
            server_stats = self._get_server_stats(server_networks)
            self._output_server_info(server_stats, unable_to_ssh)
#            self.fixture_log.debug('Sleeping while bandwidth generates.')
#            time.sleep(self.BW_TIME)
#            bw_info = [0, sys.float_info.max, 0]
#            for server_network in server_networks:
#                servers = server_network['servers']
#                for network_counter in range(NETWORKS_TO_TEST):
#                    network = server_network['networks'][network_counter]
#                    ssh_servers = servers[:SERVERS_TO_TEST]
#                    net_bw = self._get_results(network,
#                                               servers[0],
#                                               ssh_servers)
#                    bw_info[0] += net_bw[0]
#                    if net_bw[1] < bw_info[1]:
#                        bw_info[1] = net_bw[1]
#                    if net_bw[2] > bw_info[2]:
#                        bw_info[2] = net_bw[2]
#
#            bw_info[0] = bw_info[0] / (NETWORKS_TO_TEST * SERVERS_TO_TEST)
#            sys.stderr.write('\nAverage Bandwidth: %s' % str(bw_info[0]))
#            sys.stderr.write('\nMin Bandwidth: %s' % str(bw_info[1]))
#            sys.stderr.write('\nMax Bandwidth: %s' % str(bw_info[2]))
#            sys.stderr.write('\n----------------------------------------\n\n')

    @unittest2.skip("Only run when you really want to.")
    @attr('performance', 'many_networks_few_servers')
    def test_many_networks_few_servers(self):
        '''Create many networks with few servers attached.'''
#        SERVER_ITERATIONS = 28
#        SERVERS_PER_ITERATION = 50 #Be sure this is divisible by SERVERS_PER_PASS
#        SERVERS_PER_PASS = 2
#        NETWORK_ITERATIONS = 1400
#        NETWORKS_PER_ITERATION = 7

        SERVER_ITERATIONS = 1
        SERVERS_PER_ITERATION = 100 #Be sure this is divisible by SERVERS_PER_PASS
        SERVERS_PER_PASS = 2
        NETWORK_ITERATIONS = 1400
        NETWORKS_PER_ITERATION = 7

        server_networks = []
        for si in range(SERVER_ITERATIONS):
            marker = SERVERS_PER_ITERATION / SERVERS_PER_PASS
            server_networks_to_wait = []
            for i in range(NETWORK_ITERATIONS):
                if si == 0:
                    networks = self._create_networks(i, NETWORKS_PER_ITERATION)
                    new_server_networks = self._create_servers_no_wait(i,
                                                              SERVERS_PER_PASS,
                                                              networks, True)
                else:
                    networks = server_networks[si - 1]['networks']
                    new_server_networks = self._create_servers_no_wait(i,
                                                              SERVERS_PER_PASS,
                                                              networks, False)
                server_networks_to_wait.append(new_server_networks)
                if (i + 1) >= marker:
                    complete_server_networks = self._wait_for_all_server_networks_active(server_networks_to_wait)
                    server_networks.extend(complete_server_networks)
                    server_networks_to_wait = []
                    marker = marker + (SERVERS_PER_ITERATION / SERVERS_PER_PASS)
            complete_server_networks = self._wait_for_all_server_networks_active(server_networks_to_wait)
            server_networks.extend(complete_server_networks)
#            server_info = self._do_commands_many_networks(server_networks)
            server_info = self._get_server_stats(server_networks)
            self._output_server_info(server_info)
#            time.sleep(self.BW_TIME)
#            bw_info = self._get_results_many_networks(server_networks)
#            self._output_bw_info(bw_info)
#            print server_info
#            print bw_info

    @unittest2.skip("Only run when you really want to.")
    @attr('performance', 'many_networks_many_servers')
    def test_many_servers_on_many_networks(self):
        '''Create many networks and loop attaching many servers to each.'''
        network_servers = {}
        for i in range(self.NETWORK_ITERATIONS):
            new_network_servers = self._create_networks_with_servers()
            network_servers = dict(network_servers.items() +
                                   new_network_servers.items())
        server_info = {'Total': 0, 'NO_SSH': 0, 'ERROR': 0, 'BUILD': 0}
        for label in network_servers.keys():
            network = network_servers[label]['network']
            servers = network_servers[label]['servers']
            gateway_server = servers.pop(0)
            info = self._do_commands(network, gateway_server, servers)
            servers.insert(0, gateway_server)
            server_info['Total'] += info[0]
            server_info['NO_SSH'] += info[1]
            server_info['ERROR'] += info[2]
            server_info['BUILD'] += info[3]
        time.sleep(self.BW_TIME)
        bw_info = {'Total_AVG': 0, 'Total_Min': sys.float_info.max,
                   'Total_Max': 0}
        for label in network_servers.keys():
            network = network_servers[label]['network']
            servers = network_servers[label]['servers']
            gateway_server = servers.pop(0)
            bw = self._get_results(network, gateway_server, servers)
            servers.insert(0, gateway_server)
            bw_info['Total_AVG'] += bw[0]
            if bw_info['Total_Min'] > bw[1]:
                bw_info['Total_Min'] = bw[1]
            if bw_info['Total_Max'] < bw[2]:
                bw_info['Total_Max'] = bw[2]
        sys.stderr.write('\n\nTOTALS:--------------')
        sys.stderr.write('\nTotal Servers: ' + str(server_info['Total']))
        sys.stderr.write('\nUnable to SSH Servers: ' + str(server_info['NO_SSH']))
        sys.stderr.write('\nERROR Servers: ' + str(server_info['ERROR']))
        sys.stderr.write('\nBUILD Servers: ' + str(server_info['BUILD']))
        count = len(network_servers.keys())
        sys.stderr.write('\n\nTotal Average Bandwidth: ' + \
                          str(bw_info['Total_AVG'] / count))
        sys.stderr.write('\nTotal Min Bandwidth: ' + str(bw_info['Total_Min']))
        sys.stderr.write('\nTotal Max Bandwidth: ' + str(bw_info['Total_Max']))
        sys.stderr.write('\n\n')

    def _output_server_info(self, server_info, unable_to_ssh):
        sys.stderr.write('\n\n------------------------------------------')
        sys.stderr.write('\nTotal Servers: ' + str(server_info[0]))
        sys.stderr.write('\nERROR Servers: ' + str(server_info[1]))
        sys.stderr.write('\nBUILD Servers: ' + str(server_info[2]))
        sys.stderr.write('\nACTIVE Servers: ' + str(server_info[3]))
        sys.stderr.write('\nUnable to SSH Servers: ' + str(unable_to_ssh))
        sys.stderr.write('\n----------------------------------------\n\n')

    def _output_bw_info(self, bw_info):
        info = {'Total_AVG': 0, 'Total_Min': sys.float_info.max, 'Total_Max': 0}
        for network_id in bw_info.keys():
            info['Total_AVG'] += bw_info[network_id][0]
            if info['Total_Min'] > bw_info[network_id][1]:
                info['Total_Min'] = bw_info[network_id][1]
            if info['Total_Max'] < bw_info[network_id][2]:
                info['Total_Max'] = bw_info[network_id][2]
        count = len(bw_info.keys())
        sys.stderr.write('\n\nTotal Average Bandwidth: ' + \
                          str(info['Total_AVG'] / count))
        sys.stderr.write('\nTotal Min Bandwidth: ' + str(info['Total_Min']))
        sys.stderr.write('\nTotal Max Bandwidth: ' + str(info['Total_Max']))
        sys.stderr.write('\n----------------------------------------\n\n')

    def _create_servers_no_wait(self, iteration, num_servers,
                                networks, create_public):
        '''Creates servers in batch without waiting for active.  Sleeps for 1
        second in between create calls.'''
        pub_net = self.networks_provider.get_public_network()
#        pub_net_id = '00000000-0000-0000-0000-000000000000'
        created_servers = {'servers': [], 'networks': networks}
        for i in range(num_servers):
            s_networks = []
            if i == 0 and create_public == True:
                s_networks = [{"uuid": pub_net.id}]
            name = 'server_%s_%s' % (str(iteration), str(i))
            new_networks = []
            for n in networks:
                if n is None or n.id is None:
                    continue
                new_networks.append({"uuid": n.id})
            s_networks.extend(new_networks)
            r = self.servers_provider.servers_client.create_server(name=name,
                                    image_ref=self.config.isolated_networks_api.performance_image_ref,
                                    flavor_ref=self.config.compute_api.flavor_ref,
                                    networks=s_networks)
            created_servers['servers'].append(r.entity)
            time.sleep(1)
        return created_servers

    def _create_networks(self, iteration, num_networks):
        networks = []
        for i in range(num_networks):

            label = 'stress_test_network_%s_%s' % (str(iteration), str(i))
            cidr = '172.' + str(iteration + 1) + '.' + str(i + 1) + '.0/24'
            r = self.networks_provider.client.create_network(label=label,
                                                             cidr=cidr)
            networks.append(r.entity)
        return networks

    def _wait_for_all_server_networks_active(self, server_networks_to_wait):
        complete_server_networks = []
        for sn in server_networks_to_wait:
            new_servers = self._wait_for_all_servers_active(sn['servers'])
            item = {'servers': new_servers,
                    'networks': sn['networks']}
            complete_server_networks.append(item)
        return complete_server_networks

    def _wait_for_all_servers_active(self, servers):
        ret_servers = []
        for i in range(len(servers)):
            admin_pass = servers[i].adminPass
            r = self.servers_provider.wait_for_server_status(servers[i].id,
                                                  NovaServerStatusTypes.ACTIVE)
            r.entity.adminPass = admin_pass
            ret_servers.append(r.entity)
        return ret_servers

    def _create_servers_and_wait_for_all_active(self, num_servers, networks):
        pass

    def _get_server_stats(self, server_networks):
        n_total = 0
        n_error = 0
        n_build = 0
        n_active = 0
        for server_network in server_networks:
            for server in server_network['servers']:
                n_total += 1
                if server.status == NovaServerStatusTypes.ACTIVE:
                    n_active += 1
                if server.status == NovaServerStatusTypes.ERROR:
                    n_error += 1
                if server.status == NovaServerStatusTypes.BUILD:
                    n_build += 1
        return n_total, n_error, n_build, n_active

    def _do_commands(self, network, gateway_server, servers):
        first_id = servers[0].id
        last_id = servers[len(servers) - 1].id
        servers_unable_to_ssh = {}
        for server in servers:
            r = self.servers_provider.wait_for_server_status(server.id,
                                                  NovaServerStatusTypes.ACTIVE)
            if r.entity.status == NovaServerStatusTypes.ERROR:
                continue
            if r.entity.status == NovaServerStatusTypes.BUILD:
                continue
            r.entity.adminPass = server.adminPass
            server = r.entity
            try:
                from_ip = gateway_server.addresses.public.ipv4
                if from_ip is None:
                    self.fixture_log.debug('_do_commands:')
                    self.fixture_log.debug('Gateway server: %s - %s' %
                                           (gateway_server.name,
                                            gateway_server.id))
                    self.fixture_log.debug('Does not have IPv4 address.')
                    from_ip = gateway_server.addresses.public.ipv6
                    sys.stderr.write('%s - %s gateway does not have ipv4.' %
                                     (gateway_server.name, gateway_server.id))
                from_password = gateway_server.adminPass
                to_ip = server.addresses.get_by_name(network.label).ipv4
                to_password = server.adminPass
                if server.id == first_id:
                    traffic_to_ip = servers[len(servers) - 1].addresses.\
                                get_by_name(network.label).ipv4
                if server.id == last_id:
                    traffic_to_ip = servers[0].addresses.\
                                get_by_name(network.label).ipv4
                client_comm = self.CLIENT_COMMAND % (traffic_to_ip,
                                                     str(self.BW_TIME),
                                                     str(self.BW_TIME))
                traffic_to_ip = server.addresses.get_by_name(network.label).ipv4
            except Exception as e:
                self.fixture_log.debug('_do_commands:')
                self.fixture_log.debug('Error in get address block: %s' % e)
                self.fixture_log.debug('Server: %s - %s' % (server.name,
                                                            server.id))
                continue
            try:
                sshtools.execute_remote_command_through_gateway(from_ip,
                                                        from_password,
                                                        to_ip, to_password,
                                                        [client_comm])
            except Exception as e:
                self.fixture_log.debug('_do_commands:')
                self.fixture_log.debug('Unable to SSH from %s:%s to %s:%s' %
                                       (from_ip, from_password, to_ip,
                                        to_password))
                self.fixture_log.debug('Server: %s - %s' % (server.id,
                                                            server.name))
                self.fixture_log.debug('Exception: %s' % e)
                servers_unable_to_ssh[server.id] = 1
                continue
        return sum([servers_unable_to_ssh[k]
                    for k in servers_unable_to_ssh.keys()])

    def _get_results_many_networks(self, server_networks):
        ret_info = []
        for server_network in server_networks:
            for network in server_network['networks']:
                info = self._get_results(network,
                                         server_network['servers'][0],
                                         server_network['servers'])
                count = len(server_network['networks'])
                if info[0] == 0:
                    continue
                item = (info[0], info[1], info[2])
                ret_info.append(item)
        return ret_info


    def _get_results(self, network, gateway_server, servers):
        all_servers = '\n\nSERVER BANDWIDTH----------------\n'
        from_ip = ""
        to_ip = ""
        from_password = ""
        to_password = ""
        for server in servers:
            try:
                from_ip = gateway_server.addresses.public.ipv4
                if from_ip is None:
                    self.fixture_log.debug('_get_results:')
                    self.fixture_log.debug('Gateway server: %s - %s' %
                                           (gateway_server.name,
                                            gateway_server.id))
                    self.fixture_log.debug('Does not have IPv4 address.')
                    from_ip = gateway_server.addresses.public.ipv6
                from_password = gateway_server.adminPass
                to_ip = server.addresses.get_by_name(network.label).ipv4
                to_password = server.adminPass
                client_comm = 'cat output.txt'
                out = sshtools.execute_remote_command_through_gateway(from_ip,
                                                            from_password,
                                                            to_ip, to_password,
                                                            [client_comm])
                split_out = out.split('\n')
                last_line = split_out[len(split_out) - 1]
                all_servers += server.id + ': ' + last_line + '\n'
            except Exception as e:
                self.fixture_log.debug('_get_results:')
                self.fixture_log.debug('Unable to SSH from %s:%s to %s:%s' %
                                       (from_ip, from_password, to_ip,
                                        to_password))
                self.fixture_log.debug('Server: %s - %s' % (server.id,
                                                            server.name))
                self.fixture_log.debug('Exception: %s' % e)
        compiled = self._compile_data(all_servers)
#        ret =  '\n%s:\n' % network.label
#        ret += 'Average Bandwidth: %s\n' % str(compiled[0])
#        ret += 'Min Bandwidth: %s\n' % str(compiled[1])
#        ret += 'Max Bandwidth: %s\n' % str(compiled[2])
#        sys.stderr.write(ret)
        return compiled

    def _compile_data(self, data):
        lines = data.split('\n')
        avg = 0
        total_usable = 0
        total = 0
        hi = 0
        lo = sys.float_info.max
        for line in lines:
            match = re.search(r'([0-9\.]+) Mbits', line)
            if match is not None:
                value = float(match.group(1))
                total += value
                total_usable += 1
                if lo > value:
                    lo = value
                if hi < value:
                    hi = value
        if total_usable != 0:
            avg = total / total_usable
        avg_MB = avg / 8
        return avg_MB, lo / 8, hi / 8
