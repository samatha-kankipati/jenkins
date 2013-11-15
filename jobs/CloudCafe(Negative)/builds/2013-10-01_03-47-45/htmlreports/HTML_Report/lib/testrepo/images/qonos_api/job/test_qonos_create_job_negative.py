from testrepo.common.testfixtures.images import BaseImagesFixture
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute import ItemNotFound


class TestQonosCreateJobNegative(BaseImagesFixture):

    @attr('negative')
    def test_create_job_with_blank_schedule_id(self):
        '''Create job using blank schedule id'''

        """
        1) Create job from schedule using a blank schedule id
        2) Verify job is not created and that a correct
            validation message is returned
        """

        sch_id = ''

        with self.assertRaises(ItemNotFound):
            self.images_provider.jobs_client.create_job(sch_id)

    @attr('negative')
    def test_create_job_for_non_existing_schedule_id(self):
        '''Create job using non-existing schedule id'''

        """
        1) Create job from schedule using a non-existing schedule id
        2) Verify job is not created and that a correct
            validation message is returned
        """

        sch_id = '0'

        with self.assertRaises(ItemNotFound):
            self.images_provider.jobs_client.create_job(sch_id)
