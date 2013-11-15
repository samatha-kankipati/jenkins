import ccengine.common.tools.datagen as datagen
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
from testrepo.common.testfixtures.images import BaseImagesFixture


class TestQonosListScheduleMetadata(BaseImagesFixture):

    @attr('positive')
    def test_happy_path_list_schedule_metadata(self):
        """Happy Path - List schedule metadata.

        1) Create a schedule
        2) Create schedule metadata
        3) Create another schedule metadata for that schedule
        4) List schedule metadata
        5) Verify that the response code is 200
        6) Verify that the length of the schedule metadata is 2
        7) Verify that the schedule metadata is as expected
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        key = self.config.images.metadata_key
        alt_key = self.config.images.alt_metadata_key
        value = datagen.random_string(size=10)
        alt_value = datagen.random_string(size=10)
        count = 2
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

        keys = [key, alt_key]
        values = [value, alt_value]

        new_metadata_obj = \
            self.images_provider.schedules_client.set_schedule_metadata(sch.id,
                                                                        keys,
                                                                        values)
        self.assertEquals(new_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     new_metadata_obj.status_code))

        list_sch_metadata_obj = self.images_provider.schedules_client.\
            list_schedule_metadata(sch.id)
        self.assertEquals(list_sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_sch_metadata_obj.status_code))
        self.assertEqual(len(list_sch_metadata_obj.entity), count,
                         msg.format("length of the list", count,
                                    len(list_sch_metadata_obj.entity)))

        list_sch_metadata = list_sch_metadata_obj.entity

        for metadata_key, metadata_value in list_sch_metadata.items():
            if metadata_key == key:
                self.assertEquals(metadata_value, value,
                                  msg.format('value', value, metadata_value))
            elif metadata_key == alt_key:
                self.assertEquals(metadata_value, alt_value,
                                  msg.format('alt_value', alt_value,
                                             metadata_value))
            else:
                self.assertEquals(metadata_key, key,
                                  msg.format('key', key, metadata_key))
                self.assertEquals(metadata_key, alt_key,
                                  msg.format('key', alt_key, metadata_key))

    @attr('positive')
    def test_list_schedule_metadata_with_empty_schedule_metadata(self):
        """List schedule metadata with empty schedule metadata.

        1) Create a schedule without schedule metadata
        2) List schedule metadata
        3) Verify that the response code is 200
        4) Verify that the length of the schedule metadata is 0
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        count = 0
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        list_sch_metadata_obj = self.images_provider.schedules_client.\
            list_schedule_metadata(sch.id)
        self.assertEquals(list_sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_sch_metadata_obj.status_code))
        self.assertEquals(len(list_sch_metadata_obj.entity), count,
                          msg.format("length of the list", count,
                                     len(list_sch_metadata_obj.entity)))
