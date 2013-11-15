import random

from ccengine.common.tools.datagen import rand_name, random_string
from testrepo.common.testfixtures.identity.v2_0.identity \
    import IdentityAdminFixture
from ccengine.common.decorators import attr


class AdminAttrLengthTest(IdentityAdminFixture):
    @classmethod
    def setUpClass(cls):
        """
        Function to create test bed for all the test. Execute once at the
        beginning of class
        @param cls: instance of class
        """
        super(AdminAttrLengthTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        """
        Function to clean up the data after execution of all the tests
        completed. Execute once at the end of all the tests.
        @param cls: instance of class
        """
        pass

    def create_user(self):
        """
        Function to create user with some default data
        @return Response of create user
        """
        username = rand_name("ccadminname")
        email = self.config.identity_api.default_email
        domain_id = random.randrange(100000000, 999999999)
        default_region = self.config.identity_api.default_region
        created_user = self.admin_client.add_user(username=username,
                                                  email=email,
                                                  enabled=True,
                                                  defaultRegion=default_region,
                                                  domainId=domain_id,
                                                  password="Gadmpass8")
        self.assertEqual(created_user.status_code, 201,
                         msg="Response for create user is not 201.")
        # Delete user after test completion
        self.addCleanup(self.provider.delete_user_permanently,
                        user_id=created_user.entity.id,
                        client=self.admin_client,
                        service_client=self.service_client)
        return created_user

    @attr('regression', type='negative')
    def test_create_user_with_long_username_length(self):
        """
        Testing create user functionality with long username than expected.
        failure should return 400
        """
        username = rand_name("ccadminname")
        email = self.config.identity_api.default_email
        domain_id = random.randrange(100000000, 999999999)
        default_region = self.config.identity_api.default_region

        create_user_username = self.admin_client.add_user(
            username=random_string(prefix=username, size=101),
            email=email,
            enabled=True,
            defaultRegion=default_region,
            domainId=domain_id,
            password="Gadmpass8")

        self.assertEqual(create_user_username.status_code, 400,
                         msg="Response for Create user with username "
                             "length > 100 characters is not 400.")

    @attr('regression', type='negative')
    def test_create_user_with_long_email_length(self):
        """
        Testing create user functionality with long email than expected.
        failure should return 400
        """
        username = rand_name("ccadminname")
        domain_id = random.randrange(100000000, 999999999)
        default_region = self.config.identity_api.default_region

        email = random_string(prefix="testbox", size=101)
        email_domain = self.config.identity_api.default_email.split('@')
        create_user_email = self.admin_client.add_user(
            username=username,
            email="{0}@{1}".format(email, email_domain[1]),
            enabled=True,
            defaultRegion=default_region,
            domainId=domain_id,
            password="Gadmpass8")

        self.assertEqual(create_user_email.status_code, 400,
                         msg="Response for Create user with email "
                             "length > 100 characters is not 400.")

    @attr('regression', type='negative')
    def test_create_user_with_long_domain_id_length(self):
        """
        Testing create user functionality with long domain ID than expected.
        failure should return 400
        """
        username = rand_name("ccadminname_length")
        email = self.config.identity_api.default_email
        domain_id = random.randrange(100000000, 999999999)
        default_region = self.config.identity_api.default_region

        create_user_region = self.admin_client.add_user(
            username=username,
            email=email,
            enabled=True,
            defaultRegion=random_string(prefix=default_region, size=101),
            domainId=domain_id,
            password="Gadmpass8")

        self.assertEqual(create_user_region.status_code, 400,
                         msg="Response for Create user with domain ID "
                             "length > 100 characters is not 400.")

    @attr('regression', type='negative')
    def test_create_user_with_long_password_length(self):
        """
        Testing create user functionality with long password than expected.
        failure should return 400
        """
        username = rand_name("ccadminname_length")
        email = self.config.identity_api.default_email
        domain_id = random.randrange(100000000, 999999999)
        default_region = self.config.identity_api.default_region

        create_user_password = self.admin_client.add_user(
            username=username,
            email=email,
            enabled=True,
            defaultRegion=default_region,
            domainId=domain_id,
            password=random_string(prefix='Gadmpass8', size=101))

        self.assertEqual(create_user_password.status_code, 400,
                         msg="Response for Create user with password "
                             "length > 100 is not 400.")

    @attr('regression', type='negative')
    def test_update_username_attr_of_user_length(self):
        """
        Testing update user functionality with long username than expected.
        failure should return 400
        """
        created_user = self.create_user()
        update_user_username = self.admin_client.update_user(
            userId=created_user.entity.id,
            username=random_string(prefix="testuser", size=101))
        self.assertEqual(update_user_username.status_code, 400,
                         msg="Response for Update username with value greater"
                             " than 100 characters is not 400.")

    @attr('regression', type='negative')
    def test_update_email_attr_of_user_length(self):
        """
        Testing update user functionality with long email than expected.
        failure should return 400
        """
        created_user = self.create_user()
        email = random_string(prefix="testbox", size=101)
        email_domain = self.config.identity_api.default_email.split('@')
        update_user_email = self.admin_client.update_user(
            userId=created_user.entity.id,
            email="{0}@{1}".format(email, email_domain[1]))
        self.assertEqual(update_user_email.status_code, 400,
                         msg="Response for update user email with value "
                             "greater than 100 characters is not 400.")

    @attr('regression', type='negative')
    def test_update_default_region_attr_of_user_length(self):
        """
        Testing update user functionality with long default region name than
        expected.
        failure should return 400
        """
        created_user = self.create_user()
        update_user_region = self.admin_client.update_user(
            userId=created_user.entity.id,
            defaultRegion=random_string(prefix="dfw", size=101))
        self.assertEqual(update_user_region.status_code, 400,
                         msg="Response for update user default region with "
                             "value greater than 100 characters is not 400.")

    @attr('regression', type='negative')
    def test_update_password_attr_of_user_length(self):
        """
        Testing update user functionality with long password than expected.
        failure should return 400
        """
        created_user = self.create_user()
        update_user_password = self.admin_client.update_user(
            userId=created_user.entity.id,
            password=random_string(prefix='Gadmpass8', size=101))
        self.assertEqual(update_user_password.status_code, 400,
                         msg="Response for update user password with "
                             "value greater than 100 characters is not 400.")

    @attr('regression', type='negative')
    def test_add_group_with_long_name(self):
        """
        Testing add group functionality with long name than expected.
        failure should return 400
        """
        name = rand_name('Group_Name')
        add_group = self.admin_client.add_group(
            name=random_string(prefix=name, size=101),
            description='Description')
        self.assertEqual(add_group.status_code, 400,
                         msg="Response for Add group with long name (>100 "
                             "characters) is not 400.")

    @attr('regression', type='negative')
    def test_add_group_with_long_description(self):
        """
        Testing add group functionality with long description than expected.
        failure should return 400
        """
        add_group = self.admin_client.add_group(
            name=rand_name('Group_Name'),
            description=random_string(prefix='Description', size=1001))
        self.assertEqual(add_group.status_code, 400,
                         msg="Response for Add group with long description ("
                             ">1000 characters) is not 400.")

    @attr('regression', type='negative')
    def test_update_group_name_attr_length(self):
        """
        Testing update group functionality with long name than expected.
        failure should return 400
        """
        name = rand_name('Group_Name')
        description = 'Description'
        add_group = self.admin_client.add_group(name=name,
                                                description=description)
        self.assertEqual(add_group.status_code, 201,
                         msg="Response for add group is not 201.")
        # delete group after test completion
        self.addCleanup(self.admin_client.delete_group,
                        groupId=add_group.entity.id)

        update_group_name = self.admin_client.update_group(
            groupId=add_group.entity.id,
            name=random_string(prefix=name, size=101),
            description=description)
        self.assertEqual(update_group_name.status_code, 400,
                         msg="Response for update group name with "
                             "value greater than 100 characters is not 400.")

    @attr('regression', type='negative')
    def test_update_group_description_attr_length(self):
        """
        Testing update group functionality with long description than expected.
        failure should return 400
        """
        name = rand_name('Group_Name')
        description = 'Description'
        add_group = self.admin_client.add_group(name=name,
                                                description=description)
        self.assertEqual(add_group.status_code, 201,
                         msg="Response for add group is not 201.")
        # delete group after test completion
        self.addCleanup(self.admin_client.delete_group,
                        groupId=add_group.entity.id)

        update_group_desc = self.admin_client.update_group(
            groupId=add_group.entity.id,
            name=name,
            description=random_string(prefix=description, size=1001))
        self.assertEqual(update_group_desc.status_code, 400,
                         msg="Response for update group description with "
                             "value greater than 1000 characters is not 400.")

    @attr('regression', type='negative')
    def test_add_role_with_long_name(self):
        """
        Testing add role functionality with long name than expected.
        failure should return 400
        """
        name = rand_name('Role_Name')
        description = 'Description'
        add_role = self.admin_client.add_role(
            name=random_string(prefix=name, size=101),
            description=description)

        self.assertEqual(add_role.status_code, 400,
                         msg="Response for add role with name > 100 "
                             "characters is not 400.")

    @attr('regression', type='negative')
    def test_add_role_with_long_description(self):
        """
        Testing add role functionality with long description than expected.
        failure should return 400
        """
        name = rand_name('Role_Name')
        description = 'Description'
        add_role = self.admin_client.add_role(
            name=name,
            description=random_string(prefix=description, size=1001))

        self.assertEqual(add_role.status_code, 400,
                         msg="Response for add role with description > 1000"
                             " characters is not 400.")

    @attr('regression', type='negative')
    def test_create_question_attr_length(self):
        """
        Testing create question functionality with long value than expected.
        failure should return 400
        """
        question = rand_name('Test question')
        create_question_resp = self.admin_client.create_question(
            question=random_string(prefix=question, size=1001))
        self.assertEqual(create_question_resp.status_code, 400,
                         msg="Response for Create Question with value > 1000"
                             "characters is not 400.")

    @attr('regression', type='negative')
    def test_update_question_attr_length(self):
        """
        Testing update question functionality with long value than expected.
        failure should return 400
        """
        question = rand_name('Test question')
        create_question_resp = self.admin_client.create_question(
            question=question)
        self.assertEqual(create_question_resp.status_code, 201,
                         msg="Response for create question is not 201.")
        question_id = create_question_resp.headers['location'].split('/')[-1]

        # delete question after test completion
        self.addCleanup(self.admin_client.delete_question,
                        questionId=question_id)

        update_question_resp = self.admin_client.update_question(
            questionId=question_id,
            question=random_string(prefix=question, size=1001))

        self.assertEqual(update_question_resp.status_code, 400,
                         msg="Response for update question with value > 1000 "
                             "characters is not 400.")

    @attr('regression', type='negative')
    def test_create_secret_qa_attr_length(self):
        """
        Testing create secret question functionality with long answer than
        expected.
        failure should return 400
        """
        question = rand_name('this is a test question')
        answer = "Test answer"
        username = rand_name("cctestuser")
        email = self.config.identity_api.default_email
        domain_id = random.randrange(100000000, 999999999)
        default_region = self.config.identity_api.default_region

        created_user = self.admin_client.add_user(username=username,
                                                  email=email,
                                                  enabled=True,
                                                  defaultRegion=default_region,
                                                  domainId=domain_id,
                                                  password="Gadmpass8")

        self.assertEqual(created_user.status_code, 201,
                         msg="Response for create user is not 201.")
        # Delete user after test completion
        self.addCleanup(self.service_client.delete_user_hard,
                        userId=created_user.entity.id)
        self.addCleanup(self.admin_client.delete_user,
                        userId=created_user.entity.id)

        create_question_resp = self.admin_client.create_question(
            question=question)
        self.assertEqual(create_question_resp.status_code, 201,
                         msg="Response for create question is not 201.")
        question_id = create_question_resp.headers['location'].split('/')[-1]
        # delete question after test completion
        self.addCleanup(self.admin_client.delete_question,
                        questionId=question_id)

        create_secret_qa_resp = self.admin_client.create_secret_qa(
            userId=created_user.entity.id,
            questionId=question_id,
            answer=random_string(prefix=answer, size=101))
        self.assertEqual(create_secret_qa_resp.status_code, 400,
                         msg="Response for create secret question with "
                             "answer > 100 characters is not 400.")

    @attr('regression', type='negative')
    def test_update_secret_qa_attr_length(self):
        """
        Testing update secret question functionality with long answer than
        expected.
        failure should return 400
        """
        question = rand_name('this is a test question')
        answer = "Test answer"
        created_user = self.create_user()

        create_question_resp = self.admin_client.create_question(
            question=question)
        self.assertEqual(create_question_resp.status_code, 201,
                         msg="Response for create question is not 201.")
        question_id = create_question_resp.headers['location'].split('/')[-1]
        # delete question after test completion
        self.addCleanup(self.admin_client.delete_question,
                        questionId=question_id)

        create_secret_qa_resp = self.admin_client.create_secret_qa(
            userId=created_user.entity.id,
            questionId=question_id,
            answer=answer)
        self.assertEqual(create_secret_qa_resp.status_code, 200,
                         msg="Response for create secret question is not 200.")

        update_secret_qa_resp = self.admin_client.update_secret_qa(
            userId=created_user.entity.id,
            question=random_string(prefix=question, size=1001),
            answer=answer)
        self.assertEqual(update_secret_qa_resp.status_code, 400,
                         msg="Response for update Secret Question with "
                             "question > 1000 characters is not 400.")

        update_secret_qa_resp = self.admin_client.update_secret_qa(
            userId=created_user.entity.id,
            question=question,
            answer=random_string(prefix=answer, size=101))
        self.assertEqual(update_secret_qa_resp.status_code, 400,
                         msg="Response for create secret question with "
                             "answer > 100 characters is not 400.")

    @attr('regression', type='negative')
    def test_create_domain_with_long_name(self):
        """
        Testing create domain functionality with long name than
        expected.
        failure should return 400
        """
        domain_id = random.randrange(100000000, 999999999)
        name = rand_name("Test Domain Name")
        description = "Test Description"
        create_domain_resp = self.admin_client.create_domain(
            id=domain_id,
            name=random_string(prefix=name, size=101),
            description=description)
        self.assertEqual(create_domain_resp.status_code, 400,
                         msg="Response for create domain with name > 100 "
                             "characters is not 400.")

    @attr('regression', type='negative')
    def test_create_domain_with_long_description(self):
        """
        Testing create domain functionality with long description than
        expected.
        failure should return 400
        """
        domain_id = random.randrange(100000000, 999999999)
        name = rand_name("Test Domain Name")
        description = "Test Description"

        create_domain_resp = self.admin_client.create_domain(
            id=domain_id,
            name=name,
            description=random_string(prefix=description, size=1001))
        self.assertEqual(create_domain_resp.status_code, 400,
                         msg="Response for create domain with description > "
                             "1000 characters is not 400.")

    @attr('regression', type='negative')
    def test_update_domain_name_attr_length(self):
        """
        Testing update domain functionality with long name than expected.
        failure should return 400
        """
        domain_id = random.randrange(100000000, 999999999)
        name = rand_name("Test Domain Name")
        description = "Test Description"
        create_domain_resp = self.admin_client.create_domain(
            id=domain_id,
            name=name,
            description=description)
        self.assertEqual(create_domain_resp.status_code, 201,
                         msg="Response for create domain is not 201.")
        # Delete domain after test completion
        self.addCleanup(self.admin_client.delete_domain,
                        domainId=create_domain_resp.entity.id)

        update_domain_resp = self.admin_client.update_domain(
            domainId=create_domain_resp.entity.id,
            name=random_string(prefix=name, size=101))
        self.assertEqual(update_domain_resp.status_code, 400,
                         "Response for update domain name with value"
                         " > 100 characters is not 400.")

    @attr('regression', type='negative')
    def test_update_domain_description_attr_length(self):
        """
        Testing update domain functionality with long description than
        expected.
        failure should return 400
        """
        domain_id = random.randrange(100000000, 999999999)
        name = rand_name("Test Domain Name")
        description = "Test Description"
        create_domain_resp = self.admin_client.create_domain(
            id=domain_id,
            name=name,
            description=description)
        self.assertEqual(create_domain_resp.status_code, 201,
                         msg="Response for create domain is not 201.")
        # Delete domain after test completion
        self.addCleanup(self.admin_client.delete_domain,
                        domainId=create_domain_resp.entity.id)

        update_domain_resp = self.admin_client.update_domain(
            domainId=create_domain_resp.entity.id,
            description=random_string(prefix=description, size=1001))
        self.assertEqual(update_domain_resp.status_code, 400,
                         msg="Response for update domain description with "
                             "value > 100 characters is not 400")