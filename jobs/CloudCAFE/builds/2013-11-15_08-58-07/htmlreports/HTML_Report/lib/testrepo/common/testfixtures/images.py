from ccengine.common.constants.images_constants import Constants
from ccengine.common.exception_handler.exception_handler \
    import ExceptionHandler
from ccengine.common.exceptions.compute import ItemNotFound
from ccengine.domain.configuration import IdentityAPIConfig
from ccengine.domain.configuration import MiscConfig
from ccengine.providers.atomhopper import AtomHopperProvider
from ccengine.providers.configuration import MasterConfigProvider as _MCP
from ccengine.providers.images.images_api import ImagesProvider
from testrepo.common.testfixtures.fixtures import BaseTestFixture


class BaseImagesFixture(BaseTestFixture):
    """Fixture for scheduled images tests."""

    @classmethod
    def setUpClass(cls):

        super(BaseImagesFixture, cls).setUpClass()

        cls.schedules_to_delete = []
        cls.workers_to_delete = []
        cls.jobs_to_delete = []
        cls.instances_to_disable = []
        cls.servers_to_delete = []
        cls.snapshots_to_delete = []

        cls.images_provider = ImagesProvider(cls.config, cls.fixture_log,
                                             cls.schedules_to_delete,
                                             cls.workers_to_delete,
                                             cls.jobs_to_delete,
                                             cls.instances_to_disable,
                                             cls.servers_to_delete,
                                             cls.snapshots_to_delete)
        cls.images_provider.schedules_client.add_exception_handler(
            ExceptionHandler())

        cls.tenant = cls.config.images.tenant
        cls.alt_tenant = cls.config.images.alt_tenant
        cls.tenant_id = cls.config.images.tenant_id
        cls.action = cls.config.images.action
        cls.alt_action = cls.config.images.alt_action
        cls.retention = int(cls.config.images.retention)
        cls.alt_retention = int(cls.config.images.alt_retention)
        cls.msg = Constants.MESSAGE
        cls.ext_deserializer = cls.config.misc.ext_deserializer
        cls.alt_job_status = cls.config.images.alt_job_status
        cls.marker = None

    @classmethod
    def tearDownClass(cls):

        super(BaseImagesFixture, cls).tearDownClass()

        marker = None

        cls.fixture_log.debug('Cleaning up schedules, workers, jobs,'
                              'instances and snapshots')

        for schedule_id in cls.schedules_to_delete:

            keys = ["schedule_id", "marker"]
            values = [schedule_id, marker]

            try:
                cls.images_provider.schedules_client.delete_schedule(
                    schedule_id)
            except ItemNotFound:
                continue
            try:
                for job in cls.images_provider.list_jobs_for_schedule(
                        schedule_id, keys, values):
                    cls.images_provider.jobs_client.delete_job(job.id)
            except ItemNotFound:
                continue

        for job_id in cls.jobs_to_delete:
            try:
                cls.images_provider.jobs_client.delete_job(job_id)
            except ItemNotFound:
                continue

        for server_id in cls.servers_to_delete:
            try:
                cls.images_provider.servers_client.delete_server(server_id)
            except ItemNotFound:
                continue
            try:
                for snapshot in cls.images_provider.list_snapshots_for_server(
                        server_id):
                    if snapshot.id not in cls.snapshots_to_delete:
                        cls.images_provider.nova_images_client.delete_image(
                            snapshot.id)
            except ItemNotFound:
                continue

        for snapshot_id in cls.snapshots_to_delete:
            try:
                cls.images_provider.nova_images_client.delete_image(
                    snapshot_id)
            except ItemNotFound:
                continue

        cls.images_provider.schedules_client.delete_exception_handler(
            ExceptionHandler())


class ImagesEventsFixture(BaseImagesFixture):
    """Fixture for scheduled images events tests."""

    @classmethod
    def setUpClass(cls):

        super(ImagesEventsFixture, cls).setUpClass()

        ah_dict = {MiscConfig.SECTION_NAME: {'serializer': 'xml',
                                             'deserializer': 'xml'}}
        ah_config = cls.config.mcp_override(ah_dict)
        glance_atom_hopper_url = "{0}{1}".format(
            ah_config.compute_api.atom_hopper_url, "/glance/events")
        cls.glance_atomhopper_provider = AtomHopperProvider(
            glance_atom_hopper_url, ah_config)


class RbacImagesFixture(BaseImagesFixture):
    """Fixture for RBAC scheduled images tests."""

    @classmethod
    def setUpClass(cls):

        super(RbacImagesFixture, cls).setUpClass()

        # Initialize compute provider for alt Admin user
        config = _MCP()
        admin_user_auth = {IdentityAPIConfig.SECTION_NAME:
                           {'username': config.auth.alt_admin,
                            'api_key': config.auth.alt_admin_key}}
        cls.alt_admin_img_prov = cls._get_user_provider(config,
                                                        admin_user_auth)
        cls.alt_admin_img_prov.schedules_client.add_exception_handler(
            ExceptionHandler())

        # Initialize compute provider for diff Admin user
        admin_user_auth = {IdentityAPIConfig.SECTION_NAME:
                           {'username': config.auth.diff_admin,
                            'api_key': config.auth.diff_admin_key}}
        cls.diff_admin_img_prov = cls._get_user_provider(config,
                                                         admin_user_auth)
        cls.diff_admin_img_prov.schedules_client.add_exception_handler(
            ExceptionHandler())

        # Initialize compute provider for global Admin user
        admin_user_auth = {IdentityAPIConfig.SECTION_NAME:
                           {'username': config.auth.global_admin,
                            'api_key': config.auth.global_admin_key}}
        cls.global_admin_img_prov = cls._get_user_provider(config,
                                                           admin_user_auth)
        cls.global_admin_img_prov.schedules_client.add_exception_handler(
            ExceptionHandler())

        # Initialize compute provider for diff global Admin user
        admin_user_auth = {IdentityAPIConfig.SECTION_NAME:
                           {'username': config.auth.diff_global_admin,
                            'api_key': config.auth.diff_global_admin_key}}
        cls.diff_global_admin_img_prov = cls._get_user_provider(
            config, admin_user_auth)
        cls.diff_global_admin_img_prov.schedules_client.add_exception_handler(
            ExceptionHandler())

        # Initialize images provider for Creator user
        creator_user_auth = {IdentityAPIConfig.SECTION_NAME:
                             {'username': str(config.auth.creator),
                              'api_key': str(config.auth.creator_key)}}
        cls.creator_images_provider = cls._get_user_provider(config,
                                                             creator_user_auth)
        cls.creator_images_provider.schedules_client.add_exception_handler(
            ExceptionHandler())

        # Initialize images provider for alt Creator user
        creator_user_auth = {IdentityAPIConfig.SECTION_NAME:
                             {'username': str(config.auth.alt_creator),
                              'api_key': str(config.auth.alt_creator_key)}}
        cls.alt_creator_img_prov = cls._get_user_provider(config,
                                                          creator_user_auth)
        cls.alt_creator_img_prov.schedules_client.add_exception_handler(
            ExceptionHandler())

        # Initialize images provider for diff Creator user
        creator_user_auth = {IdentityAPIConfig.SECTION_NAME:
                             {'username': str(config.auth.diff_creator),
                              'api_key': str(config.auth.diff_creator_key)}}
        cls.diff_creator_img_prov = cls._get_user_provider(config,
                                                           creator_user_auth)
        cls.diff_creator_img_prov.schedules_client.add_exception_handler(
            ExceptionHandler())

        # Initialize compute provider for Observer user
        observer_user_auth = {IdentityAPIConfig.SECTION_NAME:
                              {'username': config.auth.observer,
                               'api_key': config.auth.observer_key}}
        cls.observer_images_provider = cls._get_user_provider(
            config, observer_user_auth)
        cls.observer_images_provider.schedules_client.add_exception_handler(
            ExceptionHandler())

        # Initialize compute provider for alt Observer user
        observer_user_auth = {IdentityAPIConfig.SECTION_NAME:
                              {'username': config.auth.alt_observer,
                               'api_key': config.auth.alt_observer_key}}
        cls.alt_observer_img_prov = cls._get_user_provider(config,
                                                           observer_user_auth)
        cls.alt_observer_img_prov.schedules_client.add_exception_handler(
            ExceptionHandler())

        # Initialize compute provider for diff Observer user
        observer_user_auth = {IdentityAPIConfig.SECTION_NAME:
                              {'username': config.auth.diff_observer,
                               'api_key': config.auth.diff_observer_key}}
        cls.diff_observer_img_prov = cls._get_user_provider(config,
                                                            observer_user_auth)
        cls.diff_observer_img_prov.schedules_client.add_exception_handler(
            ExceptionHandler())

        # Initialize compute provider for global Observer user
        user_auth = {IdentityAPIConfig.SECTION_NAME:
                     {'username': config.auth.global_observer,
                      'api_key': config.auth.global_observer_key}}
        cls.global_observer_img_prov = cls._get_user_provider(config,
                                                              user_auth)
        cls.global_observer_img_prov.schedules_client.add_exception_handler(
            ExceptionHandler())

        # Initialize compute provider for diff global Observer user
        user_auth = {IdentityAPIConfig.SECTION_NAME:
                     {'username': config.auth.diff_global_observer,
                      'api_key': config.auth.diff_global_observer_key}}
        cls.diff_glbl_obsrvr_img_prov = cls._get_user_provider(config,
                                                               user_auth)
        cls.diff_glbl_obsrvr_img_prov.schedules_client.add_exception_handler(
            ExceptionHandler())

    @classmethod
    def _get_user_provider(self, config, user_auth):
        """Retrieves a specific user provider."""

        user_conf = config.mcp_override(user_auth)

        return ImagesProvider(user_conf, self.fixture_log,
                              self.schedules_to_delete, self.workers_to_delete,
                              self.jobs_to_delete, self.instances_to_disable,
                              self.servers_to_delete, self.snapshots_to_delete)
