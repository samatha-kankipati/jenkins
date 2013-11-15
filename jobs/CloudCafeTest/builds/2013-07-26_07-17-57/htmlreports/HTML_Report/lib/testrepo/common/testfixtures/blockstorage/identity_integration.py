import random
import string
from unittest2 import skip

from ccengine.common.tools import datagen
from ccengine.common.decorators import attr
from ccengine.providers.identity.v2_0.identity_api import\
    IdentityAPIProvider, IdentityClientTypes
from ccengine.providers.blockstorage.volumes_api import VolumesAPIProvider
from ccengine.providers.blockstorage.lunr_api import LunrAPIProvider
from ccengine.providers.compute.volume_attachments_api import \
    VolumeAttachmentsAPIProvider
from ccengine.providers.compute.compute_api import ComputeAPIProvider

from testrepo.common.testfixtures.fixtures import BaseTestFixture


class TestUser(object):
    '''TODO: Find out if secret answer if ever actually used'''
    def __init__(self):
        self.id = None
        self.client = None
        self.username = None
        self.tenant_id = None
        self.password = None
        self.api_key = None
        self.api_token = None
        self.auth_token = None
        self.service_catalog = None

    def __str__(self):
        s = ''
        s = '{0}\nclient: {1}'.format(s, self.client)
        s = '{0}\nusername: {1}'.format(s, self.username)
        s = '{0}\ntenant_id: {1}'.format(s, self.tenant_id)
        s = '{0}\npassword: {1}'.format(s, self.password)
        s = '{0}\napi_key: {1}'.format(s, self.api_key)
        s = '{0}\napi_token: {1}'.format(s, self.api_token)
        s = '{0}\nauth_token: {1}'.format(s, self.auth_token)
        s = '{0}\nservice_catalog: {1}'.format(s, self.service_catalog)
        return s


class Identity_SUF_IntegrationTestFixture(BaseTestFixture):
    '''Create a new user using Signup Facade
    Defines various methods for adding administering that user with calls to
    identity API.

    Creates a "TestUser" object which contains an identity client for that user
    '''

    @classmethod
    def setUpClass(cls):
        super(Identity_SUF_IntegrationTestFixture, cls).setUpClass()

        #Idenity config section will only need auth endpoint, s/de serializer
        #once create_user works
        cls.identity_provider = IdentityAPIProvider(cls.config)

        #Doesn't actually create a new test user yet.  Right now, it only
        #pulls the user defined in the identity_api section of your config
        #and builds a TestUser object around it.
        cls.main_test_user = cls.create_new_test_user(
            cls.config.identity_api.username,
            cls.config.identity_api.password,
            cls.config.identity_api.api_key)

    @staticmethod
    def gen_random_domain_name():
        #all lower case alpha, 0-9
        #max length of 64 chars
        valid_chars = [s for s in string.ascii_lowercase]
        valid_chars.extend([d for d in string.digits])
        final_word = []
        length = random.randrange(10, 50)

        for x in range(length):
            value = random.sample(valid_chars, 1)
            final_word.append(value[0])
        word = "".join(final_word)
        postfix = random.sample(['us'], 1)[0]
        return "{0}.hurfasaur.{1}".format(word, postfix)

    @staticmethod
    def gen_random_username():
        #all lower case alpha, 0-9
        #3-15 char
        valid_chars = [s for s in string.ascii_lowercase]
        valid_chars.extend([d for d in string.digits])
        name = "".join(random.sample((valid_chars), random.randrange(3, 10)))
        return "raxqe{0}".format(name)

    @staticmethod
    def gen_random_password():
        #all lower case alpha, all upper case alpha, 0-9
        #8-19 characters
        lower_alpha = random.sample(
            [s for s in string.ascii_lowercase], random.randrange(3, 6))
        upper_alpha = random.sample(
            [s for s in string.ascii_uppercase], random.randrange(3, 6))
        numerical = random.sample(
            [d for d in string.digits], random.randrange(3, 6))
        final_list = []
        final_list.extend(lower_alpha)
        final_list.extend(upper_alpha)
        final_list.extend(numerical)
        final_password = "".join(final_list)
        return final_password

    @classmethod
    def add_sub_user_to_user(cls, user_client):
        #Add a sub user
        username = cls.gen_random_username()
        email = '{0}@{1}'.format(username, cls.gen_random_domain_name())
        password = cls.gen_random_password()
        resp = user_client.add_user(
            username, email, enabled=True, password=password)
        assert resp.ok, 'Could not add subuser to user'
        setattr(resp.entity, 'password', password)

        return resp.entity

    @classmethod
    def add_role_to_sub_user(
            cls, user_client, sub_user, role_id):
        resp = user_client.add_role_to_user(sub_user.id, role_id)
        assert resp.ok, 'Unable to add role to sub user'

        #Update stored user service catalog
        sub_user.service_catalog = sub_user.client.\
            authenticate_user_password(
                sub_user.username, sub_user.password).entity

    @classmethod
    def add_role_to_user(cls, main_user, role_id):
        resp = main_user.client.add_role_to_user(main_user.id, role_id)
        assert resp.ok, 'Unable to add role to user'

        #Update stored user service catalog
        main_user.service_catalog = main_user.client.\
            authenticate_user_password(
                main_user.username, main_user.password).entity

    @classmethod
    def get_role(cls, user_client, user_id, role_name):
        resp = user_client.list_roles(user_id)
        assert resp.ok, 'Unable to list roles'
        roles = resp.entity
        for role in roles:
            if role.name == role_name:
                return role

    @classmethod
    def create_new_test_user(cls, username, password, api_key):
        '''TODO:  Change this method so that it integrates with signup facade
                  to actually create new cloud accounts on the fly.'''

        #returns user object
        test_user = TestUser()
        test_user.username = username
        test_user.password = password
        test_user.api_key = api_key

        #Make user client (ServiceAdmin client, so it has access to everything)
        test_user.client = cls.identity_provider.get_client(
            username=test_user.username,
            api_key=test_user.api_key,
            client_type=IdentityClientTypes.SERVICE)

        #Get user service catalog
        test_user.service_catalog = test_user.client.authenticate_user_apikey(
            test_user.username, test_user.api_key).entity

        #Get user token, tenant_id, and user_id
        test_user.token = test_user.service_catalog.token.id
        test_user.tenant_id = test_user.service_catalog.token.tenant.id
        test_user.id = test_user.client.get_user_by_name(
            test_user.username).entity.id

        return test_user

    @classmethod
    def create_new_sub_test_user(cls, user_client):
        sub_user_entity = cls.add_sub_user_to_user(user_client)

        #CREATE SUB TEST USER OBJECT (Creates client and does some auth stuff)
        sub_user = TestUser()
        sub_user.username = sub_user_entity.username
        sub_user.password = sub_user_entity.password

        #Make user client (ServiceAdmin client, so it has access to everything)
        sub_user.client = cls.identity_provider.get_client(
            username=sub_user.username,
            api_key=sub_user.api_key,
            client_type=IdentityClientTypes.SERVICE)

        #Get user service catalog
        sub_user.service_catalog = sub_user.client.\
            authenticate_user_password(
                sub_user.username, sub_user.password).entity

        #Get user token, tenant_id, and user_id
        sub_user.token = sub_user.service_catalog.token.id
        sub_user.tenant_id = sub_user.service_catalog.token.tenant.id
        resp = user_client.get_user_by_name(sub_user.username)
        assert resp.ok, 'Unable to get user by name'
        sub_user.id = resp.entity.id

        return sub_user


class CBS_RBAC_IntegrationTestFixture(Identity_SUF_IntegrationTestFixture):
    '''Sets up everything needed to test all CBS Roles as supported by the
       Roles-Based-Access-Control Feature of Global Auth

       Defines a main_test_user, which will be used exclusively for test
       function setup. (example:  A test that tests deleting an object will use
       main_test_user to create that object, so that the test may execute even
       if object creation is beyond the scope of the role under test)
    '''

    class ExpectedResult(object):
        def __init__(
                self,
                expected_status_code=None,
                expected_status_code_range=None):

            self.expected_status_code = expected_status_code
            self.expected_status_code_range = expected_status_code_range

    GLOBAL_ADMIN = "admin"
    GLOBAL_OBSERVER = "observer"

    IDENTITY_SERVICE_ADMIN = "identity:admin"
    IDENTITY_USER_ADMIN = "identity:user-admin"

    CBS_ADMIN = "cbs:admin"
    CBS_CREATOR = "cbs:creator"
    CBS_OBSERVER = "cbs:observer"

    #this dictionary should be defined by the inheriting test class
    EXPECTED_RESULTS = {
        #admin_api
        "volume_extension:types_manage": None,
        "volume_extension:types_extra_specs": None,
        "volume_extension:quotas:update_for_project": None,
        "volume_extension:volume_admin_actions:reset_status": None,
        "volume_extension:snapshot_admin_actions:reset_status": None,
        "volume_extension:volume_admin_actions:force_delete": None,
        "volume_extension:snapshot_admin_actions:force_delete": None,
        "volume_extension:volume_host_attribute": None,
        "volume_extension:volume_tenant_attribute": None,

        #CBS Admin actions
        "volume_extension:extended_snapshot_attributes": None,
        "volume_extension:quotas:show": None,
        "volume_extension:quotas:update_for_user": None,
        "volume_extension:quota_classes": None,
        "volume:delete": None,
        "volume:update": None,
        "volume:check_detach": None,
        "volume:unreserve_volume": None,
        "volume:begin_detaching": None,
        "volume:roll_detaching": None,
        "volume:detach": None,
        "volume:terminate_connection": None,
        "volume:delete_snapshot": None,
        "volume:update_snapshot": None,
        "volume:delete_volume_metadata": None,
        "volume:update_volume_metadata": None,

        #CBS Creator actions
        "volume:create": None,
        "volume:check_attach": None,
        "volume:reserve_volume": None,
        "volume:attach": None,
        "volume:initialize_connection": None,
        "volume:create_snapshot": None,
        "volume:copy_volume_to_image": None,

        #CBS Observer actions
        "volume:get": None,
        "volume:get_all": None,
        "volume:get_snapshot": None,
        "volume:get_volume": None,
        "volume:get_all_snapshots": None,
        "volume:get_volume_metadata": None,
        "volume:get_volume_image_metadata": None}

    @classmethod
    def setUpClass(cls):
        super(CBS_RBAC_IntegrationTestFixture, cls).setUpClass()
        cls.cbs_roles = {}
        cls.cbs_roles[cls.CBS_OBSERVER] = cls.get_role(
            cls.main_test_user.client, cls.main_test_user.id, cls.CBS_OBSERVER)
        cls.cbs_roles[cls.CBS_ADMIN] = cls.get_role(
            cls.main_test_user.client, cls.main_test_user.id, cls.CBS_ADMIN)
        cls.cbs_roles[cls.CBS_CREATOR] = cls.get_role(
            cls.main_test_user.client, cls.main_test_user.id, cls.CBS_CREATOR)

        #Must be defined by inheriting test class.
        #These are the users and user clients
        #that all test functions will use to run their tests.

        #This must be a TestUser object
        cls.actual_test_user = None

        cls.main_test_user_volumes_provider = None
        cls.actual_test_user_volumes_provider = None

        cls.main_test_user_lunr_provider = None
        cls.actual_test_user_lunr_provider = None

        cls.main_test_user_vol_attach_provider = None
        cls.actual_test_user_vol_attach_provider = None

        cls.main_test_user_compute_provider = None
        cls.actual_test_user_compute_provider = None

    @attr('smoke')
    def test_main_test_user_is_identity_user_admin(self):
        identity_user_admin_role_found = False
        for role in self.main_test_user.service_catalog.user.roles:
            if role.name == self.IDENTITY_USER_ADMIN:
                identity_user_admin_role_found = True
        self.assertTrue(
            identity_user_admin_role_found,
            'Main test use is not an identity user-admin')

    @attr('smoke')
    def test_all_expected_cbs_roles_are_present(self):
        '''Verify that all roles defined by CBS policy.json file are deployed
        in the current environment'''
        for role in self.cbs_roles:
            self.assertIsNotNone(
                role, "{0} role was not found in current environment".format(
                    role))

    def assert_result(self, api_action_name, response):
        expected_result_obj = self.EXPECTED_RESULTS[api_action_name]
        expected_status_code = expected_result_obj.expected_status_code_range

        if expected_status_code is None:
            expected_status_code = expected_result_obj.expected_status_code
            msg = (
                "Test for role {0} failed.  Expected a {1} status code but "
                "API returned a {2}".format(
                    api_action_name, expected_status_code,
                    response.status_code))
            self.assertEquals(response.status_code, expected_status_code, msg)
        else:
            msg = (
                "Test for role {0} failed.  Expected a status code in the "
                "{1}'s range but API returned a {2}".format(
                    api_action_name, expected_status_code,
                    response.status_code))
            self.assertTrue(response.status_code in range(
                expected_status_code, expected_status_code + 100), msg)

    def setup_a_test_volume(self, volumes_provider=None):
        volume_name = datagen.random_string(
            prefix="CBS_RBAC_VOL_TEST", size=8)
        volume_size = self.actual_test_user_volumes_provider.min_volume_size
        volume_type = 'SSD'
        volumes_provider = volumes_provider or \
            self.main_test_user_volumes_provider

        resp = volumes_provider.create_available_volume(
            volume_name, volume_size, volume_type)

        assert resp.ok, 'Unable to create volume during setup'

        volume_id = resp.entity.id

        #Make sure volume gets deleted after test.  Always use the main test
        #user for this to guarantee cleanup
        self.addCleanup(
            self.main_test_user_volumes_provider.delete_volume_confirmed,
            volume_id)

        return resp.entity

    def setup_a_test_snapshot(self, volume_id, volumes_provider=None):
        snapshot_name = datagen.random_string(
            prefix="CBS_RBAC_SNAP_TEST", size=8)

        volumes_provider = volumes_provider or \
            self.main_test_user_volumes_provider

        resp = volumes_provider.create_available_snapshot(
            volume_id, snapshot_display_name=snapshot_name)

        assert resp.ok, 'Unable to create volume snapshot during setup'

        snapshot_id = resp.entity.id

        #Make sure snapshot gets deleted after test
        self.addCleanup(
            self.main_test_user_volumes_provider.delete_snapshot_confirmed,
            snapshot_id)

        return resp.entity

    def setup_a_test_server(self, compute_provider=None):
        server_name = datagen.random_string(
            prefix="CBS_RBAC_SERVER_TEST", size=8)
        compute_provider = compute_provider or \
            self.main_test_user_compute_provider

        self.assertIsNotNone(
            self.config.compute_api.image_ref,
            'Image ref not defined')
        self.assertIsNotNone(
            self.config.compute_api.flavor_ref,
            'Flavor ref not defined')

        resp = compute_provider.create_active_server(
            name=server_name,
            image_ref=self.config.compute_api.image_ref,
            flavor_ref=self.config.compute_api.flavor_ref)

        assert resp.ok, 'Unable to create active server during setup'

        server_id = resp.entity.id

        #Make sure snapshot gets deleted after test
        self.addCleanup(
            self.main_test_user_compute_provider.servers_client.delete_server,
            server_id)

        return resp.entity

# Tests

# admin_api

    @skip('test under construction')
    def test_volume_extension_types_manage(self):
        api_action_name = "volume_extension:types_manage"
        pass

    @skip('test under construction')
    def test_volume_extension_types_extra_specs(self):
        api_action_name = "volume_extension:types_extra_specs"
        pass

    @skip('test under construction')
    def test_volume_extension_quotas_update_for_project(self):
        api_action_name = "volume_extension:quotas:update_for_project"
        pass

    @skip('test under construction')
    def test_volume_extension_volume_admin_actions_reset_status(self):
        api_action_name = \
            "volume_extension:volume_admin_actions:reset_status"
        pass

    @skip('test under construction')
    def test_volume_extension_snapshot_admin_actions_reset_status(self):
        api_action_name = \
            "volume_extension:snapshot_admin_actions:reset_status"
        pass

    @skip('test under construction')
    def test_volume_extension_volume_admin_actions_force_delete(self):
        api_action_name = "volume_extension:volume_admin_actions:force_delete"
        pass

    @skip('test under construction')
    def test_volume_extension_snapshot_admin_actions_force_delete(self):
        api_action_name = \
            "volume_extension:snapshot_admin_actions:force_delete"
        pass

    @skip('test under construction')
    def test_volume_extension_volume_host_attribute(self):
        api_action_name = "volume_extension:volume_host_attribute"
        pass

    @skip('test under construction')
    def test_volume_extension_volume_tenant_attribute(self):
        api_action_name = "volume_extension:volume_tenant_attribute"
        pass

    @skip('test under construction')
    def test_volume_extension_extended_snapshot_attributes(self):
        api_action_name = "volume_extension:extended_snapshot_attributes"
        pass

    @skip('test under construction')
    def test_volume_extension_quotas_show(self):
        api_action_name = "volume_extension:quotas:show"
        pass

    @skip('test under construction')
    def test_volume_extension_quotas_update_for_user(self):
        api_action_name = "volume_extension:quotas:update_for_user"
        pass

    @skip('test under construction')
    def test_volume_extension_quota_classes(self):
        api_action_name = "volume_extension:quota_classes"
        pass

    @attr('cbs')
    def test_volume_delete(self):
        api_action_name = "volume:delete"
        volume = self.setup_a_test_volume()

        resp = (
            self.actual_test_user_volumes_provider.volumes_client.
            delete_volume(volume.id))

        self.assert_result(api_action_name, resp)

    @skip('test under construction')
    def test_volume_update(self):
        api_action_name = "volume:update"
        pass

    @skip('Internal API action, not directly observable from user perspective')
    def test_volume_check_detach(self):
        api_action_name = "volume:check_detach"
        pass

    @skip('Internal API action, not directly observable from user perspective')
    def test_volume_unreserve_volume(self):
        api_action_name = "volume:unreserve_volume"
        pass

    @skip('Internal API action, not directly observable from user perspective')
    def test_volume_begin_detaching(self):
        api_action_name = "volume:begin_detaching"
        pass

    @skip('Internal API action, not directly observable from user perspective')
    def test_volume_roll_detaching(self):
        api_action_name = "volume:roll_detaching"
        pass

    @attr('compute')
    def test_volume_detach(self):
        api_action_name = "volume:detach"
        server = self.setup_a_test_server()
        volume = self.setup_a_test_volume()

        resp = (self.main_test_user_vol_attach_provider.client.attach_volume(
            server.id, volume.id))

        self.assert_result(api_action_name, resp)

        attachment = resp.entity

        resp = self.actual_test_user_vol_attach_provider.client.\
            delete_volume_attachment(attachment.id, server.id)

        self.assert_result(api_action_name, resp)

        #Add additional cleanup using main user in case test user role
        #disallowes detaching
        self.addCleanup(
            self.main_test_user_vol_attach_provider.detach_volume_confirmed,
            attachment.id, server.id)

    @skip('Internal API action, not directly observable from user perspective')
    def test_volume_terminate_connection(self):
        api_action_name = "volume:terminate_connection"
        pass

    @attr('cbs')
    def test_volume_delete_snapshot(self):
        api_action_name = "volume:delete_snapshot"
        volume = self.setup_a_test_volume()
        snapshot = self.setup_a_test_snapshot(volume.id)

        resp = (
            self.actual_test_user_volumes_provider.volumes_client
            .delete_snapshot(snapshot.id))

        self.assert_result(api_action_name, resp)

    @skip('test under construction')
    def test_volume_update_snapshot(self):
        api_action_name = "volume:update_snapshot"
        pass

    @skip('test under construction')
    def test_volume_delete_volume_metadata(self):
        api_action_name = "volume:delete_volume_metadata"
        pass

    @skip('test under construction')
    def test_volume_update_volume_metadata(self):
        api_action_name = "volume:update_volume_metadata"
        pass

    @attr('cbs')
    def test_volume_create(self):
        api_action_name = "volume:create"

        volume_name = datagen.random_string(prefix="RBAC_TESTING", size=8)
        volume_size = self.actual_test_user_volumes_provider.min_volume_size
        volume_type = 'SSD'

        resp = (
            self.actual_test_user_volumes_provider.volumes_client
            .create_volume(volume_name, volume_size, volume_type))

        self.assert_result(api_action_name, resp)

    @skip('Internal API action, not directly observable from user perspective')
    def test_volume_check_attach(self):
        api_action_name = "volume:check_attach"
        pass

    @skip('Internal API action, not directly observable from user perspective')
    def test_volume_reserve_volume(self):
        api_action_name = "volume:reserve_volume"
        pass

    @attr('compute')
    def test_volume_attach(self):
        api_action_name = "volume:attach"
        server = self.setup_a_test_server()
        volume = self.setup_a_test_volume()

        resp = (self.actual_test_user_vol_attach_provider.client.attach_volume(
            server.id, volume.id))

        self.assert_result(api_action_name, resp)

        attachment = resp.entity

        #Add cleanup
        self.addCleanup(
            self.actual_test_user_vol_attach_provider.detach_volume_confirmed,
            attachment.id, server.id)

        #Add additional cleanup using main user in case test user role
        #disallowes detaching
        self.addCleanup(
            self.main_test_user_vol_attach_provider.detach_volume_confirmed,
            attachment.id, server.id)

    @skip('Internal API action, not directly observable from user perspective')
    def test_volume_initialize_connection(self):
        api_action_name = "volume:initialize_connection"
        pass

    @attr('cbs')
    def test_volume_create_snapshot(self):
        api_action_name = "volume:create_snapshot"
        volume = self.setup_a_test_volume()
        snapshot_name = datagen.random_string(prefix="RBAC_SNAP_TEST", size=8)

        resp = (
            self.actual_test_user_volumes_provider.volumes_client
            .create_snapshot(volume.id, display_name=snapshot_name))

        self.assert_result(api_action_name, resp)

    @skip('API Action not yet implemented by CloudBlockStorage')
    def test_volume_copy_volume_to_image(self):
        api_action_name = "volume:copy_volume_to_image"
        pass

    @attr('cbs')
    def test_volume_get(self):
        api_action_name = "volume:get"
        volume = self.setup_a_test_volume()

        resp = (self.actual_test_user_volumes_provider.volumes_client
                .get_volume_info(volume.id))

        self.assert_result(api_action_name, resp)

    @attr('cbs')
    def test_volume_get_all(self):
        api_action_name = "volume:get_all"
        self.setup_a_test_volume()

        resp = (self.actual_test_user_volumes_provider.volumes_client
                .list_all_volumes())

        self.assert_result(api_action_name, resp)

    @attr('cbs')
    def test_volume_get_snapshot(self):
        api_action_name = "volume:get_snapshot"
        volume = self.setup_a_test_volume()
        snapshot = self.setup_a_test_snapshot(volume.id)

        resp = (self.actual_test_user_volumes_provider.volumes_client
                .get_snapshot_info(snapshot.id))

        self.assert_result(api_action_name, resp)

    @skip('test under construction')
    def test_volume_get_volume(self):
        api_action_name = "volume:get_volume"
        pass

    @attr('cbs')
    def test_volume_get_all_snapshots(self):
        api_action_name = "volume:get_all_snapshots"
        resp = (self.actual_test_user_volumes_provider.volumes_client
                .list_all_snapshots())
        self.assert_result(api_action_name, resp)

    @attr('cbs')
    def test_volume_get_volume_metadata(self):
        api_action_name = "volume:get_volume_metadata"

        #Setup (Create volume with metadata)
        volumes_provider = self.main_test_user_volumes_provider
        volume_name = datagen.random_string(prefix="CBS_RBAC_VOL_TEST", size=8)
        volume_size = volumes_provider.min_volume_size
        volume_type = 'SSD'
        expected_metadata = {"VolumeTestMetadata": "ThisIsSomeMetadata"}

        resp = volumes_provider.volumes_client.create_volume(
            volume_name, volume_size, volume_type, metadata=expected_metadata)
        assert resp.ok, 'Unable to create volume during setup'
        volume = resp.entity
        self.addCleanup(
            self.main_test_user_volumes_provider.delete_volume_confirmed,
            volume.id)

        #Test
        resp = (self.actual_test_user_volumes_provider.volumes_client
                .get_volume_info(volume.id))
        self.assert_result(api_action_name, resp)
        metadata = resp.entity.metadata
        assert metadata == expected_metadata, \
            'Retrieved and expected metadata did not match'

    @skip('API action not yet implemented by CloudBlockStorage')
    def test_volume_get_volume_image_metadata(self):
        api_action_name = "volume:get_volume_image_metadata"
    pass


class RBAC_CBS_SubUserTestFixture(CBS_RBAC_IntegrationTestFixture):
    '''Tests all api actions for a sub user with the cbs:observer role'''

    @classmethod
    def setUpClass(cls):
        super(RBAC_CBS_SubUserTestFixture, cls).setUpClass()
        cls.actual_test_user = cls.create_new_sub_test_user(
            cls.main_test_user.client)

        #Setup main user providers
        main_test_user_config_override ={
            "identity": {
                "username": cls.main_test_user.username,
                "password": cls.main_test_user.password}}

        main_test_user_mcp = cls.config.mcp_override(
            main_test_user_config_override)

        cls.main_test_user_volumes_provider = VolumesAPIProvider(
            main_test_user_mcp)

        cls.main_test_user_lunr_provider = LunrAPIProvider(
            main_test_user_mcp.lunr_api)

        cls.main_test_user_vol_attach_provider = VolumeAttachmentsAPIProvider(
            main_test_user_mcp)

        cls.main_test_user_compute_provider = ComputeAPIProvider(
            main_test_user_mcp)

        #Setup sub user providers
        actual_test_user_config_override ={
            "identity": {
                "username": cls.actual_test_user.username,
                "password": cls.actual_test_user.password}}

        actual_test_user_mcp = cls.config.mcp_override(
            actual_test_user_config_override)

        cls.actual_test_user_volumes_provider = VolumesAPIProvider(
            actual_test_user_mcp)

        cls.actual_test_user_lunr_provider = LunrAPIProvider(
            actual_test_user_mcp.lunr_api)

        cls.actual_test_user_vol_attach_provider = VolumeAttachmentsAPIProvider(
            actual_test_user_mcp)

        cls.actual_test_user_compute_provider = ComputeAPIProvider(
            actual_test_user_mcp)

    def assert_actual_test_user_has_role(self, role_name):
        role_found = False
        for role in self.actual_test_user.service_catalog.user.roles:
            if role.name == role_name:
                role_found = True
        self.assertTrue(
            role_found,
            '{0} role was not found in assigned sub user roles'.format(
                role_name))
