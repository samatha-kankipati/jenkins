import ccengine.common.tools.datagen as datagen
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute \
    import BadRequest, InternalServerError, ItemNotFound
from testrepo.common.testfixtures.images import BaseImagesFixture


class TestQonosCreateScheduleNegative(BaseImagesFixture):

    @attr('negative')
    def test_create_schedule_request_missing_body(self):
        """Create schedule with missing body.

        1) Attempt to request the base url of '/schedules' using a POST method
            without a body
        2) Verify that a correct validation message is returned
        """

        with self.assertRaises(BadRequest):
            self.images_provider.schedules_client. \
                create_schedule_missing_body()

    @attr('negative')
    def test_create_schedule_method_mismatch(self):
        """Create schedule with method mismatch.

        1) Attempt to request the base url of '/schedules' using a PUT method
        2) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        method = "PUT"

        with self.assertRaises(ItemNotFound):
            self.images_provider.schedules_client. \
                create_schedule(tenant, action,
                                requestslib_kwargs={'method': method})

    @attr('negative')
    def test_create_schedule_without_passing_tenant(self):
        """Create schedule using valid mandatory parameters without passing the
        tenant.

        1) Create a schedule with all valid mandatory parameters without
            passing the tenant
        2) Verify that a correct validation message is returned
        """

        action = self.config.images.action

        with self.assertRaises(BadRequest):
            self.images_provider.schedules_client. \
                create_schedule(action=action)

    @attr('negative')
    def test_create_schedule_with_blank_tenant_id(self):
        """Create schedule using valid mandatory parameters using a blank
        tenant.

        1) Create a schedule with all valid mandatory parameters using a blank
            tenant
        2) Verify that a correct validation message is returned
        """

        tenant = ""
        action = self.config.images.action

        with self.assertRaises(BadRequest):
            self.images_provider.create_active_schedules(tenant, action)

    @attr('negative')
    def test_create_schedule_with_special_characters_for_tenant_id(self):
        """Create schedule using valid mandatory parameters using a blank
        tenant.

        1) Create a schedule with all valid mandatory parameters using special
            characters for tenant
        2) Verify that a correct validation message is returned
        """

        tenant = "<&&/>"
        action = self.config.images.action
        msg = Constants.MESSAGE

        '''TODO: This should fail when bug #170 is fixed'''
        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

    @attr('negative')
    def test_create_schedule_without_passing_action(self):
        """Create schedule using valid mandatory parameters without passing the
        action.

        1) Create a schedule with all valid mandatory parameters without
            passing the action
        2) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant

        with self.assertRaises(BadRequest):
            self.images_provider.schedules_client. \
                create_schedule(tenant=tenant)

    @attr('negative')
    def test_create_schedule_with_blank_action(self):
        """Create schedule using valid mandatory parameters using a blank
        action.

        1) Create a schedule with all valid mandatory parameters using a blank
            action
        2) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant
        action = ""

        with self.assertRaises(BadRequest):
            self.images_provider.create_active_schedules(tenant, action)

    @attr('negative')
    def test_create_schedule_using_non_existing_minute(self):
        """Create schedule using valid mandatory parameters using a
        non-existing minute.

        1) Create a schedule with all valid mandatory parameters using a
            non-existing minute
        2) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        minute = 61

        with self.assertRaises(InternalServerError):
            self.images_provider.create_active_schedules(tenant, action,
                                                         minute=minute)

    @attr('negative')
    def test_create_schedule_using_letters_for_minute(self):
        """Create schedule using valid mandatory parameters using letters for
        minute.

        1) Create a schedule with all valid mandatory parameters using letters
            for minute
        2) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        minute = "no"

        with self.assertRaises(InternalServerError):
            self.images_provider.create_active_schedules(tenant, action,
                                                         minute=minute)

    @attr('negative')
    def test_create_schedule_using_special_characters_for_minute(self):
        """Create schedule using valid mandatory parameters using special
        characters for minute.

        1) Create a schedule with all valid mandatory parameters using special
            characters for minute
        2) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        minute = "<>"

        with self.assertRaises(InternalServerError):
            self.images_provider.create_active_schedules(tenant, action,
                                                         minute=minute)

    @attr('negative')
    def test_create_schedule_using_non_existing_hour(self):
        """Create schedule using valid mandatory parameters using a
        non-existing hour.

        1) Create a schedule with all valid mandatory parameters using a
            non-existing hour
        2) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        hour = 25

        with self.assertRaises(InternalServerError):
            self.images_provider.create_active_schedules(tenant, action,
                                                         hour=hour)

    @attr('negative')
    def test_create_schedule_using_letters_for_hour(self):
        """Create schedule using valid mandatory parameters using letters for
        hour.

        1) Create a schedule with all valid mandatory parameters using letters
            for hour
        2) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        hour = "no"

        with self.assertRaises(InternalServerError):
            self.images_provider.create_active_schedules(tenant, action,
                                                         hour=hour)

    @attr('negative')
    def test_create_schedule_using_special_characters_for_hour(self):
        """Create schedule using valid mandatory parameters using special
        characters for hour.

        1) Create a schedule with all valid mandatory parameters using special
            characters for hour
        2) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        hour = "<>"

        with self.assertRaises(InternalServerError):
            self.images_provider.create_active_schedules(tenant, action,
                                                         hour=hour)

    @attr('negative')
    def test_create_schedule_for_a_deleted_server(self):
        """Create schedule for a deleted server.

        1) Create a valid server instance
        2) Delete the server
        3) Verify that the response code is 204
        4) Attempt to create a schedule for the deleted server
        5) Verify that the response code is 404
        """

        server_name = datagen.random_string(size=10)
        tenant = self.config.images.tenant
        action = self.config.images.action
        key = self.config.images.metadata_key
        msg = Constants.MESSAGE

        server_obj = self.images_provider.create_active_server(server_name)
        self.assertEquals(server_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     server_obj.status_code))

        instance_id = server_obj.entity.id

        del_server_obj = \
            self.images_provider.servers_client.delete_server(instance_id)
        self.assertEquals(del_server_obj.status_code, 204,
                          msg.format('status_code', 204,
                                     del_server_obj.status_code))

        metadata = {key: instance_id}

        sch_obj = \
            self.images_provider.create_active_schedules(tenant, action,
                                                         metadata=metadata)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))
