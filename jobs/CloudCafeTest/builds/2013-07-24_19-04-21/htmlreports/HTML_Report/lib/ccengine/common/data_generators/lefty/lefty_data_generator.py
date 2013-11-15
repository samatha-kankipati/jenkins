from datetime import datetime

from ccengine.common.data_generators.data_generator import DataGenerator
from ccengine.common.tools.datagen import random_string
from ccengine.domain.configuration import AuthConfig
from ccengine.domain.types import LavaClusterTypes
from ccengine.providers.configuration import MasterConfigProvider as _MCP
from testrepo.common.testfixtures.lefty import LeftyFixture


class TicketUpdateData(DataGenerator, LeftyFixture):

        def __init__(self):

            super(TicketUpdateData, self).setUpClass()

            self.category_1 = self.lefty_ticket_provider.\
                lefty_category_sub_category_client.\
                create_category(random_string("Test_Category_1_")).entity

            self.category_2 = self.lefty_ticket_provider.\
                lefty_category_sub_category_client.\
                create_category(random_string("Test_Category_2_")).entity

            self.sub_category_1 = self.lefty_ticket_provider.\
                lefty_category_sub_category_client.\
                create_sub_category(self.category_1.category_id,
                                    random_string("Test_SubCat_1_")).entity

            self.sub_category_2 = self.lefty_ticket_provider.\
                lefty_category_sub_category_client.\
                create_sub_category(self.category_2.category_id,
                                    random_string("Test_SubCat_2_")).entity

            self.test_records = []
            self.test_records.append(
                {"update_attr": {"rating": "Highest"}})
            self.test_records.append(
                {"update_attr": {"subject": "Updated Subject"}})
            self.test_records.append(
                {"update_attr": {"assignee": self.user},
                 "fetch_value_from_dict_with_key": "value"}
            )
            self.test_records.append(
                {"update_attr": {"priority": "High"}}
            )
            self.test_records.append(
                {"update_attr": {"description": "Updated Description"}}
            )
            self.test_records.append(
                {"update_attr": {"comment": random_string("Comment_")},
                 "fetch_value_from_dict_with_key": "text"}
            )
            self.test_records.append(
                {"update_attr": {"group": "Cloud_Group"}}
            )
            self.test_records.append(
                {"update_attr": {"status": "In Progress"}}
            )
            self.test_records.append(
                {"update_attr": {"difficulty": "Level 2"}}
            )
            self.test_records.append(
                {"update_attr": {"severity": "Urgent"}}
            )
            self.test_records.append(
                {"update_attr":
                    {"tags": [random_string("Tag_"), random_string("Tag_")]}}
            )
            self.test_records.append(
                {"update_attr": {"recipients": [self.user]},
                 "fetch_value_from_dict_with_key": "value"}
            )
            self.test_records.append(
                {"update_attr": {"status": "In Progress"}}
            )
            self.test_records.append(
                {"update_attr":
                    {"category_id": self.category_1.category_id,
                     "sub_category_id": self.sub_category_1.sub_category_id}}
            )
            self.test_records.append(
                {"update_attr":
                    {"sub_category_id": self.sub_category_2.sub_category_id,
                     "category_id": self.category_2.category_id}}
            )
