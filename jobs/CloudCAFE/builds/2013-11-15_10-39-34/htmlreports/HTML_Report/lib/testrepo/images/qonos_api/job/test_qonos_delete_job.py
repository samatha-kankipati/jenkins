from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute import ItemNotFound
from testrepo.common.testfixtures.images import BaseImagesFixture


class TestQonosDeleteJob(BaseImagesFixture):

    @attr('positive')
    def test_happy_path_delete_job(self):
        """Happy Path - Delete job.

        1) Create a job
        2) Delete the job
        3) Verify that the response code is 200
        4) Get the deleted job
        5) Verify that the response code is 404
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
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
            self.images_provider.jobs_client.get_job(job.id)

    @attr('positive')
    def test_delete_a_deleted_job(self):
        """Delete a deleted job.

        1) Create a job
        2) Delete the job
        3) Verify that the response code is 200
        4) Delete the job again
        5) Verify that the response code is 404
        6) Get the deleted job
        7) Verify that the response code is 404
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        job_obj = self.images_provider.create_active_jobs(sch_obj.entity.id)
        self.assertEquals(job_obj.status_code, 200,
                          msg.format('status_code', 200, job_obj.status_code))

        job = job_obj.entity

        del_job_obj = self.images_provider.jobs_client.delete_job(job.id)
        self.assertEquals(del_job_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     del_job_obj.status_code))

        with self.assertRaises(ItemNotFound):
            self.images_provider.jobs_client.delete_job(job.id)

        with self.assertRaises(ItemNotFound):
            self.images_provider.jobs_client.get_job(job.id)
