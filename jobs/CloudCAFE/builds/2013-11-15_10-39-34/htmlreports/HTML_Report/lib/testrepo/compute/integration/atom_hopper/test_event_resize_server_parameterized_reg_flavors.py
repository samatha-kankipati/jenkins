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


update_event_expected_data_on_server_resize_dict = [
    {'new_task_state': 'resize_migrating',
     'old_state': 'active',
     'old_task_state': 'resize_prep',
     'state': 'active',
     'state_description': 'resize_migrating'},
    {'new_task_state': 'resize_migrated',
     'old_state': 'active',
     'old_task_state': 'resize_migrating',
     'state': 'active',
     'state_description': 'resize_migrated'},
    {'new_task_state': 'resize_finish',
     'old_state': 'active',
     'old_task_state': 'resize_migrated',
     'state': 'active',
     'state_description': 'resize_finish'},
    {'new_task_state': 'resize_prep',
     'old_state': 'active',
     'old_task_state': None,
     'state': 'active',
     'state_description': 'resize_prep'},
    {'new_task_state': None,
     'old_state': 'active',
     'old_task_state': 'resize_finish',
     'state': 'resized',
     'state_description': ''},
    {'new_task_state': 'resize_finish',
     'old_state': None,
     'old_task_state': None,
     'state': 'active',
     'state_description': 'resize_finish'},
    {'new_task_state': 'resize_migrated',
     'old_state': None,
     'old_task_state': None,
     'state': 'active',
     'state_description': 'resize_migrated'},
    {'new_task_state': 'resize_migrating',
     'old_state': None,
     'old_task_state': None,
     'state': 'active',
     'state_description': 'resize_migrating'},
    {'new_task_state': None,
     'old_state': 'resized',
     'old_task_state': None,
     'state': 'active',
     'state_description': ''},
    {'new_task_state': None,
     'old_state': None,
     'old_task_state': None,
     'state': 'resized',
     'state_description': ''},
    {'new_task_state': 'resize_prep',
     'old_state': None,
     'old_task_state': None,
     'state': 'active',
     'state_description': 'resize_prep'}]

expected_event_list = ["compute.instance.exists",
                       "compute.instance.resize.prep.start",
                       "compute.instance.finish_resize.start",
                       "compute.instance.finish_resize.end",
                       "compute.instance.resize.prep.end",
                       "compute.instance.resize.start",
                       "compute.instance.resize.end"]


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
class RegFlavorEventsResizeServerTest(ComputeFixture, EventsValidator):

    @classmethod
    def setUpClass(cls):
        super(RegFlavorEventsResizeServerTest, cls).setUpClass()
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
        super(RegFlavorEventsResizeServerTest, cls).tearDownClass()
        cls.resources.release()
        cls.flavors_client.delete_exception_handler(ExceptionHandler())

    @data_driven_test(StaticFlavorDataGenerator())
    def ddtest_events_triggered_on_resize_instance(self, flavor):

        # Create Server and wait for it to become active
        name = "{0}_{1}".format(rand_name('ts'), self.flavor_ref)
        self.server = self.servers_client.create_server(
            name, self.image_ref, self.flavor_ref).entity
        self.admin_pass = self.server.adminPass
        self.resources.add(self.server.id, self.servers_client.delete_server)
        self.compute_provider.wait_for_server_status(self.server.id,
                                                     status.ACTIVE)
        self.launched_at_created_server = datetime.utcnow()

        # Get Server and Image details
        self.server = self.servers_client.get_server(self.server.id).entity
        self.image = self.images_client.get_image(self.server.image.id).entity

        self.expected_audit_period_ending = datetime.utcnow().strftime(
            Constants.DATETIME_FORMAT)

        # Resize server
        self.expected_audit_period_ending = datetime.utcnow().strftime(
            Constants.DATETIME_FORMAT)
        name = "{0}_{1}".format(rand_name('ts'), flavor.id)
        self.servers_client.resize(self.server.id, flavor.id, name)
        resized_server = self.compute_provider.wait_for_server_status(
            self.server.id, status.VERIFY_RESIZE).entity
        self.launched_at_resized_server = datetime.utcnow()

        resp = self.servers_client.confirm_resize(resized_server.id)
        assert resp.status_code is 204
        resized_server = self.compute_provider.wait_for_server_status(
            self.server.id, status.ACTIVE)

        # Get Resized Server details
        resized_server = self.servers_client.get_server(
            self.server.id).entity

        # Set the expected resized events details
        self.expected_data = \
            {'resized_server': resized_server,
             'server': self.server,
             'launched_at_in_exists':
                self.launched_at_created_server.strftime("%Y-%m-%dT%H:%M:%S"),
             'launched_at_resize_server':
                self.launched_at_resized_server.strftime("%Y-%m-%dT%H:%M:%S"),
             'expected_new_instance_type_id': flavor.id,
             'expected_new_instance_type': flavor.name,
             'image_meta': self.image.metadata,
             'update_event_expected_data':
                update_event_expected_data_on_server_resize_dict,
             'audit_period_beginning': self.expected_audit_period_beginning,
             'audit_period_ending': self.expected_audit_period_ending}

        # Set the expected resize event list
        expected_event_types = \
            ['compute.instance.resize.confirm.end'] + \
            ['compute.instance.update'] * 2 + \
            ['compute.instance.resize.confirm.start'] + \
            ['compute.instance.finish_resize.end'] + \
            ['compute.instance.update'] * 2 + \
            ['compute.instance.finish_resize.start'] + \
            ['compute.instance.update'] * 2 + \
            ['compute.instance.resize.end'] + \
            ['compute.instance.update'] * 7 + \
            ['compute.instance.resize.start'] + \
            ['compute.instance.update'] + \
            ['compute.instance.resize.prep.end'] + \
            ['compute.instance.update'] + \
            ['compute.instance.resize.prep.start'] + \
            ['compute.instance.update'] + \
            ['compute.instance.exists']

        self.get_and_verify_ah_events(
            wait_for_target_timestamp=self.launched_at_created_server,
            wait_for_event_type='compute.instance.resize.confirm.end',
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
                exists_type='periodic',
                server=resized_server,
                launched_at=self.launched_at_resized_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                gb_file_size=self.gb_file_size),
            msg="Failed to insert periodic exists event into DB.")
