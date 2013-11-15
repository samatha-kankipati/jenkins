import ccengine.common.tools.datagen as datagen
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
from testrepo.common.testfixtures.images import BaseImagesFixture


class TestQonosSetJobMetadata(BaseImagesFixture):

    @attr('positive')
    def test_happy_path_set_job_metadata(self):
        """Happy Path - Set valid job metadata.

        1) Create a job from a schedule without metadata
        2) Set a job metadata for the job using a valid key value pair in the
            body
        3) Verify that the response code is 200
        4) Get the job
        5) Verify that the job contains the single job metadata with auto
            generated attributes and values
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        key = self.config.images.metadata_key
        value = datagen.random_string(size=10)
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        job_obj = self.images_provider.create_active_jobs(sch.id)

        self.assertEquals(job_obj.status_code, 200,
                          msg.format('status_code', 200, job_obj.status_code))

        job = job_obj.entity

        keys = [key]
        values = [value]

        job_metadata_obj = \
            self.images_provider.jobs_client.set_job_metadata(job.id, keys,
                                                              values)
        self.assertEquals(job_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     job_metadata_obj.status_code))

        job_metadata = job_metadata_obj.entity

        # Assert that the schedule meta is created as expected
        self.assertEquals(job_metadata, {key: value},
                          msg.format('key-value', {key: value}, job_metadata))

        get_job_obj = self.images_provider.jobs_client.get_job(job.id)
        self.assertEquals(get_job_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     get_job_obj.status_code))

        get_job_metadata = get_job_obj.entity.metadata

        # Assert that the schedule meta matches the get schedule's data
        self.assertEquals(get_job_metadata, {key: value},
                          msg.format('key-value', {key: value},
                                     get_job_metadata))

    @attr('positive')
    def test_overwrite_existing_job_metadata(self):
        """Overwrite existing job metadata.

        1) Create a job from a schedule without metadata
        2) Set a job metadata for the job using a valid key value pair in the
            body
        3) Verify that the response code is 200
        4) Set job metadata for the same job
        5) Verify that the job contains only the last job metadata with auto
            generated attributes and values
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        key = self.config.images.metadata_key
        value = datagen.random_string(size=10)
        alt_key = self.config.images.alt_metadata_key
        alt_value = datagen.random_string(size=10)
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        job_obj = self.images_provider.create_active_jobs(sch.id)

        self.assertEquals(job_obj.status_code, 200,
                          msg.format('status_code', 200, job_obj.status_code))

        job = job_obj.entity

        keys = [key]
        values = [value]

        job_metadata_obj = \
            self.images_provider.jobs_client.set_job_metadata(job.id, keys,
                                                              values)
        self.assertEquals(job_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     job_metadata_obj.status_code))

        keys = [alt_key]
        values = [alt_value]

        job_metadata_obj = \
            self.images_provider.jobs_client.set_job_metadata(job.id, keys,
                                                              values)
        self.assertEquals(job_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     job_metadata_obj.status_code))

        job_metadata = job_metadata_obj.entity

        # Assert that the schedule meta is created as expected
        self.assertEquals(job_metadata, {alt_key: alt_value},
                          msg.format('key-value', {alt_key: alt_value},
                                     job_metadata))

        get_job_obj = self.images_provider.jobs_client.get_job(job.id)
        self.assertEquals(get_job_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     get_job_obj.status_code))

        get_job_metadata = get_job_obj.entity.metadata

        # Assert that the schedule meta matches the get schedule's data
        self.assertEquals(get_job_metadata, {alt_key: alt_value},
                          msg.format('key-value', {alt_key: alt_value},
                                     get_job_metadata))

    @attr('positive')
    def test_append_job_metadata(self):
        """Append job metadata.

        1) Create a job from a schedule without metadata
        2) Set a job metadata for the job using a valid key value pair in the
            body
        3) Verify that the response code is 200
        4) Set previous and new job metadata for the same job
        5) Verify that the response code is 200
        6) Verify that job contains both job metadata
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        key = self.config.images.metadata_key
        value = datagen.random_string(size=10)
        alt_key = self.config.images.alt_metadata_key
        alt_value = datagen.random_string(size=10)
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        job_obj = self.images_provider.create_active_jobs(sch.id)
        self.assertEquals(job_obj.status_code, 200,
                          msg.format('status_code', 200, job_obj.status_code))

        job = job_obj.entity

        keys = [key]
        values = [value]

        job_metadata_obj = \
            self.images_provider.jobs_client.set_job_metadata(job.id, keys,
                                                              values)
        self.assertEquals(job_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     job_metadata_obj.status_code))

        keys = [key, alt_key]
        values = [value, alt_value]

        new_metadata_obj = \
            self.images_provider.jobs_client.set_job_metadata(job.id, keys,
                                                              values)
        self.assertEquals(new_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     new_metadata_obj.status_code))

        get_job_obj = \
            self.images_provider.jobs_client.get_job(job.id)
        self.assertEquals(get_job_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     get_job_obj.status_code))

        get_job_metadata = get_job_obj.entity.metadata

        self.assertEqual(len(get_job_metadata), 2,
                         msg.format("number of key-value pairs", 2,
                                    len(get_job_metadata)))

        for metadata_key, metadata_value in get_job_metadata.items():
            if metadata_key == key:
                self.assertEquals(metadata_value, value,
                                  msg.format('value', value, metadata_value))
            elif metadata_key == alt_key:
                self.assertEquals(metadata_value, alt_value,
                                  msg.format('alt_value', alt_value,
                                             metadata_value))
            else:
                self.assertEquals(metadata_key, key,
                                  msg.format('key', key, metadata_key))
                self.assertEquals(metadata_key, alt_key,
                                  msg.format('key', alt_key, metadata_key))

    @attr('positive')
    def test_set_multiple_job_metadata(self):
        """Set multiple job metadata.

        1) Create a job from schedule without metadata
        2) Set two job metadata for the job using a valid key value pair in the
            body
        3) Verify that the response code is 200
        4) Verify that job contains both job metadata
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        key = self.config.images.metadata_key
        value = datagen.random_string(size=10)
        alt_key = self.config.images.alt_metadata_key
        alt_value = datagen.random_string(size=10)
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        job_obj = self.images_provider.create_active_jobs(sch.id)
        self.assertEquals(job_obj.status_code, 200,
                          msg.format('status_code', 200, job_obj.status_code))

        job = job_obj.entity

        keys = [key, alt_key]
        values = [value, alt_value]

        job_metadata_obj = \
            self.images_provider.jobs_client.set_job_metadata(job.id, keys,
                                                              values)
        self.assertEquals(job_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     job_metadata_obj.status_code))

        get_job_obj = \
            self.images_provider.jobs_client.get_job(job.id)
        self.assertEquals(get_job_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     get_job_obj.status_code))

        get_job_metadata = get_job_obj.entity.metadata

        self.assertEqual(len(get_job_metadata), 2,
                         msg.format("number of key-value pairs", 2,
                                    len(get_job_metadata)))

        for metadata_key, metadata_value in get_job_metadata.items():
            if metadata_key == key:
                self.assertEquals(metadata_value, value,
                                  msg.format('value', value, metadata_value))
            elif metadata_key == alt_key:
                self.assertEquals(metadata_value, alt_value,
                                  msg.format('alt_value', alt_value,
                                             metadata_value))
            else:
                self.assertEquals(metadata_key, key,
                                  msg.format('key', key, metadata_key))
                self.assertEquals(metadata_key, alt_key,
                                  msg.format('key', alt_key, metadata_key))

    @attr('positive')
    def test_set_different_value_for_job_metadata_key(self):
        """Set different value for job metadata key.

        1) Create a job from schedule without metadata
        2) set job metadata
        3) Verify that the response code is 200
        4) Set job metadata with the existing job metadata key and new value
        5) Verify that the response code is 200
        6) Get job and verify new metadata value is updated for the key passed
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        key = self.config.images.metadata_key
        value = datagen.random_string(size=10)
        alt_value = datagen.random_string(size=10)
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        job_obj = self.images_provider.create_active_jobs(sch.id)
        self.assertEquals(job_obj.status_code, 200,
                          msg.format('status_code', 200, job_obj.status_code))

        job = job_obj.entity

        keys = [key]
        values = [value]

        job_metadata_obj = \
            self.images_provider.jobs_client.set_job_metadata(job.id, keys,
                                                              values)
        self.assertEquals(job_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     job_metadata_obj.status_code))

        keys = [key]
        values = [alt_value]

        upd_metadata_obj = \
            self.images_provider.jobs_client.set_job_metadata(job.id, keys,
                                                              values)
        self.assertEquals(upd_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_metadata_obj.status_code))

        upd_metadata = upd_metadata_obj.entity

        get_job_obj = \
            self.images_provider.jobs_client.get_job(job.id)
        self.assertEquals(get_job_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     get_job_obj.status_code))

        get_job_metadata = get_job_obj.entity.metadata

        self.assertEqual(len(get_job_metadata), 1,
                         msg.format("number of key-value pairs", 1,
                                    len(get_job_metadata)))

        self.assertEquals(get_job_metadata, upd_metadata,
                          msg.format('key-value pair', upd_metadata,
                                     get_job_metadata))

    @attr('positive')
    def test_set_an_empty_job_metadata(self):
        """Set an empty job metadata.

        1) Create a job
        2) Set an empty job metadata
        3) Verify that the response code is 200
        4) Verify that get job returns empty metadata
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        job_obj = self.images_provider.create_active_jobs(sch.id)
        self.assertEquals(job_obj.status_code, 200,
                          msg.format('status_code', 200, job_obj.status_code))

        job = job_obj.entity

        keys = []
        values = []

        job_metadata_obj = \
            self.images_provider.jobs_client.set_job_metadata(job.id, keys,
                                                              values)
        self.assertEquals(job_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     job_metadata_obj.status_code))

        list_job_metadata_obj = \
            self.images_provider.jobs_client.list_job_metadata(job.id)
        self.assertEqual(len(list_job_metadata_obj.entity), 0,
                         msg.format("length of the list", 0,
                                    len(list_job_metadata_obj.entity)))

    @attr('positive')
    def test_set_an_empty_job_metadata_that_is_already_empty(self):
        """Set an empty job metadata that is already empty.

        1) Create a job
        2) Set an empty job metadata
        3) Verify that the response code is 200
        4) Verify that get job returns empty metadata
        5) Set an empty job metadata
        6) Verify that the response code is 200
        7) Verify that get job returns empty metadata
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        job_obj = self.images_provider.create_active_jobs(sch.id)
        self.assertEquals(job_obj.status_code, 200,
                          msg.format('status_code', 200, job_obj.status_code))

        job = job_obj.entity

        keys = []
        values = []

        job_metadata_obj = \
            self.images_provider.jobs_client.set_job_metadata(job.id, keys,
                                                              values)
        self.assertEquals(job_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     job_metadata_obj.status_code))

        list_job_metadata_obj = \
            self.images_provider.jobs_client.list_job_metadata(job.id)
        self.assertEqual(len(list_job_metadata_obj.entity), 0,
                         msg.format("length of the list", 0,
                                    len(list_job_metadata_obj.entity)))

        new_metadata_obj = \
            self.images_provider.jobs_client.set_job_metadata(job.id, keys,
                                                              values)
        self.assertEquals(new_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     new_metadata_obj.status_code))

        list_job_metadata_obj = \
            self.images_provider.jobs_client.list_job_metadata(job.id)
        self.assertEqual(len(list_job_metadata_obj.entity), 0,
                         msg.format("length of the list", 0,
                                    len(list_job_metadata_obj.entity)))

    @attr('positive')
    def test_overwrite_job_metadata_with_empty_job_metadata(self):
        """Overwrite job metadata with empty job metadata.

        1) Create a job from a schedule with metadata
        2) Set an empty job metadata
        3) Verify that the response code is 200
        4) Verify that get job returns empty metadata
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        key = self.config.images.metadata_key
        value = datagen.random_string(size=10)
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        keys = [key]
        values = [value]

        sch_metadata_obj = \
            self.images_provider.schedules_client.set_schedule_metadata(sch.id,
                                                                        keys,
                                                                        values)
        self.assertEquals(sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_metadata_obj.status_code))

        job_obj = self.images_provider.create_active_jobs(sch.id)
        self.assertEquals(job_obj.status_code, 200,
                          msg.format('status_code', 200, job_obj.status_code))

        job = job_obj.entity

        keys = []
        values = []

        job_metadata_obj = \
            self.images_provider.jobs_client.set_job_metadata(job.id, keys,
                                                              values)
        self.assertEquals(job_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     job_metadata_obj.status_code))

        job_metadata = job_metadata_obj.entity

        get_job_obj = \
            self.images_provider.jobs_client.get_job(job.id)
        self.assertEquals(get_job_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     get_job_obj.status_code))

        get_job_metadata = get_job_obj.entity.metadata

        self.assertEquals(get_job_metadata, job_metadata,
                          msg.format('key-value pair', job_metadata,
                                     get_job_metadata))

    @attr('positive')
    def test_set_a_job_metadata_after_setting_an_empty_job_metadata(self):
        """Set a job metadata after setting an empty job metadata.

        1) Create a job from a schedule with metadata
        2) Set an empty job metadata
        3) Verify that the response code is 200
        4) set a valid job metadata for that job
        5) Verify that the response code is 200
        6) Verify the job metadata has been updated as expected
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        key = self.config.images.metadata_key
        value = datagen.random_string(size=10)
        alt_key = self.config.images.alt_metadata_key
        alt_value = datagen.random_string(size=10)
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        keys = [key]
        values = [value]

        sch_metadata_obj = \
            self.images_provider.schedules_client.set_schedule_metadata(sch.id,
                                                                        keys,
                                                                        values)
        self.assertEquals(sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_metadata_obj.status_code))

        job_obj = self.images_provider.create_active_jobs(sch.id)
        self.assertEquals(job_obj.status_code, 200,
                          msg.format('status_code', 200, job_obj.status_code))

        job = job_obj.entity

        keys = []
        values = []

        job_metadata_obj = \
            self.images_provider.jobs_client.set_job_metadata(job.id, keys,
                                                              values)
        self.assertEquals(job_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     job_metadata_obj.status_code))

        keys = [alt_key]
        values = [alt_value]

        new_metadata_obj = \
            self.images_provider.jobs_client.set_job_metadata(job.id, keys,
                                                              values)
        self.assertEquals(new_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     new_metadata_obj.status_code))

        new_metadata = new_metadata_obj.entity

        get_job_obj = \
            self.images_provider.jobs_client.get_job(job.id)
        self.assertEquals(get_job_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     get_job_obj.status_code))

        get_job_metadata = get_job_obj.entity.metadata

        self.assertEquals(get_job_metadata, new_metadata,
                          msg.format('key-value pair', new_metadata,
                                     get_job_metadata))

    @attr('positive')
    def test_set_multiple_job_metadata_after_setting_empty_job_metadata(self):
        """Set multiple job metadata after setting an empty job metadata.

        1) Create a job from a schedule with metadata
        2) Set an empty job metadata
        3) Verify that the response code is 200
        4) set multiple valid job metadata for that schedule
        5) Verify that the response code is 200
        6) Verify the job metadata has been updated as expected
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        key = self.config.images.metadata_key
        value = datagen.random_string(size=10)
        alt_key = self.config.images.alt_metadata_key
        alt_value = datagen.random_string(size=10)
        third_key = self.config.images.third_metadata_key
        third_value = datagen.random_string(size=10)
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        keys = [key]
        values = [value]

        sch_metadata_obj = \
            self.images_provider.schedules_client.set_schedule_metadata(sch.id,
                                                                        keys,
                                                                        values)
        self.assertEquals(sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_metadata_obj.status_code))

        job_obj = self.images_provider.create_active_jobs(sch.id)
        self.assertEquals(job_obj.status_code, 200,
                          msg.format('status_code', 200, job_obj.status_code))

        job = job_obj.entity

        keys = []
        values = []

        job_metadata_obj = \
            self.images_provider.jobs_client.set_job_metadata(job.id, keys,
                                                              values)
        self.assertEquals(job_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     job_metadata_obj.status_code))

        keys = [alt_key, third_key]
        values = [alt_value, third_value]

        new_metadata_obj = \
            self.images_provider.jobs_client.set_job_metadata(job.id, keys,
                                                              values)
        self.assertEquals(new_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     new_metadata_obj.status_code))

        get_job_obj = \
            self.images_provider.jobs_client.get_job(job.id)
        self.assertEquals(get_job_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     get_job_obj.status_code))

        get_job_metadata = get_job_obj.entity.metadata

        for metadata_key, metadata_value in get_job_metadata.items():
            if metadata_key == alt_key:
                self.assertEquals(metadata_value, alt_value,
                                  msg.format('alt_value', alt_value,
                                             metadata_value))
            elif metadata_key == third_key:
                self.assertEquals(metadata_value, third_value,
                                  msg.format('third_value', third_value,
                                             metadata_value))
            else:
                self.assertEquals(metadata_key, alt_key,
                                  msg.format('key', alt_key, metadata_key))
                self.assertEquals(metadata_key, third_key,
                                  msg.format('key', third_key, metadata_key))

    @attr('positive')
    def test_set_single_job_metadata_for_job_with_more_than_one_metadata(self):
        """Set a single job metadata for job with more than one metadata.

        1) Create a job from a schedule without metadata
        2) Create multiple metadata for the job
        3) Verify that the response code is 200
        4) Overwrite all metadata with a single job metadata
        5) Verify that the response code is 200
        6) Verify the job metadata has been updated as expected
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        key = self.config.images.metadata_key
        value = datagen.random_string(size=10)
        alt_key = self.config.images.alt_metadata_key
        alt_value = datagen.random_string(size=10)
        third_key = self.config.images.third_metadata_key
        third_value = datagen.random_string(size=10)
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        keys = [key, alt_key]
        values = [value, alt_value]

        sch_metadata_obj = \
            self.images_provider.schedules_client.set_schedule_metadata(sch.id,
                                                                        keys,
                                                                        values)
        self.assertEquals(sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_metadata_obj.status_code))

        job_obj = self.images_provider.create_active_jobs(sch.id)
        self.assertEquals(job_obj.status_code, 200,
                          msg.format('status_code', 200, job_obj.status_code))

        job = job_obj.entity

        keys = [third_key]
        values = [third_value]

        job_metadata_obj = \
            self.images_provider.jobs_client.set_job_metadata(job.id, keys,
                                                              values)
        self.assertEquals(job_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     job_metadata_obj.status_code))

        job_metadata = job_metadata_obj.entity

        get_job_obj = \
            self.images_provider.jobs_client.get_job(job.id)
        self.assertEquals(get_job_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     get_job_obj.status_code))

        get_job_metadata = get_job_obj.entity.metadata

        self.assertEquals(get_job_metadata, job_metadata,
                          msg.format('key-value pair', job_metadata,
                                     get_job_metadata))

    @attr('positive')
    def test_set_multiple_job_metadata_for_job_with_a_single_metadata(self):
        """Set multiple job metadata for job with a single metadata.

        1) Create a job from a schedule without metadata
        2) Create a single metadata for the job
        3) Verify that the response code is 200
        4) Overwrite the single metadata with multiple job metadata
        5) Verify that the response code is 200
        6) Verify the job metadata has been updated as expected
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        key = self.config.images.metadata_key
        value = datagen.random_string(size=10)
        alt_key = self.config.images.alt_metadata_key
        alt_value = datagen.random_string(size=10)
        third_key = self.config.images.third_metadata_key
        third_value = datagen.random_string(size=10)
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        keys = [key]
        values = [value]

        sch_metadata_obj = \
            self.images_provider.schedules_client.set_schedule_metadata(sch.id,
                                                                        keys,
                                                                        values)
        self.assertEquals(sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_metadata_obj.status_code))

        job_obj = self.images_provider.create_active_jobs(sch.id)
        self.assertEquals(job_obj.status_code, 200,
                          msg.format('status_code', 200, job_obj.status_code))

        job = job_obj.entity

        keys = [alt_key, third_key]
        values = [alt_value, third_value]

        job_metadata_obj = \
            self.images_provider.jobs_client.set_job_metadata(job.id, keys,
                                                              values)
        self.assertEquals(job_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     job_metadata_obj.status_code))

        get_job_obj = \
            self.images_provider.jobs_client.get_job(job.id)
        self.assertEquals(get_job_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     get_job_obj.status_code))

        get_job_metadata = get_job_obj.entity.metadata

        for metadata_key, metadata_value in get_job_metadata.items():
            if metadata_key == alt_key:
                self.assertEquals(metadata_value, alt_value,
                                  msg.format('alt_value', alt_value,
                                             metadata_value))
            elif metadata_key == third_key:
                self.assertEquals(metadata_value, third_value,
                                  msg.format('third_value', third_value,
                                             metadata_value))
            else:
                self.assertEquals(metadata_key, alt_key,
                                  msg.format('key', alt_key, metadata_key))
                self.assertEquals(metadata_key, third_key,
                                  msg.format('key', third_key, metadata_key))
