from ccengine.domain.cloudsites.request.sitecontainer import SiteContainer
from ccengine.clients.base_client import BaseMarshallingClient


class SitesOrchestration(BaseMarshallingClient):

    _site_suffix = '/sites'
    _tech_suffix = '/technologies'

    def __init__(self, url, serialize_format, deserialize_format=None):
        super(SitesOrchestration, self).__init__(serialize_format,
                                                     deserialize_format)
        self.sites_url = ''.join([url, self._site_suffix])
        self.tech_url = ''.join([url, self._tech_suffix])
        self.default_headers['Bypass-Auth'] = 'true'
        ct = ''.join(['application/', self.serialize_format])
        accept = ''.join(['application/', self.deserialize_format])
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept

    def create_sitecontainer(self, site, database=None, application=None, \
                validateOnly=None, requestslib_kwargs=None):
        params = {}
        if validateOnly is not None:
            params['validateOnly'] = validateOnly
        n = SiteContainer(site=site, database=database, \
                          application=application)
        return self.request('POST', self.sites_url, params=params,
                                  response_entity_type=SiteContainer,
                                  request_entity=n,
                                  requestslib_kwargs=requestslib_kwargs)

    def get_technologies(self, requestslib_kwargs=None):
        return self.request('GET', self.tech_url,
                                  response_entity_type=SiteContainer,
                                  requestslib_kwargs=requestslib_kwargs)
