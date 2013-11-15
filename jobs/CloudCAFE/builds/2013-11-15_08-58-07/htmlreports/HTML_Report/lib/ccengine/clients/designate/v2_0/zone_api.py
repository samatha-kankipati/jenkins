from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.domain.designate.request.zone import Zone
from ccengine.domain.designate.response.zone_resp import zone as RespZone
from ccengine.domain.designate.response.zone import Zone as ZoneList


class ZoneClient(BaseMarshallingClient):

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):
        super(ZoneClient, self).__init__(serialize_format,
                                         deserialize_format)
        self.url = url
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        self.default_headers['Content-Type'] = 'application/{0}'.format(
            self.serialize_format)
        self.default_headers['Accept'] = 'application/{0}'.format(
            self.serialize_format)

    def create_zone(self, name=None, email=None,
                    ttl=None, requestslib_kwargs=None):
        """
        Create zone(Create a new zone.)
        POST
        v1/zones
        """
        zone_req = Zone(name=name, email=email, ttl=ttl)
        url = "{0}/zones".format(self.url)
        return self.request('POST', url, response_entity_type=RespZone,
                            request_entity=zone_req,
                            requestslib_kwargs=requestslib_kwargs)

    def update_zone(self, name=None, zone_id=None,
                    email=None, ttl=None, requestslib_kwargs=None):
        """
        Update zones(Update a zone.)
        PUT
        v1/zones
        """
        zone_req = Zone(name=name, email=email, ttl=ttl)
        url = "{0}/zones/{1}".format(self.url, zone_id)
        return self.request('PUT', url,
                            response_entity_type=RespZone,
                            request_entity=zone_req,
                            requestslib_kwargs=requestslib_kwargs)

    def get_zone(self, zone_id, requestslib_kwargs=None):
        """
        list zone details by id
        GET
        v1/zones/{zoneID}
        """
        url = "{0}/zones/{1}".format(self.url, zone_id)
        return self.request('GET', url,
                            response_entity_type=RespZone,
                            requestslib_kwargs=requestslib_kwargs)

    def list_zones(self, requestslib_kwargs=None):
        """
        List zones
        GET
        v1/zones
        """
        url = "{0}/zones".format(self.url)
        return self.request('GET', url, response_entity_type=ZoneList,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_zone(self, zone_id, requestslib_kwargs=None):
        """
        list zone details by id
        DELETE
        v1/zones/{zoneID}
        """
        url = "{0}/zones/{1}".format(self.url, zone_id)
        return self.request('DELETE', url, response_entity_type=RespZone,
                            requestslib_kwargs=requestslib_kwargs)
