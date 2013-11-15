from datetime import datetime
import os
import re
import time
import xml.etree.ElementTree as ET

from ccengine.domain.base_domain import BaseDomain
from ccengine.domain.base_domain import BaseMarshallingDomain
from ccengine.common.tools.datatools import string_to_datetime, \
    convert_date_from_cst_to_utc_date
from ccengine.common.tools.equality_tools import EqualityTools


class AccountServices(BaseMarshallingDomain):

    def __init__(self, hybrid_networking=None, region=None,
                 sales_force_sub_type=None, number=None, team=None,
                 sla_type=None, rcn=None, account_manager_geo_location=None,
                 type=None, name=None, status=None,
                 document_last_updated_timestamp=None,
                 id=None, total=None, limit=None, offset=None,
                 updated_at=None, high_profile=None, team_segment=None,
                 user_name=None, service_level=None,
                 team_territory_code=None, contact_names=None,
                 contact_sso=None, contacts=None, contact_roles=None):
        '''An object that represents an account services response object.
        Keyword arguments:
        '''
        super(AccountServices, self).__init__()
        self.hybrid_networking = hybrid_networking
        self.name = name
        self.region = region
        self.sales_force_sub_type = sales_force_sub_type
        self.number = number
        self.sla_type = sla_type
        self.rcn = rcn
        self.account_manager_geo_location = account_manager_geo_location
        self.type = type
        self.name = name
        self.status = status
        self.document_last_updated_timestamp = document_last_updated_timestamp
        self.id = id
        self.total = total
        self.limit = limit
        self.offset = offset
        self.updated_at = updated_at
        self.team = team
        self.high_profile = high_profile
        self.team_segment = team_segment
        self.user_name = user_name
        self.service_level = service_level
        self.team_territory_code = team_territory_code
        self.contact_names = contact_names
        self.contact_roles = contact_roles
        self.contact_sso = contact_sso
        self.contacts = contacts

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
        for key_ref in account_dict.keys():
            account_dict[
                re.sub('([a-z0-9])([A-Z])', r'\1_\2', key_ref).lower()
            ] = account_dict.pop(key_ref)
        account = AccountServices(**account_dict)
        return account

    @classmethod
    def _dict_to_obj(cls, dict_obj):
        for key_ref in dict_obj.keys():
            dict_obj[
                re.sub('([a-z0-9])([A-Z])', r'\1_\2', key_ref).lower()
            ] = dict_obj.pop(key_ref)
        account_details = AccountServices(**dict_obj)
        if hasattr(account_details, "number"):
            account_details.number = str(account_details.number)
        if not hasattr(account_details, "updated_at"):
            setattr(account_details, "updated_at", None)
        del account_details.id
        if hasattr(account_details, "document_last_updated_timestamp"):
            del account_details.document_last_updated_timestamp
        if hasattr(account_details, "contacts"):
            if account_details.contacts is not None:
                contacts_name_list = []
                contacts_sso_list = []
                contacts_role_list = []
                for i in range(len(account_details.contacts)):
                    contacts_name_list.append(
                        (account_details.contacts[i]).get('name'))
                    contacts_sso_list.append(
                        (account_details.contacts[i]).get('sso'))
                    contacts_role_list.append(
                        (account_details.contacts[i]).get('role'))
                account_details.contact_names = contacts_name_list
                account_details.contact_sso = contacts_sso_list
                account_details.contact_roles = contacts_role_list
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
                                               "high_profile",
                                               "team", "team_segment",
                                               "contacts",
                                               "contact_names",
                                               "contact_roles",
                                               "contact_sso",
                                               "service_level",
                                               "team_territory_code"])
