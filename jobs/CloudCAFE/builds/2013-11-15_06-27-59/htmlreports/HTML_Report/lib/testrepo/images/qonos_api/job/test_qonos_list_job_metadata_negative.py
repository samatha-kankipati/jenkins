import ccengine.common.tools.datagen as datagen
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute import ItemNotFound
from testrepo.common.testfixtures.images import BaseImagesFixture


class TestQonosListJobMetadataNegative(BaseImagesFixture):

    @attr('negative')
    def test_list_job_metadata_method_mismatch(self):
        """List job metadata method mismatch.

        1) Create a schedule containing metadata so that a job is created for
            it within the next 5 minutes
        2) Create a job from the schedule
        3) Attempt to request the base url of '/jobs/{id}/meta' using a POST
            method
        4) Verify that a correct validation message is returned
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

        keys = [key]
        values = [value]

        sch_metadata_obj = \
            self.images_provider.schedules_client.set_schedule_metadata(sch.id,
                                                                        keys,
                                                                        values)
        self.assertEquals(sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_metadata_obj.status_code))

        job_obj = self.images_provider.create_active_jobs(sch.id)
        self.assertEquals(job_obj.status_code, 200,
                          msg.format('status_code', 200, job_obj.status_code))

        job = job_obj.entity

        with self.assertRaises(ItemNotFound):
            self.images_provider.jobs_client. \
                list_job_metadata(job.id,
                                  requestslib_kwargs={'method': method})

    @attr('negative')
    def test_list_job_metadata_incorrect_url(self):
        """List job metadata incorrect url.

        1) Create a schedule containing metadata so that a job is created for
            it within the next 5 minutes
        2) Create a job from the schedule
        3) Attempt to request the base url of '/jobs/{id}/met'
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

        keys = [key]
        values = [value]

        sch_metadata_obj = \
            self.images_provider.schedules_client.set_schedule_metadata(sch.id,
                                                                        keys,
                                                                        values)
        self.assertEquals(sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_metadata_obj.status_code))

        job_obj = self.images_provider.create_active_jobs(sch.id)
        self.assertEquals(job_obj.status_code, 200,
                          msg.format('status_code', 200, job_obj.status_code))

        job = job_obj.entity

        bad_url = "{0}/jobs/{1}/met".format(self.config.images.url, job.id)

        with self.assertRaises(ItemNotFound):
            self.images_provider.jobs_client. \
                list_job_metadata(job.id,
                                  requestslib_kwargs={'url': bad_url})

    @attr('negative')
    def test_list_job_metadata_using_blank_id(self):
        """List job metadata using blank id.

        1) Attempt to list job metadata using a blank id
        2) Verify that a correct validation message is returned
        """

        job_id = ''

        with self.assertRaises(ItemNotFound):
            self.images_provider.jobs_client. \
                list_job_metadata(job_id)
