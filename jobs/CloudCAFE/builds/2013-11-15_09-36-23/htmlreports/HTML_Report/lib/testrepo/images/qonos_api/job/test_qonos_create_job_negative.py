from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute import ItemNotFound, BadRequest
from testrepo.common.testfixtures.images import BaseImagesFixture


class TestQonosCreateJobNegative(BaseImagesFixture):

    @attr('negative')
    def test_create_job_from_schedule_method_mismatch(self):
        """Create job from schedule with method mismatch.

        1) Attempt to request the base url of '/jobs' using a PUT method
        2) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        msg = Constants.MESSAGE
        method = "PUT"

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        with self.assertRaises(ItemNotFound):
            self.images_provider.jobs_client. \
                create_job(sch.id, requestslib_kwargs={'method': method})

    @attr('negative')
    def test_create_job_from_schedule_incorrect_url(self):
        """Create job from schedule with incorrect url.

        1) Attempt to request the base url of '/jobss'
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

        with self.assertRaises(ItemNotFound):
            self.images_provider.jobs_client. \
                create_job(sch.id, requestslib_kwargs={'url': bad_url})

    @attr('negative')
    def test_create_job_from_schedule_incorrect_job_spelling(self):
        """Create job from schedule with incorrect spelling of job in body.

        1) Create job from schedule using 'jb' in the body
        2) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        bad_body = {'jb': {'schedule_id': sch.id}}

        with self.assertRaises(BadRequest):
            self.images_provider.jobs_client. \
                create_job(sch.id, requestslib_kwargs={'data': bad_body})

    @attr('negative')
    def test_create_job_from_schedule_incorrect_schedule_id_spelling(self):
        """Create job from schedule with incorrect spelling of schedule_id in
        body.

        1) Create job from schedule using 'sch_id' in the body
        2) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        bad_param = {'job': {'sch_id': sch.id}}

        with self.assertRaises(BadRequest):
            self.images_provider.jobs_client. \
                create_job(sch.id, requestslib_kwargs={'data': bad_param})

    @attr('negative')
    def test_create_job_with_blank_schedule_id(self):
        """Create job using blank schedule id.

        1) Create job from schedule using a blank schedule id
        2) Verify job is not created and that a correct
            validation message is returned
        """

        sch_id = ''

        with self.assertRaises(ItemNotFound):
            self.images_provider.jobs_client.create_job(sch_id)

    @attr('negative')
    def test_create_job_for_non_existing_schedule_id(self):
        """Create job using non-existing schedule id.

        1) Create job from schedule using a non-existing schedule id
        2) Verify job is not created and that a correct
            validation message is returned
        """

        sch_id = '0'

        with self.assertRaises(ItemNotFound):
            self.images_provider.jobs_client.create_job(sch_id)

    @attr('negative')
    def test_create_job_from_schedule_using_letters_for_schedule_id(self):
        """Create job from schedule using letters for schedule id.

        1) Create job from schedule using letters for schedule id
        2) Verify job is not created and that a correct
            validation message is returned
        """

        sch_id = 'asdqwe'

        with self.assertRaises(ItemNotFound):
            self.images_provider.jobs_client.create_job(sch_id)

    @attr('negative')
    def test_create_job_from_schedule_using_special_chars_schedule_id(self):
        """Create job from schedule using letters for schedule id.

        1) Create job from schedule using special characters for schedule id
        2) Verify job is not created and that a correct
            validation message is returned
        """

        sch_id = '<'

        with self.assertRaises(ItemNotFound):
            self.images_provider.jobs_client.create_job(sch_id)
