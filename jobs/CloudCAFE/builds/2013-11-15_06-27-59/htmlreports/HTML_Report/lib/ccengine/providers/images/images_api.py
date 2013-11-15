import calendar
import time

import ccengine.common.tools.datagen as datagen
from ccengine.clients.compute.images_api import ImagesAPIClient
from ccengine.clients.compute.servers_api import ServerAPIClient
from ccengine.clients.images.qonos_api \
    import JobsClient, SchedulesClient, WorkersClient
from ccengine.clients.images.qonos_ext_api import ScheduledImagesClient
from ccengine.clients.images.qonos_helper_api import QonosHelperClient
from ccengine.domain.types import NovaServerStatusTypes, \
    NovaImageStatusTypes, ScheduledImagesJobStatus
from ccengine.common.exceptions.compute import BuildErrorException, \
    TimeoutException, ItemNotFound
from ccengine.common.exceptions.images import WorkerStartException, \
    WorkerKillException, UnexpectedResponse
from ccengine.providers.auth.auth_api import AuthProvider
from ccengine.providers.base_provider import BaseProvider
from ccengine.providers.identity.identity_v2_0_api import IdentityAPIProvider


class ImagesProvider(BaseProvider):

    def __init__(self, config, logger, schedules_to_delete, workers_to_delete,
                 jobs_to_delete, instances_to_disable, servers_to_delete,
                 snapshots_to_delete):
        """Sets config, sets up client, sets deserializer and serializer based
        on format defined in the config.
        """

        super(ImagesProvider, self).__init__()

        # Set variables
        self.config = config
        self.logger = logger
        self.schedules_to_delete = schedules_to_delete
        self.workers_to_delete = workers_to_delete
        self.jobs_to_delete = jobs_to_delete
        self.instances_to_disable = instances_to_disable
        self.servers_to_delete = servers_to_delete
        self.snapshots_to_delete = snapshots_to_delete
        self.servers_url = "{0}/{1}".format(config.images.ext_url,
                                            config.images.tenant_id)
        self.results_limit = self.config.images.results_limit

        # Configure auth/identity
        if (config.identity_api.api_key is not None or
                config.identity_api.password is not None):
            self.identity_api_provider = IdentityAPIProvider(self.config)
            self.identity_data = self.identity_api_provider.authenticate()
            self.auth_token = self.identity_data.response.entity.token.id

        else:
            self.auth_provider = AuthProvider(self.config)
            self.auth_data = self.auth_provider.authenticate()
            self.auth_token = self.auth_data.token.id

        # Initialize clients
        self.schedules_client = SchedulesClient(config.images.url,
                                                config.misc.serializer)
        self.workers_client = WorkersClient(config.images.url,
                                            config.misc.serializer)
        self.jobs_client = JobsClient(config.images.url,
                                      config.misc.serializer)
        self.helper_client = QonosHelperClient(config.images.helper_url,
                                               config.misc.serializer)
        self.scheduled_images_client = ScheduledImagesClient(
            config.images.ext_url, config.misc.ext_serializer,
            config.images.tenant, self.auth_token)

        self.servers_client = ServerAPIClient(
            self.servers_url, self.auth_token, self.config.misc.ext_serializer,
            self.config.misc.ext_deserializer)

        self.nova_images_client = ImagesAPIClient(
            self.servers_url, self.auth_token, self.config.misc.ext_serializer,
            self.config.misc.ext_deserializer)

    def create_active_schedules(self, tenant=None, action=None, minute=None,
                                hour=None, day_of_month=None, month=None,
                                day_of_week=None, next_run=None, metadata=None,
                                count=1, requestslib_kwargs=None):
        """Creates x active schedules and appends them to the list of
        schedules to delete during teardown.
        """

        schedule_list = []

        for i in range(count):
            if minute is None:
                minute = datagen.random_int(0, 59)
            if hour is None:
                hour = datagen.random_int(0, 23)
            schedule_resp = self.schedules_client.create_schedule(
                tenant, action, minute, hour, day_of_month, month, day_of_week,
                next_run, metadata)
            schedule_list.append(schedule_resp)
            self.schedules_to_delete.append(schedule_resp.entity.id)

        if len(schedule_list) == 1:
            schedule_list = schedule_resp

        return schedule_list

    def create_active_workers(self, host=None, count=1,
                              requestslib_kwargs=None):
        """Creates x active workers and appends them to the list of workers to
        delete during teardown.
        """

        worker_list = []

        for i in range(count):
            worker_resp = self.workers_client.create_worker(host)
            worker_list.append(worker_resp)
            self.workers_to_delete.append(worker_resp.entity.id)

        if len(worker_list) == 1:
            worker_list = worker_resp

        return worker_list

    def create_active_jobs(self, schedule_id=None, count=1,
                           requestslib_kwargs=None):
        """Creates x active jobs and appends them to the list of jobs to
        delete during teardown.
        """

        job_list = []

        for i in range(count):
            job_resp = self.jobs_client.create_job(schedule_id)
            job_list.append(job_resp)
            self.jobs_to_delete.append(job_resp.entity.id)

        if len(job_list) == 1:
            worker_list = job_resp

        return worker_list

    def list_jobs_for_schedule(self, schedule_id, keys=None, values=None):
        """List all queued jobs for the given schedule."""

        job_list = []
        jobs = self.list_jobs_pagination(keys, values)

        for job in jobs:
            if (job.schedule_id == schedule_id):
                job_list.append(job)

        return job_list

    def list_snapshots_for_server(self, instance_id):
        """List all snapshots for the given server."""

        images_resp = self.nova_images_client.list_images(
            server_ref=instance_id)

        return images_resp.entity

    def wait_for_job_status(self, job_id, status_to_wait_for):
        """Polls job details until status_to_wait_for is met."""

        time_waited = 0
        interval_time = int(self.config.images.build_interval)
        timeout = int(self.config.images.job_status_timeout)
        message = "Job went to {0} status: Job uuid {1}"
        timeout_message = "Job timed out: Job uuid {0}"

        job_response = self.jobs_client.get_job(job_id)
        job_obj = job_response.entity

        while (job_obj.status.lower() != status_to_wait_for.lower() and
               time_waited < timeout):
            job_response = self.jobs_client.get_job(job_id)
            job_obj = job_response.entity

            if (job_obj.status.lower() ==
                    ScheduledImagesJobStatus.ERROR.lower()):
                raise BuildErrorException(message.format('Error', job_obj.id))

            if (job_obj.status.lower() ==
                    ScheduledImagesJobStatus.CANCELLED.lower() and
                    status_to_wait_for != ScheduledImagesJobStatus.
                    CANCELLED.lower()):
                raise BuildErrorException(message.format('Cancelled', job_id))

            time.sleep(interval_time)
            time_waited += interval_time

            if time_waited > timeout:
                raise TimeoutException(timeout_message.format(job_obj.id))

        return job_response

    def stop_workers(self, keys=None, values=None, requestslib_kwargs=None):
        """Stops all running workers."""

        return self.helper_client.stop_workers(keys, values)

    def start_worker(self, requestslib_kwargs=None):
        """Start a worker."""

        return self.helper_client.start_worker()

    def get_running_worker_count(self, requestslib_kwargs=None):
        """Get the count of running worker."""

        return self.helper_client.get_running_worker_count()

    def get_running_scheduler_count(self, requestslib_kwargs=None):
        """Get the count of running scheduler."""

        return self.helper_client.get_running_scheduler_count()

    def is_job_status_valid(self, status):
        """Checks job status is one of the valid job status."""

        return status.lower() in [ScheduledImagesJobStatus.QUEUED.lower(),
                                  ScheduledImagesJobStatus.ERROR.lower(),
                                  ScheduledImagesJobStatus.PROCESSING.lower(),
                                  ScheduledImagesJobStatus.DONE.lower(),
                                  ScheduledImagesJobStatus.CANCELLED.lower(),
                                  ScheduledImagesJobStatus.TIMED_OUT.lower()]

    def is_job_status_workable(self, status):
        """Checks job status is one of the workable job status."""

        return status.lower() in [ScheduledImagesJobStatus.QUEUED.lower(),
                                  ScheduledImagesJobStatus.PROCESSING.lower()]

    def is_job_status_done(self, job_status):
        """Checks job status is done."""

        return job_status.lower() == ScheduledImagesJobStatus.DONE.lower()

    def wait_for_job_to_create(self, sch_id, count=1, keys=None, values=None):
        """Polls job details for a schedule until a job is created."""

        timeout = int(self.config.images.job_pickup_timeout)
        time_waited = 0
        interval_time = int(self.config.images.build_interval)
        build_message = "Schedule {0} has more than {1} job(s) available"
        timeout_message = ("Job creation timed out: {0} jobs available for "
                           "schedule with uuid {1}")

        jobs = self.list_jobs_for_schedule(sch_id, keys, values)

        while (len(jobs) != count and time_waited < timeout):
            jobs = self.list_jobs_for_schedule(sch_id, keys, values)

            if (len(jobs) > count):
                raise BuildErrorException(build_message.format(sch_id, count))

            time.sleep(interval_time)
            time_waited += interval_time

            if time_waited >= timeout:
                raise TimeoutException(timeout_message.format(len(jobs),
                                                              sch_id))
        return jobs

    def wait_for_retry_count(self, job_id, count):
        """Polls job details for a retry count until the count matches."""

        timeout = int(self.config.images.job_pickup_timeout)
        time_waited = 0
        interval_time = int(self.config.images.alt_build_interval)
        job_message = ("Job with id {0} is no longer in error or processing "
                       "status: The current status is {1}")
        timeout_message = ("Waiting for job retry count has timed out: Retry "
                           "count of {0} does not match {1}")

        get_job_obj = self.jobs_client.get_job(job_id)

        while (get_job_obj.entity.retry_count != count and
               time_waited < timeout):
            get_job_obj = self.jobs_client.get_job(job_id)

            job_status = get_job_obj.entity.status.lower()
            retry_count = get_job_obj.entity.retry_count

            time.sleep(interval_time)
            time_waited += interval_time

            if (job_status != ScheduledImagesJobStatus.ERROR.lower() and
                    job_status != ScheduledImagesJobStatus.PROCESSING.lower()):
                raise BuildErrorException(job_message.format(job_id,
                                                             job_status))

            if time_waited >= timeout:
                raise TimeoutException(timeout_message.format(retry_count,
                                                              count))

    def create_active_server(self, name=None, image_ref=None, flavor_ref=None):
        """Creates an active server."""

        if image_ref is None:
            image_ref = self.config.compute_api.image_ref
        if flavor_ref is None:
            flavor_ref = self.config.compute_api.flavor_ref

        server_obj = self.servers_client.create_server(name, image_ref,
                                                       flavor_ref)

        server = server_obj.entity

        self.instances_to_disable.append(server.id)
        self.servers_to_delete.append(server.id)

        wait_response = self.wait_for_server_status(
            server.id, NovaServerStatusTypes.ACTIVE)

        # Add admin pass from the create command into the final wait response
        wait_response.entity.adminPass = server.adminPass

        return wait_response

    def create_server_no_wait(self, name=None, imageRef=None,
                              flavorRef=None):
        """Creates a server, but does not wait for a server status."""

        if name is None:
            name = datagen.random_string(size=10)
        if imageRef is None:
            imageRef = self.config.compute_api.image_ref
        if flavorRef is None:
            flavorRef = self.config.compute_api.flavor_ref

        server_obj = self.servers_client.create_server(name, imageRef,
                                                       flavorRef)

        server = server_obj.entity

        self.servers_to_delete.append(server.id)
        self.instances_to_disable.append(server.id)

        return server_obj

    def delete_active_server(self, id):
        """Deletes an active server and waits for status deleted."""

        self.servers_client.delete_server(id)

        self.wait_for_server_status(id, NovaServerStatusTypes.DELETED)

    def wait_for_server_status(self, server_id, status_to_wait_for,
                               timeout=None):
        """Polls server status until status_to_wait_for is met."""

        time_waited = 0
        interval_time = int(self.config.images.build_interval)
        timeout = timeout or self.config.images.server_status_timeout
        timeout = int(timeout)
        timeout_message = "Server timed out: Server uuid {0}"
        build_message = "Server went to Error status: Server uuid {0}"

        if status_to_wait_for == NovaServerStatusTypes.DELETED:
            return self.wait_for_server_to_be_deleted(server_id)

        get_server_obj = self.servers_client.get_server(server_id)
        get_server = get_server_obj.entity

        while (get_server.status.lower() != status_to_wait_for.lower() and
               get_server.status.lower() != NovaServerStatusTypes.ERROR.lower()
               and time_waited <= timeout):
            get_server_obj = self.servers_client.get_server(server_id)
            get_server = get_server_obj.entity
            time.sleep(interval_time)
            time_waited += interval_time

        if time_waited > timeout:
            raise TimeoutException(timeout_message.format(server_id))

        if get_server.status.lower() == NovaServerStatusTypes.ERROR.lower():
            raise BuildErrorException(build_message.format(server_id))

        return get_server_obj

    def wait_for_server_task_state(self, server_id, state_to_wait_for,
                                   timeout=None):
        """Polls server task_state until state_to_wait_for is met."""

        time_waited = 0
        interval_time = int(self.config.images.build_interval)
        timeout = timeout or self.config.images.server_task_state_timeout
        timeout = int(timeout)
        timeout_message = ("Timed out: Server uuid {0} Expected task state {1}"
                           "Received task state {2}")

        server_obj = self.servers_client.get_server(server_id)
        task_state = server_obj.entity.task_state

        if task_state is not None:
            task_state = task_state.lower()

        if state_to_wait_for is not None:
            state_to_wait_for = state_to_wait_for.lower()

        while (task_state != state_to_wait_for and
               time_waited <= timeout):
            server_obj = self.servers_client.get_server(server_id)
            task_state = server_obj.entity.task_state
            if task_state is not None:
                task_state = task_state.lower()

            time.sleep(interval_time)
            time_waited += interval_time

        if time_waited > timeout:
            raise TimeoutException(timeout_message.format(
                server_id, state_to_wait_for, task_state))

        return server_obj

    def wait_for_server_to_be_deleted(self, server_id):
        """Polls server status until it returns deleted."""

        time_waited = 0
        interval_time = int(self.config.images.build_interval)
        timeout_message = "Server timed out while deleting: Server uuid {0}"
        message = ("Server went to Error status while deleting: Server "
                   "uuid {0}")

        try:
            while (True):
                server_response = self.servers_client.get_server(server_id)
                server_obj = server_response.entity
                if time_waited > self.config.images.server_status_timeout:
                    raise TimeoutException(timeout_message.format(server_id))

                server_status = server_obj.status.lower()

                if server_status != NovaServerStatusTypes.ERROR.lower():
                    time.sleep(interval_time)
                    time_waited += interval_time
                    continue
                    if server_status != NovaServerStatusTypes.ERROR.lower():
                        raise BuildErrorException(message.format(server_id))
                time.sleep(interval_time)
                time_waited += interval_time

        except ItemNotFound:
            pass

    def create_faux_scheduled_image(self, instance_id=None, snapshot_name=None,
                                    metadata=None):
        """Creates a snapshot, setting the correct metadata to make it appear
        as if it were a real scheduled image.
        """

        image_obj = self.servers_client.create_image(instance_id,
                                                     snapshot_name, metadata)

        image_ref = image_obj.headers['location']
        image_id = image_ref.rsplit('/')[-1]

        self.snapshots_to_delete.append(image_id)

        self.wait_for_image_status(image_id, NovaImageStatusTypes.ACTIVE)

        return image_obj

    def wait_for_image_status(self, image_id, status_to_wait_for):
        """Polls image details until status_to_wait_for is met."""

        time_waited = 0
        interval_time = int(self.config.images.build_interval)
        timeout = int(self.config.images.job_pickup_timeout)
        timeout_message = "Snapshot timed out: Snapshot uuid {0}"
        build_message = "Snapshot went to Error status: Image uuid {0}"

        image_response = self.nova_images_client.get_image(image_id)
        image_obj = image_response.entity

        while (image_obj.status.lower() != status_to_wait_for.lower() and
               time_waited < timeout):
            image_response = self.nova_images_client.get_image(image_id)
            image_obj = image_response.entity

            if image_obj.status.lower() == NovaImageStatusTypes.ERROR.lower():
                raise BuildErrorException(build_message.format(image_id))

            time.sleep(interval_time)
            time_waited += interval_time

            if time_waited > timeout:
                raise TimeoutException(timeout_message.format(image_id))

        if status_to_wait_for.lower() == NovaImageStatusTypes.DELETED.lower():
            self.snapshots_to_delete.remove(image_id)

        return image_response

    def wait_for_image_to_be_created(self, instance_id, image_count,
                                     start_time, sch_id, keys, values):
        """Polls list_images until the number of active images is met."""

        status = NovaImageStatusTypes.ACTIVE
        timeout = int(self.config.images.job_pickup_timeout)
        time_waited = 0
        interval_time = int(self.config.images.build_interval)
        timeout_message = ("Snapshot creation timed out: {0} snapshot(s) "
                           "available for server with uuid {1}, expected {2}")

        while (time_waited < timeout):
            list_images_obj = self.nova_images_client.list_images_with_detail(
                server_ref=instance_id)
            list_images = list_images_obj.entity
            count = 0

            job_list = self.list_jobs_for_schedule(sch_id, keys, values)
            for job in job_list:
                created_at = time.strptime(str(job.created_at),
                                           "%Y-%m-%dT%H:%M:%SZ")
                if (calendar.timegm(created_at) > start_time):
                    job_id = job.id
                    self.wait_for_job_status(job_id,
                                             ScheduledImagesJobStatus.DONE)

            for image in list_images:
                self.wait_for_image_status(image.id, status)
                self.wait_for_server_status(instance_id,
                                            NovaServerStatusTypes.ACTIVE)
                self.wait_for_server_task_state(instance_id, None)
                count += 1

            if count == image_count:
                break

            time.sleep(interval_time)
            time_waited += interval_time

            if time_waited >= timeout:
                raise TimeoutException(timeout_message.format(
                    count, instance_id, image_count))

    def wait_for_new_image_to_be_created(self, instance_id, start_time, sch_id,
                                         keys, values):
        """Polls list_images for the given server until new image scheduled
        after start_time is created and active status is met.
        """

        status = NovaImageStatusTypes.ACTIVE
        timeout = int(self.config.images.job_pickup_timeout)
        time_waited = 0
        interval_time = int(self.config.images.build_interval)
        unex_message = ("Single scheduled image expected: {0} snapshots "
                        "received for instance id {1} of schedule id {2}")
        timeout_message = ("Snapshot creation timed out: No snapshots "
                           "available for server with uuid {0}")

        while (time_waited < timeout):
            list_images_obj = self.nova_images_client.list_images_with_detail(
                server_ref=instance_id)
            list_images = list_images_obj.entity
            new_images = []

            job_list = self.list_jobs_for_schedule(sch_id, keys, values)
            for job in job_list:
                created_at = time.strptime(str(job.created_at),
                                           "%Y-%m-%dT%H:%M:%SZ")
                if (calendar.timegm(created_at) > start_time):
                    job_id = job.id
                    self.wait_for_job_status(job_id,
                                             ScheduledImagesJobStatus.DONE)
                    self.logger.info("New Job id: {0}".format(job_id))

            for image in list_images:
                created_at = time.strptime(str(image.created),
                                           "%Y-%m-%dT%H:%M:%SZ")
                if (calendar.timegm(created_at) > start_time):
                    new_images.append(image.id)
                    self.logger.info("New image id: {0}".format(image.id))

            if len(new_images) == 1:
                self.wait_for_image_status(new_images[0], status)
                self.wait_for_server_status(instance_id,
                                            NovaServerStatusTypes.ACTIVE)
                self.wait_for_server_task_state(instance_id, None)
                break

            if len(new_images) > 1:
                raise UnexpectedResponse(unex_message.format(
                    len(new_images), instance_id, sch_id))

            time.sleep(interval_time)
            time_waited += interval_time

            if time_waited >= timeout:
                raise TimeoutException(timeout_message.format(instance_id))

    def make_sure_new_worker_exists(self, old_worker=None):
        """Verify that the old worker is not running and that a new worker is
        running and if not, starts a worker.
        """

        running_worker = self.get_running_worker_count()
        worker_resp = running_worker.content.split('\n')
        kill_message = "Killing worker failed: Worker uuid {1}"

        if old_worker is not None:
            if str(old_worker) in (worker_resp[1]):
                return WorkerKillException(kill_message.format(old_worker))

        if int(worker_resp[0]) == 0:
            self.start_worker()
            # Wait time for starting a worker
            time.sleep(int(self.config.images.worker_start_timeout))
            running_worker = self.get_running_worker_count()
            worker_resp = running_worker.content.split('\n')
            if int(worker_resp[0]) == 0:
                raise WorkerStartException("Starting worker failed")

    def get_server_daily_list(self, instance_id):
        """Retrieves a list of daily snapshot images that match a given server
        id.
        """

        server_daily_list = []
        list_images_obj = self.nova_images_client.list_images(
            server_ref=instance_id)
        list_images = list_images_obj.entity

        for image in list_images:
            if 'Daily' in image.name:
                server_daily_list.append(image.id)

        return server_daily_list

    def get_retention(self, resp):
        """Retrieve the retention value for a given schedule."""

        type = self.config.misc.ext_deserializer

        if type == 'json':
            image_schedule = getattr(resp, "RAX-SI:image_schedule")

            for key, value in image_schedule.items():
                if key == 'retention':
                    retention = value

        else:
            image_schedule = getattr(resp, 'image_schedule')
            retention = int(image_schedule.retention)

        return retention

    def list_schedules_pagination(self, keys=None, values=None):
        """Lists all schedules accounting for pagination as needed."""

        sch_list = []
        limit = int(self.results_limit)

        list_sch_obj = self.schedules_client.list_schedules(keys, values)

        while len(list_sch_obj.entity) == limit:
            sch_list += list_sch_obj.entity

            values[1] = list_sch_obj.entity[limit - 1].id

            list_sch_obj = self.schedules_client.list_schedules(keys, values)

        sch_list += list_sch_obj.entity

        return sch_list

    def list_jobs_pagination(self, keys=None, values=None):
        """Lists all jobs accounting for pagination as needed."""

        job_list = []
        limit = int(self.results_limit)

        list_job_obj = self.jobs_client.list_jobs(keys, values)

        while len(list_job_obj.entity) == limit:
            job_list += list_job_obj.entity

            values[1] = list_job_obj.entity[limit - 1].id

            list_job_obj = self.jobs_client.list_jobs(keys, values)

        job_list += list_job_obj.entity

        return job_list

    def list_workers_pagination(self, keys=None, values=None):
        """Lists all workers accounting for pagination as needed."""

        worker_list = []
        limit = int(self.results_limit)

        list_workers_obj = self.workers_client.list_workers(keys=keys,
                                                            values=values)

        while len(list_workers_obj.entity) == limit:
            worker_list += list_workers_obj.entity

            values[0] = list_workers_obj.entity[limit - 1].id

            list_workers_obj = self.workers_client.list_workers(keys=keys,
                                                                values=values)

        worker_list += list_workers_obj.entity

        return worker_list

    def list_images_pagination(self):
        """Lists all images accounting for pagination as needed/"""

        image_list = []
        limit = int(self.results_limit)

        list_images_obj = self.nova_images_client.list_images_with_detail()

        while len(list_images_obj.entity) == limit:
            image_list += list_images_obj.entity

            marker = list_images_obj.entity[limit - 1].id

            list_images_obj = self.nova_images_client.list_images_with_detail(
                marker=marker)

        image_list += list_images_obj.entity

        return image_list

    def create_active_snapshot(self, instance_id=None, snapshot_name=None):
        """Creates a snapshot and waits for it to become active."""

        image_obj = self.servers_client.create_image(instance_id,
                                                     snapshot_name)

        image_ref = image_obj.headers['location']
        image_id = image_ref.rsplit('/')[-1]

        self.snapshots_to_delete.append(image_id)

        self.wait_for_image_status(image_id, NovaImageStatusTypes.ACTIVE)

        return image_id

    def create_snapshot_no_wait(self, instance_id=None, snapshot_name=None):
        """Creates a snapshot and does not wait for it to become active."""

        image_obj = self.servers_client.create_image(instance_id,
                                                     snapshot_name)

        image_ref = image_obj.headers['location']
        image_id = image_ref.rsplit('/')[-1]

        self.snapshots_to_delete.append(image_id)

        return image_id

    def wait_for_schedule_to_delete(self, sch_id):
        """Polls schedule until a it returns as not found."""

        timeout = int(self.config.images.server_status_timeout)
        time_waited = 0
        interval_time = int(self.config.images.build_interval)
        timeout_message = ("Schedule deletion timed out: Schedule with id {0} "
                           "was not deleted in the given time")

        try:
            while (True):
                get_sch_obj = self.schedules_client.get_schedule(sch_id)

                if time_waited > timeout:
                    raise TimeoutException(timeout_message.format(sch_id))

                status_code = get_sch_obj.status_code

                if status_code != 404:
                    time.sleep(interval_time)
                    time_waited += interval_time

        except ItemNotFound:
            pass

    @classmethod
    def parse_image_id(self, image_response):
        """
        @summary: Extract Image Id from Image response
        @param image_response: Image response
        @type image_ref: string
        @return: Image id
        @rtype: string
        """
        image_ref = image_response.headers['location']
        return image_ref.rsplit('/')[-1]
