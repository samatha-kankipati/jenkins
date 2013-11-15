'''
from datetime import datetime
from testrepo.rax_auth.smoke.rax_negative_users_test import UsersNegativeTest

from ccengine.common.loaders.base_parameterized_loader import BaseParameterizedLoader
from ccengine.common.data_generators.identity.auth_data_generator import AuthPasswordData

from unittest2.suite import TestSuite

def load_tests(loader, standard_tests, pattern):
#    smoke_data_gen = AuthPasswordData()
#    custom_loader = BaseParameterizedLoader(smoke_data_gen)
#    custom_loader.addTest(UsersNegativeTest("test_add_user_false_password"))
#    custom_loader.addTest(UsersNegativeTest("test_add_user_false_username"))
#    return custom_loader.getSuite()

#    suite = unittest.TestSuite()
#    suite.addTest(ParametrizedTestCase.parametrize(TestOne, param=42))
#    suite.addTest(ParametrizedTestCase.parametrize(TestOne, param=13))
#    unittest.TextTestRunner(verbosity=2).run(suite)

'''