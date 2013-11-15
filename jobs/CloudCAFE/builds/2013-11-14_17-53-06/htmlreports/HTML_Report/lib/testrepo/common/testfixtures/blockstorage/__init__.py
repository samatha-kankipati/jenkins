'''
EVERYTHING IN HERE IS LEGACY CODE AND DEPRECATED.  DO NOT USE OR IMPORT IT
'''
from testrepo.common.testfixtures.fixtures import\
    BaseTestFixture as _BaseTestFixture,\
    BaseParameterizedTestFixture as _BaseParameterizedTestFixture
from ccengine.providers.blockstorage.lunr_api import LunrAPIProvider as\
    _LunrAPIProvider
from ccengine.providers.blockstorage.storage_node_api import\
    StorageNodeAPIProvider as _StorageNodeAPIProvider
from ccengine.providers.blockstorage.volumes_api import VolumesAPIProvider as\
    _VolumesAPIProvider


class LunrAPIFixture(_BaseTestFixture):
    @classmethod
    def setUpClass(cls):
        super(LunrAPIFixture, cls).setUpClass()
        #init providers
        cls.LunrAPIProvider = _LunrAPIProvider(cls.config.lunr_api)

        #Breakout Lunr clients
        cls.user_client = cls.LunrAPIProvider.lunr_api_client
        cls.admin_client = cls.LunrAPIProvider.lunr_api_admin_client


class StorageNodeAPIFixture(LunrAPIFixture):
    @classmethod
    def setUpClass(cls):
        super(StorageNodeAPIFixture, cls).setUpClass()
        cls.StorageNodeAPIProvider = _StorageNodeAPIProvider(cls.config)

        #List storage nodes
        storage_node_list = cls.LunrAPIProvider.list_storage_nodes()

        #Create SNAPI Clients
        cls.snapi_clients = []
        for node in storage_node_list:
            cls.snapi_clients.append(
                cls.StorageNodeAPIProvider.create_snapi_client(node))

        #Volumes cleanup dict
        cls.expected_volumes = {}


class VolumesAPI_ParameterizedFixture(_BaseParameterizedTestFixture):
    '''
    @summary: Foundation for any Paramaterized Cinder API Tests.
              Creates instance of VolumesAPIProvider and reference its
              volumes_client.
    @cvar volumes_api_provider: Provider instance for the Volumes API
    @type volumes_api_provider: L{VolumesAPIProvider}
    @cvar volumes_client: Client instance for the Volumes API
    @type volumes_client: L{VolumesAPIProvider}
    '''
    @classmethod
    def setUpClass(cls):
        super(VolumesAPI_ParameterizedFixture, cls).setUpClass()
        cls.volumes_api_provider = _VolumesAPIProvider(cls.config)
        cls.volumes_client = cls.volumes_api_provider.volumes_client
