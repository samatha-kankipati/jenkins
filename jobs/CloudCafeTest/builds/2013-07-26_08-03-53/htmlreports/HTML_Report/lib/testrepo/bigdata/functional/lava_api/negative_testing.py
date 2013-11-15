
from testrepo.common.testfixtures.fixtures import BaseParameterizedTestFixture
from ccengine.clients.bigdata.lava_api_client import LavaAPIClient
from testrepo.bigdata.functional.lava_base_fixture import LavaBaseFixture
from ccengine.domain.types import LavaClusterTypes
from ccengine.domain.bigdata.lava import Cluster as _Cluster, \
    Node as _Node, Type as _Type, Flavor as _Flavor
from ccengine.domain.types import LavaClusterStatusTypes \
    as _LavaClusterStatusTypes
from ccengine.domain.bigdata.lava import CloudCredentials, SSHKey
from ccengine.clients.auth.auth_client import AuthClient as _AuthClient
from ccengine.domain.auth import Auth_2_0 as _Auth_2_0_DomainObject
from ccengine.domain.bigdata.lava import Node as _Node, Flavor as _Flavor, \
    Type as _Type, CloudCredentials as _CloudCredentials, SSHKey as _SSHKey
from ccengine.providers.bigdata.hadoop_provider import HadoopProvider as _HadoopProvider


from unittest2.suite import TestSuite
import json
import random


class ErrorMessageTest(LavaBaseFixture):

    @classmethod
    def setUpClass(cls):
        super(ErrorMessageTest, cls).setUpClass()
        cls.alt_username = cls.config.auth.alt_username
        cls.alt_password = cls.config.auth.alt_password
        cls.alt_api_key = cls.config.auth.alt_api_key
        cls.alt_tenant_id = cls.config.auth.alt_tenant_id
        cls.alt_user_id = cls.config.auth.alt_user_id
        cls.alt_base_url = "{0}{1}/".format(
            cls.config.lava_api.BASE_URL,
            cls.config.auth.alt_tenant_id)

    def test_no_proxy_node_web_pages(self):
        cluster = self.lava_provider.get_cluster(self.cluster_name)
        hadoop_provider = _HadoopProvider(self.config, cluster)

        self.assertFalse(hadoop_provider.verify_master_dfs_health_check(
            proxy_url=None,
            proxy_port=None,
            timeout=int(self.config.lava_api.HADOOP_WEB_PAGE_TIMEOUT)),
            "DFS Health page success launch")
        self.assertFalse(hadoop_provider.verify_job_tracker_page(
            proxy_url=None,
            proxy_port=None,
            timeout=int(self.config.lava_api.HADOOP_WEB_PAGE_TIMEOUT)),
            "Job Tracker page success launch.")
        for node in self.lava_provider.get_cluster_nodes(self.cluster):
            if str(node.role) != "NAMENODE" and \
                    str(node.role) != "GATEWAY":
                self.assertFalse(hadoop_provider.verify_task_tracker(
                    node, proxy_url=None,
                    proxy_port=None,
                    timeout=int(self.config.lava_api.HADOOP_WEB_PAGE_TIMEOUT)),
                    "{0} Success task tracker".format(
                    node.private_ip)
                )

    def test_error_messages_for_cluster_create(self):
        '''
        Need to check for response code .. add cases to include missing fields
        400 -  invalid name, invalid count, invalid type, invalid flavor
               and blanking out all the fields
        '''
        flavor_id = self.lava_provider.get_flavor_id(str(self.flavor))
        if flavor_id is None:
            flavor_id = self.flavor
        lava_client = self.lava_provider.lava_client
        response = lava_client.Clusters.create(
            self.name, self.count, self.type, self.flavor)
        self.assertTrue(response.status_code == 400,
                        "Expected status code: 400 Returned content:#{0}"
                        .format(response.content))

    def test_invalid_password(self):
        invalid_password_message = "Password must be between 8-255 "
        "characters, include at        least one upper case,"
        " one lower case one digit and one special        character"
        auth_client = _AuthClient(self.config.auth.base_url,
                                  self.config.auth.version,
                                  self.alt_username,
                                  self.alt_password,
                                  self.alt_api_key)
        response = auth_client.auth_2_0()
        if not response.ok:
            self.fixture_log.error('Quick Auth 2.0 recieved a negative \
                                   response from auth')
        ResponseDict = json.loads(response.content)
        auth_data = _Auth_2_0_DomainObject(ResponseDict)
        lava_client = LavaAPIClient(self.alt_base_url,
                                    auth_data.token.id)
        profiles_client = lava_client.Profiles
        api_response = profiles_client.edit(
            username=self.config.lava_api.USER_NAME,
            password=self.prof_password)
        self.assertTrue(api_response.status_code == 400,
                        "Clusters status expected: 400, recieved: #{0}".format(
                            api_response.content))
        self.assertTrue(
            api_response.content.find(invalid_password_message) != -1,
            "Message expected: #{0}, recieved: #{1}"
                        .format(invalid_password_message,
                                api_response.content))

    def test_no_profile_for_cluster_create(self):
        auth_client = _AuthClient(self.config.auth.base_url,
                                  self.config.auth.version,
                                  self.alt_username,
                                  self.alt_password,
                                  self.alt_api_key)
        response = auth_client.auth_2_0()
        if not response.ok:
            self.fixture_log.error('Quick Auth 2.0 recieved a negative \
                                   response from auth')
        ResponseDict = json.loads(response.content)
        auth_data = _Auth_2_0_DomainObject(ResponseDict)
        lava_client = LavaAPIClient(self.alt_base_url,
                                    auth_data.token.id)

        # Delete Profile if it exists already
        result = self.lava_provider.delete_profile(
            self.alt_username,
            self.alt_password,
            self.alt_api_key,
            self.alt_user_id,
            self.alt_tenant_id)
        self.assertTrue(result,
                        "Profile delete failed")

        # Create Cluster
        temp_name = "temp" + str(random.randint(0, 100))
        api_response = lava_client.Clusters.create\
            (temp_name, 2, LavaClusterTypes.HADOOP_HDP, 3)
        self.assertTrue(api_response.status_code == 400,
                        "Clusters status expected: 400, recieved: %s %s"
                        % (api_response.status_code, api_response.content))

    def test_default_repl_count_for_profile(self):
        '''
        Hard Coded credentials.. need to get rid of them!
        Factory style client creation inside the providers is the optimum
        way to do this.
        '''
        auth_client = _AuthClient(self.config.auth.base_url,
                                  self.config.auth.version,
                                  self.alt_username,
                                  self.alt_password,
                                  self.alt_api_key)
        response = auth_client.auth_2_0()
        if not response.ok:
            self.fixture_log.error('Quick Auth 2.0 recieved a negative \
                                   response from auth')
        ResponseDict = json.loads(response.content)
        auth_data = _Auth_2_0_DomainObject(ResponseDict)
        lava_client = LavaAPIClient(self.alt_base_url,
                                    auth_data.token.id)
        # Delete Profile if it exists already
        result = self.lava_provider.delete_profile(
            self.alt_username, self.alt_password,
            self.alt_api_key, self.alt_user_id,
            self.alt_tenant_id)
        self.assertTrue(result,
                        "Profile delete failed")

        # Create profile again
        ccs = CloudCredentials(self.alt_username, self.alt_api_key)
        profiles_client = lava_client.Profiles
        api_response = profiles_client.edit(
            username=self.config.lava_api.USER_NAME,
            password=self.config.lava_api.PASSWORD,
            cloud_credentials=ccs)
        # Create Cluster
        api_response = lava_client.Clusters.create\
            ("temp", 3, LavaClusterTypes.HADOOP_HDP, 3)
        self.assertTrue(api_response.status_code == 413,
                        "Clusters status expected: 413, recieved: %s %s"
                        % (api_response.status_code, api_response.content))

    def test_unauthorized_calls(self):
        '''
        test all the calls for 401
        @pre-reqs: assumes there is a valid cluster and a profile already
                   created
        '''

        # Get details for one cluster
        cluster = self.lava_provider.get_cluster(self.cluster_name)
        nodes = self.lava_provider.get_cluster_nodes(cluster)
        lava_client = LavaAPIClient(self.alt_base_url, "")
        # Get Cluster
        api_response = lava_client.Clusters.get_info(cluster.id)
        self.assertTrue(api_response.status_code == 401,
                        "Clusters status expected: 401, recieved: %s"
                        % api_response.status_code)
        # Create Cluster
        api_response = lava_client.Clusters.create("temp", 2,
                                                   LavaClusterTypes.HADOOP_HDP,
                                                   3)
        # Delete Cluster
        api_response = lava_client.Clusters.delete(cluster.id)
        self.assertTrue(api_response.status_code == 401,
                        "Clusters status expected: 401, recieved: %s"
                        % api_response.status_code)
        # List nodes for cluster
        api_response = api_response = lava_client.Clusters.list_nodes\
            (cluster.id)
        self.assertTrue(api_response.status_code == 401,
                        "Clusters status expected: 401, recieved: %s"
                        % api_response.status_code)
        # Get node in a cluster
        for node in nodes:
            api_response = lava_client.Clusters.get_node(cluster.id, node.id)
            self.assertTrue(api_response.status_code == 401,
                            "Clusters status expected: 401, recieved: %s"
                            % api_response.status_code)

        # Update profile
        ccs = CloudCredentials(self.alt_username,
                               self.alt_api_key)
        profiles_client = lava_client.Profiles
        api_response = profiles_client.edit(
            username=self.config.lava_api.USER_NAME,
            password=self.config.lava_api.PASSWORD,
            cloud_credentials=ccs)
        self.assertTrue(api_response.status_code == 401,
                        "Clusters status expected: 401, recieved: %s"
                        % api_response.status_code)
        # Delete Profile
        api_response = profiles_client.delete(user_id=self.alt_user_id)
        self.assertTrue(api_response.status_code == 401,
                        "Clusters status expected: 401, recieved: %s"
                        % api_response.status_code)

    def test_invalid_cluster_id(self):
        invalid_cluster_id = "vfdkgj557t57thhgthgyh"
        invalid_node_id = "ewfnrgjrbgjtgrreg"
        api_response = self.lava_client.Clusters.\
            get_info(invalid_cluster_id)
        self.assertTrue(api_response.status_code == 404,
                        "Clusters status expected: 404, recieved: %s"
                        % api_response.status_code)
        api_response = self.lava_client.Clusters.\
            list_nodes(invalid_cluster_id)
        self.assertTrue(api_response.status_code == 404,
                        "Clusters status expected: 404, recieved: %s"
                        % api_response.status_code)
        api_response = self.lava_client.Clusters.\
            get_node(invalid_cluster_id, invalid_node_id)
        self.assertTrue(api_response.status_code == 404,
                        "Clusters status expected: 404, recieved: %s"
                        % api_response.status_code)
        api_response = self.lava_client.Clusters.\
            delete(invalid_cluster_id)
        self.assertTrue(api_response.status_code == 404,
                        "Clusters status expected: 404, recieved: %s"
                        % api_response.status_code)
        api_response = self.lava_client.Clusters.\
            resize(invalid_cluster_id, 3)
        self.assertTrue(api_response.status_code == 404,
                        "Clusters status expected: 404, recieved: %s"
                        % api_response.status_code)

    def test_error_messages_for_resize_cluster(self):
        '''
        Cluster resize negative testing
        401 - Unauthorized
        400 - invalid cluster id, invalid size, missing both the fields
        '''
        new_size = self.new_size
        cluster_name = self.cluster_name
        exp_error = ""
        cluster = self.lava_provider.get_cluster(cluster_name)
        api_response = self.lava_client.Clusters.resize(cluster.id, new_size)
        self.assertTrue(api_response.status_code == 400,
                        "Expected status code: 400 Returned content:#{0}"
                        .format(api_response.content))
