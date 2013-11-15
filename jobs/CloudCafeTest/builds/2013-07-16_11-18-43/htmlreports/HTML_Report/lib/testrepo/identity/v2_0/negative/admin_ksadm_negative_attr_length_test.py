from ccengine.common.tools.datagen import rand_name
from testrepo.common.testfixtures.identity.v2_0.identity \
    import IdentityAdminFixture
from ccengine.common.decorators import attr
import random


class AdminAttrLenghtTest(IdentityAdminFixture):

    @classmethod
    def setUpClass(cls):
        super(AdminAttrLenghtTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        pass

    def multiply_value(self, value, multiple):
        return value * multiple

    @attr('regression', type='negative')
    def test_create_user_attr_length(self):
        """
        Testing the attribute length - failure should return 400
        """
        username = rand_name("ccadminname_length")
        email = self.config.identity_api.default_email
        domain_id = random.randrange(100000000, 999999999)
        default_region = self.config.identity_api.default_region

        create_user_username = self.admin_client.add_user(
                username=self.multiply_value(username, 100),
                email=email,
                enabled=True,
                defaultRegion=default_region,
                domainId=domain_id,
                password="Gadmpass8")

        self.assertEqual(
                create_user_username.status_code,
                400,
                msg="Create user should return {0} but received {1}".
                format(400, create_user_username.status_code))

        email = self.multiply_value("testbox", 100)
        email_domain = self.config.identity_api.default_email.split('@')
        create_user_email = self.admin_client.add_user(
                username=username,
                email="{0}@{1}".format(email, email_domain[1]),
                enabled=True,
                defaultRegion=default_region,
                domainId=domain_id,
                password="Gadmpass8")

        self.assertEqual(
                create_user_email.status_code,
                400,
                msg="Create user should return {0} but received {1}".
                format(400, create_user_email.status_code))

        email = self.config.identity_api.default_email
        create_user_region = self.admin_client.add_user(
                username=username,
                email=email,
                enabled=True,
                defaultRegion=self.multiply_value(default_region, 100),
                domainId=domain_id,
                password="Gadmpass8")

        self.assertEqual(
                create_user_region.status_code,
                400,
                msg="Create user should return {0} but received {1}".
                format(400, create_user_region.status_code))

        create_user_password = self.admin_client.add_user(
                username=username,
                email=email,
                enabled=True,
                defaultRegion=default_region,
                domainId=domain_id,
                password=self.multiply_value('Gadmpass8', 100))

        self.assertEqual(
                create_user_password.status_code,
                400,
                msg="Create user should return {0} but received {1}".
                format(400, create_user_password.status_code))

    @attr('regression', type='negative')
    def test_update_user_attr_length(self):
        """
        Testing the attribute length - failure should return 400
        """
        username = rand_name("ccadminname_lenght")
        email = self.config.identity_api.default_email
        domain_id = random.randrange(100000000, 999999999)
        default_region = self.config.identity_api.default_region

        create_user_username = self.admin_client.add_user(
                username=username,
                email=email,
                enabled=True,
                defaultRegion=default_region,
                domainId=domain_id,
                password="Gadmpass8")

        self.assertEqual(
                create_user_username.status_code,
                201,
                msg="Create user should return {0} but received {1}".
                format(201, create_user_username.status_code))

        update_user_username = self.admin_client.update_user(
                userId=create_user_username.entity.id,
                username=self.multiply_value(username, 100))

        self.assertEqual(
                update_user_username.status_code,
                400,
                msg="Update username should return {0} but received {1}".
                format(400, create_user_username.status_code))

        email = self.multiply_value("testbox", 100)
        email_domain = self.config.identity_api.default_email.split('@')
        update_user_email = self.admin_client.update_user(
                userId=create_user_username.entity.id,
                email="{0}@{1}".format(email, email_domain[1]))

        self.assertEqual(
                update_user_email.status_code,
                400,
                msg="Update user email should return {0} but received {1}".
                format(400, update_user_email.status_code))

        email = self.config.identity_api.default_email
        update_user_region = self.admin_client.update_user(
                userId=create_user_username.entity.id,
                defaultRegion=self.multiply_value(default_region, 100))

        self.assertEqual(
                update_user_region.status_code,
                400,
                msg="Update user region should return {0} but received {1}".
                format(400, update_user_region.status_code))

        update_user_password = self.admin_client.update_user(
                userId=create_user_username.entity.id,
                password=self.multiply_value('Gadmpass8', 100))

        self.assertEqual(
                update_user_password.status_code,
                400,
                msg="Update user password should return {0} but received {1}".
                format(400, update_user_password.status_code))

        delete_user = self.public_client.delete_user(
                userId=create_user_username.entity.id)
        self.assertEqual(
                delete_user.status_code,
                204,
                msg='Delete user expected response {0} received {1}'.
                format(204, delete_user.status_code))
        hard_delete_user = self.service_client.delete_user_hard(
                userId=create_user_username.entity.id)
        self.assertEqual(
                hard_delete_user.status_code,
                204,
                msg='Hard delete user expected response {0} received {1}'.
                format(204, hard_delete_user.status_code))

    @attr('regression', type='negative')
    def test_update_user_credentials_attr_length(self):
        """
        Testing the attribute length - failure should return 400
        """
        username = rand_name("ccadminname_lenght")
        email_domain = self.config.identity_api.default_email.split('@')
        email = username + "@{0}".format(email_domain[1])
        domain_id = random.randrange(100000000, 999999999)
        default_region = self.config.identity_api.default_region
        password = self.config.identity_api.password
        create_user = self.admin_client.add_user(
                username=username,
                email=email,
                enabled=True,
                defaultRegion=default_region,
                domainId=domain_id,
                password=password)

        update_cred = self.admin_client.update_user_credentials_password(
                create_user.entity.id,
                username,
                self.multiply_value(password, 100))

        delete_user = self.public_client.delete_user(
                userId=create_user.entity.id)
        hard_delete_user = self.service_client.delete_user_hard(
                userId=create_user.entity.id)

        self.assertEqual(
                create_user.status_code,
                201,
                msg="Create user should return {0} but received {1}".
                format(200, create_user.status_code))
        self.assertEqual(
                update_cred.status_code,
                400,
                msg="Update credentials should return {0} but received {1}".
                format(400, update_cred.status_code))
        self.assertEqual(
                delete_user.status_code,
                204,
                msg='Delete user expected response {0} received {1}'.
                format(204, delete_user.status_code))
        self.assertEqual(
                hard_delete_user.status_code,
                204,
                msg='Hard delete user expected response {0} received {1}'.
                format(204, hard_delete_user.status_code))

    @attr('regression', type='negative')
    def test_add_group_attr_length(self):
        """
        Testing the attribute length - failure should return 400
        """
        name = rand_name('Group_Name')
        description = 'Description'

        add_group = self.admin_client.add_group(
                name=self.multiply_value(name, 100),
                description=description)
        self.assertEqual(
                add_group.status_code,
                400,
                msg="Add group should return {0} but received {1}".
                format(400, add_group.status_code))

        add_group = self.admin_client.add_group(
                name=self.multiply_value('name', 100),
                description=self.multiply_value(description, 100))
        self.assertEqual(
                add_group.status_code,
                400,
                msg="Add group should return {0} but received {1}".
                format(400, add_group.status_code))

    @attr('regression', type='negative')
    def test_update_group_attr_length(self):
        name = rand_name('Group_Name')
        description = 'Description'

        add_group = self.admin_client.add_group(
                name=name,
                description=description)
        self.assertEqual(
                add_group.status_code,
                201,
                msg="Add group should return {0} but received {1}".
                format(200, add_group.status_code))

        """
        Check with CloudCafe team -- in update group do we need to have
        both name and description as mandatory -- pravin
        """
        update_group_name = self.admin_client.update_group(
                groupId=add_group.entity.id,
                name=self.multiply_value(name, 100),
                description=description)
        self.assertEqual(
                update_group_name.status_code,
                400,
                msg="Update group should return {0} but received {1}".
                format(400, update_group_name.status_code))

        update_group_desc = self.admin_client.update_group(
                groupId=add_group.entity.id,
                name=name,
                description=self.multiply_value(description, 1000))
        self.assertEqual(
                update_group_desc.status_code,
                400,
                msg="Update group should return {0} but received {1}".
                format(400, update_group_desc.status_code))

        delete_group = self.admin_client.delete_group(
                groupId=add_group.entity.id)
        self.assertEqual(
                delete_group.status_code,
                204,
                msg="Response is not 204")

    @attr('regression', type='negative')
    def test_add_role_attr_length(self):
        """
        Testing the attribute length - failure should return 400
        """
        name = rand_name('Role_Name')
        description = 'Description'
        add_role = self.admin_client.add_role(
                name=self.multiply_value(name, 100),
                description=description)

        self.assertEqual(
                add_role.status_code,
                400,
                msg="Add role should return {0} but received {1}".
                format(400, add_role.status_code))

        add_role = self.admin_client.add_role(
                name=name,
                description=self.multiply_value(description, 100))

        self.assertEqual(
                add_role.status_code,
                400,
                msg="Add role should return {0} but received {1}".
                format(400, add_role.status_code))

    @attr('regression', type='negative')
    def test_create_question_attr_length(self):
        """
        Testing the attribute length - failure should return 400
        """
        question = rand_name('this is a test question')
        create_question_resp = self.admin_client.create_question(
                question=self.multiply_value(question, 1000))
        self.assertEqual(
                create_question_resp.status_code,
                400,
                msg="Create Question should return {0} but received {1}".
                format(400, create_question_resp.status_code))

    @attr('regression', type='negative')
    def test_update_question_attr_length(self):
        """
        Testing the attribute length - failure should return 400
        """
        question = rand_name('this is a test question')

        create_question_resp = self.admin_client.create_question(
                question=question)
        question_id = create_question_resp.headers['location'].split('/')[-1]

        self.assertEqual(
                create_question_resp.status_code,
                201,
                msg="Create Question should return {0} but received {1}".
                format(201, create_question_resp.status_code))

        update_question_resp = self.admin_client.update_question(
                questionId=question_id,
                question=self.multiply_value(question, 1000))

        self.assertEqual(
                update_question_resp.status_code,
                400,
                msg="Update Question should return {0} but received {1}".
                format(400, update_question_resp.status_code))

        delete_question_resp = self.admin_client.delete_question(
                questionId=question_id)
        self.assertEqual(
                delete_question_resp.status_code,
                204,
                msg="Delete Question should return {0} but received {1}".
                format(201, delete_question_resp.status_code))

    @attr('regression', type='negative')
    def test_create_secret_qa_attr_length(self):
        """
        Testing the attribute length - failure should return 400
        """
        question = rand_name('this is a test question')
        answer = "This is a test answer"
        username = rand_name("cctestuser")
        email = self.config.identity_api.default_email
        domain_id = random.randrange(100000000, 999999999)
        default_region = self.config.identity_api.default_region

        create_user_username = self.admin_client.add_user(
                username=username,
                email=email,
                enabled=True,
                defaultRegion=default_region,
                domainId=domain_id,
                password="Gadmpass8")

        self.assertEqual(
                create_user_username.status_code,
                201,
                msg="Create user should return {0} but received {1}".
                format(201, create_user_username.status_code))

        create_question_resp = self.admin_client.create_question(
                question=question)
        self.assertEqual(
                create_question_resp.status_code,
                201,
                msg="Create Question should return {0} but received {1}".
                format(201, create_question_resp.status_code))
        question_id = create_question_resp.headers['location'].split('/')[-1]

        create_secret_qa_resp = self.admin_client.create_secret_qa(
                userId=create_user_username.entity.id,
                questionId=question_id,
                answer=self.multiply_value(answer, 100))
        self.assertEqual(
                create_secret_qa_resp.status_code,
                400,
                msg="Create Secret QA should return {0} but received {1}".
                format(400, create_secret_qa_resp.status_code))

        delete_question_resp = self.admin_client.delete_question(
                questionId=question_id)
        self.assertEqual(
                delete_question_resp.status_code,
                204,
                msg="Delete Question should return {0} but received {1}".
                format(204, delete_question_resp.status_code))

        delete_user = self.admin_client.delete_user(
                userId=create_user_username.entity.id)

        self.assertEqual(
                delete_user.status_code,
                204,
                msg="Delete user should return {0} but received {1}".
                format(204, delete_user.status_code))

        delete_user = self.service_client.delete_user_hard(
                userId=create_user_username.entity.id)

        self.assertEqual(
                delete_user.status_code,
                204,
                msg="Delete user should return {0} but received {1}".
                format(204, delete_user.status_code))

    @attr('regression', type='negative')
    def test_update_secret_qa_attr_length(self):
        """
        Testing the attribute length - failure should return 400
        """
        question = rand_name('this is a test question')
        answer = "This is a test answer"
        username = rand_name("cctestuser")
        email = self.config.identity_api.default_email
        domain_id = random.randrange(100000000, 999999999)
        default_region = self.config.identity_api.default_region

        create_user_username = self.admin_client.add_user(
                username=username,
                email=email,
                enabled=True,
                defaultRegion=default_region,
                domainId=domain_id,
                password="Gadmpass8")

        self.assertEqual(
                create_user_username.status_code,
                201,
                msg="Create user should return {0} but received {1}".
                format(201, create_user_username.status_code))

        create_question_resp = self.admin_client.create_question(
                question=question)
        self.assertEqual(
                create_question_resp.status_code,
                201,
                msg="Create Question should return {0} but received {1}".
                format(201, create_question_resp.status_code))
        question_id = create_question_resp.headers['location'].split('/')[-1]

        create_secret_qa_resp = self.admin_client.create_secret_qa(
                userId=create_user_username.entity.id,
                questionId=question_id,
                answer=answer)
        self.assertEqual(
                create_secret_qa_resp.status_code,
                200,
                msg="Create Secret QA should return {0} but received {1}".
                format(200, create_secret_qa_resp.status_code))

        update_secret_qa_resp = self.admin_client.update_secret_qa(
                userId=create_user_username.entity.id,
                question=self.multiply_value(question, 100),
                answer=answer)
        self.assertEqual(
                update_secret_qa_resp.status_code,
                400,
                msg="Update Secret QA should return {0} but received {1}".
                format(400, update_secret_qa_resp.status_code))

        update_secret_qa_resp = self.admin_client.update_secret_qa(
                userId=create_user_username.entity.id,
                question=question,
                answer=self.multiply_value(answer, 100))
        self.assertEqual(
                update_secret_qa_resp.status_code,
                400,
                msg="Update Secret QA should return {0} but received {1}".
                format(400, update_secret_qa_resp.status_code))

        delete_question_resp = self.admin_client.delete_question(
                questionId=question_id)
        self.assertEqual(
                delete_question_resp.status_code,
                204,
                msg="Delete Question should return {0} but received {1}".
                format(204, delete_question_resp.status_code))

        delete_user = self.admin_client.delete_user(
                userId=create_user_username.entity.id)

        self.assertEqual(
                delete_user.status_code,
                204,
                msg="Delete user should return {0} but received {1}".
                format(204, delete_user.status_code))

        delete_user = self.service_client.delete_user_hard(
                userId=create_user_username.entity.id)

        self.assertEqual(
                delete_user.status_code,
                204,
                msg="Delete user should return {0} but received {1}".
                format(204, delete_user.status_code))

    @attr('regression', type='negative')
    def test_create_domain_attr_length(self):
        """
        Testing the attribute length - failure should return 400
        """
        domain_id = random.randrange(100000000, 999999999)
        name = rand_name("Test Domain Name")
        description = "Test Description"
        create_domain_resp = self.admin_client.create_domain(
                id=domain_id,
                name=self.multiply_value(name, 100),
                description=description)
        self.assertEqual(
                create_domain_resp.status_code,
                400,
                msg="Create Domain should return {0} but received {1}".
                format(400, create_domain_resp.status_code))

        create_domain_resp = self.admin_client.create_domain(
                id=domain_id,
                name=name,
                description=self.multiply_value(description, 1000))
        self.assertEqual(
                create_domain_resp.status_code,
                400,
                msg="Create Domain should return {0} but received {1}".
                format(400, create_domain_resp.status_code))

    @attr('regression', type='negative')
    def test_update_domain_attr_length(self):
        """
        Testing the attribute length - failure should return 400
        """
        domain_id = random.randrange(100000000, 999999999)
        name = rand_name("Test Domain Name")
        description = "Test Description"
        create_domain_resp = self.admin_client.create_domain(
                id=domain_id,
                name=name,
                description=description)

        self.assertEqual(
                create_domain_resp.status_code,
                201,
                msg="Create Domain should return {0} but received {1}".
                format(201, create_domain_resp.status_code))

        update_domain_resp = self.admin_client.update_domain(
                domainId=create_domain_resp.entity.id,
                name=self.multiply_value(name, 100))
        self.assertEqual(
                update_domain_resp.status_code,
                400,
                msg="Create Domain should return {0} but received {1}".
                format(400, update_domain_resp.status_code))

        update_domain_resp = self.admin_client.update_domain(
                domainId=create_domain_resp.entity.id,
                description=self.multiply_value(description, 1000))
        self.assertEqual(
                update_domain_resp.status_code,
                400,
                msg="Create Domain should return {0} but received {1}".
                format(400, update_domain_resp.status_code))

        delete_domain_resp = self.admin_client.delete_domain(
                domainId=create_domain_resp.entity.id)
        self.assertEqual(
                delete_domain_resp.status_code,
                204,
                msg="Delete Domain should return {0} but received {1}".
                format(204, delete_domain_resp.status_code))
