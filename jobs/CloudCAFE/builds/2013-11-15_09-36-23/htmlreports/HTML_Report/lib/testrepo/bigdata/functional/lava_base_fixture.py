from testrepo.common.testfixtures.fixtures import BaseParameterizedTestFixture
from ccengine.providers.bigdata.lava_api import LavaAPIProvider as _LavaAPIProvider
from ccengine.domain.types import LavaClusterStatusTypes as _LavaClusterStatusTypes
from ccengine.common.connectors.ping import PingClient
from ccengine.providers.bigdata.hadoop_provider import HadoopProvider as _HadoopProvider

class LavaBaseFixture(BaseParameterizedTestFixture):
    @classmethod
    def setUpClass(cls):
        super(LavaBaseFixture, cls).setUpClass()
        cls.lava_provider = _LavaAPIProvider(cls.config)
        cls.lava_client =  cls.lava_provider.lava_client
        cls.lava_admin_client = cls.lava_provider.lava_admin_client
        
    def setUp(self):
        super(LavaBaseFixture,self).setUp()
        '''
        Not good object oriented programming at all!
        Should split the common code properly so that generic code doesnt check
        for test specific code.
        NEED TO BE FIXED!
        '''
        if self.__dict__.has_key("cluster_name") and \
        self._testMethodName != "test_add_cluster" and  \
        self._testMethodName != "test_error_messages_for_cluster_create":
            self.cluster = self.lava_provider.get_cluster(self.cluster_name)
            self.assertTrue(self.cluster != None,
                            "%s not created"%(self.cluster_name))
            self.assertEqual(self.cluster.status, 
                     _LavaClusterStatusTypes.ACTIVE, 
                     "Cluster '%s' created returned with status %s. Cluster: %s"
                      % (self.cluster_name, 
                         self.cluster.status, 
                         self.cluster))
            
            
            