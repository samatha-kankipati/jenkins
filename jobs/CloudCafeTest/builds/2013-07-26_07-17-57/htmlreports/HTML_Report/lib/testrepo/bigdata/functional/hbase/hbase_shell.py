'''
@summary: Running HBASE Shell
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from ccengine.providers.bigdata.lava_api import LavaAPIProvider as _LavaAPIProvider
from ccengine.clients.bigdata.hbase_shell_client import HbaseShellClient
from testrepo.bigdata.functional.lava_base_fixture import LavaBaseFixture

class HbaseShellTest(LavaBaseFixture):

    def test_hbase_shell(self):
        master_node = self.lava_provider.get_node_with_role(self.cluster,
                                                            "NAMENODE")
        hbase_shell_client = HbaseShellClient(self.config, master_node)
        response = hbase_shell_client.start_hbase_shell()
        self.assertIn('Type "exit<RETURN>" to leave the HBase Shell',
                      response,
                      "Did not successfully create an HBase Shell for %s"
                      % master_node)
        response = hbase_shell_client.run_command('status')
        self.assertIn('0 dead', response,
                      "Hbase Status has some dead nodes: %s"
                      % response)

        response = hbase_shell_client.run_command('create', "'t1', 'f1', 'f2'")
        self.assertIn('0 row(s)', response,
                      "Could not create 't1', 'f1', 'f2' %s" % response)

        response = hbase_shell_client.run_command('describe', "'t1'")
        self.assertIn('ENABLED', response,
                      "'t1' not described as ENABLED: %s" % response)




