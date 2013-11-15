from testrepo.common.testfixtures.loggingaas import PairingFixture


class PairingTests(PairingFixture):
    @classmethod
    def setUpClass(cls):
        super(PairingTests, cls).setUpClass()

    def setUp(self):
        super(PairingTests, self).setUp()

    def tearDown(self):
        pass

    def test_pairing(self):
        cfg_personality = self.config.loggingaas.personality

        resp_dict = self._pair_worker()

        resp_obj = resp_dict['response_object']
        self.assertTrue(cfg_personality in resp_obj.personality_module)

    def test_retrieval_of_worker_config(self):
        resp_dict = self._pair_worker()

        response = self.provider.load_configuration(
            worker_id=resp_dict['worker_id'],
            worker_token=resp_dict['worker_token'])

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.entity)

        workers = response.entity.pipeline_workers
        self.assertIsNotNone(workers)

    def test_update_worker_status(self):
        resp_dict = self._pair_worker()

        response = self.provider.register(
            worker_id=resp_dict['worker_id'],
            worker_token=resp_dict['worker_token'],
            status='online')

        self.assertEqual(200, response.status_code)
