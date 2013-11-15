from testrepo.common.testfixtures.images import BaseImagesFixture
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute \
    import BadRequest, InternalServerError, ItemNotFound
from datetime import datetime, timedelta
from ccengine.domain.types import ScheduledImagesJobStatus
import ccengine.common.tools.datagen as datagen


class TestQonosUpdateJobStatusNegative(BaseImagesFixture):

    @classmethod
    def setUpClass(cls):
        '''Creates the server instances used for all tests in this class'''

        super(TestQonosUpdateJobStatusNegative, cls).setUpClass()

        server_name = datagen.random_string(size=10)
        tenant = cls.config.images.tenant
        action = cls.config.images.action

        server_obj = cls.images_provider.create_active_server(server_name)

        sch_obj = cls.images_provider.create_active_schedules(tenant, action)

        cls.instance_id = server_obj.entity.id
        cls.schedule = sch_obj.entity

    @attr('negative')
    def test_update_job_status_missing_body(self):
        """Update job status missing body. """

        """
        1) Attempt to request the base url of '/jobs/{id}/status' using a PUT
            method without a body
        2) Verify that a correct validation message is returned
        """

        sch = self.schedule
        msg = Constants.MESSAGE

        job_obj = self.images_provider.create_active_jobs(sch.id)
        self.assertEquals(job_obj.status_code, 200,
                          msg.format('status_code', 200, job_obj.status_code))

        job = job_obj.entity

        with self.assertRaises(InternalServerError):
            self.images_provider.jobs_client. \
                update_job_status_missing_body(job.id)

    @attr('negative')
    def test_update_job_status_incorrect_parameter_name_in_body(self):
        """Update job status incorrect parameter name in body. """

        """
        1) Attempt to request the base url of '/jobs/{id}/status' using a PUT
            method and incorrect parameter name in the body
        2) Verify that a correct validation message is returned
        """

        sch = self.schedule
        job_status = "error"
        timeout = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        error_message = Constants.NOT_FOUND_ERROR_MESSAGE
        msg = Constants.MESSAGE

        job_obj = self.images_provider.create_active_jobs(sch.id)
        self.assertEquals(job_obj.status_code, 200,
                          msg.format('status_code', 200, job_obj.status_code))

        job = job_obj.entity

        bad_param = {'status': {'status': 'error',
                                'error_message': "NOT FOUND",
                                'timeout': "2013-07-09T14:21:42",
                                'test': 'test'}}

        with self.assertRaises(BadRequest):
            self.images_provider.jobs_client. \
                update_job_status(job.id, job_status, timeout, error_message,
                                  requestslib_kwargs={'data': bad_param})

    @attr('negative')
    def test_update_completed_job_status(self):
        """Update completed job status to done. """

        """
        1) Create a schedule so that a job is created for it within the
            next 5 minutes
        2) List the jobs
        3) Verify that the response code is 200
        4) Make sure a job is created from the schedule
        5) Verify job is assigned with worker id
        6) Wait for the job status to change from 'queued' to 'processing'
        to 'done'
        7) Update the job status to 'done'
        8) Verify that the update is allowed

        """

        sch = self.schedule
        key = self.config.images.metadata_key
        instance_id = self.instance_id
        user_name_metadata_key = self.config.images.user_name_metadata_key
        user_name = self.config.images.user_name
        job_status = "DONE"
        msg = Constants.MESSAGE

        keys = [key, user_name_metadata_key]
        values = [instance_id, user_name]

        sch_metadata_obj = self.images_provider.schedules_client.\
            set_schedule_metadata(sch.id, keys, values)

        self.assertEquals(sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_metadata_obj.status_code))

        tm = datetime.now() - timedelta(seconds=60)
        next_run_time = tm.strftime('%Y-%m-%d %H:%M:%S')

        upd_sch_obj = \
            self.images_provider.schedules_client.update_schedule(
                id=sch.id, next_run=next_run_time)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        self.images_provider.wait_for_job_to_create(sch.id)

        jobs = self.images_provider.list_jobs_for_schedule(sch.id)

        self.assertEquals(len(jobs), 1, msg.format('job_length', 1, len(jobs)))

        self.assertTrue(self.images_provider.\
                        is_job_status_workable(jobs[0].status),
                        msg.format('status', 'workable job status',
                                   jobs[0].status))

        self.images_provider.wait_for_job_status(jobs[0].id,
                                                 ScheduledImagesJobStatus.DONE)

        update_job_status_obj = self.images_provider.jobs_client.\
            update_job_status(jobs[0].id, status=job_status)
        self.assertEquals(update_job_status_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     update_job_status_obj.status_code))

    @attr('negative')
    def test_update_deleted_job_status_timeout_error_message(self):
        """Update deleted job status, timeout, and error message. """

        """
        1) Create a job
        2) Delete the job
        3) Verify that the response code is 200
        4) Update the job's status, timeout and error_message
        5) Verify that a correct validation message is returned
        """

        sch = self.schedule
        job_status = "error"
        timeout = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        error_message = Constants.NOT_FOUND_ERROR_MESSAGE
        msg = Constants.MESSAGE

        job_obj = self.images_provider.create_active_jobs(sch.id)
        self.assertEquals(job_obj.status_code, 200,
                          msg.format('status_code', 200, job_obj.status_code))

        job = job_obj.entity

        del_job_obj = self.images_provider.jobs_client.delete_job(job.id)
        self.assertEquals(del_job_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     del_job_obj.status_code))

        with self.assertRaises(ItemNotFound):
            self.images_provider.jobs_client.\
                update_job_status(job.id, job_status, timeout, error_message)

    @attr('negative')
    def test_update_job_status_timeout_with_blank_value(self):
        """Update job status timeout with blank value. """

        """
        1) Create a job
        2) Update the job's timeout using a blank value
        3) Verify that a correct validation message is returned
        """

        sch = self.schedule
        job_status = "processing"
        timeout = ''
        error_message = Constants.NOT_FOUND_ERROR_MESSAGE
        msg = Constants.MESSAGE

        job_obj = self.images_provider.create_active_jobs(sch.id)
        self.assertEquals(job_obj.status_code, 200,
                          msg.format('status_code', 200, job_obj.status_code))

        job = job_obj.entity

        with self.assertRaises(InternalServerError):
            self.images_provider.jobs_client. \
                update_job_status(job.id, job_status, timeout, error_message)

    @attr('negative')
    def test_update_job_status_timeout_with_non_existing_value(self):
        """Update job status timeout with non-existing value. """

        """
        1) Create a job
        2) Update the job's timeout using a non-existing value
        3) Verify that a correct validation message is returned
        """

        sch = self.schedule
        job_status = "processing"
        timeout = "0000-03-12T12:10:30Z"
        error_message = Constants.NOT_FOUND_ERROR_MESSAGE
        msg = Constants.MESSAGE

        job_obj = self.images_provider.create_active_jobs(sch.id)
        self.assertEquals(job_obj.status_code, 200,
                          msg.format('status_code', 200, job_obj.status_code))

        job = job_obj.entity

        with self.assertRaises(InternalServerError):
            self.images_provider.jobs_client. \
                update_job_status(job.id, job_status, timeout, error_message)

        timeout = "2013-13-12T12:10:30Z"
        with self.assertRaises(InternalServerError):
            self.images_provider.jobs_client. \
                update_job_status(job.id, job_status, timeout, error_message)

        timeout = "2013-03-32T12:10:30Z"
        with self.assertRaises(InternalServerError):
            self.images_provider.jobs_client. \
                update_job_status(job.id, job_status, timeout, error_message)

        timeout = "2013-03-12T25:10:30Z"
        with self.assertRaises(InternalServerError):
            self.images_provider.jobs_client. \
                update_job_status(job.id, job_status, timeout, error_message)

        timeout = "2013-03-12T12:61:30Z"
        with self.assertRaises(InternalServerError):
            self.images_provider.jobs_client. \
                update_job_status(job.id, job_status, timeout, error_message)

        timeout = "2013-03-12T12:10:61Z"
        with self.assertRaises(InternalServerError):
            self.images_provider.jobs_client. \
                update_job_status(job.id, job_status, timeout, error_message)

    @attr('negative')
    def test_update_job_status_timeout_with_special_characters(self):
        """Update job status timeout with special characters. """

        """
        1) Create a job
        2) Update the job's timeout using special characters
        3) Verify that a correct validation message is returned
        """

        sch = self.schedule
        job_status = "processing"
        timeout = '<>'
        error_message = Constants.NOT_FOUND_ERROR_MESSAGE
        msg = Constants.MESSAGE

        job_obj = self.images_provider.create_active_jobs(sch.id)
        self.assertEquals(job_obj.status_code, 200,
                          msg.format('status_code', 200, job_obj.status_code))

        job = job_obj.entity

        with self.assertRaises(InternalServerError):
            self.images_provider.jobs_client. \
                update_job_status(job.id, job_status, timeout, error_message)

    @attr('negative')
    def test_update_job_status_error_message_with_special_characters(self):
        """Update job status error message with special characters. """

        """
        1) Create a job
        2) Update the job's timeout using special characters
        3) Verify that a correct validation message is returned
        """

        sch = self.schedule
        job_status = "processing"
        timeout = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        error_message = '<>'
        msg = Constants.MESSAGE

        job_obj = self.images_provider.create_active_jobs(sch.id)
        self.assertEquals(job_obj.status_code, 200,
                          msg.format('status_code', 200, job_obj.status_code))

        job = job_obj.entity

        '''TODO: This will fail when RM bug #1688 is fixed'''
        update_job_status_obj = self.images_provider.jobs_client. \
                update_job_status(job.id, job_status, timeout, error_message)
        self.assertEquals(update_job_status_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     update_job_status_obj.status_code))

    @attr('negative')
    def test_update_job_status_timeout_only(self):
        """Update job status timeout only. """

        """
        1) Create a job
        2) Update the job's timeout only
        3) Verify that a correct validation message is returned
        """

        sch = self.schedule
        timeout = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        msg = Constants.MESSAGE

        job_obj = self.images_provider.create_active_jobs(sch.id)
        self.assertEquals(job_obj.status_code, 200,
                          msg.format('status_code', 200, job_obj.status_code))

        job = job_obj.entity

        with self.assertRaises(InternalServerError):
            self.images_provider.jobs_client. \
                update_job_status(job.id, timeout=timeout)

    @attr('negative')
    def test_update_job_status_error_message_only(self):
        """Update job status error message only. """

        """
        1) Create a job
        2) Update the job's error message only
        3) Verify that a correct validation message is returned
        """

        sch = self.schedule
        error_message = 'error'
        msg = Constants.MESSAGE

        job_obj = self.images_provider.create_active_jobs(sch.id)
        self.assertEquals(job_obj.status_code, 200,
                          msg.format('status_code', 200, job_obj.status_code))

        job = job_obj.entity

        with self.assertRaises(InternalServerError):
            self.images_provider.jobs_client. \
                update_job_status(job.id, error_message=error_message)
