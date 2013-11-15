'''
@summary: LBaaS related smoke tests for Control Panel
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from datetime import datetime
from ccengine.domain.lbaas.load_balancer import LoadBalancer
from testrepo.common.testfixtures.load_balancers import LoadBalancersFixture

class LoadBalancerSmokeFixture(LoadBalancersFixture):
    '''
    @summary: Simple LBaaS Verification Tests from the Control Panel Perspective 
    '''
    def setUp(self):
        LoadBalancersFixture.setUp(self)
        self.new_name = "ccengine_reach_lb_%s" % (datetime.now().microsecond)
        
    def test_create_simple_load_balancer(self):
        '''
        @summary: Creates a simple load balancer with an auto-generated name
        '''
        ''' Call the Provider to create a new load balancer '''
        response = self.lbaas_provider.create_active_load_balancer(name=self.new_name)
        
        ''' Make sure the response was good '''
        self.assertIsNotNone(response, "Received null response object...")
        self.assertEquals(response.error, None, "Received error: %s" % (response.error))
        self.fixture_log.info("Created new Load Balancer: %s" %(response.entity))
        
        ''' Tell the engine to clean this load balancer up '''
        self.addCleanup(self.lbaas_provider.client.delete_load_balancer, load_balancer_id=response.entity.id)
        
        ''' Make sure we got the load balancer we expected '''
        self.assertEquals(response.entity.name, self.new_name, "Un-Expected name found. Expected: %s, Received: %s" % (self.new_name, response.entity.name))
        
    
