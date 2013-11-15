from testrepo.common.testfixtures.identity.v2_0.identity import \
    IdentityAdminFixture
from ccengine.common.decorators import attr


class AdminSecretQATest(IdentityAdminFixture):
    @classmethod
    def setUpClass(cls):
        super(AdminSecretQATest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        pass

    @attr('smoke', type='positive')
    def test_admin_get_user_secret_qa(self):
        normal_response_codes = [200, 203]
        get_user = self.public_client.get_user_by_name(
            name=self.config.identity_api.username)

        self.assertIn(get_user.status_code, normal_response_codes,
                      msg='Admin get user by name expected %s recieved %s' %
                          (normal_response_codes, get_user.status_code))

        user_qa = self.admin_client.get_user_secret_qa(
            user_id=get_user.entity.id)

        self.assertIn(user_qa.status_code, normal_response_codes,
                      msg='Admin get user secret QA expected %s recieved %s' %
                          (normal_response_codes, user_qa.status_code))

    @attr('smoke', type='positive')
    def test_admin_get_user_secret_qa_list(self):
        normal_response_codes = [200, 203]
        get_user = self.public_client.get_user_by_name(
            name=self.config.identity_api.username)

        self.assertIn(get_user.status_code, normal_response_codes,
                      msg='Admin get user by name expected %s recieved %s' %
                          (normal_response_codes, get_user.status_code))

        user_qa = self.admin_client.get_user_secret_qa_list(
            user_id=get_user.entity.id)

        self.assertEqual(user_qa.status_code, 200,
                         msg='Admin get user secret QA list expected 200 '
                             'recieved %s' % user_qa.status_code)

    @attr('smoke', type='positive')
    def test_admin_update_secret_qa(self):
        normal_response_codes = [200, 203]
        qst = "what is the airspeed velocity of an unladen swallow"
        anw = "aaaaaaaaaaaaaarrrgghhh!"
        updated_qst = "Who is your favorite super hero?"
        updated_anw = "Wolverine"
        question = self.admin_client.create_question(question=qst)
        question_id = question.headers['location'].split('/')[-1]

        self.assertEqual(question.status_code, 201,
                         msg="Admin create question expected response 201 "
                             "received %s" % question.status_code)

        get_user = self.public_client.get_user_by_name(
            name=self.config.identity_api.username)

        self.assertIn(get_user.status_code, normal_response_codes,
                      msg='Admin get user by name expected %s recieved %s' %
                          (normal_response_codes, get_user.status_code))

        create_answer = self.admin_client.create_secret_qa(
            answer=anw,
            user_id=get_user.entity.id,
            question_id=question_id)

        self.assertEqual(create_answer.status_code, 200,
                         msg="Admin create secret QA expected response 200 "
                             "received %s" % create_answer.status_code)

        update_answer = self.admin_client.update_secret_qa(
            answer=updated_anw,
            user_id=get_user.entity.id,
            question=updated_qst)

        self.assertEqual(update_answer.status_code, 200,
                         msg="Admin update secret QA expected 200 "
                             "received %s" % update_answer.status_code)

        self.addCleanup(self.admin_client.delete_question,
                        question_id=question_id)

    @attr('smoke', type='positive')
    def test_admin_create_secret_qa(self):
        normal_response_codes = [200, 203]
        qst = "what is the airspeed velocity of an unladen swallow"
        anw = "aaaaaaaaaaaaaarrrgghhh!"
        question = self.admin_client.create_question(question=qst)
        question_id = question.headers['location'].split('/')[-1]

        self.assertEqual(question.status_code, 201,
                         msg="Admin create question expected response 201 "
                             "received %s" % question.status_code)

        get_user = self.public_client.get_user_by_name(
            name=self.config.identity_api.username)

        self.assertIn(get_user.status_code, normal_response_codes,
                      msg='Admin get user by name expected %s recieved %s' %
                          (normal_response_codes, get_user.status_code))

        create_answer = self.admin_client.create_secret_qa(
            answer=anw,
            user_id=get_user.entity.id,
            question_id=question_id)

        self.assertEqual(create_answer.status_code, 200,
                         msg="Admin create secret QA expected response 200 "
                             "received %s" % create_answer.status_code)

        self.addCleanup(self.admin_client.delete_question,
                        question_id=question_id)

    @attr('smoke', type='positive')
    def test_admin_get_questions(self):
        get_questions = self.admin_client.get_questions()

        self.assertEqual(get_questions.status_code, 200,
                         msg="Admin get questions expected response 200 "
                             "received %s" % get_questions.status_code)

    @attr('smoke', type='positive')
    def test_get_question(self):
        qst = "What's your fathers name?"
        question = self.admin_client.create_question(question=qst)
        question_id = question.headers['location'].split('/')[-1]

        self.assertEqual(question.status_code, 201,
                         msg="Admin create question expected response 201 "
                             "received %s" % question.status_code)

        get_question = self.admin_client.get_question(question_id=question_id)

        self.assertEqual(get_question.status_code, 200,
                         msg="Admin get question expected response 200 "
                             "received %s" % get_question.status_code)

        self.addCleanup(self.admin_client.delete_question,
                        question_id=question_id)

    @attr('smoke', type='positive')
    def test_admin_create_question(self):
        qst = "what is the airspeed velocity of an unladen swallow"
        question = self.admin_client.create_question(question=qst)
        question_id = question.headers['location'].split('/')[-1]

        self.assertEqual(question.status_code, 201,
                         msg="Admin create question expected response 201 "
                             "received %s" % question.status_code)

        self.addCleanup(self.admin_client.delete_question,
                        question_id=question_id)

    @attr('smoke', type='positive')
    def test_admin_update_question(self):
        qst = "what is the airspeed velocity of an unladen swallow"
        upd_qst = "what is the airspeed velocity of an unladen buzzard"
        question = self.admin_client.create_question(question=qst)
        question_id = question.headers['location'].split('/')[-1]

        self.assertEqual(question.status_code, 201,
                         msg="Admin create question expected response 201 "
                             "received %s" % question.status_code)

        update_question = self.admin_client.update_question(
            question=upd_qst,
            question_id=question_id)

        self.assertEqual(update_question.status_code, 204,
                         msg="Admin update question expected response 204 "
                             "received %s" % update_question.status_code)

        self.addCleanup(self.admin_client.delete_question,
                        question_id=question_id)

    @attr('smoke', type='positive')
    def test_admin_delete_question(self):
        qst = "what is the airspeed velocity of an unladen swallow"
        question = self.admin_client.create_question(question=qst)
        question_id = question.headers['location'].split('/')[-1]

        self.assertEqual(question.status_code, 201,
                         msg="Admin create question expected response 201 "
                             "received %s" % question.status_code)

        del_question = self.admin_client.delete_question(
            question_id=question_id)

        self.assertEqual(del_question.status_code, 204,
                         msg="Admin delete question expected response 204 "
                             "received %s" % del_question.status_code)

        get_question = self.admin_client.get_question(question_id=question_id)

        self.assertEqual(get_question.status_code, 404,
                         msg="Admin get question expected response 404 "
                             "received %s" % get_question.status_code)
