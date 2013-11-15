from ccengine.clients.core.core_api import CoreAPIClient


class BandwidthAPIClient(CoreAPIClient):
    '''
    Client for network related queries in CTK API
    '''
    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):

        super(BandwidthAPIClient, self).__init__(url, auth_token,
                                                 serialize_format,
                                                 deserialize_format)

    def get_allotment_attributes_using_allotmentwhere(
            self, where_conditions, attribute=None, limit=None, offset=None):
        '''
        @summary: Get Attributes of bandwidth Allotment Class
        @param where_conditions: Values of where conditions
        @type where_conditions: Array of CTK API objects
        @param attributes: Attributes of bandwidth class
        @type attributes: List or dictionary of attribute name-value pairs
        @param limit: Effective limit on returned query
        @type limit: integer
        @param offset: Effective offset of returned query
        @type offset: integer
        '''
        if attribute is None:
            attribute = ["id"]
        class_name = "Bandwidth.Allotment"
        response = self.list(class_name=class_name,
                             where_class="Bandwidth.AllotmentWhere",
                             where_conditions=where_conditions,
                             attributes=attribute,
                             limit=limit, offset=offset)
        return response

    def get_billabledevices_attributes_using_billabledeviceswhere(
            self, where_conditions, attribute=None, limit=None, offset=None):
        '''
        @summary: Get Attributes of bandwidth billabledevices class
        @param where_conditions: Values of where conditions
        @type where_conditions: Array of CTK API objects
        @param attributes: Attributes of bandwidth class
        @type attributes: List or dictionary of attribute name-value pairs
        @param limit: Effective limit on returned query
        @type limit: integer
        @param offset: Effective offset of returned query
        @type offset: integer
        '''
        if attribute is None:
            attribute = ["id"]
        class_name = "Bandwidth.BillableDevices"
        response = self.list(class_name=class_name,
                             where_class="Bandwidth.BillableDevicesWhere",
                             where_conditions=where_conditions,
                             attributes=attribute,
                             limit=limit, offset=offset)
        return response

    def get_certificate_using_certificatewhere(
            self, where_conditions, attribute=None, limit=None, offset=None):
        '''
        @summary: Get Attributes of bandwidth billabledevices class
        @param where_conditions: Values of where conditions
        @type where_conditions: Array of CTK API objects
        @param attributes: Attributes of bandwidth class
        @type attributes: List or dictionary of attribute name-value pairs
        @param limit: Effective limit on returned query
        @type limit: integer
        @param offset: Effective offset of returned query
        @type offset: integer
        '''
        if attribute is None:
            attribute = ["id"]
        class_name = "Certificate.Certificate"
        response = self.list(class_name=class_name,
                             where_class="Certificate.CertificateWhere",
                             where_conditions=where_conditions,
                             attributes=attribute,
                             limit=limit, offset=offset)
        return response
