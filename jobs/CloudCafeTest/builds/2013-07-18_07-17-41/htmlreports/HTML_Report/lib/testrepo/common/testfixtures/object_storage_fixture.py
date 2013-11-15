from testrepo.common.testfixtures.fixtures \
    import BaseTestFixture, BaseParameterizedTestFixture
from ccengine.providers.atomhopper import AtomHopperProvider
#from ccengine.providers.identity.identity_v2_0_api import IdentityAPIProvider
from ccengine.providers.objectstorage.object_storage_provider \
    import ObjectStorageClientProvider, CloudFilesClientProvider
from ccengine.common.tools import filetools
from ccengine.clients.identity.v2_0.rax_auth_api \
    import IdentityClient

class ObjectStorageTestFixture(BaseTestFixture):
    """
    Fixture provides all object storage functionality.
    """

    @classmethod
    def setUpClass(cls):
        super(ObjectStorageTestFixture, cls).setUpClass()
        cls.region = cls.config.object_storage_api.region

        #gets main client using config values
        username = cls.config.identity_api.username
        api_key = cls.config.identity_api.api_key
        region = cls.region
        cls.client = ObjectStorageClientProvider.get_client(
            username, region, api_key=api_key)

        #gets alternate(foreign) client using config values
        username = cls.config.identity_api.alt_username
        api_key = cls.config.identity_api.alt_api_key
        cls.alt_client = ObjectStorageClientProvider.get_client(
            username, region, api_key=api_key)

        #Creates an auth_client for adding and deleting subusers
        endpoint = cls.config.identity_api.authentication_endpoint
        auth_token = cls.client.auth_token
        cls.auth_client = IdentityClient(
            url=endpoint, serialize_format='json', deserialize_format='json',
            auth_token=auth_token)

        cls.filetools = filetools

    @classmethod
    def tearDownClass(cls):
        super(ObjectStorageTestFixture, cls).tearDownClass()


class CloudFilesTestFixture(BaseTestFixture):
    """
    Fixture provides all Cloud Files functionality
    """

    @classmethod
    def setUpClass(cls):
        super(CloudFilesTestFixture, cls).setUpClass()

        cls.atomhopper_provider = AtomHopperProvider(
            cls.config.object_storage_api.atom_feed_url, config=cls.config)

        username = cls.config.identity_api.username
        api_key = cls.config.identity_api.api_key
        region = cls.config.object_storage_api.region
        username = cls.config.identity_api.username

        cls.client = CloudFilesClientProvider.get_client(
            username, region, api_key=api_key)

        cls.filetools = filetools


class CloudFilesFixtureParameterized(BaseParameterizedTestFixture):
    """
    Super fixture provides all Cloud Files functionality in
    """

    @classmethod
    def setUpClass(cls):
        super(CloudFilesFixtureParameterized, cls).setUpClass()
        cls.client = ObjectStorageClientProvider.get_client(cls.config)
        cls.atomhopper_provider = AtomHopperProvider(
            cls.config.object_storage_api.atom_feed_url, config=cls.config)
