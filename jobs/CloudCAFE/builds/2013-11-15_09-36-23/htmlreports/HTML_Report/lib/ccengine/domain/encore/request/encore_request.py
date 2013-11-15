import json

from ccengine.domain.base_domain import BaseMarshallingDomain


class CreateDevice(BaseMarshallingDomain):

    def __init__(self, computer_number, account_num=None, icon_file=None,
                 datacenter=None, port_number=None, product_id=None,
                 primary_dns=None, enc_primary_userid=None, billing_notes=None,
                 status_number=None, server_name=None, leased_to_own=None,
                 product_number=None, datacenter_number=None):

        super(CreateDevice, self).__init__()
        self.computer_number = computer_number
        self.account_num = account_num
        self.product_id = product_id
        self.primary_dns = primary_dns
        self.icon_file = icon_file
        self.datacenter = datacenter
        self.enc_primary_userid = enc_primary_userid
        self.billing_notes = billing_notes
        self.port_number = port_number
        self.status_number = status_number
        self.server_name = server_name
        self.leased_to_own = leased_to_own
        self.product_number = product_number
        self.datacenter_number = datacenter_number

    def _obj_to_json(self):
        """
        @summary: Converts the address request to JSON
        @return: JSON of create customer request
        """

        return json.dumps(self._obj_to_json_dict())

    def _obj_to_json_dict(self):
        """
        @summary: Serialize the address request to JSON
        @return: Serialized JSON dictionary of address request
        """

        attrs = {}
        attrs['account_num'] = self.account_num
        attrs['product_id'] = self.product_id
        attrs['primary_dns'] = self.primary_dns
        attrs['icon_file'] = self.icon_file
        attrs['datacenter'] = self.datacenter
        attrs['enc_primary_userid'] = self.enc_primary_userid
        attrs['billing_notes'] = self.billing_notes
        attrs['port_number'] = self.port_number
        attrs['status_number'] = self.status_number
        attrs['server_name'] = self.server_name
        attrs['computer_number'] = self.computer_number
        attrs['leased_to_own'] = self.leased_to_own
        attrs['product_number'] = self.product_number
        attrs['datacenter_number'] = self.datacenter_number

        return self._remove_empty_values(attrs)
