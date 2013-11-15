'''
@summary: Tests basic functionality of novashell with servers, volumes, and snapshots
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from datetime import datetime
from time import time
from unittest2.suite import TestSuite
from testrepo.common.testfixtures.fixtures import BaseTestFixture
from ccengine.providers.compute.novashell import NovaShellProvider
from ccengine.domain.types import NovaVolumeStatusTypes
from ccengine.domain.types import NovaServerStatusTypes


def load_tests(loader, standard_tests, pattern):
    suite = TestSuite()
    suite.addTest(CBS_NovaCLI_IntegrationSmoke("test_create_sata_volume"))
    suite.addTest(CBS_NovaCLI_IntegrationSmoke("test_create_ssd_volume"))
    suite.addTest(CBS_NovaCLI_IntegrationSmoke("test_create_volume_snapshot"))
    suite.addTest(CBS_NovaCLI_IntegrationSmoke("test_create_volume_from_snapshot"))
    suite.addTest(CBS_NovaCLI_IntegrationSmoke("test_attach_sata_volume"))
    suite.addTest(CBS_NovaCLI_IntegrationSmoke("test_detach_sata_volume"))
    suite.addTest(CBS_NovaCLI_IntegrationSmoke("test_attach_ssd_volume"))
    suite.addTest(CBS_NovaCLI_IntegrationSmoke("test_detach_ssd_volume"))
    suite.addTest(CBS_NovaCLI_IntegrationSmoke("test_delete_volume_from_snapshot"))
    suite.addTest(CBS_NovaCLI_IntegrationSmoke("test_delete_volume_snapshot"))
    suite.addTest(CBS_NovaCLI_IntegrationSmoke("test_delete_sata_volume"))
    suite.addTest(CBS_NovaCLI_IntegrationSmoke("test_delete_ssd_volume"))
    return suite


class CBS_NovaCLI_IntegrationSmoke(BaseTestFixture):
    '''
    @summary: Tests creating a server instance, volume, volume snapshot,
              volume from a snapshot and deleting all of them.
    '''
    @classmethod
    def setUpClass(cls):
        '''Creating Servers (in setup)'''
        super(CBS_NovaCLI_IntegrationSmoke, cls).setUpClass()

        cls.NovaShellProvider = NovaShellProvider(cls.config)
        cls.base_resource_name = 'CBS_Novaclient_Integration_SmokeTest'
        cls.device_name = "/dev/xvde"
        cls.min_volume_size = int(cls.NovaShellProvider.config.nova_shell.
                                  min_volume_size)
        cls.max_volume_size = int(cls.NovaShellProvider.config.nova_shell.
                                  max_volume_size)
        cls.snapshot_create_wait = max((cls.min_volume_size * 30), 500)
        cls.attach_timeout = 600
        stamp = datetime.now().microsecond
        cls.volume_name = "{0}_SATAVolume{1}".format(
            cls.base_resource_name, stamp)
        cls.ssd_volume_name = "{0}_SSDVolume{1}".format(
            cls.base_resource_name, stamp)
        cls.snapshot_name = cls.volume_name + "-snapshot"
        cls.volume_from_snapshot_name = cls.snapshot_name + "-new_volume"
        cls.image_name = cls.config.nova_shell.image_name
        cls.flavor = cls.config.nova_shell.flavor or '2'

        cls.server_domain_object = None

        cls.set_server()

    @classmethod
    def set_server(cls):
        attempt = 1
        max_retries = 3
        image_id = None

        try:
            image_id = cls.NovaShellProvider.get_image_by_name(
                cls.image_name)
        except Exception as exception:
            print 'Unable to get the id for the "{0}" image'.format(
                cls.image_name)
            raise exception

        while attempt <= max_retries:
            failure = False
            start = time()
            elapsed = 0
            stamp = datetime.now().microsecond
            cls.server_name = "{0}_Server{1}".format(
                cls.base_resource_name, stamp)

            print "\nInitiating attempt {0} to create a server ({1})".format(
                attempt, cls.server_name)

            try:
                cls.server_domain_object = cls.NovaShellProvider.\
                    create_active_server(cls.server_name, cls.flavor, image_id)
            except Exception as exception:
                failure = True
                elapsed = time() - start
                print ('Server create attempt {0} failed after {1} seconds'.
                       format(attempt, elapsed))
                print 'NovaShellProvider Exception: {0}'.format(exception)

            if failure is False and cls.server_domain_object is None:
                print (
                    "\n Recieved unexpected response / could not deserialize "
                    "response")
                failure = True

            if failure is False and (cls.server_domain_object.Status !=
                                     NovaServerStatusTypes.ACTIVE):
                failure = True
                print("\nServer never entered the ACTIVE state".format(
                    cls.server_name, elapsed, cls.server_domain_object.Status))

            if failure is False and (cls.server_domain_object.Status ==
                                     NovaServerStatusTypes.ACTIVE):
                print(
                    "\nServer has entered the ACTIVE state, begining tests..."
                    .format(
                        cls.server_name, elapsed,
                        cls.server_domain_object.Status))
                cls.admin_password = cls.server_domain_object.admin_password
                break

            attempt += 1

        else:
            cls.assertClassSetupFailure(
                'Attempted to create an active server {0} times, but all '
                'attempts failed'.format(max_retries))

    @classmethod
    def tearDownClass(cls):
        cls.NovaShellProvider.delete_volume_snapshot(cls.snapshot_name)
        cls.NovaShellProvider.delete_volume(cls.volume_from_snapshot_name)
        cls.NovaShellProvider.delete_volume(cls.volume_name)
        cls.NovaShellProvider.delete_server(cls.server_name)
        super(CBS_NovaCLI_IntegrationSmoke, cls).tearDownClass()

    def test_create_sata_volume(self):
        ''' Creating Volume'''
        self.fixture_log.info("Testing creating a volume")
        volume_type_domain_object = self.NovaShellProvider.select_volume_type(
            'SATA')

        self.assertIsNotNone(
            volume_type_domain_object,
            "Could not select a volume type to create volume")

        volume = self.NovaShellProvider.create_volume(
            self.volume_name,
            volume_type_domain_object.Name,
            self.min_volume_size)

        self.assertIsNotNone(volume, "Unable to create new volume!")

        self.assertEqual(
            volume['Size'],
            str(self.min_volume_size),
            "Volume created with incorrect size")

        self.assertEqual(
            volume['VolumeType'],
            volume_type_domain_object.Name,
            "Volume created with incorrect type")

        self.fixture_log.info("Volume Created: %s" % volume)

    def test_create_ssd_volume(self):
        ''' Creating Volume'''
        self.fixture_log.info("Testing creating a volume")
        volume_type_domain_object = self.NovaShellProvider.select_volume_type(
            'SSD')

        self.assertIsNotNone(
            volume_type_domain_object,
            "Could not select a volume type to create volume")

        ssd_volume = self.NovaShellProvider.create_volume(
            self.ssd_volume_name,
            volume_type_domain_object.Name,
            self.min_volume_size)

        self.assertIsNotNone(ssd_volume, "Unable to create new volume!")

        self.assertEqual(
            ssd_volume['Size'],
            str(self.min_volume_size),
            "Volume created with incorrect size")

        self.assertEqual(
            ssd_volume['VolumeType'],
            volume_type_domain_object.Name,
            "Volume created with incorrect type")

        self.fixture_log.info("Volume Created: {0}".format(ssd_volume))

    def test_create_volume_snapshot(self):
        ''' Creating Volume Snapshot'''
        new_volume_snapshot = self.NovaShellProvider.create_volume_snapshot(
            self.volume_name,
            display_name=self.snapshot_name,
            timeout=self.snapshot_create_wait)

        self.assertNotEqual(
            new_volume_snapshot,
            {},
            "Unable to create new volume snapshot!")

        self.assertEqual(
            new_volume_snapshot['DisplayName'],
            self.snapshot_name,
            "Created Volume Snapshot name not created as expected")

        self.assertEqual(
            new_volume_snapshot['Status'],
            NovaVolumeStatusTypes.AVAILABLE,
            "Created Volume Snapshot status is NOT Available")

    def test_create_volume_from_snapshot(self):
        ''' Creating Volume FROM Snapshot'''

        volume_from_snapshot = self.NovaShellProvider.\
            create_volume_from_snapshot(
                self.volume_from_snapshot_name,
                self.snapshot_name,
                timeout=self.snapshot_create_wait,
                volume_size=int(
                    self.NovaShellProvider.config.nova_shell.min_volume_size))

        self.assertIsNotNone(
            volume_from_snapshot,
            "Unable to create new volume from snapshot!")

        self.assertEqual(
            volume_from_snapshot['DisplayName'],
            self.volume_from_snapshot_name,
            "Volume from Snapshot created with incorrect Name")

        self.assertEqual(
            volume_from_snapshot['Status'],
            NovaVolumeStatusTypes.AVAILABLE,
            "Volume from Snapshot status is NOT available.")

    def test_attach_sata_volume(self):
        '''Attaching Volume to server'''

        attached_volume = self.NovaShellProvider.attach_volume(
            self.server_domain_object.Name,
            self.volume_name, self.device_name,
            self.attach_timeout)

        self.assertIsNotNone(
            attached_volume,
            'NovaShellProvider returned an empty response')

        self.assertNotEqual(attached_volume, {}, "Unable to attach volume!")

        self.assertEqual(
            attached_volume['Status'],
            NovaVolumeStatusTypes.IN_USE,
            "Attached Volume status is NOT in-use")

        self.assertEqual(
            attached_volume['Attachedto'],
            self.server_domain_object.ID,
            "Volume attached to incorrect Server")

    def test_detach_sata_volume(self):
        '''Detaching Volume from server'''
        server_domain_object = self.NovaShellProvider.get_server(
            self.server_name)

        self.assertIsNotNone(
            server_domain_object,
            "Unable to get server {0} for volume to attach".format(
                self.server_name))

        detached_volume = self.NovaShellProvider.detach_volume(
            server_domain_object.Name,
            self.volume_name)

        self.assertNotEqual(detached_volume, {}, "Unable to detach volume!")

        self.assertEqual(
            detached_volume['Status'],
            NovaVolumeStatusTypes.AVAILABLE,
            "Detached Volume status is NOT Available")

        self.assertNotEqual(
            detached_volume['Attachedto'],
            server_domain_object.ID,
            "Volume Still Attached to Server: {0}".format(
                detached_volume['Attachedto']))

    def test_attach_ssd_volume(self):
        '''Attaching Volume to server'''

        attached_volume = self.NovaShellProvider.attach_volume(
            self.server_domain_object.Name,
            self.ssd_volume_name, self.device_name,
            self.attach_timeout)

        self.assertIsNotNone(
            attached_volume,
            'NovaShellProvider returned an empty response')

        self.assertNotEqual(attached_volume, {}, "Unable to attach volume!")

        self.assertEqual(
            attached_volume['Status'],
            NovaVolumeStatusTypes.IN_USE,
            "Attached Volume status is NOT in-use")

        self.assertEqual(
            attached_volume['Attachedto'],
            self.server_domain_object.ID,
            "Volume attached to incorrect Server")

    def test_detach_ssd_volume(self):
        '''Detaching Volume from server'''
        server_domain_object = self.NovaShellProvider.get_server(
            self.server_name)

        self.assertIsNotNone(
            server_domain_object,
            "Unable to get server {0} for volume to attach".format(
                self.server_name))

        detached_volume = self.NovaShellProvider.detach_volume(
            server_domain_object.Name,
            self.ssd_volume_name)

        self.assertNotEqual(detached_volume, {}, "Unable to detach volume!")

        self.assertEqual(
            detached_volume['Status'],
            NovaVolumeStatusTypes.AVAILABLE,
            "Detached Volume status is NOT Available")

        self.assertNotEqual(
            detached_volume['Attachedto'],
            server_domain_object.ID,
            "Volume Still Attached to Server: {0}".format(
                detached_volume['Attachedto']))

    def test_delete_volume_from_snapshot(self):
        '''Deleting volume that was created from snapshot'''
        self.fixture_log.info(
            "Testing deleting and removing volume from a snapshot: {0}".format(
                self.volume_from_snapshot_name))
        is_volume_from_snapshot_deleted = self.NovaShellProvider.delete_volume(
            self.volume_from_snapshot_name)

        self.assertTrue(
            is_volume_from_snapshot_deleted,
            "Unable to delete and remove volume {0}!".format(
                self.volume_from_snapshot_name))

    def test_delete_volume_snapshot(self):
        is_snapshot_deleted = self.NovaShellProvider.delete_volume_snapshot(
            self.snapshot_name,
            timeout=self.snapshot_create_wait)

        self.assertTrue(
            is_snapshot_deleted,
            "Unable to delete and remove Snapshot {0}!".format(
                self.snapshot_name))

    def test_delete_sata_volume(self):
        is_volume_name_deleted = self.NovaShellProvider.delete_volume(
            self.volume_name)

        self.assertTrue(
            is_volume_name_deleted,
            "Unable to delete and remove volume {0}!".format(self.volume_name))

    def test_delete_ssd_volume(self):
        is_volume_name_deleted = self.NovaShellProvider.delete_volume(
            self.ssd_volume_name)

        self.assertTrue(
            is_volume_name_deleted,
            "Unable to delete and remove volume {0}!".format(
                self.ssd_volume_name))
