from testrepo.common.testfixtures.images import BaseImagesFixture
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
import ccengine.common.tools.datagen as datagen


class TestQonosListJobMetadata(BaseImagesFixture):

    @attr('positive')
    def test_happy_path_list_job_metadata(self):
        '''Happy Path - List job metadata'''

        """
        1) Create a schedule containing metadata so that a job is created for
            it within the next 5 minutes
        2) Create a job from the schedule
        3) List job metadata
        4) Verify that the response code is 200
        5) Verify that the job metadata is as expected

        Attributes to verify:
            key
            value
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

        list_sch_metadata_obj = self.images_provider.schedules_client.\
            list_schedule_metadata(sch.id)
        self.assertEquals(list_sch_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_sch_metadata_obj.status_code))

        list_sch_metadata = list_sch_metadata_obj.entity

        job_obj = self.images_provider.create_active_jobs(sch.id)
        self.assertEquals(job_obj.status_code, 200,
                          msg.format('status_code', 200, job_obj.status_code))

        job = job_obj.entity

        list_job_metadata_obj = \
            self.images_provider.jobs_client.list_job_metadata(job.id)
        self.assertEquals(list_job_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_job_metadata_obj.status_code))

        list_job_metadata = list_job_metadata_obj.entity

        self.assertEquals(list_job_metadata, list_sch_metadata,
                          msg.format('key-value pair', list_sch_metadata,
                                     list_job_metadata))

    @attr('positive')
    def test_list_job_metadata_with_multiple_job_metadata(self):
        '''List job metadata with multiple job metadata present'''

        """
        1) Create a schedule containing multiple metadata so that a job is
            created for it within the next 5 minutes
        2) Create a job from the schedule
        3) List job metadata
        4) Verify that the response code is 200
        5) Verify that the job metadata is as expected

        Attributes to verify:
            key
            value
        """

        # Have to use random strings when using a list metadata
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

        keys = [key, alt_key]
        values = [value, alt_value]

        new_metadata_obj = \
            self.images_provider.schedules_client.set_schedule_metadata(sch.id,
                                                                        keys,
                                                                        values)
        self.assertEquals(new_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     new_metadata_obj.status_code))

        job_obj = self.images_provider.create_active_jobs(sch.id)
        self.assertEquals(job_obj.status_code, 200,
                          msg.format('status_code', 200, job_obj.status_code))

        job = job_obj.entity

        list_job_metadata_obj = \
            self.images_provider.jobs_client.list_job_metadata(job.id)
        self.assertEquals(list_job_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_job_metadata_obj.status_code))

        list_job_metadata = list_job_metadata_obj.entity

        for metadata_key, metadata_value in list_job_metadata.items():
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
    def test_list_job_metadata_with_no_job_metadata(self):
        '''List job metadata with no job metadata present'''

        """
        1) Create a schedule containing no metadata so that a job is
            created for it within the next 5 minutes
        2) Create a job from the schedule
        3) List job metadata
        4) Verify that the response code is 200
        5) Verify that the job metadata is as expected

        Attributes to verify:
            key
            value
        """

        # Have to use random strings when using a list metadata
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

        list_job_metadata_obj = \
            self.images_provider.jobs_client.list_job_metadata(job.id)
        self.assertEquals(list_job_metadata_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_job_metadata_obj.status_code))

        list_job_metadata = list_job_metadata_obj.entity
        self.assertEquals(list_job_metadata, {},
                          msg.format('key-value pair', {},
                                     list_job_metadata))
