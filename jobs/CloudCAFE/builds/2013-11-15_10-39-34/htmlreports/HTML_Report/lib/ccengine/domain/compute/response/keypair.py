import json

from ccengine.domain.base_domain import BaseMarshallingDomain
from ccengine.common.tools.equality_tools import EqualityTools


class Keypair(BaseMarshallingDomain):

    def __init__(self, public_key, name, fingerprint, private_key=None):
        self.public_key = public_key
        self.name = name
        self.fingerprint = fingerprint
        self.private_key = private_key

    def __repr__(self):
        values = []
        for prop in self.__dict__:
            values.append("%s: %s" % (prop, self.__dict__[prop]))
        return '[' + ', '.join(values) + ']'

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict.get('keypair'))

    @classmethod
    def _dict_to_obj(cls, json_dict):
        return Keypair(json_dict.get('public_key'),
                       json_dict.get('name'),
                       json_dict.get('fingerprint'),
                       json_dict.get('private_key'))

    def __eq__(self, other):
        """
        @summary: Overrides the default equals
        @param other: Flavor object to compare with
        @type other: Flavor
        @return: True if Flavor objects are equal, False otherwise
        @rtype: bool
        """
        return EqualityTools.are_objects_equal(self, other)

    def __ne__(self, other):
        """
        @summary: Overrides the default not-equals
        @param other: Flavor object to compare with
        @type other: Flavor
        @return: True if Flavor objects are not equal, False otherwise
        @rtype: bool
        """
        return not self == other


class Keypairs(Keypair):

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = []
        json_dict = json.loads(serialized_str)
        key_list = json_dict.get('keypairs')

        for key in key_list:
            key = key.get('keypair')
            ret.append(Keypair(key.get('public_key'),
                               key.get('name'),
                               key.get('fingerprint'),
                               key.get('private_key')))
        return ret
