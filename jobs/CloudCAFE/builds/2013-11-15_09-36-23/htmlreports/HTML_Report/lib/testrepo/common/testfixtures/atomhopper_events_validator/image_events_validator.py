from ccengine.common.tools.datatools import are_datetimestrings_equal
from testrepo.common.testfixtures.fixtures import BaseTestFixture


class ImageEventsValidator(BaseTestFixture):
    """
    @summary: Helper to validate all Image Event details
    """

    @classmethod
    def setUpClass(cls):
        super(ImageEventsValidator, cls).setUpClass()
        cls.tenant_id = cls.config.compute_api.tenant_id
        cls.leeway_for_timestamp = \
            cls.config.compute_api.datetime_seconds_leeway

    def verify_image_delete(self, expected_data, event):
        """
        @summary: Verifies the image.delete details
        @param expected_data: Contains all the expected data to be verified
        @type expected_data: Dictionary
        @param event: Contains event details (actual data) to be verified.
        @type event: Dictionary
        """
        self.assertIsNotNone(event.payload.checksum,
                             msg="{0}: The checksum field was blank."
                             .format(event.event_type))
        self.assertIsNotNone(event.payload.container_format,
                             msg="{0}: The container_format field was blank."
                             .format(event.event_type))
        self.assertTrue(event.payload.deleted,
                        msg="{0}: The deleted field was not set to True"
                        .format(event.event_type))
        expected_deleted_at = expected_data['image_deleted_at']
        self.assertTrue(
            are_datetimestrings_equal(expected_deleted_at,
                                      event.payload.deleted_at,
                                      self.leeway_for_timestamp),
            msg="{0}: The expected deleted_at {1} does not match with the "
            "value found in the event {2}.".format(event.event_type,
                                                   expected_deleted_at,
                                                   event.payload.deleted_at))
        self.assertIsNotNone(event.payload.disk_format,
                             msg="{0}: The disk_format field was blank.")
        self.assertGreater(event.payload.size, 0,
                           msg="{0}: The image size should be greater than 0."
                           .format(event.event_type))
        self.assertEqual(
            event.payload.size, expected_data['image'].size,
            msg="{0}: The image size did not match.\nexpected: {1}"
            "\nactual(from event): {2}".format(event.event_type,
                                               expected_data['image'].size,
                                               event.payload.size))
        self.assertEqual(event.payload.status, 'active',
                         msg="{0}: The status should be active."
                         .format(event.event_type))
        self.verify_image_event_common_details(expected_data['image'], event)

    def verify_image_update(self, expected_data, event):
        """
        @summary: Verifies the image.update details
        @param expected_data: Contains all the expected data to be verified
        @type expected_data: Dictionary
        @param event: Contains event details (actual data) to be verified.
        @type event: Dictionary
        """
        self.assertIsNotNone(event.payload.checksum,
                             msg="{0}: The checksum field was blank."
                             .format(event.event_type))
        self.assertIsNotNone(event.payload.container_format,
                             msg="{0}: The container_format field was blank.")
        self.assertFalse(event.payload.deleted,
                         msg="{0}: The deleted field was not set to False"
                         .format(event.event_type))
        self.assertIsNone(event.payload.deleted_at,
                          msg="{0}: The deleted_at field was not blank."
                          .format(event.event_type))
        self.assertIsNotNone(event.payload.disk_format,
                             msg="{0}: The disk_format field was blank.")
        self.assertGreater(event.payload.size, 0,
                           msg="{0}: The image size should be greater than 0."
                           .format(event.event_type))
        self.assertEqual(
            event.payload.size, expected_data['image'].size,
            msg="{0}: The image size did not match.\nexpected: {1}"
            "\nactual(from event): {2}".format(event.event_type,
                                               expected_data['image'].size,
                                               event.payload.size))
        self.assertEqual(event.payload.status, 'active',
                         msg="{0}: The status should be active."
                         .format(event.event_type))
        self.verify_image_event_common_details(expected_data['image'], event)

    def verify_image_activate(self, expected_data, event):
        """
        @summary: Verifies the image.activate details
        @param expected_data: Contains all the expected data to be verified
        @type expected_data: Dictionary
        @param event: Contains event details (actual data) to be verified.
        @type event: Dictionary
        """
        self.assertIsNotNone(event.payload.checksum,
                             msg="{0}: The checksum field was not blank."
                             .format(event.event_type))
        self.assertIsNotNone(event.payload.container_format,
                             msg="{0}: The container_format field was blank.")
        self.assertFalse(event.payload.deleted,
                         msg="{0}: The deleted field was not set to False"
                         .format(event.event_type))
        self.assertIsNone(event.payload.deleted_at,
                          msg="{0}: The deleted_at field was not blank."
                          .format(event.event_type))
        self.assertIsNotNone(event.payload.disk_format,
                             msg="{0}: The disk_format field was blank.")
        self.assertGreater(event.payload.size, 0,
                           msg="{0}: The image size should be greater than 0."
                           .format(event.event_type))
        self.assertEqual(
            event.payload.size, expected_data['image'].size,
            msg="{0}: The image size did not match.\nexpected: {1}"
            "\nactual(from event): {2}".format(event.event_type,
                                               expected_data['image'].size,
                                               event.payload.size))
        self.assertEqual(event.payload.status, 'active',
                         msg="{0}: The status should be active."
                         .format(event.event_type))
        self.verify_image_event_common_details(expected_data['image'], event)

    def verify_image_upload(self, expected_data, event):
        """
        @summary: Verifies the image.upload details
        @param expected_data: Contains all the expected data to be verified
        @type expected_data: Dictionary
        @param event: Contains event details (actual data) to be verified.
        @type event: Dictionary
        """
        self.assertIsNotNone(event.payload.checksum,
                             msg="{0}: The checksum field was blank."
                             .format(event.event_type))
        self.assertIsNotNone(event.payload.container_format,
                             msg="{0}: The container_format field was blank.")
        self.assertFalse(event.payload.deleted,
                         msg="{0}: The deleted field was not set to False"
                         .format(event.event_type))
        self.assertIsNone(event.payload.deleted_at,
                          msg="{0}: The deleted_at field was not blank."
                          .format(event.event_type))
        self.assertIsNotNone(event.payload.disk_format,
                             msg="{0}: The disk_format field was blank.")
        self.assertGreater(event.payload.size, 0,
                           msg="{0}: The image size should be greater than 0."
                           .format(event.event_type))
        self.assertEqual(
            event.payload.size, expected_data['image'].size,
            msg="{0}: The image size did not match.\nexpected: {1}"
            "\nactual(from event): {2}".format(event.event_type,
                                               expected_data['image'].size,
                                               event.payload.size))
        self.assertEqual(event.payload.status, 'saving',
                         msg="{0}: The status should be saving."
                         .format(event.event_type))
        self.verify_image_event_common_details(expected_data['image'], event)

    def verify_image_prepare(self, expected_data, event):
        """
        @summary: Verifies the image.prepare details
        @param expected_data: Contains all the expected data to be verified
        @type expected_data: Dictionary
        @param event: Contains event details (actual data) to be verified.
        @type event: Dictionary
        """
        self.assertIsNone(event.payload.checksum,
                          msg="{0}: The checksum field was not blank."
                          .format(event.event_type))
        self.assertIsNotNone(event.payload.container_format,
                             msg="{0}: The container_format field was blank.")
        self.assertFalse(event.payload.deleted,
                         msg="{0}: The deleted field was not set to False"
                         .format(event.event_type))
        self.assertIsNone(event.payload.deleted_at,
                          msg="{0}: The deleted_at field was not blank."
                          .format(event.event_type))
        self.assertIsNotNone(event.payload.disk_format,
                             msg="{0}: The disk_format field was blank.")
        self.assertEqual(event.payload.size, 0,
                         msg="{0}: The image size should be 0."
                         .format(event.event_type))
        self.assertEqual(event.payload.status, 'queued',
                         msg="{0}: The status should be queued."
                         .format(event.event_type))
        self.verify_image_event_common_details(expected_data['image'], event)

    def verify_image_create(self, expected_data, event):
        """
        @summary: Verifies the image.create details
        @param expected_data: Contains all the expected data to be verified
        @type expected_data: Dictionary
        @param event: Contains event details (actual data) to be verified.
        @type event: Dictionary
        """
        self.assertIsNone(event.payload.checksum,
                          msg="{0}: The checksum field was not blank."
                          .format(event.event_type))
        self.assertIsNone(event.payload.container_format,
                          msg="{0}: The container_format field was not blank.")
        self.assertFalse(event.payload.deleted,
                         msg="{0}: The deleted field was not set to False"
                         .format(event.event_type))
        self.assertIsNone(event.payload.deleted_at,
                          msg="{0}: The deleted_at field was not blank."
                          .format(event.event_type))
        self.assertIsNone(event.payload.disk_format,
                          msg="{0}: The disk_format field was not blank.")
        self.assertEqual(event.payload.size, 0,
                         msg="{0}: The image size should be 0."
                         .format(event.event_type))
        self.assertEqual(event.payload.status, 'queued',
                         msg="{0}: The status should be queued."
                         .format(event.event_type))
        self.verify_image_event_common_details(expected_data['image'], event)

    def verify_image_send(self, expected_data, event):
        """
        @summary: Verifies the image.send details
        @param expected_data: Contains all the expected data to be verified
        @type expected_data: Dictionary
        @param event: Contains event details (actual data) to be verified.
        @type event: Dictionary
        @note Placeholder for now
        """
        raise NotImplementedError("Not Implemented!")

    def verify_image_event_common_details(self, image, event):
        """
        @summary: Verifies the common details for all image related events
        @param image: Contains all the expected data to be verified
        @type image: Dictionary
        @param event: Contains event details (actual data) to be verified.
        @type event: Dictionary
        """
        self.assertEqual(
            image.id, event.payload.id,
            msg="{0}: The image id found in the event does not match the "
            "expected one.".format(event.event_type))
        self.assertFalse(
            event.payload.is_public,
            msg="{0}: The is_public field was not set to False")
        self.assertEqual(
            image.minDisk, event.payload.min_disk,
            msg="{0}: The min_disk value found in the event does not match "
            "the expected one.".format(event.event_type))
        self.assertEqual(
            image.minRam, event.payload.min_ram,
            msg="{0}: The min_ram value found in the event does not match "
            "the expected one.".format(event.event_type))
        self.assertEqual(
            image.name, event.payload.name,
            msg="{0}: The image name found in the event does not match the "
            "expected one.".format(event.event_type))
        self.assertEqual(
            self.tenant_id, event.payload.owner,
            msg="{0}: The tenant id found in the event does not match the "
            "expected one.".format(event.event_type))
        self.assertEqual(
            image.metadata, event.payload.properties,
            msg="{0}: The Properties found in the event does not match "
            "the expected one.".format(event.event_type))
        self.assertFalse(event.payload.protected,
                         msg="{0}: The protected field was not set to False")
        # a migrated image from first gen has no server 
        if hasattr(image, "server"):
            self.assertEqual(
                image.server.id, event.payload.properties.instance_uuid,
                msg="{0}: The ID of the server found in the event does not "
                "match the expected one.".format(event.event_type))
        self.assertTrue(
            are_datetimestrings_equal(image.created, event.payload.created_at),
            msg="{0}: The expected creation time for the server does not "
            "match with the one found in the event".format(event.event_type))
