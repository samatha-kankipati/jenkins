from ccengine.domain.base_domain import BaseMarshallingDomain, \
    BaseMarshallingDomainList
import json
import xml.etree.ElementTree as ET


class AlgorithmList(BaseMarshallingDomainList):

    ROOT_TAG = 'algorithms'

    def __init__(self, algorithms=[]):
        super(AlgorithmList, self).__init__()
        for algorithm in algorithms:
            self.append(algorithm)

    def get_weighted(self):
        return [algorithm for algorithm in self
                if 'WEIGHTED' in algorithm.name]

    def get_non_weighted(self):
        return [algorithm for algorithm in self
                if 'WEIGHTED' not in algorithm.name]

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        if cls.ROOT_TAG not in json_dict:
            return None
        return cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        pass

    @classmethod
    def _dict_to_obj(cls, algorithm_dict):
        kwargs = {cls.ROOT_TAG: [Algorithm._dict_to_obj(algorithm)
                                 for algorithm in algorithm_dict]}
        return AlgorithmList(**kwargs)


class Algorithm(BaseMarshallingDomain):

    ROOT_TAG = ''

    _algorithm_zeus_dict = {'ROUND_ROBIN': 'roundrobin',
                            'WEIGHTED_ROUND_ROBIN': 'wroundrobin',
                            'LEAST_CONNECTIONS': 'connections',
                            'RANDOM': 'random',
                            'WEIGHTED_LEAST_CONNECTIONS': 'wconnections'}

    def __init__(self, name=None):
        self.name = name

    @classmethod
    def zeus_name(cls, name=None):
        if name is None:
            return cls._algorithm_zeus_dict.get(cls.name)
        else:
            return cls._algorithm_zeus_dict.get(name)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        pass

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        pass

    @classmethod
    def _dict_to_obj(cls, dic):
        return Algorithm(**dic)
