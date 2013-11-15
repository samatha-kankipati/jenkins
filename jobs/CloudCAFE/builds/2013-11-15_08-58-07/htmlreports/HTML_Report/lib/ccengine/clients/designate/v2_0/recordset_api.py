from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.domain.designate.request.recordset import Record
from ccengine.domain.designate.response.recordset import Record as RecordResp
from ccengine.domain.designate.response.recordset import RecordList


class RecordsetClient(BaseMarshallingClient):

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):
        super(RecordsetClient, self).__init__(serialize_format,
                                              deserialize_format)
        self.url = url
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        self.default_headers['Content-Type'] = 'application/{0}'.format(
            self.serialize_format)
        self.default_headers['Accept'] = 'application/{0}'.format(
            self.serialize_format)

    def create_recordset(self, name_list=None,
                         type_list=None, data_list=None,
                         priority_list=None,
                         domain_id=None, requestslib_kwargs=None):
        """
        Create Records
        POST
        v1/domains/{domainID}/recordsetsets
        """
        request_rec = Record(name=name_list, data=data_list,
                             recordset_type=type_list,
                             priority=priority_list)
        url = "{0}/domains/{1}/recordsetsets".format(self.url, domain_id)
        return self.request('POST', url, request_entity=request_rec,
                            response_entity_type=RecordResp,
                            requestslib_kwargs=requestslib_kwargs)

    def list_recordsetsets(self, domain_id, requestslib_kwargs=None):
        """
        List Records
        GET
        v1/{tenant_id}/domains/{domainID}/recordsetsets
        """
        url = "{0}/domains/{1}/recordsetsets".format(self.url, domain_id)
        return self.request('GET', url, response_entity_type=RecordList,
                            requestslib_kwargs=requestslib_kwargs)

    def get_recordset(self, domain_id, recordset_id, requestslib_kwargs=None):
        """
        get recordset details by id
        GET
        v1/{tenant_id}/domains/{domainID}/recordsetsets/{recordsetID}
        """

        url = "{0}/domains/{1}/recordsetsets/{2}".format(self.url, domain_id,
                                                         recordset_id)
        return self.request('GET', url, response_entity_type=RecordResp,
                            requestslib_kwargs=requestslib_kwargs)

    def update_recordset(self, domain_id=None, name_list=None,
                         type_list=None, data_list=None, priority_list=None,
                         recordset_id=None, requestslib_kwargs=None):
        """
        Modify a recordset in the domain
        GET
        v1/domains/{domainID}/recordsetsets/{recordset_id}
        """
        request_rec = Record(name=name_list, data=data_list,
                             recordset_type=type_list, priority=priority_list)
        url = "{0}/domains/{1}/recordsetsets/{2}".format(self.url, domain_id,
                                                         recordset_id)
        return self.request('PUT', url, response_entity_type=RecordResp,
                            request_entity=request_rec,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_recordset(self, domain_id, recordset_id,
                         requestslib_kwargs=None):
        """
        Delete a Record
        DELETE
        v1/domains/{domainID}/recordsetsets/{recordsetID}
        """
        url = "{0}/domains/{1}/recordsetsets/{2}".format(self.url, domain_id,
                                                         recordset_id)
        return self.request('DELETE', url, response_entity_type=RecordResp,
                            requestslib_kwargs=requestslib_kwargs)
