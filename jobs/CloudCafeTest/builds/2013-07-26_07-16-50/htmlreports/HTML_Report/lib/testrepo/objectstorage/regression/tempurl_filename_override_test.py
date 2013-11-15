"""
Tempurl Filename Overrides
TempURLs support "filename" query parameter to override the content-disposition
header indicating to the browser what to save the file as.
"""
import random
import time

from urllib import quote
from datetime import datetime
from ccengine.common.tools.filetools import get_md5_hash
from testrepo.common.testfixtures.object_storage_fixture \
        import ObjectStorageTestFixture
from ccengine.common.tools.unicode_tools import UNICODE_BLOCKS

CONTENT_TYPE_TEXT = 'text/plain; charset=UTF-8'


class TempurlFilenameOverride(ObjectStorageTestFixture):

    def test_object_retrieval_with_filename_override(self):
        time.sleep(61)

        container_name = self.client.generate_unique_container_name()
        self.client.create_container(container_name)
        self.addCleanup(
                self.client.force_delete_containers,
                [container_name])

        object_name = self.client.generate_unique_object_name()
        object_name_override = 'foobar.txt'
        object_data = 'longshot test data'
        content_length = str(len(object_data))
        etag = self.filetools.get_md5_hash(object_data)
        headers = {'Etag': etag}
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=object_data,
                headers=headers)

        temp_key = '{0}{1}{2}{3}{4}'.format(
                'LONGSHOT308KEY',
                str(datetime.now().hour),
                str(random.randint(0, 1000)),
                str(datetime.now().second),
                str(random.randint(0, 1000)))
        key = get_md5_hash(temp_key)
        headers = {'X-Account-Meta-Temp-URL-Key': key}
        resp = self.client.set_account_temp_url_key(headers=headers)

        self.assertEqual(resp.status_code, 204)

        dl_tempurl = self.client.create_temp_url(
                'GET',
                container_name,
                object_name,
                '86400',
                key)
        resp = self.client.temp_url_get(dl_tempurl)

        self.assertIn('content-disposition', resp.headers.keys())
        self.assertEqual(
                resp.headers.get('content-disposition'),
                'attachment; filename="{0}"'.format(object_name))

        resp = self.client.temp_url_get(
                dl_tempurl,
                file_name=object_name_override)

        self.assertIn('content-disposition', resp.headers.keys())
        self.assertEqual(
                resp.headers.get('content-disposition'),
                'attachment; filename="{0}"'.format(object_name_override))

    def test_object_retrieval_with_unicode_filename_override(self):
        time.sleep(61)

        container_name = self.client.generate_unique_container_name()
        self.client.create_container(container_name)
        self.addCleanup(
                self.client.force_delete_containers,
                [container_name])

        object_name = self.client.generate_unique_object_name()
        object_name_override = 'foobar.txt'
        object_data = 'longshot test data'
        content_length = str(len(object_data))
        etag = self.filetools.get_md5_hash(object_data)
        headers = {'Etag': etag}
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=object_data,
                headers=headers)

        temp_key = '{0}{1}{2}{3}{4}'.format(
                'LONGSHOT308KEY',
                str(datetime.now().hour),
                str(random.randint(0, 1000)),
                str(datetime.now().second),
                str(random.randint(0, 1000)))
        key = get_md5_hash(temp_key)
        headers = {'X-Account-Meta-Temp-URL-Key': key}
        resp = self.client.set_account_temp_url_key(headers=headers)

        self.assertEqual(resp.status_code, 204)

        dl_tempurl = self.client.create_temp_url(
                'GET',
                container_name,
                object_name,
                '86400',
                key)

        unicode_override_name = '%s%s' % (
                '%00',
                object_name_override)

        resp = self.client.temp_url_get(
                dl_tempurl,
                file_name=unicode_override_name)

        self.assertIsNotNone(resp.headers['content-disposition'])

        expected = 'attachment; filename="%s%s"' % \
                ('%00', object_name_override)
        recieved = resp.headers['content-disposition']

        self.assertEqual(expected, recieved)

        for block in UNICODE_BLOCKS:
            block_iter = block.encoded_codepoints()
            character = block_iter.next()
            unicode_character = quote(character)
            unicode_override_name = '%s%s' % (
                    unicode_character,
                    object_name_override)

            resp = self.client.temp_url_get(
                    dl_tempurl,
                    file_name=unicode_override_name)

            self.assertIsNotNone(resp.headers['content-disposition'])

            if resp.headers['content-disposition'] is None:
                print block.name + ' ' + character
                print resp.headers
                print
            else:
                expected = 'attachment; filename="%s%s"' % \
                        (character, object_name_override)
                recieved = resp.headers['content-disposition']

                self.assertEqual(expected, recieved)
