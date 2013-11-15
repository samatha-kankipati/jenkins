import requests

from ccengine.common.tools.datagen import rand_name
from ccengine.common.tools.datagen import random_int
from testrepo.common.testfixtures.identity.v2_0.identity \
                import BaseIdentityFixture
from ccengine.common.decorators import attr


class GetRolesPagingTest(BaseIdentityFixture):

    @classmethod
    def setUpClass(cls):
        super(GetRolesPagingTest, cls).setUpClass()

        token = cls.service_client.authenticate_user_password(
                    cls.config.identity_api.service_username,
                    cls.config.identity_api.service_password).entity.token.id

        cls.service_client.token = token

    @classmethod
    def tearDownClass(cls):
        pass

    @attr('regression', type='positive')
    def test_list_roles_returns_valid_link_headers(self):
        '''
        @summary: list roles returns valid link headers
        '''
        response = self.service_client.list_roles(limit=1, marker=3)
        self._status_assertion(response.status_code, 200)

        links = response.links
        for link in links:
            link_response = self._follow_link(link,
                                              links,
                                              self.service_client.list_roles)
            self._status_assertion(link_response.status_code, 200)

    @attr('regression', type='positive')
    def test_list_roles_returns_only_first_and_prev_when_on_last_page(self):
        '''
        @summary: list roles returns only first and prev when on last page
        '''
        response = self.service_client.list_roles(limit=1, marker=0)

        response = self._follow_link('last',
                                     response.links,
                                     self.service_client.list_roles)
        for key in response.links:
            self.assertIn(key,
                          ['prev', 'first'],
                          msg='link: {0} found when on last page'.format(key))

    @attr('regression', type='positive')
    def test_list_roles_returns_valid_first_link_when_on_last_page(self):
        '''
        @summary: list roles returns valid first link when on last page
        '''
        response = self.service_client.list_roles(limit=1, marker=0)
        response = self._follow_link('last',
                                     response.links,
                                     self.service_client.list_roles)

        response = self._follow_link('first',
                                     response.links,
                                     self.service_client.list_roles)
        self._status_assertion(response.status_code, 200)
        self.assertNotEqual(len(response.entity), 0, msg='first link search is empty')

    @attr('regression', type='positive')
    def test_list_roles_returns_valid_prev_link_when_on_last_page(self):
        '''
        @summary: list roles returns valid prev link when on last page
        '''
        response = self.service_client.list_roles(limit=1, marker=0)
        response = self._follow_link('last',
                                     response.links,
                                     self.service_client.list_roles)

        response = self._follow_link('prev',
                                     response.links,
                                     self.service_client.list_roles)
        self._status_assertion(response.status_code, 200)
        self.assertNotEqual(len(response.entity), 0, msg='prev link search is empty')

    @attr('regression', type='positive')
    def test_list_roles_returns_no_links_when_indexed_past_total_results(self):
        '''
        @summary: list roles returns no links when indexed past total results
        '''
        response = self.service_client.list_roles(limit=1, marker=1000000000000)

        self.assertEqual(len(response.links),
                         0,
                         msg='Links returned when index out of bounds')

    @attr('regression', type='positive')
    def test_list_roles_returns_only_last_and_next_when_on_first_page(self):
        '''
        @summary: list roles returns only last and next when on first page
        '''
        response = self.service_client.list_roles(limit=1, marker=0)

        for key in response.links:
            self.assertIn(key,
                          ['last', 'next'],
                          msg='link: {0} found when on first page'.format(key))

    @attr('regression', type='positive')
    def test_list_roles_returns_valid_last_link_when_on_first_page(self):
        '''
        @summary: list roles returns valid last link when on first page
        '''
        response = self.service_client.list_roles(limit=1, marker=0)
        response = self._follow_link('last',
                                     response.links,
                                     self.service_client.list_roles)

        self._status_assertion(response.status_code, 200)

    @attr('regression', type='positive')
    def test_list_roles_returns_valid_next_link_when_on_first_page(self):
        '''
        @summary: list roles returns valid next link when on first page
        '''
        response = self.service_client.list_roles(limit=1, marker=0)
        response = self._follow_link('next',
                                     response.links,
                                     self.service_client.list_roles)

        self._status_assertion(response.status_code, 200)

