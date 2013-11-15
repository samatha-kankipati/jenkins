from testrepo.common.testfixtures.compute import ComputeFixture
from ccengine.common.exceptions.compute import OverLimit
from ccengine.common.tools.datagen import rand_name
from ccengine.common.decorators import attr
import time


class AbsoluteLimitsTest(ComputeFixture):

    @classmethod
    def setUpClass(cls):
        super(AbsoluteLimitsTest, cls).setUpClass()
        cls.max_ram_available = int(cls.compute_provider_for_low_limits_user.limits_client.get_max_total_RAM_size())
        cls.instance_limit = int(cls.compute_provider_for_low_limits_user.limits_client.get_max_total_instances())

        num_instances = 3 if cls.instance_limit > 3 else (cls.instance_limit / 2)
        min_ram_reqd = (cls.max_ram_available) / num_instances
        flavor_list = cls.compute_provider_for_low_limits_user.flavors_client.list_flavors_with_detail(min_ram=min_ram_reqd)
        cls.flavor_max_ram_id = flavor_list.entity[0].id

    @classmethod
    def tearDownClass(cls):
        cls.resources.release()
        time.sleep(10)

    @attr(type='limits', net='yes')
    def test_can_not_create_servers_exceeding_max_instance_limit(self):
        """A create server request exceeding the max instance quota limit should fail with an OverLimit exception"""
        servers_response_list = self.compute_provider_for_low_limits_user.servers_client.list_servers_with_detail()
        existing_servers_list = servers_response_list.entity

        number_of_servers_that_can_be_built = self.instance_limit - len(existing_servers_list)

        'Creating servers to fill up the instance limit'
        for _ in range(number_of_servers_that_can_be_built):
            server_response = self.compute_provider_for_low_limits_user.servers_client.create_server(name=rand_name(), image_ref=self.image_ref, flavor_ref=self.flavor_ref)
            self.resources.add(server_response.entity.id, self.compute_provider_for_low_limits_user.wait_for_server_to_be_deleted)
        with self.assertRaises(OverLimit):
            self.compute_provider_for_low_limits_user.create_active_server()

    @attr(type='limits', net='yes')
    def test_can_not_create_servers_exceeding_max_RAM_size_limit(self):
        """A create server request exceeding the max RAM size should fail with an OverLimit exception"""
        total_ram_used = int(self.compute_provider_for_low_limits_user.limits_client.get_total_RAM_used())
        total_ram_available = self.max_ram_available - total_ram_used

        flavor_alt_response = self.compute_provider_for_low_limits_user.flavors_client.get_flavor_details(self.flavor_max_ram_id)
        number_of_servers_can_be_created = total_ram_available / int(flavor_alt_response.entity.ram)
        for _ in range(number_of_servers_can_be_created):
            server_response = self.compute_provider_for_low_limits_user.servers_client.create_server(name=rand_name(), image_ref=self.image_ref, flavor_ref=self.flavor_max_ram_id)
            self.resources.add(server_response.entity.id, self.compute_provider_for_low_limits_user.wait_for_server_to_be_deleted)
        with self.assertRaises(OverLimit):
            self.compute_provider_for_low_limits_user.create_active_server(flavor_ref=self.flavor_max_ram_id)
