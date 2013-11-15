'''
@summary: Classes and Utilities that provide low level connectivity to the
          Rest Client
@note: Should be consumed/exposed by a a L{ccengine.providers} class and
       rarely be used directly by any other object or process
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.domain.compute.response.limits import Limits


class LimitsApiClient(BaseMarshallingClient):

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):

        super(LimitsApiClient, self).__init__(serialize_format,
                                              deserialize_format)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        ct = ''.join(['application/', self.serialize_format])
        accept = ''.join(['application/', self.deserialize_format])
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.url = url

    def get_limits(self, requestslib_kwargs=None):
        """
        @summary: Returns limits.
        @param requestslib_kwargs: Overrides any default values injected by
        the framework
        @type requestslib_kwargs:dict
        @return: limit_response
        @rtype: Limits Response Domain Object
        """
        url = '%s/limits' % (self.url)
        limit_response = self.request('GET', url,
                                      response_entity_type=Limits,
                                      requestslib_kwargs=requestslib_kwargs)
        return limit_response

    def _get_absolute_limits_property(self, limits_property=None):
        """
        @summary: Returns the value of the specified key from the
                absolute_limits dictionary
        @param requestslib_kwargs: Overrides any default values injected by
        the framework
        @type requestslib_kwargs:dict
        """
        if property is None:
            return None
        limits_response = self.get_limits()
        absolute_limits = vars(limits_response.entity).get('absolute')
        if absolute_limits is not None:
            return absolute_limits.get(limits_property)
        else:
            return None

    def get_max_server_meta(self):
        """
        @summary: Returns maximum number of metadata allowed for a server
        @return: Maximum number of server meta data
        @rtype:  Integer
        """
        return self._get_absolute_limits_property('maxServerMeta')

    def get_max_image_meta(self):
        """
        @summary: Returns maximum number of metadata allowed for an Image.
        @return: Maximum number of image meta data
        @rtype: Integer
        """
        return self._get_absolute_limits_property('maxImageMeta')

    def get_personality_file_limit(self):
        """
        @summary: Returns maximum number of personality files allowed for a
                  server
        @return: Maximum number of personality files.
        @rtype: Integer
        """
        return self._get_absolute_limits_property('maxPersonality')

    def get_personality_file_size_limit(self):
        """
        @summary: Returns the maximum size of a personality file.
        @return: Maximum size of a personality file.
        @rtype: Integer
        """
        return self._get_absolute_limits_property('maxPersonalitySize')

    def get_max_total_instances(self):
        """
        @summary: Returns maximum number of server allowed for a user
        @return: Maximum number of server
        @rtype: Integer
        """
        return self._get_absolute_limits_property('maxTotalInstances')

    def get_max_total_RAM_size(self):
        """
        @summary: Returns maximum RAM size to create servers for a user
        @return: Maximum RAM size
        @rtype: Integer
        """
        return self._get_absolute_limits_property('maxTotalRAMSize')

    def get_total_RAM_used(self):
        """
        @summary: Returns total RAM used by a user
        @return: total RAM used
        @rtype: Integer
        """
        return self._get_absolute_limits_property('totalRAMUsed')
