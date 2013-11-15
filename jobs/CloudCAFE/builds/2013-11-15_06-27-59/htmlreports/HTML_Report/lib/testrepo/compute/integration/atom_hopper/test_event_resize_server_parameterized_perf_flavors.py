from datetime import datetime, timedelta

from ccengine.common.dataset_generators import DatasetList
from ccengine.common.decorators import (DataDrivenFixture, data_driven_test)
from ccengine.common.exception_handler.exception_handler import \
    ExceptionHandler
from ccengine.common.exceptions.compute import Forbidden
from ccengine.common.tools.datagen import rand_name
from ccengine.domain.types import NovaServerStatusTypes as status
from ccengine.providers.compute.bandwidth_compute_api import \
    BandwidthComputeAPIProvider
from ccengine.providers.configuration import MasterConfigProvider as _MCP
from testrepo.common.testfixtures.atomhopper_events_validator \
    .events_validator import EventsValidator
from testrepo.common.testfixtures.compute import ComputeFixture


class StaticFlavorDataGenerator(DatasetList):

    def __init__(self):
        self.config = _MCP()
        self.bw_compute_provider = BandwidthComputeAPIProvider(self.config)
        self.flavors_client = self.bw_compute_provider.flavors_client

        flavor_details_list = (self.flavors_client.list_flavors_with_detail()
                               .entity)
        for (counter, flavor_details) in enumerate(flavor_details_list):
            if 'Performance' in flavor_details.name:
                dataset = {"flavor": flavor_details}
                test_name = "{0}_{1}".format(
                    str(counter),
                    flavor_details.name.replace(" ", "_"))
                self.append_new_dataset(name=test_name, data_dict=dataset)


@DataDrivenFixture
class PerfFlavorEventsResizeServerTest(ComputeFixture, EventsValidator):

    @classmethod
    def setUpClass(cls):
        super(PerfFlavorEventsResizeServerTest, cls).setUpClass()
        cls.test_type = cls.config.compute_api.test_type
        cls.bw_compute_provider = BandwidthComputeAPIProvider(cls.config)
        cls.date_break = datetime.utcnow() - timedelta(hours=1)
        cls.gb_file_size = cls.config.compute_api.gb_file_size
        cls.highio_instance_type_id_dict = \
            cls.config.compute_api.highio_instance_type_id_dict

    @classmethod
    def tearDownClass(cls):
        super(PerfFlavorEventsResizeServerTest, cls).tearDownClass()
        cls.resources.release()
        cls.flavors_client.delete_exception_handler(ExceptionHandler())

    @data_driven_test(StaticFlavorDataGenerator())
    def ddtest_events_triggered_on_resize_instance(self, flavor):
        name = "{0}_{1}".format(rand_name('ts'), flavor.id)

        # Create Server and wait for it to become active
        self.server = self.servers_client.create_server(
            name, self.image_ref, flavor.id).entity
        self.resources.add(self.server.id, self.servers_client.delete_server)
        self.compute_provider.wait_for_server_status(self.server.id,
                                                     status.ACTIVE)
        self.launched_at_created_server = datetime.utcnow()

        # Get Server and Image details
        self.server = self.servers_client.get_server(self.server.id).entity
        self.image = self.images_client.get_image(self.server.image.id).entity

        # Resize server
        self.flavors_client = self.bw_compute_provider.flavors_client
        flavor_details_list = (self.flavors_client.list_flavors_with_detail()
                               .entity)
        for flavor_details in flavor_details_list:
            if flavor.id != flavor_details.id:
                # check that we cannot resize to a perf flavor
                with self.assertRaises(Forbidden):
                    self.servers_client.resize(self.server.id,
                                               flavor_details.id)

        # Wait for AH to update with entries
        self.nova_atomhopper_provider.wait_for_atomhopper_timestamp(
            self.launched_at_created_server)

        # Get all actual events
        actual_events = \
            self.nova_atomhopper_provider.search_compute_events_by_attribute(
                attribute='instance_id', attribute_regex=self.server.id,
                date_break=self.date_break)

        # Check that we didn't get any resize events
        for event in actual_events:
            assert "resize" not in event.event_type
            assert "exists" not in event.event_type

        # Add verification of exists event to daily bandwidth verifications
        self.assertTrue(self.bw_compute_provider
            .insert_exists_event(
                exists_type='periodic',
                server=self.server,
                launched_at=self.launched_at_created_server,
                test_name=self._testMethodName,
                test_type=self.config.compute_api.test_type),
            msg="Failed to insert periodic exists event into DB.")
