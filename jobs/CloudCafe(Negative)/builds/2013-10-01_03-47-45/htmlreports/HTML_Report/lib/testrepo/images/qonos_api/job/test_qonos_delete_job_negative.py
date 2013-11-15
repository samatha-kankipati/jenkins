from testrepo.common.testfixtures.images import BaseImagesFixture
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute import ItemNotFound


class TestQonosDeleteJobNegative(BaseImagesFixture):

    @attr('negative')
    def test_delete_job_with_blank_job_id(self):
        '''Delete job using blank job id'''

        """
        1) Delete a job using a blank job id
        2) Verify a job is not deleted and that a correct
            validation message is returned
        """

        job_id = ''

        with self.assertRaises(ItemNotFound):
            self.images_provider.jobs_client.delete_job(job_id)

    @attr('negative')
    def test_delete_job_for_non_existing_job_id(self):
        '''Delete job using non-existing job id'''

        """
        1) Delete a job using a non-existing job id
        2) Verify a job is not deleted and that a correct
            validation message is returned
        """

        job_id = '0'

        with self.assertRaises(ItemNotFound):
            self.images_provider.jobs_client.delete_job(job_id)
