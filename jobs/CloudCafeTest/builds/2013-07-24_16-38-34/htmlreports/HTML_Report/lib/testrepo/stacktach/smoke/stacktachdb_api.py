from datetime import datetime, timedelta

from testrepo.common.testfixtures.stacktach import StackTachDBFixture
from ccengine.common.decorators import attr
from ccengine.common.tools.datatools import string_to_datetime



class StackTachDBTest(StackTachDBFixture):

    @classmethod
    def setUpClass(cls):
        super(StackTachDBTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(StackTachDBTest, cls).tearDownClass()

    @attr(type='smoke')
    def test_list_launches(self):
        '''
        @summary: Verify that List Launches records
                  returns 2xx Success response (eg: 200 ok)
        '''

        response = self.stacktachdb_provider.client.list_launches()
        response_entity_object = response.entity
        self.assertTrue(response.ok,
                        self.msg.format("status code", "2xx Success response",
                                        response.status_code,
                                        response.reason,
                                        response.content))
        self.verify_launches_entity_attribute_values(response_entity_object)

    @attr(type='smoke')
    def test_list_deletes(self):
        '''
        @summary: Verify that List Deletes records
                  returns 2xx Success response (eg: 200 ok)
        '''

        response = self.stacktachdb_provider.client.list_deletes()
        response_entity_object = response.entity
        self.assertTrue(response.ok,
                        self.msg.format("status code", "2xx Success response",
                                        response.status_code,
                                        response.reason,
                                        response.content))
        self.assertTrue(len(response_entity_object) >= 1,
                        msg="The response content is blank")
        self.verify_deletes_entity_attribute_values(response_entity_object)

    @attr(type='smoke')
    def test_list_exists(self):
        '''
        @summary: Verify that List Exists records
                  returns 2xx Success response (eg: 200 ok)
        '''

        response = self.stacktachdb_provider.client.list_exists()
        response_entity_object = response.entity
        self.assertTrue(response.ok,
                        self.msg.format("status code", "2xx Success response",
                                        response.status_code,
                                        response.reason,
                                        response.content))
        self.verify_exists_entity_attribute_values(response_entity_object)

    @attr(type='smoke')
    def test_get_launch(self):
        '''
        @summary: Verify that Get Launch record by event id
                  returns 2xx Success response (eg: 200 ok)
        '''

        response = self.stacktachdb_provider.client.list_launches()
        event_id = str(response.entity[0].id)
        response = self.stacktachdb_provider.client.get_launch(event_id)
        self.assertTrue(response.ok,
                        self.msg.format("status code", "2xx Success response",
                                        response.status_code,
                                        response.reason,
                                        response.content))

    @attr(type='smoke')
    def test_get_delete(self):
        '''
        @summary: Verify that Get Delete record by event id
                  returns 2xx Success response (eg: 200 ok)
        '''

        response = self.stacktachdb_provider.client.list_deletes()
        event_id = str(response.entity[0].id)
        response = self.stacktachdb_provider.client.get_delete(event_id)
        self.assertTrue(response.ok,
                        self.msg.format("status code", "2xx Success response",
                                        response.status_code,
                                        response.reason,
                                        response.content))

    @attr(type='smoke')
    def test_get_exist(self):
        '''
        @summary: Verify that Get Exist record by event id
                  returns 2xx Success response (eg: 200 ok)
             1.  List all exists
             2.  Get the first exists entry's exists id
             4.  Check for exists id
        '''

        response = self.stacktachdb_provider.client.list_exists()
        exists_id = response.entity[0].id
        response = self.stacktachdb_provider.client.get_exist(exists_id)
        self.assertTrue(response.ok,
                        self.msg.format("status code", "2xx Success response",
                                        response.status_code,
                                        response.reason,
                                        response.content))

    @attr(type='smoke')
    def test_get_launches_by_date_min(self):
        '''
        @summary: Verify that Get Launches by minimum date
                  returns 2xx Success response (eg: 200 ok)
        '''

        date_min = str(datetime.utcnow() - timedelta(days=self.days_passed))
        response = (self.stacktachdb_provider
                    .client
                    .get_launches_by_date_min(launched_at_min=date_min))
        response_entity_object = response.entity

        self.assertTrue(response.ok,
                        self.msg.format("status code", "2xx Success response",
                                        response.status_code,
                                        response.reason,
                                        response.content))
        self.verify_launches_entity_attribute_values(response_entity_object)

    @attr(type='smoke')
    def test_get_launches_by_date_max(self):
        '''
        @summary: Verify that Get Launches by maximum date
                  returns 2xx Success response (eg: 200 ok)
            1.  Get Launches for the past 2 days
            2.  Iterate through the list to look for a non null launched_at
            3.  Add 1 day to the launched at for maximum date filter
        '''

        date_min = str(datetime.utcnow() - timedelta(days=self.days_passed))
        response = (self.stacktachdb_provider
                    .client
                    .get_launches_by_date_min(launched_at_min=date_min))

        for launch in response.entity:
            if launch.launched_at is not None:
                launched_at = str(launch.launched_at)
                break
        # Microseconds may or may not be returned
        date_obj = string_to_datetime(launched_at)
        date_max = str(date_obj + timedelta(days=1))
        response = (self.stacktachdb_provider
                    .client
                    .get_launches_by_date_max(launched_at_max=date_max))
        response_entity_object = response.entity

        self.assertTrue(response.ok,
                        self.msg.format("status code", "2xx Success response",
                                        response.status_code,
                                        response.reason,
                                        response.content))
        self.verify_launches_entity_attribute_values(response_entity_object)

    @attr(type='smoke')
    def test_get_launches_by_date_min_and_max(self):
        '''
        @summary: Verify that Get Launches by minimum and maximum date
                  returns 2xx Success response (eg: 200 ok)
        '''

        date_max = str(datetime.utcnow())
        date_min = str(datetime.utcnow() - timedelta(days=self.days_passed))

        response = (self.stacktachdb_provider
                    .client
                    .get_launches_by_date_min_and_date_max(
                    launched_at_min=date_min,
                    launched_at_max=date_max))
        response_entity_object = response.entity

        self.assertTrue(response.ok,
                        self.msg.format("status code", "2xx Success response",
                                        response.status_code,
                                        response.reason,
                                        response.content))
        self.verify_launches_entity_attribute_values(response_entity_object)

    @attr(type='smoke')
    def test_get_deletes_by_date_min(self):
        '''
        @summary: Verify that Get Deletes by minimum date
                  returns 2xx Success response (eg: 200 ok)
        '''

        date_min = str(datetime.utcnow() - timedelta(days=self.days_passed))
        response = (self.stacktachdb_provider
                    .client
                    .get_deletes_by_date_min(deleted_at_min=date_min))
        response_entity_object = response.entity

        self.assertTrue(response.ok,
                        self.msg.format("status code", "2xx Success response",
                                        response.status_code,
                                        response.reason,
                                        response.content))
        self.assertTrue(len(response_entity_object) >= 1,
                        msg="The response content is blank")
        self.verify_deletes_entity_attribute_values(response_entity_object)

    @attr(type='smoke')
    def test_get_deletes_by_date_max(self):
        '''
        @summary: Verify that Get Deletes by maximum date
                  returns 2xx Success response (eg: 200 ok)
            1.  Get Deletes for the past 2 days
            2.  Add 1 day to the deleted at for maximum date filter
        '''

        date_min = str(datetime.utcnow() - timedelta(days=self.days_passed))
        response = (self.stacktachdb_provider
                    .client
                    .get_deletes_by_date_min(deleted_at_min=date_min))
        deleted_at = response.entity[0].deleted_at
        # Microseconds may or may not be returned
        date_obj = string_to_datetime(deleted_at)
        date_max = str(date_obj + timedelta(days=1))
        response = (self.stacktachdb_provider
                    .client
                    .get_deletes_by_date_max(deleted_at_max=date_max))
        response_entity_object = response.entity

        self.assertTrue(response.ok,
                        self.msg.format("status code", "2xx Success response",
                                        response.status_code,
                                        response.reason,
                                        response.content))
        self.assertTrue(len(response_entity_object) >= 1,
                        msg="The response content is blank")
        self.verify_deletes_entity_attribute_values(response_entity_object)

    @attr(type='smoke')
    def test_get_deletes_by_date_min_and_max(self):
        '''
        @summary: Verify that Get Deletes by minimum and maximum date
                  returns 2xx Success response (eg: 200 ok)
        '''

        date_max = str(datetime.utcnow())
        date_min = str(datetime.utcnow() - timedelta(days=self.days_passed))

        response = (self.stacktachdb_provider
                    .client
                    .get_deletes_by_date_min_and_date_max(
                    deleted_at_min=date_min,
                    deleted_at_max=date_max))
        response_entity_object = response.entity

        self.assertTrue(response.ok,
                        self.msg.format("status code", "2xx Success response",
                                        response.status_code,
                                        response.reason,
                                        response.content))
        self.assertTrue(len(response_entity_object) >= 1,
                        msg="The response content is blank")
        self.verify_deletes_entity_attribute_values(response_entity_object)

    @attr(type='smoke')
    def test_list_launches_for_uuid(self):
        '''
        @summary: Verify that List Launches by uuid
                  returns 2xx Success response (eg: 200 ok)
        '''

        date_max = str(datetime.utcnow())
        date_min = str(datetime.utcnow() - timedelta(days=self.days_passed))

        response = (self.stacktachdb_provider
                    .client
                    .get_launches_by_date_min_and_date_max(
                    launched_at_min=date_min,
                    launched_at_max=date_max))
        uuid = response.entity[0].instance
        response = (self.stacktachdb_provider.client
                    .list_launches_for_uuid(instance=uuid))
        response_entity_object = response.entity

        self.assertTrue(response.ok,
                        self.msg.format("status code", "2xx Success response",
                                        response.status_code,
                                        response.reason,
                                        response.content))
        self.verify_launches_entity_attribute_values(response_entity_object)

    @attr(type='smoke')
    def test_list_deletes_for_uuid(self):
        '''
        @summary: Verify that List Deletes by uuid
                  returns 2xx Success response (eg: 200 ok)
        '''

        date_max = str(datetime.utcnow())
        date_min = str(datetime.utcnow() - timedelta(days=self.days_passed))

        response = (self.stacktachdb_provider
                    .client
                    .get_deletes_by_date_min_and_date_max(
                    deleted_at_min=date_min,
                    deleted_at_max=date_max))
        uuid = response.entity[0].instance
        response = (self.stacktachdb_provider.client
                    .list_deletes_for_uuid(instance=uuid))
        response_entity_object = response.entity

        self.assertTrue(response.ok,
                        self.msg.format("status code", "2xx Success response",
                                        response.status_code,
                                        response.reason,
                                        response.content))
        self.assertTrue(len(response_entity_object) == 1,
                        msg="The response content is blank")
        self.verify_deletes_entity_attribute_values(response_entity_object)

    @attr(type='smoke')
    def test_list_exists_for_uuid(self):
        '''
        @summary: Verify that List Exists by uuid
                  returns 2xx Success response (eg: 200 ok)
             1.  Find a server that was deleted 2 days ago
             2.  End of audit period was 1 day ago
             3.  Check for exists event
        '''
        date_max = str(datetime.utcnow())
        date_min = str(datetime.utcnow() - timedelta(days=self.days_passed))

        response = (self.stacktachdb_provider
                    .client
                    .get_deletes_by_date_min_and_date_max(
                    deleted_at_min=date_min,
                    deleted_at_max=date_max))
        uuid = response.entity[0].instance
        response = (self.stacktachdb_provider.client
                    .list_exists_for_uuid(instance=uuid))

        self.assertTrue(response.ok,
                        self.msg.format("status code", "2xx Success response",
                                        response.status_code,
                                        response.reason,
                                        response.content))

    def verify_launches_entity_attribute_values(self, response_entity_object):
        self.assertTrue(len(response_entity_object) >= 1,
                        msg="The response content is blank")
        for element in response_entity_object:
            self.assertIsNotNone(element.id)
            self.assertIsNotNone(element.request_id)
            self.assertIsNotNone(element.instance)
            self.assertIsNotNone(element.tenant)
            self.assertTrue(hasattr(element, "instance_type_id"))
            self.assertTrue(hasattr(element, "launched_at"))

    def verify_exists_entity_attribute_values(self, response_entity_object):
        self.assertTrue(len(response_entity_object) >= 1,
                        msg="The response content is blank")
        for element in response_entity_object:
            self.assertIsNotNone(element.id)
            self.assertIsNotNone(element.raw)
            self.assertIsNotNone(element.message_id)
            self.assertIsNotNone(element.instance)
            self.assertIsNotNone(element.instance_type_id)
            self.assertIsNotNone(element.launched_at)
            self.assertIsNotNone(element.tenant)
            self.assertIsNotNone(element.status)
            self.assertIsNotNone(element.send_status)
            self.assertIsNotNone(element.received)
            self.assertIsNotNone(element.audit_period_beginning)
            self.assertIsNotNone(element.audit_period_ending)
            self.assertTrue(hasattr(element, "usage"))
            self.assertTrue(hasattr(element, "fail_reason"))
            self.assertTrue(hasattr(element, "deleted_at"))
            self.assertTrue(hasattr(element, "delete"))

    def verify_deletes_entity_attribute_values(self, response_entity_object):
        for element in response_entity_object:
            self.assertIsNotNone(element.id)
            self.assertIsNotNone(element.raw)
            self.assertIsNotNone(element.instance)
            self.assertIsNotNone(element.deleted_at)
            self.assertIsNotNone(element.launched_at)
