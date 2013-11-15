from datetime import datetime, timedelta

from ccengine.common.tools.datagen import rand_name
from ccengine.domain.types import NovaImageStatusTypes as Status
from ccengine.providers.legacyserv.server_api import \
    ServerProvider as LegacyServerProvider
from testrepo.common.testfixtures.atomhopper_events_validator\
    .events_validator import EventsValidator
from testrepo.common.testfixtures.compute import ComputeFixture


class LegacyImageSnapshotToNextGenEventsTest(ComputeFixture, EventsValidator):

    @classmethod
    def setUpClass(cls):
        super(LegacyImageSnapshotToNextGenEventsTest, cls).setUpClass()

        cls.date_break = datetime.utcnow() - timedelta(hours=1)

    def test_events_triggered_on_create_delete_image(self):
        """
        @summary: Test image events with an instance image created in Legacy,
            which is saved to Next Gen
        """

        # create server in first gen
        self.legacy_api_provider = LegacyServerProvider(self.config,
                                                        self.fixture_log)
        self.legacy_server = (self.legacy_api_provider
                             .create_active_server().entity)
        self.resources.add(self.legacy_server.id,
                           self.legacy_api_provider.client.delete_server)

        # create legacy snapshot to nextgen and wait for active status
        name = rand_name('legacy2nextgen_image')
        self.created_at = datetime.utcnow()
        image_resp = self.legacy_api_provider.client.create_next_gen_image(
            server_id=self.legacy_server.id, name=name)
        next_gen_image_id = image_resp.entity.next_gen_uuid

        # if we failed here then check that the AH error events are correct
        # the call to the API should also give the errored image details
        self.compute_provider.wait_for_image_status(next_gen_image_id,
                                                    Status.ACTIVE)
        self.image = self.images_client.get_image(next_gen_image_id).entity

        # Get expected data for verification
        expected_data = {'image': self.image,
                         'image_created_at':
                         self.created_at.strftime("%Y-%m-%dT%H:%M:%S")}
        expected_event_types = ["image.update", "image.update",
                                "image.activate", "image.create"]
        self.get_and_verify_ah_events(
            wait_for_timestamp=self.created_at,
            wait_for_event="image.activate",
            date_break=self.date_break,
            expected_data=expected_data,
            expected_event_types=expected_event_types)

        # Delete image through Next Gen API
        self.deleted_at = datetime.utcnow()
        self.images_client.delete_image(self.image.id)
        self.compute_provider.wait_for_image_to_be_deleted(self.image.id)

        # Get expected data for verification
        expected_data = {'image': self.image,
                         'image_deleted_at':
                         self.deleted_at.strftime("%Y-%m-%dT%H:%M:%S")}
        expected_event_types = ["image.delete", "image.update",
                                "image.update", "image.activate",
                                "image.create"
                                ]
        self.get_and_verify_ah_events(
            wait_for_timestamp=self.deleted_at,
            wait_for_event="image.delete",
            date_break=self.date_break,
            expected_data=expected_data,
            expected_event_types=expected_event_types)
