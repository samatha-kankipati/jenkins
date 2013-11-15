import json

from ccengine.domain.base_domain import BaseMarshallingDomain


class Metadata(BaseMarshallingDomain):

    ROOT_TAG = 'metadata'

    def __init__(self, key=None, value=None):

        super(Metadata, self).__init__()
        self.key = key
        self.value = value

    @classmethod
    def _json_to_obj(cls, serialized_str):

        ret = None

        json_dict = json.loads(serialized_str)

        if json_dict.get(cls.ROOT_TAG) is not None:
            ret = {}
            for key, value in json_dict.get(cls.ROOT_TAG).items():
                ret.update({key: value})

        return ret

    @classmethod
    def _dict_to_obj(cls, dic):

        return dic
