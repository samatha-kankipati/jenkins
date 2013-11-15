'''
@summary: Base Classes for Autoscale Test Suites (Collections of Test Cases)
@note: Correspondes DIRECTLY TO A unittest.TestCase
@see: http://docs.python.org/library/unittest.html#unittest.TestCase
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from testrepo.common.testfixtures.fixtures import BaseTestFixture
from ccengine.providers.autoscale.autoscale_api import AutoscaleAPIProvider \
    as _AutoscaleAPIProvider
from ccengine.common.resource_manager.resource_pool import ResourcePool
from ccengine.common.tools.datagen import rand_name


class AutoscaleFixture(BaseTestFixture):
    '''
    @summary: Fixture for an Autoscale test.
    '''

    @classmethod
    def setUpClass(cls):
        super(AutoscaleFixture, cls).setUpClass()
        cls.resources = ResourcePool()
        cls.autoscale_provider = _AutoscaleAPIProvider(cls.config)
        cls.autoscale_client = cls.autoscale_provider.autoscale_client
        cls.gc_name = cls.config.autoscale.gc_name
        cls.gc_cooldown = int(cls.config.autoscale.gc_cooldown)
        cls.gc_min_entities = int(cls.config.autoscale.gc_min_entities)
        cls.gc_min_entities_alt = int(cls.config.autoscale.gc_min_entities_alt)
        cls.lc_name = cls.config.autoscale.lc_name
        cls.lc_flavor_ref = cls.config.autoscale.lc_flavor_ref
        cls.lc_image_ref = cls.config.autoscale.lc_image_ref
        cls.sp_name = rand_name(cls.config.autoscale.sp_name)
        cls.sp_cooldown = int(cls.config.autoscale.sp_cooldown)
        cls.sp_change = int(cls.config.autoscale.sp_change)
        cls.sp_change_percent = int(cls.config.autoscale.sp_change_percent)
        cls.sp_steady_state = cls.config.autoscale.sp_steady_state
        cls.upd_sp_change = int(cls.config.autoscale.upd_sp_change)
        cls.lc_load_balancers = cls.config.autoscale.lc_load_balancers
        cls.sp_list = cls.config.autoscale.sp_list
        cls.wb_name = rand_name(cls.config.autoscale.wb_name)

    def validate_headers(self, headers):
        if headers.get("transfer-encoding"):
            self.assertEqual(headers["transfer-encoding"], "chunked",
                             msg="Response header transfer-encoding is not chunked")
        self.assertTrue("TwistedWeb" in headers["server"],
                        msg="Response header server is not TwistedWeb")
        self.assertEquals(headers["content-type"], 'application/json',
                        msg="Response header content-type is None")
        self.assertTrue(headers["date"] is not None,
                        msg="Time not included")
        self.assertTrue(headers["x-response-id"] is not None,
                        msg="No x-response-id")

    @classmethod
    def tearDownClass(cls):
        super(AutoscaleFixture, cls).tearDownClass()
        cls.resources.release()


class ScalingGroupFixture(AutoscaleFixture):
    '''
    @summary: Creates a scaling group using the default from
              the test data
    '''

    @classmethod
    def setUpClass(cls, gc_name=None, gc_cooldown=None, gc_min_entities=None,
                   gc_max_entities=None, gc_metadata=None, lc_name=None,
                   lc_image_ref=None, lc_flavor_ref=None,
                   lc_personality=None, lc_metadata=None,
                   lc_disk_config=None, lc_networks=None,
                   lc_load_balancers=None, sp_list=None):
        '''
        @summary:Creates a scaling group with the server launch config,
                 loadbalancers and scaling policies
        '''

        super(ScalingGroupFixture, cls).setUpClass()
        if gc_name is None:
            gc_name = rand_name('testscalinggroup')
        if gc_cooldown is None:
            gc_cooldown = cls.gc_cooldown
        if gc_min_entities is None:
            gc_min_entities = cls.gc_min_entities
        if lc_name is None:
            lc_name = rand_name('testscalinggroupserver')
        if lc_flavor_ref is None:
            lc_flavor_ref = cls.lc_flavor_ref
        if lc_image_ref is None:
            lc_image_ref = cls.lc_image_ref
        cls.create_response = cls.autoscale_client.\
            create_scaling_group(
                gc_name, gc_cooldown,
                gc_min_entities,
                lc_name, lc_image_ref,
                lc_flavor_ref,
                gc_max_entities=gc_max_entities,
                gc_metadata=gc_metadata,
                lc_personality=lc_personality,
                lc_metadata=lc_metadata,
                lc_disk_config=lc_disk_config,
                lc_networks=lc_networks,
                lc_load_balancers=lc_load_balancers,
                sp_list=sp_list)
        cls.group = cls.create_response.entity
        cls.resources.add(cls.group.id,
                          cls.autoscale_client.delete_scaling_group)

    @classmethod
    def tearDownClass(cls):
        super(ScalingGroupFixture, cls).tearDownClass()


class ScalingPolicyFixture(BaseTestFixture):
    '''
    @summary: Creates a scaling policy using the default from
              the test data
    '''

    @classmethod
    def setUpClass(cls, name=None, cooldown=None, change=None,
                   change_percent=None, steady_state=None):

        super(ScalingPolicyFixture, cls).setUpClass()
        if name is None:
            name = rand_name('testscalingpolicy')
        if cooldown is None:
            cooldown = cls.sp_cooldown
        if change:
            create_response = cls.autoscale_client.create_policy(name, cooldown,
                                                                 change=change)
        if change_percent:
            create_response = cls.autoscale_client.create_policy(name, cooldown,
                                                                 change_percent=change_percent)
        if steady_state:
            create_response = cls.autoscale_client.create_policy(name, cooldown,
                                                                 steady_state=steady_state)
        else:
            change = cls.sp_change
            create_response = cls.autoscale_client.create_policy(name, cooldown,
                                                                 change=change)
        cls.resources.add(cls.created_reponse.id,
                          cls.autoscale_client.delete_scaling_policy)
        cls.created_scaling_policy = create_response.entity

    @classmethod
    def tearDownClass(cls):
        super(ScalingPolicyFixture, cls).tearDownClass()
