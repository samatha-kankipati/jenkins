'''
@summary: Provider Module for Compute Isolated Networks
@note: Should be the primary interface to a test case or external tool.
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
import requests
import os
import time
from ccengine.providers.base_provider import BaseProvider
from ccengine.clients.lbaas.load_balancers_client import LoadBalancersClient
from ccengine.clients.lbaas.load_balancers_mgmt_client import \
    LoadBalancersMgmtClient
# from ccengine.providers.identity.identity_v2_0_api import IdentityAPIProvider
from ccengine.providers.identity.v2_0.identity_api import IdentityAPIProvider
from ccengine.clients.identity.v2_0.rax_auth_api import IdentityClient
from ccengine.domain.types import LoadBalancerStatusTypes as LBStatus, \
    LoadBalancerNodeConditions as LBNodeConditions, \
    LoadBalancerNodeTypes as LBNodeTypes
from ccengine.common.constants.lbaas import SSLConstants
import ccengine.common.tools.datagen as datagen
import urllib2

__global_lb__ = None


class LoadBalancersProvider(BaseProvider):

    def __init__(self, config, logger):
        '''
        Sets config, sets up client, sets deserializer and serializer based
        on format defined in the config.
        '''
        super(LoadBalancersProvider, self).__init__()
        self.config = config
        self.identity_provider = IdentityAPIProvider(self.config)
        auth_data = None
        if (self.config.identity_api.api_key is not None and
                len(self.config.identity_api.api_key) != 0):
            auth_data = self.identity_provider.client.authenticate_user_apikey(
                self.config.identity_api.username,
                self.config.identity_api.api_key)
        if (self.config.identity_api.password is not None and
                len(self.config.identity_api.password) != 0):
            auth_data = \
                self.identity_provider.client.authenticate_user_password(
                    self.config.identity_api.username,
                    self.config.identity_api.password)
        self.tenant_id = auth_data.entity.token.tenant.id
        service_name = self.config.lbaas_api.identity_service_name
        region = self.config.lbaas_api.region
        service = auth_data.entity.serviceCatalog.get_service(service_name)
        if service is not None:
            url = service.get_endpoint(region).publicURL
        else:
            url = config.lbaas_api.public_url
        self.client = LoadBalancersClient(url, auth_data.entity.token.id,
                                          self.config.misc.serializer,
                                          self.config.misc.deserializer)
        self.mgmt_client = LoadBalancersMgmtClient(
            self.config.lbaas_api.mgmt_url,
            self.config.lbaas_api.mgmt_username,
            self.config.lbaas_api.mgmt_password,
            self.config.misc.serializer,
            self.config.misc.deserializer)

    @property
    def global_load_balancer(self):
        global __global_lb__
        if __global_lb__ is None:
            __global_lb__ = self.create_active_load_balancer().entity
        __global_lb__ = self.client.get_load_balancer(
            __global_lb__.id).entity
        if __global_lb__.status == LBStatus.ERROR:
            __global_lb__ = self.create_active_load_balancer().entity
        return __global_lb__

    @global_load_balancer.deleter
    def global_load_balancer(self):
        global __global_lb__
        if __global_lb__ is not None:
            self.client.delete_load_balancer(__global_lb__.id)

    def wait_for_status(self, lb_id, status_to_wait_for=LBStatus.ACTIVE):
        r = self.client.get_load_balancer(lb_id)
        while r.entity.status.lower() != status_to_wait_for.lower():
            time.sleep(5)
            r = self.client.get_load_balancer(lb_id)
            if r.entity.status == LBStatus.ERROR:
                break
        return r

    def create_active_load_balancer(self, retry_on_error=True, num_tries=0,
                                    **kwargs):
        max_attempts = 5
        if 'name' not in kwargs:
            kwargs['name'] = datagen.random_string('cc_lb')
        if 'port' not in kwargs:
            kwargs['port'] = '80'
        if 'protocol' not in kwargs:
            kwargs['protocol'] = 'HTTP'
        if 'virtualIps' not in kwargs:
            kwargs['virtualIps'] = [{'type':
                                     self.config.lbaas_api.default_vip_type}]
        if 'nodes' not in kwargs:
            kwargs['nodes'] = [{'address': self.config.lbaas_api.live_node1,
                                'port': '80', 'condition': 'ENABLED'},
                               {'address': self.config.lbaas_api.live_node2,
                                'port': '80', 'condition': 'ENABLED'}]
        response = self.client.create_load_balancer(**kwargs)
        assert response.status_code == 202, 'Could not create LB: %s' \
            % response.content
        r = self.wait_for_status(response.entity.id)
        if r.entity.status == LBStatus.ERROR:
            self.mgmt_client.delete_errored_load_balancer(r.entity.id)
            if num_tries > max_attempts:
                err_str = ("Create LB retries exceeded. "
                           "{0} consecutive have gone into ERROR status")
                assert False, err_str.format(max_attempts)
            if retry_on_error is True:
                num_tries += 1
                r = self.create_active_load_balancer(num_tries=num_tries,
                                                     **kwargs)
        return r

    def create_n_load_balancers(self, n, wait_for_active=False,
                                retry_on_error=True, **kwargs):
        if 'name' not in kwargs:
            kwargs['name'] = datagen.random_string('cc_lb')
        if 'port' not in kwargs:
            kwargs['port'] = '80'
        if 'protocol' not in kwargs:
            kwargs['protocol'] = 'HTTP'
        if 'virtualIps' not in kwargs:
            kwargs['virtualIps'] = [{'type':
                                     self.config.lbaas_api.default_vip_type}]
        if 'nodes' not in kwargs:
            kwargs['nodes'] = [{'address': self.config.lbaas_api.live_node1,
                                'port': '80', 'condition': 'ENABLED'},
                               {'address': self.config.lbaas_api.live_node2,
                                'port': '80', 'condition': 'ENABLED'}]
        lbs = [self.client.create_load_balancer(**kwargs).entity
               for _ in range(n)]
        ret_lbs = []
        if wait_for_active:
            for lb in lbs:
                lb = self.wait_for_status(lb.id).entity
                if lb.status == LBStatus.ERROR and retry_on_error:
                    lb = self.create_active_load_balancer(**kwargs).entity
                ret_lbs.append(lb)
        return ret_lbs

    def add_n_nodes(self, load_balancer_id, n, wait_for_active=True,
                    **kwargs):
        addresses = []
        conditions = []
        ports = []
        weights = []
        types = []
        for _ in range(n):
            if 'address' not in kwargs:
                addresses.append(datagen.random_ip())
            else:
                addresses.append(kwargs['address'])
            if 'condition' not in kwargs:
                condition_list = [LBNodeConditions.DISABLED,
                                  LBNodeConditions.ENABLED,
                                  LBNodeConditions.DRAINING]
                conditions.append(datagen.random_item_in_list(condition_list))
            else:
                conditions.append(kwargs['condition'])
            if 'port' not in kwargs:
                ports.append(datagen.random_int(1, 500))
            else:
                ports.append(kwargs['port'])
            if 'weight' not in kwargs:
                weights.append(datagen.random_int(1, 100))
            else:
                weights.append(kwargs['weight'])
            if 'type' not in kwargs:
                type_list = [LBNodeTypes.PRIMARY]
                types.append(datagen.random_item_in_list(type_list))
            else:
                types.append(kwargs['type'])
        r = self.client.add_nodes(load_balancer_id, addresses, conditions,
                                  ports, types, weights)
        return r.entity

    # Usage generation methods
    def ssl_mixed_on(self, lb_id):
        r = self.client.update_ssl_termination(
            lb_id, securePort=443,
            privatekey=SSLConstants.privatekey,
            certificate=SSLConstants.certificate,
            enabled=True,
            secureTrafficOnly=False)
        assert r.ok, "Could not enable SSL MIXED for LB %s" % str(lb_id)
        lb = self.wait_for_status(lb_id).entity
        assert lb.status == LBStatus.ACTIVE, \
            'LB %s ERRORed after SSL MIXED enabled' % str(lb_id)
        return r

    def ssl_only_on(self, lb_id):
        r = self.client.update_ssl_termination(
            lb_id, securePort=443,
            privatekey=SSLConstants.privatekey,
            certificate=SSLConstants.certificate,
            enabled=True,
            secureTrafficOnly=True)
        assert r.ok, "Could not enable SSL ONLY for LB %s" % str(lb_id)
        lb = self.wait_for_status(lb_id).entity
        assert lb.status == LBStatus.ACTIVE, \
            'LB %s ERRORed after SSL ONLY enabled' % str(lb_id)
        return r

    def ssl_disabled(self, lb_id):
        r = self.client.update_ssl_termination(
            lb_id, securePort=443,
            privatekey=SSLConstants.privatekey,
            certificate=SSLConstants.certificate,
            enabled=False,
            secureTrafficOnly=True)
        assert r.ok, "Could not disable SSL for LB %s" % str(lb_id)
        lb = self.wait_for_status(lb_id).entity
        assert lb.status == LBStatus.ACTIVE, \
            'LB %s ERRORed after SSL disabled' % str(lb_id)
        return r

    def add_virtual_ip(self, lb_id):
        r = self.mgmt_client.add_virtual_ip(lb_id, 'PUBLIC',
                                            {'ticketId': 1234,
                                             'comment': 'Usage tests'})
        assert r.ok, "Could not add VIP to LB %s" % str(lb_id)
        lb = self.wait_for_status(lb_id).entity
        assert lb.status == LBStatus.ACTIVE, \
            'LB %s ERRORed after adding VIP' % str(lb_id)
        return r

    def delete_virtual_ip(self, lb_id, vip_id):
        r = self.client.delete_virtual_ip(lb_id, vip_id)
        assert r.ok, "Could not delete VIP %s from LB %s" % (str(vip_id),
                                                             str(lb_id))
        lb = self.wait_for_status(lb_id).entity
        assert lb.status == LBStatus.ACTIVE, \
            'LB %s ERRORed after deleting VIP %s' % (str(lb_id),
                                                     str(vip_id))
        return r

    def suspend_load_balancer(self, lb_id):
        r = self.mgmt_client.suspend_load_balancer(
            lb_id, reason='Usage Test',
            user='Usage User',
            ticket={'ticketId': 1234, 'comment': 'usage tests'})
        assert r.ok, "Could not suspend LB %s" % str(lb_id)
        lb = self.wait_for_status(lb_id, LBStatus.SUSPENDED).entity
        assert lb.status == LBStatus.SUSPENDED, \
            'LB %s ERRORed after suspension' % str(lb_id)
        return r

    def unsuspend_load_balancer(self, lb_id):
        r = self.mgmt_client.unsuspend_load_balancer(lb_id)
        assert r.ok, "Could not unsuspend LB %s" % str(lb_id)
        lb = self.wait_for_status(lb_id).entity
        assert lb.status == LBStatus.ACTIVE, \
            'LB %s ERRORed after unsuspension' % str(lb_id)
        return r

    def generate_bandwidth_out(self, ip, path='/medium.iso'):
        self.provider_log.info("Generating outgoing normal bandwidth to {0}"
                               "...".format(ip))
        protocol = 'http://'
        r = requests.api.get(''.join([protocol, ip, path]), verify=False)
        size = len(r.content)
        self.provider_log.info("Generated {0} bytes of outgoing bandwidth "
                               "to {0}...".format(size, ip))
        return size

    def generate_bandwidth_in(self, ip, filepath='./bw_in.iso'):
        bs = '2048000'
        create_file_comm = ''.join(['dd if=/dev/zero of=', filepath, ' bs=',
                                    bs, ' count=1 2> /dev/null'])
        os.system(create_file_comm)
        protocol = 'http://'
        f = open(filepath)
        self.provider_log.info("Generating incoming bandwidth to {0}"
                               "...".format(ip))
        requests.api.post(''.join([protocol, ip]),
                          data={'title': filepath},
                          files={'file': f}, verify=False)
        size = str(os.fstat(f.fileno()).st_size)
        self.provider_log.info("Generated {0} bytes of incoming bandwidth "
                               "to {0}...".format(size, ip))
        return size

    def generate_ssl_bandwidth_out(self, ip, path='/small.iso'):
        self.provider_log.info("Generating outgoing SSL bandwidth to {0}"
                               "...".format(ip))
        protocol = 'https://'
        handle = urllib2.urlopen(''.join([protocol, ip, path]))
        # r = requests.api.get(''.join([protocol, ip, path]), verify=False)
        # size = len(r.content)
        size = len(handle.read())
        self.provider_log.info("Generated {0} bytes of outgoing SSL bandwidth "
                               "to {0}...".format(size, ip))
        return size

    def generate_ssl_bandwidth_in(self, ip, filepath='./bw_in.iso'):
        bs = '1024000'
        create_file_comm = ''.join(['dd if=/dev/zero of=', filepath, ' bs=',
                                    bs, ' count=1 2> /dev/null'])
        os.system(create_file_comm)
        protocol = 'https://'
        f = open(filepath)
        self.provider_log.info("Generating incoming SSL bandwidth to {0}"
                               "...".format(ip))
        requests.api.post(''.join([protocol, ip]),
                          data={'title': filepath},
                          files={'file': f}, verify=False)
        size = str(os.fstat(f.fileno()).st_size)
        self.provider_log.info("Generated {0} bytes of incoming SSL bandwidth "
                               "to {0}...".format(size, ip))
        return size

    def generate_avg_concurrent_connections(self, ip, num_connections,
                                            num_polls=1, path='/large.iso'):
        # Appears to be a ramp up time of around 1.5 seconds for every 10
        # connections.  Obviously subjective to the hardware being run on.
        ramp_up_time = 1.5 * num_connections

        # 301 = 5 min/poll * 60 secs/min + 1 sec (to assure another polling
        # has occurred.)
        duration = (num_polls * 301) + ramp_up_time
        connections = []
        for _ in range(0, num_connections):
            try:
                req = requests.api.get('http://' + ip + path,
                                       prefetch=False, verify=False)
            except TypeError:
                req = requests.api.get('http://' + ip + path,
                                       stream=True, verify=False)
            connections.append(req)
        time.sleep(duration)
        del connections

    def generate_ssl_avg_concurrent_connections(self, ip, num_connections,
                                                num_polls=1,
                                                path='/large.iso'):
        # Appears to be a ramp up time of around 1.5 seconds for every 10
        # connections.  Obviously subjective to the hardware being run on.
        ramp_up_time = 1.5 * num_connections

        # 301 = 5 min/poll * 60 secs/min + 1 sec (to assure another polling
        # has occurred).
        duration = (num_polls * 301) + ramp_up_time
        connections = []
        for _ in range(0, num_connections):
            try:
                req = requests.api.get('https://' + ip + path,
                                       prefetch=False, verify=False)
            except TypeError:
                req = requests.api.get('https://' + ip + path,
                                       stream=True, verify=False)
            connections.append(req)
        time.sleep(duration)
        del connections

    def new_client(self, username, api_key=None, password=None, token=None,
                   region=None):
        if api_key is None  and password is None and token is None:
            return None
        auth_data = None
        if api_key is not None:
            auth_data = self.identity_provider.client.authenticate_user_apikey(
                username,
                api_key)
        if password is not None:
            auth_data = \
                self.identity_provider.client.authenticate_user_password(
                    username,
                    password)
        self.tenant_id = auth_data.entity.token.tenant.id
        service_name = self.config.lbaas_api.identity_service_name
        if region is None:
            region = self.config.lbaas_api.region
        service = auth_data.entity.serviceCatalog.get_service(service_name)
        base_url = service.get_endpoint(region).publicURL
        if token is None:
            token = auth_data.entity.token.id
        return LoadBalancersClient(base_url, token,
                                   self.client.serialize_format,
                                   self.client.deserialize_format)


