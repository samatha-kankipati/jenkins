from ccengine.domain.base_domain import BaseMarshallingDomain
import json


class Metadata(BaseMarshallingDomain):

    ROOT_TAG = 'metadata'

    def __init__(self, keys=None, values=None, bad_body=None):

        super(Metadata, self).__init__()
        self.pairs = dict(zip(keys, values))
        self.bad_body = bad_body

    def _obj_to_json(self):

        ret = self._obj_to_dict()

        if self.bad_body is not None:
            self.ROOT_TAG = self.bad_body

        return json.dumps({self.ROOT_TAG: ret})

    def _obj_to_xml(self):

        pass

    def _obj_to_dict(self):

        ret = {}

        if self.pairs is not None:
            ret = self.pairs

        return ret
