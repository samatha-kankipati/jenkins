from testrepo.common.testfixtures.autoscale import AutoscaleFixture


class GetListEntityStatusTest(AutoscaleFixture):

    @classmethod
    def setUpClass(cls):
        super(GetListEntityStatusTest, cls).setUpClass()
        ''' create a scaling group with 3 min entities'''
        cls.gc_max_entities = 10
        group_response = cls.autoscale_provider.create_scaling_group_given(
            gc_min_entities=cls.gc_min_entities_alt,
            gc_max_entities=cls.gc_max_entities)
        cls.group = group_response.entity
        cls.resources.add(cls.group.id,
                          cls.autoscale_client.delete_scaling_group)
        cls.group_state_response = cls.autoscale_client.list_status_entities_sgroups(
            cls.group.id)
        cls.group_state = cls.group_state_response.entity

    @classmethod
    def tearDownClass(cls):
        super(GetListEntityStatusTest, cls).tearDownClass()

    def test_entity_status_response(self):
        self.assertEquals(200, self.group_state_response.status_code,
                          msg="The list entities call failed with %s"
                          % self.group_state_response.status_code)
        self.assertTrue(self.group_state_response.headers is not None,
                        msg="The headers are not as expected %s"
                        % self.group_state_response.headers)
        self.validate_headers(self.group_state_response.headers)

    def test_entity_status(self):
        group_pending_count = len(self.group_state.pending)
        group_active_count = len(self.group_state.active)
        self.assertEquals(self.group_state.paused, False,
                          msg="The scaling group status is paused upon creation")
        self.assertGreaterEqual(self.group_state.steadyState, self.gc_min_entities_alt,
                                msg="Less or more than required number of servers are in steady state")
        self.assertGreaterEqual((group_active_count + group_pending_count), self.gc_min_entities_alt,
                                msg="Total server count is less minEntities")
        self.assertLessEqual((group_active_count + group_pending_count), self.gc_max_entities,
                             msg="Total server count is over maxEntities")
