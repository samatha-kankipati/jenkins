import ccengine.common.tools.datagen as datagen
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute import InternalServerError
from testrepo.common.testfixtures.images import BaseImagesFixture


class TestQonosListSchedulesNegative(BaseImagesFixture):

    @attr('neg', 'filter')
    def test_list_schedules_with_blank_tenant_id_filter_only(self):
        """List schedules with blank tenant id filter only.

        1) Create a schedule
        2) List schedules with blank tenant id
        3) Verify no schedules are returned and that a correct validation
            message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        keys = ["tenant"]
        values = [" "]
        list_sch_obj = self.images_provider.schedules_client.\
            list_schedules(keys, values)
        self.assertEquals(list_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_sch_obj.status_code))

        self.assertEquals(len(list_sch_obj.entity), 0,
                          msg.format("length of the list", 0,
                                     len(list_sch_obj.entity)))

    @attr('neg', 'filter')
    def test_list_schedules_with_blank_instance_id_filter_only(self):
        """List schedules with blank instance id filter only.

        1) Create a schedule and add schedule metadata to it
        2) List schedules with blank instance id
        3) Verify no schedules are returned and that a correct validation
            message is returned
        """

        tenant = datagen.random_string(size=10)
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

        keys = [key]
        values = [" "]
        list_sch_obj = self.images_provider.schedules_client.\
            list_schedules(keys, values)
        self.assertEquals(list_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_sch_obj.status_code))

        self.assertEquals(len(list_sch_obj.entity), 0,
                          msg.format("length of the list", 0,
                                     len(list_sch_obj.entity)))

    @attr('neg', 'filter')
    def test_list_schedules_with_non_existing_instance_id_filter_only(self):
        """List schedules with non-existing instance id filter only.

        1) List schedules with non-existing instance id
        2) Verify no schedules are returned and that a correct validation
            message is returned
        """

        key = self.config.images.metadata_key
        msg = Constants.MESSAGE

        keys = [key]
        values = ["0"]
        list_sch_obj = self.images_provider.schedules_client.\
            list_schedules(keys, values)
        self.assertEquals(list_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_sch_obj.status_code))

        self.assertEquals(len(list_sch_obj.entity), 0,
                          msg.format("length of the list", 0,
                                     len(list_sch_obj.entity)))

    @attr('neg', 'filter')
    def test_list_schedules_with_blank_next_run_after_filter_only(self):
        """List schedules with blank next_run_after filter only.

        1) Create a schedule and add schedule metadata to it
        2) List schedules with blank next run after
        3) Verify no schedules are returned and that a correct validation
            message is returned
        """

        tenant = datagen.random_string(size=10)
        action = self.config.images.action
        hour = int(self.config.images.hour)
        minute = int(self.config.images.minute)
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_obj.status_code))

        sch = sch_obj.entity

        upd_sch_obj = self.images_provider.schedules_client.\
            update_schedule(id=sch.id, hour=hour, minute=minute)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        keys = ["next_run_after"]
        values = [" "]
        '''TODO: This should fail when bug #171 is fixed'''
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

    @attr('neg', 'filter')
    def test_list_schedules_with_non_existing_next_run_after_filter_only(self):
        """List schedules with non-existing next_run_after filter only.

        1) List schedules with non-existing next run after
        2) Verify that a correct validation
            message is returned
        """

        keys = ["next_run_after"]
        values = ["0000-03-12T12:10:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013-13-12T12:10:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013-03-32T12:10:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013-03-12T25:10:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013-03-12T12:61:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013-03-12T12:10:61Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

    @attr('neg', 'filter')
    def test_lst_sch_w_time_incorrectly_formatted_next_run_after_filter(self):
        """List schedules with time incorrectly formated for next_run_after
        filter only.

        1) List schedules with time incorrectly formatted for next run after
        2) Verify that a correct validation message is returned
        """

        msg = Constants.MESSAGE

        keys = ["next_run_after"]
        values = ["2013-03-12T12:10"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013-03-12T:10:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013-03-1212:10:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013-03-12T12-10-30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013-03-12T12::10:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013:03:12T12:10:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["-03-12T12:10:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013-03-1212:10:30"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["-2013-03-12T12:10:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013-03-12-T12:10:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013--03-12T12:10:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013-03-12T-12:10:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013-03-12T12:10:30:Z"]
        '''TODO: This should fail when bug #172 is fixed'''
        list_sch_obj = self.images_provider.schedules_client.\
            list_schedules(keys, values)
        self.assertEquals(list_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_sch_obj.status_code))

        values = ["2013-03-12T12:10:30Z:"]
        '''TODO: This should fail when bug #172 is fixed'''
        list_sch_obj = self.images_provider.schedules_client.\
            list_schedules(keys, values)
        self.assertEquals(list_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_sch_obj.status_code))

    @attr('neg', 'filter')
    def test_list_schedules_with_blank_next_run_before_filter_only(self):
        """List schedules with blank next_run_before filter only.

        1) Create a schedule and add schedule metadata to it
        2) List schedules with blank next run before
        3) Verify no schedules are returned and that a correct validation
            message is returned
        """

        tenant = datagen.random_string(size=10)
        action = self.config.images.action
        hour = int(self.config.images.hour)
        minute = int(self.config.images.minute)
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_obj.status_code))

        sch = sch_obj.entity

        upd_sch_obj = self.images_provider.schedules_client.\
            update_schedule(id=sch.id, hour=hour, minute=minute)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        keys = ["next_run_before"]
        values = [" "]
        '''TODO: This should fail when bug #171 is fixed'''
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

    @attr('neg', 'filter')
    def test_list_schedule_with_non_existing_next_run_before_filter_only(self):
        """List schedules with non-existing next_run_before filter only.

        1) List schedules with non-existing next run before
        2) Verify that a correct validation
            message is returned
        """

        keys = ["next_run_before"]
        values = ["0000-03-12T12:10:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013-13-12T12:10:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013-03-32T12:10:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013-03-12T25:10:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013-03-12T12:61:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013-03-12T12:10:61Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

    @attr('neg', 'filter')
    def test_lst_sch_w_time_incorrectly_formatted_next_run_before_filter(self):
        """List schedules with time incorrectly formated for next_run_before
        filter only.

        1) List schedules with time incorrectly formatted for next run before
        2) Verify that a correct validation message is returned
        """

        msg = Constants.MESSAGE

        keys = ["next_run_before"]
        values = ["2013-03-12T12:10"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013-03-12T:10:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013-03-1212:10:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013-03-12T12-10-30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013-03-12T12::10:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013:03:12T12:10:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["-03-12T12:10:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013-03-1212:10:30"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["-2013-03-12T12:10:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013-03-12-T12:10:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013--03-12T12:10:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013-03-12T-12:10:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013-03-12T12:10:30:Z"]
        '''TODO: This should fail when bug #172 is fixed'''
        list_sch_obj = self.images_provider.schedules_client.\
            list_schedules(keys, values)
        self.assertEquals(list_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_sch_obj.status_code))

        values = ["2013-03-12T12:10:30Z:"]
        '''TODO: This should fail when bug #172 is fixed'''
        list_sch_obj = self.images_provider.schedules_client.\
            list_schedules(keys, values)
        self.assertEquals(list_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_sch_obj.status_code))

    @attr('neg', 'filter')
    def test_list_schedules_next_run_after_before_blank_filter_only(self):
        """List schedules with next_run_after filter set to t2 and
        next_run_before filter set to blank.

        1) Create schedule with next_run of t1
        2) Create schedule with next_run of t2 (t2>t1)
        3) Create schedule with next_run of t3 (t3>t2)
        4) List schedules with next_run_after set to t2 and next_run_before set
            to blank
        5) Verify no schedules are returned and that a correct validation
            message is returned
        """

        tenant = datagen.random_string(size=10)
        action = self.config.images.action
        hour = int(self.config.images.hour)
        minute = int(self.config.images.minute)
        increment = 5
        count = 3
        msg = Constants.MESSAGE

        for num in range(count):
            sch_obj = self.images_provider.create_active_schedules(tenant,
                                                                   action)
            self.assertEquals(sch_obj.status_code, 200,
                              msg.format('status_code', 200,
                                         sch_obj.status_code))

            sch = sch_obj.entity

            upd_sch_obj = self.images_provider.schedules_client.\
                update_schedule(id=sch.id, hour=hour, minute=minute)
            self.assertEquals(upd_sch_obj.status_code, 200,
                              msg.format('status_code', 200,
                                         upd_sch_obj.status_code))

            if num == 1:
                next_run_after = upd_sch_obj.entity.next_run

            minute += increment

        keys = ["next_run_after", "next_run_before"]
        values = [next_run_after, " "]
        '''TODO: This should fail when bug #171 is fixed'''
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

    @attr('neg', 'filter')
    def test_list_sch_next_run_after_before_non_existing_filter_only(self):
        """List schedules with next_run_after filter set to t2 and
        next_run_before filter set to non-existing time.

        1) Create schedule with next_run of t1
        2) Create schedule with next_run of t2 (t2>t1)
        3) Create schedule with next_run of t3 (t3>t2)
        4) List schedules with next_run_after set to t2 and next_run_before set
            to non-existing time
        5) Verify no schedules are returned and that a correct validation
            message is returned
        """

        tenant = datagen.random_string(size=10)
        action = self.config.images.action
        hour = int(self.config.images.hour)
        minute = int(self.config.images.minute)
        increment = 5
        count = 3
        msg = Constants.MESSAGE

        for num in range(count):
            sch_obj = self.images_provider.create_active_schedules(tenant,
                                                                   action)
            self.assertEquals(sch_obj.status_code, 200,
                              msg.format('status_code', 200,
                                         sch_obj.status_code))

            sch = sch_obj.entity

            upd_sch_obj = self.images_provider.schedules_client.\
                update_schedule(id=sch.id, hour=hour, minute=minute)
            self.assertEquals(upd_sch_obj.status_code, 200,
                              msg.format('status_code', 200,
                                         upd_sch_obj.status_code))

            if num == 1:
                next_run_after = upd_sch_obj.entity.next_run

            minute += increment

        keys = ["next_run_after", "next_run_before"]
        values = [next_run_after, "0000-03-12T12:10:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = [next_run_after, "2013-13-12T12:10:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = [next_run_after, "2013-03-32T12:10:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = [next_run_after, "2013-03-12T25:10:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = [next_run_after, "2013-03-12T12:61:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = [next_run_after, "2013-03-12T12:10:61Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

    @attr('neg', 'filter')
    def test_list_sch_next_run_after_before_incorrect_format_filter_only(self):
        """List schedules with next_run_after filter set to t2 and
        next_run_before filter set to non-existing time.

        1) Create schedule with next_run of t1
        2) Create schedule with next_run of t2 (t2>t1)
        3) Create schedule with next_run of t3 (t3>t2)
        4) List schedules with next_run_after set to t2 and next_run_before set
            to non-existing time
        5) Verify no schedules are returned and that a correct validation
            message is returned
        """

        tenant = datagen.random_string(size=10)
        action = self.config.images.action
        hour = int(self.config.images.hour)
        minute = int(self.config.images.minute)
        increment = 5
        count = 3
        msg = Constants.MESSAGE

        for num in range(count):
            sch_obj = self.images_provider.create_active_schedules(tenant,
                                                                   action)
            self.assertEquals(sch_obj.status_code, 200,
                              msg.format('status_code', 200,
                                         sch_obj.status_code))

            sch = sch_obj.entity

            upd_sch_obj = self.images_provider.schedules_client.\
                update_schedule(id=sch.id, hour=hour, minute=minute)
            self.assertEquals(upd_sch_obj.status_code, 200,
                              msg.format('status_code', 200,
                                         upd_sch_obj.status_code))

            if num == 1:
                next_run_after = upd_sch_obj.entity.next_run

            minute += increment

        keys = ["next_run_after", "next_run_before"]
        values = [next_run_after, "2013-03-12T12:10"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = [next_run_after, "2013-03-12T:10:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = [next_run_after, "2013-03-1212:10:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = [next_run_after, "2013-03-12T12-10-30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = [next_run_after, "2013-03-12T12::10:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = [next_run_after, "2013:03:12T12:10:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = [next_run_after, "-03-12T12:10:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = [next_run_after, "2013-03-1212:10:30"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = [next_run_after, "-2013-03-12T12:10:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = [next_run_after, "2013-03-12-T12:10:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = [next_run_after, "2013--03-12T12:10:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = [next_run_after, "2013-03-12T-12:10:30Z"]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = [next_run_after, "2013-03-12T12:10:30:Z"]
        '''TODO: This should fail when bug #172 is fixed'''
        list_sch_obj = self.images_provider.schedules_client.\
            list_schedules(keys, values)
        self.assertEquals(list_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_sch_obj.status_code))

        values = [next_run_after, "2013-03-12T12:10:30Z:"]
        '''TODO: This should fail when bug #172 is fixed'''
        list_sch_obj = self.images_provider.schedules_client.\
            list_schedules(keys, values)
        self.assertEquals(list_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_sch_obj.status_code))

    @attr('neg', 'filter')
    def test_list_schedules_next_run_before_after_blank_filter_only(self):
        """List schedules with next_run_before filter set to t2 and
        next_run_after filter set to blank.

        1) Create schedule with next_run of t1
        2) Create schedule with next_run of t2 (t2>t1)
        3) Create schedule with next_run of t3 (t3>t2)
        4) List schedules with next_run_before set to t2 and next_run_after set
            to blank
        5) Verify no schedules are returned and that a correct validation
            message is returned
        """

        tenant = datagen.random_string(size=10)
        action = self.config.images.action
        hour = int(self.config.images.hour)
        minute = int(self.config.images.minute)
        increment = 5
        count = 3
        msg = Constants.MESSAGE

        for num in range(count):
            sch_obj = self.images_provider.create_active_schedules(tenant,
                                                                   action)
            self.assertEquals(sch_obj.status_code, 200,
                              msg.format('status_code', 200,
                                         sch_obj.status_code))

            sch = sch_obj.entity

            upd_sch_obj = self.images_provider.schedules_client.\
                update_schedule(id=sch.id, hour=hour, minute=minute)
            self.assertEquals(upd_sch_obj.status_code, 200,
                              msg.format('status_code', 200,
                                         upd_sch_obj.status_code))

            if num == 1:
                next_run_before = upd_sch_obj.entity.next_run

            minute += increment

        keys = ["next_run_after", "next_run_before"]
        values = [" ", next_run_before]
        '''TODO: This should fail when bug #171 is fixed'''
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

    @attr('neg', 'filter')
    def test_list_sch_next_run_before_after_non_existing_filter_only(self):
        """List schedules with next_run_before filter set to t2 and
        next_run_after filter set to non-existing time.

        1) Create schedule with next_run of t1
        2) Create schedule with next_run of t2 (t2>t1)
        3) Create schedule with next_run of t3 (t3>t2)
        4) List schedules with next_run_before set to t2 and next_run_after set
            to non-existing time
        5) Verify no schedules are returned and that a correct validation
            message is returned
        """

        tenant = datagen.random_string(size=10)
        action = self.config.images.action
        hour = int(self.config.images.hour)
        minute = int(self.config.images.minute)
        increment = 5
        count = 3
        msg = Constants.MESSAGE

        for num in range(count):
            sch_obj = self.images_provider.create_active_schedules(tenant,
                                                                   action)
            self.assertEquals(sch_obj.status_code, 200,
                              msg.format('status_code', 200,
                                         sch_obj.status_code))

            sch = sch_obj.entity

            upd_sch_obj = self.images_provider.schedules_client.\
                update_schedule(id=sch.id, hour=hour, minute=minute)
            self.assertEquals(upd_sch_obj.status_code, 200,
                              msg.format('status_code', 200,
                                         upd_sch_obj.status_code))

            if num == 1:
                next_run_before = upd_sch_obj.entity.next_run

            minute += increment

        keys = ["next_run_after", "next_run_before"]
        values = ["0000-03-12T12:10:30Z", next_run_before]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013-13-12T12:10:30Z", next_run_before]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013-03-32T12:10:30Z", next_run_before]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013-03-12T25:10:30Z", next_run_before]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013-03-12T12:61:30Z", next_run_before]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013-03-12T12:10:61Z", next_run_before]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

    @attr('neg', 'filter')
    def test_list_sch_next_run_before_after_incorrect_format_filter_only(self):
        """List schedules with next_run_before filter set to t2 and
        next_run_after filter set to non-existing time.

        1) Create schedule with next_run of t1
        2) Create schedule with next_run of t2 (t2>t1)
        3) Create schedule with next_run of t3 (t3>t2)
        4) List schedules with next_run_before set to t2 and next_run_after set
            to non-existing time
        5) Verify no schedules are returned and that a correct validation
            message is returned
        """

        tenant = datagen.random_string(size=10)
        action = self.config.images.action
        hour = int(self.config.images.hour)
        minute = int(self.config.images.minute)
        increment = 5
        count = 3
        msg = Constants.MESSAGE

        for num in range(count):
            sch_obj = self.images_provider.create_active_schedules(tenant,
                                                                   action)
            self.assertEquals(sch_obj.status_code, 200,
                              msg.format('status_code', 200,
                                         sch_obj.status_code))

            sch = sch_obj.entity

            upd_sch_obj = self.images_provider.schedules_client.\
                update_schedule(id=sch.id, hour=hour, minute=minute)
            self.assertEquals(upd_sch_obj.status_code, 200,
                              msg.format('status_code', 200,
                                         upd_sch_obj.status_code))

            if num == 1:
                next_run_before = upd_sch_obj.entity.next_run

            minute += increment

        keys = ["next_run_after", "next_run_before"]
        values = ["2013-03-12T12:10", next_run_before]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013-03-12T:10:30Z", next_run_before]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013-03-1212:10:30Z", next_run_before]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013-03-12T12-10-30Z", next_run_before]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013-03-12T12::10:30Z", next_run_before]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013:03:12T12:10:30Z", next_run_before]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["-03-12T12:10:30Z", next_run_before]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013-03-1212:10:30", next_run_before]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["-2013-03-12T12:10:30Z", next_run_before]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013-03-12-T12:10:30Z", next_run_before]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013--03-12T12:10:30Z", next_run_before]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013-03-12T-12:10:30Z", next_run_before]
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client.list_schedules(keys, values)

        values = ["2013-03-12T12:10:30:Z", next_run_before]
        '''TODO: This should fail when bug #172 is fixed'''
        list_sch_obj = self.images_provider.schedules_client.\
            list_schedules(keys, values)
        self.assertEquals(list_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_sch_obj.status_code))

        values = ["2013-03-12T12:10:30Z:", next_run_before]
        '''TODO: This should fail when bug #172 is fixed'''
        list_sch_obj = self.images_provider.schedules_client.\
            list_schedules(keys, values)
        self.assertEquals(list_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_sch_obj.status_code))
