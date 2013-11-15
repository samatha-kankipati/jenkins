import unittest
from testrepo.common.testfixtures.object_storage_fixture import ContainerFixture

class cdnContainerSmokeTest(ContainerFixture):

    """Container Level Tests"""
    def test_cdn_enable_container(self):
        container_name = self.cf_provider.generate_unique_container_name()

        x = self.cf_provider.client.create_container(container_name)
        self.assertEqual(x.status_code, 201)

        x = self.cf_provider.cdn_client.cdn_enable_container(container_name)
        self.assertEqual(x.status_code, 201)

        x = self.cf_provider.cdn_client.cdn_enable_container(container_name)
        self.assertEqual(x.status_code, 202)

        x = self.cf_provider.client.delete_container(container_name)
        self.assertEqual(x.status_code, 204)

        self.addCleanup(self.cf_provider.force_delete_containers,
                        [container_name])

    def test_cdn_disable_container(self):
        container_name = self.cf_provider.generate_unique_container_name()

        x = self.cf_provider.client.create_container(container_name)
        self.assertEqual(x.status_code, 201)

        x = self.cf_provider.cdn_client.cdn_enable_container(container_name)
        self.assertEqual(x.status_code, 201)

        x = self.cf_provider.cdn_client.cdn_enable_container(container_name)
        self.assertEqual(x.status_code, 202)

        x = self.cf_provider.client.delete_container(container_name)
        self.assertEqual(x.status_code, 204)

        self.addCleanup(self.cf_provider.force_delete_containers,
                        [container_name])

    def test_cdn_enable_container_set_TTL(self):
        container_list = []

        container_name = self.cf_provider.generate_unique_container_name()
        container_list[len(container_list):] = [container_name]

        x = self.cf_provider.client.create_container(container_name)
        self.assertEqual(x.status_code, 201)

        headers = {'X-TTL':'900'}
        x = self.cf_provider.cdn_client.cdn_enable_container(container_name,
                                                                headers=headers)
        self.assertEqual(x.status_code, 201)

        container_name = self.cf_provider.generate_unique_container_name()
        container_list[len(container_list):] = [container_name]

        x = self.cf_provider.client.create_container(container_name)
        self.assertEqual(x.status_code, 201)

        headers = {'X-TTL':'1576800000'}
        x = self.cf_provider.cdn_client.cdn_enable_container(container_name,
                                                                headers=headers)
        self.assertEqual(x.status_code, 201)

        self.addCleanup(self.cf_provider.force_delete_containers, container_list)
