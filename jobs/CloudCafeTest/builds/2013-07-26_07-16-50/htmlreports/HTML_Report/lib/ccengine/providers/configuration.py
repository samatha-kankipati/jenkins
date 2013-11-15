import os
from ConfigParser import SafeConfigParser

from ccengine.common.tools import logging_tools
from ccengine.domain import configuration as _ConfigDomainObjects
from ccengine.common.exceptions.configuration \
    import UnreadableConfigFileException, ConfigDirectoryNotDefinedException


class _BaseConfigProvider(object):
    '''Returns a ConfigDataObject'''
    def __init__(self, SafeConfigParserObject=None):
        '''
            Reads in config file from OS_ENV variable and creates config
            object for providers to consume.
        '''
        self._log = logging_tools.getLogger(logging_tools
            .get_object_namespace(self.__class__))

        if SafeConfigParserObject is not None:
            self.info = SafeConfigParserObject
        else:
            #Retrieve the config file path from the os environment
            config_file_path = None
            try:
                config_file_path = os.environ[
                    _ConfigDomainObjects.TEST_CONFIG_FILE_OSENV]
            except KeyError:
                self._log.critical(
                    '{0} OS environment variable was not set.'
                    .format(_ConfigDomainObjects.TEST_CONFIG_FILE_OSENV))
                raise ConfigDirectoryNotDefinedException(
                    '{0} OS environment variable was not set.'
                    .format(_ConfigDomainObjects.TEST_CONFIG_FILE_OSENV))
            except:
                self._log.critical(
                    'Unable to read OS ENVironment vars for configuration.')
                raise ConfigDirectoryNotDefinedException(
                    'Unable to read OS ENVironment vars for configuration.')

            #Check the path
            if not os.path.exists(config_file_path):
                self._log.critical('Could not verify the existence of config '
                                   'file at {0}.'.format(config_file_path))
                raise ConfigDirectoryNotDefinedException(
                    'Could not verify the existence of config file at {0}.'
                    .format(config_file_path))

            #Make sure the config file is readable
            try:
                self.info = SafeConfigParser()
                self.info.read(config_file_path)
            except:
                self._log.critical('Unable to read config file:\n"{0}"'
                    .format(str(config_file_path)))
                raise UnreadableConfigFileException(
                    'Unable to read config file:\n"{0}"'
                    .format(str(config_file_path)))


class MasterConfigProvider(_BaseConfigProvider):
    '''
        @README
        You should put a linein the MasterConfigProvider (yup, the MCP ;)
        and use that to set up your providers / fixtures / etc.
    '''

    def __init__(self, SafeConfigParserObject=None):
        super(MasterConfigProvider, self).__init__(SafeConfigParserObject)
        self.misc = _ConfigDomainObjects.MiscConfig(self.info)
        self.logging = _ConfigDomainObjects.LoggingConfig(self.info)
        self.auth = _ConfigDomainObjects.AuthConfig(self.info)
        self.identity_api = _ConfigDomainObjects.IdentityAPIConfig(self.info)
        self.ldap = _ConfigDomainObjects.LdapConfig(self.info)
        self.moneyball = _ConfigDomainObjects.MoneyballAPIConfig(self.info)
        self.compute_api = _ConfigDomainObjects.ComputeAPIConfig(self.info)
        self.volumes_api = _ConfigDomainObjects.VolumesAPIConfig(self.info)
        self.volume_attachments_api\
            = _ConfigDomainObjects.VolumeAttachmentsAPIConfig(self.info)
        self.nova_shell = _ConfigDomainObjects.NovaShellConfig(self.info)
        self.cinder_shell = _ConfigDomainObjects.CinderShellConfig(self.info)
        self.images = _ConfigDomainObjects.ImagesAPIConfig(self.info)
        self.isolated_networks_api\
            = _ConfigDomainObjects.IsolatedNetworksAPIConfig(self.info)
        self.lunr_api = _ConfigDomainObjects.LunrAPIConfig(self.info)
        self.storage_node_api = _ConfigDomainObjects\
            .StorageNodeAPIConfig(self.info)
        self.object_storage_api = _ConfigDomainObjects\
            .ObjectStorageAPIConfig(self.info)
        self.cloudfiles_cdn_api = _ConfigDomainObjects\
            .CloudFilesCDNAPIConfig(self.info)
        self.lava_api = _ConfigDomainObjects.LavaAPIConfig(self.info)
        self.lbaas_api = _ConfigDomainObjects.LoadBalancersAPIConfig(self.info)
        self.dnsaas = _ConfigDomainObjects.DomainAPIConfig(self.info)
        self.rackconnect = _ConfigDomainObjects.Rackconnect(self.info)
        self.legacyserv = _ConfigDomainObjects.LegacyServAPIConfig(self.info)
        self.nvp_api = _ConfigDomainObjects.NVPAPIConfig(self.info)
        self.quantum_api = _ConfigDomainObjects.QuantumAPIConfig(self.info)
        self.checkmate = _ConfigDomainObjects.CheckmateAPIConfig(self.info)
        self.isl = _ConfigDomainObjects.IslAPIConfig(self.info)
        self.lefty = _ConfigDomainObjects.LeftyConfig(self.info)
        self.tq_search = _ConfigDomainObjects.TQSearchConfig(self.info)
        self.stacktach = _ConfigDomainObjects.StackTachAPIConfig(self.info)
        self.rax_signup = _ConfigDomainObjects.RaxSignupConfig(self.info)
        self.autoscale = _ConfigDomainObjects.AutoscaleAPIConfig(self.info)
        self.loggingaas = _ConfigDomainObjects.LoggingAPIConfig(self.info)
        self.barbican = _ConfigDomainObjects.BarbicanAPIConfig(self.info)
        self.admin_api = _ConfigDomainObjects.AdminAPIConfig(self.info)
        self.managedcloud = _ConfigDomainObjects.ManagedCloudConfig(self.info)
        self.core = _ConfigDomainObjects.CoreConfig(self.info)
        self.customer = _ConfigDomainObjects.CustomerAPIConfig(self.info)
        self.atomhopper = _ConfigDomainObjects.AtomHopperConfig(self.info)
        self.atom_hopper_events = _ConfigDomainObjects.AtomHopperEvents(
            self.info)
        self.user_identity = _ConfigDomainObjects.UserIdentity(self.info)
        self.rackconnect = _ConfigDomainObjects.Rackconnect(self.info)

    def mcp_override(self, new_values):
        '''
            Returns a MCP based on a new config with the original config values
            but the values in the sections defined in new_values overwrite what
            is in the original config.

            @TODO: Implement an easy dict-to-config-provider that generates
                   new configs so that data-driven tests can instantiate config
                   providers at will, and thus instantiate providers and
                   clients dynamically as well. - jose
        '''
        new_config = SafeConfigParser()
        for section in self.info._sections:
            new_config.add_section(section)
            for key, value in self.info._sections[section].items():
                if not key.startswith('__'):
                    new_config.set(section, key, value)
        for section in new_values:
            for key in new_values[section]:
                new_config.set(section, key, new_values[section][key])
        return MasterConfigProvider(new_config)

    def __repr__(self):
        s = ''
        s = s + str(self.misc) + '\n'
        s = s + str(self.auth) + '\n'
        s = s + str(self.compute_api) + '\n'
        s = s + str(self.nova_shell) + '\n'
        s = s + str(self.isolated_networks_api) + '\n'
        s = s + str(self.lunr_api) + '\n'
        s = s + str(self.storage_node_api) + '\n'
        s = s + str(self.object_storage_api) + '\n'
        s = s + str(self.cloudfiles_cdn_api) + '\n'
        s = s + str(self.lava_api) + '\n'
        return s
