import requests

from ccengine.common.tools.datagen import rand_name
from ccengine.common.tools.datagen import random_int
from testrepo.common.testfixtures.identity.v2_0.identity \
                import BaseIdentityFixture
from ccengine.common.decorators import attr


class UsersPagingTest(BaseIdentityFixture):

    @classmethod
    def setUpClass(cls):
        super(UsersPagingTest, cls).setUpClass()

        token = cls.service_client.authenticate_user_password(
                    cls.config.identity_api.service_username,
                    cls.config.identity_api.service_password).entity.token.id

        cls.service_client.token = token

        #Create Role to Add to Users
        cls.role = cls.service_client.add_role(rand_name('role'),
                                               description='description').entity

        #Create Users to retrieve
        resp = cls.userOne = cls.service_client.add_user(rand_name('user'),
                                                         'test@email.com').entity
        resp = cls.service_client.add_role_to_user(cls.userOne.id, cls.role.id)

        resp = cls.userTwo = cls.service_client.add_user(rand_name('user'),
                                                         'test@email.com').entity
        resp = cls.service_client.add_role_to_user(cls.userTwo.id, cls.role.id)

        resp = cls.userThree = cls.service_client.add_user(rand_name('user'),
                                                           'test@email.com').entity
        resp = cls.service_client.add_role_to_user(cls.userThree.id, cls.role.id)

        resp = cls.userFour = cls.service_client.add_user(rand_name('user'),
                                                          'test@email.com').entity
        resp = cls.service_client.add_role_to_user(cls.userFour.id, cls.role.id)

        resp = cls.userFive = cls.service_client.add_user(rand_name('user'),
                                                          'test@email.com').entity
        resp = cls.service_client.add_role_to_user(cls.userFive.id, cls.role.id)

    @classmethod
    def tearDownClass(cls):
        cls.service_client.delete_user(cls.userOne.id)
        cls.service_client.delete_user_hard(cls.userOne.id)
        cls.service_client.delete_user(cls.userTwo.id)
        cls.service_client.delete_user_hard(cls.userTwo.id)
        cls.service_client.delete_user(cls.userThree.id)
        cls.service_client.delete_user_hard(cls.userThree.id)
        cls.service_client.delete_user(cls.userFour.id)
        cls.service_client.delete_user_hard(cls.userFour.id)
        cls.service_client.delete_user(cls.userFive.id)
        cls.service_client.delete_user_hard(cls.userFive.id)

        cls.service_client.delete_role(cls.role.id)

    @attr('regression', type='positive')
    def test_list_users_returns_valid_link_headers(self):
        '''
        @summary: list users returns valid link headers
        '''
        response = self.service_client.list_users(limit=1, marker=3)
        self._status_assertion(response.status_code, 200)

        links = response.links
        for link in links:
            link_response = self._follow_link(link,
                                              links,
                                              self.service_client.list_users)
            self._status_assertion(link_response.status_code, 200)

    @attr('regression', type='positive')
    def test_list_users_returns_only_first_and_prev_when_on_last_page(self):
        '''
        @summary: list users returns only first and prev when on last page
        '''
        response = self.service_client.list_users(limit=1, marker=0)

        response = self._follow_link('last',
                                     response.links,
                                     self.service_client.list_users)
        for key in response.links:
            self.assertIn(key,
                          ['prev', 'first'],
                          msg='link: {0} found when on last page'.format(key))

    @attr('regression', type='positive')
    def test_list_users_returns_valid_first_link_when_on_last_page(self):
        '''
        @summary: list users returns valid first link when on last page
        '''
        response = self.service_client.list_users(limit=1, marker=0)
        response = self._follow_link('last',
                                     response.links,
                                     self.service_client.list_users)

        response = self._follow_link('first',
                                     response.links,
                                     self.service_client.list_users)
        self._status_assertion(response.status_code, 200)
        self.assertNotEqual(len(response.entity), 0, msg='first link search is empty')

    @attr('regression', type='positive')
    def test_list_users_returns_valid_prev_link_when_on_last_page(self):
        '''
        @summary: list users returns valid prev link when on last page
        '''
        response = self.service_client.list_users(limit=1, marker=0)
        response = self._follow_link('last',
                                     response.links,
                                     self.service_client.list_users)

        response = self._follow_link('prev',
                                     response.links,
                                     self.service_client.list_users)
        self._status_assertion(response.status_code, 200)
        self.assertNotEqual(len(response.entity), 0, msg='prev link search is empty')

    @attr('regression', type='positive')
    def test_list_users_returns_no_links_when_indexed_past_total_results(self):
        '''
        @summary: list users returns no links when indexed past total results
        '''
        response = self.service_client.list_users(limit=1, marker=1000000000000)

        self.assertEqual(len(response.links),
                         0,
                         msg='Links returned when index out of bounds')

    @attr('regression', type='positive')
    def test_list_users_returns_only_last_and_next_when_on_first_page(self):
        '''
        @summary: list users returns only last and next when on first page
        '''
        response = self.service_client.list_users(limit=1, marker=0)

        for key in response.links:
            self.assertIn(key,
                          ['next', 'last'],
                          msg='link: {0} found when on first page'.format(key))

    @attr('regression', type='positive')
    def test_list_users_returns_valid_last_link_when_on_first_page(self):
        '''
        @summary: list users returns valid last link when on first page
        '''
        response = self.service_client.list_users(limit=1, marker=0)
        response = self._follow_link('last',
                                     response.links,
                                     self.service_client.list_users)
        self._status_assertion(response.status_code, 200)

    @attr('regression', type='positive')
    def test_list_users_returns_valid_next_link_when_on_first_page(self):
        '''
        @summary: list users returns valid next link when on first page
        '''
        response = self.service_client.list_users(limit=1, marker=0)
        response = self._follow_link('next',
                                     response.links,
                                     self.service_client.list_users)
        self._status_assertion(response.status_code, 200)

    @attr('regression', type='positive')
    def test_list_users_with_role_returns_valid_link_headers(self):
        '''
        @summary: list users with role returns valid link headers
        '''
        response = self.service_client.list_users_with_role(self.role.id, limit=1, marker=3)
        self._status_assertion(response.status_code, 200)

        links = response.links
        for link in links:
            link_response = self._follow_link(link,
                                              links,
                                              self.service_client.list_users_with_role,
                                              method_args=self.role.id)
            self._status_assertion(link_response.status_code, 200)

    @attr('regression', type='positive')
    def test_list_users_with_role_returns_only_first_and_prev_when_on_last_page(self):
        '''
        @summary: list users with role returns only first and prev when on last page
        '''
        response = self.service_client.list_users_with_role(self.role.id, limit=1, marker=0)

        response = self._follow_link('last',
                                     response.links,
                                     self.service_client.list_users_with_role,
                                     method_args=self.role.id)
        for key in response.links:
            self.assertIn(key,
                          ['prev', 'first'],
                          msg='link: {0} found when on last page'.format(key))

    @attr('regression', type='positive')
    def test_list_users_with_role_returns_valid_first_link_when_on_last_page(self):
        '''
        @summary: list users with role returns valid first link when on last page
        '''
        response = self.service_client.list_users_with_role(self.role.id, limit=1, marker=0)
        response = self._follow_link('last',
                                     response.links,
                                     self.service_client.list_users_with_role,
                                     method_args=self.role.id)

        response = self._follow_link('first',
                                     response.links,
                                     self.service_client.list_users_with_role,
                                     method_args=self.role.id)
        self._status_assertion(response.status_code, 200)
        self.assertNotEqual(len(response.entity), 0, msg='first link search is empty')

    def test_list_users_with_role_returns_valid_prev_link_when_on_last_page(self):
        '''
        @summary: list users with role returns valid prev link when on last page
        '''
        response = self.service_client.list_users_with_role(self.role.id, limit=1, marker=0)
        response = self._follow_link('last',
                                     response.links,
                                     self.service_client.list_users_with_role,
                                     method_args=self.role.id)

        response = self._follow_link('prev',
                                     response.links,
                                     self.service_client.list_users_with_role,
                                     method_args=self.role.id)
        self._status_assertion(response.status_code, 200)
        self.assertNotEqual(len(response.entity), 0, msg='prev link search is empty')

    def test_list_users_with_role_returns_no_links_when_indexed_past_total_results(self):
        '''
        @summary: list users with role returns no links when indexed past total results
        '''
        response = self.service_client.list_users_with_role(self.role.id, limit=1, marker=1000000000000)

        self.assertEqual(len(response.links),
                         0,
                         msg='Links returned when index out of bounds')

    def test_list_users_with_role_returns_only_last_and_next_when_on_first_page(self):
        '''
        @summary: list users with role returns only last and next when on first page
        '''
        response = self.service_client.list_users_with_role(self.role.id, limit=1, marker=0)

        for key in response.links:
            self.assertIn(key,
                          ['next', 'last'],
                          msg='link: {0} found when on first page'.format(key))

    def test_list_users_with_role_returns_valid_last_link_when_on_first_page(self):
        '''
        @summary: list users with role returns valid last link when on first page
        '''
        response = self.service_client.list_users_with_role(self.role.id, limit=1, marker=0)
        response = self._follow_link('last',
                                     response.links,
                                     self.service_client.list_users_with_role,
                                     method_args=self.role.id)
        self._status_assertion(response.status_code, 200)

    def test_list_users_with_role_returns_valid_next_link_when_on_first_page(self):
        '''
        @summary: list users with role returns valid next link when on first page
        '''
        response = self.service_client.list_users_with_role(self.role.id, limit=1, marker=0)
        response = self._follow_link('next',
                                     response.links,
                                     self.service_client.list_users_with_role,
                                     method_args=self.role.id)
        self._status_assertion(response.status_code, 200)


