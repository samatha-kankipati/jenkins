from ccengine.clients.base_client import BaseClient
import aiclib


class AICNVPClient(BaseClient):
    '''Adapter to talk to NVP Manager using aiclib.'''

    def __init__(self, url, username, password):
        super(AICNVPClient, self).__init__()
        self.connection = aiclib.Connection(url, username=username,
                                            password=password)

    def get_lswitch(self, lswitch_uuid):
        """Get switch by id"""
        r = self.connection.lswitch(uuid=str(lswitch_uuid)).read()
        return r

    def delete_lswitch(self, lswitch_uuid):
        """Deletes the switch by uuid"""
        try:
            lswitch = self.connection.lswitch(uuid=str(lswitch_uuid))
            lswitch.delete()
        except aiclib.nvp.ResourceNotFound:
            return 404
        else:
            return 202

    def list_lswitches(self, tag=None, display_name=None, relation=None):
        """Get switches by tag or display name (relation ex.
           LogicalSwitchStatus"""
        lswitches = self.connection.lswitch("*")
        query = lswitches.query()
        if tag is not None:
            query.tags(tag)
        if display_name is not None:
            query.display_name(display_name)
        if relation is not None:
            query.relations(relation)
        return query.results()

    def list_lswitch_ports(self, lswitch_uuid='*', attachment_vif_mac=None,
                           port_number=None, relation=None):
        """Get ports by switch id (relation ex. LogicalSwitchConfig)"""
        lports = self.connection.lswitch_port(lswitch_uuid=lswitch_uuid)
        query = lports.query()
        if attachment_vif_mac is not None:
            query.attachment_vif_mac('=', attachment_vif_mac.upper())
        #port_number method call unavailable, need to set dict value for query
        if port_number is not None:
            query.query['port_number'] = port_number
        if relation is not None:
            query.relations(relation)
        return query.results()

    def get_lport(self, lswitch_port_uuid, relation=None):
        """Gets port by id (relation ex. LogicalPortAttachment)"""
        lports = self.connection.lswitch_port(lswitch_uuid='*')
        query = lports.query()
        query.uuid(lswitch_port_uuid)
        if relation is not None:
            query.relations(relation)
        return query.results()

    def get_lswitch_port(self, lswitch_uuid, lswitch_port_uuid):
        """Get port by switch and port ids"""
        r = self.connection.lswitch_port(lswitch_uuid=lswitch_uuid,
                                         uuid=lswitch_port_uuid).read()
        return r

    def list_qos(self):
        r = self.connection.qos().query().results()
        return r

    def get_qos(self, qos_uuid):
        r = self.connection.qos(uuid=qos_uuid).read()
        return r
