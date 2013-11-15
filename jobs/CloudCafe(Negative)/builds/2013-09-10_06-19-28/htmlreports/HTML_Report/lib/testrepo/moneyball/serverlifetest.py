

__author__ = 'ram5454'
from ccengine.clients.moneyball.moneyball_client import MoneyballAPIClient
from testrepo.common.testfixtures.fixtures import BaseTestFixture
class serverlifetest(BaseTestFixture):

    @classmethod
    def setUpClass(cls):
        super(serverlifetest, cls).setUpClass()
        cls.client = MoneyballAPIClient(cls.config.moneyball.base_url)

    #def test_serverlife_for_new_customer(self):

    #def test_serverlife_for_bad_account(self):

    #def test_sl_for_1Ns_0Nsu_noLU_defaultRAM(self):





