from ccengine.domain.base_domain import BaseMarshallingDomain, \
    BaseMarshallingDomainList
from ccengine.domain.lbaas.mgmt.load_balancer import LoadBalancerList
import xml.etree.ElementTree as ET
import json


class CustomerList(BaseMarshallingDomain):

    ROOT_TAG = 'customerList'

    def __init__(self, customers=None):
        '''A management load balancer list object

        '''
        self.customers = customers

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
        if Customers.ROOT_TAG in dic:
            dic[Customers.ROOT_TAG] = \
                Customers._dict_to_obj(dic.get(Customers.ROOT_TAG))
        return CustomerList(**dic)


class Customers(BaseMarshallingDomainList):

    ROOT_TAG = 'customers'

    def __init__(self, customers=None):
        '''An object detailing specific fields of a load balancer

        '''
        for customer in customers:
            self.append(customer)

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
        kwargs = {cls.ROOT_TAG: [Customer._dict_to_obj(customer)
                                 for customer in dic]}
        return Customers(**kwargs)


class Customer(BaseMarshallingDomain):

    ROOT_TAG = 'customer'

    def __init__(self, accountId=None, loadBalancers=None):
        '''An object detailing specific fields of a load balancer

        '''
        self.accountId = accountId
        self.loadBalancers = loadBalancers

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
        if LoadBalancerList.ROOT_TAG in dic:
            dic[LoadBalancerList.ROOT_TAG] = \
                LoadBalancerList._dict_to_obj(dic.get(
                    LoadBalancerList.ROOT_TAG))
        return Customer(**dic)


class CustomersById(BaseMarshallingDomain):

    ROOT_TAG = 'byIdOrName'

    def __init__(self, id=None):
        '''A management load balancer list object

        '''
        self.id = id

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
        return CustomersById(**dic)


class CustomersByName(BaseMarshallingDomain):

    ROOT_TAG = 'byIdOrName'

    def __init__(self, name=None):
        '''A management load balancer list object

        '''
        self.name = name

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
        return CustomersByName(**dic)
