import unittest
from ccengine.common.tools.datagen import rand_name
from ccengine.common.tools.datagen import random_int
from testrepo.common.testfixtures.identity.v2_0.identity \
        import IdentityAdminFixture
from ccengine.common.decorators import attr
import types


class AdminExtensionsTest(IdentityAdminFixture):

    @classmethod
    def setUpClass(cls):
        super(AdminExtensionsTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        pass

    @attr('regression', type='positive')
    def test_admin_get_extension(self):
        normal_response_codes = [200, 203]   
        get_extensions = self.admin_client.list_extensions()
        self.assertIn(get_extensions.status_code, normal_response_codes,
                msg= 'Get Extensions expected {0} received {1}'.format(
                    normal_response_codes, 
                    get_extensions.status_code))
        self.assertTrue(get_extensions.entity[0].alias is not None,
            msg="Expecting alias is not None")
        self.assertTrue(get_extensions.entity[0].description is not None,
            msg="Expecting alias is not None")
        self.assertTrue(get_extensions.entity[0].name is not None,
            msg="Expecting alias is not None")
        self.assertTrue(get_extensions.entity[0].namespace is not None,
            msg="Expecting alias is not None")
        self.assertTrue(get_extensions.entity[0].updated is not None,
            msg="Expecting alias is not None")
        self.assertIsInstance(get_extensions.entity, types.ListType,
                msg="Expecting extensions format is correct")
        self.assertIsInstance(get_extensions.entity[0].links, types.ListType,
                msg="Expecting links format is correct")
        self.assertTrue(get_extensions.entity[0].links[0].href is not None,
            msg="Expecting alias is not None")
        self.assertTrue(get_extensions.entity[0].links[0].rel is not None,
            msg="Expecting alias is not None")
        self.assertTrue(get_extensions.entity[0].links[0].type is not None,
            msg="Expecting alias is not None")
    
    @attr('regression', type='positive')
    def test_get_extension_by_alias(self):
        normal_response_codes = [200, 203]   
        get_extensions = self.admin_client.list_extensions()
        self.assertIn(get_extensions.status_code, normal_response_codes,
                msg= 'Get Extensions expected {0} received {1}'.format(
                    normal_response_codes, 
                    get_extensions.status_code))
        get_extensions_alias = self.admin_client.get_extension_by_alias(
                alias=get_extensions.entity[0].alias)
        self.assertIn(get_extensions_alias.status_code, normal_response_codes,
                msg= 'Get Extensions alias expected {0} received {1}'.format(
                    normal_response_codes, 
                    get_extensions_alias.status_code))
        self.assertTrue(get_extensions_alias.entity.alias is not None,
            msg="Expecting alias is not None")
        self.assertTrue(get_extensions_alias.entity.description is not None,
            msg="Expecting alias is not None")
        self.assertTrue(get_extensions_alias.entity.name is not None,
            msg="Expecting alias is not None")
        self.assertTrue(get_extensions_alias.entity.namespace is not None,
            msg="Expecting alias is not None")
        self.assertTrue(get_extensions_alias.entity.updated is not None,
            msg="Expecting alias is not None")
        self.assertIsInstance(get_extensions_alias.entity.links, types.ListType,
                msg="Expecting links format is correct")
        self.assertTrue(get_extensions_alias.entity.links[0].href is not None,
            msg="Expecting alias is not None")
        self.assertTrue(get_extensions_alias.entity.links[0].rel is not None,
            msg="Expecting alias is not None")
        self.assertTrue(get_extensions_alias.entity.links[0].type is not None,
            msg="Expecting alias is not None")