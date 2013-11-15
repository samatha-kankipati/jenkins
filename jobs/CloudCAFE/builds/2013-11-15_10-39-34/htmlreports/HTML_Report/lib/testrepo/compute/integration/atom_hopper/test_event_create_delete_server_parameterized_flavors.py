from datetime import datetime, timedelta

from ccengine.common.dataset_generators import DatasetList
from ccengine.common.decorators import (DataDrivenFixture, data_driven_test)
from ccengine.common.exception_handler.exception_handler import \
    ExceptionHandler
from ccengine.common.tools.datagen import rand_name
from ccengine.providers.compute.bandwidth_compute_api import \
    BandwidthComputeAPIProvider
from ccengine.providers.configuration import MasterConfigProvider as _MCP
from testrepo.common.testfixtures.compute import ComputeFixture
from testrepo.common.testfixtures.atomhopper_events_validator \
    .events_validator import EventsValidator


update_event_expected_data_on_server_creation_dict = [
    {'new_task_state': None,
     'old_state': 'building',
     'old_task_state': 'spawning',
     'state': 'active',
     'state_description': ''},
    {'new_task_state': 'spawning',
     'old_state': 'building',
     'old_task_state': 'block_device_mapping',
     'state': 'building',
     'state_description': 'spawning'},
    {'new_task_state': 'block_device_mapping',
     'old_state': 'building',
     'old_task_state': 'networking',
     'state': 'building',
     'state_description': 'block_device_mapping'},
    {'new_task_state': 'networking',
     'old_state': 'building',
     'old_task_state': None,
     'state': 'building',
     'state_description': 'networking'},
    {'new_task_state': None,
     'old_state': 'building',
     'old_task_state': 'scheduling',
     'state': 'building',
     'state_description': ''},
    {'new_task_state': None,
     'old_state': None,
     'old_task_state': None,
     'state': 'building',
     'state_description': 'scheduling'},
    {'new_task_state': 'spawning',
     'old_state': None,
     'old_task_state': None,
     'state': 'building',
     'state_description': 'spawning'},
    {'new_task_state': None,
     'old_state': 'building',
     'old_task_state': 'spawning',
     'state': 'active',
     'state_description': ''},
    {'new_task_state': 'scheduling',
     'old_state': None,
     'old_task_state': None,
     'state': 'building',
     'state_description': 'scheduling'},
    {'new_task_state': None,
     'old_state': None,
     'old_task_state': None,
     'state': 'building',
     'state_description': ''},
    {'new_task_state': None,
     'old_state': None,
     'old_task_state': None,
     'state': 'active',
     'state_description': ''}]

update_event_expected_data_on_delete_server_dict = [
    {'new_task_state': None,
     'old_state': 'active',
     'old_task_state': 'deleting',
     'state': 'deleted',
     'state_description': ''},
    {'new_task_state': 'deleting',
     'old_state': 'active',
     'old_task_state': None,
     'state': 'active',
     'state_description': 'deleting'},
    {'new_task_state': 'deleting',
     'old_state': 'active',
     'old_task_state': None,
     'state': 'active',
     'state_description': 'deleting'},
    {'new_task_state': 'deleting',
     'old_state': 'active',
     'old_task_state': None,
     'state': 'active',
     'state_description': 'deleting'},
    {'new_task_state': None,
     'old_state': None,
     'old_task_state': None,
     'state': 'deleted',
     'state_description': ''}]

create_events_list = [
    "compute.instance.create.start", "compute.instance.create.end"]

delete_events_list = [
    "compute.instance.delete.start", "compute.instance.delete.end",
    "compute.instance.shutdown.start", "compute.instance.shutdown.end"]


class StaticFlavorDataGenerator(DatasetList):

    def __init__(self):
        self.config = _MCP()
        self.bw_compute_provider = BandwidthComputeAPIProvider(self.config)
        self.flavors_client = self.bw_compute_provider.flavors_client

        flavor_details_list = (self.flavors_client.list_flavors_with_detail()
                               .entity)
        num = 0
        for flavor_details in flavor_details_list:
            dataset = {"flavor": flavor_details}
            test_name = "{0}_{1}".format(str(num),
                                         flavor_details.name.replace(" ", "_"))
            self.append_new_dataset(name=test_name, data_dict=dataset)
            num += 1


@DataDrivenFixture
class FlavorEventsCreateDeleteServerTest(ComputeFixture, EventsValidator):

    @classmethod
    def setUpClass(cls):
        super(FlavorEventsCreateDeleteServerTest, cls).setUpClass()

        cls.date_break = datetime.utcnow() - timedelta(hours=1)
        cls.bw_compute_provider = BandwidthComputeAPIProvider(cls.config)
        cls.gb_file_size = cls.config.compute_api.gb_file_size
        cls.highio_instance_type_id_dict = \
            cls.config.compute_api.highio_instance_type_id_dict

    @classmethod
    def tearDownClass(cls):
        super(FlavorEventsCreateDeleteServerTest, cls).tearDownClass()
        cls.resources.release()
        cls.flavors_client.delete_exception_handler(ExceptionHandler())

    @data_driven_test(StaticFlavorDataGenerator())
    def ddtest_events_triggered_on_create_delete_instance(self, flavor):
        name = "{0}_{1}".format(rand_name('testserver'), flavor.id)

        # Create Server and wait for it to become active
        self.server = self.servers_client.create_server(
            name, self.image_ref, flavor.id).entity
        admin_pass = self.server.adminPass
        self.resources.add(self.server.id, self.servers_client.delete_server)
        self.compute_provider.wait_for_server_status(self.server.id, 'ACTIVE')
        self.launched_at_create_server = datetime.utcnow()

        # Get Server and Image details
        self.server = self.servers_client.get_server(self.server.id).entity
        self.image = self.images_client.get_image(self.server.image.id).entity

        # Set the expected create event details
        self.expected_create_data = \
            {'server': self.server,
             'launched_at_create_server':
                self.launched_at_create_server.strftime("%Y-%m-%dT%H:%M:%S"),
             'update_event_expected_data':
                update_event_expected_data_on_server_creation_dict,
             'image_meta': self.image.metadata}

        # Set the expected create event lists
        expected_event_types = (['compute.instance.create.end'] +
                                ['compute.instance.update'] * 17 +
                                ['compute.instance.create.start',
                                 'compute.instance.update',
                                 'scheduler.run_instance.scheduled',
                                 'compute.instance.update'])

        self.get_and_verify_ah_events(
            wait_for_target_timestamp=self.launched_at_create_server,
            wait_for_event_type='compute.instance.create.end',
            date_break=self.date_break,
            expected_data=self.expected_create_data,
            expected_event_types=expected_event_types,
            atom_hopper_feed_limit=1000,
            atom_hopper_pagination_limit=30,
            product_type='nova')

        # Generate bandwidth
        self.server.adminPass = admin_pass
        self.bw_compute_provider.do_bandwidth_server_to_client(
            self.server, self.gb_file_size)

        # Delete the server and wait for it to be deleted
        self.servers_client.delete_server(self.server.id)
        self.compute_provider.wait_for_server_to_be_deleted(self.server.id)
        self.deleted_at = datetime.utcnow()

        # Get the expected delete event details
        self.expected_delete_data = \
            {'server': self.server,
             'deleted_at': self.deleted_at.strftime("%Y-%m-%dT%H:%M:%S"),
             'launched_at_create_server':
                self.launched_at_create_server.strftime("%Y-%m-%dT%H:%M:%S"),
             'update_event_expected_data':
                (update_event_expected_data_on_delete_server_dict +
                 update_event_expected_data_on_server_creation_dict),
             'image_meta': self.image.metadata}

        # Set the expected create event lists
        expected_event_types = \
            (['compute.instance.delete.end', 'compute.instance.update',
             'compute.instance.shutdown.end',
             'compute.instance.shutdown.start',
             'compute.instance.delete.start', 'compute.instance.update',
             'compute.instance.update', 'compute.instance.update'] +
             expected_event_types)

        self.get_and_verify_ah_events(
            wait_for_target_timestamp=self.deleted_at,
            wait_for_event_type='compute.instance.delete.end',
            date_break=self.date_break,
            expected_data=self.expected_delete_data,
            expected_event_types=expected_event_types,
            atom_hopper_feed_limit=1000,
            atom_hopper_pagination_limit=30,
            product_type='nova')

        # Replace ID with i/o flavor mapping if it exists
        # so that daily exists verifications do not fail falsely
        if self.server.flavor.id in self.highio_instance_type_id_dict:
            self.server.flavor.id = \
                self.highio_instance_type_id_dict[self.server.flavor.id]

        # Add verification of exists event to daily bandwidth verifications
        self.assertTrue(self.bw_compute_provider
            .insert_exists_event(
                exists_type='periodic',
                server=self.server,
                launched_at=self.launched_at_create_server,
                test_name=self._testMethodName,
                test_type=self.config.compute_api.test_type,
                gb_file_size=self.gb_file_size),
            msg="Failed to insert periodic exists event into DB.")
