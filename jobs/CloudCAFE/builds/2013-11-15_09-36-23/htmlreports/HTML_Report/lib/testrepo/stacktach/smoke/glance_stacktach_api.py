from ccengine.common.decorators import attr
from testrepo.common.testfixtures.stacktach import StackTachFixture


class GlanceStackTachTest(StackTachFixture):

    @classmethod
    def setUpClass(cls):
        super(GlanceStackTachTest, cls).setUpClass()
        cls.product = 'glance'
        cls.event_type = 'image.create'

    @attr(type='smoke')
    def test_get_event_names(self):
        """
        @summary: Verify that Get Event Names
                  returns 2xx Success response (eg: 200 ok)
        """

        response = (self.stacktach_provider.client
                    .get_event_names(product=self.product))
        self.assertTrue(response.ok,
                        self.msg.format("status code", "2xx Success response",
                                        response.status_code, response.reason,
                                        response.content))
        resp_entity_obj = response.entity
        self.assertGreaterEqual(len(resp_entity_obj), 1,
                                msg="The response content is blank")
        for element in resp_entity_obj:
            self.assertIsNotNone(getattr(element, "Event Name"))

    @attr(type='smoke')
    def test_get_watch_events(self):
        """
        @summary: Verify that Get Watch Events
                  returns 2xx Success response (eg: 200 ok)
        """

        response = (self.stacktach_provider.client
                    .get_watch_events(deployment_id='1',
                                      product=self.product))
        self.assertTrue(response.ok,
                        self.msg.format("status code", "2xx Success response",
                                        response.status_code, response.reason,
                                        response.content))

    @attr(type='smoke')
    def test_get_event_id_details(self):
        """
        @summary: Verify that Get Event ID Details
                  returns 2xx Success response (eg: 200 ok)
        """

        self.event_id = (self.stacktach_provider
                         .get_event_id_from_event_type_details(
                             event_type=self.event_type,
                             product=self.product))
        response = (self.stacktach_provider.client
                    .get_event_id_details(event_id=self.event_id,
                                          product=self.product))

        self.assertTrue(response.ok,
                        self.msg.format("status code", "2xx Success response",
                                        response.status_code, response.reason,
                                        response.content))

    @attr(type='smoke')
    def test_get_events_for_uuid(self):
        """
        @summary: Verify that Get Events For UUID
                  returns 2xx Success response (eg: 200 ok)
        """

        self.event_id = (self.stacktach_provider
                         .get_event_id_from_event_type_details(
                             event_type=self.event_type,
                             product=self.product))
        uuid = (self.stacktach_provider
                .get_uuid_from_event_id_details(event_id=self.event_id,
                                                product=self.product))
        response = (self.stacktach_provider.client
                    .get_events_for_uuid(uuid=uuid, product=self.product))
        self.assertTrue(response.ok,
                        self.msg.format("status code", "2xx Success response",
                                        response.status_code, response.reason,
                                        response.content))
        resp_entity_obj = response.entity
        self.assertGreater(len(resp_entity_obj), 0,
                           "The response content is blank")
        for element in resp_entity_obj:
            self.assertIsNotNone(getattr(element, "Event"))
            self.assertIsNotNone(getattr(element, "Deployment"))
            self.assertIsNotNone(getattr(element, "When"))
            self.assertIsNotNone(getattr(element, "Host"))
            self.assertIsNotNone(getattr(element, "Status"))

    @attr(type='smoke')
    def test_get_host_names(self):
        """
        @summary: Verify that Get Host Names
                  returns 2xx Success response (eg: 200 ok)
        """

        response = (self.stacktach_provider.client
                    .get_host_names(product=self.product))

        self.assertTrue(response.ok,
                        self.msg.format("status code", "2xx Success response",
                                        response.status_code, response.reason,
                                        response.content))

        resp_entity_obj = response.entity
        self.assertGreaterEqual(len(resp_entity_obj), 1,
                                msg="The response content is blank")
        for element in resp_entity_obj:
            self.assertIsNotNone(getattr(element, "Host Name"))

    @attr(type='negative')
    def test_watch_events_with_invalid_deployment(self):
        """
        @summary: Verify that Get Watch Events with
            Invalid Deployment ID fails
        """

        response = (self.stacktach_provider.client
                    .get_watch_events(deployment_id='aa',
                                      product=self.product))
        self.assertFalse(response.ok,
                         self.msg.format("status code",
                                         "Not a 2xx Success response",
                                         response.status_code, response.reason,
                                         response.content))
        resp_entity_obj = response.entity
        self.assertIsNone(resp_entity_obj,
                          msg="The response entity is not NONE")

    @attr(type='negative')
    def test_get_invalid_event_id_details(self):
        """
        @summary: Verify that a Get on Invalid Event ID Details fails
        """

        response = (self.stacktach_provider.client
                    .get_event_id_details(event_id='aa',
                                          product=self.product))
        self.assertFalse(response.ok,
                         self.msg.format("status code",
                                         "Not a 2xx Success response",
                                         response.status_code, response.reason,
                                         response.content))
        resp_entity_obj = response.entity
        self.assertIsNone(resp_entity_obj,
                          msg="The response entity is not NONE")

    @attr(type='negative')
    def test_get_events_for_invalid_uuid(self):
        """
        @summary: Verify that a Get on Events For Invalid UUID fails
        """

        response = (self.stacktach_provider.client
                    .get_events_for_uuid(uuid="aa", product=self.product))
        self.assertFalse(response.ok,
                         self.msg.format("status code",
                                         "Not a 2xx Success response",
                                         response.status_code, response.reason,
                                         response.content))
        resp_entity_obj = response.entity
        self.assertGreaterEqual(len(resp_entity_obj), 1,
                                msg="The response content is blank")
        for element in resp_entity_obj:
            self.assertIsNotNone(getattr(element, "Error"))
            self.assertIsNotNone(getattr(element, "Message"))
