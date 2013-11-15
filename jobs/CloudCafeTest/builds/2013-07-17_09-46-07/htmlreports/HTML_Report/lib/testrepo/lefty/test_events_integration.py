from ccengine.common.decorators import attr
from ccengine.common.tools.datagen import random_string
from testrepo.common.testfixtures.lefty import LeftyFixture


class EventsTest(LeftyFixture):

    @classmethod
    def setUpClass(cls):
        super(EventsTest, cls).setUpClass()

        cls.category_1 = cls.lefty_ticket_provider.\
            lefty_category_sub_category_client.\
            create_category(random_string("Test_Category_1_")).entity

        cls.category_2 = cls.lefty_ticket_provider.\
            lefty_category_sub_category_client.\
            create_category(random_string("Test_Category_2_")).entity

        cls.sub_category_2 = cls.lefty_ticket_provider.\
            lefty_category_sub_category_client.\
            create_sub_category(cls.category_2.category_id,
                                random_string("Test_SubCat_2_")).entity
        cls.sub_category_3 = cls.lefty_ticket_provider.\
            lefty_category_sub_category_client.\
            create_sub_category(cls.category_1.category_id,
                                random_string("Test_SubCat_4_")).entity

        cls.sub_category_1 = cls.lefty_ticket_provider.\
            lefty_category_sub_category_client.\
            create_sub_category(cls.category_1.category_id,
                                random_string("Test_SubCat_1_")).entity

        cls.first_ticket =\
            cls.lefty_ticket_provider.lefty_ticket_client.\
            create_ticket(cls.account_id, random_string("Test Ticket 1_"),
                          "Ticket for Automation Test",
                          cls.category_1.category_id,
                          cls.sub_category_1.sub_category_id).entity

    @attr(type='events')
    def test_fields_in_events_on_attribute_update(self):
        """
        Verify that when any attribute is updated there
        is an entry in events attribute

        """

        product_values = ["New Product"]
        update_ticket = self.lefty_ticket_provider.lefty_ticket_client.\
            update_ticket(
                self.account_id,
                self.first_ticket.ticket_id,
                products=product_values
            ).entity

        event_feed = self.lefty_ticket_provider.lefty_ticket_client.\
            search_events_by_attribute(
                update_ticket.events,
                "products", product_values
            )
        for attribute in self.attribute_list_on_events:
            self.assertTrue(hasattr(event_feed[0], attribute),
                            msg="The {0} attribute is not present".
                                format(attribute))
        self.assertTrue(hasattr(event_feed[0], "products"),
                        msg="The product attribute is not present in event")

    @attr(type='events')
    def test_fields_in_events_on_addition_of_comment(self):
        """
        Verify that when any comment is added there
        is an entry in events attribute

        """

        new_comment = random_string("Comment_")
        comment_list = []
        update_ticket = self.lefty_ticket_provider.\
            lefty_ticket_client.update_ticket(
                self.account_id,
                self.first_ticket.ticket_id,
                comment=new_comment
            ).entity

        event_feed = self.lefty_ticket_provider.lefty_ticket_client.\
            search_events_by_attribute(
                update_ticket.events,
                "on",
                update_ticket.last_updated
            )
        for attribute in self.attribute_list_on_events:
            self.assertTrue(hasattr(event_feed[0], attribute),
                            msg="The {0} attribute is not present".
                                format(attribute))

    @attr(type='events')
    def test_fields_in_events_on_updating_category_id(self):
        """
        Verify that when category id is updated,  there
        is an entry in events attribute with specific attributes

        """

        update_ticket = self.lefty_ticket_provider.\
            lefty_ticket_client.update_ticket(
                self.account_id,
                self.first_ticket.ticket_id,
                category_id=self.category_2.category_id,
                sub_category_id=self.sub_category_2.sub_category_id
            ).entity

        event_feed = self.lefty_ticket_provider.lefty_ticket_client.\
            search_events_by_attribute(
                update_ticket.events,
                "category_id",
                self.category_2.category_id
            )

        for attribute in self.attribute_list_on_events:
            self.assertTrue(hasattr(event_feed[0], attribute),
                            msg="The {0} attribute is not present".
                                format(attribute))

        self.assertTrue(hasattr(event_feed[0], "category_id"),
                        msg="Category_id attribute is not present in event")
        self.assertTrue(hasattr(event_feed[0], "sub_category_id"),
                        msg="sub_category_id attribute is \
                            not present in event")
        self.assertTrue(hasattr(event_feed[0], "category"),
                        msg="Category attribute is not present in event")
        self.assertTrue(hasattr(event_feed[0], "sub_category"),
                        msg="Subcategory attribute is not present in event")

        self.reset_first_ticket_with_tag = self.lefty_ticket_provider.\
            lefty_ticket_client.update_ticket(
                self.account_id,
                self.first_ticket.ticket_id,
                category_id=self.category_1.category_id,
                sub_category_id=self.sub_category_1.sub_category_id
            ).entity

    @attr(type='events')
    def test_fields_in_events_on_updating_sub_category_id(self):
        """
        Verify that when sub category id is updated,  there
        is an entry in events attribute with specific attributes

        """

        update_ticket = self.lefty_ticket_provider.\
            lefty_ticket_client.update_ticket(
                self.account_id,
                self.first_ticket.ticket_id,
                sub_category_id=self.sub_category_3.sub_category_id
            ).entity

        event_feed = self.lefty_ticket_provider.lefty_ticket_client.\
            search_events_by_attribute(
                update_ticket.events,
                "sub_category_id",
                self.sub_category_3.sub_category_id
            )
        for attribute in self.attribute_list_on_events:
            self.assertTrue(hasattr(event_feed[0], attribute),
                            msg="The {0} attribute is not present".
                                format(attribute))

        self.assertTrue(hasattr(event_feed[0], "sub_category_id"),
                        msg="sub_category_id attribute is \
                            not present in event")
        self.assertTrue(hasattr(event_feed[0], "sub_category"),
                        msg="Subcategory attribute is not present in event")

        self.reset_first_ticket_with_tag = self.lefty_ticket_provider.\
            lefty_ticket_client.update_ticket(
                self.account_id,
                self.first_ticket.ticket_id,
                sub_category_id=self.sub_category_1.sub_category_id
            ).entity

    @attr(type='events')
    def test_schema_of_the_event_generated_on_ticket_creation(self):
        """
        Verify that the schema of the event attribute inside a ticket
        details is same as expected.

        """

        event_feed = self.lefty_ticket_provider.lefty_ticket_client.\
            search_events_by_attribute(
                self.first_ticket.events,
                "on",
                self.first_ticket.created
            )
        for attribute in self.expected_event_feed_keys:
            self.assertTrue(hasattr(event_feed[0], attribute),
                            msg="The {0} attribute is not present".
                                format(attribute))

    @attr(type='events')
    def test_on_field_is_autopopulated_in_events_on_attribute_update(self):
        """
        Verify that when any attribute is updated for a ticket, the 'on'
        attribute in the generated event, is auto populated with the
        updated time

        """

        product_values = [random_string("New Product")]
        update_ticket = self.lefty_ticket_provider.lefty_ticket_client.\
            update_ticket(
                self.account_id,
                self.first_ticket.ticket_id,
                products=product_values
            ).entity
        event_feed = self.lefty_ticket_provider.lefty_ticket_client.\
            search_events_by_attribute(
                update_ticket.events,
                "products",
                product_values
            )
        self.assertEqual(event_feed[0].on,
                         update_ticket.last_updated,
                         msg="The 'on' field is not autopopulated with the\
                             updated time")

    @attr(type='events')
    def test_by_field_is_autopopulated_in_events_on_attribute_update(self):
        """
        Verify that when any attribute is updated for a ticket, the 'by'
        attribute in the generated event, is auto populated with the
        user name

        """

        product_values = [random_string("New Product")]
        update_ticket = self.lefty_ticket_provider.lefty_ticket_client.\
            update_ticket(
                self.account_id,
                self.first_ticket.ticket_id,
                products=product_values
            ).entity
        event_feed = self.lefty_ticket_provider.lefty_ticket_client.\
            search_events_by_attribute(
                update_ticket.events,
                "products",
                product_values
            )
        self.assertEqual(event_feed[0].by.get("value"),
                         self.user,
                         msg="The 'by' field is not autopopulated with the\
                             user name.")

    @attr(type='events')
    def test_ticket_id_is_autopopulated_in_events_on_attribute_update(self):
        """
        Verify that when any attribute is updated for a ticket, the
        'ticket_id' attribute in the generated event, is auto populated with
        the user name

        """

        product_values = [random_string("New Product")]
        update_ticket = self.lefty_ticket_provider.lefty_ticket_client.\
            update_ticket(
                self.account_id,
                self.first_ticket.ticket_id,
                products=product_values
            ).entity
        event_feed = self.lefty_ticket_provider.lefty_ticket_client.\
            search_events_by_attribute(
                update_ticket.events,
                "products",
                product_values
            )
        self.assertEqual(event_feed[0].ticket_id,
                         update_ticket.ticket_id,
                         msg="The 'ticket_id' field is not autopopulated with \
                             the user name.")
