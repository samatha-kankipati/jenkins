from ccengine.clients.base_client import BaseMarshallingClient


class CheckmateAPIClient(BaseMarshallingClient):

    def __init__(self, url, auth_token, tenant_id, serialize_format=None,
                 deserialize_format=None):
        super(CheckmateAPIClient, self).__init__(serialize_format,
                                               deserialize_format)
        self.url = url
        self.tenant_id = tenant_id
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        self.default_headers['Content-Type'] = 'application/%s' % \
                                               self.serialize_format
        self.default_headers['Accept'] = 'application/%s' % \
                                         self.deserialize_format

    def get_providers(self, requestslib_kwargs=None):

        url = '%s/%s/providers' % (self.url, self.tenant_id)

        return self.request('GET', url,
                                  requestslib_kwargs=requestslib_kwargs)

    def get_components(self, requestslib_kwargs=None):

        url = '%s/%s/components' % (self.url, self.tenant_id)

        return self.request('GET', url,
                                  requestslib_kwargs=requestslib_kwargs)

    def get_blueprints(self, requestslib_kwargs=None):

        url = '%s/%s/blueprints' % (self.url, self.tenant_id)

        return self.request('GET', url,
                                  requestslib_kwargs=requestslib_kwargs)

    def get_environments(self, requestslib_kwargs=None):

        url = '%s/%s/environments' % (self.url, self.tenant_id)

        return self.request('GET', url,
                                  requestslib_kwargs=requestslib_kwargs)

    def get_deployments(self, requestslib_kwargs=None):

        url = '%s/%s/deployments' % (self.url, self.tenant_id)

        return self.request('GET', url,
                                  requestslib_kwargs=requestslib_kwargs)

    def get_workflows(self, requestslib_kwargs=None):

        url = '%s/%s/workflows' % (self.url, self.tenant_id)

        return self.request('GET', url,
                                  requestslib_kwargs=requestslib_kwargs)

    def parse_deployment(self, deployment, requestslib_kwargs={}):
    
         url = '%s/%s/deployments/+parse' % (self.url, self.tenant_id)

         self.default_headers['Content-Type'] = 'application/x-yaml'
         requestslib_kwargs['data'] = deployment
        
         return self._make_request('POST', url,
                                   requestslib_kwargs=requestslib_kwargs)

    def deploy(self, deployment, requestslib_kwargs={}):
    
         url = '%s/%s/deployments/' % (self.url, self.tenant_id)

         self.default_headers['Content-Type'] = 'application/x-yaml'
         requestslib_kwargs['data'] = deployment
        
         return self._make_request('POST', url,
                                   requestslib_kwargs=requestslib_kwargs)

    def simulate(self, deployment, requestslib_kwargs={}):
    
        url = '%s/%s/deployments/simulate' % (self.url, self.tenant_id)
        
        self.default_headers['Content-Type'] = 'application/x-yaml'
        requestslib_kwargs['data'] = deployment
        
        return self._make_request('POST', url,
                                  requestslib_kwargs=requestslib_kwargs)
