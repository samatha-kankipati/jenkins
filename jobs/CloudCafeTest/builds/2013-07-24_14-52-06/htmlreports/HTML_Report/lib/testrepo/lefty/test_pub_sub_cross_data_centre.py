import time

from ccengine.common.decorators import attr
from testrepo.common.testfixtures.lefty import LeftyFixture
from ccengine.common.tools.datagen import random_string
from ccengine.common.tools.equality_tools import EqualityTools


class PubSubCrossDataCentreTest(LeftyFixture):

    @classmethod
    def setUpClass(cls):
        super(PubSubCrossDataCentreTest, cls).setUpClass()
        cls.category_1 = cls.lefty_ticket_provider.\
            lefty_category_sub_category_client.\
            create_category(random_string("Test_Category_1_")).entity

        cls.sub_category_1 = cls.lefty_ticket_provider.\
            lefty_category_sub_category_client.\
            create_sub_category(cls.category_1.category_id,
                                random_string("Test_SubCat_1_")).entity

        cls.first_ticket =\
            cls.lefty_ticket_provider.lefty_ticket_client.create_ticket(
                cls.account_id,
                "Test Ticket 1",
                "Ticket for Automation Test",
                cls.category_1.category_id,
                cls.sub_category_1.sub_category_id
            ).entity

    def test_update_attribute_in_subscribe(self):
        """
           Update the individual attributes and verify that the event shows up
           in PubSub Subscribe event list.
        """

        test_attribute = self.update_attr.keys()[0]
        test_value = self.update_attr[test_attribute]

        update_resp = self.lefty_ticket_provider.lefty_ticket_client.\
            update_ticket(
                self.account_id,
                self.first_ticket.ticket_id,
                **self.update_attr
            ).entity

        #this sleep is needed to wait for sometime till the data centres sync
        time.sleep(30)

        events = self.lefty_ticket_provider.pubsub_client_alt.\
            search_events_by_attribute(
                "ticket.ticket_id",
                self.first_ticket.ticket_id,
                update_resp.last_updated
            )

        last_event = events[len(events) - 1]

        msg_no_update = ('The event captured does not have the updated'
                         ' ticket: {0},  the ticket got captured is: {1}')

        self.assertEqual(
            update_resp,
            last_event.ticket,
            msg=msg_no_update.format(update_resp, last_event.ticket))

        for attribute in self.attribute_list_on_pub_sub_events:
            self.assertTrue(
                hasattr(last_event.update, attribute),
                msg="The {0} attribute is not present".format(attribute)
            )

        msg_update_pubsub = \
            "The updated {0} is not reflected in the pubsub event"

        expected_value = test_value

        attribute_value_from_event = getattr(last_event.update, test_attribute)

        if hasattr(self, "fetch_value_from_dict_with_key"):
            if test_attribute == 'recipients':
                actual_value = attribute_value_from_event[0].\
                    get(self.fetch_value_from_dict_with_key)
                expected_value = test_value[0]
            else:
                actual_value = attribute_value_from_event.\
                    get(self.fetch_value_from_dict_with_key)
        else:
            actual_value = attribute_value_from_event

        self.assertEqual(
            expected_value,
            actual_value,
            msg=msg_update_pubsub.format(test_attribute)
        )
