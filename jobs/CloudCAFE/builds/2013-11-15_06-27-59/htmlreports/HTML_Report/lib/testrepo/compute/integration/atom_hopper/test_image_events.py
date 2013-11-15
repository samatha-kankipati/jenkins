from datetime import datetime, timedelta

from ccengine.common.decorators import attr
from ccengine.common.tools.datagen import rand_name
from ccengine.domain.types import NovaImageStatusTypes as Status
from testrepo.common.testfixtures.atomhopper_events_validator\
    .events_validator import EventsValidator
from testrepo.common.testfixtures.compute import ComputeFixture


class ImageEventsTest(ComputeFixture, EventsValidator):

    @classmethod
    def setUpClass(cls):
        super(ImageEventsTest, cls).setUpClass()
        cls.server = cls.compute_provider.create_active_server().entity
        cls.resources.add(cls.server.id, cls.servers_client.delete_server)
        cls.date_break = datetime.utcnow() - timedelta(hours=1)
        cls.file_size = cls.config.compute_api.snapshot_gb_file_size
        cls.server_filepath = "/root/" + rand_name('file.')

    @attr('images_events')
    def test_events_triggered_on_create_delete_image(self):
        """
        @summary: Test image events with image creation and deletion
        @todo: Add tests for image.activate
            (i.e., calls to migrate from legacy)
        """
        # Get initial size
        image = self.images_client.get_image(self.server.image.id).entity
        initial_image_size = image.size
        self.fixture_log.info("inital image size: {0}".format(
            initial_image_size))

        # Create file on server
        instance_client = self.compute_provider.get_remote_instance_client(
            self.server)
        instance_client.create_a_file_on_server(filepath=self.server_filepath,
                                                multiplier=self.file_size)

        # Create image snapshot and wait for active status
        name = rand_name('image')
        image_response = self.servers_client.create_image(
            self.server.id, name)
        image_id = self.parse_image_id(image_response)
        self.compute_provider.wait_for_image_status(image_id, Status.ACTIVE)
        image = self.images_client.get_image(image_id).entity

        # Check if final size is more than the original size
        final_image_size = image.size
        self.fixture_log.info("final image size: {0}".format(
            final_image_size))
        self.fixture_log.info("difference: {0}".format(
            final_image_size - initial_image_size))
        self.assertGreater(final_image_size, initial_image_size,
                           "The size of the snapshot was not greater than "
                           "the original size.")

        # Delete image
        deleted_at = datetime.utcnow()
        self.images_client.delete_image(image.id).entity
        self.compute_provider.wait_for_image_to_be_deleted(image.id)
        self.glance_atomhopper_provider.wait_for_atomhopper_timestamp(
            deleted_at)

        # Verify actual events
        expected_data = {'image': image,
                         'image_deleted_at':
                         deleted_at.strftime("%Y-%m-%dT%H:%M:%S")}
        # Check event counts in order
        expected_event_types = ["image.delete", "image.update",
                                "image.update", "image.activate",
                                "image.upload", "image.prepare",
                                "image.create"
                                ]
        self.get_and_verify_ah_events(
            wait_for_timestamp=deleted_at,
            date_break=self.date_break,
            expected_data=expected_data,
            expected_event_types=expected_event_types)
