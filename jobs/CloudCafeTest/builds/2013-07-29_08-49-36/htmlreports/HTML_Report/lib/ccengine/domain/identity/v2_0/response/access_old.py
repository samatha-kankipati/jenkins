from ccengine.domain.base_domain import BaseMarshallingDomain, BaseDomain
import json


class Access(BaseMarshallingDomain):
    '''Domain Object representation of the data returned from a successful
       RAX Auth 2.0 request. (Global Auth)
       @TODO: Only supports json responses
    '''

    def __init__(self, ResponseDict):
        super(Access, self).__init__()
        AccessDict = ResponseDict.get('access')
        self.serviceCatalog = ServiceCatalog(AccessDict.get('serviceCatalog'))
        self.token = Token(AccessDict.get('token'))
        self.user = User((AccessDict.get('user')))

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return Access(json_dict)


class ServiceCatalog(list):
    '''special implementation of list that converts a service catalog
       dictionary into a list, and adds a service convenience function
       for accessing a service by name
    '''
    def __init__(self, ServiceCatalogDict):
        super(ServiceCatalog, self).__init__()

        for ServiceDict in ServiceCatalogDict:
            self.append(Service(ServiceDict))

    def get_service(self, name):
        self._log = BaseMarshallingDomain._log
        for Service in self:
            if Service.name == name:
                return Service
        self._log.info('Unable to find service named "%s"' % str(name))
        return None


class Service(BaseDomain):
    def __init__(self, ServiceDict):
        super(Service, self).__init__()
        self.endpoints = []
        self.name = ServiceDict.get('name')
        self.type = ServiceDict.get('type')
        for EndpointDict in ServiceDict.get('endpoints'):
            self.endpoints.append(Endpoint(EndpointDict))

    def get_endpoint(self, region):
        '''Returns the endpoint that matches the provided region,
           or None if such an endpoint is not found
        '''

        for e in self.endpoints:
            if getattr(e, 'region'):
                if str(e.region).lower() == str(region).lower():
                    return e

        self._log.critical('Unable to find endpoint for region "%s"\
                 in "%s" service' % (str(region), str(self.name)))
        return None


class Token(BaseDomain):
    def __init__(self, TokenDict):
        super(Token, self).__init__()
        self.expires = TokenDict.get('expires')
        self.id = TokenDict.get('id')


class User(BaseDomain):
    def __init__(self, UserDict):
        super(User, self).__init__()
        self.id = UserDict.get('id')
        self.name = UserDict.get('name')
        self.roles = []
        for RoleDict in UserDict.get('roles'):
            self.roles.append(Role(RoleDict))

    def get_role(self, id=None, name=None):
        '''Returns the role object if it matches all provided criteria'''

        for role in self.roles:
            if id and not name:
                if role.id == id:
                    return role

            if name and not id:
                if role.name == name:
                    return role

            if name and id:
                if (role.name == name) and (role.id == id):
                    return role


class Role(BaseDomain):
    def __init__(self, RoleDict):
        super(Role, self).__init__()
        self.id = RoleDict.get('id')
        self.description = RoleDict.get('description')
        self.name = RoleDict.get('name')


class Endpoint(BaseDomain):
    def __init__(self, EndpointDict):
        super(Endpoint, self).__init__()
        if EndpointDict.get('publicURL', None):
            self.publicURL = EndpointDict.get('publicURL', None)

        if EndpointDict.get('tenantId', None):
            self.tenantId = EndpointDict.get('tenantId', None)

        if EndpointDict.get('versionId', None):
            self.versionId = EndpointDict.get('versionId', None)

        if EndpointDict.get('versionInfo', None):
            self.versionInfo = EndpointDict.get('versionInfo', None)

        if EndpointDict.get('versionList', None):
            self.versionList = EndpointDict.get('versionList', None)

        if EndpointDict.get('region', None):
            self.region = EndpointDict.get('region', None)

        if EndpointDict.get('internalURL', None):
            self.internalURL = EndpointDict.get('internalURL', None)
