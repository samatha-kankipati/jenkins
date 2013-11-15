import ccengine.domain.networks.rs_ovs_configure_vif_flows as flow_gen


class DualModeFlowsTable(object):
    '''
    @summary: Represents the openVswitch flows created for a nova server
              virtual interface in a dual mode Cloud Networks environment
    @copyright: Copyright (c) 2013 Rackspace US, Inc.
    '''
    def __init__(self, flows_type):
        self.flows_type = flows_type

    def get_flows_class(self):
        return getattr(flow_gen, self.flows_type)

    def generate(self, dom_id, vif_id, queue_id, xenstore_data):
        return self.get_flows_class().generate(
            dom_id, vif_id, queue_id, xenstore_data)
