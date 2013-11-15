"""4.2 Storage Container Services Smoke Tests"""
from testrepo.common.testfixtures.object_storage_fixture \
        import ObjectStorageTestFixture

#these need to be moved to a config
CONTENT_TYPE_TEXT = 'text/plain; charset=UTF-8'


class MarkerTest(ObjectStorageTestFixture):

    @classmethod
    def setUpClass(cls):
        super(MarkerTest, cls).setUpClass()
        cls.min_limit = 0
        cls.max_limit = 12

    def _get_name(self, low, high, base_name=''):
        while low <= high:
            if low < 10:
                yield ''.join([base_name, '0', str(low)])
            else:
                yield ''.join([base_name, str(low)])
            low += 1

    def _get_list(self, string_list):
        to_return = string_list.split('\n')
        to_return = filter(None, to_return)
        return to_return

    def test_account_marker(self):
        base_container_name = self.client.generate_unique_container_name(
                infix='account_marker')

        cleanup_list = []

        container_names = self._get_name(self.min_limit, self.max_limit,
                base_container_name)

        for container_name in container_names:
            cleanup_list.append(container_name)
            self.client.create_container(container_name)

        self.addCleanup(self.client.force_delete_containers, cleanup_list)

        #marker and endmarker == endpoints
        marker = ''.join([base_container_name, '0'])
        end_marker = ''.join([base_container_name, '12'])
        params = {'marker': marker,
                'end_marker': end_marker}
        r = self.client.list_containers(params=params)
        container_list = self._get_list(r.content)
        self.assertGreater(len(container_list), 0, 'should return list.')

        #marker and endmarker between endpoints
        marker = ''.join([base_container_name, '01'])
        end_marker = ''.join([ base_container_name, '11'])
        params = {'marker': marker,
                'end_marker': end_marker}
        r = self.client.list_containers(params=params)
        container_list = self._get_list(r.content)
        self.assertGreater(len(container_list), 0, 'should return list.')

        #marker and endmarker are swapped
        marker = ''.join([base_container_name, '11'])
        end_marker = ''.join([base_container_name, '00'])
        params = {'marker': marker,
                'end_marker': end_marker}
        r = self.client.list_containers(params=params)
        container_list = self._get_list(r.content)
        self.assertEqual(len(container_list), 0, 'should not return a list.')

        #marker > min and endmarker > max
        marker = ''.join([base_container_name, '01'])
        end_marker = ''.join([base_container_name, '200'])
        params = {'marker': marker,
                'end_marker': end_marker}
        r = self.client.list_containers(params=params)
        container_list = self._get_list(r.content)
        self.assertGreater(len(container_list), 0, 'should return list.')

        #marker == min and endmarker > max
        marker = ''.join([base_container_name, '0'])
        end_marker = ''.join([base_container_name, '200'])
        params = {'marker': marker,
                'end_marker': end_marker}
        r = self.client.list_containers(params=params)
        container_list = self._get_list(r.content)
        self.assertGreater(len(container_list), 0, 'should return list.')

        #marker < min and endmarker < max
        marker = ''.join([base_container_name, '/'])
        end_marker = ''.join([base_container_name, '11'])
        params = {'marker': marker,
                'end_marker': end_marker}
        r = self.client.list_containers(params=params)
        container_list = self._get_list(r.content)
        self.assertGreater(len(container_list), 0, 'should return list.')

        #marker < min and endmarker == max
        marker  = ''.join([base_container_name, '/'])
        end_marker  = ''.join([base_container_name, '12'])
        params = {'marker': marker,
                'end_marker': end_marker}
        r = self.client.list_containers(params=params)
        container_list = self._get_list(r.content)
        self.assertGreater(len(container_list), 0, 'should return list.')

        #marker == min and endmarker < max
        marker  = ''.join([base_container_name, '0'])
        end_marker  = ''.join([base_container_name, '11'])
        params = {'marker': marker,
                'end_marker': end_marker}
        r = self.client.list_containers(params=params)
        container_list = self._get_list(r.content)
        self.assertGreater(len(container_list), 0, 'should return list.')

        #marker < min and endmarker == min
        marker  = ''.join([base_container_name, '/'])
        end_marker  = ''.join([base_container_name, '0'])
        params = {'marker': marker,
                'end_marker': end_marker}
        r = self.client.list_containers(params=params)
        container_list = self._get_list(r.content)
        self.assertEqual(len(container_list), 0, 'should not return a list.')

        #marker == max and endmarker > max
        marker  = ''.join([base_container_name, '12'])
        end_marker  = ''.join([base_container_name, '200'])
        params = {'marker': marker,
                'end_marker': end_marker}
        r = self.client.list_containers(params=params)
        container_list = self._get_list(r.content)
        self.assertEqual(len(container_list), 0, 'should not return a list.')

        #marker > min and endmarker == max
        marker  = ''.join([base_container_name, '01'])
        end_marker  = ''.join([base_container_name, '12'])
        params = {'marker': marker,
                'end_marker': end_marker}
        r = self.client.list_containers(params=params)
        container_list = self._get_list(r.content)
        self.assertGreater(len(container_list), 0, 'should return list.')

        #marker < min and endmarker > max
        marker  = ''.join([base_container_name, '/'])
        end_marker  = ''.join([base_container_name, '30'])
        params = {'marker': marker,
                'end_marker': end_marker}
        r = self.client.list_containers(params=params)
        container_list = self._get_list(r.content)
        self.assertGreater(len(container_list), 0, 'should return list.')


    def test_container_marker(self):
        """4.2.1.2. Controlling a Large List of Objects (Marker)"""
        container_name = self.client.generate_unique_container_name(
                infix='container_marker')
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers, [container_name])

        object_base_name = ''
        object_names = self._get_name(self.min_limit,
                                  self.max_limit,
                                  object_base_name)

        for object_name in object_names:
            object_data = ''.join([object_name, ' DATA'])
            content_length = str(len(object_data))
            self.client.set_storage_object(container_name, object_name,
                    content_length=content_length,
                    content_type=CONTENT_TYPE_TEXT, payload=object_data)

        # marker and endmarker == endpoints
        params = {'marker': '0',
                'end_marker': '12'}
        r = self.client.list_objects(container_name, params=params)
        object_list = self._get_list(r.content)
        self.assertGreater(len(object_list), 0, 'should return list.')

        #marker and endmarker between endpoints
        params = {'marker': '01',
                  'end_marker': '11'}
        r = self.client.list_objects(container_name, params=params)
        object_list = self._get_list(r.content)
        self.assertGreater(len(object_list), 0, 'should return list.')

        #marker and endmarker are swapped
        params = {'marker': '11',
                  'end_marker': '00'}
        r = self.client.list_objects(container_name, params=params)
        object_list = self._get_list(r.content)
        self.assertEqual(len(object_list), 0, 'should not return a list.')

        #marker > min and endmarker > max
        params = {'marker': '01',
                  'end_marker': '200'}
        r = self.client.list_objects(container_name, params=params)
        object_list = self._get_list(r.content)
        self.assertGreater(len(object_list), 0, 'should return list.')

        #marker == min and endmarker > max
        params = {'marker': '0',
                  'end_marker': '200'}
        r = self.client.list_objects(container_name, params=params)
        object_list = self._get_list(r.content)
        self.assertGreater(len(object_list), 0, 'should return list.')

        #marker < min and endmarker < max
        params = {'marker': '/',
                  'end_marker': '11'}
        r = self.client.list_objects(container_name, params=params)
        object_list = self._get_list(r.content)
        self.assertGreater(len(object_list), 0, 'should return list.')

        #marker < min and endmarker == max
        params = {'marker': '/',
                  'end_marker': '12'}
        r = self.client.list_objects(container_name, params=params)
        object_list = self._get_list(r.content)
        self.assertGreater(len(object_list), 0, 'should return list.')

        #marker == min and endmarker < max
        params = {'marker': '0',
                  'end_marker': '11'}
        r = self.client.list_objects(container_name, params=params)
        object_list = self._get_list(r.content)
        self.assertGreater(len(object_list), 0, 'should return list.')

        #marker > min and endmarker == max
        params = {'marker': '01',
                  'end_marker': '12'}
        r = self.client.list_objects(container_name, params=params)
        object_list = self._get_list(r.content)
        self.assertGreater(len(object_list), 0, 'should return list.')

        #marker < min and endmarker == min
        params = {'marker': '/',
                  'end_marker': '0'}
        r = self.client.list_objects(container_name, params=params)
        object_list = self._get_list(r.content)
        self.assertEqual(len(object_list), 0, 'should not return a list.')

        #marker == max and endmarker > max
        params = {'marker': '12',
                  'end_marker': '200'}
        r = self.client.list_objects(container_name, params=params)
        object_list = self._get_list(r.content)
        self.assertEqual(len(object_list), 0, 'should not return a list.')

        #marker < min and endmarker > max
        params = {'marker': '/',
                  'end_marker': '30'}
        r = self.client.list_objects(container_name, params=params)
        object_list = self._get_list(r.content)
        self.assertGreater(len(object_list), 0, 'should return list.')
