from testrepo.common.testfixtures.images import BaseImagesFixture
from ccengine.common.constants.images_constants import Constants
from ccengine.domain.types import ScheduledImagesJobStatus
from ccengine.domain.types import NovaServerStatusTypes
from ccengine.common.decorators import attr
import ccengine.common.tools.datagen as datagen
from datetime import datetime, timedelta


class TestQonosSetScheduleMetadata(BaseImagesFixture):

    @classmethod
    def setUpClass(cls):
        '''Creates the server instances used for all tests in this class'''

        super(TestQonosSetScheduleMetadata, cls).setUpClass()

        count = 2
        servers = []

        for x in range(count):
            server_name = datagen.random_string(size=10)
            server_obj = cls.images_provider.create_server_no_wait(server_name)
            servers.append(server_obj.entity)

        cls.instance_id = servers[0].id
        cls.alt_instance_id = servers[1].id

        for server in servers:
            cls.images_provider.\
                wait_for_server_status(server.id,
                                       NovaServerStatusTypes.ACTIVE)

    @attr('positive')
    def test_happy_path_set_schedule_metadata(self):
        '''Happy Path - Set valid schedule metadata'''

        """
        1) Create a schedule without schedule metadata
        2) Set schedule metadata for the schedule using a valid key value
            pair in the body
        3) Verify that the response code is 200
        4) Get the schedule
        5) Verify that the schedule contains the schedule metadata with auto
            generated attributes and values

        Attributes to verify:
            key
            value
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        key = self.config.images.metadata_key
        value = datagen.random_string(size=10)
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        keys = [key]
        values = [value]

        sch_metadata_obj = \
            self.images_provider.schedules_client.set_schedule_metadata(sch.id,
                                                                        keys,
                                                                        values)
        self.assertEquals(sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_metadata_obj.status_code))

        sch_metadata = sch_metadata_obj.entity

        # Assert that the schedule meta is created as expected
        self.assertEquals(sch_metadata, {key: value},
                          msg.format('key-value', {key: value}, sch_metadata))

        get_sch_obj = \
            self.images_provider.schedules_client.get_schedule(sch.id)
        self.assertEquals(get_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     get_sch_obj.status_code))

        get_sch_metadata = get_sch_obj.entity.metadata

        # Assert that the schedule meta matches the get schedule's data
        self.assertEquals(get_sch_metadata, {key: value},
                          msg.format('key-value', {key: value},
                                     get_sch_metadata))

    @attr('positive')
    def test_happy_path_append_schedule_metadata(self):
        '''Happy Path - Append schedule metadata'''

        """
        1) Create a schedule without schedule metadata
        2) Set schedule metadata for the schedule using a valid key value
            pair in the body
        3) Verify that the response code is 200
        4) Set schdule metadata for the same schedule using different
            schedule metadata
        5) Verify that the schedule contains both schedule metadata with auto
            generated attributes and values

        Attributes to verify:
            key
            value
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        key = self.config.images.metadata_key
        value = datagen.random_string(size=10)
        alt_key = self.config.images.alt_metadata_key
        alt_value = datagen.random_string(size=10)
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        keys = [key]
        values = [value]

        sch_metadata_obj = \
            self.images_provider.schedules_client.set_schedule_metadata(sch.id,
                                                                        keys,
                                                                        values)
        self.assertEquals(sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_metadata_obj.status_code))

        keys = [key, alt_key]
        values = [value, alt_value]

        new_metadata_obj = \
            self.images_provider.schedules_client.set_schedule_metadata(sch.id,
                                                                        keys,
                                                                        values)
        self.assertEquals(new_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     new_metadata_obj.status_code))

        get_sch_obj = \
            self.images_provider.schedules_client.get_schedule(sch.id)
        self.assertEquals(get_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     get_sch_obj.status_code))

        get_sch_metadata = get_sch_obj.entity.metadata

        self.assertTrue(len(get_sch_metadata) == 2,
                        msg.format("number of key-value pairs", 2,
                                   len(get_sch_metadata)))

        get_sch_metadata = get_sch_obj.entity.metadata

        for metadata_key, metadata_value in get_sch_metadata.items():
            if metadata_key == key:
                self.assertEquals(metadata_value, value,
                                  msg.format('value', value, metadata_value))
            elif metadata_key == alt_key:
                self.assertEquals(metadata_value, alt_value,
                                  msg.format('alt_value', alt_value,
                                             metadata_value))
            else:
                self.assertEquals(metadata_key, key,
                                  msg.format('key', key, metadata_key))
                self.assertEquals(metadata_key, alt_key,
                                  msg.format('key', alt_key, metadata_key))

    @attr('positive')
    def test_set_an_empty_schedule_metadata(self):
        '''Set an empty schedule metadata'''

        """
        1) Create a schedule
        2) Set an empty schedule metadata
        3) Verify that the response code is 200
        4) List schedule metadata
        5) Verify that the response code is 200
        6) Verify the length of the schedule metadata is 0
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        keys = []
        values = []

        remove_sch_metadata_obj = \
            self.images_provider.schedules_client.set_schedule_metadata(sch.id,
                                                                        keys,
                                                                        values)
        self.assertEquals(remove_sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     remove_sch_metadata_obj.status_code))

        list_sch_metadata_obj = self.images_provider.schedules_client.\
            list_schedule_metadata(sch.id)
        self.assertEquals(list_sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_sch_metadata_obj.status_code))
        self.assertTrue(len(list_sch_metadata_obj.entity) == 0,
                        msg.format("length of the list", 0,
                                   len(list_sch_metadata_obj.entity)))

    @attr('positive')
    def test_set_an_empty_schedule_metadata_that_is_already_empty(self):
        '''Set an empty schedule metadata that is already empty'''

        """
        1) Create a schedule with schedule metadata
        2) Remove the schedule metadata
        3) Verify that the response code is 200
        4) Removed the schedule metadata again
        5) Verify that a correct validation message is returned
        6) List the removed schedule metadata
        7) Verify that the response code is 200
        8) Verify the length of the schedule metadata is 0
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        key = self.config.images.metadata_key
        value = datagen.random_int(0, 10000)
        msg = Constants.MESSAGE

        metadata = {key: value}
        sch_obj = self.images_provider.\
                    create_active_schedules(tenant, action, metadata=metadata)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        keys = []
        values = []

        remove_sch_metadata_obj = \
            self.images_provider.schedules_client.set_schedule_metadata(sch.id,
                                                                        keys,
                                                                        values)
        self.assertEquals(remove_sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     remove_sch_metadata_obj.status_code))

        remove_sch_metadata_obj = \
            self.images_provider.schedules_client.set_schedule_metadata(sch.id,
                                                                        keys,
                                                                        values)
        self.assertEquals(remove_sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     remove_sch_metadata_obj.status_code))

        list_sch_metadata_obj = self.images_provider.schedules_client.\
            list_schedule_metadata(sch.id)
        self.assertEquals(list_sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_sch_metadata_obj.status_code))
        self.assertTrue(len(list_sch_metadata_obj.entity) == 0,
                        msg.format("length of the list", 0,
                                   len(list_sch_metadata_obj.entity)))

    @attr('positive')
    def test_overwrite_schedule_metadata(self):
        '''Overwrite schedule metadata'''

        """
        1) Create a schedule
        2) Create schedule metadata
        3) Verify that the response code is 200
        4) Overwrite schedule metadata with the created schedule metadata key
        5) Verify that the response code is 200
        6) List schedule metadata
        7) Verify that the schedule metadata is as expected

        Attributes to verify:
            key
            value
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        key = self.config.images.metadata_key
        value = datagen.random_string(size=10)
        alt_value = datagen.random_string(size=10)
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        keys = [key]
        values = [value]

        sch_metadata_obj = \
            self.images_provider.schedules_client.set_schedule_metadata(sch.id,
                                                                        keys,
                                                                        values)
        self.assertEquals(sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_metadata_obj.status_code))

        keys = [key]
        values = [alt_value]

        new_sch_metadata_obj = \
            self.images_provider.schedules_client.set_schedule_metadata(sch.id,
                                                                        keys,
                                                                        values)
        self.assertEquals(new_sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     new_sch_metadata_obj.status_code))

        new_sch_metadata = new_sch_metadata_obj.entity

        list_sch_metadata_obj = self.images_provider.schedules_client.\
            list_schedule_metadata(sch.id)
        self.assertEquals(list_sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_sch_metadata_obj.status_code))

        list_sch_metadata = list_sch_metadata_obj.entity

        self.assertEquals(list_sch_metadata, new_sch_metadata,
                          msg.format('key-value', new_sch_metadata,
                                     list_sch_metadata))

    @attr('positive')
    def test_set_multiple_schedule_metadata(self):
        '''Set multiple schedule metadata'''

        """
        1) Create a schedule without schedule metadata
        2) Set two schedule metadata for the schedule using a valid key
           valid key value pair in the body
        3) Verify that the response code is 200
        4) Verify that the schedule contains both schedule metadata

        Attributes to verify:
            key
            value
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        key = self.config.images.metadata_key
        alt_key = self.config.images.alt_metadata_key
        value = datagen.random_string(size=10)
        alt_value = datagen.random_int(0, 10)
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        keys = [key, alt_key]
        values = [value, alt_value]

        sch_metadata_obj = \
            self.images_provider.schedules_client.set_schedule_metadata(sch.id,
                                                                        keys,
                                                                        values)
        self.assertEquals(sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_metadata_obj.status_code))

        sch_metadata = sch_metadata_obj.entity

        list_sch_metadata_obj = self.images_provider.schedules_client.\
                                list_schedule_metadata(sch.id)
        self.assertEquals(list_sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_sch_metadata_obj.status_code))

        list_sch_metadata = list_sch_metadata_obj.entity

        self.assertEquals(list_sch_metadata, sch_metadata,
                          msg.format('key-value', sch_metadata,
                                     list_sch_metadata))

    @attr('positive')
    def test_set_different_value_for_schedule_metadata_key(self):
        '''Set different value for schedule metadata'''

        """
        1) Create a schedule
        2) Set schedule metadata
        3) Verify that the response code is 200
        4) Set schedule metadata with the existing schedule metadata key
           and new value
        5) Verify that the response code is 200
        6) Get a schedule and verify new metadata value is

        Attributes to verify:
            key
            value
        """
        tenant = self.config.images.tenant
        action = self.config.images.action
        key = self.config.images.metadata_key
        value = datagen.random_string(size=10)
        alt_value = datagen.random_string(size=10)
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        keys = [key]
        values = [value]

        sch_metadata_obj = \
            self.images_provider.schedules_client.set_schedule_metadata(sch.id,
                                                                        keys,
                                                                        values)
        self.assertEquals(sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_metadata_obj.status_code))

        keys = [key]
        values = [alt_value]

        new_sch_metadata_obj = \
            self.images_provider.schedules_client.set_schedule_metadata(sch.id,
                                                                        keys,
                                                                        values)
        self.assertEquals(new_sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     new_sch_metadata_obj.status_code))

        new_sch_metadata = new_sch_metadata_obj.entity

        list_sch_metadata_obj = self.images_provider.schedules_client.\
                                     list_schedule_metadata(sch.id)
        self.assertEquals(list_sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_sch_metadata_obj.status_code))

        list_sch_metadata = list_sch_metadata_obj.entity

        self.assertEquals(list_sch_metadata, new_sch_metadata,
                          msg.format('key-value', new_sch_metadata,
                                     list_sch_metadata))

    @attr('positive')
    def test_overwrite_schedule_metadata_with_empty_schedule_metadata(self):
        '''Overwrite schedule metadata with empty schedule metadata'''

        """
        1) Create a schedule with schedule metadata
        2) Set empty schedule metadata
        3) Verify that the response code is 200
        4) Verify that get schedule returns empty metadata

        Attributes to verify:
            key
            value
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        key = self.config.images.metadata_key
        value = datagen.random_string(size=10)
        msg = Constants.MESSAGE

        metadata = {key: value}
        sch_obj = self.images_provider.\
                    create_active_schedules(tenant, action, metadata=metadata)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        keys = []
        values = []

        new_sch_metadata_obj = \
            self.images_provider.schedules_client.set_schedule_metadata(sch.id,
                                                                        keys,
                                                                        values)
        self.assertEquals(new_sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     new_sch_metadata_obj.status_code))

        new_sch_metadata = new_sch_metadata_obj.entity

        list_sch_metadata_obj = self.images_provider.schedules_client.\
                                list_schedule_metadata(sch.id)
        self.assertEquals(list_sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_sch_metadata_obj.status_code))

        list_sch_metadata = list_sch_metadata_obj.entity

        self.assertEquals(list_sch_metadata, new_sch_metadata,
                          msg.format('key-value', new_sch_metadata,
                                     list_sch_metadata))

    @attr('positive')
    def test_set_schedule_metadata_after_setting_empty_metadata(self):
        '''Set schedule metadata after setting an empty schedule
           metadata'''

        """
        1) Create a schedule with schedule metadata
        2) Set empty schedule metadata
        3) Verify that the response code is 200
        4) Set a valid schedule metadata for that schedule
        5) Verify that the response code is 200
        6) Verify that get schedule metadata has been updated as expected

        Attributes to verify:
            key
            value
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        key = self.config.images.metadata_key
        value = datagen.random_string(size=10)
        alt_key = self.config.images.alt_metadata_key
        alt_value = datagen.random_string(size=10)
        msg = Constants.MESSAGE

        metadata = {key: value}
        sch_obj = self.images_provider.\
                    create_active_schedules(tenant, action, metadata=metadata)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        keys = []
        values = []

        empty_sch_metadata_obj = \
            self.images_provider.schedules_client.set_schedule_metadata(sch.id,
                                                                        keys,
                                                                        values)
        self.assertEquals(empty_sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     empty_sch_metadata_obj.status_code))

        empty_sch_metadata = empty_sch_metadata_obj.entity

        list_sch_metadata_obj = self.images_provider.schedules_client.\
                                list_schedule_metadata(sch.id)
        self.assertEquals(list_sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_sch_metadata_obj.status_code))

        list_sch_metadata = list_sch_metadata_obj.entity

        self.assertEquals(list_sch_metadata, empty_sch_metadata,
                          msg.format('key-value', empty_sch_metadata,
                                     list_sch_metadata))
        keys = [alt_key]
        values = [alt_value]

        new_sch_metadata_obj = \
            self.images_provider.schedules_client.set_schedule_metadata(sch.id,
                                                                        keys,
                                                                        values)
        self.assertEquals(new_sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     new_sch_metadata_obj.status_code))

        new_sch_metadata = new_sch_metadata_obj.entity

        list_sch_metadata_obj = self.images_provider.schedules_client.\
                                list_schedule_metadata(sch.id)
        self.assertEquals(list_sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_sch_metadata_obj.status_code))

        list_sch_metadata = list_sch_metadata_obj.entity

        self.assertEquals(list_sch_metadata, new_sch_metadata,
                          msg.format('key-value', new_sch_metadata,
                                     list_sch_metadata))

    @attr('positive')
    def test_set_multiple_schedule_metadata_after_empty_metadata(self):
        '''Set multiple schedule metadata after setting an empty schedule
           metadata'''

        """
        1) Create a schedule with schedule metadata
        2) Set empty schedule metadata
        3) Verify that the response code is 200
        4) Set multiple valid schedule metadata for that schedule
        5) Verify that the response code is 200
        6) Verify that get schedule metadata has been updated as expected

        Attributes to verify:
            key
            value
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        key = self.config.images.metadata_key
        value = datagen.random_string(size=10)
        alt_key = self.config.images.alt_metadata_key
        alt_value = datagen.random_string(size=10)
        msg = Constants.MESSAGE

        metadata = {key: value}
        sch_obj = self.images_provider.\
                    create_active_schedules(tenant, action, metadata=metadata)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        keys = []
        values = []

        empty_sch_metadata_obj = \
            self.images_provider.schedules_client.set_schedule_metadata(sch.id,
                                                                        keys,
                                                                        values)
        self.assertEquals(empty_sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     empty_sch_metadata_obj.status_code))

        empty_sch_metadata = empty_sch_metadata_obj.entity

        list_sch_metadata_obj = self.images_provider.schedules_client.\
                                list_schedule_metadata(sch.id)
        self.assertEquals(list_sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_sch_metadata_obj.status_code))

        list_sch_metadata = list_sch_metadata_obj.entity

        self.assertEquals(list_sch_metadata, empty_sch_metadata,
                          msg.format('key-value', empty_sch_metadata,
                                     list_sch_metadata))
        keys = [key, alt_key]
        values = [value, alt_value]

        new_sch_metadata_obj = \
            self.images_provider.schedules_client.set_schedule_metadata(sch.id,
                                                                        keys,
                                                                        values)
        self.assertEquals(new_sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     new_sch_metadata_obj.status_code))

        new_sch_metadata = new_sch_metadata_obj.entity

        list_sch_metadata_obj = self.images_provider.schedules_client.\
                                list_schedule_metadata(sch.id)
        self.assertEquals(list_sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_sch_metadata_obj.status_code))

        list_sch_metadata = list_sch_metadata_obj.entity

        self.assertEquals(list_sch_metadata, new_sch_metadata,
                          msg.format('key-value', new_sch_metadata,
                                     list_sch_metadata))

    @attr('positive')
    def test_set_multiple_metadata_for_schedule_with_single_metadata(self):
        '''Set multiple schedule metadata for schedule with single metadata'''

        """
        1) Create a schedule with single schedule metadata
        2) Verify that the response code is 200
        3) Set multiple schedule metadata for that schedule
        4) Verify that the response code is 200
        5) Verify that get schedule metadata has been updated as expected

        Attributes to verify:
            key
            value
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        key = self.config.images.metadata_key
        value = datagen.random_string(size=10)
        alt_key = self.config.images.alt_metadata_key
        alt_value = datagen.random_string(size=10)
        msg = Constants.MESSAGE

        metadata = {key: value}
        sch_obj = self.images_provider.\
                    create_active_schedules(tenant, action, metadata=metadata)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        keys = [key, alt_key]
        values = [value, alt_value]

        new_sch_metadata_obj = \
            self.images_provider.schedules_client.set_schedule_metadata(sch.id,
                                                                        keys,
                                                                        values)
        self.assertEquals(new_sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     new_sch_metadata_obj.status_code))

        new_sch_metadata = new_sch_metadata_obj.entity

        list_sch_metadata_obj = self.images_provider.schedules_client.\
                                list_schedule_metadata(sch.id)
        self.assertEquals(list_sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_sch_metadata_obj.status_code))

        list_sch_metadata = list_sch_metadata_obj.entity

        self.assertEquals(list_sch_metadata, new_sch_metadata,
                          msg.format('key-value', new_sch_metadata,
                                     list_sch_metadata))

    @attr('positive')
    def test_set_schedule_metadata_after_job_created(self):
        '''Set schedule metadata after a job created for it'''

        """
        1) Create a schedule with metadata such that a job is created for it
            in few minutes
        2) Make sure a job is created for that schedule
        3) Set the schedule's metadata with new instance_id value
        4) Verify that the schedule is updated with new instance_id value
        5) Verify that the currently running job is not affected and
            completes successfully
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        msg = Constants.MESSAGE
        key = self.config.images.metadata_key
        instance_id = self.instance_id
        user_name_metadata_key = self.config.images.user_name_metadata_key
        user_name = self.config.images.user_name
        alt_instance_id = self.alt_instance_id

        metadata = {key: instance_id, user_name_metadata_key: user_name}

        sch_obj = self.images_provider.\
            create_active_schedules(tenant, action, metadata=metadata)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        tm = datetime.now() - timedelta(seconds=60)
        next_run_time = tm.strftime('%Y-%m-%d %H:%M:%S')

        upd_sch_obj = \
            self.images_provider.schedules_client.update_schedule(
                id=sch.id, next_run=next_run_time)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        self.images_provider.wait_for_job_to_create(sch.id)

        jobs = self.images_provider.list_jobs_for_schedule(sch.id)

        self.assertTrue(len(jobs) > 0, msg.format('Job', 'At least 1',
                                                  len(jobs)))

        keys = [key]
        values = [alt_instance_id]

        new_sch_obj = self.images_provider.schedules_client.\
            set_schedule_metadata(sch.id, keys, values)

        self.assertEquals(new_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     new_sch_obj.status_code))

        self.assertEquals(new_sch_obj.entity, {key: alt_instance_id},
                          msg.format('key-value', {key: alt_instance_id},
                                     new_sch_obj.entity))

        job = self.images_provider.jobs_client.get_job(jobs[0].id)

        self.assertEquals(job.status_code, 200,
                          msg.format('status_code', 200, job.status_code))

        self.images_provider.wait_for_job_status(jobs[0].id,
                                                 ScheduledImagesJobStatus.DONE)

        job = self.images_provider.jobs_client.get_job(jobs[0].id)

        self.assertEquals(job.status_code, 200,
                          msg.format('status_code', 200, job.status_code))

        self.assertTrue(job.entity.worker_id is not None,
                        msg.format('worker', 'Not None',
                                   job.entity.worker_id))

    @attr('positive')
    def test_set_empty_schedule_metadata_after_job_created(self):
        '''Set empty schedule metadata after a job created for it'''

        """
        1) Create a schedule with metadata such that a job is created for it
            in few minutes
        2) Make sure a job is created for that schedule
        3) Set the schedule's metadata with empty metadata
        4) Verify that the schedule is updated with new metadata
        5) Verify that the currently running job is not affected and
            completes successfully
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        msg = Constants.MESSAGE
        key = self.config.images.metadata_key
        instance_id = self.instance_id
        user_name_metadata_key = self.config.images.user_name_metadata_key
        user_name = self.config.images.user_name

        metadata = {key: instance_id, user_name_metadata_key: user_name}

        sch_obj = self.images_provider.\
            create_active_schedules(tenant, action, metadata=metadata)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        tm = datetime.now() - timedelta(seconds=60)
        next_run_time = tm.strftime('%Y-%m-%d %H:%M:%S')

        upd_sch_obj = \
            self.images_provider.schedules_client.update_schedule(
                id=sch.id, next_run=next_run_time)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        self.images_provider.wait_for_job_to_create(sch.id)

        jobs = self.images_provider.list_jobs_for_schedule(sch.id)

        keys = []
        values = []

        new_sch_obj = self.images_provider.schedules_client.\
            set_schedule_metadata(sch.id, keys, values)

        self.assertEquals(new_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     new_sch_obj.status_code))

        self.assertEquals(new_sch_obj.entity, {},
                          msg.format('key-value', {},
                                     new_sch_obj.entity))

        job = self.images_provider.jobs_client.get_job(jobs[0].id)

        self.assertEquals(job.status_code, 200,
                          msg.format('status_code', 200, job.status_code))

        status = job.entity.status
        self.assertTrue(self.images_provider.is_job_status_workable(status) or
                        self.images_provider.is_job_status_done(status),
                        msg.format('status', 'workable/done job status',
                                   status))

        self.images_provider.wait_for_job_status(jobs[0].id,
                                                 ScheduledImagesJobStatus.DONE)

        job = self.images_provider.jobs_client.get_job(jobs[0].id)

        self.assertEquals(job.status_code, 200,
                          msg.format('status_code', 200, job.status_code))

        self.assertTrue(job.entity.worker_id is not None,
                        msg.format('worker', 'Not None',
                                   job.entity.worker_id))
