from ccengine.common.decorators import attr
from ccengine.common.tools.datagen import random_string
from testrepo.common.testfixtures.lefty import LeftyFixture


class StatusesTest(LeftyFixture):

    @attr(type='status')
    def test_fetching_all_statuses(self):
        """Verify trying to fetch all the statuses provides a 200 response
        and retrieves all the available status"""

        status_list = \
            self.lefty_ticket_provider.lefty_status_client.get_statuses()

        self.assertEqual(status_list.status_code, eval(self.OK_CODE[0]),
                         msg="The status code is {0} instead of {1}".
                             format(status_list.status_code, self.OK_CODE[0]))
        self.assertFalse(not status_list.entity.statuses,
                         msg="The status list is empty")
