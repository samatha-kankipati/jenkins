from ccengine.common.decorators import attr
from testrepo.common.testfixtures.lefty import LeftyFixture
from ccengine.common.tools.datagen import random_string


class QueueUpdateTest(LeftyFixture):

    @classmethod
    def setUpClass(cls):
        super(QueueUpdateTest, cls).setUpClass()

        cls.category_1 = cls.lefty_ticket_provider.\
            lefty_category_sub_category_client.\
            create_category(random_string("Test_Category_1_")).entity

        cls.category_2 = cls.lefty_ticket_provider.\
            lefty_category_sub_category_client.\
            create_category(random_string("Test_Category_2_")).entity

        cls.sub_category_1 = cls.lefty_ticket_provider.\
            lefty_category_sub_category_client.\
            create_sub_category(cls.category_1.category_id,
                                random_string("Test_SubCat_1_")).entity

        cls.sub_category_2 = cls.lefty_ticket_provider.\
            lefty_category_sub_category_client.\
            create_sub_category(cls.category_2.category_id,
                                random_string("Test_SubCat_2_")).entity

        cls.sub_category_3 = cls.lefty_ticket_provider.\
            lefty_category_sub_category_client.\
            create_sub_category(cls.category_1.category_id,
                                random_string("Test_SubCat_3_")).entity

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
                          cls.category_2.category_id,
                          cls.sub_category_2.sub_category_id).entity

        cls.my_tags = [random_string("my_tag_")]

        cls.my_queue = cls.lefty_ticket_provider.lefty_queue_client.\
            create_queue(random_string("User Queue 1_"),
                         description="My Queue",
                         query_occurrence="must",
                         query_property="tags",
                         query_value=cls.my_tags, sort_property="priority",
                         sort_order="desc").entity

        cls.first_ticket_with_tag = cls.lefty_ticket_provider.\
            lefty_ticket_client.update_ticket(cls.account_id,
                                              cls.first_ticket.ticket_id,
                                              tags=cls.my_tags).entity

        cls.second_ticket_with_tag = cls.lefty_ticket_provider.\
            lefty_ticket_client.update_ticket(cls.account_id,
                                              cls.second_ticket.ticket_id,
                                              tags=cls.my_tags).entity

    @attr(type='update_queue')
    def test_queue_contains_tickets_according_to_property(self):
        """A queue should contain tickets according to the property\
        provided while creation of the Queue"""

        retrieve_tickets_queue = self.lefty_ticket_provider.\
            lefty_queue_client.\
            get_tickets_for_a_queue(self.my_queue.queue_id).entity

        self.assertEqual(len(retrieve_tickets_queue.tickets), 2,
                         msg="Tickets are not added to the queue")

        list_of_ticket_ids = []

        for ticket in retrieve_tickets_queue.tickets:
            list_of_ticket_ids.append(ticket.ticket_id)

        self.assertTrue(self.first_ticket.ticket_id in list_of_ticket_ids,
                        msg="{0} is not found in list of tickets\
                            for the queue".format(self.first_ticket.ticket_id))

        self.assertTrue(self.second_ticket.ticket_id in list_of_ticket_ids,
                        msg="{0} is not found in list of tickets for\
                            the queue".format(self.second_ticket.ticket_id))

    @attr(type='update_queue')
    def test_removing_ticket_tags_will_refresh_tickets_inside_queue(self):
        """Removing the tags for tickets refreshes the no. of \
        tickets inside the Queue"""

        self.first_ticket_with_no_tag = self.lefty_ticket_provider.\
            lefty_ticket_client.update_ticket(self.account_id,
                                              self.first_ticket.ticket_id,
                                              tags=[]).entity

        retrieve_tickets_queue = self.lefty_ticket_provider.\
            lefty_queue_client.\
            get_tickets_for_a_queue(self.my_queue.queue_id).entity

        self.assertEqual(len(retrieve_tickets_queue.tickets), 1,
                         msg="Tickets are not added to the queue")

        list_of_ticket_ids = []

        for ticket in retrieve_tickets_queue.tickets:
            list_of_ticket_ids.append(ticket.ticket_id)

        self.assertTrue(self.first_ticket.ticket_id not in list_of_ticket_ids,
                        msg="{0} is found in list of tickets\
                            for the queue".format(self.first_ticket.ticket_id))

        self.assertTrue(self.second_ticket.ticket_id in list_of_ticket_ids,
                        msg="{0} is not found in list of tickets for\
                            the queue".format(self.second_ticket.ticket_id))

        self.reset_first_ticket_with_tag = self.lefty_ticket_provider.\
            lefty_ticket_client.update_ticket(self.account_id,
                                              self.first_ticket.ticket_id,
                                              tags=self.my_tags).entity

    @attr(type='update_queue')
    def test_tickets_inside_queue_are_sorted_according_to_property(self):
        """Tickets inside a queue are sorted according to sort property"""

        retrieve_tickets_queue = self.lefty_ticket_provider.\
            lefty_queue_client.\
            get_tickets_for_a_queue(self.my_queue.queue_id).entity

        list_of_ticket_ids = []

        for ticket in retrieve_tickets_queue.tickets:
            list_of_ticket_ids.append(ticket.ticket_id)

        self.assertTrue(sorted(list_of_ticket_ids, reverse=True) ==
                        list_of_ticket_ids,
                        msg="{0} is found in list of tickets for the queue".
                            format(self.first_ticket.ticket_id))

    @attr(type='update_queue')
    def test_updated_tags_for_tickets_reflects_in_respective_queues(self):
        """Tickets beloging to a queue goes to another Queue when tags
        are updated accordingly"""

        new_tag = [random_string("new_tag_")]

        new_queue = self.lefty_ticket_provider.lefty_queue_client.\
            create_queue(random_string("New Queue_"), description="New Queue",
                         query_occurrence="must",
                         query_property="tags",
                         query_value=new_tag, sort_property="priority",
                         sort_order="desc").entity
        retrieve_tickets_new_queue = self.lefty_ticket_provider.\
            lefty_queue_client.\
            get_tickets_for_a_queue(new_queue.queue_id).entity

        self.assertEqual(len(retrieve_tickets_new_queue.tickets), 0,
                         msg="The ticket list is not empty")

        retrieve_tickets_queue = self.lefty_ticket_provider.\
            lefty_queue_client.\
            get_tickets_for_a_queue(self.my_queue.queue_id).entity

        self.assertEqual(len(retrieve_tickets_queue.tickets), 2,
                         msg="Length of ticket list is not 2")

        self.first_ticket_with_new_tag = self.lefty_ticket_provider.\
            lefty_ticket_client.update_ticket(self.account_id,
                                              self.first_ticket.ticket_id,
                                              tags=new_tag).entity

        retrieve_tickets_new_queue = self.lefty_ticket_provider.\
            lefty_queue_client.\
            get_tickets_for_a_queue(new_queue.queue_id).entity

        self.assertEqual(len(retrieve_tickets_new_queue.tickets), 1,
                         msg="The length of ticket list is not 1")

        retrieve_tickets_queue = self.lefty_ticket_provider.\
            lefty_queue_client.\
            get_tickets_for_a_queue(self.my_queue.queue_id).entity

        self.assertEqual(len(retrieve_tickets_queue.tickets), 1,
                         msg="Length of ticket list is not 1")

        self.reset_first_ticket_with_tag = self.lefty_ticket_provider.\
            lefty_ticket_client.update_ticket(self.account_id,
                                              self.first_ticket.ticket_id,
                                              tags=self.my_tags).entity

    @attr(type='update_queue')
    def test_search_tickets_for_invalid_queue(self):
        """Searching tickets for invalid queue should throw 404"""

        retrieve_tickets_invalid_queue = self.lefty_ticket_provider.\
            lefty_queue_client.\
            get_tickets_for_a_queue(queue_id="abcd")

        self.assertEqual(retrieve_tickets_invalid_queue.status_code,
                         eval(self.NOT_FOUND[0]),
                         msg="The exception is {0}, instead of {1}".
                         format(retrieve_tickets_invalid_queue.status_code,
                                self.NOT_FOUND[0]))
