from ccengine.common.decorators import attr
from ccengine.common.tools.datagen import random_int, rand_name
from testrepo.common.testfixtures.identity.v1_1.identity \
    import IdentityFixture


class MossoBaseUrlAuthTest(IdentityFixture):
    @classmethod
    def setUpClass(cls):
        super(MossoBaseUrlAuthTest, cls).setUpClass()
        cls.uid = rand_name("ccUserAdmin")
        cls.key = 'asdasdasd-adsasdads-asdasdasd-adsadsasd'
        cls.mosso_id = ((-1) * random_int(1000000, 9000000))
        enabled = True
        cls.create_user = cls.admin_client.create_user(
            id=cls.uid,
            key=cls.key,
            enabled=enabled,
            mosso_id=cls.mosso_id)
        cls.get_user_id = cls.admin_client_vsec.get_user_by_name(name=cls.uid)

        cls.baseurl_id = random_int(1000000, 9000000)
        add_baseurl_resp = cls.admin_client.add_base_url(
            id=cls.baseurl_id, user_type="MOSSO", region="ORD",
            service_name="TestService", default=True, enabled=False,
            public_url="https://otherstorage.clouddrive.com/v1",
            internal_url="https://otherstorage-snet.clouddrive.com/v1",
            admin_url="https://otherstorage-snet.clouddrive.com/v1")

    @classmethod
    def tearDownClass(cls):
        cls.admin_client_vsec.delete_user(
            user_id=cls.get_user_id.entity.id)
        cls.service_client.delete_user_hard(
            user_id=cls.get_user_id.entity.id)

        cls.admin_client_vsec.delete_endpoint_template(
            endpoint_template_id=cls.baseurl_id)

    @attr('negative', type='negative')
    def test_add_neg_mosso_disabled_baseurl_user(self):
        normal_response_codes = [400]
        v1_default = True

        add_base_url = self.admin_client.add_user_base_url(
            id=self.baseurl_id,
            v1_default=v1_default,
            user_id=self.create_user.entity.id)
        self.assertIn(add_base_url.status_code,
                      normal_response_codes,
                      msg='Add base URLs expected {0} received {1}'.format(
                          normal_response_codes,
                          add_base_url.status_code))
