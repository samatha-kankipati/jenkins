from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.domain.rad.response.flavors import FlavorsResponse
from ccengine.domain.rad.request.flavors_request import FlavorsRequest


class FlavorsClient(BaseMarshallingClient):

    """
    @summary: Client for RAD API mapping to the flavors web service.
    """

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):

        super(FlavorsClient, self).__init__(serialize_format,
                                            deserialize_format)
        content_type = "application/{0}".format(self.serialize_format)
        accept = "application/{0}".format(self.deserialize_format)
        self.default_headers['Content-Type'] = content_type
        self.default_headers['Accept'] = accept
        self.url = url

    def create_flavor(self, device_id=None, ingredient_skus=None, desc=None,
                      **requestslib_kwargs):
        """
        @summary: Create a flavor
        @param device_id: Id of an existing Core device
        @param ingredient_skus: List of SKU Objects
        @param desc: Description of a flavor
        @param requestslib_kwargs: overriding request parameters
        @return Flavors Response
        """
        url = '{0}/flavors'.format(self.url)
        flavor_req_obj = FlavorsRequest(device_id=device_id,
                                        ingredient_skus=ingredient_skus,
                                        desc=desc)
        response = self.request('POST', url,
                                request_entity=flavor_req_obj,
                                response_entity_type=FlavorsResponse,
                                requestslib_kwargs=requestslib_kwargs)
        return response

    def get_flavors(self, **requestslib_kwargs):
        """
        @summary: Get all the available flavors
        @param requestslib_kwargs: overriding request parameters
        @return FlavorResponse Domain Object
        """
        url = '{0}/flavors'.format(self.url)
        response = self.request('GET', url,
                                response_entity_type=FlavorsResponse,
                                requestslib_kwargs=requestslib_kwargs)
        return response

    def get_flavor(self, flavor_id, **requestslib_kwargs):
        """
        @summary: Get a flavor by the given id
        @param flavor_id: The id of the flavor in RAD System
        @return FlavorResponse Domain Object
        """
        url = '{0}/flavors/{1}'.format(self.url, flavor_id)
        response = self.request('GET', url,
                                response_entity_type=FlavorsResponse,
                                requestslib_kwargs=requestslib_kwargs)
        return response
