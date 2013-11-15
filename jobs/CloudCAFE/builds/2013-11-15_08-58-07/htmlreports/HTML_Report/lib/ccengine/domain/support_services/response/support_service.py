import json
import re

from ccengine.domain.base_domain import BaseDomain
from ccengine.domain.base_domain import BaseMarshallingDomain


class Groups(BaseMarshallingDomain):

    def __init__(self, group_id=None, group_name=None, group_users=None):
        self.group_id = group_id
        self.group_name = group_name.encode('utf8')
        self.group_users = group_users

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = []
        json_dict = json.loads(serialized_str)
        if json_dict.get('groups') is not None:
            for group in json_dict.get('groups'):
                ret.append(cls._dict_to_obj(group))
        else:
            ret.append(cls._dict_to_obj(json_dict))
        return ret

    @classmethod
    def _dict_to_obj(cls, groups_dict):
        group = Groups(**groups_dict)
        if group.group_users is not None:
            group_users = [Users._dict_to_obj(group_user)
                           for group_user in group.group_users]
            group.group_users = group_users

        return group


class SupportAccounts(BaseMarshallingDomain):

    def __init__(self, account_service_level=None, chat_teams=None,
                 phone_teams=None, account_badges=None,
                 account_roles=None, account_teams=None, account_name=None,
                 account_linked_account=None, account_tags=None):

        self.account_service_level = account_service_level
        self.chat_teams = chat_teams
        self.phone_teams = phone_teams
        self.account_badges = account_badges
        self.account_roles = account_roles
        self.account_teams = account_teams
        self.account_name = account_name
        self.account_linked_account = account_linked_account
        self.account_tags = account_tags

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, support_accounts_dict):
        support_accounts = SupportAccounts(**support_accounts_dict)
        if support_accounts.chat_teams is not None:
            chat_teams = [ChatTeam._dict_to_obj(chat_team)
                          for chat_team in support_accounts.chat_teams]
            support_accounts.chat_teams = chat_teams

        if support_accounts.phone_teams is not None:
            phone_teams = [PhoneNumbers._dict_to_obj(phone_team) for
                             phone_team in support_accounts.phone_teams]
            support_accounts.phone_teams = phone_teams

        if support_accounts.account_badges is not None:
            account_badges = [Badges._dict_to_obj(account_badge) for
                              account_badge in support_accounts.account_badges]
            support_accounts.account_badges = account_badges

        if support_accounts.account_teams is not None:
            teams = [Teams._dict_to_obj(team) for
                     team in support_accounts.account_teams]
            support_accounts.account_teams = teams

        if support_accounts.account_roles is not None:
            roles = [Roles._dict_to_obj(role) for
                     role in support_accounts.account_roles]
            support_accounts.account_roles = roles

        return support_accounts


class ChatTeam(BaseMarshallingDomain):

    def __init__(self, chat_team_name=None, chat_team_html=None,
                 team_id=None, team_name=None, chat_team_url=None,
                 team_flags=None):
        self.chat_team_name = chat_team_name
        self.chat_team_html = chat_team_html
        self.team_id = team_id
        self.team_name = team_name
        self.chat_team_url = chat_team_url
        self.team_flags = team_flags

    @classmethod
    def _dict_to_obj(cls, chat_team_dict):
        chat_team_obj = ChatTeam(**chat_team_dict)
        return chat_team_obj


class PhoneNumbers(BaseMarshallingDomain):

    def __init__(self, phone_number_name=None, team_id=None,
                 team_name=None, phone_numbers=None,
                 phone_number_flags=None, team_flags=None,
                 phone_team_name=None):
        self.phone_number_name = phone_number_name
        self.team_id = team_id
        self.team_name = team_name
        self.phone_numbers = phone_numbers
        self.team_flags = team_flags
        self.phone_team_name = phone_team_name

    @classmethod
    def _dict_to_obj(cls, phone_number_dict):
        phone_number_obj = PhoneNumbers(**phone_number_dict)
        if phone_number_obj.phone_numbers is not None:
            phone_numbers = [PhoneNumber._dict_to_obj(phone_number) for
                             phone_number in phone_number_obj.phone_numbers]
            phone_number_obj.phone_numbers = phone_numbers        
        return phone_number_obj


class PhoneNumber(BaseMarshallingDomain):

    def __init__(self, country_code=None, phone_number= None,
                 phone_number_flags=None):
        self.country_code = country_code
        self.phone_number = phone_number
        self.phone_number_flags = phone_number_flags

    @classmethod
    def _dict_to_obj(cls, phone_number_dict):
        phone_number_obj = PhoneNumber(**phone_number_dict)
        return phone_number_obj


class Teams(BaseMarshallingDomain):

    def __init__(self, team_type=None, team_badges=None,
                 team_id=None, team_name=None, team_tags=None,
                 team_flags=None, team_business_unit=None,
                 team_segment=None, team_description=None,
                 team_internal_phone_numbers=None,
                 team_internal_emails=None):

        self.team_type = team_type
        self.team_badges = team_badges
        self.team_id = team_id
        self.team_name = team_name
        self.team_tags = team_tags
        self.team_flags = team_flags
        self.team_business_unit = team_business_unit
        self.team_segment = team_segment
        self.team_description = team_description
        self.team_internal_phone_numbers = team_internal_phone_numbers
        self.team_internal_emails = team_internal_emails

    @classmethod
    def _dict_to_obj(cls, team_dict):
        team_obj = Teams(**team_dict)

        if team_obj.team_badges is not None:
            team_badges = [Badges._dict_to_obj(team_badge) for
                           team_badge in team_obj.team_badges]
            team_obj.team_badges = team_badges

        return team_obj


class Badges(BaseMarshallingDomain):

    def __init__(self, badge_name=None, badge_description=None,
                 badge_url=None):

        self.badge_name = badge_name
        self.badge_description = badge_description
        self.badge_url = badge_url

    @classmethod
    def _dict_to_obj(cls, badges_dict):
        badges_obj = Badges(**badges_dict)
        return badges_obj


class Users(BaseMarshallingDomain):

    def __init__(self, user_id=None, user_sso=None,
                 user_name=None, user_badges=None, user_tags=None,
                 user_email=None):

        self.user_id = user_id
        self.user_sso = user_sso
        self.user_name = user_name
        self.user_badges = user_badges
        self.user_tags = user_tags
        self.user_email = user_email

    @classmethod
    def _dict_to_obj(cls, user_dict):
        user_obj = Users(**user_dict)

        if user_obj.user_badges is not None:
            user_badges = [Badges._dict_to_obj(user_badge) for
                           user_badge in user_obj.user_badges]
            user_obj.user_badges = user_badges

        return user_obj


class Roles(Users):

    def __init__(self, role=None, user_id=None, user_sso=None,
                 user_name=None, user_badges=None, user_tags=None,
                 user_email=None):

        Users.__init__(self, user_id, user_sso, user_name,
                       user_badges, user_tags, user_email)
        self.role = role

    @classmethod
    def _json_to_obj(cls, serialized_str):
        roles = []
        json_dict = json.loads(serialized_str)
        for role in json_dict.get("roles"):
            roles.append(cls._dict_to_obj(role))

        return roles

    @classmethod
    def _dict_to_obj(cls, role_dict):
        role_obj = Roles(**role_dict)

        if role_obj.user_badges is not None:
            user_badges = [Badges._dict_to_obj(user_badge) for
                           user_badge in role_obj.user_badges]
            role_obj.user_badges = user_badges

        return role_obj
