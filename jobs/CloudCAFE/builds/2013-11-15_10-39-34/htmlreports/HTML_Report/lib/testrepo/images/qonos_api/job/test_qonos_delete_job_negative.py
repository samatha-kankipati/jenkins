from datetime import datetime, timedelta

import ccengine.common.tools.datagen as datagen
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute import ItemNotFound
from ccengine.domain.types import ScheduledImagesJobStatus
from testrepo.common.testfixtures.images import BaseImagesFixture


class TestQonosDeleteJobNegative(BaseImagesFixture):

    @classmethod
    def setUpClass(cls):
        """Creates the server instance used for all tests in this class."""

        super(TestQonosDeleteJobNegative, cls).setUpClass()

        server_name = datagen.random_string(size=10)

        server_obj = cls.images_provider.create_active_server(server_name)

        cls.instance_id = server_obj.entity.id

    @attr('negative')
    def test_delete_job_with_incorrect_url(self):
        """Delete job with incorrect url.

        1) Attempt to request the base url of '/jobss' using a DELETE method
        2) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        bad_url = "{0}/jobss".format(self.config.images.url)
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        job_obj = self.images_provider.create_active_jobs(sch.id)

        job = job_obj.entity

        with self.assertRaises(ItemNotFound):
            self.images_provider.jobs_client. \
                delete_job(job.id, requestslib_kwargs={'url': bad_url})

    @attr('negative')
    def test_delete_job_with_blank_job_id(self):
        """Delete job using blank job id.

        1) Delete a job using a blank job id
        2) Verify a job is not deleted and that a correct
            validation message is returned
        """

        job_id = ''

        with self.assertRaises(ItemNotFound):
            self.images_provider.jobs_client.delete_job(job_id)

    @attr('negative')
    def test_delete_job_for_non_existing_job_id(self):
        """Delete job using non-existing job id.

        1) Delete a job using a non-existing job id
        2) Verify a job is not deleted and that a correct
            validation message is returned
        """

        job_id = '0'

        with self.assertRaises(ItemNotFound):
            self.images_provider.jobs_client.delete_job(job_id)

    @attr('negative')
    def test_delete_job_using_letters_for_id(self):
        """Delete job using letters for id.

        1) Delete a job using letters for job id
        2) Verify a job is not deleted and that a correct
            validation message is returned
        """

        job_id = 'asdqwe'

        with self.assertRaises(ItemNotFound):
            self.images_provider.jobs_client.delete_job(job_id)

    @attr('negative')
    def test_delete_job_using_special_characters_for_id(self):
        """Delete job using special characters for id.

        1) Delete a job using special characters for job id
        2) Verify a job is not deleted and that a correct
            validation message is returned
        """

        job_id = '<'

        with self.assertRaises(ItemNotFound):
            self.images_provider.jobs_client.delete_job(job_id)

    @attr('negative')
    def test_delete_job_worker_already_picked_up(self):
        """Delete job that a worker has already picked up.

        1) Create a schedule so that a job is created for it within the
            next 5 minutes
        2) List the jobs
        3) Verify that the response code is 200
        4) Make sure a job is created from the schedule
        5) Verify job is assigned with worker id
        6) Wait for the job status to change from 'queued' to 'processing'
        7) Delete the job
        8) Verify that the response code is 200
        9) Get the job
        10) Verify that the response code is 404
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        msg = Constants.MESSAGE
        key = self.config.images.metadata_key
        instance_id = self.instance_id
        user_name_metadata_key = self.config.images.user_name_metadata_key
        user_name = self.config.images.user_name
        marker = None

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

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

        keys = ["schedule_id", "marker"]
        values = [sch.id, marker]

        self.images_provider.wait_for_job_to_create(sch.id, keys=keys,
                                                    values=values)

        jobs = self.images_provider.list_jobs_for_schedule(sch.id, keys,
                                                           values)

        self.assertEquals(len(jobs), 1, msg.format('job_length', 1, len(jobs)))

        status = jobs[0].status

        self.assertTrue(self.images_provider.is_job_status_workable(status),
                        msg.format('status', 'workable job status', status))

        self.images_provider. \
            wait_for_job_status(jobs[0].id,
                                ScheduledImagesJobStatus.PROCESSING)

        del_job_obj = self.images_provider.jobs_client.delete_job(jobs[0].id)
        self.assertEquals(del_job_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     del_job_obj.status_code))

        with self.assertRaises(ItemNotFound):
            self.images_provider.jobs_client.get_job(jobs[0].id)
