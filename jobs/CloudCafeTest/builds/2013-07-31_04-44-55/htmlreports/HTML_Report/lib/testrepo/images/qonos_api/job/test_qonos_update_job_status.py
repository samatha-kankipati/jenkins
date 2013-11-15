from testrepo.common.testfixtures.images import BaseImagesFixture
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
from datetime import datetime


class TestQonosUpdateJobStatus(BaseImagesFixture):

    @attr('positive')
    def test_happy_path_update_job_status(self):
        '''Happy Path - Update job status'''

        """
        1) Create a schedule
        2) Create a job from the schedule
        3) Update the job's status
        4) Verify that the response code is 200
        5) Verify that the response is as expected

        Attributes to verify:
            status
            timeout
            error_message
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        msg = Constants.MESSAGE
        job_status = "error"
        timeout = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        error_message = Constants.NOT_FOUND_ERROR_MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        job_obj = self.images_provider.create_active_jobs(sch.id)
        self.assertEquals(job_obj.status_code, 200,
                          msg.format('status_code', 200, job_obj.status_code))

        job = job_obj.entity

        update_job_status_obj = self.images_provider.jobs_client.\
            update_job_status(job.id, job_status, timeout, error_message)
        self.assertEquals(update_job_status_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     update_job_status_obj.status_code))

        update_job_status = update_job_status_obj.entity

        self.assertEquals(update_job_status.status, job_status.upper(),
                          msg.format('status', job_status.upper(),
                                     update_job_status.status))
        self.assertEquals(update_job_status.timeout, timeout,
                          msg.format('timeout', timeout,
                                     update_job_status.timeout))
        ''' @TODO: add assertion for error message in job_fault table '''
