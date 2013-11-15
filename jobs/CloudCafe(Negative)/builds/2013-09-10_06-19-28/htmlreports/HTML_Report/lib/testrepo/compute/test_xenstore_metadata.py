from testrepo.common.testfixtures.compute import ComputeFixture
import base64
from ccengine.domain.types import NovaServerStatusTypes
from ccengine.common.tools.datagen import rand_name
from ccengine.common.constants.compute_constants import Constants
from ccengine.common.decorators import attr
import unittest2


class XenstoreMetadataTest(ComputeFixture):

    @classmethod
    def setUpClass(cls):
        super(XenstoreMetadataTest, cls).setUpClass()
        '''Setup method for all processes including initial server creation
        waiting for the server to become active and getting flavor details'''
        cls.name = rand_name("testservercc")
        '''Temporary Personality try out'''
        cls.file_contents = 'This is a test file.'
        cls.personality = [{'path': '/root/.csivh', 'contents':
                            base64.b64encode(cls.file_contents)}]

        '''Temporary Meta-data try out'''
        cls.metadata = {'meta_key_1': 'meta_value_1', 'meta_key_2': 'meta_value_2'}
        ''''''''''''''''''''''''''''''''''''
        cls.create_server_response = cls.servers_client.create_server(cls.name,
                                                                      cls.image_ref,
                                                                      cls.flavor_ref,
                                                                      cls.personality,
                                                                      cls.metadata)
        cls.created_server = cls.create_server_response.entity
        cls.active_server = cls.compute_provider.wait_for_server_status(
                                                 cls.created_server.id,
                                                 NovaServerStatusTypes.ACTIVE)
        cls.active_server.entity.adminPass = cls.created_server.adminPass
        cls.flavor_details = cls.flavors_client.get_flavor_details(cls.flavor_ref)
        cls.resources.add(cls.created_server.id,
                          cls.servers_client.delete_server)
        cls.server = cls.active_server.entity
        cls.remote_client = cls.compute_provider.get_remote_instance_client(cls.server)
        cls.server_xenstore_meta = cls.remote_client.get_xenstore_meta()

    @classmethod
    def tearDownClass(cls):
        super(XenstoreMetadataTest, cls).tearDownClass()

    @attr(type='xenstore', net='yes')
    def test_verify_xenstore_details_high_priority(self):
        self.assertEqual(self.server.name, self.server_xenstore_meta.hostname,
                         msg="Xenstore Metadata hostname did not match with server name")
        self.assertEqual(self.server.id, self.server_xenstore_meta.server_id,
                         msg="Id is not equal")
        self.assertEqual(self.server.links.self, self.server_xenstore_meta.server_uri,
                         msg="Server URI did not match")
        self.assertEqual(Constants.SERVICE_TYPE, self.server_xenstore_meta.service_type,
                         msg="Service type did not match")
        self.assertEqual(self.server.created, self.server_xenstore_meta.created_date,
                         msg="Created date is not equal")

    @attr(type='xenstore', net='yes')
    def test_verify_xenstore_metadata(self):
        self.assertEqual(self.server.metadata, self.server_xenstore_meta.metadata,
                         msg="Verify server metadata and xenstore metadata  match")

    @attr(type='xenstore', net='yes')
    def test_verify_xenstore_details_second_priority(self):
        self.assertEqual(self.server.status, self.server_xenstore_meta.status,
                         msg="Server status is matching")
        self.assertEqual(self.server.task_state, self.server_xenstore_meta.task_state,
                         msg="Task state is equal")
        self.assertEqual(self.server.vm_state, self.server_xenstore_meta.vm_state,
                         msg="VM state is equal")
        self.assertEqual(self.server.power_state, self.server_xenstore_meta.power_state,
                         msg="Power state is equal")
        self.assertEqual(self.server.image.id, self.server_xenstore_meta.image_id,
                         msg="Image ID match")
        self.assertEqual(self.server.image.links.bookmark, self.server_xenstore_meta.image_uri,
                         msg="Image URI is equal")
        self.assertEqual(self.server.flavor.id, self.server_xenstore_meta.flavor_id,
                         msg="Flavor ID match")
        self.assertEqual(self.server.flavor.links.bookmark, self.server_xenstore_meta.flavor_uri,
                         msg="Flavor URI is equal")
        self.assertEqual(self.server.accessIPv4, self.server_xenstore_meta.access_ipv4,
                         msg="Access IPv4 is equal")
        self.assertEqual(self.server.accessIPv6, self.server_xenstore_meta.access_ipv6,
                         msg="Access IPv6 is equal")
