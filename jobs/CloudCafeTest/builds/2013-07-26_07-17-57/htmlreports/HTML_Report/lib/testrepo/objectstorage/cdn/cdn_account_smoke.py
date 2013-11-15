import unittest
from testrepo.common.testfixtures.object_storage_fixture import AccountFixture


class CDNAccountSmokeTest(AccountFixture):

    #TODO: fix the tests to account for 200 or 204 empty and non empty
    """Account Level Tests"""
    def test_list_cdn_containers(self):
        #whenever you cdn enable container a container, that container
        #name is forever registered as having been cdn enabled.
        #doing a get on the cdn url returns a list of cdn enabled container
        #names AND a containers names that were cdn enabled at one time
        container_name = self.cf_provider.generate_unique_container_name()

        x = self.cf_provider.client.create_container(container_name)
        self.assertEqual(x.status_code, 201)

        x = self.cf_provider.cdn_client.cdn_enable_container(container_name)
        self.assertEqual(x.status_code, 201)

        x = self.cf_provider.cdn_client.list_cdn_enabled_containers()
        self.assertEqual(x.status_code, 200)

        self.addCleanup(self.cf_provider.force_delete_containers,
                        [container_name])

    def test_list_cdn_containers_json(self):
        container_name = self.cf_provider.generate_unique_container_name()

        x = self.cf_provider.client.create_container(container_name)
        self.assertEqual(x.status_code, 201)

        x = self.cf_provider.cdn_client.cdn_enable_container(container_name)
        self.assertEqual(x.status_code, 201)

        params = {'format':'json'}
        x = self.cf_provider.cdn_client.list_cdn_enabled_containers(params=params)
        self.assertEqual(x.status_code, 200)

        self.addCleanup(self.cf_provider.force_delete_containers,
                        [container_name])

    def test_list_cdn_containers_xml(self):
        container_name = self.cf_provider.generate_unique_container_name()

        x = self.cf_provider.client.create_container(container_name)
        self.assertEqual(x.status_code, 201)

        x = self.cf_provider.cdn_client.cdn_enable_container(container_name)
        self.assertEqual(x.status_code, 201)

        params = {'format':'xml'}
        x = self.cf_provider.cdn_client.list_cdn_enabled_containers(params=params)
        self.assertEqual(x.status_code, 200)

        self.addCleanup(self.cf_provider.force_delete_containers,
                        [container_name])

    def test_list_cdn_containers_limit(self):
        container_name = self.cf_provider.generate_unique_container_name()

        x = self.cf_provider.client.create_container(container_name)
        self.assertEqual(x.status_code, 201)

        x = self.cf_provider.cdn_client.cdn_enable_container(container_name)
        self.assertEqual(x.status_code, 201)

        params = {'limit':'10'}
        x = self.cf_provider.cdn_client.list_cdn_enabled_containers(params=params)
        self.assertEqual(x.status_code, 200)

        self.addCleanup(self.cf_provider.force_delete_containers,
                        [container_name])

    def test_list_cdn_containers_marker(self):
        container_name = self.cf_provider.generate_unique_container_name()

        x = self.cf_provider.client.create_container(container_name)
        self.assertEqual(x.status_code, 201)

        x = self.cf_provider.cdn_client.cdn_enable_container(container_name)
        self.assertEqual(x.status_code, 201)

        params = {'marker':'c'}
        x = self.cf_provider.cdn_client.list_cdn_enabled_containers(params=params)
        self.assertEqual(x.status_code, 200)

        self.addCleanup(self.cf_provider.force_delete_containers,
                        [container_name])

    def test_list_cdn_containers_enabled_only(self):
        #sending enabled_only:true returns a list of container names that
        #are currently cdn enabled
        container_name = self.cf_provider.generate_unique_container_name()

        x = self.cf_provider.client.create_container(container_name)
        self.assertEqual(x.status_code, 201)

        x = self.cf_provider.cdn_client.cdn_enable_container(container_name)
        self.assertEqual(x.status_code, 201)

        params = {'enabled_only':'true'}
        x = self.cf_provider.cdn_client.list_cdn_enabled_containers(params=params)
        self.assertEqual(x.status_code, 200)

        self.addCleanup(self.cf_provider.force_delete_containers,
                        [container_name])
