from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersRBACFixture
from ccengine.common.decorators import attr


class TestAccessListsRBAC(LoadBalancersRBACFixture):

    @attr('rbac')
    def test_rbac_list_access_list(self):
        '''View error page details with observer and creator roles.'''
        observer_resp = self.observer.get_access_list(self.rbac_lb.id)
        self.assertEquals(observer_resp.status_code, 200, 'Observer should '
                          'be allowed to list access list.')
        creator_resp = self.creator.get_access_list(self.rbac_lb.id)
        self.assertEquals(creator_resp.status_code, 200, 'Creator should '
                          'be allowed to list access list.')

    @attr('rbac')
    def test_rbac_add_access_list_item(self):
        '''Add access list item with observer and creator roles.'''
        address = '11.11.11.11'
        type_ = 'ALLOW'
        observer_resp = self.observer.create_access_list(self.rbac_lb.id,
                                                         address=address,
                                                         type=type_)
        self.assertEquals(observer_resp.status_code, 405, 'Observer should '
                          'not be allowed to create or add to an access list.')
        creator_resp = self.creator.create_access_list(self.rbac_lb.id,
                                                       address=address,
                                                       type=type_)
        self.assertEquals(creator_resp.status_code, 202, 'Creator should '
                          'be allowed to create or add to an access list.')

    @attr('rbac')
    def test_rbac_delete_access_list_item(self):
        '''Delete access list item with observer and creator roles.'''
        address = '10.10.10.10'
        type_ = 'ALLOW'
        self.user_admin.create_access_list(self.rbac_lb.id,
                                           address=address,
                                           type=type_)
        self.lbaas_provider.wait_for_status(self.rbac_lb.id)
        al_list = self.user_admin.get_access_list(self.rbac_lb.id).entity
        al_item = None
        for item in al_list:
            if item.address == address:
                al_item = item
        observer_resp = self.observer.delete_access_list_item(self.rbac_lb.id,
                                                              al_item.id)
        self.assertEquals(observer_resp.status_code, 405, 'Observer should '
                          'not be allowed to delete an access list item.')
        creator_resp = self.creator.delete_access_list_item(self.rbac_lb.id,
                                                            al_item.id)
        self.assertEquals(creator_resp.status_code, 405, 'Creator should '
                          'not be allowed to delete an access list item.')

    @attr('rbac')
    def test_rbac_batch_delete_access_list_item(self):
        '''Batch delete access list items with observer and creator roles.'''
        address = '12.12.12.12'
        type_ = 'ALLOW'
        self.user_admin.create_access_list(self.rbac_lb.id,
                                           address=address,
                                           type=type_)
        self.lbaas_provider.wait_for_status(self.rbac_lb.id)
        al_list = self.user_admin.get_access_list(self.rbac_lb.id).entity
        al_item = None
        for item in al_list:
            if item.address == address:
                al_item = item
        observer_resp = self.observer.batch_delete_access_list_items(
            self.rbac_lb.id, [al_item.id])
        self.assertEquals(observer_resp.status_code, 405, 'Observer should '
                          'not be allowed to batch delete access list items.')
        creator_resp = self.creator.batch_delete_access_list_items(
            self.rbac_lb.id, [al_item.id])
        self.assertEquals(creator_resp.status_code, 405, 'Creator should '
                          'not be allowed to batch delete access list items.')

    @attr('rbac')
    def test_rbac_delete_access_list(self):
        '''Delete entire access list with observer and creator roles.'''
        observer_resp = self.observer.delete_access_list(self.rbac_lb.id)
        self.assertEquals(observer_resp.status_code, 405, 'Observer should '
                          'not be allowed to delete entire access list.')
        creator_resp = self.creator.delete_access_list(self.rbac_lb.id)
        self.assertEquals(creator_resp.status_code, 405, 'Creator should '
                          'not be allowed to delete entire access list.')
