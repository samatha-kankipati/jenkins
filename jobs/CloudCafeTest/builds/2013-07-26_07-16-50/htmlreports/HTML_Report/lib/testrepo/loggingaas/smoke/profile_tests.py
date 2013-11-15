import os
import json
from testrepo.common.testfixtures.loggingaas import ProfileFixture
from ccengine.providers.loggingaas.logging_provider \
    import LoggingProducerProvider


class CreateProfileTests(ProfileFixture):

    @classmethod
    def setUpClass(cls):
        super(CreateProfileTests, cls).setUpClass()
        cls.tenant_provider.create_tenant()

    def setUp(self):
        super(CreateProfileTests, self).setUp()
        self.profiles_created = []

        self.producer_provider = LoggingProducerProvider(self.config)
        response = self.producer_provider.create_producer("boom",
                                                          create_depend=False)
        self.producer_id = self.get_id(response)

    def tearDown(self):
        for profile_id in self.profiles_created:
            self._delete_profile(profile_id, False)

        self.profiles_created = []
        self.producer_provider.delete_producer(self.producer_id)

    def get_id(self, request):
        """
        Helper function to extract the profile id from location header
        """
        assert request.status_code == 201
        location = request.headers.get('location')
        ret_id = int(os.path.split(location)[1])
        return ret_id

    def _delete_profile(self, profile_id, remove_from_array=True):
        response = self.provider.delete_profile(profile_id)
        self.assertEqual(200, response.status_code,
                         'Delete response code should have returned 200 OK.')

        if remove_from_array:
            self.profiles_created.remove(profile_id)

        return response

    def _create_new_profile(self, profile_name=None, event_producer_ids=None):
        profile_req = self.provider.create_profile(profile_name,
                                                   event_producer_ids,
                                                   create_depend=False)

        self.assertEquals(201, profile_req.status_code,
                          'expected 201 Created Response Code')

        location = profile_req.headers.get('location')
        profile_id = int(os.path.split(location)[1])

        self.assertIsNotNone(location, 'Headers should have returned' +
                            'a location in the headers after creation')
        self.assertGreater(profile_id, 0, "Invalid profile ID")

        self.profiles_created.append(profile_id)

        return {
            'request': profile_req,
            'location': location,
            'profile_id': profile_id
        }

    def test_create_profile(self):
        self._create_new_profile(event_producer_ids=[self.producer_id])

    def test_get_profile_by_profile_id(self):
        profile_results = self._create_new_profile(
            event_producer_ids=[self.producer_id])
        profile_id = profile_results['profile_id']
        event_profile_resp = self.provider.get_profile(profile_id)
        resp_entity = event_profile_resp.entity

        self.assertEqual(200, event_profile_resp.status_code,
                         'Status code should have been 200 OK')
        self.assertIsNotNone(resp_entity)
        self.assertEqual('appservers-1', resp_entity.name)

    def test_update_profile(self):
        initial_profile_results = self._create_new_profile(
            event_producer_ids=[self.producer_id])
        created_id = initial_profile_results['profile_id']

        # Update
        update_profile_results = self.provider.update_profile(
            profile_id=created_id,
            profile_name='updated_profile',
            event_producer_ids=[self.producer_id])

        self.assertEqual(200, update_profile_results.status_code,
                         'Should have been 200 OK')

        updated_results = self.provider.get_profile(created_id)
        updated_name = updated_results.entity.name

        self.assertEqual('updated_profile', updated_name)

    def test_unlink_producer_update_profile(self):
        initial_profile_results = self._create_new_profile(
            event_producer_ids=[self.producer_id])
        created_id = initial_profile_results['profile_id']
        update_profile_results = self.provider.update_profile(
            profile_id=created_id,
            profile_name='updated_profile',
            event_producer_ids=json.loads('[]'))
        self.assertEqual(200, update_profile_results.status_code,
                         'Should have been 200 OK')

        updated_results = self.provider.get_profile(created_id)
        updated_obj = updated_results.entity

        self.assertEqual('updated_profile', updated_obj.name)
        self.assertEqual(0, len(updated_obj.event_producers),
                         'event producer size is 0')

    def test_get_all_profiles(self):
        profile_id_one = self._create_new_profile(
            event_producer_ids=[self.producer_id])['profile_id']
        profile_id_two = self._create_new_profile(
            profile_name='newprofile3',
            event_producer_ids=[self.producer_id])['profile_id']

        profile_res_one = self.provider.get_profile(profile_id_one)
        profile_res_two = self.provider.get_profile(profile_id_two)

        profile_list_req = self.provider.get_all_profiles()
        profile_list = profile_list_req.entity

        profile_one_name = profile_res_one.entity.name
        profile_two_name = profile_res_two.entity.name

        self.assertEqual(2, len(profile_list))
        self.assertEqual('appservers-1', profile_one_name)
        self.assertEqual('newprofile3', profile_two_name)

    def test_delete_profile(self):
        profile_results = self._create_new_profile(
            event_producer_ids=[self.producer_id])

        # Assertion is in the helper method
        self._delete_profile(profile_results['profile_id'])
