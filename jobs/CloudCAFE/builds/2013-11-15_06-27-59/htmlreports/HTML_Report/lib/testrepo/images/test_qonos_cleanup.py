from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute import ItemNotFound
from ccengine.domain.types \
    import ImageMetadata, ImageTypes, ScheduledImagesJobStatus
from testrepo.common.testfixtures.images import BaseImagesFixture


class TestQonosCleanup(BaseImagesFixture):

    @attr('qonos-cleanup')
    def test_cleanup(self):
        """Cleans the environment by deleting all schedules, jobs, faux
        workers, instances, and snapshots created by our tenant_id.
        """

        self._cleanup_schedules()
        self._cleanup_jobs()
        self._cleanup_workers()
        self._cleanup_instances()
        self._cleanup_snapshots()

    def _cleanup_schedules(self):
        """Grabs all schedules created by test accounts and deletes them."""

        keys = ["tenant", "marker"]
        values = [self.tenant, self.marker]

        schedules_to_delete = self.images_provider. \
            list_schedules_pagination(keys, values)

        keys = ["tenant", "marker"]
        values = ["", self.marker]

        schedules_to_delete.extend(self.images_provider.
                                   list_schedules_pagination(keys, values))

        for schedule in schedules_to_delete:
            try:
                self.images_provider.schedules_client. \
                    delete_schedule(schedule.id)
            except ItemNotFound:
                msg = "Error in deleting schedule {0}".format(schedule.id)
                self.images_provider.logger.warning(msg)

        msg = "No. of Schedules deleted : {0}".format(len(schedules_to_delete))
        self.images_provider.logger.info(msg)

    def _cleanup_jobs(self):
        """Grabs all jobs created by test accounts and in status done, error
        and cancelled and deletes them."""

        jobs_to_delete = []
        keys = ["tenant", "marker"]
        values = [self.tenant, self.marker]
        status_done = ScheduledImagesJobStatus.DONE.lower()
        status_error = ScheduledImagesJobStatus.ERROR.lower()
        status_cancelled = ScheduledImagesJobStatus.CANCELLED.lower()

        jobs = self.images_provider.list_jobs_pagination(keys, values)

        keys = ["tenant", "marker"]
        values = ["", self.marker]
        jobs.extend(self.images_provider.list_jobs_pagination(keys, values))

        for job in jobs:
            if (job.status.lower() == status_done or
                    job.status.lower() == status_error or
                    job.status.lower() == status_cancelled):
                jobs_to_delete.append(job)

        for job in jobs_to_delete:
            try:
                self.images_provider.jobs_client.delete_job(job.id)
            except ItemNotFound:
                msg = "Error in deleting jobs {0}".format(job.id)
                self.images_provider.logger.warning(msg)

        msg = "No. of Jobs deleted : {0}".format(len(jobs_to_delete))
        self.images_provider.logger.info(msg)

    def _cleanup_workers(self):
        """Grabs all faux workers registered by test account and
        unregisters them."""

        workers_to_delete = []

        keys = ["marker"]
        values = [self.marker]

        workers = self.images_provider.list_workers_pagination(keys, values)
        for worker in workers:
            if worker.process_id is None:
                workers_to_delete.append(worker)

        for worker in workers_to_delete:
            try:
                self.images_provider.workers_client. \
                    delete_worker(worker.id)
            except ItemNotFound:
                msg = "Error in unregistering worker {0}".format(worker.id)
                self.images_provider.logger.warning(msg)

        msg = "No. of faux workers deleted: {0}".format(len(workers_to_delete))
        self.images_provider.logger.info(msg)

    def _cleanup_instances(self):
        """Grabs all instances created by our tenant_id and deletes them."""

        tenant_id = self.tenant_id

        instances = \
            self.images_provider.servers_client.list_servers().entity

        for instance in instances:
            get_server = self.images_provider.servers_client. \
                get_server(instance.id).entity
            if get_server.tenant_id == tenant_id:
                self.images_provider.servers_client. \
                    delete_server(get_server.id)

    def _cleanup_snapshots(self):
        """Grabs all snapshots created by our tenant_id and deletes them."""

        tenant_id = self.tenant_id

        snapshots = self.images_provider.nova_images_client. \
            list_images_with_detail().entity

        for snapshot in snapshots:
            if (hasattr(snapshot.metadata, ImageMetadata.IMAGE_TYPE) and
                    hasattr(snapshot.metadata, ImageMetadata.OWNER_ID) and
                    snapshot.metadata.image_type == ImageTypes.SNAPSHOT and
                    snapshot.metadata.owner_id == tenant_id):
                self.images_provider.nova_images_client. \
                    delete_image(snapshot.id)
