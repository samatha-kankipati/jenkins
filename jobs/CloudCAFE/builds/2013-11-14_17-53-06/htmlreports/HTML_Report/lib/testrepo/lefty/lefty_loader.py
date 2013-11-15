from datetime import datetime
from testrepo.lefty.test_pub_sub_cross_data_centre import \
    PubSubCrossDataCentreTest
from ccengine.common.loaders.base_parameterized_loader import \
    BaseParameterizedLoader
from ccengine.common.data_generators.lefty.lefty_data_generator import \
    TicketUpdateData

from unittest2.suite import TestSuite


def load_tests(loader, standard_tests, pattern):
    lefty_api_data_generator = TicketUpdateData()
    update_attribute_loader = BaseParameterizedLoader(lefty_api_data_generator)
    update_attribute_loader.addTest(
        PubSubCrossDataCentreTest("test_update_attribute_in_subscribe"))
    return update_attribute_loader.getSuite()
