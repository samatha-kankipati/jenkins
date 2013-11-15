from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.domain.isl.response.incident import Incident
from ccengine.domain.isl.request.incident_request import CreateIncident
from ccengine.common.tools.datagen import rand_name
from urlparse import urlparse


class IncidentAPIClient(BaseMarshallingClient):
    
    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):
        '''
        @param logger: PBLogger instance to use,
         Generates private logger if None
        @type logger: L{PBLogger}
        '''
        super(IncidentAPIClient, self).__init__(serialize_format,
                                                deserialize_format)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        ct = ''.join(['application/', self.serialize_format])
        accept = ''.join(['application/', self.deserialize_format])
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.url = url

    def list_incidents(self):
        '''
             Write proper comments
        '''
        url = '%s/incidents' % (self.url)
        incident_response = self.request('GET', url,
                                         response_entity_type=Incident)
        return incident_response

    def create_incidents(self, subject, description, 
                         email, category, comment=[], 
                         requestslib_kwargs=None):
        '''
             Write proper comments
        '''
        incident_request_object = CreateIncident(subject=subject,
                                                 description=description,
                                                 email_cc=email,
                                                 category=category,
                                                 comment=comment)

        url = '%s/incidents' % (self.url)
        server_response = self.request('POST', url,
                                       response_entity_type=Incident,
                                       request_entity=incident_request_object,
                                       requestslib_kwargs=requestslib_kwargs)
        return server_response
