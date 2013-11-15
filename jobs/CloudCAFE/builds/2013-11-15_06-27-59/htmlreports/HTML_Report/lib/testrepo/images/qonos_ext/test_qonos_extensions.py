from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
from testrepo.common.testfixtures.images import BaseImagesFixture


class TestQonosExtensions(BaseImagesFixture):

    @attr('smoke')
    def test_happy_path_list_extensions(self):
        """Happy Path - List Extensions.

        1) List extensions
        2) Verify that the response code is 200
        3) Verify that the rax-si-image-schedule extension is listed
        4) Verify that all of the attributes are listed as expected
        """

        tenant_id = self.config.images.tenant_id
        alias_list = []
        msg = Constants.MESSAGE

        list_ext_obj = self.images_provider.scheduled_images_client. \
            list_extensions(tenant_id)
        self.assertEquals(list_ext_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_ext_obj.status_code))

        list_ext = list_ext_obj.entity

        for e in list_ext:
            alias_list.append(e.alias)
            if e.alias == 'rax-si-image-schedule':
                ext = e

        self.assertIn('rax-si-image-schedule', alias_list,
                      msg.format('rax-si-image-schedule',
                                 "rax-si-image-schedule to be in list",
                                 "rax-si-image-schedule not in list"))
        self.assertIsNotNone(ext.updated, msg.format('updated', "valid value",
                                                     None))
        self.assertEquals(ext.name, 'ScheduledImages',
                          msg.format('name', "ScheduledImages", ext.name))
        self.assertEquals(ext.links, [],
                          msg.format('links', [], ext.links))
        url = "http://docs.openstack.org/servers/api/ext/scheduled_images/v1.0"
        self.assertEquals(ext.namespace, url,
                          msg.format('namespace', url, ext.namespace))
        self.assertEquals(ext.alias, 'rax-si-image-schedule',
                          msg.format('alias', 'rax-si-image-schedule',
                                     ext.alias))
        desc = "Enables automatic scheduled images to be taken of a server."
        self.assertEquals(ext.description, desc,
                          msg.format('description', desc, ext.description))

    @attr('smoke')
    def test_happy_path_get_os_si_image_schedule_extension(self):
        """Happy Path - Get rax-si-image-schedule extension.

        1) Get rax-si-image-schedule extension
        2) Verify that the response code is 200
        3) Verify that all of the attributes are listed as expected
        """

        tenant_id = self.config.images.tenant_id
        alias = self.config.images.scheduled_images_alias
        msg = Constants.MESSAGE

        get_ext_obj = self.images_provider.scheduled_images_client. \
            get_extension(tenant_id, alias)
        self.assertEquals(get_ext_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     get_ext_obj.status_code))

        get_ext = get_ext_obj.entity

        self.assertIsNotNone(get_ext.updated, msg.format(
            'updated', "valid value", None))
        self.assertEquals(get_ext.name, 'ScheduledImages',
                          msg.format('name', "ScheduledImages", get_ext.name))
        self.assertEquals(get_ext.links, [],
                          msg.format('links', [], get_ext.links))
        url = "http://docs.openstack.org/servers/api/ext/scheduled_images/v1.0"
        self.assertEquals(get_ext.namespace, url,
                          msg.format('namespace', url, get_ext.namespace))
        self.assertEquals(get_ext.alias, 'rax-si-image-schedule',
                          msg.format('alias', 'rax-si-image-schedule',
                                     get_ext.alias))
        desc = "Enables automatic scheduled images to be taken of a server."
        self.assertEquals(get_ext.description, desc,
                          msg.format('description', desc, get_ext.description))
