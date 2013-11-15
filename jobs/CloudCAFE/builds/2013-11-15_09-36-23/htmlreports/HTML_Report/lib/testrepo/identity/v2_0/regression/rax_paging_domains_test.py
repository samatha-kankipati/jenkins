import requests

from ccengine.common.tools.datagen import rand_name
from ccengine.common.tools.datagen import random_int
from testrepo.common.testfixtures.identity.v2_0.identity \
                import BaseIdentityFixture
from ccengine.common.decorators import attr


class GetDomainsPagingTest(BaseIdentityFixture):

    @classmethod
    def setUpClass(cls):
        super(GetDomainsPagingTest, cls).setUpClass()

        token = cls.service_client.authenticate_user_password(
                    cls.config.identity_api.service_username,
                    cls.config.identity_api.service_password).entity.token.id

        cls.service_client.token = token

    @classmethod
    def tearDownClass(cls):
        pass

    @attr('regression', type='positive')
    def test_get_domains_returns_valid_link_headers(self):
        response = self.service_client.get_domains(limit=1, marker=3)
        self._status_assertion(response.status_code, 200)

        links = response.links
        for link in links:
            link_response = self._follow_link(link,
                                              links,
                                              self.service_client.get_domains)
            self._status_assertion(link_response.status_code, 200)

    @attr('regression', type='positive')
    def test_get_domains_returns_only_first_and_prev_when_on_last_page(self):
        response = self.service_client.get_domains(limit=1, marker=0)

        response = self._follow_link('last',
                                     response.links,
                                     self.service_client.get_domains)
        for key in response.links:
            self.assertIn(key,
                          ['prev', 'first'],
                          msg='link: {0} found when on last page'.format(key))

    @attr('regression', type='positive')
    def test_get_domains_returns_valid_first_link_when_on_last_page(self):
        response = self.service_client.get_domains(limit=1, marker=0)
        response = self._follow_link('last',
                                     response.links,
                                     self.service_client.get_domains)

        response = self._follow_link('first',
                                     response.links,
                                     self.service_client.get_domains)
        self._status_assertion(response.status_code, 200)
        self.assertNotEqual(len(response.entity), 0, msg='first link search is empty')

    @attr('regression', type='positive')
    def test_get_domains_returns_valid_prev_link_when_on_last_page(self):
        response = self.service_client.get_domains(limit=1, marker=0)
        response = self._follow_link('last',
                                     response.links,
                                     self.service_client.get_domains)

        response = self._follow_link('prev',
                                     response.links,
                                     self.service_client.get_domains)
        self._status_assertion(response.status_code, 200)
        self.assertNotEqual(len(response.entity), 0, msg='prev link search is empty')

    @attr('regression', type='positive')
    def test_get_domains_returns_no_links_when_indexed_past_total_results(self):
        response = self.service_client.get_domains(limit=1, marker=1000000000000)

        self.assertEqual(len(response.links),
                         0,
                         msg='Links returned when index out of bounds')

    @attr('regression', type='positive')
    def test_get_domains_returns_only_last_and_next_when_on_first_page(self):
        response = self.service_client.get_domains(limit=1, marker=0)

        for key in response.links:
            self.assertIn(key,
                          ['next', 'last'],
                          msg='link: {0} found when on first page'.format(key))

    @attr('regression', type='positive')
    def test_get_domains_returns_valid_last_link_when_on_first_page(self):
        response = self.service_client.get_domains(limit=1, marker=0)

        response = self._follow_link('last',
                                     response.links,
                                     self.service_client.get_domains)
        self._status_assertion(response.status_code, 200)

    @attr('regression', type='positive')
    def test_get_domains_returns_valid_next_link_when_on_first_page(self):
        response = self.service_client.get_domains(limit=1, marker=0)
        response = self._follow_link('next',
                                     response.links,
                                     self.service_client.get_domains)
        self._status_assertion(response.status_code, 200)

