import json
from ccengine.domain.core.request.core_request import WhereEquals
from testrepo.common.testfixtures.core import CoreFixture
from ccengine.common.decorators import attr
from ccengine.common.tools.datagen import rand_name


class TestAccountAccount(CoreFixture):
    """
    This contains all the test verification details on Account.Account class
    """

    @classmethod
    def setUpClass(cls):
        super(TestAccountAccount, cls).setUpClass()
        cls.result_map = {"id": "id"}
        cls.account_id = cls.config.core.account_id

    @attr(type='smoke')
    def test_add_contract_with_default_params(self):
        """
        @summary: Verify creation of contract  using Account.Account class's
        addContract's method using mandatory parameters
        """
        start_date = "2013-03-30 00:00:00"
        length = 5
        contract = self.account_client.\
                   account_add_contract(account_id=self.account_id,
                                        start_date=start_date, length=length,
                                        result_map=self.result_map).entity
        expected_contract_label = "Contract " + str(contract.id)
        contract_details = self.contract_client.\
                           get_contract_details(contract.id).entity

        self.assertEqual(contract.id, contract_details[0].id,
                         "Expected contract id doesn't match \
                          with actual contract id")
        self.assertEqual(start_date, contract_details[0].start,
                         "Actual start date is not same as the start date")
        self.assertEqual(length, contract_details[0].length,
                         "Actual contract length is not same as\
                          expected contract length")
        self.assertEqual(expected_contract_label, contract_details[0].label,
                         "Actual contract label is not same as\
                          expected contract label")

    @attr(type='smoke')
    def test_add_contract_with_optional(self):
        """summary:
        Verify creation of contract  using Account.Account class's
        addContract's method using optional parameters and verify the
        parameters by getting the contract details using Contract.Contract """
        start_date = "2013-03-30 00:00:00"
        length = 2
        site_id = 11
        sales_rep = 11
        expected_contract_label = rand_name("new test Contract")
        contract_with_label = self.account_client.\
                              account_add_contract(account_id=self.account_id,
                                                   start_date=start_date,
                                                   length=length,
                                                   site_id=site_id,
                                                   label=expected_contract_label,
                                                   sales_rep=sales_rep,
                                                   result_map=self.result_map
                                                   ).entity
        contract_details = self.contract_client.\
                           get_contract_details(contract_with_label.id).entity

        self.assertEqual(expected_contract_label, contract_details[0].label,
                         "Actual contract label {0} is not same as expected\
                         contract label {1}".format(expected_contract_label,
                                                    contract_details[0].label))
        self.assertEqual(sales_rep, contract_details[0].salesperson.get('id'),
                         "Actual  sales rep {0} is not same as expected sales \
                          rep {1}".format(sales_rep,
                                          contract_details[0].salesperson.get('id')))
        self.assertEqual(site_id, contract_details[0].site_id,
                        "Actual site_id {0} is not same as expected site_id \
                         {1}".format(site_id, contract_details[0].site_id))

    @attr(type='smoke')
    def test_add_note_to_contract(self):
        """@summary:
        Verify addition of a note to an account using Account.Account class's
        addNotes's method using optional parameters and verify the
        parameters by getting the account notes using Account.Account
        """
        new_note = rand_name("new note ")
        result = self.account_client.\
                                add_note_account(account_id=self.account_id,
                                               note=new_note).status_code
        self.assertEquals(result, 200, "Expected value {0}, Actual value {1}".
                                       format("200", result))
        recent_notes = self.account_client.\
                                get_recent_notes(account_id=self.account_id).entity
        self.assertTrue(new_note in recent_notes[0].recent_note,
                        "Newly added note {0} is not present in the recent notes\
                        ".format(new_note))

    @attr(type='smoke')
    def test_verify_account_details_using_accountwhere(self):
        """
        @summary: get all the attributes of a account using accountwhere as
        loadargs and verify the user can get all the attributes of an account
        """
        response_id = self.account_client.\
                              get_account_attribute(self.account_id,
                                                     attribute="id")
        expected_id = response_id.content
        response_account_type_id = \
            self.account_client.\
                    get_account_attribute(self.account_id, attribute="account_type_id")
        expected_account_type_id = response_account_type_id.content
        response_account_created_date = \
            self.account_client.\
                    get_account_attribute(self.account_id, attribute="created")
        expected_account_created_date = response_account_created_date.content
        response_support_queue = \
            self.account_client.\
                    get_account_attribute(self.account_id,
                                          attribute="support_queue")
        expected_support_queue_description = \
            eval(response_support_queue.content).get("description")
        where_condition = WhereEquals("number", self.account_id)
        attributes = ["account_coordinator", "account_exec",
                      "account_level_domains", "account_type_id",
                      "active_mbu_devices", "additional_bandwidth",
                      "all_employees", "all_notes", "am_queue", "ar_specialist",
                      "business_development", "calculated_is_dev_series",
                      "calculated_is_devseries", "cloud_account_numbers",
                      "cloud_accounts", "created", "customer_contacts",
                      "customers", "employees", "flags", "mbu_devices",
                      "monitoring_queue", "online_mbu_devices", "statuses",
                      "support_queue", "total_bandwidth", "number", "id"]

        response = self.account_client.\
                               get_account_attributes(where_condition,
                                                      attributes=attributes)
        account_details = response.entity[0]
        self.assertEqual(response.status_code, 200,
                         "expected status code is not same as 200")
        self.assertEqual(json.dumps(account_details.id), expected_id,
                         "expected id {0} is not same as actual id\
                         {1}".format(expected_id, account_details.id))
        self.assertEqual(json.dumps(account_details.account_type_id),
                         expected_account_type_id,
                         "expected account_type_id {0} is not same as actual\
                         type_id {1}".format(expected_account_type_id,
                                             account_details.account_type_id))
        self.assertEqual(json.dumps(account_details.created),
                         expected_account_created_date,
                         "expected created date {0} is not same as actual created\
                          date {1}".format(expected_account_created_date,
                                           account_details.created))
        self.assertEqual(account_details.support_queue["description"],
                         expected_support_queue_description,
                         "expected status queue {0} is not same as actual {1}"\
                         .format(expected_support_queue_description,
                                 account_details.support_queue["description"]))

    @attr(type='smoke')
    def test_department_details_in_session(self):
        """
        @summary : Verify session details contains employee
        details with  department info-LAM1042
        """
        employee_detils = self.account_client.get_session_details()

        self.assertEquals(employee_detils.status_code, 200,
                          "response status is not 200")
        employee_detils = employee_detils.entity
        self.assertTrue(employee_detils["valid"], "Valid is not true")
        self.assertTrue(employee_detils["contact_id"] is not None,
                        "Contact id is missing")
        self.assertTrue(employee_detils["employee_number"] is not None,
                        "Employee number is missing")
        self.assertTrue(employee_detils["departments"] is not None and\
                        len(employee_detils["departments"]) >= 1,
                        "Department details is missing")

    @attr(type='negative')
    def test_no_department_details_invalid_session(self):
        """
        @summary : Verify invalid session details should not have employee\
        department info-LAM1042
        """
        employee_detils = self.account_client.get_invalid_session_details()
        self.assertEquals(employee_detils.status_code, 200,
                          "Response status id different than expected")
        employee_detils = employee_detils.entity

        self.assertFalse(employee_detils["valid"], "Valid should be false")
        self.assertTrue(employee_detils["contact_id"] is None,
                        "Contact number is present")
        self.assertTrue(employee_detils["employee_number"] is None,
                        "Employee number is present")
        self.assertTrue(employee_detils["departments"] is None,
                        "Department details is missing")
