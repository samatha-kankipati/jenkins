import os
from ccengine.common.tools.datagen import rand_name
from testrepo.common.testfixtures.loggingaas import ProducerFixture


class CreateEventProducer(ProducerFixture):

    @classmethod
    def setUpClass(cls):
        super(CreateEventProducer, cls).setUpClass()
        cls.tenant_provider.create_tenant()

    def setUp(self):
        super(CreateEventProducer, self).setUp()
        self.producers_created = []

    def tearDown(self):
        for producer_id in self.producers_created:
            self._delete_producer(producer_id, False)

        self.producers_created = []

    def get_id(self, request):
        """
        Helper function to extract the producer id from location header
        """
        assert request.status_code == 201
        location = request.headers.get('location')
        ret_id = int(os.path.split(location)[1])
        return ret_id

    def _delete_producer(self, producer_id, remove_from_array=True):
        response = self.provider.delete_producer(producer_id)
        self.assertEqual(200, response.status_code,
                         'Delete response code should have returned 200 OK.')

        if remove_from_array:
            self.producers_created.remove(producer_id)

        return response

    def _create_new_producer(self, name=None, pattern=None,
                             durable=None, encrypted=None):
        """
        Create Producer helper function.
        """
        event_producer_req = self.provider.create_producer(name, pattern,
                                                           durable, encrypted,
                                                           create_depend=False)
        self.assertEqual(201, event_producer_req.status_code,
                         'Status code should have been 201 Created. ')

        location = event_producer_req.headers.get('location')
        producer_id = int(os.path.split(location)[1])

        bad_loc_msg = ('Headers should have returned a location in the '
                       'headers after creation')
        self.assertIsNotNone(location, bad_loc_msg)
        self.assertGreater(producer_id, 0, "Invalid producer ID")

        self.producers_created.append(producer_id)

        return {
            'request': event_producer_req,
            'location': location,
            'producer_id': producer_id
        }

    def test_create_producer(self):
        self._create_new_producer()

    def test_get_producer(self):
        producer_results = self._create_new_producer()
        producer_id = producer_results['producer_id']

        event_producer_resp = self.provider.get_producer(producer_id)
        resp_entity = event_producer_resp.entity

        self.assertEqual(200, event_producer_resp.status_code,
                         'Status code should have been 200 OK')
        self.assertIsNotNone(resp_entity)
        self.assertEqual('testapp', resp_entity.name)

    def test_get_all_producers(self):
        prod_name = rand_name()

        prod_id_one = self._create_new_producer()['producer_id']
        prod_id_two = self._create_new_producer(name=prod_name)['producer_id']

        producer_res_one = self.provider.get_producer(prod_id_one)
        producer_res_two = self.provider.get_producer(prod_id_two)

        producer_list_req = self.provider.get_all_producers()
        producer_list = producer_list_req.entity

        prod_one_name = producer_res_one.entity.name
        prod_two_name = producer_res_two.entity.name

        self.assertEqual(2, len(producer_list))
        self.assertEqual('testapp', prod_one_name)
        self.assertEqual(prod_name, prod_two_name)

    def test_update_producer(self):
        initial_producer_results = self._create_new_producer()
        created_id = initial_producer_results['producer_id']

        update_producer_results = self.provider.update_producer(
            producer_id=created_id,
            producer_name='test_provider',
            producer_pattern='test_pattern',
            producer_durable=True,
            producer_encrypted=True)

        self.assertEqual(200, update_producer_results.status_code,
                         'Should have been 200 OK')

        updated_results = self.provider.get_producer(created_id)
        updated_obj = updated_results.entity

        self.assertEqual('test_provider', updated_obj.name)
        self.assertEqual('test_pattern', updated_obj.pattern)
        self.assertEqual(True, updated_obj.durable)
        self.assertEqual(True, updated_obj.encrypted)

    def test_delete_producer(self):
        producer_results = self._create_new_producer()

        # Assertion is in the helper method
        self._delete_producer(producer_results['producer_id'])
