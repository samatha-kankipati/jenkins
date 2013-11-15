from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.domain.dnsaas.request.record import RecordsList, Record
from ccengine.domain.dnsaas.response.asyncresponse import AsyncResponse
from ccengine.domain.dnsaas.response.record import Record as ResponseRecord
import ccengine.common.connectors.rest as rest


class RecordsAPIClient(BaseMarshallingClient):

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):
        super(RecordsAPIClient, self).__init__(serialize_format,
                                               deserialize_format)

        self.url = url
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        self.default_headers['Content-Type'] = 'application/{0}'.format(
            self.serialize_format)
        self.default_headers['Accept'] = 'application/{0}'.format(
            self.serialize_format)

    def create_record(self, name_list=None, type_list=None, data_list=None,
                      ttl_list=None, priority_list=None, comment_list=None,
                      domain_id=None, requestslib_kwargs=None):
        """
        Create Records
        POST
        v1/{tenant_id}/domains/{domainID}/records
        """
        request_rec = None
        if name_list is not None:
                records = []
                for i in range(len(name_list)):
                    rec = Record(data=data_list[i], record_type=type_list[i],
                                 name=name_list[i])
                    if ttl_list is not None:
                        rec.ttl = ttl_list[i]
                    if comment_list is not None:
                        rec.comment = comment_list[i]
                    if priority_list is not None:
                        rec.priority = priority_list[i]
                    records.append(rec)

                request_rec = RecordsList(records=records)
        url = "{0}/domains/{1}/records".format(self.url, domain_id)

        return self.request('POST', url, request_entity=request_rec,
                            response_entity_type=AsyncResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def list_records(self, domain_id, requestslib_kwargs=None):
        """
        List Records
        GET
        v1/{tenant_id}/domains/{domainID}/records
        """
        url = "{0}/domains/{1}/records".format(self.url, domain_id)

        return self.request('GET', url,
                            response_entity_type=ResponseRecord,
                            requestslib_kwargs=requestslib_kwargs)

    def list_records_id(self, domain_id, record_id, requestslib_kwargs=None):
        """
        list record details by id
        GET
        v1/{tenant_id}/domains/{domainID}/records/{recordID}
        """

        url = "{0}/domains/{1}/records/{2}".format(self.url,
                                                   domain_id,
                                                   record_id)

        return self.request('GET', url,
                            response_entity_type=ResponseRecord,
                            requestslib_kwargs=requestslib_kwargs)

    def update_record_id(self, domain_id=None, name_list=None, data_list=None,
                         priority_list=None, id_list=None, ttl_list=None,
                         comment_list=None, requestslib_kwargs=None):
        """
        Modify a record in the domain
        GET
        v1/{tenant_id}/domains/{domainID}/records
        """
        if name_list is not None:

                for i in range(len(name_list)):
                    records = []
                    if id_list is not None:
                        rec = Record(record_id=id_list[i])
                    if ttl_list is not None:
                        rec.ttl = ttl_list[i]
                    records.append(rec)
                    if comment_list is not None:
                        rec.comment = comment_list[i]
                    records.append(rec)
                    if priority_list is not None:
                        rec.priority = priority_list[i]
                    records.append(rec)
                    r = RecordsList(records=records)

                    url = "{0}/domains/{1}/records".format(self.url, domain_id)
                    return self.request('PUT', url,
                                        response_entity_type=AsyncResponse,
                                        request_entity=r,
                                        requestslib_kwargs=requestslib_kwargs)

    def call_backUrl(self, callbackUrl, requestslib_kwargs=None):
        """
        callbackURL after async. response
        GET
        {callbackURl}/?showDetails=true
        """
        url = '%s/?showDetails=true' % (callbackUrl)
        return self.request('GET', url, response_entity_type=AsyncResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_records_id(self, domain_id, record_id, requestslib_kwargs=None):
        """
        Delete a Record
        DELETE
        v1/{tenant_id}/domains/{domainID}/records/{recordID}
        """

        url = "{0}/domains/{1}/records/{2}".format(self.url,
                                                   domain_id,
                                                   record_id)
        return self.request('DELETE', url,
                            response_entity_type=AsyncResponse,
                            requestslib_kwargs=requestslib_kwargs)
