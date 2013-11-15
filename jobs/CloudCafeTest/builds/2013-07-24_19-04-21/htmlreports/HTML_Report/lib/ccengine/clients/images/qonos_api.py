from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.domain.images.request.schedule import Schedule as SchRequest
from ccengine.domain.images.response.schedule import Schedule as SchResponse
from ccengine.domain.images.request.metadata import Metadata as MetaRequest
from ccengine.domain.images.response.metadata import Metadata as MetaResponse
from ccengine.domain.images.request.worker import Worker as WorkerRequest
from ccengine.domain.images.response.worker import Worker as WorkerResponse
from ccengine.domain.images.request.job import Job as JobRequest
from ccengine.domain.images.response.job import Job as JobResponse
from ccengine.domain.images.request.job_status import JobStatus as \
    JobStatusRequest
from ccengine.domain.images.response.job_status import JobStatus as \
    JobStatusResponse


class SchedulesClient(BaseMarshallingClient):

    _suffix = '/schedules'

    def __init__(self, url, serialize_format, deserialize_format=None):

        super(SchedulesClient, self).__init__(serialize_format,
                                              deserialize_format)

        self.url = "{0}{1}".format(url, self._suffix)
        ct = "application/{0}".format(self.serialize_format)
        accept = "application/{0}".format(self.deserialize_format)
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept

    def create_schedule(self, tenant=None, action=None, minute=None,
                          hour=None, day_of_month=None, month=None,
                          day_of_week=None, next_run=None, metadata=None,
                          requestslib_kwargs=None):

        schedule = SchRequest(tenant=tenant, action=action, minute=minute,
                              hour=hour, day_of_month=day_of_month,
                              month=month, day_of_week=day_of_week,
                              metadata=metadata)

        return self.request("POST", self.url, request_entity=schedule,
                            response_entity_type=SchResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def get_schedule(self, id=None, requestslib_kwargs=None):

        full_url = "{0}/{1}".format(self.url, id)

        return self.request("GET", full_url, response_entity_type=SchResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def list_schedules(self, keys=None, values=None, requestslib_kwargs=None):

        params = None

        if keys is not None and values is not None:
            params = dict(zip(keys, values))

        return self.request("GET", self.url, params=params,
                            response_entity_type=SchResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def update_schedule(self, id=None, hour=None, tenant=None,
                          updated_at=None, created_at=None,
                          day_of_week=None, day_of_month=None,
                          metadata=None, last_scheduled=None, action=None,
                          month=None, minute=None, next_run=None,
                          requestslib_kwargs=None):

        full_url = "{0}/{1}".format(self.url, id)

        schedule = SchRequest(tenant=tenant, action=action, minute=minute,
                              hour=hour, day_of_month=day_of_month,
                              month=month, day_of_week=day_of_week,
                              next_run=next_run, last_scheduled=last_scheduled,
                              updated_at=updated_at, created_at=created_at,
                              metadata=metadata)

        return self.request("PUT", full_url, request_entity=schedule,
                            response_entity_type=SchResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_schedule(self, id=None, requestslib_kwargs=None):

        if id is not None:
            full_url = "{0}/{1}".format(self.url, id)
        else:
            full_url = self.url

        return self.request("DELETE", full_url,
                            requestslib_kwargs=requestslib_kwargs)

    def set_schedule_metadata(self, id=None, keys=None, values=None,
                              requestslib_kwargs=None):

        full_url = "{0}/{1}/metadata".format(self.url, id)

        metadata = MetaRequest(keys=keys, values=values)

        return self.request("PUT", full_url, request_entity=metadata,
                            response_entity_type=MetaResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def list_schedule_metadata(self, id=None, requestslib_kwargs=None):

        return self.request("GET", self.url,
                            response_entity_type=MetaResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def create_schedule_missing_body(self, requestslib_kwargs=None):

        return self.request("POST", self.url, response_entity_type=SchResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def update_schedule_missing_body(self, id=None, requestslib_kwargs=None):

        full_url = "{0}/{1}".format(self.url, id)

        return self.request("PUT", full_url, response_entity_type=SchResponse,
                            requestslib_kwargs=requestslib_kwargs)


class WorkersClient(BaseMarshallingClient):

    _suffix = '/workers'

    def __init__(self, url, serialize_format, deserialize_format=None):

        super(WorkersClient, self).__init__(serialize_format,
                                            deserialize_format)

        self.url = "{0}{1}".format(url, self._suffix)
        ct = "application/{0}".format(self.serialize_format)
        accept = "application/{0}".format(self.deserialize_format)
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept

    def create_worker(self, host=None, requestslib_kwargs=None):

        worker = WorkerRequest(host=host)

        return self.request("POST", self.url,
                            response_entity_type=WorkerResponse,
                            request_entity=worker,
                            requestslib_kwargs=requestslib_kwargs)

    def get_worker(self, id=None, requestslib_kwargs=None):

        full_url = "{0}/{1}".format(self.url, id)

        return self.request("GET", full_url,
                            response_entity_type=WorkerResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def list_workers(self, keys=None,
                     values=None, requestslib_kwargs=None):

        params = None

        if keys is not None and values is not None:
            params = dict(zip(keys, values))

        return self.request("GET", self.url, params=params,
                            response_entity_type=WorkerResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_worker(self, id=None, requestslib_kwargs=None):

        full_url = "{0}/{1}".format(self.url, id)

        return self.request("DELETE", full_url,
                            requestslib_kwargs=requestslib_kwargs)


class JobsClient(BaseMarshallingClient):

    _suffix = '/jobs'

    def __init__(self, url, serialize_format, deserialize_format=None):

        super(JobsClient, self).__init__(serialize_format,
                                         deserialize_format)

        self.url = "{0}{1}".format(url, self._suffix)
        ct = "application/{0}".format(self.serialize_format)
        accept = "application/{0}".format(self.deserialize_format)
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept

    def create_job(self, schedule_id=None, requestslib_kwargs=None):

        job = JobRequest(schedule_id=schedule_id)

        return self.request("POST", self.url,
                            response_entity_type=JobResponse,
                            request_entity=job,
                            requestslib_kwargs=requestslib_kwargs)

    def get_job(self, id=None, http_method="GET", url_addition=None,
                requestslib_kwargs=None):

        if url_addition is not None:
            full_url = "{0}{1}/{2}".format(self.url, url_addition, id)
        else:
            full_url = "{0}/{1}".format(self.url, id)

        return self.request(http_method, full_url, response_entity_type=JobResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def list_jobs(self, keys=None, values=None, requestslib_kwargs=None):

        params = None

        if keys is not None and values is not None:
            params = dict(zip(keys, values))

        return self.request("GET", self.url, params=params,
                            response_entity_type=JobResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_job(self, id=None, requestslib_kwargs=None):

        return self.request("DELETE", self.url,
                            requestslib_kwargs=requestslib_kwargs)

    def update_job_status(self, id=None, status=None, timeout=None,
                            error_message=None, requestslib_kwargs=None):

        full_url = "{0}/{1}/status".format(self.url, id)

        status = JobStatusRequest(status=status, timeout=timeout,
                                  error_message=error_message)

        return self.request("PUT", full_url,
                            response_entity_type=JobStatusResponse,
                            request_entity=status,
                            requestslib_kwargs=requestslib_kwargs)

    def update_job_status_missing_body(self, id=None, requestslib_kwargs=None):

        full_url = "{0}/{1}/status".format(self.url, id)

        return self.request("PUT", full_url,
                            response_entity_type=JobStatusResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def set_job_metadata(self, id=None, keys=None, values=None,
                                 requestslib_kwargs=None):

        full_url = "{0}/{1}/metadata".format(self.url, id)

        metadata = MetaRequest(keys=keys, values=values)

        return self.request("PUT", full_url, response_entity_type=MetaResponse,
                            request_entity=metadata,
                            requestslib_kwargs=requestslib_kwargs)

    def list_job_metadata(self, id=None, requestslib_kwargs=None):

        full_url = "{0}/{1}/metadata".format(self.url, id)

        return self.request("GET", full_url, response_entity_type=MetaResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def update_job_status_missing_body(self, id=None, requestslib_kwargs=None):

        full_url = "{0}/{1}/status".format(self.url, id)

        return self.request("PUT", full_url,
                            response_entity_type=JobStatusResponse,
                            requestslib_kwargs=requestslib_kwargs)
