from testrepo.common.testfixtures.core import CoreFixture
from ccengine.common.decorators import attr
from ccengine.domain.core.request.core_request import WhereEquals


class TestQueue(CoreFixture):

    @attr(type='smoke')
    def test_list_catagory_subcategories(self):
        """
        @summary : Verify that listing of sub categories,categories available
        for a given queue id specified by using a query method.
        """
        expected_category_name = "Fixed Assets Request"
        expected_subcategories_ids = ["11030", "11031"]
        queue_id = 341
        category = self.queue_client.\
                   list_subcategories_by_queue_query(queue_id).entity
        subcategories_list = category[0].subcategories

        self.assertTrue(len(category) == 1, "Number of category result \
                        doesn't match with the expected list")
        self.assertEqual(expected_category_name, category[0].name,
                        "Actual category name does not match with the \
                         expected category name")
        self.assertEqual(len(subcategories_list), len(expected_subcategories_ids),
                         "Number of subcategories for the a given queue \
                          doesn't match as the expected list")

    @attr(type="smoke")
    def test_verify_queue_all_attributes(self):
        """
        @summary:  Verify all the required attributes of a queue for a given
        queue id and default attributes
        """
        queue_id = 1
        queue_details = self.queue_client.\
                                get_queue_attributes(queue_id)
        # asserting all the attribute details
        self.assertEqual(200, queue_details.status_code,
                         "Response code is not same as 200")
        self.assertTrue(queue_details.entity[0].id == 1,
                        "queue id {0} is different than expected"
                        .format(queue_details.entity[0].id))
        self.assertTrue(queue_details.entity[0].name == "Managed (All Teams)",
                        "queue name {0} is different that expected"
                        .format(queue_details.entity[0].name))
        self.assertEqual(len(queue_details.entity[0].categories), 24,
                         "expected categories count {0} is not same as expected"
                         .format(len(queue_details.entity[0].categories)))  # 24
        self.assertEqual(len(queue_details.entity[0].all_categories), 27,
                         "expected all_categories count {0} is not same as expected"
                         .format(len(queue_details.entity[0].all_categories)))  # 27
        self.assertEqual(len(queue_details.entity[0].all_statuses), 23,
                         "expected all_statuses count {0} is not same as expected"
                         .format(len(queue_details.entity[0].all_statuses)))  # 23
        self.assertEqual(queue_details.entity[0].description,
                         "Rackspace Managed Segment",
                         "queue description {0} is different that expected"
                        .format(queue_details.entity[0].description))
        self.assertEqual(len(queue_details.entity[0].displayable_categories), 8,
                         "expected displayable_categories count {0} is not same as expected"
                         .format(len(queue_details.entity[0].displayable_categories)))  # 8
        self.assertEqual(len(queue_details.entity[0].roles), 6,
                         "expected roles count {0} is not same as expected"
                         .format(len(queue_details.entity[0].roles)))  # 6
        self.assertEqual(len(queue_details.entity[0].statuses), 19,
                         "expected statuses count {0} is not same as expected"
                         .format(len(queue_details.entity[0].statuses)))  # 19
        self.assertEqual(len(queue_details.entity[0].priorities), 4,
                         "expected priorities count {0} is not same as expected"
                         .format(len(queue_details.entity[0].priorities)))  # 4
        self.assertEqual(len(queue_details.entity[0].inactive_statuses), 4,
                         "expected inactive_statuses count {0} is not same as expected"
                         .format(len(queue_details.entity[0].inactive_statuses)))  # 4
        self.assertEqual(len(queue_details.entity[0].inactive_categories), 3,
                         "expected inactive_categories count {0} is not same as expected"
                         .format(len(queue_details.entity[0].inactive_categories)))  # 3
        self.assertEqual(len(queue_details.entity[0].sources), 13,
                         "expected sources count {0} is not same as expected"
                         .format(len(queue_details.entity[0].sources)))  # 13
        self.assertEqual(len(queue_details.entity[0].work_types), 21,
                         "expected work_types count {0} is not same as expected"
                         .format(len(queue_details.entity[0].all_statuses)))  # 21

    @attr(type="smoke")
    def test_verify_queue_all_attributes_using_QueueWhere(self):
        queue_id = 1
        where_condition = WhereEquals("id", queue_id)
        attributes = ["all_categories", "product_suites", "roles", "sources",
                      "statuses"]
        queue_details = \
            self.queue_client.get_queue_attributes_using_queuewhere(
                where_condition,
                attributes,
                limit=None,
                offset=None
            )
        self.assertEqual(200, queue_details.status_code, "Response status code\
                                                         is not 200")
        queue_details = queue_details.entity[0]
        attribute_name = "all_categories"
        attribute_reponse = self.queue_client.\
                                  get_queue_attribute(queue_id,
                                                       attribute=attribute_name)
        self.assertEqual(len(queue_details.all_categories),
                         len(attribute_reponse.entity),
                         "expected all_categories count {0} is not same as expected"
                         .format(len(queue_details.all_categories)))
        attribute_name = "product_suites"
        attribute_reponse = self.queue_client.\
                                  get_queue_attribute(queue_id,
                                                       attribute=attribute_name)
        self.assertEqual(len(queue_details.product_suites),
                         len(attribute_reponse.entity),
                         "expected all_categories count {0} is not same as expected"
                         .format(len(queue_details.product_suites)))
        attribute_name = "sources"
        attribute_reponse = self.queue_client.\
                                  get_queue_attribute(queue_id,
                                                       attribute=attribute_name)
        self.assertEqual(len(queue_details.sources), len(attribute_reponse.entity),
                         "expected sources count {0} is not same as expected"
                         .format(len(queue_details.sources)))

        attribute_name = "roles"
        attribute_reponse = self.queue_client.\
                                  get_queue_attribute(queue_id,
                                                       attribute=attribute_name)
        self.assertEqual(len(queue_details.roles), len(attribute_reponse.entity),
                         "expected roles count {0} is not same as expected"
                         .format(len(queue_details.roles)))
