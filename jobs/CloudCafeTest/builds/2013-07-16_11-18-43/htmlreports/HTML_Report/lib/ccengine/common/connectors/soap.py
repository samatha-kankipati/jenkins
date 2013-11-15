from ccengine.common.connectors.base_connector import BaseConnector
import logging
try:
    import suds
    import suds.xsd.doctor as suds_doctor
    from suds.sax.element import Element
except:
    pass


class SoapConnector(BaseConnector):

    def __init__(self, wsdl, endpoint=None, username=None, password=None):
        super(SoapConnector, self).__init__()
        logging.getLogger('suds').setLevel(logging.CRITICAL)
        #logging.basicConfig(level=logging.INFO)
        #logging.getLogger('suds.client').setLevel(logging.DEBUG)
        #logging.getLogger('suds.transport').setLevel(logging.CRITICAL)
        #logging.getLogger('suds.xsd').setLevel(logging.CRITICAL)
        #logging.getLogger('suds.wsdl').setLevel(logging.CRITICAL)
        #logging.getLogger('suds.resolver').setLevel(logging.CRITICAL)
        #logging.getLogger('suds.metrics').setLevel(logging.CRITICAL)
        #logging.getLogger('suds.').setLevel(logging.CRITICAL)
        self.wsdl = wsdl
        self.endpoint = endpoint
        self.username = username
        self.password = password

        # Fix import for parsing most WSDLs
        ns_import = suds_doctor.Import(
                        'http://schemas.xmlsoap.org/soap/encoding/')
        doctor = suds_doctor.ImportDoctor(ns_import)
        self.client = suds.client.Client(wsdl,
                                         doctor=doctor,
                                         location=endpoint,
                                         username=username,
                                         password=password,
                                         faults=False)

    def print_services(self):
        '''Prints the methods that can be used to make soap requests.'''
        print self.client

    def get_service(self):
        return self.client.service

    def set_location(self, location):
        self.client.set_options(location=location)

    def set_credentials(self, username, password):
        self.client.set_options(username=username, password=password)

    def set_wsdl(self, wsdl):
        self.client.wsdl = wsdl

    def set_headers(self, header_list):
        """
        expecting a list of headers. each header is a dictionary consisting
        of:
        header['ns_prefix'] = prefix for the namespace 
        header['ns_url'] = url of the namespace
        header['name'] = name of the header element (tag name)
        header['text'] = text of the header element
        """
        element_list = []
        for h in header_list:
            ns = (h['ns_prefix'], h['ns_url'])
            e = Element(h['name'], ns=ns).setText(h['text'])
            element_list.append(e)
        self.client.set_options(soapheaders=element_list)
