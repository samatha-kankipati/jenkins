from ccengine.common.tools.datatools import\
    string_to_datetime, are_datetimestrings_equal
from ccengine.providers.compute.compute_api import ComputeAPIProvider
from testrepo.common.testfixtures.fixtures import BaseTestFixture


class InstanceEventsValidator(BaseTestFixture):
    """
    @summary: Helper to validate all Instance Event details
    """

    @classmethod
    def setUpClass(cls):
        super(InstanceEventsValidator, cls).setUpClass()
        cls.compute_provider = ComputeAPIProvider(cls.config, cls.fixture_log)
        cls.flavors_client = cls.compute_provider.flavors_client
        cls.tenant_id = cls.config.compute_api.tenant_id
        cls.leeway_for_timestamp = \
            cls.config.compute_api.datetime_seconds_leeway
        cls.highio_instance_type_id_dict = \
            cls.config.compute_api.highio_instance_type_id_dict
        cls.region_datacenter_mapping = \
            cls.config.compute_api.region_datacenter_mapping
        cls.region = cls.config.compute_api.region

    def verify_compute_instance_create_start(self, expected_data, event):
        """
        @summary: Verifies the compute.instance.create.start details
        @param expected_data: Contains all the expected data to be verified
        @type expected_data: Dictionary
        @param event: Contains event details (actual data) to be verified.
        @type event: Dictionary
        """
        server = expected_data['server']
        expected_image_metadata = expected_data['image_meta']
        self.assertEqual('', event.payload.launched_at,
                         msg="{0}: The launched_at field was not blank."
                         .format(event.event_type))
        self.assertEqual('', event.payload.deleted_at,
                         msg="{0}: The deleted_at field was not blank."
                         .format(event.event_type))
        self.verify_server_event_common_details(
            server, event, expected_image_metadata)

    def verify_compute_instance_create_end(self, expected_data, event):
        """
        @summary: Verifies the compute.instance.create.end details
        @param expected_data: Contains all the expected data to be verified
        @type expected_data: Dictionary
        @param event: Contains event details (actual data) to be verified.
        @type event: Dictionary
        """
        expected_launched_at = expected_data['launched_at_create_server']
        expected_image_metadata = expected_data['image_meta']
        self.assertEqual('active', event.payload.state,
                         msg="{0}: The state was not active."
                         .format(event.event_type))
        self.assertEqual('', event.payload.deleted_at,
                         msg="{0}: The deleted_at field was not blank."
                         .format(event.event_type))
        self._verify_fixed_ips(expected_data['server'], event)
        self.assertTrue(
            are_datetimestrings_equal(expected_launched_at,
                                      event.payload.launched_at,
                                      self.leeway_for_timestamp),
            msg="{0}: The expected launched_at {1} does not match with the "
                "value found in the event {2}."
                .format(event.event_type,
                        expected_launched_at,
                        event.payload.launched_at))
        self.verify_server_event_common_details(
            expected_data['server'], event, expected_image_metadata)

    def verify_compute_instance_exists(self, expected_data, event):
        """
        @summary: Verifies the compute.instance.exists details
        @param expected_data: Contains all the expected data to be verified
        @type expected_data: Dictionary
        @param event: Contains event details (actual data) to be verified.
        @type event: Dictionary
        """
        self._verify_exists_event_common_details(expected_data, event)

    def verify_compute_instance_exists_verified_old(self, expected_data,
                                                    event):
        """
        @summary: Verifies the compute.instance.exists.old details
        @param expected_data: Contains all the expected data to be verified
        @type expected_data: Dictionary
        @param event: Contains event details (actual data) to be verified.
        @type event: Dictionary
        """
        self._verify_exists_event_common_details(expected_data, event)

    def _verify_exists_event_common_details(self, expected_data, event):
        """
        @summary: Verifies the *.exists details
        @param expected_data: Contains all the expected data to be verified
        @type expected_data: Dictionary
        @param event: Contains event details (actual data) to be verified.
        @type event: Dictionary
        """
        expected_image_metadata = expected_data['image_meta']
        expected_launched_at = expected_data['launched_at_in_exists']
        expected_audit_period_beginning = \
            expected_data['audit_period_beginning']
        expected_audit_period_ending = expected_data['audit_period_ending']

        self.assertTrue(
            are_datetimestrings_equal(expected_audit_period_beginning,
                                      event.payload.audit_period_beginning,
                                      self.leeway_for_timestamp),
            msg="{0}: The expected audit period beginning {1} does not match "
                "with the actual value found in the event {2}."
                .format(event.event_type,
                        expected_audit_period_beginning,
                        event.payload.audit_period_beginning))

        self.assertTrue(
            are_datetimestrings_equal(expected_audit_period_ending,
                                      event.payload.audit_period_ending,
                                      self.leeway_for_timestamp),
            msg="{0}: The expected audit period ending {1} does not match "
                "with the actual value found in the event {2}."
                .format(event.event_type,
                        expected_audit_period_ending,
                        event.payload.audit_period_ending))

        self.assertTrue(
            are_datetimestrings_equal(expected_launched_at,
                                      event.payload.launched_at,
                                      self.leeway_for_timestamp),
            msg="{0}: The expected launched_at {1} does not match with the "
                "value found in the event {2}."
                .format(event.event_type,
                        expected_launched_at,
                        event.payload.launched_at))

        self.verify_server_event_common_details(
            expected_data['server'], event, expected_image_metadata)

    def verify_compute_instance_resize_start(self, expected_data, event):
        """
        @summary: Verifies the compute.instance.resize.start details
        @param expected_data: Contains all the expected data to be verified
        @type expected_data: Dictionary
        @param event: Contains event details (actual data) to be verified.
        @type event: Dictionary
        """
        expected_launched_at = expected_data['launched_at_resize_server']
        expected_image_metadata = expected_data['image_meta']
        self.assertTrue(
            are_datetimestrings_equal(expected_launched_at,
                                      event.payload.launched_at,
                                      self.leeway_for_timestamp),
            msg="{0}: The expected launched_at {1} does not match with the "
                "value found in the event {2}."
                .format(event.event_type,
                        expected_launched_at,
                        event.payload.launched_at))
        self._verify_fixed_ips(expected_data['server'], event)
        self.assertEqual('', event.payload.deleted_at,
                         msg="{0}: The deleted_at field was not blank."
                         .format(event.event_type))
        self.verify_server_event_common_details(
            expected_data['server'], event, expected_image_metadata)

    def verify_compute_instance_resize_end(self, expected_data, event):
        """
        @summary: Verifies the compute.instance.resize.end details
        @param expected_data: Contains all the expected data to be verified
        @type expected_data: Dictionary
        @param event: Contains event details (actual data) to be verified.
        @type event: Dictionary
        """
        expected_launched_at = expected_data['launched_at_resize_server']
        expected_image_metadata = expected_data['image_meta']
        self.assertTrue(
            are_datetimestrings_equal(expected_launched_at,
                                      event.payload.launched_at,
                                      self.leeway_for_timestamp),
            msg="{0}:The expected launched_at {1} does not match with the "
                " value found in the event {2}."
                .format(event.event_type,
                        expected_launched_at,
                        event.payload.launched_at))

        self._verify_fixed_ips(expected_data['server'], event)
        self.assertEqual('', event.payload.deleted_at,
                         msg="{0}: The deleted_at field was not blank."
                             .format(event.event_type))

        self.verify_server_event_common_details(
            expected_data['server'], event, expected_image_metadata)

    def verify_compute_instance_resize_prep_start(self, expected_data, event):
        """
        @summary: Verifies the compute.instance.resize.prep.start details
        @param expected_data: Contains all the expected data to be verified
        @type expected_data: Dictionary
        @param event: Contains event details (actual data) to be verified.
        @type event: Dictionary
        """
        expected_launched_at = expected_data['launched_at_resize_server']
        expected_image_metadata = expected_data['image_meta']
        self.assertTrue(
            are_datetimestrings_equal(expected_launched_at,
                                      event.payload.launched_at,
                                      self.leeway_for_timestamp),
            msg="{0}: The expected launched_at {1} does not match with the "
            "value found in the event {2}.".format(event.event_type,
                                                   expected_launched_at,
                                                   event.payload.launched_at))
        self.assertEqual('', event.payload.deleted_at,
                         msg="{0}: The deleted_at field was not blank."
                         .format(event.event_type))
        self.verify_server_event_common_details(
            expected_data['server'], event, expected_image_metadata)

    def verify_compute_instance_resize_prep_end(self, expected_data, event):
        """
        @summary: Verifies the compute.instance.resize.prep.end details
        @param expected_data: Contains all the expected data to be verified
        @type expected_data: Dictionary
        @param event: Contains event details (actual data) to be verified.
        @type event: Dictionary
        """
        expected_launched_at = expected_data['launched_at_resize_server']
        expected_image_metadata = expected_data['image_meta']
        self.assertEqual(expected_data['expected_new_instance_type_id'],
                         str(event.payload.new_instance_type_id),
                         msg="{0}:The id of the flavor with which the server "
                         "is resized does not match with the one found in "
                         "the event.".format(event.event_type))
        self.assertEqual(expected_data['expected_new_instance_type'],
                         str(event.payload.new_instance_type),
                         msg="{0}: The name of the flavor with which the "
                         "server is resized does not match with the one "
                         "found in the event.".format(event.event_type))

        self.assertTrue(
            are_datetimestrings_equal(expected_launched_at,
                                      event.payload.launched_at,
                                      self.leeway_for_timestamp),
            msg="{0}: The expected launched_at {1} does not match with the "
            "value found in the event {2}.".format(event.event_type,
                                                   expected_launched_at,
                                                   event.payload.launched_at))
        self.assertEqual('', event.payload.deleted_at,
                         msg="{0}: The deleted_at field was not blank."
                         .format(event.event_type))
        self.verify_server_event_common_details(
            expected_data['server'], event, expected_image_metadata)

    def verify_compute_instance_resize_confirm_start(self, expected_data,
                                                     event):
        """
        @summary: Verifies the compute.instance.resize.confirm.start details
        @param expected_data: Contains all the expected data to be verified
        @type expected_data: Dictionary
        @param event: Contains event details (actual data) to be verified.
        @type event: Dictionary
        """
        expected_launched_at = expected_data['launched_at_resize_server']
        expected_image_metadata = expected_data['image_meta']

        self.assertTrue(
            are_datetimestrings_equal(expected_launched_at,
                                      event.payload.launched_at,
                                      self.leeway_for_timestamp),
            msg="{0}: The expected launched_at {1} does not match with the "
            "value found in the event {2}.".format(event.event_type,
                                                   expected_launched_at,
                                                   event.payload.launched_at))

        self.assertEqual('', event.payload.deleted_at,
                         msg="{0}: The deleted_at field was not blank."
                         .format(event.event_type))
        self.verify_server_event_common_details(
            expected_data['resized_server'], event, expected_image_metadata)

    def verify_compute_instance_resize_confirm_end(self, expected_data, event):
        """
        @summary: Verifies the compute.instance.resize.confirm.end details
        @param expected_data: Contains all the expected data to be verified
        @type expected_data: Dictionary
        @param event: Contains event details (actual data) to be verified.
        @type event: Dictionary
        """
        expected_launched_at = expected_data['launched_at_resize_server']
        expected_image_metadata = expected_data['image_meta']

        self.assertTrue(
            are_datetimestrings_equal(expected_launched_at,
                                      event.payload.launched_at,
                                      self.leeway_for_timestamp),
            msg="{0}: The expected launched_at {1} does not match with the "
            "value found in the event {2}.".format(event.event_type,
                                                   expected_launched_at,
                                                   event.payload.launched_at))
        self._verify_fixed_ips(expected_data['server'], event)
        self.assertEqual('', event.payload.deleted_at,
                         msg="{0}: The deleted_at field was not blank."
                         .format(event.event_type))

        self.verify_server_event_common_details(
            expected_data['resized_server'], event, expected_image_metadata)

    def verify_compute_instance_resize_revert_start(self, expected_data,
                                                    event):
        """
        @summary: Verifies the compute.instance.resize.revert.start details
        @param expected_data: Contains all the expected data to be verified
        @type expected_data: Dictionary
        @param event: Contains event details (actual data) to be verified.
        @type event: Dictionary
        """
        expected_launched_at = expected_data['launched_at_resize_server']
        expected_image_metadata = expected_data['image_meta']
        self.assertTrue(
            are_datetimestrings_equal(expected_launched_at,
                                      event.payload.launched_at,
                                      self.leeway_for_timestamp),
            msg="{0}: The expected launched_at {1} does not match with the "
            "value found in the event {2}."
            .format(event.event_type,
                    expected_launched_at,
                    event.payload.launched_at))
        self.assertEqual('', event.payload.deleted_at,
                         msg="{0}: The deleted_at field was not blank."
                         .format(event.event_type))
        self.verify_server_event_common_details(
            expected_data['server'], event, expected_image_metadata)

    def verify_compute_instance_resize_revert_end(self, expected_data, event):
        """
        @summary: Verifies the compute.instance.resize.revert.end details
        @param expected_data: Contains all the expected data to be verified
        @type expected_data: Dictionary
        @param event: Contains event details (actual data) to be verified.
        @type event: Dictionary
        """
        expected_launched_at = expected_data['launched_at_resize_server']
        expected_image_metadata = expected_data['image_meta']
        self.assertTrue(
            are_datetimestrings_equal(expected_launched_at,
                                      event.payload.launched_at,
                                      self.leeway_for_timestamp),
            msg="{0}: The expected launched_at {1} does not match with the "
            "value found in the event {2}.".format(event.event_type,
                                                   expected_launched_at,
                                                   event.payload.launched_at))
        # verify_fixed_ips commented out due to RM 3307
        # self._verify_fixed_ips(expected_data['resize_reverted_server'],
        #                        event)
        self.assertEqual('', event.payload.deleted_at,
                         msg="{0}: The deleted_at field was not blank."
                         .format(event.event_type))

        self.verify_server_event_common_details(
            expected_data['resize_reverted_server'], event,
            expected_image_metadata)

    def verify_compute_instance_finish_resize_start(self, expected_data,
                                                    event):
        """
        @summary: Verifies the compute.instance.resize.finish.start details
        @param expected_data: Contains all the expected data to be verified
        @type expected_data: Dictionary
        @param event: Contains event details (actual data) to be verified.
        @type event: Dictionary
        """
        expected_launched_at = expected_data['launched_at_create_server']
        expected_image_metadata = expected_data['image_meta']
        self.assertTrue(
            are_datetimestrings_equal(expected_launched_at,
                                      event.payload.launched_at,
                                      self.leeway_for_timestamp),
            msg="{0}: The expected launched_at {1} does not match with the "
            "value found in the event {2}.".format(event.event_type,
                                                   expected_launched_at,
                                                   event.payload.launched_at))
        self._verify_fixed_ips(expected_data['resized_server'], event)
        self.assertEqual('', event.payload.deleted_at,
                         msg="{0}: The deleted_at field was not blank."
                         .format(event.event_type))
        self.verify_server_event_common_details(
            expected_data['resized_server'], event, expected_image_metadata)

    def verify_compute_instance_finish_resize_end(self, expected_data, event):
        """
        @summary: Verifies the compute.instance.resize.finish.end details
        @param expected_data: Contains all the expected data to be verified
        @type expected_data: Dictionary
        @param event: Contains event details (actual data) to be verified.
        @type event: Dictionary
        """
        expected_launched_at = expected_data['launched_at_resize_server']
        expected_image_metadata = expected_data['image_meta']
        self.assertTrue(
            are_datetimestrings_equal(expected_launched_at,
                                      event.payload.launched_at,
                                      self.leeway_for_timestamp),
            msg="{0}: The expected launched_at {1} does not match with the "
            "value found in the event {2}.".format(event.event_type,
                                                   expected_launched_at,
                                                   event.payload.launched_at))
        self.assertEqual('', event.payload.deleted_at,
                         msg="{0}: The deleted_at field was not blank."
                         .format(event.event_type))
        self._verify_fixed_ips(expected_data['resized_server'], event)
        self.verify_server_event_common_details(
            expected_data['resized_server'], event, expected_image_metadata)

    def verify_compute_instance_rebuild_start(self, expected_data, event):
        """
        @summary: Verifies the compute.instance.rebuild.start details
        @param expected_data: Contains all the expected data to be verified
        @type expected_data: Dictionary
        @param event: Contains event details (actual data) to be verified.
        @type event: Dictionary
        """
        expected_launched_at_created_server = \
            expected_data['launched_at_in_exists']
        server_after_rebuild = expected_data["server_after_rebuild"]
        expected_image_metadata = expected_data['rebuilt_server_image_meta']
        self.assertEqual('active', event.payload.state,
                         msg="{0}: The state was not active"
                         .format(event.event_type))
        self.assertEqual('rebuilding', event.payload.state_description,
                         msg="{0}: The state description was not rebuilding"
                         .format(event.event_type))
        self.assertTrue(
            are_datetimestrings_equal(expected_launched_at_created_server,
                                      event.payload.launched_at,
                                      self.leeway_for_timestamp),
            msg="{0}: The expected launched_at {1} does not match with the "
            "value found in the event {2}.".format(
                event.event_type,
                expected_launched_at_created_server,
                event.payload.launched_at))

        self.verify_server_event_common_details(
            server_after_rebuild, event, expected_image_metadata)

    def verify_compute_instance_rebuild_end(self, expected_data, event):
        """
        @summary: Verifies the compute.instance.rebuild.end details
        @param expected_data: Contains all the expected data to be verified
        @type expected_data: Dictionary
        @param event: Contains event details (actual data) to be verified.
        @type event: Dictionary
        """
        expected_launched_at = expected_data['launched_at_in_rebuild']
        expected_image_metadata = expected_data['rebuilt_server_image_meta']
        self.assertEqual('active', event.payload.state,
                         msg="{0}: The state was not active"
                         .format(event.event_type))
        self.assertEqual('', event.payload.state_description,
                         msg="{0}: The state description was not blank"
                         .format(event.event_type))

        # launched_at sometimes gets reset at the start of the action,
        # then again at the end of the action so the leeway needs to
        # be large here; ~20 mins
        self.assertTrue(
            are_datetimestrings_equal(expected_launched_at,
                                      event.payload.launched_at,
                                      self.leeway_for_timestamp),
            msg="{0}: The expected launched_at {1} does not match with the "
            "value found in the event {2}.".format(event.event_type,
                                                   expected_launched_at,
                                                   event.payload.launched_at))

        self._verify_fixed_ips(expected_data['server_after_rebuild'], event)
        self.verify_server_event_common_details(
            expected_data['server_after_rebuild'], event,
            expected_image_metadata)

    def verify_compute_instance_delete_start(self, expected_data, event):
        """
        @summary: Verifies the compute.instance.delete.start details
        @param expected_data: Contains all the expected data to be verified
        @type expected_data: Dictionary
        @param event: Contains event details (actual data) to be verified.
        @type event: Dictionary
        """
        expected_image_metadata = expected_data['image_meta']
        self.assertEqual('deleting', event.payload.state_description,
                         msg='{0}: The event state description did not match '
                         'the expected value.'.format(event.event_type))
        self.assertEqual('', event.payload.deleted_at,
                         msg="{0}: The deleted_at field was not blank."
                         .format(event.event_type))
        self.assertNotEqual('', event.payload.launched_at,
                            msg="{0}: The launched_at field was blank."
                            .format(event.event_type))
        self.verify_server_event_common_details(
            expected_data['server'], event, expected_image_metadata)

    def verify_compute_instance_delete_end(self, expected_data, event):
        """
        @summary: Verifies the compute.instance.delete.end details
        @param expected_data: Contains all the expected data to be verified
        @type expected_data: Dictionary
        @param event: Contains event details (actual data) to be verified.
        @type event: Dictionary
        """
        expected_image_metadata = expected_data['image_meta']
        expected_deleted_at = expected_data['deleted_at']
        self.assertEqual('', event.payload.state_description,
                         msg='{0}: The event state description was not blank.'
                         .format(event.event_type))
        self.assertEqual('deleted', event.payload.state,
                         msg="{0}: The state was not deleted."
                         .format(event.event_type))
        self.assertTrue(
            are_datetimestrings_equal(expected_deleted_at,
                                      event.payload.deleted_at,
                                      self.leeway_for_timestamp),
            msg="{0}: The expected deleted_at {1} does not match with the "
            "value found in the event {2}.".format(event.event_type,
                                                   expected_deleted_at,
                                                   event.payload.deleted_at))

        # terminated_at should occur around the same time as the deleted at
        expected_terminated_at = expected_deleted_at
        self.assertTrue(
            are_datetimestrings_equal(expected_terminated_at,
                                      event.payload.terminated_at,
                                      self.leeway_for_timestamp),
            msg="{0}: The expected terminated at {1} does not match with the "
            "value found in the event {2}.".format(
                event.event_type,
                expected_terminated_at,
                event.payload.terminated_at))

        self.assertNotEqual('', event.payload.launched_at,
                            msg="{0}: The launched_at field was blank."
                            .format(event.event_type))
        self.verify_server_event_common_details(
            expected_data['server'], event, expected_image_metadata)

    def verify_compute_instance_shutdown_start(self, expected_data, event):
        """
        @summary: Verifies the compute.instance.shutdown.start details
        @param expected_data: Contains all the expected data to be verified
        @type expected_data: Dictionary
        @param event: Contains event details (actual data) to be verified.
        @type event: Dictionary
        """
        expected_image_metadata = expected_data['image_meta']
        self.verify_server_event_common_details(
            expected_data['server'], event, expected_image_metadata)

    def verify_compute_instance_shutdown_end(self, expected_data, event):
        """
        @summary: Verifies the compute.instance.shutdown.end details
        @param expected_data: Contains all the expected data to be verified
        @type expected_data: Dictionary
        @param event: Contains event details (actual data) to be verified.
        @type event: Dictionary
        """
        expected_image_metadata = expected_data['image_meta']
        self.verify_server_event_common_details(
            expected_data['server'], event, expected_image_metadata)

    def verify_scheduler_run_instance_scheduled(self, expected_data, event):
        """
        @summary: Verifies the scheduler.run_instance.scheduled details
        @param expected_data: Contains all the expected data to be verified
        @type expected_data: Dictionary
        @param event: Contains event details (actual data) to be verified.
        @type event: Dictionary
        @note Pass for now until we have time to implement later
        """
        pass

    def verify_server_event_common_details(self, server, event,
                                           expected_image_metadata):
        """
        @summary: Verifies the common details for all server related events
        @param server: Contains all the expected data to be verified
        @type server: Dictionary
        @param event: Contains event details (actual data) to be verified.
        @type event: Dictionary
        """

        # Needed because of RM3272
        if event.region.upper() == 'PREPROD-ORD':
            self.assertEqual(self.region.upper(), 'ORD',
                             msg="{0}: The expected region does not match "
                             "with the one found in the event."
                             .format(event.event_type))
        else:
            self.assertEqual(self.region.upper(), event.region.upper(),
                             msg="{0}: The expected region does not match "
                             "with the one found in the event."
                             .format(event.event_type))
        self.assertIn(event.datacenter,
                      self.region_datacenter_mapping[event.region],
                      msg="{0}: The expected datacenter does not have a "
                      "corresponding match with the regional datacenters "
                      "found in the event.".format(event.event_type))

        image_id = event.payload.image_ref_url.rsplit('/')[-1]
        self.assertEqual(self.tenant_id, event.payload.tenant_id,
                         msg="{0}: The expected tenant ID does not match "
                         "with the one found in the event."
                         .format(event.event_type))
        self.assertEqual(server.user_id, event.payload.user_id,
                         msg="{0}: The expected user ID does not match "
                         "with the one found in the event."
                         .format(event.event_type))

        flavor_details = self.flavors_client.get_flavor_details(
            server.flavor.id).entity

        flavor_id = server.flavor.id
        total_disk_size = flavor_details.disk

        self.assertEqual(str(flavor_id),
                         str(event.payload.instance_flavor_id),
                         msg="{0}: The expected Flavor ID does not match "
                         "with the instance_flavor_id found in the event."
                         .format(event.event_type))

        # Check for High IO flavor then replace ID with mapping
        if server.flavor.id in self.highio_instance_type_id_dict:
            flavor_id = self.highio_instance_type_id_dict[server.flavor.id]
            total_disk_size = flavor_details.disk + flavor_details.ephemeral
        self.assertEqual(str(flavor_id),
                         str(event.payload.instance_type_id),
                         msg="{0}: The expected Flavor ID does not match "
                         "with the instance_type_id found in the event."
                         .format(event.event_type))
        self.assertEqual(
            flavor_details.name, event.payload.instance_type,
            msg="{0}: The expected Flavor name does not match with "
            "the one found in the event. server.id: {1}"
            .format(event.event_type, server.id))
        self.assertEqual(
            str(flavor_details.ram), str(event.payload.memory_mb),
            msg="{0}: The expected RAM size does not match with the one "
            "found in the event.".format(event.event_type))
        self.assertEqual(
            str(total_disk_size), str(event.payload.disk_gb),
            msg="{0}: The expected Disk size does not match with the one "
            "found in the event. flavor name: {1} flavor id: {2}"
            .format(event.event_type, flavor_details.name, flavor_id))

        self.assertEqual(
            server.id, event.payload.instance_id,
            msg="{0}: The expected Server id does not match with the one "
            "found in the event.".format(event.event_type))
        self.assertEqual(
            server.name, event.payload.display_name,
            msg="{0}: The expected Server name does not match with the one "
            "found in the event.".format(event.event_type))
        self.assertEqual(
            server.image.id, image_id,
            msg="{0}: The expected image ID does not match with the one "
            "found in the event.".format(event.event_type))
        self.assertEqual(
            string_to_datetime(server.created),
            string_to_datetime(event.payload.created_at),
            msg="{0}: The expected creation time for the server does not "
            "match with the one found in the event.".format(event.event_type))
        self.assertEqual(
            expected_image_metadata, event.payload.image_meta,
            msg="{0}: The Image Meta found in the event does not match "
            "the expected Image Metadata.".format(event.event_type))

    def _verify_fixed_ips(self, server, event):
        """
        @summary: Verifies the fixed ips of the event against the expected ips
        @param expected_data: Contains all the expected data to be verified
        @type expected_data: Dictionary
        @param event: Contains event details (actual data) to be verified.
        @type event: Dictionary
        """

        expected_fixed_ips = []
        for address in server.addresses.public.addresses:
            expected_fixed_ips.append(
                self._construct_fixed_ip_dict(address, 'public'))
        for address in server.addresses.private.addresses:
            expected_fixed_ips.append(
                self._construct_fixed_ip_dict(address, 'private'))

        self.assertTrue(
            self._compare_fixed_ips(expected_fixed_ips,
                                    event.payload.fixed_ips),
            msg="{0}: The expected fixed ips and the event fixed ips do not "
            " match\nExpected Fixed IPs: {1} \nEvent Fixed Ips: {2}."
            .format(event.event_type, expected_fixed_ips,
                    event.payload.fixed_ips))

    def _construct_fixed_ip_dict(self, address, label):
        """
        @summary: Constructs a dictionary, with the specified IP address,
            in the same format of the event.
        @return: Fixed IP
        @rtype: Dictionary
        """
        return {"floating_ips": [],
                "meta": {},
                "type": "fixed",
                "version": address.version,
                "address": address.addr,
                "label": label
                }

    def _compare_fixed_ips(self, expected_fixed_ips, actual_fixed_ips):
        """
        @summary: Compares the two lists of fixed ips for equality
        @param expected_fixed_ips: List of the expected fixed IPs
        @type expected_fixed_ips: List of Dictionary
        @param actual_fixed_ips: List of the actual fixed IPs
        @type actual_fixed_ips: List of Dictionary
        @return : True if equal else False
        @rtype: bool
        """
        if expected_fixed_ips is None and actual_fixed_ips is None:
            return True
        if expected_fixed_ips is None or actual_fixed_ips is None:
            return False
        if len(expected_fixed_ips) != len(actual_fixed_ips):
            return False
        index_actual_fixed_ips = {}
        for item in actual_fixed_ips:
            index_actual_fixed_ips[item['address']] = item
        for item in expected_fixed_ips:
            if(item["address"] not in index_actual_fixed_ips or
               item != index_actual_fixed_ips[item["address"]]):
                return False
        return True
