from ccengine.providers.base_provider import BaseProvider
from ccengine.clients.lbaas.zeus_client import ZeusClient


class ZeusProvider(BaseProvider):

    class ZeusServiceTypes(object):
        VIRTUAL_SERVER = 'VirtualServer.wsdl'
        TRAFFIC_IP_GROUPS = 'TrafficIPGroups.wsdl'
        POOL = 'Pool.wsdl'
        SSL_CERTIFICATES = 'Catalog.SSL.Certificates.wsdl'
        PROTECTION = 'Catalog.Protection.wsdl'
        MONITOR = 'Catalog.Monitor.wsdl'

    def __init__(self, config, logger):
        '''
        Sets config, sets up client, sets deserializer and serializer based
        on format defined in the config.
        '''
        super(ZeusProvider, self).__init__()
        self.config = config
        #alias config values to smaller namespace
        soap_ep = config.lbaas_api.zeus_soap_endpoint
        soap_un = config.lbaas_api.zeus_username
        soap_pw = config.lbaas_api.zeus_password

        #set up zeus virtual server client
        vs_wsdl = '/'.join([config.lbaas_api.zeus_wsdl_location,
                            self.ZeusServiceTypes.VIRTUAL_SERVER])
        self.zeus_vs = ZeusClient(vs_wsdl, endpoint=soap_ep, username=soap_un,
                                  password=soap_pw)

        #set up zeus traffic ip groups client
        tig_wsdl = '/'.join([config.lbaas_api.zeus_wsdl_location,
                             self.ZeusServiceTypes.TRAFFIC_IP_GROUPS])
        self.zeus_tig = ZeusClient(tig_wsdl, endpoint=soap_ep,
                                   username=soap_un, password=soap_pw)

        #set up zeus pool client
        pool_wsdl = '/'.join([config.lbaas_api.zeus_wsdl_location,
                              self.ZeusServiceTypes.POOL])
        self.zeus_pool = ZeusClient(pool_wsdl, endpoint=soap_ep,
                                    username=soap_un, password=soap_pw)

        #set up zeus ssl certificate client
        ssl_wsdl = '/'.join([config.lbaas_api.zeus_wsdl_location,
                            self.ZeusServiceTypes.SSL_CERTIFICATES])
        self.zeus_ssl = ZeusClient(ssl_wsdl, endpoint=soap_ep,
                                   username=soap_un, password=soap_pw)

        #set up zeus protection client
        prot_wsdl = '/'.join([config.lbaas_api.zeus_wsdl_location,
                             self.ZeusServiceTypes.PROTECTION])
        self.zeus_protection = ZeusClient(prot_wsdl, endpoint=soap_ep,
                                          username=soap_un, password=soap_pw)

        #set up zeus protection client
        hm_wsdl = '/'.join([config.lbaas_api.zeus_wsdl_location,
                            self.ZeusServiceTypes.MONITOR])
        self.zeus_monitor = ZeusClient(hm_wsdl, endpoint=soap_ep,
                                       username=soap_un, password=soap_pw)
