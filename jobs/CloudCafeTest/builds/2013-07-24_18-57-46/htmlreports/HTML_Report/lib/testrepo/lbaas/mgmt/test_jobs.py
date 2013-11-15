from testrepo.common.testfixtures.load_balancers \
    import BaseLoadBalancersFixture
from ccengine.common.decorators import attr


class JobTests(BaseLoadBalancersFixture):

    @classmethod
    def setUpClass(cls):
        super(JobTests, cls).setUpClass()

    @attr('positive')
    def test_get_jobs_calls(self):
        '''Test the list jobs calls'''
        r = self.mgmt_client.get_jobs()
        self.assertEquals(r.status_code, 200)
        self.assertTrue(len(r.entity) > 0)
        job = r.entity[0]
        r = self.mgmt_client.get_job(job_id=job.id)
        self.assertEquals(r.status_code, 200)
        self.assertTrue(job.id == r.entity.id)
        self.assertTrue(job.state == r.entity.state)
        self.assertTrue(job.jobName == job.jobName)
