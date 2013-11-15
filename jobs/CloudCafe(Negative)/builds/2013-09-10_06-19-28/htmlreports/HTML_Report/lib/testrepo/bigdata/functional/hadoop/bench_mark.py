'''
@summary: Hive Job test for Cluster Nodes
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from ccengine.providers.bigdata.hadoop_provider import HadoopProvider
from testrepo.bigdata.functional.lava_base_fixture import LavaBaseFixture


class BenchMarkTests(LavaBaseFixture):

    def test_tera_sort(self):
        hadoop_provider = HadoopProvider(self.config, self.cluster)
        result, msg = hadoop_provider.run_max_tera_sort()
        self.assertTrue(result,msg)
        
        
        
        
