__author__ = 'ram5454'

from ccengine.common.connectors import rest
from ccengine.clients.base_client import BaseRESTClient


class MoneyballAPIClient(BaseRESTClient):

    def __init__(self, url, auth_token):
        super(MoneyballAPIClient, self).__init__()
        self.url = url
        self.default_headers = {'X-Auth-Token': auth_token}


    def give_account_details(self, id, requestslib_kwargs=None):
        url = "{0}/accounts/{1}".format(self.url, str(id))
        return self.request('GET', url, headers=self.default_headers,
                            requestslib_kwargs=requestslib_kwargs)


    def give_defection_index(self, id, requestslib_kwargs=None):
        url = "{0}/models/defection/{1}".format(self.url, str(id))
        return self.request('GET', url, headers=self.default_headers,
                            requestslib_kwargs=requestslib_kwargs)

    def give_customer_footprint(self, id, requestslib_kwargs=None):
        url = "{0}/models/footprint/{1}".format(self.url, str(id))
        return self.request('GET', url, headers=self.default_headers,
                            requestslib_kwargs=requestslib_kwargs)

    def give_user_agent(self, id, requestslib_kwargs=None):
        url = "{0}/reports/{1}".format(self.url, str(id))
        return self.request('GET', url, headers=self.default_headers,
                            requestslib_kwargs=requestslib_kwargs)

