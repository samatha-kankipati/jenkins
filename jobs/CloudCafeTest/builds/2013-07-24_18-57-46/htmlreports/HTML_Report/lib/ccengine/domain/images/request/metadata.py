from ccengine.domain.base_domain import BaseMarshallingDomain
import json


class Metadata(BaseMarshallingDomain):

    ROOT_TAG = 'metadata'

    def __init__(self, keys=None, values=None):

        super(Metadata, self).__init__()
        self.pairs = dict(zip(keys, values))

    def _obj_to_json(self):

        ret = self._obj_to_dict()

        return json.dumps({self.ROOT_TAG: ret})

    def _obj_to_xml(self):

        pass

    def _obj_to_dict(self):

        ret = {}

        if self.pairs is not None:
            ret = self.pairs

        return ret
