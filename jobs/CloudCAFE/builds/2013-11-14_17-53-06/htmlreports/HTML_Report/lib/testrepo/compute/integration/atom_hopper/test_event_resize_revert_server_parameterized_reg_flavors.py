from datetime import datetime, timedelta

from ccengine.common.constants.compute_constants import Constants
from ccengine.common.dataset_generators import DatasetList
from ccengine.common.decorators import DataDrivenFixture, data_driven_test
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


update_event_expected_data_on_server_resize_revert = [
    {'old_state': 'resized',
     'state_description': '',
     'state': 'active',
     'old_task_state': 'resize_reverting',
     'new_task_state': None},
    {'old_state': 'resized',
     'state_description': 'resize_reverting',
     'state': 'resized',
     'old_task_state': None,
     'new_task_state': 'resize_reverting'},
    {'old_state': None,
     'state_description': 'resize_reverting',
     'state': 'resized',
     'old_task_state': None,
     'new_task_state': 'resize_reverting'}]

expected_events_list = ["compute.instance.exists",
                        "compute.instance.resize.revert.start",
                        "compute.instance.resize.revert.end"]


class StaticFlavorDataGenerator(DatasetList):

    def __init__(self):
        self.config = _MCP()
        self.bw_compute_provider = BandwidthComputeAPIProvider(self.config)
        self.flavors_client = self.bw_compute_provider.flavors_client

        flavor_details_list = (self.flavors_client.list_flavors_with_detail()
                               .entity)

        for (counter, flavor_details) in enumerate(flavor_details_list):
            # Get all Standard flavors except the one that we started with
            if ('Standard' in flavor_details.name and
                    flavor_details.id != self.config.compute_api.flavor_ref):
                dataset = {"flavor": flavor_details}
                test_name = "{0}_{1}".format(
                    str(counter),
                    flavor_details.name.replace(" ", "_"))
                self.append_new_dataset(name=test_name, data_dict=dataset)


@DataDrivenFixture
class RegFlavorEventsResizeRevertServerTest(ComputeFixture, EventsValidator):

    @classmethod
    def setUpClass(cls):
        super(RegFlavorEventsResizeRevertServerTest, cls).setUpClass()
        cls.test_type = cls.config.compute_api.test_type
        cls.flavor_ref = cls.config.compute_api.flavor_ref
        cls.expected_audit_period_beginning = datetime.now().strftime(
            Constants.DATETIME_0AM_FORMAT)
        cls.date_break = datetime.utcnow() - timedelta(hours=1)
        cls.bw_compute_provider = BandwidthComputeAPIProvider(cls.config)
        cls.gb_file_size = cls.config.compute_api.gb_file_size
        cls.highio_instance_type_id_dict = \
            cls.config.compute_api.highio_instance_type_id_dict

    @classmethod
    def tearDownClass(cls):
        super(RegFlavorEventsResizeRevertServerTest, cls).tearDownClass()
        cls.resources.release()
        cls.flavors_client.delete_exception_handler(ExceptionHandler())

    @data_driven_test(StaticFlavorDataGenerator())
    def ddtest_events_triggered_on_resize_revert_instance(self, flavor):

        # Create Server and wait for it to become active
        name = "{0}_{1}".format(rand_name('ts'), self.flavor_ref)
        self.server = self.servers_client.create_server(
            name, self.image_ref, self.flavor_ref).entity
        self.admin_pass = self.server.adminPass
        self.resources.add(self.server.id, self.servers_client.delete_server)
        self.compute_provider.wait_for_server_status(self.server.id,
                                                     status.ACTIVE)
        self.launched_at_created_server = datetime.utcnow()

        # Resize server
        name = "{0}_{1}".format(rand_name('ts'), flavor.id)
        self.servers_client.resize(self.server.id, flavor.id, name)
        resized_server = self.compute_provider.wait_for_server_status(
            self.server.id, status.VERIFY_RESIZE).entity
        self.launched_at_resized_server = datetime.utcnow()
        self.reverted_expected_audit_period_ending = \
            datetime.utcnow().strftime(Constants.DATETIME_FORMAT)

        # Get Server and Image details now for validation in the
        # second immediate exists event
        self.server = self.servers_client.get_server(self.server.id).entity
        self.image = self.images_client.get_image(self.server.image.id).entity

        # Revert Resize server
        self.expected_audit_period_ending = datetime.utcnow().strftime(
            Constants.DATETIME_FORMAT)
        resp = self.servers_client.revert_resize(self.server.id)
        assert resp.status_code is 202
        self.compute_provider.wait_for_server_status(self.server.id,
                                                     status.ACTIVE)
        self.launched_at_reverted_resized_server = datetime.utcnow()

        # Get Resize Reverted Server details
        resize_reverted_server = self.servers_client.get_server(
            self.server.id).entity

        # Set the expected resized events details
        self.expected_data = \
            {'resize_reverted_server': resize_reverted_server,
             'server': self.server,
             'launched_at_in_exists':
                self.launched_at_resized_server.strftime("%Y-%m-%dT%H:%M:%S"),
             'launched_at_create_server':
                self.launched_at_created_server.strftime("%Y-%m-%dT%H:%M:%S"),
             'launched_at_resize_server':
                self.launched_at_resized_server.strftime("%Y-%m-%dT%H:%M:%S"),
             'image_meta': self.image.metadata,
             'update_event_expected_data':
                update_event_expected_data_on_server_resize_revert,
             'audit_period_beginning': self.expected_audit_period_beginning,
             'audit_period_ending': self.expected_audit_period_ending}

        # Set the expected resize event list
        expected_event_types = \
            ['compute.instance.resize.revert.end'] + \
            ['compute.instance.update'] * 3 + \
            ['compute.instance.resize.revert.start'] + \
            ['compute.instance.update'] + \
            ['compute.instance.exists']

        self.get_and_verify_ah_events(
            wait_for_target_timestamp=self.launched_at_created_server,
            wait_for_event_type='compute.instance.resize.revert.end',
            date_break=self.launched_at_resized_server,
            expected_data=self.expected_data,
            expected_event_types=expected_event_types,
            product_type='nova')

        # Generate bandwidth
        self.server.adminPass = self.admin_pass
        self.bw_compute_provider.do_bandwidth_server_to_client(
            self.server, self.gb_file_size)

        # Add verification of exists events to daily bandwidth verifications
        self.assertTrue(self.bw_compute_provider
            .insert_exists_event(
                exists_type='immediate',
                server=self.server,
                audit_period_ending=self.expected_audit_period_ending,
                launched_at=self.launched_at_created_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                state_description='resize_prep'),
            msg="Failed to insert immediate exists event into DB.")
        self.assertTrue(self.bw_compute_provider
            .insert_exists_event(
                exists_type='immediate',
                server=resized_server,
                audit_period_ending=(self
                                     .reverted_expected_audit_period_ending),
                launched_at=self.launched_at_resized_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                state_description='resize_reverting'),
            msg="Failed to insert immediate exists event into DB.")
        self.assertTrue(self.bw_compute_provider
            .insert_exists_event(
                exists_type='periodic',
                server=resized_server,
                launched_at=self.launched_at_reverted_resized_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                gb_file_size=self.gb_file_size),
            msg="Failed to insert periodic exists event into DB.")
