from datetime import datetime, timedelta

from ccengine.common.constants.compute_constants import Constants
from ccengine.common.dataset_generators import DatasetList
from ccengine.common.decorators import (DataDrivenFixture, data_driven_test)
from ccengine.common.exception_handler.exception_handler import \
    ExceptionHandler
from ccengine.common.tools.datagen import rand_name
from ccengine.domain.types import NovaServerStatusTypes as status
from ccengine.providers.compute.bandwidth_compute_api import \
    BandwidthComputeAPIProvider
from ccengine.providers.configuration import MasterConfigProvider as _MCP
from testrepo.common.testfixtures.atomhopper_events_validator \
    .events_validator import EventsValidator
from testrepo.common.testfixtures.compute import ComputeFixture


update_event_expected_data_on_rebuild_server_dicts = [
    {'new_task_state': 'rebuilding',
     'old_state': 'active',
     'old_task_state': None,
     'state': 'active',
     'state_description': 'rebuilding'},
    {'new_task_state': 'rebuild_block_device_mapping',
     'old_state': 'active',
     'old_task_state': 'rebuilding',
     'state': 'active',
     'state_description': 'rebuild_block_device_mapping'},
    {'new_task_state': 'rebuild_spawning',
     'old_state': 'active',
     'old_task_state': 'rebuild_block_device_mapping',
     'state': 'active',
     'state_description': 'rebuild_spawning'},
    {'new_task_state': None,
     'old_state': 'active',
     'old_task_state': 'rebuild_spawning',
     'state': 'active',
     'state_description': ''},
    {'new_task_state': 'rebuilding',
     'old_state': None,
     'old_task_state': None,
     'state': 'active',
     'state_description': 'rebuilding'},
    {'new_task_state': 'rebuild_spawning',
     'old_state': None,
     'old_task_state': None,
     'state': 'active',
     'state_description': 'rebuild_spawning'},
    {'new_task_state': None,
     'old_state': None,
     'old_task_state': None,
     'state': 'active',
     'state_description': ''}]

rebuild_server_event_list = [
    "compute.instance.exists", "compute.instance.rebuild.start",
    "compute.instance.rebuild.end"]


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
class FlavorEventsRebuildServerTest(ComputeFixture, EventsValidator):

    @classmethod
    def setUpClass(cls):
        super(FlavorEventsRebuildServerTest, cls).setUpClass()
        cls.test_type = cls.config.compute_api.test_type
        cls.expected_audit_period_beginning = datetime.now().strftime(
            Constants.DATETIME_0AM_FORMAT)
        cls.date_break = datetime.utcnow() - timedelta(hours=1)
        cls.bw_compute_provider = BandwidthComputeAPIProvider(cls.config)
        cls.gb_file_size = cls.config.compute_api.gb_file_size
        cls.highio_instance_type_id_dict = \
            cls.config.compute_api.highio_instance_type_id_dict

    @classmethod
    def tearDownClass(cls):
        super(FlavorEventsRebuildServerTest, cls).tearDownClass()
        cls.resources.release()
        cls.flavors_client.delete_exception_handler(ExceptionHandler())

    @data_driven_test(StaticFlavorDataGenerator())
    def ddtest_events_triggered_on_rebuild_instance(self, flavor):
        name = "{0}_{1}".format(rand_name('ts'), flavor.id)

        # Create Server and wait for it to become active
        self.server = self.servers_client.create_server(
            name, self.image_ref, flavor.id).entity
        admin_pass = self.server.adminPass
        self.resources.add(self.server.id, self.servers_client.delete_server)
        self.compute_provider.wait_for_server_status(self.server.id,
                                                     status.ACTIVE)
        self.launched_at_created_server = datetime.utcnow()

        # Get Server and Image details
        self.server = self.servers_client.get_server(self.server.id).entity
        self.image = self.images_client.get_image(self.server.image.id).entity

        self.expected_audit_period_ending = datetime.utcnow().strftime(
            Constants.DATETIME_FORMAT)
        # Rebuild server and wait for it to become active
        self.servers_client.rebuild(self.server.id, self.image_ref_alt,
                                    admin_pass=admin_pass)
        self.rebuilt_server = self.compute_provider.wait_for_server_status(
            self.server.id, status.ACTIVE).entity
        self.launched_at_rebuilt_server = datetime.utcnow()

        # Get Server and Image details
        self.rebuilt_server = self.servers_client.get_server(
            self.server.id).entity
        self.image_rebuilt_server = self.images_client.get_image(
            self.rebuilt_server.image.id).entity

        # Set the expected rebuild events details
        self.expected_data = \
            {'server_after_rebuild': self.rebuilt_server,
             'server': self.server,
             'launched_at_in_exists':
                self.launched_at_created_server.strftime("%Y-%m-%dT%H:%M:%S"),
             'launched_at_in_rebuild':
                self.launched_at_rebuilt_server.strftime("%Y-%m-%dT%H:%M:%S"),
             'image_meta': self.image.metadata,
             'update_event_expected_data':
                update_event_expected_data_on_rebuild_server_dicts,
             'rebuilt_server_image_meta': self.image_rebuilt_server.metadata,
             'audit_period_beginning': self.expected_audit_period_beginning,
             'audit_period_ending': self.expected_audit_period_ending}

        # Set the expected rebuild event lists
        expected_event_types = (['compute.instance.rebuild.end'] +
                                ['compute.instance.update'] * 14 +
                                ['compute.instance.rebuild.start',
                                 'compute.instance.exists'])

        self.get_and_verify_ah_events(
            wait_for_target_timestamp=self.launched_at_rebuilt_server,
            wait_for_event_type='compute.instance.rebuild.end',
            date_break=self.launched_at_rebuilt_server,
            expected_data=self.expected_data,
            expected_event_types=expected_event_types,
            product_type='nova')

        # Generate bandwidth
        self.server.adminPass = admin_pass
        self.bw_compute_provider.do_bandwidth_server_to_client(
            self.server, self.gb_file_size)

        # Delete the server and wait for it to be deleted
        self.servers_client.delete_server(self.server.id)
        self.compute_provider.wait_for_server_to_be_deleted(self.server.id)

        # Replace ID with high i/o flavor mapping if it exists
        # so that daily exists verifications do not fail falsely
        if self.server.flavor.id in self.highio_instance_type_id_dict:
            self.server.flavor.id = \
                self.highio_instance_type_id_dict[self.server.flavor.id]

        if self.rebuilt_server.flavor.id in self.highio_instance_type_id_dict:
            self.rebuilt_server.flavor.id = \
                self.highio_instance_type_id_dict[
                    self.rebuilt_server.flavor.id]

        # Add verification of exists events to daily bandwidth verifications
        self.assertTrue(self.bw_compute_provider
            .insert_exists_event(
                exists_type='immediate',
                server=self.server,
                audit_period_ending=self.expected_audit_period_ending,
                launched_at=self.launched_at_created_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                state_description='rebuilding'),
            msg="Failed to insert immediate exists event into DB.")
        self.assertTrue(self.bw_compute_provider
            .insert_exists_event(
                exists_type='periodic',
                server=self.rebuilt_server,
                launched_at=self.launched_at_rebuilt_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                gb_file_size=self.gb_file_size),
            msg="Failed to insert periodic exists event into DB.")
