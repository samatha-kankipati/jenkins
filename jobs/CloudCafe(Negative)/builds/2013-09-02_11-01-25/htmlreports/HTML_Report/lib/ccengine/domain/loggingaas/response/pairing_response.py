import json
from ccengine.domain.base_domain import BaseMarshallingDomain


class PipelineWorker(BaseMarshallingDomain):
    def __init__(self, hostname=None, ip_address_v4=None, ip_address_v6=None,
                 personality=None):
        super(PipelineWorker, self).__init__()

        self.hostname = hostname
        self.ip_address_v4 = ip_address_v4
        self.ip_address_v6 = ip_address_v6
        self.personality = personality

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, dic):
        kwargs = {
            'hostname': dic.get('hostname'),
            'ip_address_v4': dic.get('ip_address_v4'),
            'ip_address_v6': dic.get('ip_address_v6'),
            'personality': dic.get('personality')
        }
        return PipelineWorker(**kwargs)


class WorkerConfiguration(BaseMarshallingDomain):
    ROOT_TAG = 'pipeline_workers'

    def __init__(self, pipeline_workers=[]):
        super(WorkerConfiguration, self).__init__()

        self.pipeline_workers = pipeline_workers

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)

        return cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))

    @classmethod
    def _dict_to_obj(cls, dic):
        """Helper method to turn dictionary into Xenmeta instance."""
        workers = []
        for worker in dic:
            workers.append(PipelineWorker._dict_to_obj(worker))

        kwargs = {
            'pipeline_workers': workers
            }
        return WorkerConfiguration(**kwargs)


class WorkerPairingConfiguration(BaseMarshallingDomain):
    ROOT_TAG = 'worker_configuration'

    def __init__(self, personality=None, personality_module=None,
                 worker_token=None, worker_id=None):
        super(WorkerPairingConfiguration, self).__init__()

        self.personality = personality
        self.personality_module = personality_module
        self.worker_token = worker_token
        self.worker_id = worker_id

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """Returns an instance of a Version based on the json serialized_str
        passed in."""
        result = None
        ret = json.loads(serialized_str)
        if ret is not None:
            result = cls._dict_to_obj(ret)
        return result

    @classmethod
    def _dict_to_obj(cls, dic):
        """Helper method to turn dictionary into Xenmeta instance."""
        kwargs = {
            'personality': dic.get('personality'),
            'personality_module': dic.get('personality_module'),
            'worker_token': dic.get('worker_token'),
            'worker_id': dic.get('worker_id'),
        }
        return WorkerPairingConfiguration(**kwargs)
