import json
from testrepo.common.testfixtures.core import CoreFixture
from ccengine.common.decorators import attr
from ccengine.domain.core.request.core_request import WhereEquals


class TestContactContact(CoreFixture):
    """
    This contains all the test verification details on Account.Account class"""

    @classmethod
    def setUpClass(cls):
        super(TestContactContact, cls).setUpClass()
        cls.contact_id = cls.config.core.contact_id
        where_condition = WhereEquals("id", cls.contact_id)
        attributes = ["address", "created", "crm_individual_id", "crm_userid",
                      "departments", "email_list", "employee_datacenter",
                      "employee_number", "employee_userid", "first_name",
                      "id", "imaway", "individual", "last_active",
                      "login_time", "name", "notes", "role"]
        cls.response = cls.contact_client.\
                               get_contact_attributes(where_condition,
                                                      attributes=attributes)
        cls.contact_details = cls.response.entity[0]

    @attr(type='smoke')
    def test_verify_contact_name_from_contact_details(self):
        """
        @summary: get name attributes of a contact using
        contactWhere as loadargs and verify the same with expected attributes
        """
        attribute_name = "name"
        attribute_reponse = self.contact_client.\
                                 get_contact_attribute(self.contact_id,
                                                       attribute=attribute_name)
        expected_name = attribute_reponse.content

        self.assertEqual(self.response.status_code, 200,
                         "status code is not as expected {0}\
                         ".format(self.response.status_code))
        self.assertEqual(json.dumps(self.contact_details.name), expected_name,
                        "expected_name {0} is not same as actual {1}".
                         format(expected_name, self.contact_details.name))

    @attr(type='smoke')
    def test_verify_contact_created_date_from_contact_details(self):
        """
        @summary: get contact created date attributes of a contact using
        contactWhere as loadargs and verify the same with expected attributes
        """
        attribute_name = "created"
        attribute_reponse = self.contact_client.\
                                 get_contact_attribute(self.contact_id,
                                                       attribute=attribute_name)
        expected_created_date = attribute_reponse.content
        self.assertEqual(json.dumps(self.contact_details.created),
                         expected_created_date,
                         "expected_created date {0} is not same as actual\
                         created date ".format(expected_created_date,
                                               self.contact_details.created))

    @attr(type='smoke')
    def test_verify_contact_first_name_from_contact_details(self):
        """@summary:get first name attributes of a contact using
        contactWhere as loadargs and verify the same with expected attributes"""
        attribute_name = "first_name"
        attribute_reponse = self.contact_client.\
                                 get_contact_attribute(self.contact_id,
                                                       attribute=attribute_name)
        expected_first_name = attribute_reponse.content
        self.assertEqual(json.dumps(self.contact_details.first_name),
                         expected_first_name,
                         "expected_created date {0} is not same as actual first\
                         name".format(expected_first_name,
                                      self.contact_details.first_name))

    @attr(type='smoke')
    def test_verify_contact_role_from_contact_details(self):
        """@summary: get role attributes of a contact using
        contactWhere as loadargs and verify the same with expected attributes"""
        attribute_name = "role"
        attribute_reponse = self.contact_client.\
                                 get_contact_attribute(self.contact_id,
                                                       attribute=attribute_name)
        expected_role = eval(attribute_reponse.content).get("description")
        actual_role = str(self.contact_details.role.get("description"))
        self.assertEqual(actual_role, expected_role,
                         "expected role {0} is not same as actual role {1} \
                         ".format(expected_role, actual_role))

    @attr(type='smoke')
    def test_verify_contact_crm_individual_id_from_contact_details(self):
        """@summary: get crm_individual_id attributes of a contact using
        contactWhere as loadargs and verify the same with expcted attributes
        """
        attribute_name = "crm_individual_id"
        attribute_reponse = self.contact_client.\
                                 get_contact_attribute(self.contact_id,
                                                       attribute=attribute_name)
        expected_crm_individual_id = attribute_reponse.content
        self.assertEqual(json.dumps(self.contact_details.crm_individual_id),
                         expected_crm_individual_id,
                         "expected crm id {0} is not same as actual {1}"
                         .format(expected_crm_individual_id,
                                 self.contact_details.crm_individual_id))
