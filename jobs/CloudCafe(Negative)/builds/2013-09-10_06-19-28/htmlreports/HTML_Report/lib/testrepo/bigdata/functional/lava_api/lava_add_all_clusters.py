'''
@summary: Tests Lava (Big Data) REST API
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
import json
from testrepo.common.testfixtures.fixtures import BaseTestFixture
from ccengine.providers.bigdata.lava_api import LavaAPIProvider as \
        _LavaAPIProvider
from ccengine.domain.bigdata.lava import Flavor as _Flavor


class LavaAddClusterTest(BaseTestFixture):
    '''
    @summary: Basic smoke test for Big Data REST API
    '''

    @classmethod
    def setUpClass(cls):
        super(LavaAddClusterTest, cls).setUpClass()

        cls.lava_provider = _LavaAPIProvider(cls.config)
        cls.lava_client = cls.lava_provider.lava_client
        cluster_flavor_list = json.loads(cls.lava_client.Flavors.list().content)['flavors']
        cls.flavor_domain_objects = cls.lava_provider.convert_json_to_domain_object_list(cluster_flavor_list, _Flavor)
        cls.count = 2

    @classmethod
    def tearDownClass(cls):
        super(LavaAddClusterTest, cls).tearDownClass()

    def test_add_all_cluster_flavor_types(self):
        for cluster_flavor in self.flavor_domain_objects:
            '''@note: Issue #249. Can't create xlarge clusters on Lab'''
            if int(cluster_flavor.id) != 5:
                created_cluster_list = self.lava_provider.concurrent_cluster_create(int(cluster_flavor.id))
                self.lava_provider.delete_active_clusters(self.lava_client, created_cluster_list)
