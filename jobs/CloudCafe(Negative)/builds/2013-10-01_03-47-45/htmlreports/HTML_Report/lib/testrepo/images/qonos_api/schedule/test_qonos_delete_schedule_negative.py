from testrepo.common.testfixtures.images import BaseImagesFixture
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute import ItemNotFound
from ccengine.domain.types import ScheduledImagesJobStatus
from ccengine.common.constants.images_constants import Constants
import ccengine.common.tools.datagen as datagen
import calendar
import time
from datetime import datetime, timedelta


class TestQonosDeleteScheduleNegative(BaseImagesFixture):

    @classmethod
    def setUpClass(cls):
        '''Creates the server instances used for all tests in this class'''

        super(TestQonosDeleteScheduleNegative, cls).setUpClass()

        server_name = datagen.random_string(size=10)

        server_obj = cls.images_provider.create_active_server(server_name)

        cls.instance_id = server_obj.entity.id

    @attr('negative')
    def test_delete_schedule_url_mismatch(self):
        '''Delete schedule with url mismatch'''

        """
        1) Attempt to request the base url of '/schedules' using a DELETE
            method
        2) Verify that a correct validation message is returned
        """

        with self.assertRaises(ItemNotFound):
            self.images_provider.schedules_client.delete_schedule()

    @attr('negative')
    def test_delete_schedule_with_blank_id(self):
        '''Delete schedule using a blank id'''

        """
        1) Delete a schedule using a blank id
        2) Verify that a correct validation message is returned
        """

        sch_id = ""
        with self.assertRaises(ItemNotFound):
            self.images_provider.schedules_client.delete_schedule(sch_id)

    @attr('negative')
    def test_delete_schedule_using_non_existing_id(self):
        '''Delete schedule using a non-existing id'''

        """
        1) Delete a schedule using a non-existing id
        2) Verify that a correct validation message is returned
        """

        sch_id = "1111"
        with self.assertRaises(ItemNotFound):
            self.images_provider.schedules_client.delete_schedule(sch_id)

    @attr('negative')
    def test_delete_schedule_using_letters_for_id(self):
        '''Delete schedule using letters for id'''

        """
        1) Delete a schedule using letters for id
        2) Verify that a correct validation message is returned
        """

        sch_id = "abc"
        with self.assertRaises(ItemNotFound):
            self.images_provider.schedules_client.delete_schedule(sch_id)

    @attr('negative')
    def test_delete_schedule_using_special_characters_for_id(self):
        '''Delete schedule using special characters for id'''

        """
        1) Delete a schedule using special characters for id
        2) Verify that a correct validation message is returned
        """

        sch_id = "<&&/>"
        with self.assertRaises(ItemNotFound):
            self.images_provider.schedules_client.delete_schedule(sch_id)

    @attr('negative')
    def test_delete_schedule_after_job_created(self):
        '''Delete schedule after a job created for it'''

        """
        1) Create a schedule such that a job is created for it in few minutes
        2) Make sure a job is created for that schedule
        3) Delete the schedule and make sure response code is 200
        4) Verify that the currently running job is not affected and
            completes successfully
        5) Get the deleted schedule and verify the response code is 404
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        msg = Constants.MESSAGE
        key = self.config.images.metadata_key
        instance_id = self.instance_id
        user_name_metadata_key = self.config.images.user_name_metadata_key
        user_name = self.config.images.user_name

        metadata = {key: instance_id, user_name_metadata_key: user_name}

        sch_obj = self.images_provider.\
            create_active_schedules(tenant, action, metadata=metadata)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

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

        job = self.images_provider.jobs_client.get_job(jobs[0].id)

        self.assertEquals(job.status_code, 200,
                          msg.format('status_code', 200, job.status_code))

        self.assertTrue(self.images_provider.\
                        is_job_status_workable(job.entity.status),
                        msg.format('status', 'workable job status',
                                   job.entity.status))

        self.images_provider.\
        wait_for_job_status(jobs[0].id, ScheduledImagesJobStatus.PROCESSING)

        del_sch_obj = self.images_provider.schedules_client.\
            delete_schedule(id=sch.id)
        self.assertEquals(del_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     del_sch_obj.status_code))

        self.images_provider.wait_for_job_status(jobs[0].id,
                                                 ScheduledImagesJobStatus.DONE)

        job = self.images_provider.jobs_client.get_job(jobs[0].id)

        self.assertEquals(job.status_code, 200,
                          msg.format('status_code', 200, job.status_code))

        self.assertTrue(job.entity.worker_id is not None,
                        msg.format('worker', 'Not None',
                                   job.entity.worker_id))

        with self.assertRaises(ItemNotFound):
            self.images_provider.schedules_client.get_schedule(sch.id)
