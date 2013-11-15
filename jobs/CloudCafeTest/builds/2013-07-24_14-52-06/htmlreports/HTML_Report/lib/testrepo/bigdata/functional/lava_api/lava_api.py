'''
@summary: Tests Lava (Big Data) REST API
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from ccengine.common.connectors import rest
from testrepo.common.testfixtures.fixtures import BaseParameterizedTestFixture
from ccengine.providers.bigdata.lava_api import LavaAPIProvider as _LavaAPIProvider
from ccengine.providers.bigdata.hadoop_provider import HadoopProvider as _HadoopProvider
from ccengine.domain.bigdata.lava import Node as _Node, Flavor as _Flavor
from ccengine.domain.types import LavaClusterStatusTypes as _LavaClusterStatusTypes
from ccengine.common.connectors.ping import PingClient
from testrepo.bigdata.functional.lava_base_fixture import LavaBaseFixture

class LavaAPITest(LavaBaseFixture):
    '''
    @summary: Functional Tests for Lava API
    '''

        