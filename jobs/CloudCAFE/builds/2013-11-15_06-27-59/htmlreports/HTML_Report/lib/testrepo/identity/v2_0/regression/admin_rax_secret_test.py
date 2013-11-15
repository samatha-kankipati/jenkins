from testrepo.common.testfixtures.identity.v2_0.identity import \
    IdentityAdminFixture
from ccengine.common.decorators import attr
from ccengine.domain.identity.v2_0.response.question import Question
from ccengine.domain.identity.v2_0.response.secret_qa import SecretQA


class SecretTest(IdentityAdminFixture):
    @classmethod
    def setUpClass(cls):
        super(SecretTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        pass

    @attr('regression', type='positive')
    def test_admin_get_user_secret_qa(self):
        qst = "what is the airspeed velocity of an unladen swallow"
        anw = "aaaaaaaaaaaaaarrrgghhh!"

        question = self.admin_client.create_question(question=qst)

        question_id = question.headers['location'].split('/')[-1]

        get_user = self.public_client.get_user_by_name(
            name=self.config.identity_api.username)

        self.admin_client.create_secret_qa(
            answer=anw,
            user_id=get_user.entity.id,
            question_id=question_id)

        user_qa = self.admin_client.get_user_secret_qa(
            user_id=get_user.entity.id)

        self.assertEquals(
            user_qa.entity.question,
            qst,
            msg='Admin get user secret qa expected question {0} recieved '
                '{1}'.format(qst, user_qa.entity.question))

        self.assertEquals(
            user_qa.entity.answer,
            anw,
            msg='Admin get user secret qa expected answer {0} recieved '
                '{1}'.format(anw, user_qa.entity.answer))

        self.addCleanup(self.admin_client.delete_question,
                        question_id=question_id)

    @attr('regression', type='positive')
    def test_admin_get_user_secret_qa_list(self):
        get_user = self.public_client.get_user_by_name(
            name=self.config.identity_api.username)

        user_qa = self.admin_client.get_user_secret_qa_list(
            user_id=get_user.entity.id)

        for qa in user_qa.entity:
            self.assertIsInstance(
                qa,
                SecretQA,
                msg='Admin get user QA expected a SecretQA obj recieved '
                    '{0}'.format(qa))

            self.assertIsNotNone(
                qa.id,
                msg='QA obj expected a question ID recieved '
                    '{0}'.format(qa.id))

            self.assertIsNotNone(
                qa.question,
                msg='QA obj expected a question recieved '
                    '{0}'.format(qa.question))

            self.assertIsNotNone(
                qa.answer,
                msg='QA obj expected an answer recieved '
                    '{0}'.format(qa.answer))

    @attr('regression', type='positive')
    def test_admin_update_secret_qa(self):
        qst = "what is the airspeed velocity of an unladen swallow"
        anw = "aaaaaaaaaaaaaarrrgghhh!"
        updated_qst = "Who is your favorite super hero?"
        updated_anw = "Wolverine"

        question = self.admin_client.create_question(question=qst)

        question_id = question.headers['location'].split('/')[-1]

        get_user = self.public_client.get_user_by_name(
            name=self.config.identity_api.username)

        self.admin_client.create_secret_qa(
            answer=anw,
            user_id=get_user.entity.id,
            question_id=question_id)

        user_qa = self.admin_client.get_user_secret_qa(
            user_id=get_user.entity.id)

        self.assertEquals(
            user_qa.entity.question,
            qst,
            msg='Admin get user secret qa expected question {0} recieved '
                '{1}'.format(qst, user_qa.entity.question))

        self.assertEquals(
            user_qa.entity.answer,
            anw,
            msg='Admin get user secret qa expected answer {0} recieved '
                '{1}'.format(anw, user_qa.entity.answer))

        self.admin_client.update_secret_qa(
            answer=updated_anw,
            user_id=get_user.entity.id,
            question=qst)

        upd_user_qa = self.admin_client.get_user_secret_qa(
            user_id=get_user.entity.id)

        self.assertEquals(
            upd_user_qa.entity.question,
            qst,
            msg='Admin get user secret qa expected question {0} recieved '
                '{1}'.format(updated_qst, upd_user_qa.entity.question))

        self.assertEquals(
            user_qa.entity.answer,
            anw,
            msg='Admin get user secret qa expected answer {0} recieved '
                '{1}'.format(updated_anw, upd_user_qa.entity.answer))

        self.addCleanup(
            self.admin_client.delete_question,
            question_id=question_id)

    @attr('regression', type='positive')
    def test_admin_create_secret_qa(self):
        qst = "what is the airspeed velocity of an unladen swallow"
        anw = "aaaaaaaaaaaaaarrrgghhh!"

        question = self.admin_client.create_question(question=qst)

        question_id = question.headers['location'].split('/')[-1]

        get_user = self.public_client.get_user_by_name(
            name=self.config.identity_api.username)

        self.admin_client.create_secret_qa(
            answer=anw,
            user_id=get_user.entity.id,
            question_id=question_id)

        user_qa = self.admin_client.get_user_secret_qa(
            user_id=get_user.entity.id)

        self.assertEquals(
            user_qa.entity.question,
            qst,
            msg='Admin get user secret qa expected question {0} recieved '
                '{1}'.format(qst, user_qa.entity.question))

        self.assertEquals(
            user_qa.entity.answer,
            anw,
            msg='Admin get user secret qa expected answer {0} recieved '
                '{1}'.format(anw, user_qa.entity.answer))

        self.addCleanup(
            self.admin_client.delete_question,
            question_id=question_id)

    @attr('regression', type='positive')
    def test_admin_get_questions(self):
        questions = self.admin_client.get_questions()

        for question in questions.entity:
            self.assertIsInstance(
                question,
                Question,
                msg='Admin get question expected a Question obj recieved '
                    '{0}'.format(question))

            self.assertIsNotNone(
                question.id,
                msg='question returned expected a question ID recieved '
                    '{0}'.format(question.id))

            self.assertIsNotNone(
                question.question,
                msg='question returned expected a question recieved '
                    '{0}'.format(question.question))

    @attr('regression', type='positive')
    def test_admin_get_question(self):
        qst = "What's your fathers name?"

        question = self.admin_client.create_question(question=qst)

        question_id = question.headers['location'].split('/')[-1]

        get_question = self.admin_client.get_question(question_id=question_id)

        self.assertIsInstance(
            get_question.entity,
            Question,
            msg='Admin get question expected a question obj recieved '
                '{0}'.format(get_question.entity))

        self.assertIsNotNone(
            get_question.entity.id,
            msg='question returned expected a question ID recieved '
                '{0}'.format(get_question.entity.id))

        self.assertEqual(
            int(get_question.entity.id),
            int(question_id),
            msg='Admin get question ID expected {0} recieved {1}'.format(
                question_id,
                get_question.entity.id))

        self.assertEquals(
            get_question.entity.question,
            qst,
            msg='Admin get question expected question {0} recieved '
                '{1}'.format(qst, get_question.entity.question))

        self.addCleanup(self.admin_client.delete_question,
                        question_id=question_id)

    @attr('regression', type='positive')
    def test_admin_create_question(self):
        qst = "what is the airspeed velocity of an unladen swallow"

        question = self.admin_client.create_question(question=qst)

        question_id = question.headers['location'].split('/')[-1]

        get_question = self.admin_client.get_question(question_id=question_id)

        self.assertEquals(
            get_question.entity.question,
            qst,
            msg='Admin get question expected {0} recieved {1}'.format(
                qst, get_question.entity.question))

        self.addCleanup(
            self.admin_client.delete_question,
            question_id=question_id)

    @attr('regression', type='positive')
    def test_admin_update_question(self):
        qst = "what is the airspeed velocity of an unladen swallow"
        upd_qst = "what is the airspeed velocity of an unladen buzzard"

        question = self.admin_client.create_question(question=qst)

        question_id = question.headers['location'].split('/')[-1]

        get_question = self.admin_client.get_question(question_id=question_id)

        self.assertEquals(
            get_question.entity.question,
            qst,
            msg='Admin get question expected {0} recieved {1}'.format(
                qst,
                get_question.entity.question))

        self.admin_client.update_question(
            question=upd_qst,
            question_id=question_id)

        get_question = self.admin_client.get_question(question_id=question_id)

        self.assertEquals(
            get_question.entity.question,
            upd_qst,
            msg='Admin get question expected {0} recieved {1}'.format(
                upd_qst,
                get_question.entity.question))

        self.addCleanup(
            self.admin_client.delete_question,
            question_id=question_id)

    @attr('regression', type='positive')
    def test_admin_delete_question(self):
        qst = "what is the airspeed velocity of an unladen swallow"

        question = self.admin_client.create_question(question=qst)

        question_id = question.headers['location'].split('/')[-1]

        get_question = self.admin_client.get_question(question_id=question_id)

        self.assertIsInstance(
            get_question.entity,
            Question,
            msg='Admin get question expected a question obj recieved '
                '{0}'.format(type(get_question.entity)))

        self.assertEquals(
            get_question.entity.question,
            qst,
            msg='Admin get question expected {0} recieved {1}'.format(
                qst,
                get_question.entity.question))

        self.admin_client.delete_question(question_id=question_id)

        get_question = self.admin_client.get_question(question_id=question_id)

        self.assertIsNone(
            get_question.entity,
            msg='Admin get question '
                'on a deleted question expected None recieved '
                '{0}'.format(get_question.entity))
