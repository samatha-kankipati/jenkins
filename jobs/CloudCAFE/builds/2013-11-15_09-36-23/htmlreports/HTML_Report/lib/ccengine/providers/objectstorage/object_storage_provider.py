from ccengine.providers.identity.v2_0.identity_api import IdentityAPIProvider
from ccengine.clients.objectstorage.object_storage_client \
    import ObjectStorageAPIClient
from ccengine.clients.objectstorage.cloud_files_client \
    import CloudFilesClient
from ccengine.providers.configuration import MasterConfigProvider


class ObjectStorageClientProvider(object):
    """
    Provider for ObjectStorage/CloudFiles
    """
    SERVICE_CATALOG_CLOUD_FILES = "cloudFiles"
    SERVICE_CATALOG_CLOUD_FILES_CDN = "cloudFilesCDN"

    @staticmethod
    def get_auth_data(username, api_key=None, password=None):
        """
        Authenticate a user using either an API key or password and return the
        data from the authentication request.

        @type  username: string
        @param username: The username to auth with.
        @type  api_key: string
        @param api_key: API key to be used in authenticating.
        @type  password: string
        @param password: Password to be used to authenticate.

        @rtype: object
        @return: Requests response object containing the auth data.
        """
        if api_key is None and password is None:
            raise Exception('You must specify a api_key or password.')

        config = MasterConfigProvider()
        identity_provider = IdentityAPIProvider(config)

        if api_key is not None:
            auth_response = identity_provider.client.authenticate_user_apikey(
                username=username, api_key=api_key)
        if password is not None:
            auth_response = \
                identity_provider.client.authenticate_user_password(
                    username=username, password=password)

        auth_data = auth_response.entity

        return auth_data

    @staticmethod
    def get_client(
            username, region, api_key=None, password=None,
            base_container_name='', base_object_name='', auth_token=None,
            storage_url=None, snet_url=None):
        """
        Get a client which has been authenticated with the provided
        credentials.

        @type  username: string
        @param username: The username to auth with.
        @type  region: string
        @param region: The region to pull the object storage data from in the
            auth request.
        @type  api_key: string
        @param api_key: API key to be used in authenticating.
        @type  password: string
        @param password: Password to be used to authenticate.
        @type  base_container_name: string
        @param base_container_name: Name to be prepended to all containers
            created.
        @type  base_object_name: string
        @param base_object_name: Name to be prepended to all objects created.
        @type  auth_token: string
        @param auth_token: If provided, use this token in the client instead
            of the one provided by auth.
        @type  storage_url: string
        @param storage_url: If provided, use this storage URL in the client
            instead of the one provided by auth.
        @type  snet_url: string
        @param snet_url: If provided, use this SNET URL in the client instead
            of the one provided by auth.

        @rtype: object
        @return: ObjectStorageAPIClient.
        """
        if api_key is None and password is None:
            raise Exception('You must specify a api_key or password.')

        if api_key is not None:
            auth_data = ObjectStorageClientProvider.get_auth_data(
                username, api_key=api_key)

        if password is not None:
            auth_data = ObjectStorageClientProvider.get_auth_data(
                username, password=password)

        service = auth_data.serviceCatalog.get_service(
            ObjectStorageClientProvider.SERVICE_CATALOG_CLOUD_FILES)

        endpoint = service.get_endpoint(region)

        if storage_url is None:
            storage_url = endpoint.publicURL
        if snet_url is None:
            snet_url = endpoint.internalURL
        if auth_token is None:
            auth_token = auth_data.token.id

        client = ObjectStorageAPIClient(
            storage_url, snet_url, auth_token,
            base_container_name=base_container_name,
            base_object_name=base_object_name)

        return client


class CloudFilesClientProvider(object):

    @staticmethod
    def get_client(
            username, region, api_key=None, password=None,
            base_container_name='', base_object_name='', auth_token=None,
            storage_url=None, snet_url=None, cdn_management_url=None):
        """
        Get a client which has been authenticated with the provided
        credentials.

        @type  username: string
        @param username: The username to auth with.
        @type  region: string
        @param region: The region to pull the object storage data from in the
            auth request.
        @type  api_key: string
        @param api_key: API key to be used in authenticating.
        @type  password: string
        @param password: Password to be used to authenticate.
        @type  base_container_name: string
        @param base_container_name: Name to be prepended to all containers
            created.
        @type  base_object_name: string
        @param base_object_name: Name to be prepended to all objects created.
        @type  auth_token: string
        @param auth_token: If provided, use this token in the client instead
            of the one provided by auth.
        @type  storage_url: string
        @param storage_url: If provided, use this storage URL in the client
            instead of the one provided by auth.
        @type  snet_url: string
        @param snet_url: If provided, use this SNET URL in the client instead
            of the one provided by auth.

        @rtype: object
        @return: CloudFilesAPIClient.
        """
        if api_key is None and password is None:
            raise Exception('You must specify a api_key or password.')

        if api_key is not None:
            auth_data = ObjectStorageClientProvider.get_auth_data(
                username, region, api_key=api_key)

        if password is not None:
            auth_data = ObjectStorageClientProvider.get_auth_data(
                username, region, password=password)

        service = auth_data.serviceCatalog.get_service(
            ObjectStorageClientProvider.SERVICE_CATALOG_CLOUD_FILES)

        endpoint = service.get_endpoint(region)

        if storage_url is None:
            storage_url = endpoint.publicURL
        if snet_url is None:
            snet_url = endpoint.internalURL
        if auth_token is None:
            auth_token = auth_data.token.id

        if cdn_management_url is None:
            service = auth_data.serviceCatalog.get_service(
                ObjectStorageClientProvider.SERVICE_CATALOG_CLOUD_FILES_CDN)
            endpoint = cdn_service.get_endpoint(
                config.cloudfiles_cdn_api.region)
            cdn_management_url = endpoint.publicURL

        client = CloudFilesClient(
            storage_url, auth_token, cdn_management_url,
            base_container_name=base_container_name,
            base_object_name=base_object_name)

        return client
