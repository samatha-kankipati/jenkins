from ccengine.domain.base_domain import BaseDomain
from ccengine.domain.base_domain import BaseMarshallingDomain
import xml.etree.ElementTree as ET
from ccengine.common.tools.equality_tools import EqualityTools
from ccengine.common.tools.datatools import string_to_datetime, \
    convert_date_from_cst_to_utc_date
from datetime import datetime
import time
import os


class AccountServices(BaseMarshallingDomain):

    ROOT_TAG = ''

    def __init__(self, **kwargs):
        '''An object that represents an account services response object.
        Keyword arguments:
        '''
        super(AccountServices, self).__init__(**kwargs)
        for keys, values in kwargs.items():
            setattr(self, keys, values)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        '''Returns an instance of a Account svs based on the
        xml serialized_str passed in.'''
        element = ET.fromstring(serialized_str)
        cls._remove_namespace(element,
                              'http://rackspace.com/service/account/v1.0')

        if element.tag == 'account':
            account = cls._xml_ele_to_obj(element)
            for child in element:
                if (child.tag == "profiles"):
                    setattr(account, "highProfile", False)
                    for sub_child in child:
                        if sub_child.tag == "profile":
                            setattr(account, "highProfile", True)
            return account

        if element.tag == 'accounts':
            accounts = cls._xml_ele_to_obj(element)
            return accounts

        if element.tag == 'accountGroup':
            accounts = []
            for account in element.findall('account'):
                account = cls._xml_ele_to_obj(account)
                accounts.append(account)
            return accounts

    @classmethod
    def _xml_ele_to_obj(cls, element):
        '''Helper method to turn ElementTree instance to
        accountsvs instance.'''
        account_dict = element.attrib
        account = AccountServices(**account_dict)
        return account

    @classmethod
    def _dict_to_obj(cls, dict_obj):
        account_details = AccountServices(**dict_obj)
        if hasattr(account_details, "number"):
            account_details.number = str(account_details.number)
        if not hasattr(account_details, "updatedAt"):
            setattr(account_details, "updatedAt", None)
        del account_details.id
        if hasattr(account_details, "documentLastUpdatedTimestamp"):
            del account_details.documentLastUpdatedTimestamp
        return account_details

    def __eq__(self, other):
        return EqualityTools.\
            are_objects_equal(self, other,
                              keys_to_exclude=["userName",
                                               "hybridNetworking",
                                               "region", "salesForceType",
                                               "slaType",
                                               "accountManagerGeoLocation",
                                               "_log", "updatedAt"])
