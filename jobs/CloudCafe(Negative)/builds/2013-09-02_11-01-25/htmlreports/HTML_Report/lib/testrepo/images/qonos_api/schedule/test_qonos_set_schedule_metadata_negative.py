from testrepo.common.testfixtures.images import BaseImagesFixture
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute \
    import ItemNotFound, BadRequest, InternalServerError
from ccengine.common.constants.images_constants import Constants
import ccengine.common.tools.datagen as datagen


class TestQonosSetScheduleMetadataNegative(BaseImagesFixture):

    @attr('negative')
    def test_set_schedule_metadata_method_mismatch(self):
        '''Set schedule metadata with method mismatch'''

        """
        1) Attempt to request the base url of '/schedules/{id}/metadata' using
            POST method
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

        with self.assertRaises(ItemNotFound):
            self.images_provider.schedules_client. \
                set_schedule_metadata(sch.id, keys, values, http_method="POST")

    @attr('negative')
    def test_set_schedule_metadata_incorrect_url(self):
        '''Set schedule metadata with incorrect url'''

        """
        1) Attempt to request the base url of '/schedules/{id}/metadat'
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

        with self.assertRaises(ItemNotFound):
            self.images_provider.schedules_client. \
                set_schedule_metadata(sch.id, keys, values, sub_url="metadat")

    @attr('negative')
    def test_set_schedule_metadata_incorrect_spelling_of_meta_in_body(self):
        '''Request incorrect spelling of meta in the body'''

        """
        1) Set scheduled metadata using 'metadat' in the body
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

        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client. \
                set_schedule_metadata(sch.id, keys, values, bad_body="metadat")

    @attr('negative')
    def test_set_schedule_metadata_incorrect_format_in_body(self):
        '''Request incorrect format in the body'''

        """
        1) Set scheduled metadata using incorrect format in the body
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

        with self.assertRaises(InternalServerError):
            self.images_provider.schedules_client. \
                set_schedule_metadata(sch.id, keys, values,
                                      bad_body="metadata:")

    @attr('negative')
    def test_set_schedule_metadata_with_blank_id(self):
        '''Set schedule metadata using a blank id'''

        """
        1) Set schedule metadata using a blank id
        2) Verify that a correct validation message is returned
        """

        key = self.config.images.metadata_key
        value = datagen.random_string(size=10)
        sch_id = ""

        keys = [key]
        values = [value]

        with self.assertRaises(BadRequest):
            self.images_provider.schedules_client. \
                set_schedule_metadata(sch_id, keys, values)

    @attr('negative')
    def test_set_schedule_metadata_using_non_existing_id(self):
        '''Set schedule metadata using a non-existing id'''

        """
        1) Set schedule metadata using a non-existing id
        2) Verify that a correct validation message is returned
        """

        sch_id = "1111"
        key = self.config.images.metadata_key
        value = datagen.random_string(size=10)

        keys = [key]
        values = [value]

        with self.assertRaises(ItemNotFound):
            self.images_provider.schedules_client. \
                set_schedule_metadata(sch_id, keys, values)

    @attr('negative')
    def test_set_schedule_metadata_using_letters_for_id(self):
        '''Set schedule metadata using letters for id'''

        """
        1) Set schedule metadata using letters for id
        2) Verify that a correct validation message is returned
        """

        sch_id = "abc"
        key = self.config.images.metadata_key
        value = datagen.random_string(size=10)

        keys = [key]
        values = [value]

        with self.assertRaises(ItemNotFound):
            self.images_provider.schedules_client. \
                set_schedule_metadata(sch_id, keys, values)

    @attr('negative')
    def test_set_schedule_metadata_using_special_characters_for_id(self):
        '''Set schedule metadata using special characters for id'''

        """
        1) Set schedule metadata using special characters for id
        2) Verify that a correct validation message is returned
        """

        sch_id = "<&&/>"
        key = self.config.images.metadata_key
        value = datagen.random_string(size=10)

        keys = [key]
        values = [value]

        with self.assertRaises(ItemNotFound):
            self.images_provider.schedules_client. \
                set_schedule_metadata(sch_id, keys, values)

    @attr('negative')
    def test_set_schedule_metadata_using_special_characters_for_key(self):
        '''Set schedule metadata using special characters for key'''

        """
        1) Set schedule metadata using special characters for key
        2) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        key = "<&&/>"
        value = datagen.random_string(size=10)
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        keys = [key]
        values = [value]

        '''TODO: This will fail with bug 221# is fixed'''
        self.images_provider.schedules_client. \
            set_schedule_metadata(sch.id, keys, values)

    @attr('negative')
    def test_set_schedule_metadata_using_special_characters_for_value(self):
        '''Set schedule metadata using special characters for value'''

        """
        1) Set schedule metadata using special characters for value
        2) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        key = self.config.images.metadata_key
        value = "<&&/>"
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        keys = [key]
        values = [value]

        '''TODO: This will fail with bug 220# is fixed'''
        self.images_provider.schedules_client. \
            set_schedule_metadata(sch.id, keys, values)

    @attr('negative')
    def test_set_schedule_metadata_using_blank_key(self):
        '''Set schedule metadata using blank key'''

        """
        1) Set schedule metadata using blank key
        2) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        key = ""
        value = datagen.random_string(size=10)
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        keys = [key]
        values = [value]

        '''TODO: This will fail with bug 219# is fixed'''
        self.images_provider.schedules_client. \
            set_schedule_metadata(sch.id, keys, values)

    @attr('negative')
    def test_set_schedule_metadata_for_deleted_schedule(self):
        '''Set schedule metadata for deleted schedule'''

        """
        1) Create a schedule with schedule metadata
        2) Delete the schedule
        3) Set the schedule metadata
        4) Verify that a correct validation message is returned
        """
        tenant = self.config.images.tenant
        action = self.config.images.action
        key = self.config.images.metadata_key
        value = datagen.random_string(0, 10000)
        msg = Constants.MESSAGE

        metadata = {key: value}
        sch_obj = self.images_provider.\
                    create_active_schedules(tenant, action, metadata=metadata)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        del_sch_obj = self.images_provider.schedules_client.\
            delete_schedule(id=sch.id)
        self.assertEquals(del_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     del_sch_obj.status_code))
        keys = [key]
        values = [value]

        with self.assertRaises(ItemNotFound):
            self.images_provider.schedules_client. \
                set_schedule_metadata(sch.id, keys, values)
