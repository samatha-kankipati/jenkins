from xml.etree import ElementTree
import json
from ccengine.domain.base_domain \
    import BaseMarshallingDomain, BaseMarshallingDomainList
from ccengine.common.constants.identity import V1_1Constants


class Auth(BaseMarshallingDomain):

    ROOT_TAG = 'auth'

    def __init__(self, token=None, serviceCatalog=None):
        super(Auth, self).__init__()
        self.token = token
        self.serviceCatalog = serviceCatalog

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = json.loads(serialized_str)
        return cls._dict_to_obj(ret.get(cls.ROOT_TAG))

    @classmethod
    def _dict_to_obj(cls, dic):
        if Token.ROOT_TAG in dic:
            dic[Token.ROOT_TAG] = Token(**dic.get(Token.ROOT_TAG))
        if ServiceCatalog.ROOT_TAG in dic:
            dic[ServiceCatalog.ROOT_TAG] = ServiceCatalog.\
                _dict_to_obj(dic.get(ServiceCatalog.ROOT_TAG))
        return Auth(**dic)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_namespace(element, V1_1Constants.XML_NS)
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        kwargs = {}
        token = xml_ele.find(Token.ROOT_TAG)
        service_catalog = xml_ele.find(ServiceCatalog.ROOT_TAG)
        if token is not None:
            kwargs['token'] = Token._xml_ele_to_obj(token)
        if service_catalog is not None:
            kwargs['serviceCatalog'] = ServiceCatalog._xml_ele_to_obj(
                    service_catalog)
        return Auth(**kwargs)


class Token(BaseMarshallingDomain):

    ROOT_TAG = 'token'

    def __init__(self, id=None, expires=None):
        super(Token, self).__init__()
        self.id = id
        self.expires = expires

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        kwargs = {'id': xml_ele.get('id'), 'expires': xml_ele.get('expires')}
        return Token(**kwargs)


class ServiceCatalog(BaseMarshallingDomainList):

    ROOT_TAG = 'serviceCatalog'

    def __init__(self, serviceCatalog=None):
        super(ServiceCatalog, self).__init__()
        for service in serviceCatalog:
            self.append(service)

    def get(self, service_name):
        for service in self:
            if service.name == service_name:
                return service

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = json.loads(serialized_str)
        ret = cls._dict_to_obj(ret.get(cls.ROOT_TAG))
        return ret

    @classmethod
    def _dict_to_obj(cls, dic):
        ret = {cls.ROOT_TAG: [Service._dict_to_obj(service_name=service,
                                                   endpoints=dic.get(service))
                              for service in dic]}
        return ServiceCatalog(**ret)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_namespace(element, V1_1Constants.XML_NS)
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        kwargs = {}
        xml_services = xml_ele.findall(Service.ROOT_TAG)
        services = [Service._xml_ele_to_obj(xml_service)
                    for xml_service in xml_services]
        kwargs[cls.ROOT_TAG] = services
        return ServiceCatalog(**kwargs)


class Service(BaseMarshallingDomain):

    ROOT_TAG = 'service'

    def __init__(self, name=None, endpoints=None):
        super(Service, self).__init__()
        self.name = name
        self.endpoints = endpoints

    @classmethod
    def _dict_to_obj(cls, service_name, endpoints):
        endpoints = EndpointList._list_to_obj(endpoints)
        kwargs = {'name': service_name, 'endpoints': endpoints}
        return Service(**kwargs)

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        kwargs = {'name': xml_ele.get('name')}
        xml_endpoints = xml_ele.findall(Endpoint.ROOT_TAG)
        kwargs['endpoints'] = EndpointList._xml_ele_to_obj(xml_endpoints)
        return Service(**kwargs)


class EndpointList(BaseMarshallingDomainList):

    ROOT_TAG = 'endpoints'

    def __init__(self, endpoints=None):
        super(EndpointList, self).__init__()
        for ep in endpoints:
            self.append(ep)

    @classmethod
    def _list_to_obj(cls, list_):
        kwargs = {cls.ROOT_TAG: [Endpoint(**ep) for ep in list_]}
        return EndpointList(**kwargs)

    @classmethod
    def _xml_ele_to_obj(cls, list_):
        endpoints = [Endpoint._xml_ele_to_obj(xml_endpoint)
                     for xml_endpoint in list_]
        kwargs = {cls.ROOT_TAG: endpoints}
        return EndpointList(**kwargs)


class Endpoint(BaseMarshallingDomain):

    ROOT_TAG = 'endpoint'

    def __init__(self, region=None, v1Default=None, publicURL=None,
                 internalURL=None):
        super(Endpoint, self).__init__()
        self.region = region
        self.v1Default = v1Default
        self.publicURL = publicURL
        self.internalURL = internalURL

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        kwargs = {'region': xml_ele.get('region'),
                  'publicURL': xml_ele.get('publicURL'),
                  'internalURL': xml_ele.get('internalURL')}
        if xml_ele.get('v1Default') is not None:
            kwargs['v1Default'] = json.loads(xml_ele.get('v1Default').lower())
        return Endpoint(**kwargs)
