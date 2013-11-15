import unittest
from ccengine.common.tools.datagen import rand_name
from ccengine.common.tools.datagen import random_int
from testrepo.common.testfixtures.identity.v1_1.identity \
    import IdentityFixture
from ccengine.common.decorators import attr
import types
from time import strptime, struct_time, mktime
from datetime import datetime, timedelta


class LenghtValidationTest(IdentityFixture):
    @classmethod
    def setUpClass(cls):
        super(LenghtValidationTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        pass

    @attr('regression', type='negative')
    def test_admin_create_user_attr_lenght(self):
        normal_response_codes = [400]   
        key = 'asdasdasd-adsasdads-asdasdasd-adsadsasd'
        mossoId = random_int(1000000, 9000000)
        #nastId = random_int(1000000, 9000000) - present in the api doc
        enabled=True
        create_user_username = self.admin_client.create_user(
            id=multiply_value('lenght', 100),
            key=key,
            enabled=enabled,
            mossoId=mossoId,
            #nastId=nastId - present in the api doc
            )
        create_user_key = self.admin_client.create_user(
            id='name',
            key=multiply_value('key',100),
            enabled=enabled,
            mossoId=mossoId,
            #nastId=nastId - present in the api doc
            )
        create_user_nast = self.admin_client.create_user(
            id='name',
            key=key,
            enabled=enabled,
            mossoId=mossoId,
            nastId=multiply_value('nast',100)
            )

        self.assertIn(create_user_username.status_code, normal_response_codes,
            msg= 'Create user expected {0} received {1}'.format(
                normal_response_codes, 
                create_user_username.status_code))
        self.assertIn(create_user_key.status_code, normal_response_codes,
            msg= 'Create user expected {0} received {1}'.format(
                normal_response_codes, 
                create_user_key.status_code))
        self.assertIn(create_user_nast.status_code, normal_response_codes,
            msg= 'Create user expected {0} received {1}'.format(
                normal_response_codes, 
                create_user_nast.status_code))

    @attr('regression', type='negative')
    def test_admin_update_user_attr_lenght(self):
        normal_response_codes = [201]   
        uid = rand_name('updateUserForLenghtValidation')
        key = '1234657890'
        mossoId = random_int(1000000, 9000000)
        enabled=True

        create_user = self.admin_client.create_user(
            id=uid,
            key=key,
            enabled=enabled,
            mossoId=mossoId,
            )

        update_user_username = self.admin_client.update_user(
                userId=uid, 
                id=multiply_value('updateName',100),
                key=key,
                enabled=enabled,
                mossoId=mossoId)

        update_user_key = self.admin_client.update_user(
                userId=uid, 
                id=uid,
                key=multiply_value('key',100),
                enabled=enabled,
                mossoId=mossoId)

        update_user_nast = self.admin_client.update_user(
                userId=uid, 
                id=uid,
                key=key,
                enabled=enabled,
                mossoId=mossoId,
                nastId=multiply_value('nast',100))


        self.assertIn(create_user.status_code, normal_response_codes,
            msg= 'Create user expected {0}, received {1}'.format(
                normal_response_codes, 
                create_user.status_code))
        self.assertEqual(update_user_username.status_code, 400,
            msg= 'Update user expected 400, received {0}'
                .format(update_user_username.status_code))
        self.assertEqual(update_user_key.status_code, 400,
            msg= 'Update user expected 400, received {0}'
                .format(update_user_key.status_code))
        self.assertEqual(update_user_nast.status_code, 400,
            msg= 'Update user expected 400, received {0}'
                .format(update_user_nast.status_code))

        get_user = self.admin_client_vsec.get_user_by_name(name=uid)
        delete_user = self.admin_client.delete_user(userId=uid)
        self.assertEqual(delete_user.status_code, 204,
            msg='Create user expected response 204, received {0}'
                .format(delete_user.status_code))
        self.addCleanup(self.service_client.delete_user_hard,
                        userId=get_user.entity.id)

    @attr('regression', type='negative')
    def test_admin_add_baseURL(self):
        id = '123'
        userType = 'NAST'
        region = 'ORD'
        serviceName = 'someService'
        publicURL = 'http://publicUrl.com'
        internalURL = 'http://internalUrl.com'
        adminURL = 'http://adminUrl.com'
        default = False
        enabled = True

        add_baseURL_region = self.admin_client.add_base_url(
                id=id, userType=userType, region=multiply_value(region,100),
                serviceName=serviceName, publicURL=publicURL,
                internalURL=internalURL, adminURL=adminURL,
                default=default, enabled=enabled)
        add_baseURL_service = self.admin_client.add_base_url(
                id=id, userType=userType, region=region,
                serviceName=multiply_value(serviceName,100), publicURL=publicURL,
                internalURL=internalURL, adminURL=adminURL,
                default=default, enabled=enabled)
        add_baseURL_public = self.admin_client.add_base_url(
                id=id, userType=userType, region=region,
                serviceName=serviceName, publicURL=multiply_value(publicURL,100),
                internalURL=internalURL, adminURL=adminURL,
                default=default, enabled=enabled)
        add_baseURL_internal = self.admin_client.add_base_url(
                id=id, userType=userType, region=region,
                serviceName=serviceName, publicURL=publicURL, 
                internalURL=multiply_value(internalURL,100), adminURL=adminURL,
                default=default, enabled=enabled)
        add_baseURL_admin = self.admin_client.add_base_url(
                id=id, userType=userType, region=region,
                serviceName=serviceName, publicURL=publicURL,
                internalURL=internalURL, adminURL=multiply_value(adminURL,100),
                default=default, enabled=enabled)

        self.assertEqual(add_baseURL_region.status_code, 400,
                msg= 'Add baseUrl expected 400, received {0}'
                .format(add_baseURL_region.status_code)) 
        self.assertEqual(add_baseURL_service.status_code, 400,
                msg= 'Add baseUrl expected 400, received {0}'
                .format(add_baseURL_service.status_code)) 
        self.assertEqual(add_baseURL_public.status_code, 400,
                msg= 'Add baseUrl expected 400, received {0}'
                .format(add_baseURL_public.status_code)) 
        self.assertEqual(add_baseURL_internal.status_code, 400,
                msg= 'Add baseUrl expected 400, received {0}'
                .format(add_baseURL_internal.status_code)) 
        self.assertEqual(add_baseURL_admin.status_code, 400,
                msg= 'Add baseUrl expected 400, received {0}'
                .format(add_baseURL_admin.status_code))

    
def multiply_value(value, multiple):
    return value * multiple

