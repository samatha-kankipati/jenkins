from ccengine.domain.identity.v2_0.base_identity_domain \
    import BaseIdentityDomain
import json


class RateLimit(BaseIdentityDomain):

    ROOT_TAG = 'rateLimitConfig'

    def __init__(self, enabled=None, interval=None, threshold=None,
                 allow=None):

        super(RateLimit, self).__init__()
        self.enabled = enabled
        self.interval = interval
        self.threshold = threshold
        self.allow = allow

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)
