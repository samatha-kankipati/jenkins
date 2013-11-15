from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.domain.designate.request.domain import Domain
from ccengine.domain.designate.response.domain_resp import Domain as RespDomain
from ccengine.domain.designate.response.domain import Domain as DomainList
from ccengine.domain.designate.response.server import ServerList


class DomainsApiClient(BaseMarshallingClient):

    def __init__(self, url, serialize_format=None, deserialize_format=None):
        super(DomainsApiClient, self).__init__(serialize_format,
                                               deserialize_format)
        self.url = url
        self.default_headers['Content-Type'] = 'application/{0}'.format(
            self.serialize_format)
        self.default_headers['Accept'] = 'application/{0}'.format(
            self.serialize_format)

    def create_domain(self, name=None, email=None,
                      ttl=None, requestslib_kwargs=None):
        """
        Create Domain(Create a new domain.)
        POST
        v1/domains
        """
        domain_req = Domain(name=name, email=email, ttl=ttl)
        url = "{0}/domains".format(self.url)
        return self.request('POST', url, response_entity_type=RespDomain,
                            request_entity=domain_req,
                            requestslib_kwargs=requestslib_kwargs)

    def update_domain(self, name=None, domain_id=None,
                      email=None, ttl=None, requestslib_kwargs=None):
        """
        Update Domains(Update a domain.)
        PUT
        v1/domains
        """
        domain_req = Domain(name=name, email=email, ttl=ttl)
        url = "{0}/domains/{1}".format(self.url, domain_id)
        return self.request('PUT', url, response_entity_type=RespDomain,
                            request_entity=domain_req,
                            requestslib_kwargs=requestslib_kwargs)

    def get_domain(self, domain_id, requestslib_kwargs=None):
        """
        list domain details by id
        GET
        v1/domains/{domainID}
        """
        url = "{0}/domains/{1}".format(self.url, domain_id)
        return self.request('GET', url, response_entity_type=RespDomain,
                            requestslib_kwargs=requestslib_kwargs)

    def list_domains(self, requestslib_kwargs=None):
        """
        List Domains
        GET
        v1/domains
        """
        url = "{0}/domains".format(self.url)
        return self.request('GET', url, response_entity_type=DomainList,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_domain(self, domain_id, requestslib_kwargs=None):
        """
        list domain details by id
        DELETE
        v1/domains/{domainID}
        """
        url = "{0}/domains/{1}".format(self.url, domain_id)
        return self.request('DELETE', url, response_entity_type=RespDomain,
                            requestslib_kwargs=requestslib_kwargs)

    def list_domain_servers(self, domain_id, requestslib_kwargs=None):
        """
        Lists the nameservers hosting a particular domain
        GET
        v1/domains/{domainID}/servers
        """
        url = "{0}/domains/{1}/servers".format(self.url, domain_id)
        return self.request('GET', url, response_entity_type=ServerList,
                            requestslib_kwargs=requestslib_kwargs)
