from testrepo.common.testfixtures.images import BaseImagesFixture
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute import ItemNotFound


class TestQonosDeleteSchedule(BaseImagesFixture):

    @attr('positive')
    def test_delete_a_deleted_schedule(self):
        '''Delete a deleted schedule'''

        """
        1) Create a schedule
        2) Delete the schedule
        3) Verify that the response code is 200
        4) Delete the schedule again
        5) Verify that the response code 404 is returned
        6) Get the deleted schedule
        7) Verify that the response code is 404
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        msg = Constants.MESSAGE

        sch_obj = \
            self.images_provider.schedules_client.create_schedule(tenant,
                                                                  action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        del_sch_obj = \
            self.images_provider.schedules_client.delete_schedule(sch.id)
        self.assertEquals(del_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     del_sch_obj.status_code))

        with self.assertRaises(ItemNotFound):
            self.images_provider.schedules_client.delete_schedule(sch.id)

        with self.assertRaises(ItemNotFound):
            self.images_provider.schedules_client.get_schedule(sch.id)
