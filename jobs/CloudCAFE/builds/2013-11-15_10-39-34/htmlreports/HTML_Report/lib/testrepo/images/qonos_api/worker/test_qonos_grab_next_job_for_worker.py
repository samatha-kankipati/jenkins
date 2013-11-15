import ccengine.common.tools.datagen as datagen
from ccengine.common.decorators import attr
from ccengine.domain.types import ScheduledImagesJobStatus
from testrepo.common.testfixtures.images import BaseImagesFixture


class TestQonosGrabNextJob(BaseImagesFixture):
    """ Tests Qonos grab next job."""

    @classmethod
    def setUpClass(cls):
        """ Creates the server instance used for all tests in this class."""

        super(TestQonosGrabNextJob, cls).setUpClass()

        server_name = datagen.random_string(size=10)

        server_obj = cls.images_provider.create_active_server(server_name)

        cls.instance_id = server_obj.entity.id

    @attr('positive')
    def test_grab_next_job_order(self):
        """ Tests jobs processing order.

        1) Create 2 schedules for reboot action
        2) Create a job for those 2 schedules
        3) Make sure worker_id is none for both the jobs
        4) Update the status of job 1 to "test_status" and then to "queued"
            so that, updated_at is updated to latest time.
        5) Grab next job for a worker and make sure job 2 is fetched since it
            has earliest updated_at though its created_at is not earliest
        6) Make sure worker_id is not none for job 2 and it is none for job 1

        """

        tenant = self.tenant
        action = self.alt_action

        key = self.config.images.metadata_key
        instance_id = self.instance_id
        user_name_metadata_key = self.config.images.user_name_metadata_key
        user_name = self.config.images.user_name

        metadata = {key: instance_id, user_name_metadata_key: user_name}

        sch1 = \
            self.images_provider.create_active_schedules(tenant, action,
                                                         metadata=metadata)

        sch2 = \
            self.images_provider.create_active_schedules(tenant, action,
                                                         metadata=metadata)

        job1 = self.images_provider.create_active_jobs(sch1.entity.id)

        job2 = self.images_provider.create_active_jobs(sch2.entity.id)

        self.assertIsNone(job1.entity.worker_id,
                          self.msg.format('worker_id', None,
                                          job1.entity.worker_id))

        self.assertIsNone(job2.entity.worker_id,
                          self.msg.format('worker_id', None,
                                          job2.entity.worker_id))

        self.images_provider.jobs_client.\
            update_job_status(job1.entity.id, status="test_status")

        self.images_provider.jobs_client.\
            update_job_status(job1.entity.id, status="queued")

        keys = ["status", "marker"]
        values = [ScheduledImagesJobStatus.DONE, self.marker]

        jobs = self.images_provider.list_jobs_pagination(keys, values)

        worker_id = jobs[0].worker_id

        next_job = self.images_provider.workers_client.\
            grab_next_job(worker_id, action=action)

        self.assertEquals(next_job.status_code, 200,
                          self.msg.format('status_code', 200,
                                          next_job.status_code))

        self.assertEquals(next_job.entity.id, job2.entity.id,
                          self.msg.format('next grabbed job', job2.entity.id,
                                          next_job.entity.id))

        job1 = self.images_provider.jobs_client.get_job(job1.entity.id)
        job2 = self.images_provider.jobs_client.get_job(job2.entity.id)

        self.assertEquals(job2.entity.worker_id, worker_id,
                          self.msg.format('worker_id', worker_id,
                                          job2.entity.worker_id))

        self.assertIsNone(job1.entity.worker_id,
                          self.msg.format('worker_id', None,
                                          job1.entity.worker_id))
