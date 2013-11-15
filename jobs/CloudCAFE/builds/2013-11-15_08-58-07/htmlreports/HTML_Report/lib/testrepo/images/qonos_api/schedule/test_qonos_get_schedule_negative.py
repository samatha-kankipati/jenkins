from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute import ItemNotFound
from testrepo.common.testfixtures.images import BaseImagesFixture


class TestQonosGetScheduleNegative(BaseImagesFixture):

    @attr('negative')
    def test_get_schedule_with_blank_schedule_id(self):
        """Get details of schedule using blank schedule id.

        1) Get details of a schedule using a blank schedule id
        2) Verify that a correct validation message is returned
        """

        id = " "

        with self.assertRaises(ItemNotFound):
            self.images_provider.schedules_client. \
                get_schedule(id)

    @attr('negative')
    def test_get_schedule_for_non_existing_schedule_id(self):
        """Get details of schedule using non-existing schedule id.

        1) Get details of a schedule using a non-existing schedule id
        2) Verify that a correct validation message is returned
        """

        id = "0"

        with self.assertRaises(ItemNotFound):
            self.images_provider.schedules_client. \
                get_schedule(id)

    @attr('negative')
    def test_get_schedule_with_letters_for_schedule_id(self):
        """Get details of schedule using letters for schedule id.

        1) Get details of a schedule using letters for schedule id
        2) Verify that a correct validation message is returned
        """

        id = "abcd"

        with self.assertRaises(ItemNotFound):
            self.images_provider.schedules_client. \
                get_schedule(id)

    @attr('negative')
    def test_get_schedule_with_special_characters_for_schedule_id(self):
        """Get details of schedule using letters for schedule id.

        1) Get details of a schedule using special characters for schedule id
        2) Verify that a correct validation message is returned
        """

        id = "<&&/>"

        with self.assertRaises(ItemNotFound):
            self.images_provider.schedules_client. \
                get_schedule(id)

    @attr('negative')
    def test_get_schedule_with_numbers_and_special_chars_for_schedule_id(self):
        """Get details of schedule using numbers and special characters other
        than '-' for schedule id.

        1) Get details of a schedule using numbers and special characters other
            than '-' for schedule id
        2) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        id = sch_obj.entity.id.replace('-', '_')

        with self.assertRaises(ItemNotFound):
            self.images_provider.schedules_client. \
                get_schedule(id)

    @attr('negative')
    def test_get_schedule_using_invalid_schedule_id_format(self):
        """Get details of schedule using invalid schedule id format.

        1) Get details of a schedule using special characters for schedule id
        2) Verify that a correct validation message is returned
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        id = sch_obj.entity.id.replace('-', '')

        with self.assertRaises(ItemNotFound):
            self.images_provider.schedules_client. \
                get_schedule(id)
