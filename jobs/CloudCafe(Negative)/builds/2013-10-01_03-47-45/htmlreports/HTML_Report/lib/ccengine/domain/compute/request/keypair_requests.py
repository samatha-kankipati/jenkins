from ccengine.domain.base_domain import BaseMarshallingDomain
import json


class CreateKeypair(BaseMarshallingDomain):

    def __init__(self, name, public_key=None):
        super(CreateKeypair, self).__init__()
        self.name = name
        self.public_key = public_key

    def _obj_to_json(self):
        ret = {'keypair': self._obj_to_dict()}
        return json.dumps(ret)

    def _obj_to_dict(self):
        ret = {}
        ret['name'] = self.name
        if self.public_key is not None:
            ret['public_key'] = self.public_key
        return ret

    def _obj_to_xml(self):
        raise NotImplemented

    def _obj_to_xml_ele(self):
        raise NotImplemented
