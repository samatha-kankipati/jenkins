'''
@summary: Interfaces to provide config values to code
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''

import ConfigParser
import json
from ccengine.common.tools import logging_tools

# testconfig dict keywords
TEST_CONFIG_FILE_OSENV = 'CLOUDCAFE_TEST_CONFIG'


class _BaseConfig(object):
    SECTION_NAME = None

    def __init__(self, conf):
        self.conf = conf
        self._log = logging_tools.getLogger(
            logging_tools.get_object_namespace(self.__class__))

    def __repr__(self):
        return str(self.conf)

    def get(self, item_name, default=None):

        try:
            return self.conf.get(self.SECTION_NAME, item_name)
        except ConfigParser.NoOptionError as e:
            self._log.error(str(e))
            return default
        except ConfigParser.NoSectionError as e:
            self._log.error(str(e))
            pass

    def get_raw(self, item_name, default=None):
        '''Performs a get() on SafeConfigParser object without interopolation
        '''

        try:
            return self.conf.get(self.SECTION_NAME, item_name, raw=True)
        except ConfigParser.NoOptionError as e:
            self._log.error(str(e))
            return default
        except ConfigParser.NoSectionError as e:
            self._log.error(str(e))
            pass

    def getboolean(self, item_name, default=None):

        try:
            return self.conf.getboolean(self.SECTION_NAME, item_name)
        except ConfigParser.NoOptionError as e:
            self._log.error(str(e))
            return default
        except ConfigParser.NoSectionError as e:
            self._log.error(str(e))
            pass


class MiscConfig(_BaseConfig):

    SECTION_NAME = 'misc'

    @property
    def serializer(self):
        return self.get("serializer")

    @property
    def deserializer(self):
        return self.get("deserializer")

    @property
    def ext_serializer(self):
        return self.get("ext_serializer")

    @property
    def ext_deserializer(self):
        return self.get("ext_deserializer")


class LoggingConfig(_BaseConfig):

    SECTION_NAME = 'logging'

    @property
    def python_log_file(self):
        return self.get("python_log_file", 'cclog.log')

    @property
    def python_log_dir(self):
        return self.get("python_log_dir", './')

    @property
    def python_log_level(self):
        return self.get("python_log_dir", 'debug')


class IdentityAPIConfig(_BaseConfig):
    '''http://docs.rackspace.com/auth/api/v2.0/auth-client-devguide/content/
    QuickStart-000.html'''

    SECTION_NAME = 'identity'

    @property
    def authentication_endpoint(self):
        return self.get("authentication_endpoint")

    @property
    def username(self):
        return self.get("username")

    @property
    def password(self):
        return self.get("password")

    @property
    def api_key(self):
        return self.get("api_key")

    @property
    def version(self):
        return self.get("version")

    @property
    def alt_username(self):
        return self.get("alt_username")

    @property
    def alt_password(self):
        return self.get("alt_password")

    @property
    def alt_api_key(self):
        return self.get("alt_api_key")

    @property
    def admin_username(self):
        return self.get("admin_username")

    @property
    def admin_password(self):
        return self.get("admin_password")

    @property
    def admin_api_key(self):
        return self.get("admin_api_key")

    @property
    def tenant_name(self):
        return self.get("tenant_name")

    @property
    def tenant_id(self):
        return self.get('tenant_id')

    @property
    def id(self):
        return self.get('id')

    @property
    def low_limit_username(self):
        return self.get("low_limit_username")

    @property
    def low_limit_user_password(self):
        return self.get("low_limit_user_password")

    @property
    def false_api_key(self):
        return self.get("false_api_key")

    @property
    def false_password(self):
        return self.get("false_password")

    @property
    def false_token(self):
        return self.get("false_token")

    @property
    def false_tenant_id(self):
        return self.get("false_tenant_id")

    @property
    def mosso_Id(self):
        return self.get("mosso_Id")

    @property
    def mosso_key(self):
        return self.get("mosso_key")

    @property
    def nast_Id(self):
        return self.get("nast_Id")

    @property
    def nast_key(self):
        return self.get("nast_key")

    @property
    def service_username(self):
        return self.get("service_username")

    @property
    def service_password(self):
        return self.get("service_password")

    @property
    def wait_time(self):
        return self.get("wait_time")

    @property
    def identityAdminRoleId(self):
        return self.get('identityAdminRoleId')

    @property
    def userAdminRoleId(self):
        return self.get('userAdminRoleId')

    @property
    def defaultUserRoleId(self):
        return self.get('defaultUserRoleId')

    @property
    def serviceAdminRoleId(self):
        return self.get('serviceAdminRoleId')

    @property
    def default_email(self):
        return self.get("default_email")

    @property
    def default_region(self):
        return self.get("default_region")

    @property
    def atom_hopper_url(self):
        return self.get('atom_hopper_url')

    @property
    def user_manage_role_id(self):
        return self.get('user_manage_role_id')


class AuthConfig(_BaseConfig):

    SECTION_NAME = 'auth'

    @property
    def base_url(self):
        return self.get("base_url")

    @property
    def username(self):
        return self.get("username")

    @property
    def admin_username(self):
        return self.get("admin_username")

    @property
    def password(self):
        return self.get("password")

    @property
    def admin_password(self):
        return self.get("admin_password")

    @property
    def tenant_name(self):
        return self.get("tenant_name")

    @property
    def tenant_id(self):
        return self.get('tenant_id')

    @property
    def id(self):
        return self.get('id')

    @property
    def api_key(self):
        return self.get("api_key")

    @property
    def alt_username(self):
        return self.get("alt_username")

    @property
    def alt_password(self):
        return self.get("alt_password")

    @property
    def alt_api_key(self):
        return self.get("alt_api_key")

    @property
    def alt_tenant_id(self):
        return self.get("alt_tenant_id")

    @property
    def alt_user_id(self):
        return self.get("alt_user_id")

    @property
    def low_limit_username(self):
        return self.get("low_limit_username")

    @property
    def low_limit_user_password(self):
        return self.get("low_limit_user_password")

    @property
    def creator(self):
        return self.get("creator")

    @property
    def creator_key(self):
        return self.get("creator_key")

    @property
    def alt_creator(self):
        return self.get("alt_creator")

    @property
    def alt_creator_key(self):
        return self.get("alt_creator_key")

    @property
    def diff_creator(self):
        return self.get("diff_creator")

    @property
    def diff_creator_key(self):
        return self.get("diff_creator_key")

    @property
    def observer(self):
        return self.get("observer")

    @property
    def observer_key(self):
        return self.get("observer_key")

    @property
    def alt_observer(self):
        return self.get("alt_observer")

    @property
    def alt_observer_key(self):
        return self.get("alt_observer_key")

    @property
    def diff_observer(self):
        return self.get("diff_observer")

    @property
    def diff_observer_key(self):
        return self.get("diff_observer_key")

    @property
    def global_observer(self):
        """Global observer user name."""
        return self.get("global_observer")

    @property
    def global_observer_key(self):
        """Global observer api key."""
        return self.get("global_observer_key")

    @property
    def diff_global_observer(self):
        """Global observer user name for different account."""
        return self.get("diff_global_observer")

    @property
    def diff_global_observer_key(self):
        """Global observer api key for different account."""
        return self.get("diff_global_observer_key")

    @property
    def alt_admin(self):
        return self.get("alt_admin")

    @property
    def alt_admin_key(self):
        return self.get("alt_admin_key")

    @property
    def diff_admin(self):
        return self.get("diff_admin")

    @property
    def diff_admin_key(self):
        return self.get("diff_admin_key")

    @property
    def global_admin(self):
        """Global admin user name."""
        return self.get("global_admin")

    @property
    def global_admin_key(self):
        """Global admin api key."""
        return self.get("global_admin_key")

    @property
    def diff_global_admin(self):
        """Global admin user name for different account."""
        return self.get("diff_global_admin")

    @property
    def diff_global_admin_key(self):
        """Global admin api key for different account."""
        return self.get("diff_global_admin_key")

    @property
    def version(self):
        return self.get("version")

    @property
    def false_api_key(self):
        return self.get("false_api_key")

    @property
    def false_password(self):
        return self.get("false_password")

    @property
    def false_token(self):
        return self.get("false_token")

    @property
    def false_tenant_id(self):
        return self.get("false_tenant_id")

    @property
    def mosso_Id(self):
        return self.get("mosso_Id")

    @property
    def mosso_key(self):
        return self.get("mosso_key")

    @property
    def core_auth_url(self):
        return self.get("core_auth_url")

    @property
    def core_username(self):
        return self.get("core_username")

    @property
    def core_password(self):
        return self.get("core_password")

    @property
    def core_version(self):
        return self.get("core_version")

    @property
    def account_services_url(self):
        return self.get("account_services_url")

    @property
    def account_services_username(self):
        return self.get("account_services_username")

    @property
    def account_services_password(self):
        return self.get("account_services_password")

    def __repr__(self):
        s = ''
        s = s + 'base_url: %s \n' % (self.base_url)
        s = s + 'username: %s \n' % (self.username)
        s = s + 'password: %s \n' % (self.password)
        s = s + 'api_key: %s \n' % (self.api_key)
        s = s + 'version: %s \n' % (self.version)
        return s


class LdapConfig(_BaseConfig):
    SECTION_NAME = 'ldap'

    @property
    def host(self):
        return self.get("host")

    @property
    def bind_dn(self):
        return self.get("bind_dn")

    @property
    def password(self):
        return self.get("password")

    @property
    def port(self):
        return self.get("port")

    @property
    def open_ldap(self):
        return self.get("open_ldap")

    @property
    def page_size(self):
        return self.get("page_size")

    @property
    def openldap_host(self):
        return self.get("openldap_host")

    @property
    def openldap_port(self):
        return self.get("openldap_port")


class MoneyballAPIConfig(_BaseConfig):
    SECTION_NAME = 'moneyball'

    @property
    def base_url(self):
        return self.get("base_url")

    @property
    def base_url_dev(self):
        return self.get("base_url_dev")

    @property
    def base_url_prod(self):
        return self.get("base_url_prod")


class Rackconnect(_BaseConfig):
    SECTION_NAME = 'rackconnect'

    @property
    def account_number(self):
        return self.get("account_number")

    @property
    def url(self):
        return self.get("url")

    @property
    def user(self):
        return self.get("user")

    @property
    def password(self):
        return self.get("password")

    @property
    def rackconnect_timeout(self):
        return self.get("rackconnect_timeout")


class LavaAPIConfig(_BaseConfig):
    SECTION_NAME = 'lava_api'

    @property
    def AUTH_TOKEN(self):
        """Authentication TOKEN for lava api"""
        return self.get("AUTH_TOKEN")

    @property
    def BASE_URL(self):
        """Base URL for lava api"""
        return self.get("BASE_URL")

    @property
    def VERSIONLESS_LINK(self):
        """Versionless URL for lava api"""
        return self.get("VERSIONLESS_LINK")

    @property
    def USER_NAME(self):
        """Username for lava api authentication """
        return self.get("USER_NAME")

    @property
    def PASSWORD(self):
        """Username for lava api authentication """
        return self.get("PASSWORD")

    @property
    def TEST_DATA_PATH(self):
        """Location of our test data for LAVA """
        return self.get("TEST_DATA_PATH")

    @property
    def SWIFTLY_AUTH_URL(self):
        """Authentication url for swiftly """
        return self.get("SWIFTLY_AUTH_URL")

    @property
    def SWIFTLY_AUTH_USER(self):
        """Authentication username for swiftly """
        return self.get("SWIFTLY_AUTH_USER")

    @property
    def SWIFTLY_AUTH_KEY(self):
        """Authentication key for swiftly """
        return self.get("SWIFTLY_AUTH_KEY")

    @property
    def PIG_TIMEOUT(self):
        return self.get("PIG_TIMEOUT")

    @property
    def BULK_CLUSTER_CREATE_TIMEOUT(self):
        return self.get("BULK_CLUSTER_CREATE_TIMEOUT")

    @property
    def NODE_REBOOT_TIMEOUT(self):
        return self.get("NODE_REBOOT_TIMEOUT")

    @property
    def MAX_SIMULTANEOUS_CLUSTERS(self):
        return self.get("MAX_SIMULTANEOUS_CLUSTERS")

    @property
    def REPEATED_CLUSTER_CREATION(self):
        return self.get("REPEATED_CLUSTER_CREATION")

    @property
    def PROGRESSIVE_CLUSTER_RESIZE_FACTOR(self):
        return self.get("PROGRESSIVE_CLUSTER_RESIZE_FACTOR")

    @property
    def PROGRESSIVE_CLUSTER_RESIZE_MAX(self):
        return self.get("PROGRESSIVE_CLUSTER_RESIZE_MAX")

    @property
    def PROGRESSIVE_CLUSTER_CREATE_FACTOR(self):
        return self.get("PROGRESSIVE_CLUSTER_CREATE_FACTOR")

    @property
    def PROGRESSIVE_CLUSTER_CREATE_MAX(self):
        return self.get("PROGRESSIVE_CLUSTER_CREATE_MAX")

    @property
    def CLUSTER_CREATE_TIMEOUT(self):
        return self.get("CLUSTER_CREATE_TIMEOUT")

    @property
    def CLUSTER_SLEEP_INTERVAL(self):
        return self.get("CLUSTER_SLEEP_INTERVAL")

    @property
    def EPHEMERAL_DISK_PATH(self):
        return self.get("EPHEMERAL_DISK_PATH")

    @property
    def PRIMARY_DISK_PATH(self):
        return self.get("PRIMARY_DISK_PATH")

    @property
    def DELETE_CLUSTER_TIMEOUT(self):
        return self.get("DELETE_CLUSTER_TIMEOUT")

    @property
    def FLAVOR(self):
        return self.get("FLAVOR")

    @property
    def HADOOP_WEB_PAGE_TIMEOUT(self):
        return self.get("HADOOP_WEB_PAGE_TIMEOUT")

    @property
    def PROFILE_EMAIL(self):
        return self.get("PROFILE_EMAIL")

    @property
    def HADOOP_REPLICATION_COUNT(self):
        return self.get("HADOOP_REPLICATION_COUNT")

    @property
    def TERA_SORT_TIMEOUT(self):
        return self.get("TERA_SORT_TIMEOUT")

    @property
    def SOCKS_PROXY_PORT(self):
        return self.get("SOCKS_PROXY_PORT")


class LunrAPIConfig(_BaseConfig):

    SECTION_NAME = 'lunr_api'

    @property
    def host(self):
        """IP address where lunr api host resides"""
        return self.get("host")

    @property
    def port(self):
        """Port to use for lunr api host"""
        return self.get("port")

    @property
    def ssl(self):
        """Port to use for lunr api host"""
        return self.getboolean("ssl")

    @property
    def version(self):
        return self.get('version')

    @property
    def account_name(self):
        return self.get('account_name')

    @property
    def account_id(self):
        return self.get('account_id')

    @property
    def min_volume_size(self):
        return self.get('min_volume_size', default=100)


class StorageNodeAPIConfig(_BaseConfig):

    SECTION_NAME = 'storage_node_api'

    @property
    def autodetect(self):
        """Bool to tell whether or not to find the info for the storage
        nodes via the lunr api"""
        return self.getboolean("autodetect")

    @property
    def host(self):
        """IP address where lunr api host resides"""
        return self.get("host")

    @property
    def port(self):
        """Port to use for lunr api host"""
        return self.get("port")

    @property
    def ssl(self):
        """Port to use for lunr api host"""
        return self.getboolean("ssl")

ENABLED_VARS = (
    'CINDERCLIENT_INSECURE',
    'CINDER_RAX_AUTH',
    'CINDER_VOLUME_SERVICE_NAME',
    'NOVA_RAX_AUTH',
    'NOVA_API_KEY',
    'NOVACLIENT_DEBUG',
    'NOVACLIENT_INSECURE',
    'NOVA_PROJECT_ID',
    'NOVA_RAX_AUTH',
    'NOVA_SERVICE_NAME',
    'NOVA_URL',
    'NOVA_USERNAME',
    'NOVA_VERSION',
    'NOVA_VOLUME_SERVICE_NAME',
    'OS_AUTH_URL',
    'OS_NO_CACHE',
    'OS_PASSWORD',
    'OS_REGION_NAME',
    'OS_TENANT_NAME',
    'OS_USERNAME',
    'OS_AUTH_SYSTEM',
)


def make_getter(var):
    # this will close the scope on var
    return lambda self: self.get(var, None)


class OpenStackShellConfig(_BaseConfig):

    @property
    def environment_type(self):
        return self.get("environment_type")


# setup properties for OpenStackShellConfig base class
for var in ENABLED_VARS:
    setattr(OpenStackShellConfig, var, property(make_getter(var)))


class CinderShellConfig(OpenStackShellConfig):
    SECTION_NAME = 'cinder_shell'

    @property
    def max_volume_size(self):
        return self.get("max_volume_size", default='1024')

    @property
    def min_volume_size(self):
        return self.get("min_volume_size", default='1')


class NovaShellConfig(OpenStackShellConfig):
    SECTION_NAME = 'nova_shell'

    @property
    def IMAGE_ID(self):
        return self.get("IMAGE_ID", None)

    @property
    def image_name(self):
        return self.get("image_name")

    @property
    def flavor(self):
        return self.get("flavor")

    @property
    def max_volume_size(self):
        return self.get("max_volume_size", default='1024')

    @property
    def min_volume_size(self):
        return self.get("min_volume_size", default='1')


class ComputeAPIConfig(_BaseConfig):
    SECTION_NAME = 'compute'

    @property
    def tenant_id(self):
        return self.get('tenant_id')

    @property
    def region(self):
        return self.get('region')

    @property
    def ssh_timeout(self):
        return int(self.get('ssh_timeout', 300))

    @property
    def build_interval(self):
        return int(self.get('build_interval', 10))

    @property
    def server_status_timeout(self):
        return int(self.get('server_status_timeout', 300))

    @property
    def server_delete_timeout(self):
        return int(self.get('server_delete_timeout', 30))

    @property
    def datetime_seconds_leeway(self):
        return int(self.get('datetime_seconds_leeway', 60))

    @property
    def image_ref(self):
        return self.get('image_ref')

    @property
    def image_ref_alt(self):
        return self.get('image_ref_alt')

    @property
    def windows_image_ref(self):
        return self.get('windows_image_ref')

    @property
    def flavor_ref(self):
        return self.get('flavor_ref')

    @property
    def flavor_ref_alt(self):
        return self.get('flavor_ref_alt')

    @property
    def create_image_enabled(self):
        return self.get('create_image_enabled')

    @property
    def resize_available(self):
        return self.get('resize_available')

    @property
    def authentication(self):
        return self.get('authentication')

    @property
    def os_type(self):
        return self.get('os_type')

    @property
    def use_xml_format(self):
        return self.get('use_xml_format')

    @property
    def ip_address_version_for_ssh(self):
        return self.get('ip_address_version_for_ssh')

    @property
    def network_for_ssh(self):
        return self.get('network_for_ssh')

    @property
    def compute_endpoint_name(self):
        return self.get('compute_endpoint_name')

    @property
    def atom_hopper_url(self):
        return self.get('atom_hopper_url')

    @property
    def nova_atom_hopper_url_path(self):
        return self.get('nova_atom_hopper_url_path', '/nova/events')

    @property
    def atom_hopper_feed_limit(self):
        return self.get('atom_hopper_feed_limit')

    @property
    def atom_hopper_pagination_limit(self):
        return self.get('atom_hopper_pagination_limit')

    @property
    def mysql_conn_string(self):
        return self.get('mysql_conn_string')

    @property
    def identity_service_name(self):
        return self.get('identity_service_name')

    @property
    def image_status_timeout(self):
        return self.get('image_status_timeout')

    @property
    def env_name(self):
        return self.get('env_name')

    @property
    def instance_disk_path(self):
        return self.get('instance_disk_path')

    @property
    def gb_file_size(self):
        return float(self.get('gb_file_size'))

    @property
    def test_type(self):
        return self.get('test_type')

    @property
    def server_metadata_timeout(self):
        return int(self.get('server_metadata_timeout', 300))

    @property
    def managed_timeout(self):
        return self.get('managed_timeout')

    @property
    def min_polling_interval(self):
        return int(self.get('min_polling_interval'))

    @property
    def max_delete_wait(self):
        return int(self.get('max_delete_wait'))


class VolumeAttachmentsAPIConfig(_BaseConfig):
    SECTION_NAME = 'volume_attachments'

    @property
    def identity_service_name(self):
        return self.get('identity_service_name')

    @property
    def region(self):
        return self.get('region')


class VolumesAPIConfig(_BaseConfig):
    SECTION_NAME = 'volumes'

    @property
    def identity_service_name(self):
        return self.get('identity_service_name')

    @property
    def region(self):
        return self.get('region')

    @property
    def atom_feed_url(self):
        return self.get('atom_feed_url')

    @property
    def max_volume_size(self):
        return self.get("max_volume_size", default='1024')

    @property
    def min_volume_size(self):
        return self.get("min_volume_size", default='1')

    @property
    def default_wait_interval(self):
        return self.get("default_wait_interval", default='10')

    @property
    def default_max_waits(self):
        return self.get("default_wait_interval", default='30')


class IsolatedNetworksAPIConfig(_BaseConfig):
    SECTION_NAME = 'isolated_networks'

    @property
    def identity_service_name(self):
        return self.get('identity_service_name')

    @property
    def region(self):
        return self.get('region')

    @property
    def performance_image_ref(self):
        return self.get('performance_image_ref')

    @property
    def managed_username(self):
        return self.get('managed_username')

    @property
    def managed_api_key(self):
        return self.get('managed_api_key')

    @property
    def managed_password(self):
        return self.get('managed_password')

    @property
    def rackconnect_username(self):
        return self.get('rackconnect_username')

    @property
    def rackconnect_api_key(self):
        return self.get('rackconnect_api_key')

    @property
    def rackconnect_password(self):
        return self.get('rackconnect_password')

    @property
    def run_nvp(self):
        return self.get('run_nvp')

    @property
    def ifconfig_order_check(self):
        return self.get('ifconfig_order_check')

    @property
    def admin_username(self):
        return self.get('admin_username')

    @property
    def admin_api_key(self):
        return self.get('admin_api_key')

    @property
    def admin_password(self):
        return self.get('admin_password')

    @property
    def creator_username(self):
        return self.get('creator_username')

    @property
    def creator_api_key(self):
        return self.get('creator_api_key')

    @property
    def creator_password(self):
        return self.get('creator_password')

    @property
    def observer_username(self):
        return self.get('observer_username')

    @property
    def observer_api_key(self):
        return self.get('observer_api_key')

    @property
    def observer_password(self):
        return self.get('observer_password')


class ObjectStorageAPIConfig(_BaseConfig):
    SECTION_NAME = 'object_storage'

    @property
    def identity_service_name(self):
        return self.get('identity_service_name')

    @property
    def default_content_length(self):
        return self.get('default_content_length')

    @property
    def region(self):
        return self.get('region')

    @property
    def base_container_name(self):
        return self.get('base_container_name')

    @property
    def base_object_name(self):
        return self.get('base_object_name')

    @property
    def atom_feed_url(self):
        return self.get('atom_feed_url')

    @property
    def http_headers_per_request_count(self):
        return int(self.get('http_headers_per_request_count'))

    @property
    def http_headers_combined_max_len(self):
        return int(self.get('http_headers_combined_max_len'))

    @property
    def http_request_line_max_len(self):
        return int(self.get('http_request_line_max_len'))

    @property
    def http_request_max_content_len(self):
        return int(self.get('http_request_max_content_len'))

    @property
    def containers_name_max_len(self):
        return int(self.get('containers_name_max_len'))

    @property
    def containers_list_default_count(self):
        return int(self.get('containers_list_default_count'))

    @property
    def containers_list_default_max_count(self):
        return int(self.get('containers_list_default_max_count'))

    @property
    def containers_max_count(self):
        return int(self.get('containers_max_count'))

    @property
    def object_name_max_len(self):
        return int(self.get('object_name_max_len'))

    @property
    def object_max_size(self):
        return int(self.get('object_max_size'))

    @property
    def object_metadata_max_count(self):
        return int(self.get('object_metadata_max_count'))

    @property
    def object_metadata_combined_byte_len(self):
        return int(self.get('object_metadata_combined_byte_len'))

    @property
    def object_list_default_count(self):
        return int(self.get('object_list_default_count'))

    @property
    def object_list_default_max_count(self):
        return int(self.get('object_list_default_max_count'))

    @property
    def metadata_name_max_len(self):
        return int(self.get('metadata_name_max_len'))

    @property
    def metadata_value_max_len(self):
        return int(self.get('metadata_value_max_len'))

    @property
    def tempurl_key_cache_time(self):
        return int(self.get('tempurl_key_cache_time'))

    @property
    def formpost_key_cache_time(self):
        return int(self.get('formpost_key_cache_time'))

    @property
    def slo_min_segment_size(self):
        return int(self.get('slo_min_segment_size'))

    @property
    def slo_max_segment_count(self):
        return int(self.get('slo_max_segment_count'))


class CloudFilesCDNAPIConfig(_BaseConfig):
    SECTION_NAME = 'cloudfiles_cdn'

    @property
    def region(self):
        return self.get('region')

    @property
    def cdn_min_ttl(self):
        return int(self.get('cdn_min_ttl'))

    @property
    def cdn_max_ttl(self):
        return int(self.get('cdn_max_ttl'))

    @property
    def cdn_purge_max_count(self):
        return int(self.get('cdn_purge_max_count'))


class LoadBalancersAPIConfig(_BaseConfig):
    SECTION_NAME = 'lbaas'

    @property
    def identity_service_name(self):
        return self.get('identity_service_name')

    @property
    def region(self):
        return self.get('region')

    @property
    def mgmt_url(self):
        return self.get('mgmt_url')

    @property
    def mgmt_username(self):
        return self.get('mgmt_username')

    @property
    def mgmt_password(self):
        return self.get('mgmt_password')

    @property
    def live_node1(self):
        return self.get('live_node1')

    @property
    def live_node2(self):
        return self.get('live_node2')

    @property
    def live_node1_servicenet(self):
        return self.get('live_node1_servicenet')

    @property
    def live_node2_servicenet(self):
        return self.get('live_node2_servicenet')

    @property
    def live_node_password(self):
        return self.get('live_node_password')

    @property
    def atom_feed_url(self):
        return self.get('atom_feed_url')

    @property
    def atom_feed_user(self):
        return self.get('atom_feed_user')

    @property
    def atom_feed_password(self):
        return self.get('atom_feed_password')

    @property
    def public_url(self):
        return self.get('public_url')

    @property
    def zeus_username(self):
        return self.get('zeus_username')

    @property
    def zeus_password(self):
        return self.get('zeus_password')

    @property
    def zeus_soap_endpoint(self):
        return self.get('zeus_soap_endpoint')

    @property
    def zeus_replication_time(self):
        return int(self.get('zeus_replication_time', 1))

    @property
    def zeus_wsdl_location(self):
        return self.get('zeus_wsdl_location')

    @property
    def tenant_id(self):
        return self.get('tenant_id')

    @property
    def domain_node(self):
        return self.get('domain_node')

    @property
    def is_qa_env(self):
        return self.getboolean('is_qa_env', False)

    @property
    def default_vip_type(self):
        return self.get('default_vip_type', 'PUBLIC')

    @property
    def jenkins_url(self):
        return self.get('jenkins_url')

    @property
    def connection_log_job(self):
        return self.get('connection_log_job')

    @property
    def rbac_region(self):
        return self.get('rbac_region')

    @property
    def creator_role_user(self):
        return self.get('creator_role_user')

    @property
    def creator_role_password(self):
        return self.get('creator_role_password')

    @property
    def observer_role_user(self):
        return self.get('observer_role_user')

    @property
    def observer_role_password(self):
        return self.get('observer_role_password')

    @property
    def user_admin_role_user(self):
        return self.get('user_admin_role_user')

    @property
    def user_admin_role_password(self):
        return self.get('user_admin_role_password')


class LegacyServAPIConfig(_BaseConfig):
    SECTION_NAME = 'legacyserv'

    @property
    def identity_service_name(self):
        return self.get('identity_service_name')

    @property
    def region(self):
        return self.get('region')

    @property
    def url(self):
        return self.get('url')

    @property
    def rel(self):
        return self.get('name')


class DomainAPIConfig(_BaseConfig):
    SECTION_NAME = 'dnsaas'

    @property
    def identity_service_name(self):
        return self.get('identity_service_name')

    @property
    def region(self):
        return self.get('region')

    @property
    def url(self):
        return self.get('url')

    @property
    def rel(self):
        return self.get('rel')

    @property
    def href(self):
        return self.get('href')

    @property
    def name(self):
        return self.get('name')

    @property
    def type(self):
        return self.get('type')

    @property
    def data(self):
        return self.get('data')

    @property
    def ptr_timeout(self):
        return self.get('ptr_timeout')


class AdminAPIConfig(_BaseConfig):
    SECTION_NAME = 'admin'

    @property
    def admin_auth_url(self):
        return self.get('admin_auth_url')

    @property
    def admin_url(self):
        return self.get('admin_url')

    @property
    def admin_username(self):
        return self.get('admin_username')

    @property
    def admin_password(self):
        return self.get('admin_password')


class QuantumAPIConfig(_BaseConfig):
    SECTION_NAME = 'quantum'

    @property
    def endpoint(self):
        return self.get('endpoint')


class NVPAPIConfig(_BaseConfig):
    SECTION_NAME = 'nvp'

    @property
    def endpoint(self):
        return self.get('endpoint')

    @property
    def username(self):
        return self.get('username')

    @property
    def password(self):
        return self.get('password')

    @property
    def endpoint2(self):
        return self.get('endpoint2')


class CheckmateAPIConfig(_BaseConfig):
    SECTION_NAME = 'checkmate'

    @property
    def host(self):
        return self.get('host')

    @property
    def tenant_id(self):
        return self.get('tenant_id')


class ImagesAPIConfig(_BaseConfig):
    SECTION_NAME = 'images'

    @property
    def url(self):
        return self.get('url')

    @property
    def ext_url(self):
        return self.get('ext_url')

    @property
    def helper_url(self):
        return self.get('helper_url')

    @property
    def tenant_id(self):
        return self.get('tenant_id')

    @property
    def tenant(self):
        return self.get('tenant')

    @property
    def alt_tenant(self):
        return self.get('alt_tenant')

    @property
    def retention(self):
        return self.get('retention')

    @property
    def alt_retention(self):
        return self.get('alt_retention')

    @property
    def sch_img_metadata_key(self):
        return self.get('sch_img_metadata_key')

    @property
    def sch_img_metadata_value(self):
        return self.get('sch_img_metadata_value')

    @property
    def action(self):
        return self.get('action')

    @property
    def alt_action(self):
        return self.get('alt_action')

    @property
    def minute(self):
        return self.get('minute')

    @property
    def hour(self):
        return self.get('hour')

    @property
    def month(self):
        return self.get('month')

    @property
    def day_of_week(self):
        return self.get('day_of_week')

    @property
    def day_of_month(self):
        return self.get('day_of_month')

    @property
    def schedule_metadata(self):
        return self.get('schedule_metadata')

    @property
    def metadata_key(self):
        return self.get('metadata_key')

    @property
    def alt_metadata_key(self):
        return self.get('alt_metadata_key')

    @property
    def third_metadata_key(self):
        return self.get('third_metadata_key')

    @property
    def host(self):
        return self.get('host')

    @property
    def alt_host(self):
        return self.get('alt_host')

    @property
    def job_status(self):
        return self.get('job_status')

    @property
    def alt_job_status(self):
        return self.get('alt_job_status')

    @property
    def build_interval(self):
        return self.get('build_interval')

    @property
    def job_status_timeout(self):
        return self.get('job_status_timeout')

    @property
    def job_pickup_timeout(self):
        return self.get('job_pickup_timeout')

    @property
    def server_status_timeout(self):
        return self.get('server_status_timeout')

    @property
    def worker_stop_timeout(self):
        return self.get('worker_stop_timeout')

    @property
    def worker_start_timeout(self):
        return self.get('worker_start_timeout')

    @property
    def scheduler_nextrun_timeout(self):
        return self.get('scheduler_nextrun_timeout')

    @property
    def hard_timeout_offset(self):
        return self.get('hard_timeout_offset')

    @property
    def scheduled_images_alias(self):
        return self.get('scheduled_images_alias')

    @property
    def user_name(self):
        return self.get("user_name")

    @property
    def user_name_metadata_key(self):
        return self.get("user_name_metadata_key")

    @property
    def results_limit(self):
        return self.get("results_limit")


class IslAPIConfig(_BaseConfig):
    SECTION_NAME = 'isl'

    @property
    def base_request_url(self):
        return self.get('base_request_url')


class TQSearchConfig(_BaseConfig):
    SECTION_NAME = 'gate'

    @property
    def base_url(self):
        return self.get('base_url')

    @property
    def start_time(self):
        return self.get('start_time')

    @property
    def end_time(self):
        return self.get('end_time')

    @property
    def end_time_1(self):
        return self.get('end_time_1')

    @property
    def utc_end_time_1(self):
        return self.get('utc_end_time_1')

    @property
    def tq_search_account_number_1(self):
        return self.get('tq_search_account_number_1')

    @property
    def tq_search_account_number_2(self):
        return self.get('tq_search_account_number_2')

    @property
    def status_1(self):
        return self.get('status_1')

    @property
    def status_2(self):
        return self.get('status_2')

    @property
    def status_3(self):
        return self.get('status_3')

    @property
    def status_type(self):
        return self.get('status_type')

    @property
    def priority_1(self):
        return self.get('priority_1')

    @property
    def priority_3(self):
        return self.get('priority_3')

    @property
    def account_number_1(self):
        return self.get('account_number_1')

    @property
    def account_number_2(self):
        return self.get('account_number_2')

    @property
    def queue_name(self):
        return self.get('queue_name')

    @property
    def utc_date_constant(self):
        return self.get('utc_date_constant')

    @property
    def utc_start_time(self):
        return self.get('utc_start_time')

    @property
    def utc_start_time_2(self):
        return self.get('utc_start_time_2')

    @property
    def utc_end_time(self):
        return self.get('utc_end_time')

    @property
    def content_type(self):
        return self.get('content_type')

    @property
    def tq_search_priority_1(self):
        return self.get('tq_search_priority_1')

    @property
    def tq_search_priority_2(self):
        return self.get('tq_search_priority_2')

    @property
    def tq_search_account_number_1(self):
        return self.get('tq_search_account_number_1')

    @property
    def tq_search_account_number_2(self):
        return self.get('tq_search_account_number_2')

    @property
    def start_time_1(self):
        return self.get('start_time_1')

    @property
    def utc_start_time_1(self):
        return self.get('utc_start_time_1')

    @property
    def elastic_search_url(self):
        return self.get('elastic_search_url')

    @property
    def account_type_1(self):
        return self.get('account_type_1')

    @property
    def account_type_2(self):
        return self.get('account_type_2')

    @property
    def account_number_1(self):
        return self.get('account_number_1')

    @property
    def account_number_2(self):
        return self.get('account_number_2')

    @property
    def account_number_3(self):
        return self.get('account_number_3')

    @property
    def account_number_4(self):
        return self.get('account_number_4')

    @property
    def team_name(self):
        return self.get('team_name')

    @property
    def start_time_1(self):
        return self.get('start_time_1')

    @property
    def start_time_2(self):
        return self.get('start_time_2')

    @property
    def status_4(self):
        return self.get('status_4')

    @property
    def queue_name_1(self):
        return self.get('queue_name_1')

    @property
    def queue_name_1(self):
        return self.get('queue_name_1')

    @property
    def sync_queue_id(self):
        return self.get('sync_queue_id')

    @property
    def sync_sub_category(self):
        return self.get('sync_sub_category')

    @property
    def sync_account_id(self):
        return self.get('sync_account_id')

    @property
    def sync_ticket_text(self):
        return self.get('sync_ticket_text')

    @property
    def sync_ticket_list(self):
        return self.get('sync_ticket_list')

    @property
    def sync_ticket_subject(self):
        return self.get('sync_ticket_subject')

    @property
    def sync_ticket_subject2(self):
        return self.get('sync_ticket_subject2')

    @property
    def sync_source(self):
        return self.get('sync_source')

    @property
    def sync_severity(self):
        return self.get('sync_severity')

    @property
    def sync_account_id(self):
        return self.get('sync_account_id')

class LeftyConfig(_BaseConfig):
    SECTION_NAME = 'lefty'

    @property
    def base_url(self):
        return self.get('base_url')

    @property
    def account_id(self):
        return self.get('account_id')

    @property
    def pubsub_url_dfw(self):
        return self.get('pubsub_url_dfw')

    @property
    def pubsub_url_ord(self):
        return self.get('pubsub_url_ord')

    @property
    def data_centre(self):
        return self.get('data_centre')

class StackTachAPIConfig(_BaseConfig):
    SECTION_NAME = 'stacktach'

    @property
    def url(self):
        return self.get('url')

    @property
    def db_url(self):
        return self.get('db_url')

    @property
    def event_id(self):
        return self.get('event_id')

    @property
    def days_passed(self):
        return self.get('days_passed')


class AutoscaleAPIConfig(_BaseConfig):
    SECTION_NAME = 'autoscale'

    @property
    def tenant_id(self):
        return self.get('tenant_id')

    @property
    def region(self):
        return self.get('region')

    @property
    # group configuration name
    def gc_name(self):
        return self.get('gc_name')

    @property
    # group configuration cooldown time
    def gc_cooldown(self):
        return self.get('gc_cooldown')

    @property
    # group configuration minimum entities
    def gc_min_entities(self):
        return self.get('gc_min_entities')

    @property
    # group configuration maximum entities
    def gc_max_entities(self):
        return self.get('gc_max_entities')

    @property
    # group configuration alternate minimum entities
    def gc_min_entities_alt(self):
        return self.get('gc_min_entities_alt')

    @property
    # launch configuration server name
    def lc_name(self):
        return self.get('lc_name')

    @property
    # launch configuration server flavor
    def lc_flavor_ref(self):
        return self.get('lc_flavor_ref')

    @property
    # launch configuration server image id
    def lc_image_ref(self):
        return self.get('lc_image_ref')

    @property
    # scaling policy name
    def sp_name(self):
        return self.get('sp_name')

    @property
    # scaling policy cooldown time
    def sp_cooldown(self):
        return self.get('sp_cooldown')

    @property
    # scaling policy change in servers
    def sp_change(self):
        return self.get('sp_change')

    @property
    # scaling policy's update to change in servers
    def upd_sp_change(self):
        return self.get('upd_sp_change')

    @property
    # scaling policy percent change in servers
    def sp_change_percent(self):
        return self.get('sp_change_percent')

    @property
    # scaling policy's servers required to be in steady state
    def sp_steady_state(self):
        return self.get('sp_steady_state')

    @property
    # launch configuration for load balancers
    def lc_load_balancers(self):
        return self.get('lc_load_balancers')

    @property
    # list of scaling policies
    def sp_list(self):
        return self.get('sp_list')

    @property
    # Webhook name
    def wb_name(self):
        return self.get('wb_name')

    @property
    def identity_service_name(self):
        return self.get('identity_service_name')


class RaxSignupConfig(_BaseConfig):
    SECTION_NAME = 'rax_signup'

    @property
    def base_url(self):
        return self.get('base_url')


class LoggingAPIConfig(_BaseConfig):
    SECTION_NAME = 'loggingaas'

    @property
    def base_url(self):
        return self.get('base_url')

    @property
    def appver(self):
        return self.get('appver')

    @property
    def tenant_id(self):
        return self.get('tenant_id')

    @property
    def producer_name(self):
        return self.get('producer_name')

    @property
    def producer_pattern(self):
        return self.get('producer_pattern')

    @property
    def producer_durable(self):
        return self.getboolean('producer_durable')

    @property
    def producer_encrypted(self):
        return self.getboolean('producer_encrypted')

    @property
    def profile_name(self):
        return self.get('profile_name')

    @property
    def event_producer_ids(self):
        return json.loads(self.get('event_producer_ids'))

    @property
    def hostname(self):
        return self.get('hostname')

    @property
    def ip_address_v4(self):
        return self.get('ip_address_v4')

    @property
    def ip_address_v6(self):
        return self.get('ip_address_v6')

    @property
    def api_secret(self):
        return self.get('api_secret')

    @property
    def coordinator_base_url(self):
        return self.get('coordinator_base_url')

    @property
    def worker_base_url(self):
        return self.get('worker_base_url')

    @property
    def personality(self):
        return self.get('personality')

    @property
    def os_type(self):
        return self.get('os_type')

    @property
    def memory_mb(self):
        return self.get('memory_mb')

    @property
    def arch(self):
        return self.get('arch')

    @property
    def callback(self):
        return self.get('callback')

    @property
    def cpu_cores(self):
        return self.get('cpu_cores')

    @property
    def load_average(self):
        return self.get('load_average')

    @property
    def disk_path(self):
        return self.get('disk_path')

    @property
    def disk_total(self):
        return self.get('disk_total')

    @property
    def disk_used(self):
        return self.get('disk_used')


class BarbicanAPIConfig(_BaseConfig):
    SECTION_NAME = 'barbican'

    @property
    def base_url(self):
        return self.get('base_url')

    @property
    def appver(self):
        return self.get('appver')

    @property
    def build_version(self):
        return self.get('build_version')

    @property
    def appver_current(self):
        return self.get('appver_current')


class ManagedCloudConfig(_BaseConfig):
    SECTION_NAME = "managedcloud"

    @property
    def valkyrie_base_url(self):
        return self.get('valkyrie_base_url')

    @property
    def valkyrie_auth_token(self):
        return self.get('valkyrie_auth_token')

    @property
    def maas_url(self):
        return self.get('mass_url')

    @property
    def managed_cloud_timeout(self):
        return self.get('managed_cloud_timeout')


class CoreConfig(_BaseConfig):
    SECTION_NAME = 'core'

    @property
    def account_id(self):
        return self.get('account_id')

    @property
    def contact_id(self):
        return self.get('contact_id')

    @property
    def contract_id(self):
        return self.get('contract_id')


class CustomerAPIConfig(_BaseConfig):
    SECTION_NAME = 'customer'

    @property
    def base_url(self):
        return self.get('base_url')

    @property
    def auth_token(self):
        return self.get('auth_token')


class AtomHopperConfig(_BaseConfig):

    SECTION_NAME = 'atomhopper'

    @property
    def serializer(self):
        return self.get("serializer", default=None)

    @property
    def deserializer(self):
        return self.get("deserializer", default=None)


class AtomHopperEvents(_BaseConfig):
    SECTION_NAME = 'atom_hopper_events'

    @property
    def ah_endpoint(self):
        return self.get('ah_endpoint')


class UserIdentity(_BaseConfig):
    SECTION_NAME = 'user_identiy'

    @property
    def identity_endpoint(self):
        return self.get('identity_endpoint')


class RackConnectConfig(_BaseConfig):
    SECTION_NAME = 'rackconnect'

    @property
    def max_wait(self):
        return int(self.get('max_wait'))

    @property
    def min_polling_interval(self):
        return int(self.get('min_polling_interval'))

    @property
    def rackconnect_initials(self):
        return self.get('rackconnect_initials')
