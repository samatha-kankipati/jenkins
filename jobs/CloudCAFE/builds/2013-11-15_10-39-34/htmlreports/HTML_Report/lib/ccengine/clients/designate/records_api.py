from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.domain.designate.request.record import Record
from ccengine.domain.designate.response.record import Record as RecordResp
from ccengine.domain.designate.response.record import RecordList


class RecordsApiClient(BaseMarshallingClient):

    def __init__(self, url, serialize_format=None, deserialize_format=None):
        super(RecordsApiClient, self).__init__(serialize_format,
                                               deserialize_format)
        self.url = url
        self.default_headers['Content-Type'] = 'application/{0}'.format(
            self.serialize_format)
        self.default_headers['Accept'] = 'application/{0}'.format(
            self.serialize_format)

    def create_record(self, name_list=None, type_list=None, data_list=None,
                      priority_list=None, domain_id=None,
                      requestslib_kwargs=None):
        """
        Create Records
        POST
        v1/domains/{domainID}/records
        """
        request_rec = Record(name=name_list, data=data_list,
                             record_type=type_list, priority=priority_list)
        url = "{0}/domains/{1}/records".format(self.url, domain_id)
        return self.request('POST', url, request_entity=request_rec,
                            response_entity_type=RecordResp,
                            requestslib_kwargs=requestslib_kwargs)

    def list_records(self, domain_id, requestslib_kwargs=None):
        """
        List Records
        GET
        v1/{tenant_id}/domains/{domainID}/records
        """
        url = "{0}/domains/{1}/records".format(self.url, domain_id)

        return self.request('GET', url, response_entity_type=RecordList,
                            requestslib_kwargs=requestslib_kwargs)

    def get_record(self, domain_id, record_id, requestslib_kwargs=None):
        """
        get record details by id
        GET
        v1/{tenant_id}/domains/{domainID}/records/{recordID}
        """
        url = "{0}/domains/{1}/records/{2}".format(self.url, domain_id,
                                                   record_id)
        return self.request('GET', url, response_entity_type=RecordResp,
                            requestslib_kwargs=requestslib_kwargs)

    def update_record(self, domain_id=None, name_list=None, type_list=None,
                      data_list=None, priority_list=None, record_id=None,
                      requestslib_kwargs=None):
        """
        Modify a record in the domain
        GET
        v1/domains/{domainID}/records/{record_id}
        """
        request_rec = Record(name=name_list, data=data_list,
                             record_type=type_list,
                             priority=priority_list)

        url = "{0}/domains/{1}/records/{2}".format(self.url, domain_id,
                                                   record_id)
        return self.request('PUT', url, response_entity_type=RecordResp,
                            request_entity=request_rec,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_record(self, domain_id, record_id, requestslib_kwargs=None):
        """
        Delete a Record
        DELETE
        v1/domains/{domainID}/records/{recordID}
        """
        url = "{0}/domains/{1}/records/{2}".format(self.url, domain_id,
                                                   record_id)
        return self.request('DELETE', url, response_entity_type=RecordResp,
                            requestslib_kwargs=requestslib_kwargs)
