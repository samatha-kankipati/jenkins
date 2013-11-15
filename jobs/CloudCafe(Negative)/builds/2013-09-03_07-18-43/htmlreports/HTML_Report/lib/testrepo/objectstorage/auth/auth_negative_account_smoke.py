from testrepo.common.testfixtures.object_storage_fixture \
        import ObjectStorageTestFixture
from ccengine.providers.objectstorage.object_storage_provider \
        import ObjectStorageClientProvider
from ccengine.clients.objectstorage.object_storage_client \
        import ObjectStorageAPIClient


"""4.1 Auth Storage Account Services Negative Smoke Tests"""


class AuthNegativeAccountSmokeTest(ObjectStorageTestFixture):
    @classmethod
    def setUpClass(cls):
        super(AuthNegativeAccountSmokeTest, cls).setUpClass()

        alt_config = cls.config
        v = {
            'identity': {
                'username': cls.config.identity_api.alt_username,
                'api_key': cls.config.identity_api.alt_api_key
            }
        }
        alt_config = alt_config.mcp_override(v)
        cls.alt_client = ObjectStorageClientProvider.get_client(alt_config)

    """4.1.1. List Containers"""
    def test_container_list_fails_with_valid_foreign_api_key(self):
        storage_url = self.client.storage_url
        cross_auth_token = self.alt_client.auth_token
        cross_client = ObjectStorageAPIClient(storage_url, cross_auth_token)

        r = cross_client.list_containers()
        self.assertEqual(r.status_code, 401, 'should not list containers')

    """4.1.1.1. Serialized List Output"""

    """4.1.1.2. Controlling a Large List of Containers"""

    """4.1.2. Retrieve Account Metadata"""

    def test_metadata_retrieval_fails_with_valid_foreign_api_key(self):
        storage_url = self.client.storage_url
        cross_auth_token = self.alt_client.auth_token
        cross_client = ObjectStorageAPIClient(storage_url, cross_auth_token)

        r = cross_client.retrieve_account_metadata()
        self.assertEqual(r.status_code, 401, 'should not list containers')
