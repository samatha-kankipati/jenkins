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

    def __init__(self, hybridNetworking=None, userName=None, region=None,
                 salesForceSubType=None, number=None, team=None,
                 slaType=None, rcn=None, accountManagerGeoLocation=None,
                 type=None, name=None, status=None,
                 documentLastUpdatedTimestamp=None,
                 id=None, total=None, limit=None, offset=None,
                 updatedAt=None, highProfile=None):
        '''An object that represents an account services response object.
        Keyword arguments:
        '''
        super(AccountServices, self).__init__()
        self.hybrid_networking = hybridNetworking
        self.name = name
        self.region = region
        self.sales_force_sub_type = salesForceSubType
        self.number = number
        self.sla_type = slaType
        self.rcn = rcn
        self.account_manager_geo_location = accountManagerGeoLocation
        self.type = type
        self.name = name
        self.status = status
        self.document_last_updated_timestamp = documentLastUpdatedTimestamp
        self.id = id
        self.total = total
        self.limit = limit
        self.offset = offset
        self.updated_at = updatedAt
        self.user_name = userName
        self.team = team
        self.highProfile = highProfile

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        '''Returns an instance of a Account svs based on the
        xml serialized_str passed in.'''
        element = ET.fromstring(serialized_str)
        cls._remove_namespace(element,
                              'http://rackspace.com/service/account/v1.0')

        if element.tag == 'account':
            account = cls._xml_ele_to_obj(element)
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
        if not hasattr(account_details, "updated_at"):
            setattr(account_details, "updated_at", None)
        del account_details.id
        if hasattr(account_details, "document_last_updated_timestamp"):
            del account_details.document_last_updated_timestamp
        return account_details

    def __eq__(self, other):
        return EqualityTools.\
            are_objects_equal(self, other,
                              keys_to_exclude=["user_name",
                                               "hybrid_networking",
                                               "region",
                                               "sales_force_sub_type",
                                               "sla_type",
                                               "account_manager_geo_location",
                                               "_log", "updated_at", "id",
                                               "highProfile",
                                               "team"])
