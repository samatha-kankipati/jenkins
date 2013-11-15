from ccengine.common.decorators import attr
from ccengine.common.tools.datagen import rand_name, random_int
from testrepo.common.testfixtures.identity.v1_1.identity \
    import IdentityFixture


class UsersTestDomainTenant(IdentityFixture):

    @attr('regression', type='positive')
    def test_admin_create_user(self):
        """
        Docs: nastId should be provided and processed by identity,
        but identity doesn't process it in present behaviour

        """
        normal_response_codes = [201, 203]
        uid = rand_name("ccusername")
        key = 'asdasdasd-adsasdads-asdasdasd-adsadsasd'
        mossoId = random_int(1000000, 9000000)
        #nastId = random_int(1000000, 9000000) - present in the api doc
        enabled = True
        create_user = self.admin_client.create_user(
                id=uid,
                key=key,
                enabled=enabled,
                mossoId=mossoId)
        self.assertIn(
                create_user.status_code,
                normal_response_codes,
                msg='Get base URLs expected {0} received {1}'.
                format(normal_response_codes, create_user.status_code))

        self.assertEquals(
                create_user.entity.mossoId,
                mossoId,
                msg='User mossoId expected {0} but received {1}'.
                format(mossoId, create_user.entity.mossoId))
        get_user = self.admin_client_vsec.get_user_by_name(name=uid)
        self.assertEqual(
                get_user.entity.domainId,
                str(mossoId),
                msg='Created user DomainId {0}, expected {1}'.
                format(get_user.entity.domainId, mossoId))
        delete_user = self.admin_client.delete_user(userId=uid)
        self.assertEqual(
                delete_user.status_code,
                204,
                msg='Create user expected response 204, received {0}'.
                format(delete_user.status_code))
        self.addCleanup(self.service_client.delete_user_hard,
                        userId=get_user.entity.id)

    @attr('regression', type='positive')
    def test_user_in_domain_list(self):
        """
        Docs: nastId should be provided and processed by identity,
        but identity doesn't process it in present behaviour

        """
        normal_response_codes = [201, 203]
        uid = rand_name("ccusername")
        key = 'asdasdasd-adsasdads-asdasdasd-adsadsasd'
        mossoId = random_int(1000000, 9000000)
        enabled = True
        create_user = self.admin_client.create_user(
                id=uid,
                key=key,
                enabled=enabled,
                mossoId=mossoId)
        self.assertIn(
                create_user.status_code,
                normal_response_codes,
                msg='Get base URLs expected {0} received {1}'.
                format(normal_response_codes, create_user.status_code))

        self.assertEquals(
                create_user.entity.mossoId,
                mossoId,
                msg='User mossoId expected {0} but received {1}'.
                format(mossoId, create_user.entity.mossoId))

        get_user = self.admin_client_vsec.get_users_in_domain(domainId=mossoId)
        self.assertEqual(get_user.entity[0].username,
                         uid,
                         msg='Created user not present in the domain')

        delete_user = self.admin_client.delete_user(userId=uid)
        self.assertEqual(
                delete_user.status_code,
                204,
                msg='Create user expected response 204, received {0}'.
                format(delete_user.status_code))
        self.addCleanup(self.service_client.delete_user_hard,
                        userId=get_user.entity[0].id)
