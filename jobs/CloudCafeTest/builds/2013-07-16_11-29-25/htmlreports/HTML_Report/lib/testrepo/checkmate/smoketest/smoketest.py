import json
from testrepo.common.testfixtures.checkmate import CheckmateFixture


class SmokeTest(CheckmateFixture):

    def test_components(self):
        ''' Testing Checkmate Components '''
        api_response = self.checkmate_provider.client.get_components()

        self.assertTrue(api_response.ok, "Components get failed with error: \
            '%s' and status code '%s': \n '%s'" \
            % (api_response.reason, api_response.status_code,
                json.loads(api_response.content)))

    def test_blueprints(self):
        ''' Testing Checkmate Blueprints '''
        api_response = self.checkmate_provider.client.get_blueprints()

        self.assertTrue(api_response.ok, "Blueprints get failed with error: \
            '%s' and status code '%s': \n '%s'" \
            % (api_response.reason, api_response.status_code,
                json.loads(api_response.content)))

    def test_environments(self):
        ''' Testing Checkmate Environments '''
        api_response = self.checkmate_provider.client.get_environments()

        self.assertTrue(api_response.ok, "Environments get failed with error: \
            '%s' and status code '%s': \n '%s'" \
            % (api_response.reason, api_response.status_code,
                json.loads(api_response.content)))

    def test_deployments(self):
        ''' Testing Checkmate Deployments '''
        api_response = self.checkmate_provider.client.get_deployments()

        self.assertTrue(api_response.ok, "Deployments get failed with error: \
            '%s' and status code '%s': \n '%s'" \
            % (api_response.reason, api_response.status_code,
                json.loads(api_response.content)))

    def test_workflows(self):
        ''' Testing Checkmate Workflows '''
        api_response = self.checkmate_provider.client.get_workflows()

        self.assertTrue(api_response.ok, "Workflows get failed with error: \
            '%s' and status code '%s': \n '%s'" \
            % (api_response.reason, api_response.status_code,
                json.loads(api_response.content)))

    def test_providers(self):
        ''' Testing Checkmate Providers '''
        api_response = self.checkmate_provider.client.get_providers()

        self.assertTrue(api_response.ok, "Providers get failed with error: \
            '%s' and status code '%s': \n '%s'" \
            % (api_response.reason, api_response.status_code,
                json.loads(api_response.content)))

