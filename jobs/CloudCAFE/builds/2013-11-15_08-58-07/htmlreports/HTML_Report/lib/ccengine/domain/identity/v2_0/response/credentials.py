import json
from xml.etree import ElementTree
from ccengine.domain.identity.v2_0.base_identity_domain \
    import BaseIdentityDomain, BaseIdentityDomainList


class Credentials(BaseIdentityDomainList):

    ROOT_TAG = 'credentials'

    def __init__(self, apiKeyCredentials=None, passwordCredentials=None):
        super(Credentials, self).__init__()
        self.apiKeyCredentials = apiKeyCredentials
        self.passwordCredentials = passwordCredentials

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        ret = cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))
        return ret

    @classmethod
    def _dict_to_obj(cls, json_dict):
        api_key_credentials = None
        password_credentials = None
        for element in json_dict:
            if ApiKeyCredentials.JSON_ROOT_TAG in element:
                api_key_credentials = ApiKeyCredentials \
                    ._dict_to_obj(element.get(ApiKeyCredentials.JSON_ROOT_TAG))
            if PasswordCredentials.ROOT_TAG in element:
                password_credentials = PasswordCredentials \
                    ._dict_to_obj(element.get(PasswordCredentials.ROOT_TAG))
        return Credentials(
            apiKeyCredentials=api_key_credentials,
            passwordCredentials=password_credentials)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_identity_xml_namespaces(element)
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        kwargs = {cls.ROOT_TAG: []}
        api_key_cred = xml_ele.find(ApiKeyCredentials.ROOT_TAG)
        pw_cred = xml_ele.find(PasswordCredentials.ROOT_TAG)
        if api_key_cred is not None:
            kwargs[cls.ROOT_TAG].\
                append(ApiKeyCredentials._xml_ele_to_obj(api_key_cred))
        if pw_cred is not None:
            kwargs[cls.ROOT_TAG].\
                append(PasswordCredentials._xml_ele_to_obj(pw_cred))
        return Credentials(**kwargs)


class ApiKeyCredentials(BaseIdentityDomain):

    ROOT_TAG = 'apiKeyCredentials'
    JSON_ROOT_TAG = 'RAX-KSKEY:{0}'.format(ROOT_TAG)

    def __init__(self, username=None, apiKey=None):
        super(ApiKeyCredentials, self).__init__()
        self.username = username
        self.apiKey = apiKey

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return ApiKeyCredentials(**json_dict.get(cls.JSON_ROOT_TAG))

    @classmethod
    def _dict_to_obj(cls, json_dict):
        if ApiKeyCredentials.JSON_ROOT_TAG in json_dict:
            json_dict[cls.ROOT_TAG] = json_dict[cls.JSON_ROOT_TAG]
            del json_dict[cls.JSON_ROOT_TAG]
        return ApiKeyCredentials(**json_dict)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_identity_xml_namespaces(element)
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        kwargs = {'username': xml_ele.get('username'),
                  'apiKey': xml_ele.get('apiKey')}
        return ApiKeyCredentials(**kwargs)


class PasswordCredentials(BaseIdentityDomain):

    ROOT_TAG = 'passwordCredentials'

    def __init__(self, username=None, password=None):
        super(PasswordCredentials, self).__init__()

        self.username = username
        self.password = password

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return PasswordCredentials(**json_dict.get(cls.ROOT_TAG))

    @classmethod
    def _dict_to_obj(cls, json_dict):
        return PasswordCredentials(**json_dict)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_identity_xml_namespaces(element)
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        kwargs = {'username': xml_ele.get('username'),
                  'password': xml_ele.get('password')}
        return PasswordCredentials(**kwargs)


class RackerPasswordCredentials(BaseIdentityDomain):

    ROOT_TAG = 'passwordCredentials'

    def __init__(self, username=None, password=None):
        super(PasswordCredentials, self).__init__()
        self.username = username
        self.password = password

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return PasswordCredentials(**json_dict.get(cls.ROOT_TAG))

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_identity_xml_namespaces(element)
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        kwargs = {'username': xml_ele.get('username'),
                  'password': xml_ele.get('password')}
        return PasswordCredentials(**kwargs)
