from testrepo.common.testfixtures.images import BaseImagesFixture
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
import ccengine.common.tools.datagen as datagen
import calendar
import time


class TestQonosListSchedules(BaseImagesFixture):

    @attr('positive')
    def test_happy_path_list_schedules(self):
        '''Happy Path - List schedules'''

        """
        1) Create a valid schedule
        2) Verify that the response code is 200
        3) List schedules
        4) Verify that the response code is 200
        5) Verify that the length of the returned list is 1
        6) Verify that the auto-generated parameters (id, created-at,
           updated-at, next_run, last_scheduled, etc) are generated correctly
        7) Verify that the non-auto-generated parameters (month, week,
           day_of_week, _day_of_month, meta_data, etc) are created as entered

        Attributes to verify:
            next_run
            hour
            tenant
            created_at
            updated_at
            day_of_week
            day_of_month
            metadata
            last_scheduled
            action
            month
            id
            minute
        """

        tenant = datagen.random_string(size=10)
        action = self.config.images.action
        sch_list = []
        count = 1
        marker = None
        keys = ["tenant", "marker"]
        values = [tenant, marker]
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        list_sch = self.images_provider.list_schedules_pagination(keys, values)

        for s in list_sch:
            if s.id == sch_obj.entity.id:
                sch_list.append(s)
        self.assertTrue(len(sch_list) == count,
                        msg.format("length of the list", count, len(sch_list)))

        listed_sch = sch_list[0]
        created_sch = sch_obj.entity

        listed_next_run_in_sec = \
            calendar.timegm(time.strptime(str(listed_sch.next_run),
                                          "%Y-%m-%dT%H:%M:%SZ"))
        created_next_run_in_sec = \
            calendar.timegm(time.strptime(str(created_sch.next_run),
                                          "%Y-%m-%dT%H:%M:%SZ"))
        listed_created_at_in_sec = \
            calendar.timegm(time.strptime(str(listed_sch.created_at),
                                          "%Y-%m-%dT%H:%M:%SZ"))
        created_created_at_in_sec = \
            calendar.timegm(time.strptime(str(created_sch.created_at),
                                          "%Y-%m-%dT%H:%M:%SZ"))
        listed_updated_at_in_sec = \
            calendar.timegm(time.strptime(str(listed_sch.updated_at),
                                          "%Y-%m-%dT%H:%M:%SZ"))
        created_updated_at_in_sec = \
            calendar.timegm(time.strptime(str(created_sch.updated_at),
                                          "%Y-%m-%dT%H:%M:%SZ"))

        next_run_diff_in_sec = \
            abs(listed_next_run_in_sec - created_next_run_in_sec)
        created_at_diff_in_sec = \
            abs(listed_created_at_in_sec - created_created_at_in_sec)
        updated_at_diff_in_sec = \
            abs(listed_updated_at_in_sec - created_updated_at_in_sec)

        self.assertTrue(next_run_diff_in_sec <= 10,
                        msg.format('next_run', created_sch.next_run,
                                   listed_sch.next_run))
        self.assertEquals(listed_sch.hour, created_sch.hour,
                          msg.format('hour', created_sch.hour,
                                     listed_sch.hour))
        self.assertEquals(listed_sch.tenant, created_sch.tenant,
                          msg.format('tenant', created_sch.tenant,
                                     listed_sch.tenant))
        self.assertTrue(created_at_diff_in_sec <= 10,
                        msg.format('created_at', created_sch.created_at,
                                   listed_sch.created_at))
        self.assertTrue(updated_at_diff_in_sec <= 10,
                        msg.format('updated_at', created_sch.updated_at,
                                   listed_sch.updated_at))
        self.assertEquals(listed_sch.day_of_week, created_sch.day_of_week,
                          msg.format('day_of_week', created_sch.day_of_week,
                                     listed_sch.day_of_week))
        self.assertEquals(listed_sch.day_of_month, created_sch.day_of_month,
                          msg.format('day_of_month', created_sch.day_of_month,
                                     listed_sch.day_of_month))
        self.assertEquals(listed_sch.metadata, created_sch.metadata,
                          msg.format('metadata', created_sch.metadata,
                                     listed_sch.metadata))
        self.assertEquals(listed_sch.last_scheduled,
                          created_sch.last_scheduled,
                          msg.format('last_scheduled',
                                     created_sch.last_scheduled,
                                     listed_sch.last_scheduled))
        self.assertEquals(listed_sch.action, created_sch.action,
                          msg.format('action', created_sch.action,
                                     listed_sch.action))
        self.assertEquals(listed_sch.month, created_sch.month,
                          msg.format('month', created_sch.month,
                                     listed_sch.month))
        self.assertEquals(listed_sch.id, created_sch.id,
                          msg.format('id', created_sch.id, listed_sch.id))
        self.assertEquals(listed_sch.minute, created_sch.minute,
                          msg.format('minute', created_sch.minute,
                                     listed_sch.minute))

    @attr('positive')
    def test_list_multiple_schedules(self):
        '''List multiple schedules'''

        """
        1) Create three valid schedules
        2) Verify that the response code is 200
        3) List schedules
        4) Verify that the response code is 200
        5) Verify that the length of the returned list is 3
        6) Verify that the auto-generated parameters (id, created-at,
           updated-at, next_run, last_scheduled, etc) are generated correctly
        7) Verify that the non-auto-generated parameters (month, week,
           day_of_week, _day_of_month, meta_data, etc) are created as entered

        Attributes to verify:
            next_run
            hour
            tenant
            created_at
            updated_at
            day_of_week
            day_of_month
            metadata
            last_scheduled
            action
            month
            id
            minute
        """

        tenant = datagen.random_string(size=10)
        action = self.config.images.action
        count = 3
        sch_list = []
        sch_id_list = []
        index = 0
        marker = None
        keys = ["tenant", "marker"]
        values = [tenant, marker]
        msg = Constants.MESSAGE

        sch_obj = \
            self.images_provider.create_active_schedules(tenant, action,
                                                         count=count)

        for sch in sch_obj:
            self.assertEquals(sch.status_code, 200,
                              msg.format('status_code', 200, sch.status_code))
            sch_id_list.append(sch.entity.id)

        list_sch = self.images_provider.list_schedules_pagination(keys, values)

        for list_sch in list_sch:
            if list_sch.id in sch_id_list:
                sch_list.append(list_sch)
        self.assertTrue(len(sch_list) == count,
                        msg.format("length of the list", count, len(sch_list)))

        for sch in sch_list:
            for item in sch_obj:
                if sch.id == item.entity.id:
                    current_sch = sch_obj[index].entity
                    index = 0
                    break
                else:
                    index += 1

            sch_next_run_in_sec = \
                calendar.timegm(time.strptime(str(sch.next_run),
                                              "%Y-%m-%dT%H:%M:%SZ"))
            current_next_run_in_sec = \
                calendar.timegm(time.strptime(str(current_sch.next_run),
                                              "%Y-%m-%dT%H:%M:%SZ"))
            sch_created_at_in_sec = \
                calendar.timegm(time.strptime(str(sch.created_at),
                                              "%Y-%m-%dT%H:%M:%SZ"))
            current_created_at_in_sec = \
                calendar.timegm(time.strptime(str(current_sch.created_at),
                                              "%Y-%m-%dT%H:%M:%SZ"))
            sch_updated_at_in_sec = \
                calendar.timegm(time.strptime(str(sch.updated_at),
                                              "%Y-%m-%dT%H:%M:%SZ"))
            current_updated_at_in_sec = \
                calendar.timegm(time.strptime(str(current_sch.updated_at),
                                              "%Y-%m-%dT%H:%M:%SZ"))

            next_run_diff_in_sec = \
                abs(sch_next_run_in_sec - current_next_run_in_sec)
            created_at_diff_in_sec = \
                abs(sch_created_at_in_sec - current_created_at_in_sec)
            updated_at_diff_in_sec = \
                abs(sch_updated_at_in_sec - current_updated_at_in_sec)

            self.assertTrue(next_run_diff_in_sec <= 10,
                            msg.format('next_run', current_sch.next_run,
                                       sch.next_run))
            self.assertEquals(sch.hour, current_sch.hour,
                              msg.format('hour', current_sch.hour, sch.hour))
            self.assertEquals(sch.tenant, current_sch.tenant,
                              msg.format('tenant', current_sch.tenant,
                                         sch.tenant))
            self.assertTrue(created_at_diff_in_sec <= 10,
                            msg.format('created_at', current_sch.created_at,
                                       sch.created_at))
            self.assertTrue(updated_at_diff_in_sec <= 10,
                            msg.format('updated_at', current_sch.updated_at,
                                       sch.updated_at))
            self.assertEquals(sch.day_of_week, current_sch.day_of_week,
                              msg.format('day_of_week',
                                         current_sch.day_of_week,
                                         sch.day_of_week))
            self.assertEquals(sch.day_of_month, current_sch.day_of_month,
                              msg.format('day_of_month',
                                         current_sch.day_of_month,
                                         sch.day_of_month))
            self.assertEquals(sch.metadata, current_sch.metadata,
                          msg.format('metadata', current_sch.metadata,
                                     sch.metadata))
            self.assertEquals(sch.last_scheduled, current_sch.last_scheduled,
                            msg.format('last_scheduled',
                                       current_sch.last_scheduled,
                                       sch.last_scheduled))
            self.assertEquals(sch.action, current_sch.action,
                              msg.format('action', current_sch.action,
                                         sch.action))
            self.assertEquals(sch.month, current_sch.month,
                              msg.format('month', current_sch.month,
                                         sch.month))
            self.assertEquals(sch.id, current_sch.id,
                              msg.format('id', current_sch.id, sch.id))
            self.assertEquals(sch.minute, current_sch.minute,
                              msg.format('minute', current_sch.minute,
                                         sch.minute))

    @attr('pos', 'filter')
    def test_list_schedules_with_tenant_filter_only(self):
        '''List schedules with tenant id filter only'''

        """
        1) Create a valid schedule containing specific tenant id
        2) Verify that the response code is 200
        3) List schedule with a second tenant id filter only
        4) Verify that the length of the returned list is 0
        5) Create another valid schedule containing the second tenant id
        6) Verify that the response code is 200
        7) List schedules with the second tenant id filter only
        8) Verify that the length of the returned list is 1
        9) Create another valid schedule containing the second tenant id
        10) Verify that the response code is 200
        11) List schedules with the second tenant id filter only
        12) Verify that the length of the returned list is 2
        """

        tenant = datagen.random_string(size=10)
        alt_tenant = datagen.random_string(size=10)
        action = self.config.images.action
        marker = None
        keys = ["tenant", "marker"]
        values = [alt_tenant, marker]
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        list_sch = self.images_provider.list_schedules_pagination(keys, values)

        self.assertTrue(len(list_sch) == 0,
                        msg.format("length of the list", 0,
                                   len(list_sch)))

        sch_obj = self.images_provider.create_active_schedules(alt_tenant,
                                                               action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        list_sch = self.images_provider.list_schedules_pagination(keys, values)

        self.assertTrue(len(list_sch) == 1,
                        msg.format("length of the list", 1,
                                   len(list_sch)))

        sch_obj = self.images_provider.create_active_schedules(alt_tenant,
                                                               action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        list_sch = self.images_provider.list_schedules_pagination(keys, values)

        self.assertTrue(len(list_sch) == 2,
                        msg.format("length of the list", 2,
                                   len(list_sch)))

    @attr('pos', 'filter')
    def test_list_schedules_with_instance_id_filter_only(self):
        '''List schedules with instance id filter only'''

        """
        1) Create a valid schedule containing specific instance id
        2) Verify that the response code is 200
        3) List schedule with a second instance id filter only
        4) Verify that the length of the returned list is 0
        5) Create another valid schedule containing the second instance id
        6) Verify that the response code is 200
        7) List schedules with the second instance id filter only
        8) Verify that the length of the returned list is 1
        9) Create another valid schedule containing the second instance id
        10) Verify that the response code is 200
        11) List schedules with the second instance id filter only
        12) Verify that the length of the returned list is 2
        """

        tenant = datagen.random_string(size=10)
        action = self.config.images.action
        key = self.config.images.metadata_key
        value = datagen.random_string(size=10)
        alt_value = datagen.random_string(size=10)
        marker = None
        keys = [key]
        values = [value]
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        sch_metadata_obj = \
            self.images_provider.schedules_client.set_schedule_metadata(sch.id,
                                                                        keys,
                                                                        values)
        self.assertEquals(sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_metadata_obj.status_code))

        filter_keys = [key, "marker"]
        filter_values = [alt_value, marker]

        list_sch = \
            self.images_provider.list_schedules_pagination(filter_keys,
                                                           filter_values)

        self.assertTrue(len(list_sch) == 0,
                        msg.format("length of the list", 0,
                                   len(list_sch)))

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        keys = [key]
        values = [alt_value]

        sch_metadata_obj = \
            self.images_provider.schedules_client.set_schedule_metadata(sch.id,
                                                                        keys,
                                                                        values)
        self.assertEquals(sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_metadata_obj.status_code))

        list_sch = \
            self.images_provider.list_schedules_pagination(filter_keys,
                                                           filter_values)

        self.assertTrue(len(list_sch) == 1,
                        msg.format("length of the list", 1,
                                   len(list_sch)))

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        keys = [key]
        values = [alt_value]

        sch_metadata_obj = \
            self.images_provider.schedules_client.set_schedule_metadata(sch.id,
                                                                        keys,
                                                                        values)
        self.assertEquals(sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_metadata_obj.status_code))

        list_sch = \
            self.images_provider.list_schedules_pagination(filter_keys,
                                                           filter_values)

        self.assertTrue(len(list_sch) == 2,
                        msg.format("length of the list", 2,
                                   len(list_sch)))

    @attr('pos', 'filter')
    def test_list_schedules_with_multiple_metadata_key_filters(self):
        '''List schedules with multiple metadata key filters'''

        """
        1) Create a valid schedule containing specific instance id
        2) Verify that the response code is 200
        3) Create a valid schedule containing specific instance id and
            retention values
        4) List schedules with the instance id filter only
        4) Verify that the length of the returned list is 2
        5) List schedules with the retention filter only
        6) Verify that the length of the returned list is 1
        7) List schedules with both instance id and retention filters
        8) Verify that the length of the returned list is 1
        9) Verify expected schedules are returned
        """

        tenant = datagen.random_string(size=10)
        action = self.config.images.action
        key = self.config.images.metadata_key
        value = datagen.random_string(size=10)
        alt_key = self.config.images.alt_metadata_key
        alt_value = datagen.random_string(size=10)
        marker = None
        keys = [key]
        values = [value]
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        sch_metadata_obj = self.images_provider.schedules_client.\
            set_schedule_metadata(sch.id, keys, values)

        self.assertEquals(sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_metadata_obj.status_code))

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        keys = [key, alt_key]
        values = [value, alt_value]

        sch_metadata_obj = self.images_provider.schedules_client.\
            set_schedule_metadata(sch.id, keys, values)

        self.assertEquals(sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_metadata_obj.status_code))

        filter_keys = [key, "marker"]
        filter_values = [value, marker]

        list_sch = \
            self.images_provider.list_schedules_pagination(filter_keys,
                                                           filter_values)

        self.assertTrue(len(list_sch) == 2,
                        msg.format("length of the list", 2,
                                   len(list_sch)))

        filter_keys = [alt_key, "marker"]
        filter_values = [alt_value, marker]

        list_sch = \
            self.images_provider.list_schedules_pagination(filter_keys,
                                                           filter_values)

        self.assertTrue(len(list_sch) == 1,
                        msg.format("length of the list", 1,
                                   len(list_sch)))

        filter_keys = [key, alt_key, "marker"]
        filter_values = [value, alt_value, marker]

        list_sch = \
            self.images_provider.list_schedules_pagination(filter_keys,
                                                           filter_values)

        self.assertTrue(len(list_sch) == 1,
                        msg.format("length of the list", 1,
                                   len(list_sch)))

    @attr('pos', 'filter')
    def test_list_schedules_next_run_after_filter_only(self):
        '''List schedules with next_run_after filter only'''

        """
        1) Create schedule with next_run of t1
        2) Create schedule with next_run of t2 (t2>t1)
        3) Create schedule with next_run of t3 (t3>t2)
        4) List schedules with next_run_after=t2
        5) Verify that the length of the returned list is 2 and lists the
            schedules containing t2 and t3 only
        """

        tenant = datagen.random_string(size=10)
        action = self.config.images.action
        hour = int(self.config.images.hour)
        minute = int(self.config.images.minute)
        increment = 5
        count = 3
        schs = []
        ret_schs = []
        marker = None
        msg = Constants.MESSAGE

        for x in range(count):
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

            schs.append(upd_sch_obj.entity)

            if x == 1:
                next_run_after = upd_sch_obj.entity.next_run

            minute += increment

        filter_keys = ["next_run_after", "marker"]
        filter_values = [next_run_after, marker]

        list_sch = \
            self.images_provider.list_schedules_pagination(filter_keys,
                                                           filter_values)

        for s in list_sch:
            if s in schs:
                ret_schs.append(s)

        self.assertTrue(len(ret_schs) == 2,
                        msg.format("length of the list", 2, len(ret_schs)))

        for sch in list_sch:
            if sch.tenant == tenant:
                self.assertTrue(("15:35:00Z" in sch.next_run) or
                                ("15:40:00Z" in sch.next_run),
                                msg.format('time', "to contain 15:35:00Z or"
                                           + " 15:40:00Z", sch.next_run))

    @attr('pos', 'filter')
    def test_list_schedules_next_run_after_filter_only_t1_distant_future(self):
        '''List schedules with next_run_after filter only set to t1 where no
        schedules exist'''

        """
        1) List schedules with next_run_after=t1, where t1 is in distant future
        2) Verify that the length of the returned list is 0
        """

        count = 0
        msg = Constants.MESSAGE

        filter_keys = ["next_run_after"]
        filter_values = ["2099-10-10T15:35:00Z"]
        list_sch_obj = self.images_provider.schedules_client.\
                list_schedules(filter_keys, filter_values)
        self.assertEquals(list_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_sch_obj.status_code))

        list_sch = list_sch_obj.entity

        self.assertTrue(len(list_sch) == count,
                        msg.format("length of the list", count, len(list_sch)))

    @attr('pos', 'filter')
    def test_list_schedules_next_run_before_filter_only(self):
        '''List schedules with next_run_before filter only'''

        """
        1) Create schedule with next_run of t1
        2) Create schedule with next_run of t2 (t2<t1)
        3) Create schedule with next_run of t3 (t3<t2)
        4) List schedules with next_run_before=t2
        5) Verify that the length of the returned list is 2 and lists the
            schedules containing t2 and t3 only
        """

        tenant = datagen.random_string(size=10)
        action = self.config.images.action
        # Make sure the time/hour of the schedules are different from other test
        hour = int(self.config.images.hour) - 1
        minute = int(self.config.images.minute)
        increment = 5
        count = 3
        schs = []
        ret_schs = []
        marker = None
        msg = Constants.MESSAGE

        for x in range(count):
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

            schs.append(upd_sch_obj.entity)

            if x == 1:
                next_run_before = upd_sch_obj.entity.next_run

            minute -= increment

        filter_keys = ["next_run_before", "marker"]
        filter_values = [next_run_before, marker]

        list_sch = \
            self.images_provider.list_schedules_pagination(filter_keys,
                                                           filter_values)

        for s in list_sch:
            if s in schs:
                ret_schs.append(s)

        self.assertTrue(len(ret_schs) == 2,
                        msg.format("length of the list", 2, len(ret_schs)))

        for sch in list_sch:
            if sch.tenant == tenant:
                self.assertTrue(("14:25:00Z" in sch.next_run) or
                                ("14:20:00Z" in sch.next_run),
                                msg.format('time', "to contain 14:25:00Z or"
                                           + " 14:20:00Z", sch.next_run))

    @attr('pos', 'filter')
    def test_list_schedules_next_run_before_filter_only_t1_distant_past(self):
        '''List schedules with next_run_before filter only set to t1 where no
        schedules exist'''

        """
        1) List schedules with next_run_before=t1, where t1 is in distant past
        2) Verify that the length of the returned list is 0
        """

        count = 0
        msg = Constants.MESSAGE

        filter_keys = ["next_run_before"]
        filter_values = ["1999-10-10T15:35:00Z"]
        list_sch_obj = self.images_provider.schedules_client.\
                list_schedules(filter_keys, filter_values)
        self.assertEquals(list_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_sch_obj.status_code))

        list_sch = list_sch_obj.entity

        self.assertTrue(len(list_sch) == count,
                        msg.format("length of the list", count, len(list_sch)))

    @attr('pos', 'filter')
    def test_list_schedules_next_run_after_before_filter_only(self):
        '''List schedules with next_run_after and next_run_before filters
        only'''

        """
        1) Create schedule with next_run of t1
        2) Create schedule with next_run of t2 (t2>t1)
        3) Create schedule with next_run of t3 (t3>t2)
        4) Create schedule with next_run of t4 (t4>t3)
        5) Create schedule with next_run of t5 (t5>t4)
        6) List schedules with next_run_after=t2 and next_run_before=t4
        7) Verify that the length of the returned list is 3 and lists the
            schedules containing t2, t3 and t4 only
        """

        tenant = datagen.random_string(size=10)
        action = self.config.images.action
        # Make sure the time/hour of the schedules are different from other test
        hour = int(self.config.images.hour) - 2
        minute = int(self.config.images.minute)
        increment = 5
        count = 5
        marker = None
        msg = Constants.MESSAGE

        for x in range(count):
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

            if x == 1:
                next_run_after = upd_sch_obj.entity.next_run

            if x == 3:
                next_run_before = upd_sch_obj.entity.next_run

            minute += increment

        filter_keys = ["next_run_after", "next_run_before", "marker"]
        filter_values = [next_run_after, next_run_before, marker]

        list_sch = \
            self.images_provider.list_schedules_pagination(filter_keys,
                                                           filter_values)

        self.assertTrue(len(list_sch) == 3,
                        msg.format("length of the list", 3, len(list_sch)))

        for sch in list_sch:
            if sch.tenant == tenant:
                self.assertTrue(("13:35:00Z" in sch.next_run) or
                                ("13:40:00Z" in sch.next_run) or
                                ("13:45:00Z" in sch.next_run),
                                msg.format('time', "to contain 13:35:00Z,"
                                           + " 13:40:00Z, or 13:45:00Z",
                                           sch.next_run))

    @attr('pos', 'filter')
    def test_list_schedules_next_run_after_before_filter_t2(self):
        '''List schedules with next_run_after and next_run_before both set to
        t2'''

        """
        1) Create schedule with next_run of t1
        2) Create schedule with next_run of t2 (t2>t1)
        3) Create schedule with next_run of t3 (t3>t2)
        6) List schedules with next_run_after and next_run_before=t2
        7) Verify that the length of the returned list is 1 and lists the
            schedules contains t2 only
        """

        tenant = datagen.random_string(size=10)
        action = self.config.images.action
        # Make sure the time/hour of the schedules are different from other test
        hour = int(self.config.images.hour) + 1
        minute = int(self.config.images.minute)
        increment = 5
        count = 3
        marker = None
        msg = Constants.MESSAGE

        for x in range(count):
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

            if x == 1:
                next_run_after = upd_sch_obj.entity.next_run
                next_run_before = upd_sch_obj.entity.next_run

            minute += increment

        filter_keys = ["next_run_after", "next_run_before", "marker"]
        filter_values = [next_run_after, next_run_before, marker]

        list_sch = \
            self.images_provider.list_schedules_pagination(filter_keys,
                                                           filter_values)

        self.assertTrue(len(list_sch) == 1,
                        msg.format("length of the list", 1, len(list_sch)))

        for sch in list_sch:
            if sch.tenant == tenant:
                self.assertTrue("16:35:00Z" in sch.next_run,
                                msg.format('time', "to contain 16:35:00Z",
                                           sch.next_run))
