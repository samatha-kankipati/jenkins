import json

from ccengine.domain.base_domain import BaseMarshallingDomain


class Worker(BaseMarshallingDomain):

    ROOT_TAG = 'worker'

    def __init__(self, host=None, created_at=None, updated_at=None,
                 process_id=None, id=None):

        super(Worker, self).__init__()
        self.host = host
        self.created_at = created_at
        self.updated_at = updated_at
        self.process_id = process_id
        self.id = id

    @classmethod
    def _json_to_obj(cls, serialized_str):

        ret = None

        json_dict = json.loads(serialized_str)

        if json_dict.get(cls.ROOT_TAG) is not None:
            ret = cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))

        if json_dict.get("{0}{1}".format(cls.ROOT_TAG, 's')) is not None:
            ret = []
            for item in json_dict.get("{0}{1}".format(cls.ROOT_TAG, 's')):
                ret.append(cls._dict_to_obj(item))

        return ret

    @classmethod
    def _dict_to_obj(cls, dic):

        return Worker(**dic)
