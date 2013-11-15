import ccengine.common.tools.datagen as datagen
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute import BadRequest, ItemNotFound
from testrepo.common.testfixtures.images import BaseImagesFixture


class TestQonosSetJobMetadata(BaseImagesFixture):

    @attr('negative')
    def test_set_job_metadata_method_mismatch(self):
        """Set job metadata method mismatch.

        1) Create a job from schedule without metadata
        2) Attempt to request the base url of '/jobs'{id}/metadata' using a
            POST method
        3) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        key = self.config.images.metadata_key
        value = datagen.random_string(size=10)
        method = "POST"
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        job_obj = self.images_provider.create_active_jobs(sch.id)

        self.assertEquals(job_obj.status_code, 200,
                          msg.format('status_code', 200, job_obj.status_code))

        job = job_obj.entity

        with self.assertRaises(ItemNotFound):
            self.images_provider.jobs_client. \
                set_job_metadata(job.id, key, value,
                                 requestslib_kwargs={'method': method})

    @attr('negative')
    def test_set_job_metadata_incorrect_url(self):
        """Set job metadata incorrect url.

        1) Create a job from schedule without metadata
        2) Attempt to request the base url of '/jobs'{id}/metadat'
        3) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        key = self.config.images.metadata_key
        value = datagen.random_string(size=10)
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        job_obj = self.images_provider.create_active_jobs(sch.id)

        self.assertEquals(job_obj.status_code, 200,
                          msg.format('status_code', 200, job_obj.status_code))

        job = job_obj.entity

        bad_url = "{0}/jobs/{1}/metadat".format(self.config.images.url, job.id)

        with self.assertRaises(ItemNotFound):
            self.images_provider.jobs_client. \
                set_job_metadata(job.id, key, value,
                                 requestslib_kwargs={'url': bad_url})

    @attr('negative')
    def test_set_job_metadata_incorrect_spelling_of_metadata(self):
        """Set job metadata incorrect spelling of metadata in the body.

        1) Create a job from schedule without metadata
        2) Create job metadata using 'metadat' in the body
        3) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        key = self.config.images.metadata_key
        value = datagen.random_string(size=10)
        alt_key = self.config.images.alt_metadata_key
        alt_value = datagen.random_string(size=10)
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        job_obj = self.images_provider.create_active_jobs(sch.id)

        self.assertEquals(job_obj.status_code, 200,
                          msg.format('status_code', 200, job_obj.status_code))

        job = job_obj.entity

        bad_data = {'metadat': {alt_key: alt_value}}

        with self.assertRaises(BadRequest):
            self.images_provider.jobs_client. \
                set_job_metadata(job.id, key, value,
                                 requestslib_kwargs={'data': bad_data})

    @attr('negative')
    def test_set_job_metadata_using_blank_id(self):
        """Set job metadata using a blank id.

        1) Create job metadata using a blank id
        2) Verify that a correct validation message is returned
        """

        key = self.config.images.metadata_key
        value = datagen.random_string(size=10)
        job_id = ''

        with self.assertRaises(ItemNotFound):
            self.images_provider.jobs_client. \
                set_job_metadata(job_id, key, value)

    @attr('negative')
    def test_set_job_metadata_using_special_characters_for_key(self):
        """Set job metadata using special characters for key.

        1) Create a job from schedule without metadata
        2) Create job metadata using special characters for key
        3) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        key = "<>"
        value = datagen.random_string(size=10)
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        job_obj = self.images_provider.create_active_jobs(sch.id)

        self.assertEquals(job_obj.status_code, 200,
                          msg.format('status_code', 200, job_obj.status_code))

        job = job_obj.entity

        '''TODO: Test will fail when RM bug #1714 is fixed'''
        job_metadata_obj = self.images_provider.jobs_client. \
            set_job_metadata(job.id, key, value)
        self.assertEquals(job_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     job_metadata_obj.status_code))

    @attr('negative')
    def test_set_job_metadata_using_special_characters_for_value(self):
        """Set job metadata using special characters for value.

        1) Create a job from schedule without metadata
        2) Create job metadata using special characters for value
        3) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        key = self.config.images.metadata_key
        value = "<>"
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        job_obj = self.images_provider.create_active_jobs(sch.id)
        self.assertEquals(job_obj.status_code, 200,
                          msg.format('status_code', 200, job_obj.status_code))

        job = job_obj.entity

        '''TODO: Test will fail when RM bug #1714 is fixed'''
        job_metadata_obj = self.images_provider.jobs_client. \
            set_job_metadata(job.id, key, value)
        self.assertEquals(job_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     job_metadata_obj.status_code))

    @attr('negative')
    def test_set_job_metadata_blank_parameter(self):
        """Set job metadata using a blank parameter.

        1) Create a job from schedule without metadata
        2) Create job metadata using a blank parameter
        3) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        key = self.config.images.metadata_key
        value = datagen.random_string(size=10)
        alt_value = datagen.random_string(size=10)
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        job_obj = self.images_provider.create_active_jobs(sch.id)

        self.assertEquals(job_obj.status_code, 200,
                          msg.format('status_code', 200, job_obj.status_code))

        job = job_obj.entity

        bad_data = {'metadata': {'': alt_value}}

        with self.assertRaises(BadRequest):
            self.images_provider.jobs_client. \
                set_job_metadata(job.id, key, value,
                                 requestslib_kwargs={'data': bad_data})

    @attr('negative')
    def test_set_job_metadata_for_deleted_job(self):
        """Set job metadata for deleted job.

        1) Create a job from schedule without metadata
        2) Delete the job
        3) Create job metadata for the deleted job
        4) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        key = self.config.images.metadata_key
        value = datagen.random_string(size=10)
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        job_obj = self.images_provider.create_active_jobs(sch.id)

        self.assertEquals(job_obj.status_code, 200,
                          msg.format('status_code', 200, job_obj.status_code))

        job = job_obj.entity

        del_job_obj = self.images_provider.jobs_client.delete_job(job.id)
        self.assertEquals(del_job_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     del_job_obj.status_code))

        with self.assertRaises(ItemNotFound):
            self.images_provider.jobs_client. \
                set_job_metadata(job.id, key, value)
