"""
Tests Swfit Bulk Operations:
http://docs.openstack.org/developer/swift/misc.html#module-swift.common.middleware.bulk
"""
import os
import tarfile

from ccengine.common.tools.datatools import CLOUDCAFE_DATA_DIRECTORY
from ccengine.common.tools.datatools import CLOUDCAFE_TEMP_DIRECTORY
from testrepo.common.testfixtures.object_storage_fixture \
    import ObjectStorageTestFixture


class BulkExtractArchiveSmokeTest(ObjectStorageTestFixture):
    """
    Expand tar files into a swift account.
    """

    @classmethod
    def setUpClass(cls):
        super(BulkExtractArchiveSmokeTest, cls).setUpClass()

        archive_dir = '{0}{1}'.format(
            CLOUDCAFE_DATA_DIRECTORY, '/objectstorage/staticweb')

        filelist = []
        for f in os.listdir(archive_dir):
            filelist.append({
                'path': os.path.join(archive_dir, f),
                'name': f})

        supported_compression = (None, 'gz', 'bz2')
        cls.archives = {}

        for a in supported_compression:
            archive_name = '{0}{1}'.format(
                CLOUDCAFE_TEMP_DIRECTORY, '/qe_bulk_archive')

            archive_ext = 'tar'
            write_mode = 'w'
            if a is not None:
                archive_ext = '{0}.{1}'.format(archive_ext, a)
                write_mode = '{0}:{1}'.format(write_mode, a)

            archive_file = '{0}.{1}'.format(archive_name, archive_ext)

            tar = tarfile.open(archive_file, write_mode)
            for f in filelist:
                tar.add(f['path'], arcname=f['name'])
            tar.close()

            f = open(archive_file, 'r')
            cls.archives[archive_ext] = f.read()
            f.close()

    def test_objects_expanded_with_tar_archive(self):
        """
        Verify user can expand tar archive files
        Preconditions: None
        Assumptions: None
        Notes: This feature is not yet in production
        """
        container_name = self.client.generate_unique_container_name('bulk_tar')
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers, [container_name])

        r = self.client.extract_archive(
            self.archives['tar'],
            data_format='tar',
            container_name=container_name)
        self.assertEqual(r.status_code, 201, 'should extract tar archive.')

        # TODO(rich5317): add regression test -
        # 1. parse content for 13 ('Number Files Created: 13')
        # 2. parse content to check Errors is empty ('Errors:')

    def test_objects_expanded_with_tar_gz_archive(self):
        """
        Verify user can expand tar.gz archive files
        Preconditions: None
        Assumptions: None
        Notes: This feature is not yet in production
        """
        container_name = self.client.generate_unique_container_name('bulk_gz')
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers, [container_name])

        r = self.client.extract_archive(
            self.archives['tar.gz'],
            data_format='tar.gz',
            container_name=container_name)
        self.assertEqual(r.status_code, 201, 'should extract tar.gz archive.')

        # TODO(rich5317): add regression test -
        # 1. parse content for 13 ('Number Files Created: 13')
        # 2. parse content to check Errors is empty ('Errors:')

    def test_objects_expanded_with_tar_bz2_archive(self):
        """
        Verify user can expand tar.bz2 archive files
        Preconditions: None
        Assumptions: None
        Notes: This feature is not yet in production
        """
        container_name = self.client.generate_unique_container_name('bulk_bz2')
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers, [container_name])

        r = self.client.extract_archive(
            self.archives['tar.bz2'],
            data_format='tar.bz2',
            container_name=container_name)
        self.assertEqual(r.status_code, 201, 'should extract tar.bz2 archive.')

        # TODO(rich5317): add regression test -
        # 1. parse content for 13 ('Number Files Created: 13')
        # 2. parse content to check Errors is empty ('Errors:')

    def test_object_creation_with_tar_archive(self):
        """
        Verify user can upload tar archive files as objects
        Preconditions: None
        Assumptions: None
        Notes: This feature is not yet in production
        """
        container_name = self.client.generate_unique_container_name('bulk_tar')
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers, [container_name])

        object_name = self.client.generate_unique_object_name()
        object_data = self.archives['tar']
        content_length = str(len(object_data))
        r = self.client.set_storage_object(
            container_name,
            object_name,
            content_length=content_length,
            payload=object_data)
        self.assertEqual(r.status_code, 201, 'should create object.')

        r = self.client.get_storage_object(container_name, object_name)
        self.assertEqual(r.status_code, 200, 'should retrieve object')

    def test_object_creation_with_tar_gz_archive(self):
        """
        Verify user can upload tar.gz archive files as objects
        Preconditions: None
        Assumptions: None
        Notes: This feature is not yet in production
        """
        container_name = self.client.generate_unique_container_name('bulk_gz')
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers, [container_name])

        object_name = self.client.generate_unique_object_name()
        object_data = self.archives['tar.gz']
        content_length = str(len(object_data))
        r = self.client.set_storage_object(
            container_name,
            object_name,
            content_length=content_length,
            payload=object_data)
        self.assertEqual(r.status_code, 201, 'should create object.')

        r = self.client.get_storage_object(container_name, object_name)
        self.assertEqual(r.status_code, 200, 'should retrieve object')

    def test_object_creation_with_tar_bz2_archive(self):
        """
        Verify user can upload tar.bz2 archive files as objects
        Preconditions: None
        Assumptions: None
        Notes: This feature is not yet in production
        """
        container_name = self.client.generate_unique_container_name('bulk_bz2')
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers, [container_name])

        object_name = self.client.generate_unique_object_name()
        object_data = self.archives['tar.bz2']
        content_length = str(len(object_data))
        r = self.client.set_storage_object(
            container_name,
            object_name,
            content_length=content_length,
            payload=object_data)
        self.assertEqual(r.status_code, 201, 'should create object.')

        r = self.client.get_storage_object(container_name, object_name)
        self.assertEqual(r.status_code, 200, 'should retrieve object')

    def test_error_reported_with_tar_archive_and_tar_gz_identifier(self):
        """
        Verify behavior when an archive file is uploaded with incorrect
        extract-archive

        Preconditions: None
        Assumptions: None
        Notes: This feature is not yet in production
        """
        container_name = self.client.generate_unique_container_name('bulk_tar')
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers, [container_name])

        r = self.client.extract_archive(
            self.archives['tar'],
            data_format='tar.gz',
            container_name=container_name)
        self.assertEqual(r.status_code, 400, 'should return error.')

    def test_error_reported_with_tar_archive_and_tar_bz2_identifier(self):
        """
        Verify behavior when an archive file is uploaded with incorrect
        extract-archive

        Preconditions: None
        Assumptions: None
        Notes: This feature is not yet in production
        """
        container_name = self.client.generate_unique_container_name('bulk_tar')
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers, [container_name])

        r = self.client.extract_archive(
            self.archives['tar'],
            data_format='tar.bz2',
            container_name=container_name)
        self.assertEqual(r.status_code, 400, 'should return error.')

    def test_error_reported_with_tar_gz_archive_and_tar_identifier(self):
        """
        Verify behavior when an archive file is uploaded with incorrect
        extract-archive

        Preconditions: None
        Assumptions: None
        Notes: This feature is not yet in production
        """
        container_name = self.client.generate_unique_container_name('bulk_tar')
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers, [container_name])

        r = self.client.extract_archive(
            self.archives['tar.gz'],
            data_format='tar',
            container_name=container_name)
        self.assertEqual(r.status_code, 400, 'should return error.')

    def test_error_reported_with_tar_gz_archive_and_tar_bz2_identifier(self):
        """
        Verify behavior when an archive file is uploaded with incorrect
        extract-archive

        Preconditions: None
        Assumptions: None
        Notes: This feature is not yet in production
        """
        container_name = self.client.generate_unique_container_name('bulk_tar')
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers, [container_name])

        r = self.client.extract_archive(
            self.archives['tar.gz'],
            data_format='tar.bz2',
            container_name=container_name)
        self.assertEqual(r.status_code, 400, 'should return error.')

    def test_error_reported_with_tar_bz2_archive_and_tar_identifier(self):
        """
        Verify behavior when an archive file is uploaded with incorrect
        extract-archive

        Preconditions: None
        Assumptions: None
        Notes: This feature is not yet in production
        """
        container_name = self.client.generate_unique_container_name('bulk_gz')
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers, [container_name])

        r = self.client.extract_archive(
            self.archives['tar.bz2'],
            data_format='tar',
            container_name=container_name)
        self.assertEqual(r.status_code, 400, 'should return error.')

    def test_error_reported_with_tar_bz2_archive_and_tar_gz_identifier(self):
        """
        Verify behavior when an archive file is uploaded with incorrect
        extract-archive

        Preconditions: None
        Assumptions: None
        Notes: This feature is not yet in production
        """
        container_name = self.client.generate_unique_container_name('bulk_bz2')
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers, [container_name])

        r = self.client.extract_archive(
            self.archives['tar.bz2'],
            data_format='tar.gz',
            container_name=container_name)
        self.assertEqual(r.status_code, 400, 'should return error.')

    def test_error_reported_with_corrupt_tar_archive(self):
        """
        Verify behavior when a corrupt archive file is uploaded

        Preconditions: None
        Assumptions: None
        Notes: This feature is not yet in production
        """
        container_name = self.client.generate_unique_container_name('bulk_tar')
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers, [container_name])

        data = self.archives['tar']
        data = data.replace('css/staticweb.css', 'css/stat\x00cweb.css')

        r = self.client.extract_archive(
            data, data_format='tar', container_name=container_name)

        self.assertEqual(r.status_code, 400, 'should report error.')

    def test_error_reported_with_corrupt_tar_gz_archive(self):
        """
        Verify user can expand tar.gz archive files

        Preconditions: None
        Assumptions: None
        Notes: This feature is not yet in production
        """
        container_name = self.client.generate_unique_container_name('bulk_gz')
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers, [container_name])

        data = self.archives['tar.gz']
        data = data.replace('i', '\x00')

        r = self.client.extract_archive(
            data, data_format='tar', container_name=container_name)
        self.assertEqual(r.status_code, 400, 'should report error.')

    def test_error_reported_with_corrupt_tar_bz2_archive(self):
        """
        Verify user can expand tar.bz2 archive files

        Preconditions: None
        Assumptions: None
        Notes: This feature is not yet in production
        """
        container_name = self.client.generate_unique_container_name('bulk_bz2')
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers, [container_name])

        data = self.archives['tar.bz2']
        data = data.replace('i', '\x00')

        r = self.client.extract_archive(
            data, data_format='tar', container_name=container_name)
        self.assertEqual(r.status_code, 400, 'should report error.')
