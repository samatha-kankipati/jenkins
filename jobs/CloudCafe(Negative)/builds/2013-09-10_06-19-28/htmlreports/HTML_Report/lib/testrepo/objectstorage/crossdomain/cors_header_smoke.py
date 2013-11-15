import unittest

from testrepo.common.testfixtures.object_storage_fixture \
        import ObjectStorageTestFixture
from ccengine.common.connectors import rest
from ccengine.common.decorators import attr


class CorsHeaderSmokeTest(ObjectStorageTestFixture):

    @classmethod
    def setUpClass(cls):
        super(CorsHeaderSmokeTest, cls).setUpClass()
        cls.cors_headers = []
        cls.cors_allow_origin = 'Access-Control-Allow-Origin'
        cls.cors_allow_headers = 'Access-Control-Allow-Headers'
        cls.cors_max_age = 'Access-Control-Max-Age'
        cls.cors_allow_methods = 'Access-Control-Allow-Methods'
        cls.containers = []
        cls.storage_objects = []

    @classmethod
    def tearDownClass(cls):
        super(CorsHeaderSmokeTest, cls).tearDownClass()

    def setUp(self):
        #Create container
        self.testcontainer_name = self.client.generate_unique_container_name()
        resp = self.client.create_container(self.testcontainer_name)
        assert resp.ok, 'Container create in setup failed'
        self.containers.append(self.testcontainer_name)

    def tearDown(self):
        #Create container
        for container_name, object_name in self.storage_objects:
            self.client.delete_storage_object(container_name, object_name)

        for container_name in self.containers:
            self.client.delete_container(container_name)

    @attr('negative')
    def test_negative_set_cors_headers_without_x_container_meta_prefix(self):
        headers = {}

        #Set headers
        headers[self.cors_allow_origin] = '*'
        headers[self.cors_allow_headers] = '*'
        headers[self.cors_max_age] = '*'

        resp = self.client.set_container_metadata(self.testcontainer_name,
                metadata=None, headers=headers)
        assert resp.ok, 'Unable to set cors headers'

        #Verify that header was set
        resp = self.client.get_container_metadata(self.testcontainer_name)
        assert resp.ok, 'Unable to verify cors header is set'
        assert self.cors_allow_origin not in resp.headers, \
                'CORS %s header accepted without x-container-meta prefix' % \
                str(self.cors_allow_origin)
        assert self.cors_allow_headers not in resp.headers, \
                'CORS %s header accepted without x-container-meta prefix' % \
                str(self.cors_allow_headers)
        assert self.cors_max_age not in resp.headers, \
                'CORS %s header accepted without x-container-meta prefix' % \
                str(self.cors_max_age)

    @attr('negative')
    def test_negative_options_request_on_cors_origin_restricted_container(self):
        metadata = {}

        #Set metadata
        metadata[self.cors_allow_origin] = 'http://goodhost.com'

        resp = self.client.set_container_metadata(self.testcontainer_name,
                metadata=metadata)
        assert resp.ok, 'Unable to set cors headers'

        #Verify that header was set
        resp = self.client.get_container_metadata(self.testcontainer_name)
        assert resp.ok, 'Unable to verify cors header is set'
        assert 'x-container-meta-' + self.cors_allow_origin in resp.headers, \
                'CORS %s header was not accepted with ' \
                'x-container-meta prefix' % \
                str('x-container-meta-' + self.cors_allow_origin)

        #Perform OPTIONS request
        headers = {}
        headers['origin'] = 'http://badhost'
        headers['Access-Control-Request-Method'] = 'GET'
        resp = self.client.get_container_options(self.testcontainer_name,
                headers=headers)
        assert not resp.ok, 'Unallowed origin OPTIONS request against cors ' \
                'restricted container was allowed to succeed (HTTP %s)' % \
                resp.status_code

    @attr('negative')
    def test_options_request_on_cors_origin_unrestricted_container_full_host_name_no_request_method_header(self):
        metadata = {}

        #Set metadata
        metadata[self.cors_allow_origin] = '*'

        resp = self.client.set_container_metadata(self.testcontainer_name,
                metadata=metadata)
        assert resp.ok, 'Unable to set cors headers'

        #Verify that header was set
        resp = self.client.get_container_metadata(self.testcontainer_name)
        assert resp.ok, 'Unable to verify cors header is set'
        assert 'x-container-meta-' + self.cors_allow_origin in resp.headers, \
                'CORS %s header was not accepted with ' \
                'x-container-meta prefix' % \
                str('x-container-meta-' + self.cors_allow_origin)
        assert resp.headers['x-container-meta-' + self.cors_allow_origin] == \
                '*', 'CORS header was not set properly'

        #Perform OPTIONS request
        headers = {}
        headers['origin'] = 'http://hurfasaur.us'
        resp = self.client.get_container_options(self.testcontainer_name,
                headers=headers)
        assert not resp.ok, 'Unable to perform OPTIONS request against cors ' \
                'unrestricted container (HTTP %S)' % resp.status_code

    def test_set_cors_headers_with_x_container_meta_prefix(self):
        metadata = {}

        #Set metadata
        metadata[self.cors_allow_origin] = '*'
        metadata[self.cors_allow_headers] = '*'
        metadata[self.cors_max_age] = '*'

        resp = self.client.set_container_metadata(self.testcontainer_name,
                metadata=metadata)
        assert resp.ok, 'Unable to set cors headers'

        #Verify that header was set
        resp = self.client.get_container_metadata(self.testcontainer_name)
        assert resp.ok, 'Unable to verify cors header is set'
        assert 'x-container-meta-' + self.cors_allow_origin in resp.headers, \
                'CORS %s header was not accepted with ' \
                'x-container-meta prefix' % \
                str('x-container-meta-' + self.cors_allow_origin)
        assert 'x-container-meta-' + self.cors_allow_headers in resp.headers, \
                'CORS %s header was not accepted with ' \
                'x-container-meta prefix' % \
                str('x-container-meta-' + self.cors_allow_headers)
        assert 'x-container-meta-' + self.cors_max_age in resp.headers, \
                'CORS %s header was not accepted with ' \
                'x-container-meta prefix' % \
                str('x-container-meta-' + self.cors_max_age)

    def test_options_request_on_cors_origin_unrestricted_container_full_host_name(self):
        metadata = {}

        #Set metadata
        metadata[self.cors_allow_origin] = '*'

        resp = self.client.set_container_metadata(self.testcontainer_name,
                metadata=metadata)
        assert resp.ok, 'Unable to set cors headers'

        #Verify that header was set
        resp = self.client.get_container_metadata(self.testcontainer_name)
        assert resp.ok, 'Unable to verify cors header is set'
        assert 'x-container-meta-' + self.cors_allow_origin in resp.headers, \
                'CORS %s header was not accepted with '\
                'x-container-meta prefix' % \
                str('x-container-meta-' + self.cors_allow_origin)
        assert resp.headers['x-container-meta-' + self.cors_allow_origin] == \
                '*', 'CORS header was not set properly'

        #Perform OPTIONS request
        headers = {}
        headers['origin'] = 'http://hurfasaur.us'
        headers['Access-Control-Request-Method'] = 'HEAD'
        resp = self.client.get_container_options(self.testcontainer_name,
                headers=headers)
        assert resp.ok, 'Unable to perform OPTIONS request against cors ' \
                'unrestricted container (HTTP %s)' % resp.status_code

    def test_options_request_on_cors_origin_restricted_container_full_host_name(self):
        metadata = {}

        #Set metadata
        allowed_origin = 'http://hurfasaur.us'
        metadata[self.cors_allow_origin] = allowed_origin

        resp = self.client.set_container_metadata(self.testcontainer_name,
                metadata=metadata)
        assert resp.ok, 'Unable to set cors headers'

        #Verify that header was set
        resp = self.client.get_container_metadata(self.testcontainer_name)
        assert resp.ok, 'Unable to verify cors header is set'
        assert 'x-container-meta-' + self.cors_allow_origin in resp.headers, \
                'CORS %s header was not accepted with ' \
                'x-container-meta prefix' % str('x-container-meta-' + \
                self.cors_allow_origin)
        self.assertEqual(resp.headers['x-container-meta-' + \
                self.cors_allow_origin], allowed_origin,
                'CORS header was not set properly')

        #Perform OPTIONS request
        headers = {}
        headers['origin'] = 'http://hurfasaur.us'
        headers['Access-Control-Request-Method'] = 'GET'
        resp = self.client.get_container_options(self.testcontainer_name,
                headers=headers)
        assert resp.ok, 'Unable to perform OPTIONS request against cors ' \
                'restricted container (HTTP %s)' % resp.status_code

    def test_options_request_on_cors_origin_restricted_container_full_host_name_list(self):
        metadata = {}

        #Set metadata
        allowed_origin = 'http://firsthost.com ' \
                'http://secondhost.com http://thirdhost.com'
        metadata[self.cors_allow_origin] = allowed_origin

        resp = self.client.set_container_metadata(self.testcontainer_name,
                metadata=metadata)
        assert resp.ok, 'Unable to set cors headers'

        #Verify that header was set
        resp = self.client.get_container_metadata(self.testcontainer_name)
        assert resp.ok, 'Unable to verify cors header is set'
        assert 'x-container-meta-' + self.cors_allow_origin in resp.headers, \
                'CORS %s header was not accepted with ' \
                'x-container-meta prefix' % str('x-container-meta-' + \
                self.cors_allow_origin)
        self.assertEqual(resp.headers['x-container-meta-' + \
                self.cors_allow_origin], allowed_origin,
                'CORS header was not set properly')

        #Perform OPTIONS request
        headers = {}
        headers['origin'] = 'http://firsthost.com'
        headers['Access-Control-Request-Method'] = 'GET'
        resp = self.client.get_container_options(self.testcontainer_name,
                headers=headers)
        assert resp.ok, 'Unable to perform OPTIONS request against cors ' \
                'restricted container with first host in list (HTTP %s)' % \
                resp.status_code

        headers = {}
        headers['origin'] = 'http://secondhost.com'
        headers['Access-Control-Request-Method'] = 'GET'
        resp = self.client.get_container_options(self.testcontainer_name,
                headers=headers)
        assert resp.ok, 'Unable to perform OPTIONS request against cors \
                restricted container with second host in list (HTTP %s)' % \
                resp.status_code

        headers = {}
        headers['origin'] = 'http://thirdhost.com'
        headers['Access-Control-Request-Method'] = 'GET'
        resp = self.client.get_container_options(self.testcontainer_name,
                headers=headers)
        assert resp.ok, 'Unable to perform OPTIONS request against cors ' \
                'restricted container with third host in list (HTTP %s)' % \
                resp.status_code

    def test_options_request_on_cors_origin_restricted_container_partial_host_name(self):
        metadata = {}

        #Set metadata
        allowed_origin = 'hurfasaur.us'
        metadata[self.cors_allow_origin] = allowed_origin

        resp = self.client.set_container_metadata(self.testcontainer_name,
                metadata=metadata)
        assert resp.ok, 'Unable to set cors headers'

        #Verify that header was set
        resp = self.client.get_container_metadata(self.testcontainer_name)
        assert resp.ok, 'Unable to verify cors header is set'
        assert 'x-container-meta-' + self.cors_allow_origin in resp.headers, \
                'CORS %s header was not accepted with ' \
                'x-container-meta prefix' % str('x-container-meta-' + \
                self.cors_allow_origin)
        self.assertEqual(resp.headers['x-container-meta-' + \
                self.cors_allow_origin], allowed_origin,
                'CORS header was not set properly')

        #Perform OPTIONS request
        headers = {}
        headers['origin'] = 'hurfasaur.us'
        headers['Access-Control-Request-Method'] = 'GET'
        resp = self.client.get_container_options(self.testcontainer_name,
                headers=headers)
        assert resp.ok, 'Unable to perform OPTIONS request against cors ' \
                'restricted container (HTTP %s)' % resp.status_code

    @attr('regression')
    def test_options_request_on_cors_age_restricted_container_partial_host_name(self):
        metadata = {}

        #Set metadata
        allowed_origin = 'hurfasaur.us'
        metadata[self.cors_allow_origin] = allowed_origin
        metadata[self.cors_max_age] = '1000'

        resp = self.client.set_container_metadata(self.testcontainer_name,
                metadata=metadata)
        assert resp.ok, 'Unable to set cors headers'

        #Verify that header was set
        resp = self.client.get_container_metadata(self.testcontainer_name)
        assert resp.ok, 'Unable to verify cors header is set'
        #assert 'x-container-meta-' + self.cors_allow_origin in resp.headers, \
        #        'CORS %s header was not accepted with ' \
        #        'x-container-meta prefix' % str('x-container-meta-' + \
        #        self.cors_allow_origin)
        #self.assertEqual(resp.headers['x-container-meta-' + \
        #        self.cors_max_age], '1000', 'CORS header was not set properly')

        #Perform OPTIONS request
        headers = {}
        headers['origin'] = allowed_origin
        headers['Access-Control-Request-Method'] = 'GET'
        resp = self.client.get_container_options(self.testcontainer_name,
                headers=headers)
        assert resp.ok, 'Unable to perform OPTIONS request against cors age ' \
                'restricted container (HTTP %s)' % resp.status_code
