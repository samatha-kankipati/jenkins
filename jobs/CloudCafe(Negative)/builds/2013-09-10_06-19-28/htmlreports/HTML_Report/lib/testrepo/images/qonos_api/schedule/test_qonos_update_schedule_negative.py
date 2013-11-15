from datetime import datetime
from testrepo.common.testfixtures.images import BaseImagesFixture
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute \
    import InternalServerError, ItemNotFound, Forbidden


class TestQonosUpdateScheduleNegative(BaseImagesFixture):

    @attr('negative')
    def test_update_schedule_request_missing_body(self):
        '''Update schedule with missing body'''

        """
        1) Attempt to request the base url of '/schedules/{id}' using a PUT
            method without a body
        2) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        '''TODO: This will fail with bug #176 is fixed'''
        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client. \
                update_schedule_missing_body(sch.id)

    @attr('negative')
    def test_update_schedule_method_mismatch(self):
        '''Update schedule with method mismatch'''

        """
        1) Attempt to request the base url of '/schedules/{id}' using a POST
            method
        2) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        with self.assertRaises(ItemNotFound):
            self.images_provider.schedules_client. \
                update_schedule(sch.id, http_method="POST")

    @attr('negative')
    def test_update_schedule_request_incorrect_parameter(self):
        '''Update schedule with missing body'''

        """
        1) Attempt to request the base url of '/schedules/{id}' using a PUT
            method without a body
        2) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        '''TODO: This will fail with bug #177 is fixed'''
        upd_sch_obj = self.images_provider.schedules_client. \
            update_schedule_incorrect_parameter(sch.id, bad_param='test')
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

    @attr('negative')
    def test_update_schedule_with_blank_tenant(self):
        '''Update schedule using valid mandatory parameters using a blank
        tenant'''

        """
        1) Create a schedule with all valid mandatory parameters
        2) Update the schedule using a blank tenant
        3) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        alt_tenant = ""
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        '''TODO: This will fail with bug #210 is fixed'''
        self.images_provider.schedules_client. \
            update_schedule(id=sch_obj.entity.id, tenant=alt_tenant)

    @attr('negative')
    def test_update_schedule_with_special_characters_for_tenant(self):
        '''Update schedule using valid mandatory parameters using special
        characters for tenant'''

        """
        1) Create a schedule with all valid mandatory parameters
        2) Update the schedule using special characters for tenant
        3) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        alt_tenant = "<&&/>"
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        '''TODO: This will fail with bug #211 is fixed'''
        self.images_provider.schedules_client. \
            update_schedule(id=sch_obj.entity.id, tenant=alt_tenant)

    @attr('negative')
    def test_update_schedule_using_non_existing_minute(self):
        '''Update schedule using valid mandatory parameters using a
        non-existing minute'''

        """
        1) Create a schedule with all valid mandatory parameters
        2) Update the schedule using a non-existing minute
        3) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        minute = 61
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client. \
                update_schedule(id=sch_obj.entity.id, tenant=tenant,
                                minute=minute)

    @attr('negative')
    def test_update_schedule_using_non_existing_hour(self):
        '''Update schedule using valid mandatory parameters using a
        non-existing hour'''

        """
        1) Create a schedule with all valid mandatory parameters
        2) Update the schedule using a non-existing hour
        3) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        hour = 25
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client. \
                update_schedule(id=sch_obj.entity.id, tenant=tenant,
                                hour=hour)

    @attr('negative')
    def test_update_schedule_using_letters_for_minute(self):
        '''Update schedule using valid mandatory parameters using letters for
        minute'''

        """
        1) Create a schedule with all valid mandatory parameters
        2) Update the schedule using letters for minute
        3) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        minute = "no"
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client. \
                update_schedule(id=sch_obj.entity.id, tenant=tenant,
                                minute=minute)

    @attr('negative')
    def test_update_schedule_using_letters_for_hour(self):
        '''Update schedule using valid mandatory parameters using letters for
        hour'''

        """
        1) Create a schedule with all valid mandatory parameters
        2) Update the schedule using letters for hour
        3) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        hour = "no"
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client. \
                update_schedule(id=sch_obj.entity.id, tenant=tenant,
                                hour=hour)

    @attr('negative')
    def test_update_schedule_using_numbers_for_action(self):
        '''Update schedule using valid mandatory parameters using numbers for
        action'''

        """
        1) Create a schedule with all valid mandatory parameters
        2) Update the schedule using numbers for action
        3) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        alt_action = 12345
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        '''TODO: This will fail until RM #883 is fixed'''
        self.images_provider.schedules_client. \
                update_schedule(id=sch_obj.entity.id, tenant=tenant,
                                action=alt_action)

    @attr('negative')
    def test_update_schedule_using_special_characters_for_minute(self):
        '''Update schedule using valid mandatory parameters using special
        characters for minute'''

        """
        1) Create a schedule with all valid mandatory parameters
        2) Update the schedule using special characters for minute
        3) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        minute = "<>"
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client. \
                update_schedule(id=sch_obj.entity.id, tenant=tenant,
                                minute=minute)

    @attr('negative')
    def test_update_schedule_using_special_characters_for_hour(self):
        '''Update schedule using valid mandatory parameters using special
        characters for hour'''

        """
        1) Create a schedule with all valid mandatory parameters
        2) Update the schedule using special characters for hour
        3) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        hour = "<>"
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client. \
                update_schedule(id=sch_obj.entity.id, tenant=tenant,
                                hour=hour)

    @attr('negative')
    def test_update_schedule_using_special_characters_for_action(self):
        '''Update schedule using valid mandatory parameters using special
        characters for action'''

        """
        1) Create a schedule with all valid mandatory parameters
        2) Update the schedule using special characters for action
        3) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        alt_action = "<>"
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        '''TODO: This will fail until RM #883 is fixed'''
        self.images_provider.schedules_client. \
                update_schedule(id=sch_obj.entity.id, tenant=tenant,
                                action=alt_action)

    @attr('negative')
    def test_update_schedule_using_incorrect_format_for_next_run(self):
        '''Update schedule using an incorrect format for next_run'''

        """
        1) Create a schedule
        2) Update the schedule using incorrect format for next_run
        3) Verify that the schedule is not updated and correct validation
            message is returned

        """
        tenant = self.config.images.tenant
        action = self.config.images.action
        alt_next_run = "0000-03-15T12:10:30Z"
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        created_sch = sch_obj.entity

        '''TODO: This will fail when RM #889 is fixed'''
        upd_sch_obj = self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, next_run=alt_next_run)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        alt_next_run = "2013-13-15T12:10:30Z"
        upd_sch_obj = self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, next_run=alt_next_run)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        alt_next_run = "2013-03-32T12:10:30Z"
        upd_sch_obj = self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, next_run=alt_next_run)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        alt_next_run = "2013-03-15T25:10:30Z"
        upd_sch_obj = self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, next_run=alt_next_run)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        alt_next_run = "2013-03-15T12:61:30Z"
        upd_sch_obj = self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, next_run=alt_next_run)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        alt_next_run = "2013-03-15T25:10:30Z"
        upd_sch_obj = self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, next_run=alt_next_run)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        alt_next_run = "2013-03-15T12:61:30Z"
        upd_sch_obj = self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, next_run=alt_next_run)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        alt_next_run = "2013-03-15T12:10:61Z"
        upd_sch_obj = self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, next_run=alt_next_run)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        alt_next_run = "-2013-03-15T12:10:30Z"
        upd_sch_obj = self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, next_run=alt_next_run)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        alt_next_run = "2013-03-15T12:10:30Z-"
        upd_sch_obj = self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, next_run=alt_next_run)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        alt_next_run = "2013-03-1512:10:30Z"
        upd_sch_obj = self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, next_run=alt_next_run)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        alt_next_run = "2013-03-15T12:10:30"
        upd_sch_obj = self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, next_run=alt_next_run)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        alt_next_run = "03-15-2013T12:10:30Z"
        upd_sch_obj = self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, next_run=alt_next_run)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        alt_next_run = "15-03-2013T12:10:30Z"
        upd_sch_obj = self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, next_run=alt_next_run)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        alt_next_run = "15-03-2013"
        upd_sch_obj = self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, next_run=alt_next_run)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        alt_next_run = "T12:10:30Z"
        upd_sch_obj = self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, next_run=alt_next_run)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

    @attr('negative')
    def test_update_schedule_using_incorrect_format_for_created_at(self):
        '''Update schedule using an incorrect format for created_at'''

        """
        1) Create a schedule
        2) Update the schedule using incorrect format for created_at
        3) Verify that the schedule is not updated and correct validation
            message is returned

        """
        tenant = self.config.images.tenant
        action = self.config.images.action
        alt_created_at = "0000-03-15T12:10:30Z"
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        created_sch = sch_obj.entity

        with self.assertRaises(Forbidden):
            self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, created_at=alt_created_at)

        alt_created_at = "2013-13-15T12:10:30Z"
        with self.assertRaises(Forbidden):
            self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, created_at=alt_created_at)

        alt_created_at = "2013-03-32T12:10:30Z"
        with self.assertRaises(Forbidden):
            self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, created_at=alt_created_at)

        alt_created_at = "2013-03-15T25:10:30Z"
        with self.assertRaises(Forbidden):
            self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, created_at=alt_created_at)

        alt_created_at = "2013-03-15T12:61:30Z"
        with self.assertRaises(Forbidden):
            self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, created_at=alt_created_at)

        alt_created_at = "2013-03-15T25:10:30Z"
        with self.assertRaises(Forbidden):
            self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, created_at=alt_created_at)

        alt_created_at = "2013-03-15T12:61:30Z"
        with self.assertRaises(Forbidden):
            self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, created_at=alt_created_at)

        alt_created_at = "2013-03-15T12:10:61Z"
        with self.assertRaises(Forbidden):
            self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, created_at=alt_created_at)

        alt_created_at = "-2013-03-15T12:10:30Z"
        with self.assertRaises(Forbidden):
            self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, created_at=alt_created_at)

        alt_created_at = "2013-03-15T12:10:30Z-"
        with self.assertRaises(Forbidden):
            self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, created_at=alt_created_at)

        alt_created_at = "2013-03-1512:10:30Z"
        with self.assertRaises(Forbidden):
            self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, created_at=alt_created_at)

        alt_created_at = "2013-03-15T12:10:30"
        with self.assertRaises(Forbidden):
            self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, created_at=alt_created_at)

        alt_created_at = "03-15-2013T12:10:30Z"
        with self.assertRaises(Forbidden):
            self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, created_at=alt_created_at)

        alt_created_at = "15-03-2013T12:10:30Z"
        with self.assertRaises(Forbidden):
            self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, created_at=alt_created_at)

        alt_created_at = "15-03-2013"
        with self.assertRaises(Forbidden):
            self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, created_at=alt_created_at)

        alt_created_at = "T12:10:30Z"
        with self.assertRaises(Forbidden):
            self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, created_at=alt_created_at)

    @attr('negative')
    def test_update_schedule_using_incorrect_format_for_updated_at(self):
        '''Update schedule using an incorrect format for updated_at'''

        """
        1) Create a schedule
        2) Update the schedule using incorrect format for updated_at
        3) Verify that the schedule is not updated and correct validation
            message is returned

        """
        tenant = self.config.images.tenant
        action = self.config.images.action
        alt_updated_at = "0000-03-15T12:10:30Z"
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        created_sch = sch_obj.entity

        with self.assertRaises(Forbidden):
            self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, updated_at=alt_updated_at)

        alt_updated_at = "2013-13-15T12:10:30Z"
        with self.assertRaises(Forbidden):
            self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, updated_at=alt_updated_at)

        alt_updated_at = "2013-03-32T12:10:30Z"
        with self.assertRaises(Forbidden):
            self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, updated_at=alt_updated_at)

        alt_updated_at = "2013-03-15T25:10:30Z"
        with self.assertRaises(Forbidden):
            self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, updated_at=alt_updated_at)

        alt_updated_at = "2013-03-15T12:61:30Z"
        with self.assertRaises(Forbidden):
            self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, updated_at=alt_updated_at)

        alt_updated_at = "2013-03-15T25:10:30Z"
        with self.assertRaises(Forbidden):
            self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, updated_at=alt_updated_at)

        alt_updated_at = "2013-03-15T12:61:30Z"
        with self.assertRaises(Forbidden):
            self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, updated_at=alt_updated_at)

        alt_updated_at = "2013-03-15T12:10:61Z"
        with self.assertRaises(Forbidden):
            self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, updated_at=alt_updated_at)

        alt_updated_at = "-2013-03-15T12:10:30Z"
        with self.assertRaises(Forbidden):
            self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, updated_at=alt_updated_at)

        alt_updated_at = "2013-03-15T12:10:30Z-"
        with self.assertRaises(Forbidden):
            self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, updated_at=alt_updated_at)

        alt_updated_at = "2013-03-1512:10:30Z"
        with self.assertRaises(Forbidden):
            self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, updated_at=alt_updated_at)

        alt_updated_at = "2013-03-15T12:10:30"
        with self.assertRaises(Forbidden):
            self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, updated_at=alt_updated_at)

        alt_updated_at = "03-15-2013T12:10:30Z"
        with self.assertRaises(Forbidden):
            self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, updated_at=alt_updated_at)

        alt_updated_at = "15-03-2013T12:10:30Z"
        with self.assertRaises(Forbidden):
            self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, updated_at=alt_updated_at)

        alt_updated_at = "15-03-2013"
        with self.assertRaises(Forbidden):
            self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, updated_at=alt_updated_at)

        alt_updated_at = "T12:10:30Z"
        with self.assertRaises(Forbidden):
            self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, updated_at=alt_updated_at)

    @attr('negative')
    def test_update_schedule_using_incorrect_format_for_last_scheduled(self):
        '''Update schedule using an incorrect format for last_scheduled'''

        """
        1) Create a schedule
        2) Update the schedule using incorrect format for last_scheduled
        3) Verify that the schedule is not updated and correct validation
            message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        alt_last_scheduled = "0000-03-15T12:10:30Z"
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        created_sch = sch_obj.entity

        '''TODO: This will fail until RM #889 is fixed'''
        upd_sch_obj = self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id,
                                last_scheduled=alt_last_scheduled)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        alt_last_scheduled = "2013-13-15T12:10:30Z"
        upd_sch_obj = self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id,
                                last_scheduled=alt_last_scheduled)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        alt_last_scheduled = "2013-03-32T12:10:30Z"
        upd_sch_obj = self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id,
                                last_scheduled=alt_last_scheduled)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        alt_last_scheduled = "2013-03-15T25:10:30Z"
        upd_sch_obj = self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id,
                                last_scheduled=alt_last_scheduled)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        alt_last_scheduled = "2013-03-15T12:61:30Z"
        upd_sch_obj = self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id,
                                last_scheduled=alt_last_scheduled)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        alt_last_scheduled = "2013-03-15T25:10:30Z"
        upd_sch_obj = self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id,
                                last_scheduled=alt_last_scheduled)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        alt_last_scheduled = "2013-03-15T12:61:30Z"
        upd_sch_obj = self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id,
                                last_scheduled=alt_last_scheduled)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        alt_last_scheduled = "2013-03-15T12:10:61Z"
        upd_sch_obj = self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id,
                                last_scheduled=alt_last_scheduled)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        alt_last_scheduled = "-2013-03-15T12:10:30Z"
        upd_sch_obj = self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id,
                                last_scheduled=alt_last_scheduled)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        alt_last_scheduled = "2013-03-15T12:10:30Z-"
        upd_sch_obj = self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id,
                                last_scheduled=alt_last_scheduled)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        alt_last_scheduled = "2013-03-1512:10:30Z"
        upd_sch_obj = self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id,
                                last_scheduled=alt_last_scheduled)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        alt_last_scheduled = "2013-03-15T12:10:30"
        upd_sch_obj = self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id,
                                last_scheduled=alt_last_scheduled)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        alt_last_scheduled = "03-15-2013T12:10:30Z"
        upd_sch_obj = self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id,
                                last_scheduled=alt_last_scheduled)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        alt_last_scheduled = "15-03-2013T12:10:30Z"
        upd_sch_obj = self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id,
                                last_scheduled=alt_last_scheduled)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        alt_last_scheduled = "15-03-2013"
        upd_sch_obj = self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id,
                                last_scheduled=alt_last_scheduled)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        alt_last_scheduled = "T12:10:30Z"
        upd_sch_obj = self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id,
                                last_scheduled=alt_last_scheduled)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

    @attr('negative')
    def test_update_a_deleted_schedule(self):
        '''Update a deleted schedule'''

        """
        1) Create a schedule
        2) Delete the schedule
        3) Verify that the response code is 200
        4) Update the deleted schedule
        5) Verify that the correct error message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        alt_tenant = self.config.images.alt_tenant
        msg = Constants.MESSAGE

        sch_obj = \
            self.images_provider.schedules_client.create_schedule(tenant,
                                                                  action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        del_sch_obj = \
            self.images_provider.schedules_client.delete_schedule(sch.id)
        self.assertEquals(del_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     del_sch_obj.status_code))

        with self.assertRaises(ItemNotFound):
            self.images_provider.schedules_client. \
                update_schedule(id=sch.id, tenant=alt_tenant)

    @attr('negative')
    def test_update_schedule_for_next_run(self):
        '''Update schedule for auto-generated parameter - next_run'''

        """
        1) Create a schedule
        2) Update the schedule with new next_run value
        3) Verify that the schedule is not updated and correct validation
            message is returned

        """
        tenant = self.config.images.tenant
        action = self.config.images.action
        alt_next_run = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        created_sch = sch_obj.entity

        '''TODO: This will fail when RM #889 is fixed'''
        upd_sch_obj = self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, next_run=alt_next_run)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

    @attr('negative')
    def test_update_schedule_for_created_at(self):
        '''Update schedule for auto-generated parameter - created_at'''

        """
        1) Create a schedule
        2) Update the schedule with new created_at value
        3) Verify that the schedule is not updated and correct validation
            message is returned

        """
        tenant = self.config.images.tenant
        action = self.config.images.action
        alt_created_at = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        created_sch = sch_obj.entity

        with self.assertRaises(Forbidden):
            self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, created_at=alt_created_at)

    @attr('negative')
    def test_update_schedule_for_updated_at(self):
        '''Update schedule for auto-generated parameter - updated_at'''

        """
        1) Create a schedule
        2) Update the schedule with new updated_at value
        3) Verify that the schedule is not updated and correct validation
            message is returned

        """
        tenant = self.config.images.tenant
        action = self.config.images.action
        alt_updated_at = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        created_sch = sch_obj.entity

        with self.assertRaises(Forbidden):
            self.images_provider.schedules_client. \
                update_schedule(id=created_sch.id, updated_at=alt_updated_at)

    @attr('negative')
    def test_update_schedule_for_last_scheduled(self):
        '''Update schedule for auto-generated parameter - last_scheduled'''

        """
        1) Create a schedule
        2) Update the schedule with new last_scheduled value
        3) Verify that the schedule is not updated and correct validation
            message is returned

        """
        tenant = self.config.images.tenant
        action = self.config.images.action
        alt_last_scheduled = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        created_sch = sch_obj.entity

        '''TODO: This will fail when bug #48 is fixed'''
        self.images_provider.schedules_client. \
            update_schedule(id=created_sch.id,
                            last_scheduled=alt_last_scheduled)
