'''
@summary: Provider Module for direct access to NVP Manager API
@note: Should be the primary interface to a test case or external tool.
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from ccengine.providers.base_provider import BaseProvider
from ccengine.clients.nvp.aic_nvp_api import AICNVPClient
from ccengine.clients.nvp.nvp_api import NVPClient


class NVPProvider(BaseProvider):
    '''
    aic-client info can be found here:
    https://one.rackspace.com/display/NOVA/AIC+Suite
    '''
    def __init__(self, config, logger):
        '''
        Sets config, sets up client, sets deserializer and serializer based
        on format defined in the config.
        '''
        super(NVPProvider, self).__init__()
        self.config = config
        endpoint = self.config.nvp_api.endpoint
        username = self.config.nvp_api.username
        password = self.config.nvp_api.password
        self.aic_client = AICNVPClient(endpoint, username, password)

        # used for defining NVP client for cell0002 when testing MDI and
        # running with leo.netdev.config
        if self.config.nvp_api.endpoint2:
            endpoint2 = self.config.nvp_api.endpoint2
            self.aic_client2 = AICNVPClient(endpoint2, username, password)
        else:
            self.aic_client2 = None

    def get_switch_uuid(self, network_id):
        """Returns the MDI swtich uuid by Cell given the network ID"""
        res_01 = self.aic_client.list_lswitches(tag=network_id)
        if self.aic_client2:
            res_02 = self.aic_client2.list_lswitches(tag=network_id)
        else:
            res_02 = {u'results': [], u'result_count': 0}
        if res_01['result_count'] >= 1:
            switch_id_01 = res_01['results'][0]['uuid']
        else:
            switch_id_01 = None
        if res_02['result_count'] >= 1:
            switch_id_02 = res_02['results'][0]['uuid']
        else:
            switch_id_02 = None
        return switch_id_01, switch_id_02

    class PortData(object):
        """Creates an NVP switch port object"""
        def __init__(self, port_id=None, switch_id=None, port_num=None,
                     relation=None, switch_config=None, att_config=None):
            self.display_name = str(port_id)
            self._href = '/ws.v1/lswitch/%s/lport/%s' % (str(switch_id),
                                                         str(port_id))
            self.portno = port_num
            self.tags = []
            self.queue_uuid = None
            self._schema = '/ws.v1/schema/LogicalSwitchPortConfig'
            self.allowed_address_pairs = []
            self.admin_status_enabled = True
            self.type = 'LogicalSwitchPortConfig'
            self.security_profiles = []
            self.uuid = str(port_id)
            if relation:
                relations = NVPProvider.Relations(str(switch_id), relation,
                                                  switch_config, att_config)
                self._relations = relations.get_dict()

        def get_dict(self):
            return vars(self)

        def update(self, nvp_data):
            assert isinstance(nvp_data, dict)
            self.__dict__.update(nvp_data)

    class SwitchData(object):
        """Creates an NVP switch data object"""
        def __init__(self, tenant_id=None, switch_id=None, network_id=None,
                        network_label=None, zone_uuid=None, relation=None):

            self.display_name = str(network_label)
            self.port_isolation_enabled = False
            tag_os_tid = NVPProvider.Tag('os_tid', str(tenant_id))
            tag_quantum_net_id = NVPProvider.Tag('quantum-net-id:mci', \
                                                 str(network_id))
            self.tags = [tag_quantum_net_id.get_dict(), tag_os_tid.get_dict()]
            self.type = 'LogicalSwitchConfig'
            self._schema = '/ws.v1/schema/LogicalSwitchConfig'
            self._href = '/ws.v1/lswitch/%s' % (str(switch_id))
            if relation:
                relations = NVPProvider.Relations(str(switch_id), relation)
                self._relations = relations.get_dict()
            transport_zones = NVPProvider.TransportZones(str(zone_uuid))
            self.transport_zones = [transport_zones.get_dict()]
            self.uuid = str(switch_id)

        def get_dict(self):
            return vars(self)

        def update(self, nvp_data):
            assert isinstance(nvp_data, dict)
            self.__dict__.update(nvp_data)

    class TransportZones(object):
        def __init__(self, zone_uuid=None):
            self.zone_uuid = str(zone_uuid)
            self.transport_type = 'stt'

        def get_dict(self):
            return vars(self)

    class Tag(object):
        def __init__(self, scope, tag):
            self.scope = str(scope)
            self.tag = str(tag)

        def get_dict(self):
            return vars(self)

    class Relations(object):
        def __init__(self, switch_id=None, relation=None, switch_config=None,
                     att_config=None):
            if isinstance(relation, str):
                relation = [relation]
            for rel in relation:
                if rel == 'LogicalSwitchStatus':
                    logical_switch_status = NVPProvider.LogicalSwitchStatus(
                                                                    switch_id)
                    self.LogicalSwitchStatus = logical_switch_status.get_dict()
                elif rel == 'LogicalSwitchConfig':
                    if switch_config is None:
                        switch_config = {}
                    assert isinstance(switch_config, dict), 'dict type missing'
                    lswitch_config = NVPProvider.SwitchData(**switch_config)
                    self.LogicalSwitchConfig = lswitch_config.get_dict()
                elif rel == 'LogicalPortAttachment':
                    if att_config is None:
                        att_config = {}
                    assert isinstance(att_config, dict), 'dict type missing'
                    lport_attachment = NVPProvider.LogicalPortAttachment(
                                                                    att_config)
                    self.LogicalPortAttachment = lport_attachment.get_dict()
                else:
                    self.LogicalSwitchStatus = None
                    self.LogicalSwitchConfig = None
                    self.LogicalPortAttachment = None

        def get_dict(self):
            return vars(self)

    class LogicalPortAttachment(object):
        def __init__(self, att_config):
            """Creates a Logical Switch Port Data Object: MDI or VIF"""
            assert isinstance(att_config, dict), 'dict type expected'
            switch_id = att_config['switch_id']
            port_id = att_config['port_id']

            self.type = att_config['type']
            self._href = '/ws.v1/lswitch/%s/lport/%s/attachment' \
                                            % (str(switch_id), str(port_id))
            if self.type == 'DomainGatewayAttachment':
                dgs_uuid = att_config['domain_gateway_service_uuid']
                icc_id = att_config['interconnect_context_id']
                self.set_domain_gateway(dgs_uuid, icc_id)
            elif self.type == 'VifAttachment':
                vif_uuid = att_config['vif_uuid']
                self.set_vif(vif_uuid)

        def set_domain_gateway(self, dgs_uuid, icc_id):
            """DomainGateway Port Parameters"""
            self.domain_gateway_service_uuid = dgs_uuid
            self.interconnect_context_id = icc_id
            self._schema = '/ws.v1/schema/DomainGatewayAttachment'

        def set_vif(self, vif_uuid):
            self.vif_uuid = vif_uuid
            self._schema = '/ws.v1/schema/VifAttachment'

        def get_dict(self):
            return vars(self)

    class LogicalSwitchStatus(object):
        def __init__(self, switch_id):
            self._href = ''.join(['/ws.v1/lswitch/', str(switch_id),
                                                        '/status'])
            self.lport_admin_up_count = 0
            self._schema = '/ws.v1/schema/LogicalSwitchStatus'
            self.lport_count = 0
            self.lport_fabric_up_count = 0
            self.fabric_status = True
            self.type = 'LogicalSwitchStatus'
            self.lport_link_up_count = 0

        def get_dict(self):
            return vars(self)
