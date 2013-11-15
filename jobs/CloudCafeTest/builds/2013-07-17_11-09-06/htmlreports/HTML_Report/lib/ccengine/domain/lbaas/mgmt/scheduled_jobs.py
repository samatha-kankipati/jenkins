from ccengine.domain.base_domain import BaseMarshallingDomain, \
    BaseMarshallingDomainList
import xml.etree.ElementTree as ET
import json


class JobList(BaseMarshallingDomainList):

    ROOT_TAG = 'jobs'

    def __init__(self, jobs=None):
        '''An object that data concerning tickets on a load balancer.

        '''
        for job in jobs:
            self.append(job)

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret[self.ROOT_TAG])

    def _obj_to_xml(self):
        ret = self._auto_to_xml()
        return ET.tostring(ret)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        pass

    @classmethod
    def _dict_to_obj(cls, dic):
        kwargs = {cls.ROOT_TAG: [Job._dict_to_obj(job) for job in dic]}
        return JobList(**kwargs)


class Job(BaseMarshallingDomain):

    ROOT_TAG = 'job'

    def __init__(self, id=None, jobName=None, state=None, startTime=None,
                 endTime=None, inputPath=None):
        '''An object that data concerning tickets on a load balancer.

        '''
        self.jobName = jobName
        self.id = id
        self.state = state
        self.startTime = startTime
        self.endTime = endTime
        self.inputPath = inputPath

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret[self.ROOT_TAG])

    def _obj_to_xml(self):
        ret = self._auto_to_xml()
        return ET.tostring(ret)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        pass

    @classmethod
    def _dict_to_obj(cls, dic):
        return Job(**dic)
