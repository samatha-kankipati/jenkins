import json
from xml.etree import ElementTree
from ccengine.domain.identity.v2_0.base_identity_domain \
    import BaseIdentityDomain, BaseIdentityDomainList
from ccengine.domain.identity.v2_0.response.user import User
from ccengine.domain.identity.v2_0.response.tenant import Tenant
from ccengine.domain.identity.v2_0.response.endpoint import Endpoints, Endpoint
from ccengine.domain.identity.v2_0.response.role import Roles


class Access(BaseIdentityDomain):

    ROOT_TAG = 'access'

    def __init__(self, token=None, impersonation=None, serviceCatalog=None, user=None):
        '''An object that represents an groups response object.
        '''
        super(Access, self).__init__()
        self.token = token
        self.impersonation = impersonation
        self.serviceCatalog = serviceCatalog
        self.user = user

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        ret = cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))
        return ret

    @classmethod
    def _dict_to_obj(cls, json_dict):
        if Token.ROOT_TAG in json_dict:
            json_dict[Token.ROOT_TAG] = \
                Token._dict_to_obj(json_dict[Token.ROOT_TAG])
        if Impersonation.ROOT_TAG in json_dict:
            json_dict[Impersonation.ROOT_TAG] = \
                Impersonation._dict_to_obj(
                    json_dict.get(Impersonation.ROOT_TAG, {}))
        if User.ROOT_TAG in json_dict:
            json_dict[User.ROOT_TAG] = \
                User._dict_to_obj(json_dict[User.ROOT_TAG])
        if ServiceCatalog.ROOT_TAG in json_dict:
            json_dict[ServiceCatalog.ROOT_TAG] = \
                ServiceCatalog._list_to_obj(json_dict[ServiceCatalog.ROOT_TAG])
        return Access(
            token=json_dict.get(Token.ROOT_TAG),
            serviceCatalog=json_dict.get(ServiceCatalog.ROOT_TAG),
            user=json_dict.get(User.ROOT_TAG),
            impersonation=json_dict.get(Impersonation.ROOT_TAG))

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_identity_xml_namespaces(element)
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        kwargs = {}
        token = xml_ele.find(Token.ROOT_TAG)
        serviceCatalog = xml_ele.find(ServiceCatalog.ROOT_TAG)
        user = xml_ele.find(User.ROOT_TAG)
        if token is not None:
            kwargs[Token.ROOT_TAG] = Token._xml_ele_to_obj(token)
        if serviceCatalog is not None:
            kwargs[ServiceCatalog.ROOT_TAG] = \
                ServiceCatalog._xml_ele_to_obj(serviceCatalog)
        if user is not None:
            kwargs[User.ROOT_TAG] = User._xml_ele_to_obj(user)
        return Access(**kwargs)


class Token(BaseIdentityDomain):

    ROOT_TAG = 'token'

    def __init__(self, id=None, expires=None, tenant=None, authenticatedBy=None):
        '''An object that represents an groups response object.
        '''
        super(Token, self).__init__()
        self.id = id
        self.expires = expires
        self.tenant = tenant
        self.authenticatedBy = authenticatedBy

    @classmethod
    def _dict_to_obj(cls, json_dict):
        if Tenant.ROOT_TAG in json_dict:
            json_dict[Tenant.ROOT_TAG] = Tenant(**json_dict[Tenant.ROOT_TAG])
        if 'RAX-AUTH:authenticatedBy' in json_dict:
            json_dict['authenticatedBy'] = \
                    json_dict['RAX-AUTH:authenticatedBy']
            del json_dict['RAX-AUTH:authenticatedBy']
        return Token(**json_dict)

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        kwargs = {'expires': xml_ele.get('expires'),
                  'tenant': xml_ele.get('tenant')}
        try:
            kwargs['id'] = int(xml_ele.get('id'))
        except (ValueError, TypeError):
            kwargs['id'] = xml_ele.get('id')
        tenant = xml_ele.find(Tenant.ROOT_TAG)
        if tenant is not None:
            kwargs[Tenant.ROOT_TAG] = Tenant._xml_ele_to_obj(tenant)
        return Token(**kwargs)


class ServiceCatalog(BaseIdentityDomainList):

    ROOT_TAG = 'serviceCatalog'

    def __init__(self, serviceCatalog=None):
        super(ServiceCatalog, self).__init__()
        self.extend(serviceCatalog)

    def get_service(self, name):
        for Service in self:
            if Service.name == name:
                return Service
        self._log.info('Unable to find service named "%s"' % str(name))
        return None

    @classmethod
    def _list_to_obj(cls, list_):
        ret = {cls.ROOT_TAG: [Service._dict_to_obj(service)
                              for service in list_]}
        return ServiceCatalog(**ret)

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        services = xml_ele.findall(Service.ROOT_TAG)
        ret = {cls.ROOT_TAG: [Service._xml_ele_to_obj(service)
                              for service in services]}
        return ServiceCatalog(**ret)


class Service(BaseIdentityDomain):

    ROOT_TAG = 'service'

    def __init__(self, name=None, endpoints=None, type=None):
        super(Service, self).__init__()
        self.name = name
        self.endpoints = endpoints
        self.type = type

    def get_endpoint(self, region):
        '''Returns the endpoint that matches the provided region,
           or None if such an endpoint is not found
        '''
        for ep in self.endpoints:
            if getattr(ep, 'region'):
                if str(ep.region).lower() == str(region).lower():
                    return ep

        self._log.critical('Unable to find endpoint for region "%s"\
                 in "%s" service' % (str(region), str(self.name)))

    @classmethod
    def _dict_to_obj(cls, dic):
        if Endpoints.ROOT_TAG in dic:
            dic[Endpoints.ROOT_TAG] = \
                Endpoints._list_to_obj(dic[Endpoints.ROOT_TAG])
        return Service(**dic)

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        kwargs = {'name': xml_ele.get('name'), 'type': xml_ele.get('type')}
        endpoints = xml_ele.findall(Endpoint.ROOT_TAG)
        if endpoints is not None:
            kwargs[Endpoints.ROOT_TAG] = Endpoints._xml_list_to_obj(endpoints)
        return Service(**kwargs)


class Impersonation(BaseIdentityDomain):

    ROOT_TAG = 'RAX-AUTH:impersonator'

    def __init__(self, id=None, roles=None, name=None):
        '''
        An object that validates the response of an impersonated token.
        '''
        super(Impersonation, self).__init__()
        self.id = id
        self.roles = roles
        self.name = name

    @classmethod
    def _dict_to_obj(cls, json_dict):
        if Roles.ROOT_TAG in json_dict:
            json_dict[Roles.ROOT_TAG] = Roles.\
                 _list_to_obj(json_dict[Roles.ROOT_TAG])
        return Impersonation(**json_dict)

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        kwargs = {'roles': xml_ele.get('roles'),
                  'name': xml_ele.get('name')}
        try:
            kwargs['id'] = int(xml_ele.get('id'))
        except (ValueError, TypeError):
            kwargs['id'] = xml_ele.get('id')
        roles = xml_ele.find(Roles.ROOT_TAG)
        if roles is not None:
            kwargs[Roles.ROOT_TAG] = Roles._xml_to_obj(roles)
        return Token(**kwargs)

