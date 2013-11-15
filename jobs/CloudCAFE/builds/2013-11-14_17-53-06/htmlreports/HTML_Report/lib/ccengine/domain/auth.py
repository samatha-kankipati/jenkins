from ccengine.domain.base_domain import BaseDomain
import pprint


class Auth_1_1(BaseDomain):
    def __init__(self, response_dict):
        super(Auth_1_1, self).__init__()
        self.response = response_dict
        _auth = self.response.get('auth')
        self.token = self.Token(_auth.get('token'))
        self.service_catalog = []
        for s_name, s_endpoints in enumerate(_auth.get('serviceCatalog')):
            self.service_catalog.append(self.Service(s_name, s_endpoints))

    def get_service(self, name):
        for s in self.service_catalog:
            if getattr(s, 'name'):
                if str(s.name).lower() == str(name).lower():
                    return s
        return None

    def print_auth_response(self):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.response)

    def __repr__(self):
        s = ''
        s = s + 'token: %s' % str(self.token)
        s = s + 'ServiceCatalog\n'
        for sobj in self.service_catalog:
            s = s + 'service\n'
            s = s + '%s\n' % str(sobj)
        return s

    class Token(object):
        def __init__(self, token_dict):
            self.id = token_dict.get('id')
            self.expires = token_dict.get('expires')

        def __repr__(self):
            s = ''
            s = s + 'id: %s' % str(self.id)
            s = s + 'expires: %s' % str(self.expires)
            return s

    class Service(object):
        def __init__(self, name, endpoints):
            self.name = name
            self.endpoints = []
            for ep in endpoints:
                self.endpoints.append(self.Endpoint(ep))

        @property
        def endpoint(self, region=None):
            '''Returns the endpoint if there's only one.'''
            if region == None:
                return self.endpoints[0]
            else:
                for ep in self.endpoints:
                    if getattr(ep, 'region'):
                        if str(ep.region).lower() == str(region).lower():
                            return ep
                return None

        '''TODO: Deprecate this,. it's been replaced by endpoint()'''
        def get_endpoint_by_region(self, region):
            for ep in self.endpoints:
                if getattr(ep, 'region'):
                    if str(ep.region).lower() == str(region).lower():
                        return ep
            return None

        def __repr__(self):
            s = ''
            s = s + 'name: %s' % str(self.name)
            s = s + 'Endpoints\n'
            for epobj in self.endpoints:
                s = s + 'Endpoint\n'
                s = s + '%s\n' % str(epobj)
            return s

        class Endpoint(object):
            def __init__(self, endpoint_dict):
                self.region = endpoint_dict.get('region')
                self.v1Default = endpoint_dict.get('v1Default')
                self.publicURL = endpoint_dict.get('publicURL')
                self.internalURL = endpoint_dict.get('internalURL')

            def __repr__(self):
                s = ''
                s = s + 'region: %s' % str(self.region)
                s = s + 'v1Default: %s' % str(self.v1Default)
                s = s + 'publicURL: %s' % str(self.publicURL)
                s = s + 'internalURL: %s' % str(self.internalURL)
                return s


class Auth_2_0(BaseDomain):
    '''Domain Object representation of the data returned from a successful
       RAX Auth 2.0 request. (Global Auth)
       @TODO: Only supports json responses
    '''

    def __init__(self, ResponseDict):
        super(Auth_2_0, self).__init__()
        self.response = ResponseDict
        self.service_catalog = []
        self.token = Token_2_0(ResponseDict.get('access').get('token'))
        self.user = User_2_0((ResponseDict.get('access').get('user')))

        for ServiceDict in ResponseDict.get('access').get('serviceCatalog'):
            self.service_catalog.append(Service_2_0(ServiceDict))

    def print_auth_response(self):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.response)

    def get_service(self, name):
        for s in self.service_catalog:
            if getattr(s, 'name'):
                if str(s.name).lower() == str(name).lower():
                    return s
        self._log.critical('Service "%s" not found in service catalog' % str(name))
        return None


class Token_2_0(BaseDomain):
    def __init__(self, TokenDict):
        super(Token_2_0, self).__init__()
        self.expires = TokenDict.get('expires')
        self.id = TokenDict.get('id')


class User_2_0(BaseDomain):
    def __init__(self, UserDict):
        super(User_2_0, self).__init__()
        self.id = UserDict.get('id')
        self.name = UserDict.get('name')
        self.roles = []
        for RoleDict in UserDict.get('roles'):
            self.roles.append(Role_2_0(RoleDict))

    @property
    def role(self):
        '''Returns the endpoint if there's only one.'''
        return self.roles[0]


class Role_2_0(BaseDomain):
    def __init__(self, RoleDict):
        super(Role_2_0, self).__init__()
        self.id = RoleDict.get('id')
        self.description = RoleDict.get('description')
        self.name = RoleDict.get('name')


class Service_2_0(BaseDomain):
    def __init__(self, ServiceDict):
        super(Service_2_0, self).__init__()
        self.endpoints = []
        self.name = ServiceDict.get('name')
        self.type = ServiceDict.get('type')
        for EndpointDict in ServiceDict.get('endpoints'):
            self.endpoints.append(Endpoint_2_0(EndpointDict))

    @property
    def endpoint(self, region=None):
        '''Returns the endpoint if there's only one, or the specific
           endpoint if a region is provided
        '''
        if region == None:
            return self.endpoints[0]
        else:
            for e in self.endpoints:
                if getattr(e, 'region'):
                    if str(e.region).lower() == str(region).lower():
                        return e

            self._log.critical('Unable to find endpoint for region "%s"\
                     in "%s" service' % (str(region), str(self.name)))
            return None

    '''@TODO: This function is no longer neccessary, now that endpoint
              returns by region as well'''
    def get_endpoint_by_region(self, region):
        for e in self.endpoints:
            if getattr(e, 'region'):
                if str(e.region).lower() == str(region).lower():
                    return e

        self._log.critical('Unable to find endpoint for region "%s"\
                                 in "%s" service' % (str(region), str(self.name)))
        return None


class Endpoint_2_0(BaseDomain):
    def __init__(self, EndpointDict):
        super(Endpoint_2_0, self).__init__()
        self.publicURL = EndpointDict.get('publicURL', None)
        self.tenantId = EndpointDict.get('tenantId', None)
        self.versionId = EndpointDict.get('versionId', None)
        self.versionInfo = EndpointDict.get('versionInfo', None)
        self.versionList = EndpointDict.get('versionList', None)
        self.region = EndpointDict.get('region', None)
        self.internalURL = EndpointDict.get('internalURL', None)
