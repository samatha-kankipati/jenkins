from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.domain.dnsaas.response.asyncresponse import AsyncResponse
from ccengine.domain.dnsaas.request.rdns import RDNS as RequestRDNS
from ccengine.domain.dnsaas.request.record import Record as RequestRecord
from ccengine.domain.dnsaas.request.record import RecordsList, Link
from ccengine.domain.dnsaas.response.record import Record as ResponseRecord


class PtrAPIClient(BaseMarshallingClient):
        def __init__(self, url, rel, href, auth_token, serialize_format=None,
                     deserialize_format=None):
            super(PtrAPIClient, self).__init__(serialize_format,
                                                   deserialize_format)

            self.url = url
            self.rel = rel
            self.href = href
            self.auth_token = auth_token
            self.default_headers['X-Auth-Token'] = auth_token
            self.default_headers['Content-Type'] = 'application/{0}'.\
                format(self.serialize_format)
            self.default_headers['Accept'] = 'application/{0}'.\
                format(self.deserialize_format)

        def delete_ptr(self, requestslib_kwargs=None):
            """
            delete ptr records PTR  Records lbaas and nova
            DELETE
            v1/rdns/{service}/{ptrID}?href={serviceUrl}
            """

            url = "{0}/rdns/{1}?href={2}".format(self.url,
                                                 self.rel,
                                                 self.href)

            return self.request('DELETE', url,
                                requestslib_kwargs=requestslib_kwargs)

        def list_ptr(self, requestslib_kwargs=None):
            """
            list Ptr_recordsPTR  Records lbaas and nova
            GET
            v1/rdns/{service}/{ptrID}?href={serviceUrl}/
                {ServiceID for LB or Nova}
            """
            url = "{0}/rdns/{1}?href={2}".format(self.url,
                                                 self.rel,
                                                 self.href)

            return self.request('GET', url,
                                response_entity_type=ResponseRecord,
                                requestslib_kwargs=requestslib_kwargs)

        def create_ptr(self, name_list=None, type_list=None, data_list=None,
                       ttl_list=None, link=None, requestslib_kwargs=None):
            """
            create Ptr_recordsPTR  Records lbaas and nova
            POST
            v1/rdns
            """
            link = Link(href=link['href'], rel=link['rel'])
            records = []
            for i in range(len(name_list)):
                rec = RequestRecord(name=name_list[i], record_type=type_list[i],
                                    data=data_list[i])
                if ttl_list is not None:
                    rec.ttl = ttl_list[i]
                records.append(rec)

            recordsList = RecordsList(records=records)

            r = RequestRDNS(recordsList=recordsList, link=link)
            url = "{0}/rdns".format(self.url)

            return self.request('POST', url,
                                response_entity_type=AsyncResponse,
                                request_entity=r,
                                requestslib_kwargs=requestslib_kwargs)

        def update_ptr(self, name_list=None, type_list=None, data_list=None,
                       id_list=None, ttl_list=None, link=None,
                       requestslib_kwargs=None):
            """
            update Ptr_recordsPTR  Records lbaas and nova
            PUT
            v1/rdns
            """
            link = Link(href=link['href'], rel=link['rel'])
            records = []
            for i in range(len(name_list)):
                rec = RequestRecord(name=name_list[i],
                                    record_type=type_list[i],
                                    record_id=id_list[i],
                                    data=data_list[i])
                if ttl_list is not None:
                    rec.ttl = ttl_list[i]
                records.append(rec)
            recordsList = RecordsList(records=records)
            r = RequestRDNS(recordsList=recordsList, link=link)

            url = "{0}/rdns".format(self.url)

            return self.request('PUT', url,
                                response_entity_type=AsyncResponse,
                                request_entity=r,
                                requestslib_kwargs=requestslib_kwargs)

        def list_ptr_info(self, ptr_id, requestslib_kwargs=None):
            """
            PTR  Records info lbaas and nova
            GET
            v1/rdns/{service}/{ptrID}?href={serviceUrls}
            """

            url = "{0}/rdns/{1}/{2}?href={3}".format(self.url,
                                                     self.rel,
                                                     ptr_id,
                                                     self.href)

            return self.request('GET', url,
                                response_entity_type=ResponseRecord,
                                requestslib_kwargs=requestslib_kwargs)

        def delete_ptr_ip(self, data, requestslib_kwargs=None):
            """
            delete ptr record individual PTR  Records lbaas and nova
            DELETE
            v1/rdns/{service}/{ptrID}?href={serviceUrl}/
                {ServiceID for LB or Nova}/IPaddress
            """
            url = "{0}/rdns/{1}?href={2}&ip={3}".format(self.url,
                                                        self.rel,
                                                        self.href,
                                                        data)

            return self.request('DELETE', url,
                                response_entity_type=AsyncResponse,
                                requestslib_kwargs=requestslib_kwargs)

        def delete_ptr_lb(self, rel_id, requestslib_kwargs=None):
            """
            delete ptr records PTR  Records lbaas and nova
            DELETE
            v1/rdns/{service}/{ptrID}?href={serviceUrl}/
                {ServiceID for LB or Nova}
            """
            url = "{0}/rdns/{1}?href={2}/{3}".format(self.url,
                                                     self.rel,
                                                     self.href,
                                                     rel_id)
            return self.request('DELETE', url,
                                response_entity_type=AsyncResponse,
                                requestslib_kwargs=requestslib_kwargs)

        def list_ptr_lb(self, rel_id, requestslib_kwargs=None):
            """
            PTR  Records info lbaas and nova
            GET
            v1/rdns/{service}/{ptrID}?href={serviceUrl}/
                {ServiceID for LB or Nova}
            """

            url = "{0}/rdns/{1}?href={2}/{3}".format(self.url,
                                                     self.rel,
                                                     self.href,
                                                     rel_id)
            return self.request('GET', url,
                                response_entity_type=ResponseRecord,
                                requestslib_kwargs=requestslib_kwargs)

        def delete_ptr_ip_lb(self, rel_id, data, requestslib_kwargs=None):
            """
            delete ptr record individual PTR  Records lbaas and nova
            DELETE
            v1/rdns/{service}/{ptrID}?href={serviceUrl}/
                {ServiceID for LB or Nova}/IPaddress
            """

            url = "{0}/rdns/{1}?href={2}/{3}&ip={4}".format(self.url,
                                                            self.rel,
                                                            self.href,
                                                            rel_id,
                                                            data)

            return self.request('DELETE', url,
                                response_entity_type=AsyncResponse,
                                requestslib_kwargs=requestslib_kwargs)

        def list_ptr_info_lb(self, rel_id, ptr_id, requestslib_kwargs=None):
            """
            PTR  Records info lbaas and nova
            GET
            v1/rdns/{service}/{ptrID}?href={serviceUrl}/
                {ServiceID for LB or Nova}
            """

            url = "{0}/rdns/{1}/{2}?href={3}/{4}".format(self.url,
                                                         self.rel,
                                                         ptr_id,
                                                         self.href,
                                                         rel_id)

            return self.request('GET', url,
                                response_entity_type=ResponseRecord,
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
