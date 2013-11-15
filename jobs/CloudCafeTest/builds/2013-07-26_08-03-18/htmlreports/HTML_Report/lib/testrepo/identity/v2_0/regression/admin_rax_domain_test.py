from testrepo.common.testfixtures.identity.v2_0.identity \
    import IdentityAdminFixture
from ccengine.common.decorators import attr
from ccengine.common.tools.datagen import rand_name
from ccengine.common.tools.datagen import random_int


class DomainTest(IdentityAdminFixture):

    @classmethod
    def setUpClass(cls):
        super(DomainTest, cls).setUpClass()
        cls.name = rand_name("ccdomname")
        cls.domid = random_int(1, 10000)
        cls.enabled = True
        cls.descr = 'static_descr'
        cls.upd_name = rand_name("ccupdname")

    @classmethod
    def tearDownClass(cls):
        pass

    @attr('regression', type='positive')
    def test_create_user_domain_details(self):
        create_domain = self.admin_client.create_domain(
                name=self.name,
                id=self.domid,
                enabled=self.enabled,
                description=self.descr)
        self.assertEqual(create_domain.status_code, 201,
                msg="Expected response 201 but received  %s" %
                create_domain.status_code)
        self.assertEqual(create_domain.entity.id, str(self.domid),
                msg="Expected id is %s but received  %s" % \
                (self.domid, create_domain.entity.id))
        self.assertEqual(create_domain.entity.name, str(self.name),
                msg="Expected name is %s but received  %s" % \
                (self.name, create_domain.entity.name))
        self.assertEqual(create_domain.entity.enabled, self.enabled,
                msg="Expected enabled state is %s but received  %s" % \
                (self.enabled, create_domain.entity.enabled))
        self.assertEqual(create_domain.entity.description, str(self.descr),
                msg="Expected description is %s but received  %s" % \
                (self.descr, create_domain.entity.description))
        delete_domain = self.admin_client.delete_domain(
                domainId=create_domain.entity.id)
        self.assertEqual(delete_domain.status_code, 204,
                msg="Expected response 204 but received  %s" %
                delete_domain.status_code)
