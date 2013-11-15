from testrepo.common.testfixtures.images import BaseImagesFixture
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute import ItemNotFound


class TestQonosGetJobNegative(BaseImagesFixture):

    @attr('negative')
    def test_get_job_with_blank_job_id(self):
        '''Get job using blank job id'''

        """
        1) Get job using a blank job id
        2) Verify job is not returned and that a correct
            validation message is returned
        """

        job_id = ''

        with self.assertRaises(ItemNotFound):
            self.images_provider.jobs_client.get_job(job_id)

    @attr('negative')
    def test_get_job_for_non_existing_job_id(self):
        '''Get job using non-existing job id'''

        """
        1) Get job using a non-existing job id
        2) Verify job is not returned and that a correct
            validation message is returned
        """

        job_id = '0'

        with self.assertRaises(ItemNotFound):
            self.images_provider.jobs_client.get_job(job_id)
