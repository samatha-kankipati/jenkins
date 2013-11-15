from ccengine.common.decorators import attr
from testrepo.common.testfixtures.lefty import LeftyFixture
from ccengine.common.tools.datagen import random_string
from ccengine.common.tools.equality_tools import EqualityTools


class PubSubTest(LeftyFixture):

    @classmethod
    def setUpClass(cls):
        super(PubSubTest, cls).setUpClass()
        cls.category_1 = cls.lefty_ticket_provider.\
            lefty_category_sub_category_client.\
            create_category(random_string("Test_Category_1_")).entity

        cls.sub_category_1 = cls.lefty_ticket_provider.\
            lefty_category_sub_category_client.\
            create_sub_category(cls.category_1.category_id,
                                random_string("Test_SubCat_1_")).entity

        cls.category_2 = cls.lefty_ticket_provider.\
            lefty_category_sub_category_client.\
            create_category(random_string("Test_Category_2_")).entity

        cls.sub_category_2 = cls.lefty_ticket_provider.\
            lefty_category_sub_category_client.\
            create_sub_category(cls.category_2.category_id,
                                random_string("Test_SubCat_2_")).entity

        cls.sub_category_3 = cls.lefty_ticket_provider.\
            lefty_category_sub_category_client.\
            create_sub_category(cls.category_2.category_id,
                                random_string("Test_SubCat_3_")).entity

        cls.first_ticket =\
            cls.lefty_ticket_provider.lefty_ticket_client.create_ticket(
                cls.account_id,
                "Test Ticket 1",
                "Ticket for Automation Test",
                cls.category_1.category_id,
                cls.sub_category_1.sub_category_id
            ).entity

        cls.second_ticket =\
            cls.lefty_ticket_provider.lefty_ticket_client.create_ticket(
                cls.account_id,
                "Test Ticket 2",
                "Ticket for Automation Test",
                cls.category_2.category_id,
                cls.sub_category_2.sub_category_id
            ).entity

        cls.third_ticket =\
            cls.lefty_ticket_provider.lefty_ticket_client.create_ticket(
                cls.account_id,
                "Test Ticket 3",
                "Ticket for Automation Test",
                cls.category_2.category_id,
                cls.sub_category_2.sub_category_id
            ).entity

    @attr(type='pub_sub')
    def test_update_rating_has_event_in_subscribe(self):
        '''
            Update the rating and verify that the event shows up in PubSub
            Subscribe event list.
        '''
        attributes = {"rating": "Highest"}
        self.update_attribute_in_subscribe(**attributes)

    @attr(type='pub_sub')
    def test_update_assignee_has_event_in_subscribe(self):
        '''
            Update the assignee and verify that the event shows up in PubSub
            Subscribe event list.
        '''
        attributes = {"assignee": self.user}
        self.update_attribute_in_subscribe(dict_key="value", **attributes)

    @attr(type='pub_sub')
    def test_update_subject_has_event_in_subscribe(self):
        '''
            Update the subject and verify that the event shows up in PubSub
            Subscribe event list.
        '''
        attributes = {"subject": "Updated Subject"}
        self.update_attribute_in_subscribe(**attributes)

    @attr(type='pub_sub')
    def test_update_description_has_event_in_subscribe(self):
        '''
            Update the description and verify that the event shows up in PubSub
            Subscribe event list.
        '''
        attributes = {"description": "Updated Description"}
        self.update_attribute_in_subscribe(**attributes)

    @attr(type='pub_sub')
    def test_update_priority_has_event_in_subscribe(self):
        '''
            Update the priority and verify that the event shows up in PubSub
            Subscribe event list.
        '''
        attributes = {"priority": "High"}
        self.update_attribute_in_subscribe(**attributes)

    @attr(type='pub_sub')
    def test_add_comment_has_event_in_subscribe(self):
        '''
            Add a comment and verify that the event shows up in PubSub
            Subscribe event list.
        '''
        attributes = {"comment": random_string("Comment_")}
        self.update_attribute_in_subscribe(dict_key="text", **attributes)

    @attr(type='pub_sub')
    def test_update_group_has_event_in_subscribe(self):
        '''
            Update the group and verify that the event shows up in PubSub
            Subscribe event list.
        '''
        attributes = {"group": "Cloud_Group"}
        self.update_attribute_in_subscribe(**attributes)

    @attr(type='pub_sub')
    def test_update_product_has_event_in_subscribe(self):
        '''
            Update the product and verify that the event shows up in PubSub
            Subscribe event list.
        '''
        new_products = [random_string("Product_"), random_string("Product_")]
        attributes = {"products": new_products}
        self.update_attribute_in_subscribe(**attributes)

    @attr(type='pub_sub')
    def test_update_receipents_has_event_in_subscribe(self):
        '''
            Update the receipents and verify that the event shows up in PubSub
            Subscribe event list.
        '''
        new_recipients = [self.user]
        attributes = {"recipients": new_recipients}
        self.update_attribute_in_subscribe(dict_key="value", **attributes)

    @attr(type='pub_sub')
    def test_update_status_has_event_in_subscribe(self):
        '''
            Update the status and verify that the event shows up in PubSub
            Subscribe event list.
        '''
        new_status = "In Progress"
        attributes = {"status": new_status}
        self.update_attribute_in_subscribe(**attributes)

    @attr(type='pub_sub')
    def test_update_difficulty_has_event_in_subscribe(self):
        '''
            Update the difficulty and verify that the event shows up in PubSub
            Subscribe event list.
        '''
        new_difficulty = "Level 2"
        attributes = {"difficulty": new_difficulty}
        self.update_attribute_in_subscribe(**attributes)

    @attr(type='pub_sub')
    def test_update_severity_has_event_in_subscribe(self):
        '''
            Update the severity and verify that the event shows up in PubSub
            Subscribe event list.
        '''
        new_severity = "Urgent"
        attributes = {"severity": new_severity}
        self.update_attribute_in_subscribe(**attributes)

    @attr(type='pub_sub')
    def test_update_tag_has_event_in_subscribe(self):
        '''
            Update the tag and verify that the event shows up in PubSub
            Subscribe event list.
        '''
        new_tags = [random_string("Tag_"), random_string("Tag_")]
        attributes = {"tags": new_tags}
        self.update_attribute_in_subscribe(**attributes)

    @attr(type='pub_sub')
    def test_update_category_has_event_in_subscribe(self):
        '''
            Update the category and verify that the event shows up in PubSub
            Subscribe event list.
        '''
        attributes = {"category_id": self.category_1.category_id,
                      "sub_category_id": self.sub_category_1.sub_category_id}
        self.update_attribute_in_subscribe(
            ticket_obj=self.second_ticket,
            **attributes
        )

    @attr(type='pub_sub')
    def test_update_sub_category_has_event_in_subscribe(self):
        '''
            Update the Subcategory and verify that the event shows up in PubSub
            Subscribe event list.
        '''
        attributes = {"sub_category_id": self.sub_category_3.sub_category_id,
                      "category_id": self.category_2.category_id}
        self.update_attribute_in_subscribe(
            ticket_obj=self.third_ticket,
            **attributes
        )

    def update_attribute_in_subscribe(self, ticket_obj=None,
                                      dict_key=None, **kwargs):
        """
        @summary: Performs some common actions and asserts
        @param name: ticket_obj
        @param desc: Ticket on which the actions will be performed
        @param type: <Ticket Object>
        @param name: dict_key
        @param desc: If the expected value is a dict, use this dict_key to
                     fetch a specific value as expected result in assertion
        @param type: String
        """

        if ticket_obj is None:
            ticket_obj = self.first_ticket

        test_attribute = kwargs.keys()[0]
        test_value = kwargs[test_attribute]

        update_resp = self.lefty_ticket_provider.lefty_ticket_client.\
            update_ticket(
                self.account_id,
                ticket_obj.ticket_id,
                **kwargs
            ).entity

        events = self.lefty_ticket_provider.pubsub_client.\
            search_events_by_attribute(
                "ticket.ticket_id",
                ticket_obj.ticket_id,
                ticket_obj.last_updated
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

        expected_value = getattr(last_event.update, test_attribute)
        actual_value = test_value

        if type(expected_value) is dict:
            expected_value = expected_value.get(dict_key)

        if test_attribute == 'recipients':
            expected_value = expected_value[0].get(dict_key)
            actual_value = test_value[0]

        self.assertEqual(
            expected_value,
            actual_value,
            msg=msg_update_pubsub.format(test_attribute)
        )
