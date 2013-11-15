from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute import ItemNotFound
from testrepo.common.testfixtures.images import BaseImagesFixture


class TestQonosGetJobNegative(BaseImagesFixture):

    @attr('negative')
    def test_get_job_with_method_mismatch(self):
        """Get job with method mismatch.

        1) Attempt to request the base url of '/jobs/{id}' using a POST method
        2) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        method = "POST"
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        job_obj = self.images_provider.create_active_jobs(sch.id)

        job = job_obj.entity

        with self.assertRaises(ItemNotFound):
            self.images_provider.jobs_client. \
                get_job(job.id, requestslib_kwargs={'method': method})

    @attr('negative')
    def test_get_job_with_incorrect_url(self):
        """Get job with method mismatch.

        1) Attempt to request the base url of '/jobss/{id}'
        2) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        job_obj = self.images_provider.create_active_jobs(sch.id)

        job = job_obj.entity

        bad_url = "{0}/jobss/{1}".format(self.config.images.url, job.id)

        with self.assertRaises(ItemNotFound):
            self.images_provider.jobs_client. \
                get_job(job.id, requestslib_kwargs={'url': bad_url})

    @attr('negative')
    def test_get_job_with_blank_job_id(self):
        """Get job using blank job id.

        1) Get job using a blank job id
        2) Verify job is not returned and that a correct
            validation message is returned
        """

        job_id = ''

        with self.assertRaises(ItemNotFound):
            self.images_provider.jobs_client.get_job(job_id)

    @attr('negative')
    def test_get_job_for_non_existing_job_id(self):
        """Get job using non-existing job id.

        1) Get job using a non-existing job id
        2) Verify job is not returned and that a correct validation message is
            returned
        """

        job_id = '0'

        with self.assertRaises(ItemNotFound):
            self.images_provider.jobs_client.get_job(job_id)

    @attr('negative')
    def test_get_job_using_letters_for_id(self):
        """Get job using letters for id.

        1) Get job using letters for id
        2) Verify job is not returned and that a correct validation message is
            returned
        """

        job_id = 'asdqwe'

        with self.assertRaises(ItemNotFound):
            self.images_provider.jobs_client.get_job(job_id)

    @attr('negative')
    def test_get_job_using_special_characters_for_id(self):
        """Get job using letters for id.

        1) Get job using special characters for id
        2) Verify job is not returned and that a correct validation message is
            returned
        """

        job_id = '<'

        with self.assertRaises(ItemNotFound):
            self.images_provider.jobs_client.get_job(job_id)
