from ccengine.domain.base_domain import BaseDomain
from ccengine.domain.base_domain import BaseMarshallingDomain
import json


class Core(BaseMarshallingDomain):

    def __init__(self, **kwargs):
        super(Core, self).__init__(**kwargs)
        for keys, values in kwargs.items():
            setattr(self, keys, values)

    @classmethod
    def _json_to_obj(cls, serialized_str):

        ret = None
        json_dict = json.loads(serialized_str)
        json_dict = json_dict[0]
        if 'result' in json_dict.keys():
            if type(json_dict.get('result')) is list:
                ret = []
                for result in json_dict['result']:
                    if  type(result) is dict:
                        s = cls._dict_to_obj(result)
                        ret.append(s)
                    else:
                        ret.append(result)
            elif isinstance(json_dict.get('result'), basestring):
                ret = cls._dict_to_obj(json_dict)
            elif isinstance(json_dict.get('result'), int):
                ret = cls._dict_to_obj(json_dict)
            else:
                ret = {}
                ret = cls._dict_to_obj(json_dict.get('result'))
        return ret

    @classmethod
    def _dict_to_obj(cls, result_dict):
        core = Core(**result_dict)
        return core


class Value(BaseMarshallingDomain):

    def __init__(self, **kwargs):
        super(Value, self).__init__(**kwargs)
        for keys, values in kwargs.items():
            setattr(self, keys, values)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = None
        json_dict = json.loads(serialized_str)
        ret = json_dict
        return ret

    def __repr__(self):
        values = []
        for prop in self.__dict__:
            values.append("%s: %s" % (prop, self.__dict__[prop]))
        return '[' + ', '.join(values) + ']'
