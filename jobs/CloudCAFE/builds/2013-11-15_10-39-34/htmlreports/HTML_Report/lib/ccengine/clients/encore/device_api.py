from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.domain.encore.response.encore_response import Device
from ccengine.domain.encore.response.encore_response import Devices


class DeviceAPIClient(BaseMarshallingClient):
    """
    @summary:Client for Encore Device API
    """
    def __init__(self, url, auth_token, serialize_format, deserialize_format):
        super(DeviceAPIClient, self).__init__(serialize_format,
                                              deserialize_format)
        content_type = "application/{0}".format(self.serialize_format)
        accept = "application/{0}".format(self.deserialize_format)
        self.default_headers['Content-Type'] = content_type
        self.default_headers['Accept'] = accept
        self.url = url

    def list_devices(self, account_id):
        """
        @summary: Device API to list all available devices
        @param account_id: Account Number for which devices are to be listed
        @type account_id: String
        @return: Devices response object
        @rtype: Response Domain Object
        
        """
        url = '{0}/accounts/{1}/devices'.format(self.url, account_id)
        response = self.request('GET', url, response_entity_type=Devices)
        return response

    def get_device(self, account_id, device_id):
        """
        @summary: Device API to get a specific device details
        @param account_id: Account to which device belongs to
        @type account_id: String
        @param device_id: Device whose details are required
        @type device_id: String
        @return: Device response object
        @rtype: Response Domain Object
        
        """
        url = '{0}/accounts/{1}/devices/{2}'.format(self.url,
                                                    account_id,
                                                    device_id)
        response = self.request('GET', url, response_entity_type=Device)
        return response
