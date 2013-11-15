import json
from ccengine.domain.base_domain import BaseMarshallingDomain


class Tenant(BaseMarshallingDomain):

    def __init__(self, tenant_id=None):
        super(Tenant, self).__init__()
        self.tenant_id = tenant_id

    def _obj_to_json(self):
        body = {'tenant_id': self.tenant_id}
        return json.dumps(body)


class Producer(BaseMarshallingDomain):

    def __init__(self, producer_name=None, producer_pattern=None,
                 producer_durable=None, producer_encrypted=None):
        super(Producer, self).__init__()

        self.pattern = producer_pattern
        self.durable = producer_durable
        self.encrypted = producer_encrypted
        self.name = producer_name

    def _obj_to_json(self):
        body = {
            'pattern': self.pattern,
            'durable': self.durable,
            'encrypted': self.encrypted,
            'name': self.name
        }

        return json.dumps(body)


class Profile(BaseMarshallingDomain):

    def __init__(self, profile_name=None, event_producer_ids=None):
        super(Profile, self).__init__()

        self.name = profile_name
        self.event_producer_ids = event_producer_ids

    def _obj_to_json(self):
        body = {
            'name': self.name,
            'event_producer_ids': self.event_producer_ids
        }
        return json.dumps(body)


class Host(BaseMarshallingDomain):

    def __init__(self, hostname=None, profile_id=None, ip_address_v4=None,
                 ip_address_v6=None):
        super(Host, self).__init__()

        self.hostname = hostname
        self.ip_address_v4 = ip_address_v4
        self.ip_address_v6 = ip_address_v6
        self.profile_id = profile_id

    def _obj_to_json(self):
        body = {
            'hostname': self.hostname,
            'ip_address_v4': self.ip_address_v4,
            'ip_address_v6': self.ip_address_v6,
            'profile_id': self.profile_id
        }

        return json.dumps(body)
