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
        cls.domid = random_int(10000, 90000)
        cls.enabled = True
        cls.descr = 'static_descr'
        cls.create_domain = cls.admin_client.create_domain(
            name=cls.name,
            id=cls.domid,
            enabled=cls.enabled,
            description=cls.descr)

    @classmethod
    def tearDownClass(cls):
        cls.admin_client.delete_domain(
            domain_id=cls.create_domain.entity.id)

    @attr('regression', type='positive')
    def test_create_user_domain_details(self):
        """
        Verify Create domain call response

        """
        self.assertEqual(
            self.create_domain.status_code, 201,
            msg=("Expected response 201 but received {0}"
                 .format(self.create_domain.status_code)))
        self.assertEqual(
            self.create_domain.entity.id, str(self.domid),
            msg=("Expected id is {0} but received  {1}"
                 .format(self.domid, self.create_domain.entity.id)))
        self.assertEqual(
            self.create_domain.entity.name, str(self.name),
            msg=("Expected name is {0} but received {1}"
                 .format(self.name, self.create_domain.entity.name)))
        self.assertEqual(
            self.create_domain.entity.enabled, self.enabled,
            msg=("Expected enabled state is {0} but received {1}"
                 .format(self.enabled, self.create_domain.entity.enabled)))
        self.assertEqual(
            self.create_domain.entity.description, str(self.descr),
            msg=("Expected description is {0} but received {1}"
                 .format(self.descr, self.create_domain.entity.description)))
