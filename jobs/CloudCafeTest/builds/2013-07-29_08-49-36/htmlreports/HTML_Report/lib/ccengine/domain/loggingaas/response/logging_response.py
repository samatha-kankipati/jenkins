import json
from ccengine.domain.base_domain import BaseMarshallingDomain


class Version(BaseMarshallingDomain):

    def __init__(self, v1):
        super(Version, self).__init__()
        self.v1 = v1

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """Returns an instance of a Version based on the json serialized_str
        passed in."""
        result = None
        json_obj = json.loads(serialized_str)
        if json_obj is not None:
            result = []
            for _ in json_obj:
                result.append(cls._dict_to_obj(json_obj))
        return result

    @classmethod
    def _dict_to_obj(cls, dic):
        """Helper method to turn dictionary into Xenmeta instance."""
        kwargs = {'v1': dic.get('v1')}
        return Version(**kwargs)


class Profiles(BaseMarshallingDomain):
    ROOT_TAG = 'profiles'

    def __init__(self):
        super(Profiles, self).__init__()

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)

        converted = []
        json_profile_list = json_dict.get(cls.ROOT_TAG)

        for json_profile in json_profile_list:
            profile = Profile._dict_to_obj(json_profile)
            converted.append(profile)

        return converted


class Tenant(BaseMarshallingDomain):

    ROOT_TAG = 'tenant'

    def __init__(self, tenant_id=None, event_producers=None, hosts=None,
                 profiles=None):
        """An object that represents an tenants response object."""
        super(Tenant, self).__init__()
        self.tenant_id = tenant_id
        self.event_producers = event_producers
        self.hosts = hosts
        self.profiles = profiles

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        @param serialized_str:
        @return:
        """
        result = None
        ret = json.loads(serialized_str)
        if ret is not None:
                result = [cls._dict_to_obj(ret.get(cls.ROOT_TAG))]
        return result

    @classmethod
    def _dict_to_obj(cls, dic):
        """Helper method to turn dictionary into Xenmeta instance."""
        event_producers = cls._convert_to_type(Producer,
                                               dic.get('event_producers'))
        hosts = cls._convert_to_type(Host, dic.get('hosts'))
        profiles = cls._convert_to_type(Profile, dic.get('profiles'))

        kwargs = {
            'tenant_id': dic.get('tenant_id'),
            'event_producers': event_producers,
            'hosts': hosts,
            'profiles': profiles
        }
        return Tenant(**kwargs)

    @classmethod
    def _convert_to_type(cls, obj_type, data_array):
        result = None
        if len(data_array) > 0:
            result = []
            for item in data_array:
                result.append(obj_type._dict_to_obj(item))
        return result


class Producer(BaseMarshallingDomain):
    ROOT_TAG = 'event_producer'

    def __init__(self, pattern=None, durable=None, encrypted=None, id=None,
                 name=None):
        super(Producer, self).__init__()
        self.pattern = pattern
        self.durable = durable
        self.encrypted = encrypted
        self.id = id
        self.name = name

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = json.loads(serialized_str)
        return cls._dict_to_obj(ret.get(cls.ROOT_TAG))

    @classmethod
    def _dict_to_obj(cls, dic):
        """Helper method to turn dictionary into Xenmeta instance."""
        kwargs = {
            'pattern': dic.get('pattern'),
            'durable': dic.get('durable'),
            'encrypted': dic.get('encrypted'),
            'id': dic.get('id'),
            'name': dic.get('name')
        }
        return Producer(**kwargs)


class Producers(BaseMarshallingDomain):
    ROOT_TAG = 'event_producers'

    def __init__(self):
        super(Producers, self).__init__()

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)

        converted = []
        json_producer_list = json_dict.get(cls.ROOT_TAG)

        for json_producer in json_producer_list:
            producer = Producer._dict_to_obj(json_producer)
            converted.append(producer)

        return converted


class Host(BaseMarshallingDomain):
    ROOT_TAG = 'host'

    def __init__(self, ip_address_v6=None, profile=None, ip_address_v4=None,
                 hostname=None, id=None):
        super(Host, self).__init__()
        self.ip_address_v6 = ip_address_v6
        self.ip_address_v4 = ip_address_v4
        self.profile = profile
        self.hostname = hostname
        self.id = id

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = json.loads(serialized_str)
        return cls._dict_to_obj(ret.get(cls.ROOT_TAG))

    @classmethod
    def _dict_to_obj(cls, dic):
        """Helper method to turn dictionary into Xenmeta instance."""
        kwargs = {
            'ip_address_v6': dic.get('ip_address_v6'),
            'profile': dic.get('profile'),
            'ip_address_v4': dic.get('ip_address_v4'),
            'hostname': dic.get('hostname'),
            'id': dic.get('id')
        }
        return Host(**kwargs)


class Hosts(BaseMarshallingDomain):
    ROOT_TAG = 'hosts'

    def __init__(self):
        super(Hosts, self).__init__()

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)

        converted = []
        json_producer_list = json_dict.get(cls.ROOT_TAG)

        for json_producer in json_producer_list:
            producer = Host._dict_to_obj(json_producer)
            converted.append(producer)

        return converted


class Profile(BaseMarshallingDomain):
    ROOT_TAG = 'profile'

    def __init__(self, event_producers=None, id=None, name=None):
        super(Profile, self).__init__()
        self.event_producers = event_producers
        self.id = id
        self.name = name

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = json.loads(serialized_str)
        return cls._dict_to_obj(ret.get(cls.ROOT_TAG))

    @classmethod
    def _dict_to_obj(cls, dic):
        """Helper method to turn dictionary into Xenmeta instance."""
        kwargs = {
            'event_producers': dic.get('event_producers'),
            'id': dic.get('id'),
            'name': dic.get('name')
        }
        return Profile(**kwargs)
