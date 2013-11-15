"""
RBAC Tests
"""
import unittest
from ccengine.common.tools.datagen import rand_name

from ccengine.common.decorators import attr
from testrepo.common.testfixtures.object_storage_fixture \
    import ObjectStorageTestFixture
from ccengine.providers.objectstorage.object_storage_provider \
    import ObjectStorageClientProvider

CONTENT_TYPE_TEXT = 'text/plain; charset=UTF-8'


#TODO once all the auth stuff is fix all the classes could be combined although
# I think keeping them seperate will make you think of better tests
class RBACFilesPermissionsTest(ObjectStorageTestFixture):
    """
    The main account user has full access to Cloud Files. This account user is
    recognized by the "identity:user-admin" role.
    Other subusers on an account have no access to Cloud Files by default.

    To grant a subuser access to a container you have add that user name to the
    X-Container-(Read|Write) header values

    or...

    You can create a role, add that user to the role, and add that role to the
    X-Container-(Read|Write) header values


    You can add the account/tenant name or hash to the X-Container-(Read|Write)
    header values.

    The X-Container-(Read|Write) header values are a CSV single line format.
    In other words, if you have a comma or double quote in your name (user or
    role) you have to quote it according to CSV rules. Double-quotes are
    escaped by having two in a row. For example: user,"user,with,commas",
    "user""with""quotes"

    X-Container-Read lets you GET and HEAD.

    X-Container-Write lets you PUT, POST, COPY, and DELETE.

    One exception is that the role "object-storage:observer" will grant the
    same as if you were in X-Container-Read.
    """

    @classmethod
    def setUpClass(cls):
        """
        This setup class sets the X-Container-Read and write to object vars.
        It then creates a subuser and role and adds the subuser to the role.
        """
        super(RBACFilesPermissionsTest, cls).setUpClass()
        #set header values
        cls.container_read_header = 'X-Container-Read'
        cls.container_write_header = 'X-Container-Write'

        #create subuser
        subuser = rand_name("subuser")
        resp = cls.auth_client.add_user(subuser, 'fakemail@rackspace.com')
        if resp.status_code is not 201:
            raise Exception('Could not create subuser')

        subpassword = resp.json['user']['OS-KSADM:password']
        cls.subuser_id = resp.json['user']['id']

        #get subuser client
        cls.sub_client = ObjectStorageClientProvider.get_client(
            subuser, cls.region, password=subpassword)
        cls.subuser = subuser

        #create role TODO:(nath4854) this can be uncommented when the ability
        #to create a role is given to customers.  Currently only admin auth
        # accouts can add roles
#        cls.auth_role = rand_name("role")
#        resp = cls.auth_client.add_role(cls.auth_role)
#        if resp.status_code is not 201:
#            raise Exception('Could not create role')
#        cls.role_id = resp.json['role']['id']

        #add subuser to role
#        resp = cls.auth_client.add_role_to_user(cls.role_id,cls.subuser_id)
#        if resp.status_code is not 201:
#            raise Exception('Could not add role to subuser')

    @classmethod
    def tearDownClass(cls):
        """
        This tearDownClass deletes the created subuser and role.
        """
        super(RBACFilesPermissionsTest, cls).tearDownClass()
        cls.auth_client.delete_user(cls.subuser_id)
#        cls.auth_client.delete_role(cls.role_id)

    def setUp(self):
        """
        This setUp creates a container and object and gives the subuser full
        access.  This is not the container under test, it is the container that
        subuser will copy from and to.
        """
        #create full access container
        headers = {}
        headers[self.container_read_header] = self.subuser
        headers[self.container_write_header] = self.subuser
        self.container_name = self.client.generate_unique_container_name()
        resp = self.client.create_container(self.container_name,
                                            headers=headers)
        self.addCleanup(self.client.force_delete_containers,
                        [self.container_name])
        if resp.status_code is not 201:
            raise Exception('Create container failed')

        #create an object in previously created container(put)
        self.object_name = self.client.generate_unique_object_name()
        object_data = 'created in setUP by main user'
        content_length = str(len(object_data))
        resp = self.client.set_storage_object(
            self.container_name, self.object_name,
            content_length=content_length, content_type=CONTENT_TYPE_TEXT,
            payload=object_data)
        if resp.status_code is not 201:
            raise Exception('Create object failed')

    def rbac_regression_test(self, client, dic, container_name, object_name):
        """
        This is what I defined as the standard rbac regression test.  It uses
        all the methods and test read and writes on containers and objects.
        It covers most cases but there are a few cases that will have seperate
        tests.
        @type  client: Object(ObjectStorageAPIClient)
        @param client: This is the client for the created subuser

        @type  dic: Dictionary
        @param dic: This is a dic that contains the expected response and msg
            for each test.

        @type  container_name: String
        @param container_name: Contains the container name of the container
            that the subuser has the specific access that is under test(read,
            write, none, revoked read, revoked write)
        """
        #list containers(get)
        resp = client.list_containers()
        self.assertEqual(resp.status_code,
                         dic['list_containers']['code'],
                         dic['list_containers']['msg'])

        #create container(put)
        c_name = client.generate_unique_container_name()
        resp = client.create_container(c_name)
        self.addCleanup(self.client.force_delete_containers, [c_name])
        self.assertEqual(resp.status_code,
                         dic['create_c']['code'],
                         dic['create_c']['msg'])

        #get container metadata(head)
        resp = client.get_container_metadata(container_name)
        self.assertEqual(resp.status_code,
                         dic['get_c_meta']['code'],
                         dic['get_c_meta']['msg'])

        #list objects in a container(get)
        resp = client.list_objects(container_name)
        self.assertEqual(resp.status_code,
                         dic['list_objects']['code'],
                         dic['list_objects']['msg'])

        #create an object(put)
        o_name = client.generate_unique_object_name()
        object_data = 'Test file data'
        content_length = str(len(object_data))
        resp = client.set_storage_object(
            container_name, o_name, content_length=content_length,
            content_type=CONTENT_TYPE_TEXT, payload=object_data)
        self.assertEqual(resp.status_code,
                         dic['create_o']['code'],
                         dic['create_o']['msg'])

        #get object metadata(head)
        resp = client.get_storage_object_metadata(
            container_name, object_name)
        self.assertEqual(resp.status_code,
                         dic['get_o_meta']['code'],
                         dic['get_o_meta']['msg'])

        #update object metadata(post)
        metadata = {'Meta': 'Data'}
        resp = client.set_storage_object_metadata(
            container_name, object_name, metadata)
        self.assertEqual(resp.status_code,
                         dic['set_o_meta']['code'],
                         dic['set_o_meta']['msg'])

        #get object(get)
        resp = client.get_storage_object(container_name, object_name)
        self.assertEqual(resp.status_code,
                         dic['get_object']['code'],
                         dic['get_object']['msg'])

        #copy an object(copy)
        resp = client.copy_storage_object(
            self.container_name, self.object_name,
            dst_container=container_name, dst_object=self.object_name)
        self.assertEqual(resp.status_code,
                         dic['copy']['code'],
                         dic['copy']['msg'])

        #copy an object(put) (from none to none)
        resp = client.putcopy_storage_object(
            container_name, object_name,
            dst_container=self.container_name, dst_object=object_name)
        self.assertEqual(resp.status_code,
                         dic['put_copy']['code'],
                         dic['put_copy']['msg'])

        #delete object(delete)
        resp = client.delete_storage_object(
            container_name, object_name)
        self.assertEqual(resp.status_code,
                         dic['delete_object']['code'],
                         dic['delete_object']['msg'])

    @attr('regression', type='positive')
    def test_subuser_container_full_access(self):
        """
        Scenario:  This test will create a container and an object inside the
                   container then it will get both and then delete them

        Expected Results: Success on all calls
        """
        client = self.client

        #create container with full subuser access
        headers = {}
        headers[self.container_read_header] = self.subuser
        headers[self.container_write_header] = self.subuser
        container_name = client.generate_unique_container_name()
        resp = client.create_container(container_name, headers=headers)
        self.addCleanup(client.force_delete_containers, [container_name])
        self.assertEqual(resp.status_code, 201, 'Create container failed')

        #create an object
        object_name = client.generate_unique_object_name()
        object_data = 'Created in test by main user'
        content_length = str(len(object_data))
        resp = client.set_storage_object(
            container_name, object_name, content_length=content_length,
            content_type=CONTENT_TYPE_TEXT, payload=object_data)
        self.assertEqual(resp.status_code, 201, 'Create object failed')

        dic = {}
        dic['list_containers'] = {'code': 403,
                                  'msg': 'Get containers should fail'}
        dic['create_c'] = {'code': 403,
                           'msg': 'Create container should fail'}
        dic['get_c_meta'] = {'code': 204,
                             'msg': 'Get container metadata should pass'}
        dic['list_objects'] = {'code': 200, 'msg': 'Get obj list should pass'}
        dic['create_o'] = {'code': 201, 'msg': 'Create object should pass'}
        dic['get_o_meta'] = {'code': 200,
                             'msg': 'Get obj metadata should fail'}
        dic['set_o_meta'] = {'code': 202, 'msg': 'Metadata update should pass'}
        dic['get_object'] = {'code': 200, 'msg': 'Get obj should fail'}
        dic['copy'] = {'code': 201, 'msg': 'Copy Object should pass'}
        dic['put_copy'] = {'code': 201, 'msg': 'PutCopy Object should pass'}
        dic['delete_object'] = {'code': 204,
                                'msg': 'Delete object should pass'}

        self.rbac_regression_test(
            self.sub_client, dic, container_name, object_name)

    @attr('regression', type='negative')
    def test_subuser_container_no_access(self):
        """
        Scenario:

        Expected Results: The account user calls should succeed and the subuser
                          Calls should fail due to no permissions
        """
        client = self.client

        #create container with no subuser access
        container_name = client.generate_unique_container_name()
        resp = client.create_container(container_name)
        self.addCleanup(client.force_delete_containers, [container_name])
        self.assertEqual(resp.status_code, 201, 'Create container failed')

        #create an object
        object_name = client.generate_unique_object_name()
        object_data = 'Created in test by main user'
        content_length = str(len(object_data))
        resp = client.set_storage_object(
            container_name, object_name, content_length=content_length,
            content_type=CONTENT_TYPE_TEXT, payload=object_data)
        self.assertEqual(resp.status_code, 201, 'Create object failed')

        dic = {}
        dic['list_containers'] = {'code': 403,
                                  'msg': 'Get containers should fail'}
        dic['create_c'] = {'code': 403, 'msg': 'Create container should fail'}
        dic['get_c_meta'] = {'code': 403,
                             'msg': 'Get container metadata should fail'}
        dic['list_objects'] = {'code': 403,
                               'msg': 'Get object list should fail forbidden'}
        dic['create_o'] = {'code': 403, 'msg': 'Create object should fail'}
        dic['get_o_meta'] = {'code': 403,
                             'msg': 'Get object metadata should fail'}
        dic['set_o_meta'] = {'code': 403, 'msg': 'Metadata update should fail'}
        dic['get_object'] = {'code': 403, 'msg': 'Get obj should fail'}
        dic['copy'] = {'code': 403, 'msg': 'Copy Object should fail'}
        dic['put_copy'] = {'code': 403, 'msg': 'PutCopy Object should fail'}
        dic['delete_object'] = {'code': 403,
                                'msg': 'Delete object should fail'}
        self.rbac_regression_test(
            self.sub_client, dic, container_name, object_name)

    @attr('regression', type='positive')
    def test_subuser_container_read_access(self):
        """
        Scenario:

        Expected Results:
        """
        client = self.client

        #create container with subuser read access
        headers = {}
        headers[self.container_read_header] = self.subuser
        container_name = client.generate_unique_container_name()
        resp = client.create_container(container_name, headers=headers)
        self.addCleanup(client.force_delete_containers, [container_name])
        self.assertEqual(resp.status_code, 201, 'Create container failed')

        #create an object
        object_name = client.generate_unique_object_name()
        object_data = 'Created in test by main user'
        content_length = str(len(object_data))
        resp = client.set_storage_object(
            container_name, object_name, content_length=content_length,
            content_type=CONTENT_TYPE_TEXT, payload=object_data)
        self.assertEqual(resp.status_code, 201, 'Create object failed')

        dic = {}
        dic['list_containers'] = {'code': 403,
                                  'msg': 'Get containers should fail'}
        dic['create_c'] = {'code': 403, 'msg': 'Create container should fail'}
        dic['get_c_meta'] = {'code': 204,
                             'msg': 'Get container metadata should pass'}
        dic['list_objects'] = {'code': 200, 'msg': 'Get obj list should pass'}
        dic['create_o'] = {'code': 403, 'msg': 'Create object should fail'}
        dic['get_o_meta'] = {'code': 200,
                             'msg': 'Get obj metadata should fail'}
        dic['set_o_meta'] = {'code': 403, 'msg': 'Metadata update should fail'}
        dic['get_object'] = {'code': 200, 'msg': 'Get obj should fail'}
        dic['copy'] = {'code': 403, 'msg': 'Copy Object should fail'}
        dic['put_copy'] = {'code': 201, 'msg': 'PutCopy Object should pass'}
        dic['delete_object'] = {'code': 403,
                                'msg': 'Delete object should fail'}
        self.rbac_regression_test(
            self.sub_client, dic, container_name, object_name)

    @attr('regression', type='negative')
    def test_subuser_container_revoked_read_access(self):
        """
        Scenario:

        Expected Results:
        """
        client = self.client
        #create container with subuser read access
        headers = {}
        headers[self.container_read_header] = self.subuser
        container_name = client.generate_unique_container_name()
        resp = client.create_container(container_name, headers=headers)
        self.addCleanup(client.force_delete_containers, [container_name])
        self.assertEqual(resp.status_code, 201, 'Create container failed')

        #create an object
        object_name = client.generate_unique_object_name()
        object_data = 'Created in test by main user'
        content_length = str(len(object_data))
        resp = client.set_storage_object(
            container_name, object_name, content_length=content_length,
            content_type=CONTENT_TYPE_TEXT, payload=object_data)
        self.assertEqual(resp.status_code, 201, 'Create object failed')

        #get object with subclient(get)
        resp = self.sub_client.get_storage_object(container_name, object_name)
        self.assertEqual(resp.status_code, 200, 'Should have access to obj')

        headers = {}
        #revoke subuser permissions
        headers[self.container_write_header] = 'notthesubuser'
        headers[self.container_read_header] = 'notthesubuser'
        resp = self.client.set_container_metadata(
            container_name, metadata=None, headers=headers)
        self.assertEqual(resp.status_code, 204, 'Set headers failed')

        dic = {}
        dic['list_containers'] = {'code': 403,
                                  'msg': 'Get containers should fail'}
        dic['create_c'] = {'code': 403, 'msg': 'Create container should fail'}
        dic['get_c_meta'] = {'code': 403,
                             'msg': 'Get container metadata should fail'}
        dic['list_objects'] = {'code': 403,
                               'msg': 'Get object list should fail'}
        dic['create_o'] = {'code': 403,
                           'msg': 'Create object should fail'}
        dic['get_o_meta'] = {'code': 403,
                             'msg': 'Get object metadata should fail'}
        dic['set_o_meta'] = {'code': 403, 'msg': 'Metadata update should fail'}
        dic['get_object'] = {'code': 403, 'msg': 'Get obj should fail'}
        dic['copy'] = {'code': 403, 'msg': 'Copy Object should fail'}
        dic['put_copy'] = {'code': 403, 'msg': 'PutCopy Object should fail'}
        dic['delete_object'] = {'code': 403,
                                'msg': 'Delete object should fail'}
        self.rbac_regression_test(
            self.sub_client, dic, container_name, object_name)

    @attr('regression', type='positive')
    def test_subuser_container_write_access(self):
        """
        Scenario:

        Expected Results:
        """
        client = self.client
        #create container with subuser write access
        headers = {}
        headers[self.container_write_header] = self.subuser
        container_name = client.generate_unique_container_name()
        resp = client.create_container(container_name, headers=headers)
        self.addCleanup(client.force_delete_containers, [container_name])
        self.assertEqual(resp.status_code, 201, 'Create container failed')

        #create an object
        object_name = client.generate_unique_object_name()
        object_data = 'Created in test by main user'
        content_length = str(len(object_data))
        resp = client.set_storage_object(
            container_name, object_name, content_length=content_length,
            content_type=CONTENT_TYPE_TEXT, payload=object_data)
        self.assertEqual(resp.status_code, 201, 'Create object failed')

        dic = {}
        dic['list_containers'] = {'code': 403,
                                  'msg': 'Get containers should fail'}
        dic['create_c'] = {'code': 403, 'msg': 'Create container should fail'}
        dic['get_c_meta'] = {'code': 403,
                             'msg': 'Get container metadata should fail'}
        dic['list_objects'] = {'code': 403,
                               'msg': 'Get object list should fail'}
        dic['create_o'] = {'code': 201, 'msg': 'Create object should pass'}
        dic['get_o_meta'] = {'code': 403,
                             'msg': 'Get object metadata should fail'}
        dic['set_o_meta'] = {'code': 403, 'msg': 'Metadata update should fail'}
        dic['get_object'] = {'code': 403, 'msg': 'Get obj should fail'}
        dic['copy'] = {'code': 201, 'msg': 'Copy Object should pass'}
        dic['put_copy'] = {'code': 403, 'msg': 'PutCopy Object should fail'}
        dic['delete_object'] = {'code': 204,
                                'msg': 'Delete object should pass'}
        self.rbac_regression_test(
            self.sub_client, dic, container_name, object_name)

    @attr('regression', type='negative')
    def test_subuser_container_revoked_write_access(self):
        """
        Scenario:

        Expected Results:
        """
        client = self.client
        #create container with subuser write access
        headers = {}
        headers[self.container_write_header] = self.subuser
        container_name = client.generate_unique_container_name()
        resp = client.create_container(container_name, headers=headers)
        self.addCleanup(client.force_delete_containers, [container_name])
        self.assertEqual(resp.status_code, 201, 'Create container failed')

        #create an object
        object_name = client.generate_unique_object_name()
        object_data = 'Created in test by main user'
        content_length = str(len(object_data))
        resp = client.set_storage_object(
            container_name, object_name, content_length=content_length,
            content_type=CONTENT_TYPE_TEXT, payload=object_data)
        self.assertEqual(resp.status_code, 201, 'Create object failed')

        #create object with subclient
        o_name = client.generate_unique_object_name()
        object_data = 'Created in test by main user'
        content_length = str(len(object_data))
        resp = self.sub_client.set_storage_object(
            container_name, o_name, content_length=content_length,
            content_type=CONTENT_TYPE_TEXT, payload=object_data)
        self.assertEqual(resp.status_code, 201, 'Create object failed')

        headers = {}
        #revoke subuser permissions
        headers[self.container_write_header] = 'notthesubuser'
        headers[self.container_read_header] = 'notthesubuser'
        resp = self.client.set_container_metadata(
            container_name, metadata=None, headers=headers)
        self.assertEqual(resp.status_code, 204, 'Set headers failed')

        dic = {}
        dic['list_containers'] = {'code': 403,
                                  'msg': 'Get containers should fail'}
        dic['create_c'] = {'code': 403, 'msg': 'Create container should fail'}
        dic['get_c_meta'] = {'code': 403,
                             'msg': 'Get container metadata should fail'}
        dic['list_objects'] = {'code': 403,
                               'msg': 'Get object list should fail forbidden'}
        dic['create_o'] = {'code': 403, 'msg': 'Create object should fail'}
        dic['get_o_meta'] = {'code': 403,
                             'msg': 'Get object metadata should fail'}
        dic['set_o_meta'] = {'code': 403, 'msg': 'Metadata update should fail'}
        dic['get_object'] = {'code': 403, 'msg': 'Get obj should fail'}
        dic['copy'] = {'code': 403, 'msg': 'Copy Object should fail'}
        dic['put_copy'] = {'code': 403, 'msg': 'PutCopy Object should fail'}
        dic['delete_object'] = {'code': 403,
                                'msg': 'Delete object should fail'}
        self.rbac_regression_test(
            self.sub_client, dic, container_name, object_name)

    @unittest.skip('Skipping test.')
    @attr('regression', type='positive')
    def test_subuser_container_role_based_read_access(self):
        """
        Scenario:

        Expected Results:
        """
        client = self.client

        #create container with subuser read access
        headers = {}
        headers[self.container_read_header] = self.auth_role
        container_name = client.generate_unique_container_name()
        resp = client.create_container(container_name, headers=headers)
        self.addCleanup(client.force_delete_containers, [container_name])
        self.assertEqual(resp.status_code, 201, 'Create container failed')

        #create an object
        object_name = client.generate_unique_object_name()
        object_data = 'Created in test by main user'
        content_length = str(len(object_data))
        resp = client.set_storage_object(
            container_name, object_name, content_length=content_length,
            content_type=CONTENT_TYPE_TEXT, payload=object_data)
        self.assertEqual(resp.status_code, 201, 'Create object failed')

        dic = {}
        dic['list_containers'] = {'code': 403,
                                  'msg': 'Get containers should fail'}
        dic['create_c'] = {'code': 403, 'msg': 'Create container should fail'}
        dic['get_c_meta'] = {'code': 204,
                             'msg': 'Get container metadata should pass'}
        dic['list_objects'] = {'code': 200, 'msg': 'Get obj list should pass'}
        dic['create_o'] = {'code': 403, 'msg': 'Create object should fail'}
        dic['get_o_meta'] = {'code': 200,
                             'msg': 'Get obj metadata should fail'}
        dic['set_o_meta'] = {'code': 403, 'msg': 'Metadata update should fail'}
        dic['get_object'] = {'code': 200, 'msg': 'Get obj should fail'}
        dic['copy'] = {'code': 403, 'msg': 'Copy Object should fail'}
        dic['put_copy'] = {'code': 201, 'msg': 'PutCopy Object should pass'}
        dic['delete_object'] = {'code': 403,
                                'msg': 'Delete object should fail'}
        self.rbac_regression_test(
            self.sub_client, dic, container_name, object_name)

    @unittest.skip('Skipping test.')
    @attr('regression', type='negative')
    def test_subuser_container_revoked_role_based_read_access(self):
        """
        Scenario:

        Expected Results:
        """
        client = self.client
        #create container with subuser read access
        headers = {}
        headers[self.container_read_header] = self.auth_role
        container_name = client.generate_unique_container_name()
        resp = client.create_container(container_name, headers=headers)
        self.addCleanup(client.force_delete_containers, [container_name])
        self.assertEqual(resp.status_code, 201, 'Create container failed')

        #create an object
        object_name = client.generate_unique_object_name()
        object_data = 'Created in test by main user'
        content_length = str(len(object_data))
        resp = client.set_storage_object(
            container_name, object_name, content_length=content_length,
            content_type=CONTENT_TYPE_TEXT, payload=object_data)
        self.assertEqual(resp.status_code, 201, 'Create object failed')

        #get object with subclient(get)
        resp = self.sub_client.get_storage_object(container_name, object_name)
        self.assertEqual(resp.status_code, 200, 'Should have access to obj')

        headers = {}
        #revoke subuser permissions
        headers[self.container_write_header] = 'notthesubuser'
        headers[self.container_read_header] = 'notthesubuser'
        resp = self.client.set_container_metadata(
            container_name, metadata=None, headers=headers)
        self.assertEqual(resp.status_code, 204, 'Set headers failed')

        dic = {}
        dic['list_containers'] = {'code': 403,
                                  'msg': 'Get containers should fail'}
        dic['create_c'] = {'code': 403, 'msg': 'Create container should fail'}
        dic['get_c_meta'] = {'code': 403,
                             'msg': 'Get container metadata should fail'}
        dic['list_objects'] = {'code': 403,
                               'msg': 'Get object list should fail'}
        dic['create_o'] = {'code': 403,
                           'msg': 'Create object should fail'}
        dic['get_o_meta'] = {'code': 403,
                             'msg': 'Get object metadata should fail'}
        dic['set_o_meta'] = {'code': 403, 'msg': 'Metadata update should fail'}
        dic['get_object'] = {'code': 403, 'msg': 'Get obj should fail'}
        dic['copy'] = {'code': 403, 'msg': 'Copy Object should fail'}
        dic['put_copy'] = {'code': 403, 'msg': 'PutCopy Object should fail'}
        dic['delete_object'] = {'code': 403,
                                'msg': 'Delete object should fail'}
        self.rbac_regression_test(
            self.sub_client, dic, container_name, object_name)

    @unittest.skip('Skipping test.')
    @attr('regression', type='positive')
    def test_subuser_container_role_based_write_access(self):
        """
        Scenario:

        Expected Results:
        """
        client = self.client
        #create container with subuser write access
        headers = {}
        headers[self.container_write_header] = self.auth_role
        container_name = client.generate_unique_container_name()
        resp = client.create_container(container_name, headers=headers)
        self.addCleanup(client.force_delete_containers, [container_name])
        self.assertEqual(resp.status_code, 201, 'Create container failed')

        #create an object
        object_name = client.generate_unique_object_name()
        object_data = 'Created in test by main user'
        content_length = str(len(object_data))
        resp = client.set_storage_object(
            container_name, object_name, content_length=content_length,
            content_type=CONTENT_TYPE_TEXT, payload=object_data)
        self.assertEqual(resp.status_code, 201, 'Create object failed')

        dic = {}
        dic['list_containers'] = {'code': 403,
                                  'msg': 'Get containers should fail'}
        dic['create_c'] = {'code': 403, 'msg': 'Create container should fail'}
        dic['get_c_meta'] = {'code': 403,
                             'msg': 'Get container metadata should fail'}
        dic['list_objects'] = {'code': 403,
                               'msg': 'Get object list should fail'}
        dic['create_o'] = {'code': 201, 'msg': 'Create object should pass'}
        dic['get_o_meta'] = {'code': 403,
                             'msg': 'Get object metadata should fail'}
        dic['set_o_meta'] = {'code': 403, 'msg': 'Metadata update should fail'}
        dic['get_object'] = {'code': 403, 'msg': 'Get obj should fail'}
        dic['copy'] = {'code': 201, 'msg': 'Copy Object should pass'}
        dic['put_copy'] = {'code': 403, 'msg': 'PutCopy Object should fail'}
        dic['delete_object'] = {'code': 204,
                                'msg': 'Delete object should pass'}
        self.rbac_regression_test(
            self.sub_client, dic, container_name, object_name)

    @unittest.skip('Skipping test.')
    @attr('regression', type='negative')
    def test_subuser_container_revoked_role_based_write_access(self):
        """
        Scenario:

        Expected Results:
        """
        client = self.client
        #create container with subuser write access
        headers = {}
        headers[self.container_write_header] = self.auth_role
        container_name = client.generate_unique_container_name()
        resp = client.create_container(container_name, headers=headers)
        self.addCleanup(client.force_delete_containers, [container_name])
        self.assertEqual(resp.status_code, 201, 'Create container failed')

        #create an object
        object_name = client.generate_unique_object_name()
        object_data = 'Created in test by main user'
        content_length = str(len(object_data))
        resp = client.set_storage_object(
            container_name, object_name, content_length=content_length,
            content_type=CONTENT_TYPE_TEXT, payload=object_data)
        self.assertEqual(resp.status_code, 201, 'Create object failed')

        #create object with subclient
        o_name = client.generate_unique_object_name()
        object_data = 'Created in test by main user'
        content_length = str(len(object_data))
        resp = self.sub_client.set_storage_object(
            container_name, o_name, content_length=content_length,
            content_type=CONTENT_TYPE_TEXT, payload=object_data)
        self.assertEqual(resp.status_code, 201, 'Create object failed')

        headers = {}
        #revoke subuser permissions
        headers[self.container_write_header] = 'notthesubuser'
        headers[self.container_read_header] = 'notthesubuser'
        resp = self.client.set_container_metadata(
            container_name, metadata=None, headers=headers)
        self.assertEqual(resp.status_code, 204, 'Set headers failed')

        dic = {}
        dic['list_containers'] = {'code': 403,
                                  'msg': 'Get containers should fail'}
        dic['create_c'] = {'code': 403, 'msg': 'Create container should fail'}
        dic['get_c_meta'] = {'code': 403,
                             'msg': 'Get container metadata should fail'}
        dic['list_objects'] = {'code': 403,
                               'msg': 'Get object list should fail forbidden'}
        dic['create_o'] = {'code': 403, 'msg': 'Create object should fail'}
        dic['get_o_meta'] = {'code': 403,
                             'msg': 'Get object metadata should fail'}
        dic['set_o_meta'] = {'code': 403, 'msg': 'Metadata update should fail'}
        dic['get_object'] = {'code': 403, 'msg': 'Get obj should fail'}
        dic['copy'] = {'code': 403, 'msg': 'Copy Object should fail'}
        dic['put_copy'] = {'code': 403, 'msg': 'PutCopy Object should fail'}
        dic['delete_object'] = {'code': 403,
                                'msg': 'Delete object should fail'}
        self.rbac_regression_test(
            self.sub_client, dic, container_name, object_name)


class RBACGlobalPermissionsTest(ObjectStorageTestFixture):
    """
    The main account user has full access to Cloud Files. This account user is
    recognized by the "identity:user-admin" role.
    Other subusers on an account have no access to Cloud Files by default.

    To grant a subuser access to a container you have add that user name to the
    X-Container-(Read|Write) header values

    or...

    You can create a role, add that user to the role, and add that role to the
    X-Container-(Read|Write) header values


    You can add the account/tenant name or hash to the X-Container-(Read|Write)
    header values.

    The X-Container-(Read|Write) header values are a CSV single line format.
    In other words, if you have a comma or double quote in your name (user or
    role) you have to quote it according to CSV rules. Double-quotes are
    escaped by having two in a row. For example: user,"user,with,commas",
    "user""with""quotes"

    X-Container-Read lets you GET and HEAD.

    X-Container-Write lets you PUT, POST, COPY, and DELETE.

    One exception is that the role "object-storage:observer" will grant the
    same as if you were in X-Container-Read.
    """
    @classmethod
    def setUpClass(cls):
        """
        This setup class sets the X-Container-Read and write to object vars.
        """
        super(RBACGlobalPermissionsTest, cls).setUpClass()
        #set header values
        cls.container_read_header = 'X-Container-Read'
        cls.container_write_header = 'X-Container-Write'

    @classmethod
    def tearDownClass(cls):
        super(RBACGlobalPermissionsTest, cls).tearDownClass()

    def setUp(self):
        """
        This setup class creates a subuser and adds the subuser to the role.
        It also creates a container and give the subuser read and write access
        to it via the subusers username.  This is not the container under test
        it is the container that subuser will copy from and to.
        """
        #create subuser
        subuser = rand_name("subuser")
        resp = self.auth_client.add_user(subuser, 'fakemail@rackspace.com')
        if resp.status_code is not 201:
            raise Exception('Could not create subuser')

        subpassword = resp.json['user']['OS-KSADM:password']
        self.subuser_id = resp.json['user']['id']

        #get subuser client
        self.sub_client = ObjectStorageClientProvider.get_client(
            subuser, self.region, password=subpassword)
        self.subuser = subuser

        #create role
        self.auth_role = rand_name("role")
        resp = self.auth_client.add_role(self.auth_role)
        if resp.status_code is not 201:
            raise Exception('Could not create role')
        self.role_id = resp.json['role']['id']

        #add subuser to role
        resp = self.auth_client.add_role_to_user(self.role_id, self.subuser_id)
        if resp.status_code is not 201:
            raise Exception('Could not add role to subuser')

        #create full access container
        headers = {}
        headers[self.container_read_header] = self.subuser
        headers[self.container_write_header] = self.subuser
        self.container_name = self.client.generate_unique_container_name()
        resp = self.client.create_container(self.container_name,
                                            headers=headers)
        self.addCleanup(self.client.force_delete_containers,
                        [self.container_name])
        if resp.status_code is not 201:
            raise Exception('Create container failed')

        #create an object in previously created container(put)
        self.object_name = self.client.generate_unique_object_name()
        object_data = 'created in setUP by main user'
        content_length = str(len(object_data))
        resp = self.client.set_storage_object(
            self.container_name, self.object_name,
            content_length=content_length, content_type=CONTENT_TYPE_TEXT,
            payload=object_data)
        if resp.status_code is not 201:
            raise Exception('Create object failed')

    def tearDown(self):
        """
        This tearDown deletes the created subuser and role.  The container is
        taken care of with the addCleanup function because the possible copied
        containers are name local in the method and we dont want a failed
        container delete here.
        """
        self.auth_client.delete_user(self.subuser_id)
        self.auth_client.delete_role(self.role_id)

    def rbac_regression_test(self, client, dic, container_name, object_name):
        """
        This is what I defined as the standard rbac regression test.  It uses
        all the methods and test read and writes on containers and objects.
        It covers most cases but there are a few cases that will have seperate
        tests.
        @type  client: Object(ObjectStorageAPIClient)
        @param client: This is the client for the created subuser

        @type  dic: Dictionary
        @param dic: This is a dic that contains the expected response and msg
            for each test.

        @type  container_name: String
        @param container_name: Contains the container name of the container
            that the subuser has the specific access that is under test(read,
            write, none, revoked read, revoked write)
        """
        #list containers(get)
        resp = client.list_containers()
        self.assertEqual(resp.status_code,
                         dic['list_containers']['code'],
                         dic['list_containers']['msg'])

        #create container(put)
        c_name = client.generate_unique_container_name()
        resp = client.create_container(c_name)
        self.addCleanup(self.client.force_delete_containers, [c_name])
        self.assertEqual(resp.status_code,
                         dic['create_c']['code'],
                         dic['create_c']['msg'])

        #get container metadata(head)
        resp = client.get_container_metadata(container_name)
        self.assertEqual(resp.status_code,
                         dic['get_c_meta']['code'],
                         dic['get_c_meta']['msg'])

        #list objects in a container(get)
        resp = client.list_objects(container_name)
        self.assertEqual(resp.status_code,
                         dic['list_objects']['code'],
                         dic['list_objects']['msg'])

        #create an object(put)
        o_name = client.generate_unique_object_name()
        object_data = 'Test file data'
        content_length = str(len(object_data))
        resp = client.set_storage_object(
            container_name, o_name, content_length=content_length,
            content_type=CONTENT_TYPE_TEXT, payload=object_data)
        self.assertEqual(resp.status_code,
                         dic['create_o']['code'],
                         dic['create_o']['msg'])

        #get object metadata(head)
        resp = client.get_storage_object_metadata(
            container_name, object_name)
        self.assertEqual(resp.status_code,
                         dic['get_o_meta']['code'],
                         dic['get_o_meta']['msg'])

        #update object metadata(post)
        metadata = {'Meta': 'Data'}
        resp = client.set_storage_object_metadata(
            container_name, object_name, metadata)
        self.assertEqual(resp.status_code,
                         dic['set_o_meta']['code'],
                         dic['set_o_meta']['msg'])

        #get object(get)
        resp = client.get_storage_object(container_name, object_name)
        self.assertEqual(resp.status_code,
                         dic['get_object']['code'],
                         dic['get_object']['msg'])

        #copy an object(copy)
        resp = client.copy_storage_object(
            self.container_name, self.object_name,
            dst_container=container_name, dst_object=self.object_name)
        self.assertEqual(resp.status_code,
                         dic['copy']['code'],
                         dic['copy']['msg'])

        #copy an object(put) (from none to none)
        resp = client.putcopy_storage_object(
            container_name, object_name,
            dst_container=self.container_name, dst_object=object_name)
        self.assertEqual(resp.status_code,
                         dic['put_copy']['code'],
                         dic['put_copy']['msg'])

        #delete object(delete)
        resp = client.delete_storage_object(
            container_name, object_name)
        self.assertEqual(resp.status_code,
                         dic['delete_object']['code'],
                         dic['delete_object']['msg'])

    @unittest.skip('Skipping test.')
    @attr('regression', type='negative')
    def test_subuser_auth_revoked_role_based_read_access(self):
        """
        Scenario:

        Expected Results:
        """
        client = self.client
        #create container with subuser read access
        headers = {}
        headers[self.container_read_header] = self.auth_role
        container_name = client.generate_unique_container_name()
        resp = client.create_container(container_name, headers=headers)
        self.addCleanup(client.force_delete_containers, [container_name])
        self.assertEqual(resp.status_code, 201, 'Create container failed')

        #create an object
        object_name = client.generate_unique_object_name()
        object_data = 'Created in test by main user'
        content_length = str(len(object_data))
        resp = client.set_storage_object(
            container_name, object_name, content_length=content_length,
            content_type=CONTENT_TYPE_TEXT, payload=object_data)
        self.assertEqual(resp.status_code, 201, 'Create object failed')

        #get object with subclient(get)
        resp = self.sub_client.get_storage_object(container_name, object_name)
        self.assertEqual(resp.status_code, 200, 'Should have access to obj')

        # TODO:(nath4854) need to remove user from role here
        # self.auth_client.delete_role_from_user(self.role_id)

        dic = {}
        dic['list_containers'] = {'code': 403,
                                  'msg': 'Get containers should fail'}
        dic['create_c'] = {'code': 403, 'msg': 'Create container should fail'}
        dic['get_c_meta'] = {'code': 403,
                             'msg': 'Get container metadata should fail'}
        dic['list_objects'] = {'code': 403,
                               'msg': 'Get object list should fail'}
        dic['create_o'] = {'code': 403,
                           'msg': 'Create object should fail'}
        dic['get_o_meta'] = {'code': 403,
                             'msg': 'Get object metadata should fail'}
        dic['set_o_meta'] = {'code': 403, 'msg': 'Metadata update should fail'}
        dic['get_object'] = {'code': 403, 'msg': 'Get obj should fail'}
        dic['copy'] = {'code': 403, 'msg': 'Copy Object should fail'}
        dic['put_copy'] = {'code': 403, 'msg': 'PutCopy Object should fail'}
        dic['delete_object'] = {'code': 403,
                                'msg': 'Delete object should fail'}
        self.rbac_regression_test(
            self.sub_client, dic, container_name, object_name)

    @unittest.skip('Skipping test.')
    @attr('regression', type='negative')
    def test_subuser_auth_revoked_role_based_write_access(self):
        """
        Scenario:

        Expected Results:
        """
        client = self.client
        #create container with subuser write access
        headers = {}
        headers[self.container_write_header] = self.auth_role
        container_name = client.generate_unique_container_name()
        resp = client.create_container(container_name, headers=headers)
        self.addCleanup(client.force_delete_containers, [container_name])
        self.assertEqual(resp.status_code, 201, 'Create container failed')

        #create an object
        object_name = client.generate_unique_object_name()
        object_data = 'Created in test by main user'
        content_length = str(len(object_data))
        resp = client.set_storage_object(
            container_name, object_name, content_length=content_length,
            content_type=CONTENT_TYPE_TEXT, payload=object_data)
        self.assertEqual(resp.status_code, 201, 'Create object failed')

        #create object with subclient
        o_name = client.generate_unique_object_name()
        object_data = 'Created in test by main user'
        content_length = str(len(object_data))
        resp = self.sub_client.set_storage_object(
            container_name, o_name, content_length=content_length,
            content_type=CONTENT_TYPE_TEXT, payload=object_data)
        self.assertEqual(resp.status_code, 201, 'Create object failed')

        # TODO:(nath4854) need to remove user from role here
        # self.auth_client.delete_role_from_user(self.role_id)

        dic = {}
        dic['list_containers'] = {'code': 403,
                                  'msg': 'Get containers should fail'}
        dic['create_c'] = {'code': 403, 'msg': 'Create container should fail'}
        dic['get_c_meta'] = {'code': 403,
                             'msg': 'Get container metadata should fail'}
        dic['list_objects'] = {'code': 403,
                               'msg': 'Get object list should fail forbidden'}
        dic['create_o'] = {'code': 403, 'msg': 'Create object should fail'}
        dic['get_o_meta'] = {'code': 403,
                             'msg': 'Get object metadata should fail'}
        dic['set_o_meta'] = {'code': 403, 'msg': 'Metadata update should fail'}
        dic['get_object'] = {'code': 403, 'msg': 'Get obj should fail'}
        dic['copy'] = {'code': 403, 'msg': 'Copy Object should fail'}
        dic['put_copy'] = {'code': 403, 'msg': 'PutCopy Object should fail'}
        dic['delete_object'] = {'code': 403,
                                'msg': 'Delete object should fail'}
        self.rbac_regression_test(
            self.sub_client, dic, container_name, object_name)

    @unittest.skip('Skipping test.')
    @attr('regression', type='positive')
    def test_subuser_container_observer_role(self):
        """
        Scenario:

        Expected Results:
        """
        #create role
        observer_role = "object-storage:observer"
        resp = self.auth_client.add_role(observer_role)
        if resp.status_code is not 201:
            raise Exception('Could not create role')
        observer_id = resp.json['role']['id']

        #add subuser to role
        resp = self.auth_client.add_role_to_user(self.role_id, self.subuser_id)
        if resp.status_code is not 201:
            raise Exception('Could not add role to subuser')

        client = self.client

        #create container with subuser read access
        headers = {}
        headers[self.container_read_header] = observer_role
        container_name = client.generate_unique_container_name()
        resp = client.create_container(container_name, headers=headers)
        self.addCleanup(client.force_delete_containers, [container_name])
        self.assertEqual(resp.status_code, 201, 'Create container failed')

        #create an object
        object_name = client.generate_unique_object_name()
        object_data = 'Created in test by main user'
        content_length = str(len(object_data))
        resp = client.set_storage_object(
            container_name, object_name, content_length=content_length,
            content_type=CONTENT_TYPE_TEXT, payload=object_data)
        self.assertEqual(resp.status_code, 201, 'Create object failed')

        dic = {}
        dic['list_containers'] = {'code': 403,
                                  'msg': 'Get containers should fail'}
        dic['create_c'] = {'code': 403, 'msg': 'Create container should fail'}
        dic['get_c_meta'] = {'code': 204,
                             'msg': 'Get container metadata should pass'}
        dic['list_objects'] = {'code': 200, 'msg': 'Get obj list should pass'}
        dic['create_o'] = {'code': 403, 'msg': 'Create object should fail'}
        dic['get_o_meta'] = {'code': 200,
                             'msg': 'Get obj metadata should fail'}
        dic['set_o_meta'] = {'code': 403, 'msg': 'Metadata update should fail'}
        dic['get_object'] = {'code': 200, 'msg': 'Get obj should fail'}
        dic['copy'] = {'code': 403, 'msg': 'Copy Object should fail'}
        dic['put_copy'] = {'code': 201, 'msg': 'PutCopy Object should pass'}
        dic['delete_object'] = {'code': 403,
                                'msg': 'Delete object should fail'}
        self.rbac_regression_test(
            self.sub_client, dic, container_name, object_name)

    @unittest.skip('Skipping test.')
    @attr('regression', type='negative')
    def test_subuser_container_revoked_observer_role(self):
        """
        Scenario:

        Expected Results:
        """
        #create role
        observer_role = "object-storage:observer"
        resp = self.auth_client.add_role(observer_role)
        if resp.status_code is not 201:
            raise Exception('Could not create role')
        observer_id = resp.json['role']['id']

        #add subuser to role
        resp = self.auth_client.add_role_to_user(self.role_id, self.subuser_id)
        if resp.status_code is not 201:
            raise Exception('Could not add role to subuser')

        client = self.client
        #create container with subuser read access
        headers = {}
        headers[self.container_read_header] = self.auth_role
        container_name = client.generate_unique_container_name()
        resp = client.create_container(container_name, headers=headers)
        self.addCleanup(client.force_delete_containers, [container_name])
        self.assertEqual(resp.status_code, 201, 'Create container failed')

        #create an object
        object_name = client.generate_unique_object_name()
        object_data = 'Created in test by main user'
        content_length = str(len(object_data))
        resp = client.set_storage_object(
            container_name, object_name, content_length=content_length,
            content_type=CONTENT_TYPE_TEXT, payload=object_data)
        self.assertEqual(resp.status_code, 201, 'Create object failed')

        #get object with subclient(get)
        resp = self.sub_client.get_storage_object(container_name, object_name)
        self.assertEqual(resp.status_code, 200, 'Should have access to obj')

        # TODO:(nath4854) need to remove user from observer role here
        # self.auth_client.delete_role_from_user(self.role_id)

        dic = {}
        dic['list_containers'] = {'code': 403,
                                  'msg': 'Get containers should fail'}
        dic['create_c'] = {'code': 403, 'msg': 'Create container should fail'}
        dic['get_c_meta'] = {'code': 403,
                             'msg': 'Get container metadata should fail'}
        dic['list_objects'] = {'code': 403,
                               'msg': 'Get object list should fail'}
        dic['create_o'] = {'code': 403,
                           'msg': 'Create object should fail'}
        dic['get_o_meta'] = {'code': 403,
                             'msg': 'Get object metadata should fail'}
        dic['set_o_meta'] = {'code': 403, 'msg': 'Metadata update should fail'}
        dic['get_object'] = {'code': 403, 'msg': 'Get obj should fail'}
        dic['copy'] = {'code': 403, 'msg': 'Copy Object should fail'}
        dic['put_copy'] = {'code': 403, 'msg': 'PutCopy Object should fail'}
        dic['delete_object'] = {'code': 403,
                                'msg': 'Delete object should fail'}
        self.rbac_regression_test(
            self.sub_client, dic, container_name, object_name)


class RBACForeignAccountPermissionsTest(ObjectStorageTestFixture):
    """
    The main account user has full access to Cloud Files. This account user is
    recognized by the "identity:user-admin" role.
    Other subusers on an account have no access to Cloud Files by default.

    To grant a subuser access to a container you have add that user name to the
    X-Container-(Read|Write) header values

    or...

    You can create a role, add that user to the role, and add that role to the
    X-Container-(Read|Write) header values


    You can add the account/tenant name or hash to the X-Container-(Read|Write)
    header values.

    The X-Container-(Read|Write) header values are a CSV single line format.
    In other words, if you have a comma or double quote in your name (user or
    role) you have to quote it according to CSV rules. Double-quotes are
    escaped by having two in a row. For example: user,"user,with,commas",
    "user""with""quotes"

    X-Container-Read lets you GET and HEAD.

    X-Container-Write lets you PUT, POST, COPY, and DELETE.

    One exception is that the role "object-storage:observer" will grant the
    same as if you were in X-Container-Read.
    """
    @classmethod
    def setUpClass(cls):
        """
        This setup class sets the X-Container-Read and write to object vars.
        It then creates a subuser and role and adds the subuser to the role.
        """
        super(RBACForeignAccountPermissionsTest, cls).setUpClass()
        #set header values
        cls.container_read_header = 'X-Container-Read'
        cls.container_write_header = 'X-Container-Write'
        cls.foreign_name = cls.config.identity_api.alt_username
        cls.alt_client.storage_url = cls.client.storage_url

    def setUp(self):
        """
        This setUp creates a container and object and gives the subuser full
        access.  This is not the container under test, it is the container that
        subuser will copy from and to.
        """

        #create full access container
        headers = {}
        headers[self.container_read_header] = self.foreign_name
        headers[self.container_write_header] = self.foreign_name
        self.container_name = self.client.generate_unique_container_name()
        resp = self.client.create_container(self.container_name,
                                            headers=headers)
        self.addCleanup(self.client.force_delete_containers,
                        [self.container_name])
        if resp.status_code is not 201:
            raise Exception('Create container failed')

        #create an object in previously created container(put)
        self.object_name = self.client.generate_unique_object_name()
        object_data = 'created in setUP by main user'
        content_length = str(len(object_data))
        resp = self.client.set_storage_object(
            self.container_name, self.object_name,
            content_length=content_length, content_type=CONTENT_TYPE_TEXT,
            payload=object_data)
        if resp.status_code is not 201:
            raise Exception('Create object failed')

    def rbac_regression_test(self, client, dic, container_name, object_name):
        """
        This is what I defined as the standard rbac regression test.  It uses
        all the methods and test read and writes on containers and objects.
        It covers most cases but there are a few cases that will have seperate
        tests.
        @type  client: Object(ObjectStorageAPIClient)
        @param client: This is the client for the created subuser

        @type  dic: Dictionary
        @param dic: This is a dic that contains the expected response and msg
            for each test.

        @type  container_name: String
        @param container_name: Contains the container name of the container
            that the subuser has the specific access that is under test(read,
            write, none, revoked read, revoked write)
        """
        #list containers(get)
        resp = client.list_containers()
        self.assertEqual(resp.status_code,
                         dic['list_containers']['code'],
                         dic['list_containers']['msg'])

        #create container(put)
        c_name = client.generate_unique_container_name()
        resp = client.create_container(c_name)
        self.addCleanup(self.client.force_delete_containers, [c_name])
        self.assertEqual(resp.status_code,
                         dic['create_c']['code'],
                         dic['create_c']['msg'])

        #get container metadata(head)
        resp = client.get_container_metadata(container_name)
        self.assertEqual(resp.status_code,
                         dic['get_c_meta']['code'],
                         dic['get_c_meta']['msg'])

        #list objects in a container(get)
        resp = client.list_objects(container_name)
        self.assertEqual(resp.status_code,
                         dic['list_objects']['code'],
                         dic['list_objects']['msg'])

        #create an object(put)
        o_name = client.generate_unique_object_name()
        object_data = 'Test file data'
        content_length = str(len(object_data))
        resp = client.set_storage_object(
            container_name, o_name, content_length=content_length,
            content_type=CONTENT_TYPE_TEXT, payload=object_data)
        self.assertEqual(resp.status_code,
                         dic['create_o']['code'],
                         dic['create_o']['msg'])

        #get object metadata(head)
        resp = client.get_storage_object_metadata(
            container_name, object_name)
        self.assertEqual(resp.status_code,
                         dic['get_o_meta']['code'],
                         dic['get_o_meta']['msg'])

        #update object metadata(post)
        metadata = {'Meta': 'Data'}
        resp = client.set_storage_object_metadata(
            container_name, object_name, metadata)
        self.assertEqual(resp.status_code,
                         dic['set_o_meta']['code'],
                         dic['set_o_meta']['msg'])

        #get object(get)
        resp = client.get_storage_object(container_name, object_name)
        self.assertEqual(resp.status_code,
                         dic['get_object']['code'],
                         dic['get_object']['msg'])

# TODO: write copy tests for cross account copy
#        #copy an object(copy)
#        resp = client.copy_storage_object(
#            self.container_name, self.object_name,
#            dst_container=container_name, dst_object=self.object_name)
#        self.assertEqual(resp.status_code,
#                         dic['copy']['code'],
#                         dic['copy']['msg'])
#
#        #copy an object(put) (from none to none)
#        resp = client.putcopy_storage_object(
#            container_name, object_name,
#            dst_container=self.container_name, dst_object=object_name)
#        self.assertEqual(resp.status_code,
#                         dic['put_copy']['code'],
#                         dic['put_copy']['msg'])

        #delete object(delete)
        resp = client.delete_storage_object(
            container_name, object_name)
        self.assertEqual(resp.status_code,
                         dic['delete_object']['code'],
                         dic['delete_object']['msg'])

    @attr('regression', type='negative')
    def test_foreign_account_container_no_access(self):
        """
        Scenario:  Creates a container  and object with the account user.
                   Gets a foreign user client.  Tries to access
                   account create container, create object, read preexisting
                   objects, delete preexisting object and container.

        Expected Results:  The account user calls should succeed and the
                           subuser calls should fail due to no permissions
        """
        client = self.client
        #create container with no foreign access
        container_name = client.generate_unique_container_name()
        resp = client.create_container(container_name)
        self.addCleanup(client.force_delete_containers, [container_name])
        self.assertEqual(resp.status_code, 201, 'Create container failed')

        #create an object
        object_name = client.generate_unique_object_name()
        object_data = 'Created in test by main user'
        content_length = str(len(object_data))
        resp = client.set_storage_object(
            container_name, object_name, content_length=content_length,
            content_type=CONTENT_TYPE_TEXT, payload=object_data)
        self.assertEqual(resp.status_code, 201, 'Create object failed')

        dic = {}
        dic['list_containers'] = {'code': 403,
                                  'msg': 'Get containers should fail'}
        dic['create_c'] = {'code': 403, 'msg': 'Create container should fail'}
        dic['get_c_meta'] = {'code': 403,
                             'msg': 'Get container metadata should fail'}
        dic['list_objects'] = {'code': 403,
                               'msg': 'Get object list should fail forbidden'}
        dic['create_o'] = {'code': 403, 'msg': 'Create object should fail'}
        dic['get_o_meta'] = {'code': 403,
                             'msg': 'Get object metadata should fail'}
        dic['set_o_meta'] = {'code': 403, 'msg': 'Metadata update should fail'}
        dic['get_object'] = {'code': 403, 'msg': 'Get obj should fail'}
        dic['copy'] = {'code': 403, 'msg': 'Copy Object should fail'}
        dic['put_copy'] = {'code': 403, 'msg': 'PutCopy Object should fail'}
        dic['delete_object'] = {'code': 403,
                                'msg': 'Delete object should fail'}
        self.rbac_regression_test(
            self.alt_client, dic, container_name, object_name)

    @attr('regression', type='positive')
    def test_foreign_account_container_read_access(self):
        """
        Scenario:

        Expected Results:
        """
        client = self.client

        #create container with subuser read access
        headers = {}
        headers[self.container_read_header] = self.foreign_name
        container_name = client.generate_unique_container_name()
        resp = client.create_container(container_name, headers=headers)
        self.addCleanup(client.force_delete_containers, [container_name])
        self.assertEqual(resp.status_code, 201, 'Create container failed')

        #create an object
        object_name = client.generate_unique_object_name()
        object_data = 'Created in test by main user'
        content_length = str(len(object_data))
        resp = client.set_storage_object(
            container_name, object_name, content_length=content_length,
            content_type=CONTENT_TYPE_TEXT, payload=object_data)
        self.assertEqual(resp.status_code, 201, 'Create object failed')

        dic = {}
        dic['list_containers'] = {'code': 403,
                                  'msg': 'Get containers should fail'}
        dic['create_c'] = {'code': 403, 'msg': 'Create container should fail'}
        dic['get_c_meta'] = {'code': 204,
                             'msg': 'Get container metadata should pass'}
        dic['list_objects'] = {'code': 200, 'msg': 'Get obj list should pass'}
        dic['create_o'] = {'code': 403, 'msg': 'Create object should fail'}
        dic['get_o_meta'] = {'code': 200,
                             'msg': 'Get obj metadata should fail'}
        dic['set_o_meta'] = {'code': 403, 'msg': 'Metadata update should fail'}
        dic['get_object'] = {'code': 200, 'msg': 'Get obj should fail'}
        dic['copy'] = {'code': 403, 'msg': 'Copy Object should fail'}
        dic['put_copy'] = {'code': 201, 'msg': 'PutCopy Object should pass'}
        dic['delete_object'] = {'code': 403,
                                'msg': 'Delete object should fail'}
        self.rbac_regression_test(
            self.alt_client, dic, container_name, object_name)

    @attr('regression', type='negative')
    def test_foreign_account_container_revoked_read_access(self):
        """
        Scenario:

        Expected Results:
        """
        client = self.client
        #create container with subuser read access
        headers = {}
        headers[self.container_read_header] = self.foreign_name
        container_name = client.generate_unique_container_name()
        resp = client.create_container(container_name, headers=headers)
        self.addCleanup(client.force_delete_containers, [container_name])
        self.assertEqual(resp.status_code, 201, 'Create container failed')

        #create an object
        object_name = client.generate_unique_object_name()
        object_data = 'Created in test by main user'
        content_length = str(len(object_data))
        resp = client.set_storage_object(
            container_name, object_name, content_length=content_length,
            content_type=CONTENT_TYPE_TEXT, payload=object_data)
        self.assertEqual(resp.status_code, 201, 'Create object failed')

        #get object with subclient(get)
        resp = self.alt_client.get_storage_object(container_name, object_name)
        self.assertEqual(resp.status_code, 200, 'Should have access to obj')

        headers = {}
        #revoke subuser permissions
        headers[self.container_write_header] = 'notthesubuser'
        headers[self.container_read_header] = 'notthesubuser'
        resp = self.client.set_container_metadata(
            container_name, metadata=None, headers=headers)
        self.assertEqual(resp.status_code, 204, 'Set headers failed')

        dic = {}
        dic['list_containers'] = {'code': 403,
                                  'msg': 'Get containers should fail'}
        dic['create_c'] = {'code': 403, 'msg': 'Create container should fail'}
        dic['get_c_meta'] = {'code': 403,
                             'msg': 'Get container metadata should fail'}
        dic['list_objects'] = {'code': 403,
                               'msg': 'Get object list should fail'}
        dic['create_o'] = {'code': 403,
                           'msg': 'Create object should fail'}
        dic['get_o_meta'] = {'code': 403,
                             'msg': 'Get object metadata should fail'}
        dic['set_o_meta'] = {'code': 403, 'msg': 'Metadata update should fail'}
        dic['get_object'] = {'code': 403, 'msg': 'Get obj should fail'}
        dic['copy'] = {'code': 403, 'msg': 'Copy Object should fail'}
        dic['put_copy'] = {'code': 403, 'msg': 'PutCopy Object should fail'}
        dic['delete_object'] = {'code': 403,
                                'msg': 'Delete object should fail'}
        self.rbac_regression_test(
            self.alt_client, dic, container_name, object_name)

    @attr('regression', type='positive')
    def test_foreign_account_container_write_access(self):
        """
        Scenario:

        Expected Results:
        """
        client = self.client
        #create container with subuser write access
        headers = {}
        headers[self.container_write_header] = self.foreign_name
        container_name = client.generate_unique_container_name()
        resp = client.create_container(container_name, headers=headers)
        self.addCleanup(client.force_delete_containers, [container_name])
        self.assertEqual(resp.status_code, 201, 'Create container failed')

        #create an object
        object_name = client.generate_unique_object_name()
        object_data = 'Created in test by main user'
        content_length = str(len(object_data))
        resp = client.set_storage_object(
            container_name, object_name, content_length=content_length,
            content_type=CONTENT_TYPE_TEXT, payload=object_data)
        self.assertEqual(resp.status_code, 201, 'Create object failed')

        dic = {}
        dic['list_containers'] = {'code': 403,
                                  'msg': 'Get containers should fail'}
        dic['create_c'] = {'code': 403, 'msg': 'Create container should fail'}
        dic['get_c_meta'] = {'code': 403,
                             'msg': 'Get container metadata should fail'}
        dic['list_objects'] = {'code': 403,
                               'msg': 'Get object list should fail'}
        dic['create_o'] = {'code': 201, 'msg': 'Create object should pass'}
        dic['get_o_meta'] = {'code': 403,
                             'msg': 'Get object metadata should fail'}
        dic['set_o_meta'] = {'code': 403, 'msg': 'Metadata update should fail'}
        dic['get_object'] = {'code': 403, 'msg': 'Get obj should fail'}
        dic['copy'] = {'code': 201, 'msg': 'Copy Object should pass'}
        dic['put_copy'] = {'code': 403, 'msg': 'PutCopy Object should fail'}
        dic['delete_object'] = {'code': 204,
                                'msg': 'Delete object should pass'}
        self.rbac_regression_test(
            self.alt_client, dic, container_name, object_name)

    @attr('regression', type='negative')
    def test_foreign_account_container_revoked_write_access(self):
        """
        Scenario:

        Expected Results:
        """
        client = self.client
        #create container with subuser write access
        headers = {}
        headers[self.container_write_header] = self.foreign_name
        container_name = client.generate_unique_container_name()
        resp = client.create_container(container_name, headers=headers)
        self.addCleanup(client.force_delete_containers, [container_name])
        self.assertEqual(resp.status_code, 201, 'Create container failed')

        #create an object
        object_name = client.generate_unique_object_name()
        object_data = 'Created in test by main user'
        content_length = str(len(object_data))
        resp = client.set_storage_object(
            container_name, object_name, content_length=content_length,
            content_type=CONTENT_TYPE_TEXT, payload=object_data)
        self.assertEqual(resp.status_code, 201, 'Create object failed')

        #create object with foreign client
        o_name = client.generate_unique_object_name()
        object_data = 'Created in test by main user'
        content_length = str(len(object_data))
        resp = self.alt_client.set_storage_object(
            container_name, o_name, content_length=content_length,
            content_type=CONTENT_TYPE_TEXT, payload=object_data)
        self.assertEqual(resp.status_code, 201, 'Create object failed')

        headers = {}
        #revoke subuser permissions
        headers[self.container_write_header] = 'notthesubuser'
        headers[self.container_read_header] = 'notthesubuser'
        resp = self.client.set_container_metadata(
            container_name, metadata=None, headers=headers)
        self.assertEqual(resp.status_code, 204, 'Set headers failed')

        dic = {}
        dic['list_containers'] = {'code': 403,
                                  'msg': 'Get containers should fail'}
        dic['create_c'] = {'code': 403, 'msg': 'Create container should fail'}
        dic['get_c_meta'] = {'code': 403,
                             'msg': 'Get container metadata should fail'}
        dic['list_objects'] = {'code': 403,
                               'msg': 'Get object list should fail forbidden'}
        dic['create_o'] = {'code': 403, 'msg': 'Create object should fail'}
        dic['get_o_meta'] = {'code': 403,
                             'msg': 'Get object metadata should fail'}
        dic['set_o_meta'] = {'code': 403, 'msg': 'Metadata update should fail'}
        dic['get_object'] = {'code': 403, 'msg': 'Get obj should fail'}
        dic['copy'] = {'code': 403, 'msg': 'Copy Object should fail'}
        dic['put_copy'] = {'code': 403, 'msg': 'PutCopy Object should fail'}
        dic['delete_object'] = {'code': 403,
                                'msg': 'Delete object should fail'}
        self.rbac_regression_test(
            self.alt_client, dic, container_name, object_name)

#TODO: Special cases to consider.
#1. Since you can create subusers with any name and the containers can add
#   usernames  or rolenames or tenant id.  Is it possible to make a subuser
#   with a name that matches a rolename or a tenent id to get access to a
#   container. Example subuser name = "readgroup" accesses a role that a was
#   made by a customer.
#2.  Extra Foreign account tests.  Can a forigen account added to role access
#another account with a role of the same name added to a container
#3.  Can a foreign account with the observer role access another accounts files


