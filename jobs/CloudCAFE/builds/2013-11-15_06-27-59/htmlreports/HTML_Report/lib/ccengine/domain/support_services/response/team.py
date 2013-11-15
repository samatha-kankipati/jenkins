import json

from ccengine.domain.base_domain import BaseMarshallingDomain
from ccengine.domain.support_services.response.support_service import Badges,\
    Roles, ChatTeam, PhoneNumbers


class SupportTeam(BaseMarshallingDomain):

    def __init__(self, team_badges,
                 team_id, team_name, team_description,
                 team_business_unit, team_segment,
                 team_parent, team_roles,
                 chat_teams, phone_numbers, team_tags,
                 team_internal_phone_numbers, team_internal_emails):

        self.team_badges = team_badges
        self.team_id = team_id
        self.team_name = team_name
        self.team_description = team_description
        self.team_business_unit = team_business_unit
        self.team_segment = team_segment
        self.chat_teams = chat_teams
        self.phone_numbers = phone_numbers
        self.team_parent = team_parent
        self.team_roles = team_roles
        self.team_tags = team_tags
        self.team_internal_phone_numbers = team_internal_phone_numbers
        self.team_internal_emails = team_internal_emails

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = []
        json_dict = json.loads(serialized_str)
        if json_dict.get('teams') is not None:
            for team in json_dict.get('teams'):
                ret.append(cls._dict_to_obj(team))
        else:
            ret.append(cls._dict_to_obj(json_dict))
        return ret

    @classmethod
    def _dict_to_obj(cls, team_dict):
        team_obj = SupportTeam(**team_dict)
        if len(team_obj.team_badges) != 0:
            team_badges = [Badges._dict_to_obj(team_badge) for
                           team_badge in team_obj.team_badges]
            team_obj.team_badges = team_badges

        if len(team_obj.team_roles) != 0:
            team_roles = [Roles._dict_to_obj(team_role) for
                          team_role in team_obj.team_roles]
            team_obj.team_roles = team_roles

        if len(team_obj.chat_teams) != 0:
            chat_teams = [ChatTeam._dict_to_obj(chat_team) for
                          chat_team in team_obj.chat_teams]
            team_obj.chat_teams = chat_teams

        if len(team_obj.phone_numbers) != 0:
            phone_numbers = [PhoneNumbers._dict_to_obj(phone_number) for
                             phone_number in team_obj.phone_numbers]
            team_obj.phone_numbers = phone_numbers

        return team_obj
