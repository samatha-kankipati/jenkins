from ccengine.common.decorators import attr
from testrepo.common.testfixtures.lefty import LeftyFixture
from ccengine.common.tools.datagen import random_string


class CategorySubcategoryTest(LeftyFixture):

    @classmethod
    def setUpClass(cls):
        super(CategorySubcategoryTest, cls).setUpClass()
        cls.category_1 = cls.lefty_ticket_provider.\
            lefty_category_sub_category_client.\
            create_category(random_string("Test_Category_1_")).entity

    @attr(type='category')
    def test_fetching_non_existing_category_gives_404(self):
        """Trying to fetch non existing category gives 404"""

        non_existing_category_id = "9999999"
        category_details = \
            self.lefty_ticket_provider.lefty_category_sub_category_client.\
            get_category(non_existing_category_id)
        self.assertEqual(category_details.status_code, eval(self.NOT_FOUND[0]),
                         msg="The status code is {0} instead of {1}".
                             format(category_details.status_code,
                                    self.NOT_FOUND[0]))

    @attr(type='category')
    def test_deleting_non_existing_category_gives_404(self):
        """Trying to delete non existing category gives 404"""

        non_existing_category_id = "9999999"
        category_details = \
            self.lefty_ticket_provider.lefty_category_sub_category_client.\
            delete_category(non_existing_category_id)
        self.assertEqual(category_details.status_code, eval(self.NOT_FOUND[0]),
                         msg="The status code is {0} instead of {1}".
                             format(category_details.status_code,
                                    self.NOT_FOUND[0]))

    @attr(type='sub_category')
    def test_fetching_non_existing_sub_category_gives_404(self):
        """Trying to fetch non existing Subcategory gives 404"""

        non_existing_sub_category_id = "9999999"
        sub_category_details = \
            self.lefty_ticket_provider.lefty_category_sub_category_client.\
            get_sub_category(self.category_1.category_id,
                             non_existing_sub_category_id)
        self.assertEqual(sub_category_details.status_code,
                         eval(self.NOT_FOUND[0]),
                         msg="The status code is {0} instead of {1}".
                             format(sub_category_details.status_code,
                                    self.NOT_FOUND[0]))

    @attr(type='sub_category')
    def test_deleting_non_existing_sub_category_gives_404(self):
        """Trying to delete non existing Subcategory gives 404"""

        non_existing_sub_category_id = "9999999"
        sub_category_details = \
            self.lefty_ticket_provider.lefty_category_sub_category_client.\
            delete_sub_category(self.category_1.category_id,
                                non_existing_sub_category_id)
        self.assertEqual(sub_category_details.status_code,
                         eval(self.NOT_FOUND[0]),
                         msg="The status code is {0} instead of {1}".
                             format(sub_category_details.status_code,
                                    self.NOT_FOUND[0]))
