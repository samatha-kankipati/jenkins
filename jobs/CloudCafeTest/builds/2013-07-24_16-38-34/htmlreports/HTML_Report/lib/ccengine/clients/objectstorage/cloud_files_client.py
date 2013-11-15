import re
from ccengine.clients.objectstorage.object_storage_client\
    import ObjectStorageAPIClient


class CloudFilesClient(ObjectStorageAPIClient):
    def __init__(
            self, storage_url, snet_url, auth_token, cdn_management_url,
            base_container_name=None, base_object_name=None):
        """
        Constructor for the Cloud Files Client.

        @type  storage_url: string
        @param storage_url: URL of the storage account to use.
        @type  auth_token: string
        @param auth_token: Authentication token to send with requests.
        @type  cdn_management_url: string
        @param cdn_management_url: URL to use when managing CDN for containers.
        @type  base_container_name: string
        @param base_container_name: Used in creation of container names when
            using helper functions.
        @type  base_object_name: string
        @param base_object_name: Used in creation of object names when
            using helper functions.
        """
        super(CloudFilesClient, self).__init__(
            storage_url, snet_url, auth_token, base_container_name,
            base_object_name)

        self.cdn_management_url = cdn_management_url

    def create_cdn_container(self, name, ttl=None, log_delivery=None):
        self.create_container(name)
        self.cdn_enable_container(name, ttl, log_delivery)

    def get_cdn_containers(self):
        """
        Lists the CDN enabled containers for the accont.

        @rtype:  object
        @return: requests object for the call.
        """

        # TODO(rich5317): Improve to use the following for managing accounts
        # with a large amount of CDN enabled containers.
        #     limit, marker, end_marker, format, enabled_only
        headers = {}

        url = self.cdn_management_url

        return self.request('PUT', url, headers=headers)

    def get_cdn_container_ttl(self, name):
        """
        Get the TTL set for a given container.

        @rtype:  integer
        @return: TTL
        """
        details = self.get_cdn_container_details(name)

        if 'x-ttl' not in details:
            return None

        return int(details['x-ttl'])

    def set_cdn_container_ttl(self, name, ttl):
        """
        Set the TTL on a given container.

        @type  name: string
        @param name: The name of the container to set the TTL for.
        @type  ttl:  integer
        @param ttl: The TTL to set for the container.
        """
        headers = {}
        headers['x-ttl'] = str(ttl)

        url = '/'.join([self.cdn_management_url, name])
        r = self.request('PUT', url, headers=headers)

    def is_cdn_log_delivery_enabled(self, name):
        """
        Get the status of log retention for a given container.

        @type  name: string
        @param name: The name of the container to check for log retention.
        @rtype:  boolean
        @return: True if log retention is enabled, False otherwise.
        """
        details = self.get_cdn_container_details(name)

        if 'x-log-retention' not in details:
            return None

        return details['x-log-retention']

    def cdn_enable_log_delivery(self, name):
        """
        Enable log delivery for a given container.

        @type  name: string
        @param name: The name of the container to enable log retention for.
        """
        headers = {}
        headers['x-log-retention'] = 'True'

        url = '/'.join([self.cdn_management_url, name])
        r = self.request('PUT', url, headers=headers)

    def cdn_disable_log_delivery(self, name):
        """
        Disable log delivery for a given container.

        @type  name: string
        @param name: The name of the container to disable log retention for.
        """
        headers = {}
        headers['x-log-retention'] = 'False'

        url = '/'.join([self.cdn_management_url, name])
        r = self.request('PUT', url, headers=headers)

    def get_cdn_container_uri(self, name):
        """
        Get the URI for the CDN enabled container.

        @type  name: string
        @param name: The name of the container to retrieve the URI for.
        """
        details = self.get_cdn_container_details(name)

        if 'x-cdn-uri' not in details:
            return None

        return details['x-cdn-uri']

    def get_cdn_container_ssl_uri(self, name):
        """
        Get the SSL URI for the CDN enabled container.

        @type  name: string
        @param name: The name of the container to retrieve the URI for.
        """
        details = self.get_cdn_container_details(name)

        if 'x-cdn-ssl-uri' not in details:
            return None

        return details['x-cdn-ssl-uri']

    def get_cdn_container_streaming_uri(self, name):
        """
        Get the Streaming URI for the CDN enabled container.

        @type  name: string
        @param name: The name of the container to retrieve the URI for.
        """
        details = self.get_cdn_container_details(name)

        if 'x-cdn-streaming-uri' not in details:
            return None

        return details['x-cdn-streaming-uri']

    def get_cdn_container_ios_streaming_uri(self, name):
        """
        Get the iOS Streaming URI for the CDN enabled container.

        @type  name: string
        @param name: The name of the container to retrieve the URI for.
        """
        details = self.get_cdn_container_details(name)

        if 'x-cdn-ios-uri' not in details:
            return None

        return details['x-cdn-ios-uri']

    def get_cdn_container_details(self, name):
        """
        Returns the details on the CDN enabled container.

        @type  name: string
        @param name: The name of the container to retrieve the details for.
        @rtype:  list
        @return: list of strings containing the headers set for the container.
        """

        url = '/'.join([self.cdn_management_url, name])
        r = self.request('HEAD', url)
        details = r.headers

        return details

    def cdn_enable_container(self, name, ttl=None, log_delivery=None):
        """
        Adds the container to the CDN.

        @type  name: string
        @param name: The name of the container to CDN enable.
        @type  ttl: integer
        @param ttl: The TTL to set for the container.
        @type  log_delivery: boolean
        @param log_delivery: True to enable log delivery else False.
        """

        headers = {}
        headers['x-cdn-enabled'] = 'True'

        url = '/'.join([self.cdn_management_url, name])
        r = self.request('PUT', url, headers=headers)

        if ttl is not None:
            headers['X-TTL'] = ttl

        if log_delivery is not None:
            headers['X-LOG-RETENTION'] = log_delivery

        url = '/'.join([self.cdn_management_url, name])

        return self.request('PUT', url, headers=headers)

    def cdn_disable_container(self, name):
        """
        Removes the container from the CDN.  Objects remain public until their
        TTL expires.

        @param name: The name of the container to remove from the CDN.
        @type  ttl: integer
        """

        headers = {}
        headers['X-CDN-Enabled'] = 'False'

        url = '/'.join([self.cdn_management_url, name])

        return self.request('POST', url, headers=headers)

    def get_object_via_cdn(self, container_name, object_name):
        """
        Retrieves a object via the CDN network

        @type  container_name: string
        @param container_name: the contianer the object belongs to.
        @type  object_name: string
        @param object_name: the object to be retrieved.

        @rtype:  object
        @return: requests object for the request.
        """

        # TODO(rich5317): Add ability to use akamai staging.

        url = self.get_cdn_container_uri(container_name)
        url = '/'.join([url, object_name])

        return self.request('GET', url)

    def get_object_via_cdn_ssl(self, container_name, object_name):
        """
        Retrieves a object via the CDN network using SSL

        @type  container_name: string
        @param container_name: the contianer the object belongs to.
        @type  object_name: string
        @param object_name: the object to be retrieved.

        @rtype:  object
        @return: requests object for the request.
        """

        # TODO(rich5317): Add ability to use akamai staging.

        url = self.get_cdn_container_ssl_uri(container_name)
        url = '/'.join([url, object_name])

        return self.request('GET', url)

    def get_object_via_cdn_streaming(self, container_name, object_name):
        """
        Streams a object over the CDN network.

        @type  container_name: string
        @param container_name: the contianer the object belongs to.
        @type  object_name: string
        @param object_name: the object to be retrieved.

        @rtype:  object
        @return: requests object for the request.
        """

        # TODO(rich5317): Add ability to use akamai staging.

        url = self.get_cdn_container_streaming_uri(container_name)
        url = '/'.join([url, object_name])

        return self.request('GET', url)

    def get_object_via_cdn_ios_streaming(self, container_name, object_name):
        """
        Streams a object over the CDN network.

        @type  container_name: string
        @param container_name: the contianer the object belongs to.
        @type  object_name: string
        @param object_name: the object to be retrieved.

        @rtype:  list
        @return: list of requests objects used in streaming the object.
        """

        # TODO(rich5317): Add ability to use akamai staging.

        request_list = []

        # Make the inital requeset (which is redirected)
        url = self.get_cdn_container_ios_streaming_uri(container_name)
        url = '/'.join([url, object_name])
        r = self.request('GET', url)
        request_list.append(r)

        # Request the 'manifest' of video segments
        m = re.findall('^(http.*/)master.*', r.url)
        if len(m) != 1:
            return None
        base_url = m[0]
        m = re.findall('\n(index.*)\n', r.content)
        if len(m) != 1:
            return None
        url = ''.join([base_url, m[0]])
        r = self.request('GET', url)
        request_list.append(r)

        # Request each segment
        m = re.findall('\n(segment.*)\n', r.content)
        for segment in m:
            # 5 - get segments
            url = ''.join([base_url, segment])
            r = self.request('GET', url)
            request_list.append(r)

        return request_list
