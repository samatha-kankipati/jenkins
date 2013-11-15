from testrepo.common.testfixtures.images import BaseImagesFixture
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute import BadRequest, ItemNotFound
import ccengine.common.tools.datagen as datagen


class TestQonosListScheduleMetadataNegative(BaseImagesFixture):

    @attr('negative')
    def test_list_schedule_metadata_method_mismatch(self):
        '''List schedule metadata with method mismatch'''

        """
        1) Attempt to request the base url of '/schedules/{id}/metadata' using
            a POST method
        2) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        key = self.config.images.metadata_key
        value = datagen.random_string(size=10)
        method = "POST"
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        keys = [key]
        values = [value]

        sch_metadata_obj = \
            self.images_provider.schedules_client.set_schedule_metadata(sch.id,
                                                                        keys,
                                                                        values)
        self.assertEquals(sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_metadata_obj.status_code))

        with self.assertRaises(BadRequest):
            self.images_provider.schedules_client. \
                list_schedule_metadata(sch.id,
                                       requestslib_kwargs={'method': method})

    @attr('negative')
    def test_list_schedule_metadata_incorrect_url(self):
        '''List schedule metadata using incorrect url'''

        """
        1) Attempt to request the base url of '/schedules/{id}/metadatas'
        2) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        key = self.config.images.metadata_key
        value = datagen.random_string(size=10)
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        keys = [key]
        values = [value]

        sch_metadata_obj = \
            self.images_provider.schedules_client.set_schedule_metadata(sch.id,
                                                                        keys,
                                                                        values)
        self.assertEquals(sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_metadata_obj.status_code))

        bad_url = "{0}/schedules/{0}/metadatas".format(self.config.images.url,
                                                       sch.id)

        with self.assertRaises(ItemNotFound):
            self.images_provider.schedules_client. \
                list_schedule_metadata(sch.id,
                                       requestslib_kwargs={'url': bad_url})

    @attr('negative')
    def test_list_schedule_metadata_with_blank_schedule_id(self):
        '''List schedule metadata using blank schedule id'''

        """
        1) List schedule metadata using a blank id
        2) Verify schedule metadata is not returned and that a correct
            validation message is returned
        """

        sch_id = ''

        with self.assertRaises(ItemNotFound):
            self.images_provider.schedules_client. \
                list_schedule_metadata(sch_id)

    @attr('negative')
    def test_list_schedule_metadata_for_non_existing_schedule_id(self):
        '''List schedule metadata for non-existing schedule id'''

        """
        1) List schedule metadata using a non-existing id
        2) Verify schedule metadata is not returned and that a correct
            validation message is returned
        """

        sch_id = '123'

        with self.assertRaises(ItemNotFound):
            self.images_provider.schedules_client. \
                list_schedule_metadata(sch_id)

    @attr('negative')
    def test_list_schedule_metadata_letters_for_schedule_id(self):
        '''List schedule metadata using letters for schedule id'''

        """
        1) List schedule metadata using letters for schedule id
        2) Verify schedule metadata is not returned and that a correct
            validation message is returned
        """

        sch_id = 'abcdef'

        with self.assertRaises(ItemNotFound):
            self.images_provider.schedules_client. \
                list_schedule_metadata(sch_id)

    @attr('negative')
    def test_list_schedule_metadata_special_characters_for_schedule_id(self):
        '''List schedule metadata using special characters for schedule id'''

        """
        1) List schedule metadata using special characters for schedule id
        2) Verify schedule metadata is not returned and that a correct
            validation message is returned
        """

        sch_id = '<>'

        with self.assertRaises(ItemNotFound):
            self.images_provider.schedules_client. \
                list_schedule_metadata(sch_id)
