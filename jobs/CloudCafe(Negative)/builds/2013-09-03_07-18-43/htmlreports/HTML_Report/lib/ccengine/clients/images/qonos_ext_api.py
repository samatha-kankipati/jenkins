from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.domain.images.qonos_ext.request.scheduled_images import \
    ScheduledImages as SchImagesRequest
from ccengine.domain.images.qonos_ext.response.scheduled_images import \
    ScheduledImages as SchImagesResponse
from ccengine.domain.images.qonos_ext.extensions import \
    Extensions as ExtResponse


class ScheduledImagesClient(BaseMarshallingClient):

    def __init__(self, url, serialize_format, tenant, auth_token,
                 deserialize_format=None):

        super(ScheduledImagesClient, self).__init__(serialize_format,
                                                    deserialize_format)

        self.url = url
        ct = 'application/{0}'.format(self.serialize_format)
        accept = 'application/{0}'.format(self.deserialize_format)
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.default_headers['X-Auth-Project-Id'] = tenant
        self.default_headers['X-Auth-Token'] = auth_token

    def enable_scheduled_images(self, tenant_id=None, instance_id=None,
                                retention=None, requestslib_kwargs=None):

        full_url = \
            "{0}/{1}/servers/{2}/rax-si-image-schedule".format(self.url,
                                                              tenant_id,
                                                              instance_id)

        scheduled_images = SchImagesRequest(retention=retention)

        return self.request("POST", full_url,
                            response_entity_type=SchImagesResponse,
                            request_entity=scheduled_images,
                            requestslib_kwargs=requestslib_kwargs)

    def disable_scheduled_images(self, tenant_id=None, instance_id=None,
                                 requestslib_kwargs=None):

        full_url = \
            "{0}/{1}/servers/{2}/rax-si-image-schedule".format(self.url,
                                                              tenant_id,
                                                              instance_id)

        return self.request("DELETE", full_url,
                            response_entity_type=SchImagesResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def get_scheduled_images_settings(self, tenant_id=None,
                                      instance_id=None,
                                      requestslib_kwargs=None):

        full_url = \
            "{0}/{1}/servers/{2}/rax-si-image-schedule".format(self.url,
                                                              tenant_id,
                                                              instance_id)

        return self.request("GET", full_url,
                            response_entity_type=SchImagesResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def get_incorrect_base_url(self, tenant_id=None, instance_id=None,
                               url_addition=None, requestslib_kwargs=None):

        full_url = \
            "{0}/{1}/servers/{2}/rax-si-image-schedule{3}".format(self.url,
                                                                 tenant_id,
                                                                 instance_id,
                                                                 url_addition)

        self.request("GET", full_url, response_entity_type=SchImagesResponse,
                     requestslib_kwargs=requestslib_kwargs)

    def enable_sch_images_missing_body(self, tenant_id=None,
                                       instance_id=None,
                                       requestslib_kwargs=None):

        full_url = \
            "{0}/{1}/servers/{2}/rax-si-image-schedule".format(self.url,
                                                              tenant_id,
                                                              instance_id)

        return self.request("POST", full_url,
                            response_entity_type=SchImagesResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def disable_sch_images_including_body(self, tenant_id=None,
                                          instance_id=None, retention=None,
                                          requestslib_kwargs=None):

        full_url = \
            "{0}/{1}/servers/{2}/rax-si-image-schedule".format(self.url,
                                                              tenant_id,
                                                              instance_id)

        scheduled_images = SchImagesRequest(retention=retention)

        return self.request("DELETE", full_url,
                            response_entity_type=SchImagesResponse,
                            request_entity=scheduled_images,
                            requestslib_kwargs=requestslib_kwargs)

    def get_scheduled_images_settings_including_body(self, tenant_id=None,
                                                     instance_id=None,
                                                     retention=None,
                                                     requestslib_kwargs=None):

        full_url = \
            "{0}/{1}/servers/{2}/rax-si-image-schedule".format(self.url,
                                                              tenant_id,
                                                              instance_id)

        scheduled_images = SchImagesRequest(retention=retention)

        return self.request("GET", full_url,
                            response_entity_type=SchImagesResponse,
                            request_entity=scheduled_images,
                            requestslib_kwargs=requestslib_kwargs)

    def list_extensions(self, tenant_id=None, requestslib_kwargs=None):

        full_url = \
            "{0}/{1}/extensions".format(self.url, tenant_id)

        return self.request("GET", full_url,
                            response_entity_type=ExtResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def get_extension(self, tenant_id=None, alias=None,
                      requestslib_kwargs=None):

        full_url = \
            "{0}/{1}/extensions/{2}".format(self.url, tenant_id, alias)

        return self.request("GET", full_url,
                            response_entity_type=ExtResponse,
                            requestslib_kwargs=requestslib_kwargs)
