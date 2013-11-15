from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.domain.loggingaas.response.pairing_response import \
    WorkerPairingConfiguration, WorkerConfiguration
from ccengine.domain.loggingaas.request.pairing_request import WorkerStatus


class PairingClient(BaseMarshallingClient):
    def __init__(self, coordinator_url, worker_url, api_version, api_secret,
                 personality):
        super(PairingClient, self).__init__()

        self.coordinator_url = coordinator_url
        self.worker_url = worker_url
        self.api_version = api_version
        self.api_secret = api_secret
        self.personality = personality

    def pair_worker(self, request_obj):
        url = '{0}/{1}/pairing'.format(self.coordinator_url, self.api_version)
        headers = {'X-AUTH-TOKEN': self.api_secret}

        pair_resp = self.request('POST', url, headers,
                                 response_entity_type=WorkerPairingConfiguration,
                                 request_entity=request_obj)

        return pair_resp

    def load_configuration(self, worker_id, worker_token):
        url = '{0}/{1}/worker/{2}/configuration'.format(self.coordinator_url,
                                                        self.api_version,
                                                        worker_id)
        headers = {'WORKER-TOKEN': worker_token}
        config_resp = self.request('GET', url, headers,
                                   response_entity_type=WorkerConfiguration)
        return config_resp

    def register(self, worker_id, worker_token, status):
        url = '{0}/{1}/worker/{2}/status'.format(self.coordinator_url,
                                                 self.api_version,
                                                 worker_id)
        headers = {'WORKER-TOKEN': worker_token}
        request_obj = WorkerStatus(status)

        reg_resp = self.request('PUT', url, headers,
                                request_entity=request_obj)

        return reg_resp
