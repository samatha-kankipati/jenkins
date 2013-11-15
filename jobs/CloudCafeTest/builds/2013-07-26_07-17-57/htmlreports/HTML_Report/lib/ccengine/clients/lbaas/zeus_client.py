from ccengine.clients.base_client import BaseSOAPClient


class ZeusClient(BaseSOAPClient):

    def __init__(self, wsdl, endpoint=None, username=None, password=None):
        BaseSOAPClient.__init__(self, wsdl, endpoint, username, password)
