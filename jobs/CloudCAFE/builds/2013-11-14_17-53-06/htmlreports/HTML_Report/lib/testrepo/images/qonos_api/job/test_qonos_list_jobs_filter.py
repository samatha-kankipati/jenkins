from ccengine.common.decorators import attr
from ccengine.domain.types import ScheduledImagesJobStatus
from testrepo.common.testfixtures.images import BaseImagesFixture


class TestQonosListJobsFilter(BaseImagesFixture):

    @classmethod
    def setUpClass(cls):
        """Creates schedules and jobs used for all tests in this class."""

        super(TestQonosListJobsFilter, cls).setUpClass()

        sch_obj = cls.images_provider.create_active_schedules(cls.tenant,
                                                              cls.alt_action)

        alt_sch_obj = cls.images_provider. \
            create_active_schedules(cls.alt_tenant, cls.alt_action)

        job_obj = cls.images_provider.create_active_jobs(sch_obj.entity.id)

        alt_job_obj = cls.images_provider. \
            create_active_jobs(alt_sch_obj.entity.id)

        cls.schedule = sch_obj.entity
        cls.alt_schedule = alt_sch_obj.entity
        cls.job = job_obj.entity
        cls.alt_job = alt_job_obj.entity
        cls.marker = None

    def _list_jobs_by_single_attribute_only(self, keys, values):
        """Helper method to list jobs by a specified attribute only."""

        count = 1

        list_jobs = self.images_provider.list_jobs_pagination(keys, values)

        job_match = [x for x in list_jobs if x.id == self.job.id]

        self.assertEquals(len(job_match), count,
                          self.msg.format("Matched job length", count,
                                          len(job_match)))

    @attr('pos', 'filter')
    def test_list_jobs_by_schedule_id_only(self):
        """List jobs by schedule_id filter only.

        1) List jobs by schedule_id filter only
        2) Verify that the response code is 200
        3) Verify that the length of the returned list is 1
        4) Verify that the returned job is for passed schedule
        """

        count = 1
        keys = ["schedule_id", "marker"]
        values = [self.schedule.id, self.marker]

        list_jobs = self.images_provider.list_jobs_pagination(keys, values)

        self.assertEquals(len(list_jobs), count,
                          self.msg.format("length of the list", count,
                                          len(list_jobs)))

        self.assertEquals(list_jobs[0].schedule_id, self.schedule.id,
                          self.msg.format("schedule_id", self.schedule.id,
                                          list_jobs[0].schedule_id))

    @attr('pos', 'filter')
    def test_list_jobs_by_tenant_only(self):
        """List jobs by tenant filter only.

        1) List jobs by tenant filter only
        2) Verify that the response code is 200
        3) Verify that the length of the returned list is 1
        4) Verify that the returned job is matches the passed attribute
        """

        data = {"tenant": self.tenant, "marker": self.marker}
        self._list_jobs_by_single_attribute_only(keys=data.keys(),
                                                 values=data.values())

    @attr('pos', 'filter')
    def test_list_jobs_by_action_only(self):
        """List jobs by action filter only.

        1) List jobs by action filter only
        2) Verify that the response code is 200
        3) Verify that the length of the returned list is 1
        4) Verify that the returned job is matches the passed attribute
        """

        data = {"action": self.alt_action, "marker": self.marker}
        self._list_jobs_by_single_attribute_only(keys=data.keys(),
                                                 values=data.values())

    @attr('pos', 'filter')
    def test_list_jobs_by_status_only(self):
        """List jobs by status filter only.

        1) List jobs by status filter only
        2) Verify that the response code is 200
        3) Verify that the length of the returned list is 1
        4) Verify that the returned job is matches the passed attribute
        """

        alt_job_status = self.alt_job_status
        data = {"status": self.alt_job_status, "marker": self.marker}

        update_job_status_obj = self.images_provider.jobs_client.\
            update_job_status(self.job.id, alt_job_status)
        self.assertEquals(update_job_status_obj.status_code, 200,
                          self.msg.format('status_code', 200,
                                          update_job_status_obj.status_code))

        self._list_jobs_by_single_attribute_only(keys=data.keys(),
                                                 values=data.values())

    @attr('pos', 'filter')
    def test_list_jobs_by_worker_id_only(self):
        """List jobs by worker_id filter only.

        1) List jobs by worker id filter only
        2) Verify that the response code is 200
        3) Verify that the length of the returned list is 1
        4) Verify that the returned job is matches the passed attribute
        """

        count = 1
        keys = ["status", "marker"]
        values = [ScheduledImagesJobStatus.DONE, self.marker]

        jobs = self.images_provider.list_jobs_pagination(keys, values)
        self.assertGreaterEqual(len(jobs), count, "At least 1 job expected")

        data = {"worker_id": jobs[0].worker_id, "marker": self.marker}
        list_jobs = self.images_provider.list_jobs_pagination(data.keys(),
                                                              data.values())
        job_match = [x for x in list_jobs if x.id == jobs[0].id]
        self.assertGreaterEqual(len(job_match), count)

    @attr('pos', 'filter')
    def test_list_jobs_by_timeout_only(self):
        """List jobs by timeout filter only.

        1) List jobs by timeout filter only
        2) Verify that the response code is 200
        3) Verify that the length of the returned list is 1
        4) Verify that the returned job is matches the passed attribute
        """

        data = {"timeout": self.job.timeout, "marker": self.marker}
        self._list_jobs_by_single_attribute_only(keys=data.keys(),
                                                 values=data.values())

    @attr('pos', 'filter')
    def test_list_jobs_by_hard_timeout_only(self):
        """List jobs by hard_timeout filter only.

        1) List jobs by hard timeout filter only
        2) Verify that the response code is 200
        3) Verify that the length of the returned list is 1
        4) Verify that the returned job is matches the passed attribute
        """

        data = {"hard_timeout": self.job.hard_timeout, "marker": self.marker}
        self._list_jobs_by_single_attribute_only(keys=data.keys(),
                                                 values=data.values())

    @attr('pos', 'filter')
    def test_list_jobs_by_multiple_filter(self):
        """List jobs by multiple filter.

        1) List jobs by multiple filter
        2) Verify that the response code is 200
        3) Verify that the length of the returned list is 1
        4) Verify that the returned job is for passed schedule_id, tenant,
           action, worker_id, status, time_out and hard_timeout
        """

        count = 1
        keys = ["tenant", "schedule_id", "action", "worker_id", "status",
                "timeout", "hard_timeout", "marker"]
        values = [self.tenant, self.schedule.id, self.alt_action,
                  self.job.worker_id, self.job.status, self.job.timeout,
                  self.job.hard_timeout, self.marker]

        list_jobs = self.images_provider.list_jobs_pagination(keys, values)

        self.assertEquals(len(list_jobs), count,
                          self.msg.format("length of the list", count,
                                          len(list_jobs)))
