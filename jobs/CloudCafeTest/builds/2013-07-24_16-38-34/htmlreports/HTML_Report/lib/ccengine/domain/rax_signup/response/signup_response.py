import json
from xml.etree import ElementTree
from ccengine.domain.base_domain import\
        BaseMarshallingDomain, BaseMarshallingDomainList
from ccengine.domain.rax_signup.request.signup_request import \
        BaseMarshallingSubDomain, BaseMarshallingSubDomainList


class ReferenceEntity(BaseMarshallingDomain):
    ROOT_TAG = 'referenceEntity'
    def __init__(self, id_=None):
        self.id_ = id_

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        #Look into removing the name spaces
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        kwargs = {'id': xml_ele.get('id')}
        return ReferenceEntity(**kwargs)

    #Response Deserializers
    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return ReferenceEntity(id_=json_dict.get('id'))


class ListSignupResponse(BaseMarshallingDomain):
    def __init__(self, limit=None, marker=None, total=None, xmlns=None,
                 xmlns_atom=None, link=None, signup=None):
        self.limit = limit
        self.marker = marker
        self.total = total
        self.xmlns = xmlns
        self.xmlns_atom = xmlns_atom
        self.link = ListSignupResponse_LinkList()
        self.signups = ListSignupResponse_SignupList()

        self.link.extend_new_links(link)
        self.signups.extend_new_signups(signup)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        limit = json_dict.get('limit')
        marker = json_dict.get('marker')
        total = json_dict.get('total')

        #Convert the args from the json response into local args
        #This allows us to replace "problem args" like args with dashes in them
        #into usable python params
        links = json_dict.get('link')
        signup = json_dict.get('signup')
        arg_translation_dict = {"id": "id_", "type": "type_",
                                "referenceEntityId": "reference_entity_id"}
        for i in range(len(signup)):
            for json_arg in arg_translation_dict:
                local_arg = arg_translation_dict.get(json_arg)
                signup[i][local_arg] = signup[i].get(json_arg)
                if signup[i][local_arg] is not None:
                    del signup[i][json_arg]
        return ListSignupResponse(limit=limit, marker=marker, total=total,
                                  link=links, signup=signup)


class ListSignupResponse_SignupList(BaseMarshallingDomainList):
    def append_new_signup(self, date=None, duration=None, id_=None,
                          reference_entity_id=None, region=None, status=None,
                          type_=None, description=None, link=None):
        self.append(ListSignupResponse_SignupItem(
                        date=date, duration=duration, id_=id_,
                        reference_entity_id=reference_entity_id, region=region,
                        status=status, type_=type_, description=description,
                        link=link))

    def extend_new_signups(self, list_of_kwarg_dicts):
        list_of_kwarg_dicts = list_of_kwarg_dicts or []
        if list_of_kwarg_dicts is not None:
            for kwarg_dict in list_of_kwarg_dicts:
                self.append_new_signup(**kwarg_dict)


class ListSignupResponse_SignupItem(BaseMarshallingDomain):
    def __init__(self, date=None, duration=None, id_=None,
                 reference_entity_id=None, region=None, status=None,
                 type_=None, description=None, link=None):

        self.date = date
        self.duration = duration
        self.id_ = id_
        self.reference_entity_id = reference_entity_id
        self.region = region
        self.status = status
        self.type_ = type_
        self.description = description
        self.link = ListSignupResponse_LinkList()

        #Init sub domain objects
        self.link.extend_new_links(link)


class ListSignupResponse_Description(BaseMarshallingDomain):
    def __init__(self, description=None):
        self.description = description


class ListSignupResponse_Link(BaseMarshallingDomain):
    def __init__(self, href=None, rel=None):
        self.href = href
        self.rel = rel


class ListSignupResponse_LinkList(BaseMarshallingDomainList):
    def append_new_link(self, href=None, rel=None):
        self.append(ListSignupResponse_Link(href=href, rel=rel))

    def extend_new_links(self, list_of_kwarg_dicts):
        list_of_kwarg_dicts = list_of_kwarg_dicts or []
        if list_of_kwarg_dicts is not None:
            for kwarg_dict in list_of_kwarg_dicts:
                self.append_new_link(**kwarg_dict)
