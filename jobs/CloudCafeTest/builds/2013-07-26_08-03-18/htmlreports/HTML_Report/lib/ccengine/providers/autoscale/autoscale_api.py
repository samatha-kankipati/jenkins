from ccengine.providers.base_provider import BaseProvider
from ccengine.clients.autoscale.autoscale_api import AutoscalingAPIClient
from ccengine.providers.auth.auth_api import AuthProvider as _AuthProvider
from ccengine.common.tools.datagen import rand_name
from ccengine.domain.autoscale.servers import Metadata
import os


class AutoscaleAPIProvider(BaseProvider):
    '''
    @summary: Provider Module for the Autoscale REST API
    @note: Should be the primary interface to a test case or external tool
    @copyright: Copyright (c) 2012 Rackspace US, Inc.
    '''

    def __init__(self, config, logger=None):
        super(AutoscaleAPIProvider, self).__init__()
        if config is None:
            self.client_log.warning('empty (=None) config recieved in init')
            ''' Load configuration from default.conf '''
            self.config = _AuthProvider
        else:
            self.config = config

        # # Get Auth Info
        # self.auth_provider = _AuthProvider(self.config)

        # self.auth_data = self.auth_provider.authenticate()

        # # Get Auth Token
        # self.auth_token = self.auth_data.token.id
        self.auth_token = 87686868768

        # autoscale_service = self.auth_data.get_service(
        #     self.config.autoscale.identity_service_name)

        # # Set up regions
        # self.autoscale_region = self.config.autoscale.region

        # setup url
        env = os.environ['CLOUDCAFE_TEST_CONFIG']
        if "dev" in env.lower():
            self.autoscale_url = 'http://localhost:9000/v1.0/121213'
        # else:
        #     self.autoscale_url = autoscale_service.get_endpoint_by_region(self.autoscale_region).publicURL
        # #print self.autoscale_url

        # # setup tenant
        # self.tenant_id = autoscale_service.get_endpoint_by_region(self.autoscale_region).tenantId

        # initialize autoscale api client
        self.autoscale_client = AutoscalingAPIClient(self.autoscale_url,
                                                     self.auth_token,
                                                     self.config.misc.serializer,
                                                     self.config.misc.deserializer)

    def create_scaling_group_min(self, gc_name=None,
                                 gc_cooldown=None,
                                 gc_min_entities=None,
                                 lc_name=None,
                                 lc_image_ref=None,
                                 lc_flavor_ref=None):
        '''
        Creates a scaling group with only the required fields
        '''
        if gc_name is None:
            gc_name = rand_name('test_sgroup')
        else:
            gc_name = (str(gc_name))
        if gc_cooldown is None:
            gc_cooldown = int(self.config.autoscale.gc_cooldown)
        if gc_min_entities is None:
            gc_min_entities = int(self.config.autoscale.gc_min_entities)
        if lc_name is None:
            lc_name = rand_name('test_lc_srv')
        else:
            lc_name = rand_name(str(lc_name))
        if lc_image_ref is None:
            lc_image_ref = self.config.autoscale.lc_image_ref
        if lc_flavor_ref is None:
            lc_flavor_ref = self.config.autoscale.lc_flavor_ref
        create_response = self.autoscale_client.create_scaling_group(gc_name,
                                                                     gc_cooldown,
                                                                     gc_min_entities,
                                                                     lc_name,
                                                                     lc_image_ref,
                                                                     lc_flavor_ref)
        return create_response

    def create_scaling_group_given(self, gc_name=None, gc_cooldown=None,
                                   gc_min_entities=None, gc_max_entities=None,
                                   gc_metadata=None, lc_name=None,
                                   lc_image_ref=None, lc_flavor_ref=None,
                                   lc_personality=None, lc_metadata=None,
                                   lc_disk_config=None, lc_networks=None,
                                   lc_load_balancers=None, sp_list=None):
        '''
        Creates a scaling group with given parameters and default the other
        required fileds if not already given
        '''
        if gc_name is None:
            gc_name = rand_name('test_sgroup')
        else:
            gc_name = (str(gc_name))
        if gc_cooldown is None:
            gc_cooldown = int(self.config.autoscale.gc_cooldown)
        if gc_min_entities is None:
            gc_min_entities = int(self.config.autoscale.gc_min_entities)
        if lc_name is None:
            lc_name = rand_name('test_lc_srv')
        else:
            lc_name = (str(lc_name))
        if lc_image_ref is None:
            lc_image_ref = self.config.autoscale.lc_image_ref
        if lc_flavor_ref is None:
            lc_flavor_ref = self.config.autoscale.lc_flavor_ref
        create_response = self.autoscale_client.create_scaling_group(gc_name,
                                                                     gc_cooldown,
                                                                     gc_min_entities,
                                                                     lc_name,
                                                                     lc_image_ref,
                                                                     lc_flavor_ref,
                                                                     gc_max_entities=gc_max_entities,
                                                                     gc_metadata=gc_metadata,
                                                                     lc_personality=lc_personality,
                                                                     lc_metadata=lc_metadata,
                                                                     lc_disk_config=lc_disk_config,
                                                                     lc_networks=lc_networks,
                                                                     lc_load_balancers=lc_load_balancers,
                                                                     sp_list=sp_list)
        return create_response

    def create_policy_min(self, group_id, sp_name=None, sp_cooldown=None,
                          sp_change=None, sp_change_percent=None,
                          sp_steady_state=None):
        '''
        Creates a scaling policy with only the required fields
        '''
        if sp_name is None:
            sp_name = rand_name('test_sp')
        else:
            sp_name = (str(sp_name))
        if sp_cooldown is None:
            sp_cooldown = int(self.config.autoscale.sp_cooldown)
        if sp_change is None:
            sp_change = int(self.config.autoscale.sp_change)
        create_response = self.autoscale_client.create_policy(group_id=group_id,
                                                              name=sp_name,
                                                              cooldown=sp_cooldown,
                                                              change=sp_change)
        return create_response

    def to_data(self, data):
        ''' converts test data to the respective object type '''
        if "Metadata" in str(type(data)):
            return Metadata._obj_to_dict(data)

    def network_uuid_list(self, data):
        network_list = []
        for i in data:
            if isinstance(i, dict):
                network_list.append(i["uuid"])
            else:
                network_list.append(i.uuid)
        return network_list

    def lbaas_list(self, data):
        lbaas_id_list = []
        lbaas_port_list = []
        for i in data:
            if isinstance(i, dict):
                lbaas_id_list.append(i["loadBalancerId"])
                lbaas_port_list.append(i["port"])
            else:
                lbaas_id_list.append(i.loadBalancerId)
                lbaas_port_list.append(i.port)
        return lbaas_id_list, lbaas_port_list

    def personality_list(self, data):
        path_list = []
        contents_list = []
        for i in data:
            if isinstance(i, dict):
                path_list.append(i["path"])
                contents_list.append(i["contents"])
            else:
                path_list.append(i.path)
                contents_list.append(i.contents)
        return path_list, contents_list

    def policy_details_list(self, data):
        # @todo : make the obj list work for changePercent and steadystate
        policy_name = []
        policy_chng = []
        policy_cooldown = []
        for i in data:
            if isinstance(i, dict):
                chng_type = i.get("change") or i.get("changePercent") or i.get("steadyState")
                policy_name.append(i["name"])
                policy_chng.append(chng_type)
                policy_cooldown.append(i["cooldown"])
            else:
                policy_name.append(i.name)
                policy_cooldown.append(i.cooldown)
                policy_chng.append(i.change)
        return policy_name, policy_cooldown, policy_chng

    def get_policy_properties(self, policy_list):
        # @todo : find the change type
        policy = {}
        for policy_type in policy_list:
            try:
                if policy_type.change:
                    policy["change"] = policy_type.change
            except AttributeError:
                pass
            try:
                if policy_type.changePercent:
                    policy["change_percent"] = policy_type.changePercent
            except AttributeError:
                pass
            try:
                if policy_type.steadyState:
                    policy["steady_state"] = policy_type.steadyState
            except AttributeError:
                pass
            policy["id"] = policy_type.id
            policy["links"] = policy_type.links
            policy["name"] = policy_type.name
            policy["cooldown"] = policy_type.cooldown
            policy["count"] = len(policy_list)
            return policy

    def get_webhooks_properties(self, webhook_list):
        webhook = {}
        for i in webhook_list:
            webhook["id"] = i.id
            webhook["links"] = i.links
            webhook["name"] = i.name
            try:
                if i.metadata:
                    webhook["metadata"] = i.metadata
            except AttributeError:
                pass
            webhook["count"] = len(webhook_list)
            return webhook
