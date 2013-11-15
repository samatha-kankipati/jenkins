#from ccengine.common.connectors import rest
from ccengine.clients.base_client import BaseRESTClient


class ServiceMixAPIClient(BaseRESTClient):
    def __init__(self, url):
        super(ServiceMixAPIClient, self).__init__()
        self.url = url

    def set_account_status(
            self, account_id, account_status, requestslib_kwargs=None):

        url = "{0}/account/v1.0".format(self.url)
        soapenv = "http://schemas.xmlsoap.org/soap/envelope/"
        rax_xmlns = "http://cloud.rackspace.com/account/1.0"
        soap_request = (
            '<soapenv:Envelope xmlns:soapenv="{soapenv}"xmlns:ns="{rax_xmlns}'
            '"><soapenv:Header/><soapenv:Body><ns:UpdateAccountStatus>'
            '<ns:accountId>{account_id}</ns:accountId><ns:accountStatus>'
            '{account_status}</ns:accountStatus></ns:UpdateAccountStatus>'
            '</soapenv:Body></soapenv:Envelope>'.format(
                soapenv=soapenv, rax_xmlns=rax_xmlns, account_id=account_id,
                account_status=account_status))

        return self.request(
            'POST', url, data=soap_request,
            requestslib_kwargs=requestslib_kwargs)
