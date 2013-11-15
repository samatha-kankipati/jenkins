from testrepo.common.testfixtures.stacktach import StackTachFixture
from ccengine.common.decorators import attr


class StackTachTest(StackTachFixture):

    @classmethod
    def setUpClass(cls):
        super(StackTachTest, cls).setUpClass()
        cls.product = 'nova'

    @classmethod
    def tearDownClass(cls):
        super(StackTachTest, cls).tearDownClass()

    @attr(type='smoke')
    def test_get_event_names(self):
        '''
        @summary: Verify that Get Event Names
                  returns 2xx Success response (eg: 200 ok)
        '''

        response = (self.stacktach_provider.client
                    .get_event_names(product=self.product))

        self.assertTrue(response.ok,
                        self.msg.format("status code", "2xx Success response",
                                        response.status_code, response.reason,
                                        response.content))
        resp_entity_obj = response.entity
        self.assertTrue(len(resp_entity_obj) >= 1,
                        msg="The response content is blank")
        for element in resp_entity_obj:
            self.assertIsNotNone(getattr(element, "Event Name"))

    @attr(type='smoke')
    def test_get_host_names(self):
        '''
        @summary: Verify that Get Host Names
                  returns 2xx Success response (eg: 200 ok)
        '''

        response = (self.stacktach_provider.client
                    .get_host_names(product=self.product))

        self.assertTrue(response.ok,
                        self.msg.format("status code", "2xx Success response",
                                        response.status_code, response.reason,
                                        response.content))

        resp_entity_obj = response.entity
        self.assertTrue(len(resp_entity_obj) >= 1,
                        msg="The response content is blank")
        for element in resp_entity_obj:
            self.assertIsNotNone(getattr(element, "Host Name"))

    @attr(type='smoke')
    def test_get_deployments(self):
        '''
        @summary: Verify that Get Deployments
                  returns 2xx Success response (eg: 200 ok)
        '''

        response = self.stacktach_provider.client.get_deployments()

        self.assertTrue(response.ok,
                        self.msg.format("status code", "2xx Success response",
                                        response.status_code, response.reason,
                                        response.content))

        resp_entity_obj = response.entity
        self.assertTrue(len(resp_entity_obj) >= 1,
                        msg="The response content is blank")
        for element in resp_entity_obj:
            self.assertIsNotNone(getattr(element, "Name"))

    @attr(type='smoke')
    def test_get_timings_summary(self):
        '''
        @summary: Verify that Get Timings Summary
                  returns 2xx Success response (eg: 200 ok)
        '''

        response = self.stacktach_provider.client.get_timings_summary()
        self.assertTrue(response.ok,
                        self.msg.format("status code", "2xx Success response",
                                        response.status_code, response.reason,
                                        response.content))
        resp_entity_obj = response.entity
        self.assertTrue(len(resp_entity_obj) >= 1,
                        msg="The response content is blank")
        for element in resp_entity_obj:
            self.assertIsNotNone(getattr(element, "Event"))
            self.assertIsNotNone(getattr(element, "N"))
            self.assertIsNotNone(getattr(element, "Min"))
            self.assertIsNotNone(getattr(element, "Max"))
            self.assertIsNotNone(getattr(element, "Avg"))

    @attr(type='smoke')
    def test_get_kpi(self):
        '''
        @summary: Verify that Get KPI
                  returns 2xx Success response (eg: 200 ok)
        '''

        response = self.stacktach_provider.client.get_kpi()

        self.assertTrue(response.ok,
                        self.msg.format("status code", "2xx Success response",
                                        response.status_code, response.reason,
                                        response.content))
        resp_entity_obj = response.entity
        self.assertTrue(len(resp_entity_obj) >= 1,
                        msg="The response content is blank")
        for element in resp_entity_obj:
            self.assertIsNotNone(getattr(element, "Event"))
            self.assertIsNotNone(getattr(element, "Time"))
            self.assertIsNotNone(getattr(element, "UUID"))
            self.assertIsNotNone(getattr(element, "Deployment"))

    @attr(type='smoke')
    def test_get_kpi_for_tenant_id(self):
        '''
        @summary: Verify that Get KPI For Tenant ID
                  returns 2xx Success response (eg: 200 ok)
        @note:  This test requres that the tenant_id has been actively
            creating usage during the current audit period
        '''
        tenant_id = (self.stacktach_provider
                     .get_active_tenant_id_from_launches())
        response = (self.stacktach_provider.client
                    .get_kpi_for_tenant_id(tenant_id))
        self.assertTrue(response.ok,
                        self.msg.format("status code", "2xx Success response",
                                        response.status_code, response.reason,
                                        response.content))
        resp_entity_obj = response.entity
        self.assertTrue(len(resp_entity_obj) >= 1,
                        msg="The response content is blank")
        for element in resp_entity_obj:
            self.assertIsNotNone(getattr(element, "Event"))
            self.assertIsNotNone(getattr(element, "Time"))
            self.assertIsNotNone(getattr(element, "UUID"))
            self.assertIsNotNone(getattr(element, "Deployment"))

    @attr(type='smoke')
    def test_get_watch_events(self):
        '''
        @summary: Verify that Get Watch Events
                  returns 2xx Success response (eg: 200 ok)
        '''

        response = (self.stacktach_provider.client
                    .get_watch_events(deployment_id='1',
                                      product=self.product))
        self.assertTrue(response.ok,
                        self.msg.format("status code", "2xx Success response",
                                        response.status_code, response.reason,
                                        response.content))

    @attr(type='smoke')
    def test_get_event_id_details(self):
        '''
        @summary: Verify that Get Event ID Details
                  returns 2xx Success response (eg: 200 ok)
        '''

        response = (self.stacktach_provider.client
                    .get_event_id_details(event_id=self.event_id,
                                          product=self.product))

        self.assertTrue(response.ok,
                        self.msg.format("status code", "2xx Success response",
                                        response.status_code, response.reason,
                                        response.content))

    @attr(type='smoke')
    def test_get_timings_for_event_name(self):
        '''
        @summary: Verify that Get Timings For Event
                  returns 2xx Success response (eg: 200 ok)
        '''

        response = (self.stacktach_provider.client
                    .get_timings_for_event_name("compute.instance.reboot"))

        self.assertTrue(response.ok,
                        self.msg.format("status code", "2xx Success response",
                                        response.status_code, response.reason,
                                        response.content))
        resp_entity_obj = response.entity
        self.assertTrue(len(resp_entity_obj) >= 1,
                        msg="The response content is blank")

    @attr(type='smoke')
    def test_get_timings_for_uuid(self):
        '''
        @summary: Verify that Get Timings For UUID
                  returns 2xx Success response (eg: 200 ok)
        '''

        uuid = (self.stacktach_provider
                .get_uuid_from_event_id_details(event_id=self.event_id,
                                                product=self.product))
        response = (self.stacktach_provider
                    .client.get_timings_for_uuid(uuid=uuid))

        self.assertTrue(response.ok,
                        self.msg.format("status code", "2xx Success response",
                                        response.status_code, response.reason,
                                        response.content))
        resp_entity_obj = response.entity
        self.assertTrue(len(resp_entity_obj) >= 1,
                        msg="The response content is blank")
        for element in resp_entity_obj:
            self.assertIsNotNone(getattr(element, "Event"))
            self.assertIsNotNone(getattr(element, "Time (secs)"))

    @attr(type='smoke')
    def test_get_events_for_uuid(self):
        '''
        @summary: Verify that Get Events For UUID
                  returns 2xx Success response (eg: 200 ok)
        '''

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
        self.assertTrue(len(resp_entity_obj) >= 1,
                        msg="The response content is blank")
        for element in resp_entity_obj:
            self.assertIsNotNone(getattr(element, "Event"))
            self.assertIsNotNone(getattr(element, "Deployment"))
            self.assertIsNotNone(getattr(element, "When"))
            self.assertIsNotNone(getattr(element, "Host"))
            self.assertIsNotNone(getattr(element, "State"))

    @attr(type='smoke')
    def test_get_events_for_request_id(self):
        '''
        @summary: Verify that Get Events For Request ID
                  returns 2xx Success response (eg: 200 ok)
        '''

        request_id = (self.stacktach_provider
                      .get_request_id_from_event_id_details(
                          event_id=self.event_id,
                          product=self.product))
        response = (self.stacktach_provider.client
                    .get_events_for_request_id(request_id=request_id))
        self.assertTrue(response.ok,
                        self.msg.format("status code", "2xx Success response",
                                        response.status_code, response.reason,
                                        response.content))
        resp_entity_obj = response.entity
        self.assertTrue(len(resp_entity_obj) >= 1,
                        msg="The response content is blank")
        for element in resp_entity_obj:
            self.assertIsNotNone(getattr(element, "Event"))
            self.assertIsNotNone(getattr(element, "Deployment"))
            self.assertIsNotNone(getattr(element, "When"))
            self.assertIsNotNone(getattr(element, "Host"))
            self.assertIsNotNone(getattr(element, "State"))

    @attr(type='smoke')
    def test_get_reports(self):
        '''
        @summary: Verify that Get Reports
                  returns 2xx Success response (eg: 200 ok)
        '''

        response = self.stacktach_provider.client.get_reports()
        self.assertTrue(response.ok,
                        self.msg.format("status code", "2xx Success response",
                                        response.status_code, response.reason,
                                        response.content))

    @attr(type='smoke')
    def test_get_nova_usage_report_no_escaped_json(self):
        '''
        @summary: Verify that the "nova usage audit" does not contain
            double encoded json
        '''

        report_id = (self.stacktach_provider
                     .get_report_id_by_report_name_from_reports
                     ('nova usage audit'))
        response = (self.stacktach_provider.client
                    .get_report_details(report_id))
        self.assertNotIn('\\', response.json(),
                         self.msg.format("Double encoded json",
                                         "No backslashes",
                                         "Backslashes",
                                         "Escaped characters",
                                         response.json()))
