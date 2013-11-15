from datetime import timedelta
from time import gmtime, strftime

from ccengine.common.decorators import attr
from testrepo.common.testfixtures.lefty import LeftyFixture
from ccengine.common.tools.datagen import random_string
from ccengine.common.tools.datatools import string_to_datetime, \
    are_datetimestrings_equal


class TicketUpdateTest(LeftyFixture):

    @classmethod
    def setUpClass(cls):
        super(TicketUpdateTest, cls).setUpClass()

        cls.category_1 = cls.lefty_ticket_provider. \
            lefty_category_sub_category_client. \
            create_category(random_string("Test_Category_1_")).entity

        cls.category_2 = cls.lefty_ticket_provider. \
            lefty_category_sub_category_client. \
            create_category(random_string("Test_Category_2_")).entity

        cls.category_3 = cls.lefty_ticket_provider. \
            lefty_category_sub_category_client. \
            create_category(random_string("Test_Category_3_")).entity

        cls.sub_category_1 = cls.lefty_ticket_provider. \
            lefty_category_sub_category_client. \
            create_sub_category(cls.category_1.category_id,
                                random_string("Test_SubCat_1_")).entity

        cls.sub_category_2 = cls.lefty_ticket_provider. \
            lefty_category_sub_category_client. \
            create_sub_category(cls.category_2.category_id,
                                random_string("Test_SubCat_2_")).entity

        cls.sub_category_3 = cls.lefty_ticket_provider. \
            lefty_category_sub_category_client. \
            create_sub_category(cls.category_1.category_id,
                                random_string("Test_SubCat_3_")).entity

        cls.sub_category_4 = cls.lefty_ticket_provider. \
            lefty_category_sub_category_client. \
            create_sub_category(cls.category_1.category_id,
                                random_string("Test_SubCat_4_")).entity

        cls.first_ticket = \
            cls.lefty_ticket_provider.lefty_ticket_client.create_ticket(
                cls.account_id, "Test Ticket 1", "Ticket for Automation Test",
                cls.category_1.category_id,
                cls.sub_category_1.sub_category_id).entity

        cls.second_ticket = cls.lefty_ticket_provider.lefty_ticket_client. \
            create_ticket(cls.account_id, "Test Ticket 2", "Automation ticket",
                          cls.category_2.category_id,
                          cls.sub_category_2.sub_category_id).entity

        cls.third_ticket = cls.lefty_ticket_provider.lefty_ticket_client. \
            create_ticket(cls.account_id, "Test Ticket 3", "Automation ticket",
                          cls.category_2.category_id,
                          cls.sub_category_2.sub_category_id).entity

        cls.invalid_description_comment_string = "x" * 70001

        cls.invalid_subject_string = "x" * 151

    @attr(type='update_ticket')
    def test_update_priority(self):
        """ Update priority for a ticket"""
        new_priority = "high"
        update_resp = self.lefty_ticket_provider. \
            lefty_ticket_client. \
            update_ticket(self.account_id, self.first_ticket.ticket_id,
                          priority=new_priority).entity

        self.assertEqual(update_resp.priority, new_priority,
                         msg="The priority is not updated")

    @attr(type='update_ticket')
    def test_add_tags_for_ticket(self):
        """Adding tags for a ticket """
        tag_list = ["tag1", "tag2", "./_-~^", "Alphanum34e4ic./_-~^"]
        update_resp = self.lefty_ticket_provider.lefty_ticket_client. \
            update_ticket(self.account_id, self.first_ticket.ticket_id,
                          tags=tag_list).entity
        self.assertEqual(update_resp.tags, tag_list,
                         msg="The tag list do not match")

    @attr(type='update_ticket')
    def test_add_invalid_tags_for_ticket(self):
        """Adding invalid tags for a ticket"""
        tag_list = ["$%^&*("]
        update_resp = self.lefty_ticket_provider.lefty_ticket_client. \
            update_ticket(self.account_id, self.first_ticket.ticket_id,
                          tags=tag_list)
        self.assertEqual(update_resp.status_code, eval(self.BAD_REQ_CODE[0]),
                         msg="The response code is {0},\
                             instead of {1}".format(update_resp.status_code,
                                                    self.BAD_REQ_CODE[0]))

    @attr(type='update_ticket')
    def test_update_ratings(self):
        """ Update rating for a ticket"""
        new_rating = "Highest"
        update_resp = self.lefty_ticket_provider. \
            lefty_ticket_client. \
            update_ticket(self.account_id, self.first_ticket.ticket_id,
                          rating=new_rating).entity

        self.assertEqual(update_resp.rating, new_rating,
                         msg="The rating is not updated")

    @attr(type='update_ticket')
    def test_add_comments_to_existing_ticket(self):
        """ Update comments for a ticket"""
        new_comment = random_string("Comment_")
        comment_list = []
        update_resp = self.lefty_ticket_provider. \
            lefty_ticket_client. \
            update_ticket(self.account_id, self.first_ticket.ticket_id,
                          comment=new_comment).entity

        for comment in update_resp.comments:
            comment_list.append(comment.get("text"))

        self.assertTrue(new_comment in comment_list, msg="Comment not added")

    @attr(type='update_ticket')
    def test_update_assignee(self):
        """ Update assignee for a ticket"""
        new_assignee = self.user
        update_resp = self.lefty_ticket_provider. \
            lefty_ticket_client. \
            update_ticket(self.account_id, self.first_ticket.ticket_id,
                          assignee=new_assignee).entity
        self.assertEqual(update_resp.assignee.get("value"), new_assignee,
                         msg="The assignee is not updated")

    @attr(type='update_ticket')
    def test_update_products(self):
        """ Update products for a ticket"""
        new_products = self.products
        update_resp = self.lefty_ticket_provider. \
            lefty_ticket_client. \
            update_ticket(self.account_id, self.first_ticket.ticket_id,
                          products=new_products).entity

        self.assertEqual(update_resp.products, new_products,
                         msg="The products are not updated")

    @attr(type='update_ticket')
    def test_update_recipients(self):
        """ Update recipients for a ticket"""
        new_recipients = [self.user]

        update_resp = self.lefty_ticket_provider. \
            lefty_ticket_client. \
            update_ticket(self.account_id, self.first_ticket.ticket_id,
                          recipients=new_recipients).entity

        found_recipients = \
            [recipient.get('value') for recipient in update_resp.recipients]

        self.assertEqual(found_recipients, new_recipients,
                         msg="The recipients are not updated")

    @attr(type='update_ticket')
    def test_last_updated_time_for_ticket(self):
        """ The last updated time gets updated on attribute update"""
        new_priority = "low"
        update_resp = self.lefty_ticket_provider. \
            lefty_ticket_client. \
            update_ticket(self.account_id, self.first_ticket.ticket_id,
                          priority=new_priority).entity

        update_time = strftime("%Y-%m-%dT%H:%M:%S.000000Z", gmtime())
        self.assertTrue(are_datetimestrings_equal(update_resp.last_updated,
                                                  update_time, 70),
                        msg="The last_updated field is not updated \
                            when a field is updated", )

    @attr(type='update_ticket')
    def test_by_field_is_autopopulated_on_creating_comment(self):
        """ 'by' field is autopopulated on creating a comment"""
        new_comment = random_string("Comment_")
        created_by = self.user
        comment_list = []
        update_resp = self.lefty_ticket_provider. \
            lefty_ticket_client. \
            update_ticket(self.account_id, self.first_ticket.ticket_id,
                          comment=new_comment).entity

        for comment in update_resp.comments:
            comment_list.append(comment.get("text"))

        self.assertTrue(new_comment in comment_list,
                        msg="The comment is not added")

        for comment in update_resp.comments:
            if comment.get("text") == new_comment:
                self.assertTrue(comment.get("by") is not None,
                                msg="The by field is not auto populated")
                self.assertEqual(comment.get("by").get("value"), created_by,
                                 msg="The by is not auto populated with \
                                     username")

    @attr(type='update_ticket')
    def test_on_field_is_autopopulated_on_creating_comment(self):
        """ 'on' field is autopopulated on creating a comment"""
        new_comment = random_string("Comment_")
        comment_list = []
        update_resp = self.lefty_ticket_provider. \
            lefty_ticket_client. \
            update_ticket(self.account_id, self.first_ticket.ticket_id,
                          comment=new_comment).entity

        creating_time = strftime("%Y-%m-%dT%H:%M:%S.000000Z", gmtime())

        for comment in update_resp.comments:
            comment_list.append(comment.get("text"))

        self.assertTrue(new_comment in comment_list,
                        msg="The comment is not added")

        for comment in update_resp.comments:
            if comment.get("text") == new_comment:
                self.assertTrue(comment.get("on") is not None,
                                msg="The on field is not auto populated")
                self.assertTrue(are_datetimestrings_equal(comment.get("on"),
                                                          creating_time, 70),
                                msg="The on is not auto populated \
                                    with creation time")

    @attr(type='update_ticket')
    def test_update_category_id(self):
        """ Update category ID for a ticket"""
        update_resp = self.lefty_ticket_provider. \
            lefty_ticket_client. \
            update_ticket(self.account_id, self.first_ticket.ticket_id,
                          category_id=self.category_2.category_id,
                          sub_category_id=self.
                          sub_category_2.sub_category_id).entity

        self.assertEqual(update_resp.category_id, self.category_2.category_id,
                         msg="The category id did not get updated")

    @attr(type='update_ticket')
    def test_update_category_id_auto_updates_category_name(self):
        """ Update category ID auto updates Category name for a ticket"""
        update_resp = self.lefty_ticket_provider. \
            lefty_ticket_client. \
            update_ticket(self.account_id, self.first_ticket.ticket_id,
                          category_id=self.category_2.category_id,
                          sub_category_id=self.
                          sub_category_2.sub_category_id).entity

        self.assertEqual(update_resp.category, self.category_2.name,
                         msg="The category name did not get updated")

    @attr(type='update_ticket')
    def test_update_sub_category_id(self):
        """ Update Subcategory ID for a ticket"""
        update_resp = self.lefty_ticket_provider. \
            lefty_ticket_client. \
            update_ticket(self.account_id, self.first_ticket.ticket_id,
                          category_id=self.category_1.category_id,
                          sub_category_id=self.
                          sub_category_3.sub_category_id).entity

        self.assertEqual(update_resp.sub_category_id,
                         self.sub_category_3.sub_category_id,
                         msg="The sub category id did not get updated")

    @attr(type='update_ticket')
    def test_update_sub_category_id_auto_updates_sub_category_name(self):
        """ Update Subcategory ID auto updates subcategory name for a ticket"""
        update_resp = self.lefty_ticket_provider. \
            lefty_ticket_client. \
            update_ticket(self.account_id, self.first_ticket.ticket_id,
                          category_id=self.category_1.category_id,
                          sub_category_id=self.
                          sub_category_4.sub_category_id).entity

        self.assertEqual(update_resp.sub_category,
                         self.sub_category_4.name,
                         msg="The sub category name did not get updated")

    @attr(type='bug')
    def test_update_just_category_id_throws_bad_request(self):
        """ Updating just the category throws a Bad Request"""
        update_resp = self.lefty_ticket_provider. \
            lefty_ticket_client. \
            update_ticket(self.account_id, self.first_ticket.ticket_id,
                          category_id=self.category_3.category_id)

        self.assertEqual(update_resp.status_code, eval(self.BAD_REQ_CODE[0]),
                         msg="The exception is {0},\
                             instead of {1}".format(update_resp.status_code,
                                                    self.BAD_REQ_CODE[0]))

        self.assertEqual(update_resp.reason, self.BAD_REQ_CODE[1],
                         msg="The exception is {0}, instead of\
                             {1}".format(update_resp.reason,
                                         self.BAD_REQ_CODE[1]))

    @attr(type='update_ticket')
    def test_update_status_for_ticket(self):
        """ Updating the status of a ticket"""
        update_resp = self.lefty_ticket_provider. \
            lefty_ticket_client. \
            update_ticket(self.account_id, self.first_ticket.ticket_id,
                          status="In Progress")

        self.assertEqual(update_resp.status_code, eval(self.OK_CODE[0]),
                         msg="The response code is {0},\
                             instead of {1}".format(update_resp.status_code,
                                                    self.OK_CODE[0]))

        self.assertEqual(update_resp.entity.status, "In Progress",
                         msg="The status did not get updated")

    @attr(type='update_ticket')
    def test_transition_ticket_new_to_solved(self):
        """Verify error when ticket is moved from new to solved"""
        update_resp = self.lefty_ticket_provider. \
            lefty_ticket_client. \
            update_ticket(self.account_id, self.second_ticket.ticket_id,
                          status="Solved")
        self.assertEqual(update_resp.status_code, eval(self.BAD_REQ_CODE[0]),
                         msg="The response code is {0},\
                             instead of {1}".format(update_resp.status_code,
                                                    self.BAD_REQ_CODE[0]))
        update_resp = self.lefty_ticket_provider.lefty_ticket_client. \
            get_ticket(self.account_id, ticket_id=self.second_ticket.ticket_id)
        self.assertEqual(update_resp.entity.status, "New",
                         msg="Ticket not in New status")

    @attr(type='update_ticket')
    def test_transition_ticket_new_to_closed(self):
        """Verify error when ticket is moved from new to solved"""
        update_resp = self.lefty_ticket_provider. \
            lefty_ticket_client. \
            update_ticket(self.account_id, self.second_ticket.ticket_id,
                          status="Closed")
        self.assertEqual(update_resp.status_code, eval(self.BAD_REQ_CODE[0]),
                         msg="The response code is {0},\
                             instead of {1}".format(update_resp.status_code,
                                                    self.BAD_REQ_CODE[0]))
        update_resp = self.lefty_ticket_provider.lefty_ticket_client. \
            get_ticket(self.account_id, ticket_id=self.second_ticket.ticket_id)
        self.assertEqual(update_resp.entity.status, "New",
                         msg="Ticket not in New status")

    @attr(type='update_ticket')
    def test_case_sensitivity_in_updates(self):
        """Verify status,severity,difficulty & priority are case sensitive"""
        update_resp = self.lefty_ticket_provider.lefty_ticket_client. \
            update_ticket(self.account_id, self.third_ticket.ticket_id,
                          status="in progress")
        self.assertEqual(update_resp.status_code, eval(self.BAD_REQ_CODE[0]),
                         msg="The response code is {0},\
                             instead of {1}".format(update_resp.status_code,
                                                    self.BAD_REQ_CODE[0]))

        update_resp = self.lefty_ticket_provider.lefty_ticket_client. \
            update_ticket(self.account_id, self.third_ticket.ticket_id,
                          severity="standard")
        self.assertEqual(update_resp.status_code, eval(self.BAD_REQ_CODE[0]),
                         msg="The response code is {0},\
                             instead of {1}".format(update_resp.status_code,
                                                    self.BAD_REQ_CODE[0]))

        update_resp = self.lefty_ticket_provider.lefty_ticket_client. \
            update_ticket(self.account_id, self.third_ticket.ticket_id,
                          priority="High")
        self.assertEqual(update_resp.status_code, eval(self.BAD_REQ_CODE[0]),
                         msg="The response code is {0},\
                             instead of {1}".format(update_resp.status_code,
                                                    self.BAD_REQ_CODE[0]))

    @attr(type='update_ticket')
    def test_assignee_required_for_solved(self):
        """Verify assignee is required to Solve a ticket"""

        new_assignee = self.user

        update_resp = self.lefty_ticket_provider.lefty_ticket_client. \
            update_ticket(self.account_id, self.third_ticket.ticket_id,
                          status="In Progress")
        self.assertEqual(update_resp.status_code, eval(self.OK_CODE[0]),
                         msg="The response code is {0},\
                             instead of {1}".format(update_resp.status_code,
                                                    self.OK_CODE[0]))

        update_resp = self.lefty_ticket_provider. \
            lefty_ticket_client. \
            update_ticket(self.account_id, self.third_ticket.ticket_id,
                          status="Closed")
        self.assertEqual(update_resp.status_code, eval(self.BAD_REQ_CODE[0]),
                         msg="The response code is {0},\
                             instead of {1}".format(update_resp.status_code,
                                                    self.BAD_REQ_CODE[0]))

        update_resp = self.lefty_ticket_provider. \
            lefty_ticket_client. \
            update_ticket(self.account_id, self.third_ticket.ticket_id,
                          assignee=new_assignee).entity
        self.assertEqual(update_resp.assignee.get("value"), new_assignee,
                         msg="The assignee is not updated")

        update_resp = self.lefty_ticket_provider. \
            lefty_ticket_client. \
            update_ticket(self.account_id, self.third_ticket.ticket_id,
                          status="Solved")
        self.assertEqual(update_resp.status_code, eval(self.OK_CODE[0]),
                         msg="The response code is {0},\
                             instead of {1}".format(update_resp.status_code,
                                                    self.OK_CODE[0]))

        update_resp = self.lefty_ticket_provider.lefty_ticket_client.\
            get_ticket(self.account_id, self.third_ticket.ticket_id).entity
        self.assertEqual(update_resp.status, "Solved",
                         msg="The ticket is not closed")

    @attr(type='update_ticket')
    def test_character_limit_on_comment(self):
        """ Verify character count on comment"""
        new_comment = random_string(self.invalid_description_comment_string)
        update_resp = self.lefty_ticket_provider. \
            lefty_ticket_client. \
            update_ticket(self.account_id, self.first_ticket.ticket_id,
                          comment=new_comment)
        self.assertEqual(update_resp.status_code, eval(self.BAD_REQ_CODE[0]),
                         msg="Response code is {0},instead of {1} for invalid"
                             "longer comment".format(update_resp.status_code,
                                                     self.BAD_REQ_CODE[0]))

    @attr(type='update_ticket')
    def test_character_limit_on_description(self):
        """ Verify character count on description"""
        new_description = random_string(
            self.invalid_description_comment_string)
        update_resp = self.lefty_ticket_provider. \
            lefty_ticket_client. \
            update_ticket(self.account_id, self.first_ticket.ticket_id,
                          description=new_description)
        self.assertEqual(update_resp.status_code, eval(self.BAD_REQ_CODE[0]),
                         msg="Response code is {0},instead of {1} for invalid"
                             "long description".format(update_resp.status_code,
                                                       self.BAD_REQ_CODE[0]))

    @attr(type='update_ticket')
    def test_character_limit_on_subject(self):
        """ Verify character count on subject"""
        new_subject = random_string(self.invalid_subject_string)
        update_resp = self.lefty_ticket_provider. \
            lefty_ticket_client. \
            update_ticket(self.account_id, self.first_ticket.ticket_id,
                          subject=new_subject)
        self.assertEqual(update_resp.status_code, eval(self.BAD_REQ_CODE[0]),
                         msg="Response code is {0},instead of {1} for invalid"
                             "long subject".format(update_resp.status_code,
                                                   self.BAD_REQ_CODE[0]))

    @attr(type='update_ticket')
    def test_offset_list_tickets(self):
        """List tickets with offset and count"""
        ticket_list_1 = self.lefty_ticket_provider.lefty_ticket_client. \
            list_tickets(account_id=self.account_id, ticket_status="open",
                         offset=0).entity
        ticket_list_2 = self.lefty_ticket_provider.lefty_ticket_client. \
            list_tickets(account_id=self.account_id, ticket_status="open",
                         offset=10).entity
        self.assertNotEqual(ticket_list_1[0].ticket_id,
                            ticket_list_2[0].ticket_id,
                            msg="Offset returning same tickets")

    @attr(type='update_ticket')
    def test_count_list_tickets(self):
        """List tickets with offset and count"""
        ticket_count = 6
        ticket_list = self.lefty_ticket_provider.lefty_ticket_client. \
            list_tickets(account_id=self.account_id, count=ticket_count).entity
        self.assertEqual(len(ticket_list), ticket_count,
                         msg="Number of tickets doesnt match count parameter")

    @attr(type='update_ticket')
    def test_get_open_tickets(self):
        """ Get Open tickets """
        update_resp = self.lefty_ticket_provider.lefty_ticket_client. \
            list_tickets(account_id=self.account_id,
                         ticket_status="open").entity
        for ticket in update_resp:
            self.assertNotEqual(ticket.status, "Solved",
                                msg="Solved tickets returned in open list")
            self.assertNotEqual(ticket.status, "Closed",
                                msg="Closed tickets returned in open list")

    @attr(type='update_ticket')
    def test_get_closed_tickets(self):
        """ Get Closed tickets """
        update_resp = self.lefty_ticket_provider.lefty_ticket_client. \
            list_tickets(account_id=self.account_id,
                         ticket_status="closed").entity
        for ticket in update_resp:
            self.assertNotEqual(ticket.status, "New",
                                msg="New tickets returned in closed list")
            self.assertNotEqual(ticket.status, "In Progress",
                                msg="In Progress tickets are in open list")
