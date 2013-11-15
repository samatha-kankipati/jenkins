from ccengine.domain.base_domain import BaseMarshallingDomain, \
    BaseMarshallingDomainList
import xml.etree.ElementTree as ET
import json


class HostCustomerCount(BaseMarshallingDomainList):

    ROOT_TAG = 'accountInHosts'

    def __init__(self, totalAccounts=None, accountInHosts=None):
        '''An object that holds information about the number of accounts in a
                host
        '''
        self.totalAccounts = totalAccounts
        for account in accountInHosts:
            self.append(account)

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret[self.ROOT_TAG])

    def _obj_to_xml(self):
        ret = self._auto_to_xml()
        return ET.tostring(ret)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        pass

    @classmethod
    def _dict_to_obj(cls, dic):
        kwargs = {cls.ROOT_TAG: [AccountInHost._dict_to_obj(account)
                                 for account in dic]}
        return HostCustomerCount(**kwargs)


class AccountInHost(BaseMarshallingDomain):

    ROOT_TAG = 'accountInHost'

    def __init__(self, accountId=None, hostId=None, loadBalancerCount=None):
        '''An object to hold information about a single account on a host

        '''
        self.accountId = accountId
        self.hostId = hostId
        self.loadBalancerCount = loadBalancerCount

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret[self.ROOT_TAG])

    def _obj_to_xml(self):
        ret = self._auto_to_xml()
        return ET.tostring(ret)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        pass

    @classmethod
    def _dict_to_obj(cls, dic):
        return AccountInHost(**dic)
