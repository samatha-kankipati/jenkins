from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.domain.dnsaas.request.domain import Domain, ImportDomain
from ccengine.domain.dnsaas.request.record import RecordsList, Record
from ccengine.domain.dnsaas.request.subdomain import SubDomain, SubDomainsList
from ccengine.domain.dnsaas.response.asyncresponse import AsyncResponse
from ccengine.domain.dnsaas.response.domain import Domain as ResponseDomain
from ccengine.domain.dnsaas.response.domainlist import DomainList


class DnsaasAPIClient(BaseMarshallingClient):

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):
        super(DnsaasAPIClient, self).__init__(serialize_format,
                                               deserialize_format)

        self.url = url
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        self.default_headers['Content-Type'] = 'application/{0}'.format(
            self.serialize_format)
        self.default_headers['Accept'] = 'application/{0}'.format(
            self.serialize_format)

    def create_domain(self, name=None, emailAddress=None, ttl=None,
                      comment=None, name_list=None, subname_list=None,
                      type_list=None, data_list=None, recordsList=None,
                      ttl_list=None, comment_list=None, subDomains=None,
                      requestslib_kwargs=None):
        """
        Create Domains(Create a new domain.)
        POST
        v1/{tenant_id}/domains
        """
        if name_list is not None:
            records = []
            for i in range(len(name_list)):
                rec = Record(data=data_list[i], record_type=type_list[i],
                             name=name_list[i])
                if ttl_list is not None:
                    rec.ttl = ttl_list[i]
                records.append(rec)

            recordsList = RecordsList(records=records)
        if name_list is not None:
            subdomains = []
            for i in range(len(subname_list)):
                dom = SubDomain(name=subname_list[i], comment=comment_list[i],
                                ttl=ttl_list[i], emailAddress=emailAddress)
                subdomains.append(dom)

            subDomains = SubDomainsList(subdomains=subdomains)

        domain_req = Domain(name=name, emailAddress=emailAddress, ttl=ttl,
                   comment=comment, subdomains=subDomains,
                   recordsList=recordsList)

        url = "{0}/domains".format(self.url)

        return self.request('POST', url,
                            response_entity_type=AsyncResponse,
                            request_entity=domain_req,
                            requestslib_kwargs=requestslib_kwargs)

    def update_domain(self, pdomain_id=None, emailAddress=None, ttl=None,
                      comment=None, requestslib_kwargs=None):
        """
        Update Domains(Update a domain.)
        PUT
        v1/{tenant_id}/domains
        """

        domain_req = Domain(emailAddress=emailAddress, ttl=ttl,
                   domain_id=pdomain_id, comment=comment)

        url = "{0}/domains".format(self.url)
        return self.request('PUT', url,
                            response_entity_type=AsyncResponse,
                            request_entity=domain_req,
                            requestslib_kwargs=requestslib_kwargs)

    def list_all_domain(self, requestslib_kwargs=None):
        """
        List Domains
        GET
        v1/{tenant_id}/domains
        """
        url = "{0}/domains".format(self.url)

        return self.request('GET', url,
                            response_entity_type=DomainList,
                            requestslib_kwargs=requestslib_kwargs)

    def list_domain_name(self, domain_name, requestslib_kwargs=None):
        """
        List domains by name
        GET
        v1/{tenant_id}/domains/?{domainName}
        """
        url = "{0}/domains/?name={1}".format(self.url, domain_name)
        return self.request('GET', url,
                            response_entity_type=ResponseDomain,
                            requestslib_kwargs=requestslib_kwargs)

    def list_domain_id(self, domain_id, requestslib_kwargs=None):
        """
        list domain details by id
        GET
        v1/{tenant_id}/domains/{domainID}
        """
        url = "{0}/domains/{1}".format(self.url, domain_id)

        return self.request('GET', url,
                            requestslib_kwargs=requestslib_kwargs)

    def list_domain_details(self, domain_id, requestslib_kwargs=None):
        """
        list domain details with SubDomains and Records
        GET
        v1/{tenant_id}/domains/{domainID}?showRecords=true&showSubdomains=true?
        """

        url = "{0}/domains/{1}?showRecords=true&showSubdomains=true?"\
                    .format(self.url, domain_id)
        return self.request('GET', url,
                            requestslib_kwargs=requestslib_kwargs)

    def list_domain_time(self, domain_id, timechange, requestslib_kwargs=None):
        """
        List Domain Changes by time
        GET
        v1/{tenant_id}/domains/{domainID}/changes?since={time}
        """
        url = "{0}/domains/{1}/changes?since={2}".format(
                                                         self.url,
                                                         domain_id,
                                                         timechange)

        return self.request('GET', url,
                            requestslib_kwargs=requestslib_kwargs)

    def clone_domain(self, domain_id, clone_name,
                     cloneSubdomain=None,
                     modifyRecordsData=None,
                     modifyEmailAddress=None,
                     modifyComment=None,
                     requestlib_kwargs=None):
        """
        Clone an already existing domain
        POST
        v1/{tenant_id}/domains/{domainID}/clone?cloneName={name}"
        """

        url = "{0}/domains/{1}/clone?cloneName={2}".format(self.url,
                                                           domain_id,
                                                           clone_name)
        if cloneSubdomain is not None:
            url = "{0}/domains/{1}/clone?cloneName={2}&cloneSubdomains={3}"\
                .format(self.url, domain_id, clone_name, cloneSubdomain)

        if modifyRecordsData is not None:
            url = "{0}&modifyRecordData={1}".format(self.url,
                                                    modifyRecordsData)

        elif modifyEmailAddress is not None:
            url = "{0}&modifyEmailAddress={1}".format(self.url,
                                                      modifyEmailAddress)

        elif modifyComment is not None:
            url = "{0}&modifyComment={1}".format(self.url, modifyComment)
        return self.request('POST', url,
                            response_entity_type=AsyncResponse,
                            requestslib_kwargs=requestlib_kwargs)

    def export_domain(self, domain_id, requestslib_kwargs=None):
        """
        Export an already existing domain
        GET
        v1/{tenant_id}/domains/{domainID}/export
        """

        url = "{0}/domains/{1}/export".format(self.url, domain_id)
        return self.request('GET', url,
                            response_entity_type=AsyncResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def import_domain(self, import_name, requestslib_kwargs=None):
        """
        Import domain
        POST
        v1/{tenant_id}/domains/import"
        """
        url = "{0}/domains/import".format(self.url)
        d = ImportDomain(import_name=import_name)

        return self.request('POST', url,
                            request_entity=d,
                            response_entity_type=AsyncResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_domain(self, domain_id, requestslib_kwargs=None):
        """
        Delete domain
        DELETE
        v1/{tenant_id}/domains/{domainID}"
        """
        url = "{0}/domains/{1}".format(self.url, domain_id)
        return self.request('DELETE', url,
                            response_entity_type=AsyncResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def call_backUrl(self, callbackUrl, requestslib_kwargs=None):
        """
        callbackURL after async. response
        GET
        {callbackURl}/?showDetails=true
        """
        url = "{0}/?showDetails=true".format(callbackUrl)
        return self.request('GET', url,
                            response_entity_type=AsyncResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def list_all_limits(self, requestslib_kwargs=None):
        """
        list limits
        GET
        v1/{tenant_id}/limits
        """
        url = "{0}/limits".format(self.url)
        return self.request('GET', url,
                            requestslib_kwargs=requestslib_kwargs)

    def list_limits_types(self, requestslib_kwargs=None):
        """
        list limits types
        GET
        v1/{tenant_id}/limits/types
        """
        url = "{0}/limits/types".format(self.url)
        return self.request('GET', url,
                            requestslib_kwargs=requestslib_kwargs)

    def list_limits_rate_limit(self, requestslib_kwargs=None):
        """
        list rate_limit
        GET
        v1/{tenant_id}/limits/rate_limit
        """
        url = "{0}/limits/rate_limit".format(self.url)
        return self.request('GET', url,
                            requestslib_kwargs=requestslib_kwargs)

    def list_domain_limit(self, requestslib_kwargs=None):
        """
        list Limits domain_limit
        GET
        v1/{tenant_id}/limits/domain_limit
        """
        url = "{0}/limits/domain_limit".format(self.url)

        return self.request('GET', url,
                            requestslib_kwargs=requestslib_kwargs)

    def list_domain_record_limits(self, requestslib_kwargs=None):
        """
        list domain_record_limit
        GET
        v1/{tenant_id}/limits/domain_record_limit
        """
        url = "{0}/limits/domain_record_limit".format(self.url)
        return self.request('GET', url,
                            requestslib_kwargs=requestslib_kwargs)
