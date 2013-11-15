import time

from ccengine.common.decorators import attr
from testrepo.common.testfixtures.lefty import LeftyFixture
from ccengine.common.tools.datagen import random_string
from ccengine.common.tools.datatools import are_datetimestrings_equal
from ccengine.common.tools.equality_tools import EqualityTools


class CrossDataCentreIntegrationTest(LeftyFixture):

    @classmethod
    def setUpClass(cls):
        super(CrossDataCentreIntegrationTest, cls).setUpClass()
        cls.category_1 = cls.lefty_ticket_provider.\
            lefty_category_sub_category_client.\
            create_category(random_string("Test_Category_1_")).entity

        cls.sub_category_1 = cls.lefty_ticket_provider.\
            lefty_category_sub_category_client.\
            create_sub_category(cls.category_1.category_id,
                                random_string("Test_SubCat_1_")).entity

        cls.sub_category_2 = cls.lefty_ticket_provider.\
            lefty_category_sub_category_client.\
            create_sub_category(cls.category_1.category_id,
                                random_string("Test_SubCat_2_")).entity

        cls.category_2 = cls.lefty_ticket_provider.\
            lefty_category_sub_category_client.\
            create_category(random_string("Test_Category_1_")).entity

        cls.my_tags = [random_string("my_tag_")]

        cls.queue_1 = cls.lefty_ticket_provider.lefty_queue_client.\
            create_queue(random_string("User Queue 1_"),
                         description="Queue To Be Deleted",
                         query_occurrence="must",
                         query_type="match", query_property="tags",
                         query_text=cls.my_tags[0], sort_property="priority",
                         sort_order="desc").entity

        cls.first_ticket =\
            cls.lefty_ticket_provider.lefty_ticket_client.\
            create_ticket(cls.account_id, "Test Ticket 1",
                          "Ticket for Automation Test",
                          cls.category_1.category_id,
                          cls.sub_category_1.sub_category_id).entity

        cls.second_ticket =\
            cls.lefty_ticket_provider.lefty_ticket_client.\
            create_ticket(cls.account_id, "Test Ticket 2",
                          "Ticket for Automation Test",
                          cls.category_1.category_id,
                          cls.sub_category_1.sub_category_id).entity

        cls.queue_2 = cls.lefty_ticket_provider.lefty_queue_client.\
            create_queue(random_string("User Queue 2_"),
                         description="Queue To Be Updated",
                         query_occurrence="must",
                         query_type="match", query_property="tags",
                         query_text=cls.my_tags[0], sort_property="priority",
                         sort_order="desc").entity

    @attr(type='cross_data_centre')
    def test_create_ticket_and_verify_in_other_data_centre(self):
        """
            @summary: Verify that when a Ticket is created in One data centre,
            the Ticket is visible to Other data centres
        """
        new_ticket =\
            self.lefty_ticket_provider.lefty_ticket_client.\
            create_ticket(self.account_id, "Test Ticket 1",
                          "Ticket for Automation Test",
                          self.category_1.category_id,
                          self.sub_category_1.sub_category_id).entity

        self.lefty_ticket_provider.lefty_ticket_client.\
            wait_for_ticket_to_sync_in_data_centre(
                self.base_url_alt,
                new_ticket.last_updated,
                account_id=self.account_id,
                ticket_id=new_ticket.ticket_id
            )
        retrieved_ticket_from_other_data_centre = \
            self.lefty_ticket_provider.lefty_ticket_client.\
            get_ticket(
                self.account_id,
                new_ticket.ticket_id,
                data_centre_url=self.base_url_alt
            ).entity

        self.assertEqual(new_ticket, retrieved_ticket_from_other_data_centre,
                         msg="The ticket {0} is not visible in other"
                             "data centre".format(new_ticket))

    @attr(type='cross_data_centre')
    def test_create_queue_and_verify_in_other_data_centre(self):
        """
            @summary: Verify that when a Queue is created in One data centre,
            the Queue is visible to Other data centres
        """
        my_tags = [random_string("my_tag_")]
        my_queue = self.lefty_ticket_provider.lefty_queue_client.\
            create_queue(random_string("User Queue 1_"),
                         description="My Queue",
                         query_occurrence="must",
                         query_type="match", query_property="tags",
                         query_text=my_tags[0], sort_property="priority",
                         sort_order="desc").entity

        #time to sync across data centres
        time.sleep(self.sync_wait_time)

        retrieved_queue_from_other_data_centre = \
            self.lefty_ticket_provider.lefty_queue_client.\
            get_queue(
                my_queue.queue_id,
                data_centre_url=self.base_url_alt
            ).entity

        self.assertTrue(EqualityTools.
                        are_objects_equal(
                            my_queue,
                            retrieved_queue_from_other_data_centre,
                            keys_to_exclude=["last_updated", "created"]
                        ),
                        msg="The Queue {0} is not visible in other data centre"
                            .format(my_queue))

        self.assertTrue(
            are_datetimestrings_equal(
                my_queue.last_updated,
                retrieved_queue_from_other_data_centre.last_updated,
                leeway=1), msg="The last updated time does not match")

        self.assertTrue(
            are_datetimestrings_equal(
                my_queue.created,
                retrieved_queue_from_other_data_centre.created,
                leeway=1), msg="The created time does not match")

    @attr(type='cross_data_centre')
    def test_create_category_and_verify_in_other_data_centre(self):
        """
            @summary: Verify that when a Category is created in One data centre
            the Category is visible to Other data centres
        """

        new_category = self.lefty_ticket_provider.\
            lefty_category_sub_category_client.\
            create_category(random_string("Test_Category_1_")).entity

        #time to sync across data centres
        time.sleep(self.sync_wait_time)

        retrieved_category_from_other_data_centre = \
            self.lefty_ticket_provider.lefty_category_sub_category_client.\
            get_category(
                new_category.category_id,
                data_centre_url=self.base_url_alt
            ).entity

        self.assertEqual(new_category,
                         retrieved_category_from_other_data_centre,
                         msg="The Category {0} is not visible in other"
                             "data centre".format(new_category))

    @attr(type='cross_data_centre')
    def test_create_sub_category_and_verify_in_other_data_centre(self):
        """
            @summary: Verify that when a SubCategory is created in
            One data centre, the SubCategory is visible to Other data centres
        """

        new_sub_category = self.lefty_ticket_provider.\
            lefty_category_sub_category_client.\
            create_sub_category(self.category_1.category_id,
                                random_string("Test_SubCat_New_")).entity

        #time to sync across data centres
        time.sleep(self.sync_wait_time)

        retrieved_sub_category_from_other_data_centre = \
            self.lefty_ticket_provider.lefty_category_sub_category_client.\
            get_sub_category(
                self.category_1.category_id,
                new_sub_category.sub_category_id,
                data_centre_url=self.base_url_alt).entity

        self.assertEqual(new_sub_category,
                         retrieved_sub_category_from_other_data_centre,
                         msg="The Sub_Category {0} is not visible in other"
                             "data centre".format(new_sub_category))

    @attr(type='cross_data_centre')
    def test_delete_sub_category_and_verify_in_other_data_centre(self):
        """
            @summary: Verify that when a SubCategory is deleted in
            One data centre, the SubCategory is not visible to
            Other data centres
        """

        delete_sub_category = self.lefty_ticket_provider.\
            lefty_category_sub_category_client.\
            delete_sub_category(self.category_1.category_id,
                                self.sub_category_2.sub_category_id).entity

        #time to sync across data centres
        time.sleep(self.sync_wait_time)

        retrieved_from_other_data_centre = \
            self.lefty_ticket_provider.lefty_category_sub_category_client.\
            get_sub_category(
                self.category_1.category_id,
                self.sub_category_2.sub_category_id,
                data_centre_url=self.base_url_alt)

        self.assertEqual(self.NOT_FOUND[0],
                         str(retrieved_from_other_data_centre.status_code),
                         msg="The Sub_Category {0} is visible in other"
                             "data centre".format(self.sub_category_2))

    @attr(type='cross_data_centre')
    def test_delete_category_and_verify_in_other_data_centre(self):
        """
            @summary: Verify that when a Category is deleted in
            One data centre, the Category is not visible to Other data centres
        """

        delete_category = self.lefty_ticket_provider.\
            lefty_category_sub_category_client.\
            delete_category(self.category_2.category_id)

        #time to sync across data centres
        time.sleep(self.sync_wait_time)

        retrieved_from_other_data_centre = \
            self.lefty_ticket_provider.lefty_category_sub_category_client.\
            get_category(
                self.category_2.category_id,
                data_centre_url=self.base_url_alt
            )

        self.assertEqual(self.NOT_FOUND[0],
                         str(retrieved_from_other_data_centre.status_code),
                         msg="The Category {0} is visible in other"
                             "data centre".format(self.category_2))

    @attr(type='cross_data_centre')
    def test_delete_queue_and_verify_in_other_data_centre(self):
        """
            @summary: Verify that when a Queue is deleted in
            One data centre, the Queue is not visible to Other data centres
        """

        delete_queue = self.lefty_ticket_provider.lefty_queue_client.\
            delete_queue(self.queue_1.queue_id)

        #time to sync across data centres
        time.sleep(self.sync_wait_time)

        retrieved_from_other_data_centre = \
            self.lefty_ticket_provider.lefty_queue_client.\
            get_queue(
                self.queue_1.queue_id,
                data_centre_url=self.base_url_alt
            )

        self.assertEqual(self.NOT_FOUND[0],
                         str(retrieved_from_other_data_centre.status_code),
                         msg="The Queue {0} is visible in other"
                             "data centre".format(self.category_2))

    @attr(type='cross_data_centre')
    def test_update_ticket_and_verify_in_other_data_centre(self):
        """
            @summary: Verify that when a Ticket is updated in
            One data centre, the Ticket is updated in Other data centres
        """

        new_priority = "High"
        update_resp = self.lefty_ticket_provider.\
            lefty_ticket_client.\
            update_ticket(self.account_id, self.second_ticket.ticket_id,
                          priority=new_priority).entity

        self.lefty_ticket_provider.lefty_ticket_client.\
            wait_for_ticket_to_sync_in_data_centre(
                self.base_url_alt,
                update_resp.last_updated,
                account_id=self.account_id,
                ticket_id=self.second_ticket.ticket_id
            )

        retrieved_ticket_from_other_data_centre = \
            self.lefty_ticket_provider.lefty_ticket_client.\
            get_ticket(
                self.account_id,
                self.second_ticket.ticket_id,
                data_centre_url=self.base_url_alt
            ).entity

        self.assertEqual(update_resp.priority,
                         retrieved_ticket_from_other_data_centre.priority,
                         msg="The ticket {0} is not updated in other"
                             "data centre".format(self.second_ticket))

    @attr(type='cross_data_centre')
    def test_update_ticket_and_verify_event_in_other_data_centre(self):
        """
            @summary: Verify when a ticket is updated in one data centre, the
            "event" attribute gets updated accordingly in other data centres.
        """

        product_values = self.products
        update_ticket = self.lefty_ticket_provider.lefty_ticket_client.\
            update_ticket(
                self.account_id,
                self.first_ticket.ticket_id,
                products=product_values
            ).entity

        self.lefty_ticket_provider.lefty_ticket_client.\
            wait_for_ticket_to_sync_in_data_centre(
                self.base_url_alt,
                update_ticket.last_updated,
                account_id=self.account_id,
                ticket_id=self.first_ticket.ticket_id
            )

        retrieved_ticket_from_other_data_centre = \
            self.lefty_ticket_provider.lefty_ticket_client.\
            get_ticket(
                self.account_id,
                self.first_ticket.ticket_id,
                data_centre_url=self.base_url_alt
            ).entity

        event_feed = self.lefty_ticket_provider.lefty_ticket_client.\
            search_events_by_attribute(
                retrieved_ticket_from_other_data_centre.events,
                "products", product_values
            )
        self.assertTrue(len(event_feed) is not 0,
                        msg="The event is not found in other data centre")
