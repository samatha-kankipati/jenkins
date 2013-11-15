from ccengine.clients.base_client import BaseRESTClient
import json


class NVPClient(BaseRESTClient):
    '''Client using requests to talk to NVP Manager.'''

    _SUFFIX = '/ws.v1'

    def __init__(self, url, username, password):
        super(NVPClient, self).__init__()
        self.url = str(url) + self._SUFFIX
        self.default_headers = {}
        self.default_headers['Content-Type'] = 'application/json'
        self.default_headers['Accept'] = 'application/json'
        self._login(username, password)

    def _login(self, username, password):
        url = '/'.join([self.url, 'login'])
        body = {'username': username, 'password': password}
        login_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        r = self.post(url, body, headers=login_headers, params=body)
        self.default_headers['Cookie'] = r.headers['set-cookie']

    def list_lswitches(self, fields='*', page_length=1000):
        url = '/'.join([self.url, 'lswitch'])
        params = {'fields': fields, '_page_length': page_length}
        r = self.get(url, params=params)
        return json.loads(r.content)

    def get_lswitch(self, lswitch_uuid):
        url = '/'.join([self.url, 'lswitch', str(lswitch_uuid)])
        r = self.get(url)
        return json.loads(r.content)

    def list_lswitch_ports(self, lswitch_uuid='*', attachment_vif_mac=None,
                           fields='*', page_length=1000):
        url = '/'.join([self.url, 'lswitch', str(lswitch_uuid), 'lport'])
        params = {'fields': fields, '_page_length': page_length}
        if attachment_vif_mac is not None:
            params['attachment_vif_mac'] = attachment_vif_mac.upper()
        r = self.get(url, params=params)
        return json.loads(r.content)

    def get_lswitch_port(self, lswitch_uuid, lswitch_port_uuid):
        url = '/'.join([self.url, 'lswitch', str(lswitch_uuid), 'lport',
                        str(lswitch_port_uuid)])
        r = self.get(url)
        return json.loads(r.content)

    def list_qos(self, page_length=1000):
        url = '/'.join([self.url, 'lqueue'])
        params = {'_page_length': str(page_length)}
        r = self.get(url, params=params,
                     verify=False)
        return json.loads(r.content)

    def get_qos(self, qos_uuid):
        url = '/'.join([self.url, 'lqueue', str(qos_uuid)])
        r = self.get(url)
        return json.loads(r.content)
