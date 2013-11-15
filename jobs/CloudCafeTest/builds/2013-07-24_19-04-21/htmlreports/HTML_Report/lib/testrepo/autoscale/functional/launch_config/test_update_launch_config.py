from testrepo.common.testfixtures.autoscale import ScalingGroupFixture
from ccengine.common.tools.datagen import rand_name


class UpdateLaunchConfigTest(ScalingGroupFixture):

    @classmethod
    def setUpClass(cls):
        super(UpdateLaunchConfigTest, cls).setUpClass()
        cls.lc_name = rand_name("upd_server_name")
        cls.lc_image_ref = 'XYZ'
        cls.lc_flavor_ref = 4
        cls.lc_load_balancers = [{'loadBalancerId': 1234, 'port': 8181}]
        cls.lc_disk_config = 'AUTO'
        cls.lc_personality = [{"path": '/root/.ssh/authorized_keys',
                               "contents": ("DQoiQSBjbG91ZCBkb2VzIG5vdCBrbm93IHdoeSBp")}]
        cls.lc_metadata = {'lc_meta_key_1': 'lc_meta_value_1',
                           'lc_meta_key_2': 'lc_meta_value_2'}
        cls.lc_networks = [{'uuid': '11111111-1111-1111-1111-111111111111'}]
        cls.update_lc_response = cls.autoscale_client.update_launch_config(
            group_id=cls.group.id,
            name=cls.lc_name,
            image_ref=cls.lc_image_ref,
            flavor_ref=cls.lc_flavor_ref,
            personality=cls.lc_personality,
            metadata=cls.lc_metadata,
            disk_config=cls.lc_disk_config,
            networks=cls.lc_networks,
            load_balancers=cls.lc_load_balancers)
        cls.update_lc = cls.update_lc_response.entity

    @classmethod
    def tearDownClass(cls):
        super(UpdateLaunchConfigTest, cls).tearDownClass()

    def test_update_launch_config_response(self):
        # headers = None                     # TBD
        launchconfig_response = self.autoscale_client.view_launch_config(self.group.id)
        updated_launchconfig = launchconfig_response.entity
        self.assertEquals(self.update_lc_response.status_code, 204,
                          msg="Update launch config failed with %s as against a 204"
                          % self.update_lc_response.status_code)
        self.assertTrue(self.update_lc_response.headers is not None,
                        msg="The headers are not as expected")
        self.validate_headers(self.update_lc_response.headers)
        self.assertEquals(updated_launchconfig.server.name, self.lc_name,
                          msg="Prefix/Suffix server name in the launch config did not update")
        self.assertEquals(updated_launchconfig.server.flavorRef, self.lc_flavor_ref,
                          msg="Server flavor in the launch config did not update")
        self.assertEquals(updated_launchconfig.server.imageRef, self.lc_image_ref,
                          msg="Server ImageRef in the launch config did not update")
        self.assertEquals(self.autoscale_provider.personality_list(updated_launchconfig.server.personality),
                          self.autoscale_provider.personality_list(self.lc_personality),
                          msg="Server personality in the launch config did not update")
        self.assertEquals(self.autoscale_provider.to_data(updated_launchconfig.server.metadata),
                          self.lc_metadata,
                          msg="Server metadata in the launch config did not update")
        self.assertEquals(self.autoscale_provider.network_uuid_list(updated_launchconfig.server.networks),
                          self.autoscale_provider.network_uuid_list(self.lc_networks),
                          msg="Server networks did not update")
        self.assertEquals(self.autoscale_provider.lbaas_list(updated_launchconfig.loadBalancers),
                          self.autoscale_provider.lbaas_list(self.lc_load_balancers),
                          msg="Load balancers in the launch config did not update")
