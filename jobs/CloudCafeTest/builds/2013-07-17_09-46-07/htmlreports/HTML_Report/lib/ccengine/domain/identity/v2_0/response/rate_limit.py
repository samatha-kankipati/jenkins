import json
from xml.etree import ElementTree
from ccengine.domain.identity.v2_0.base_identity_domain \
    import BaseIdentityDomain, BaseIdentityDomainList


class RateLimit(BaseIdentityDomain):

    ROOT_TAG = 'rateLimitConfigRepresentation'

    def __init__(self, enabled=None, interval=None, threshold=None):
        '''An object that represents an imperson response object.
        Keyword arguments:
        '''
        super(RateLimit, self).__init__()
        self.enabled = enabled
        self.interval = interval
        self.threshold = threshold

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        ret = cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))
        return ret

    @classmethod
    def _dict_to_obj(cls, json_dict):
        ratelim = RateLimit(**json_dict)
        return ratelim
