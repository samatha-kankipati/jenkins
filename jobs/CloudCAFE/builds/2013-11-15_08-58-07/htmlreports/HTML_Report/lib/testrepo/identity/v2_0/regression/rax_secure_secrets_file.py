from ConfigParser import SafeConfigParser
from urlparse import urlparse
import unittest

from ccengine.common.connectors.crypto import Crypto
from ccengine.common.decorators import attr
from ccengine.common.tools import logging_tools
from ccengine.clients.remote_instance.instance_client import LinuxClient
from ccengine.domain import configuration as _ConfigDomainObjects
from testrepo.common.testfixtures.identity.v2_0.identity \
    import BaseIdentityFixture


class SecureSecretsFile(BaseIdentityFixture):

    @classmethod
    def setUpClass(cls):
        super(SecureSecretsFile, cls).setUpClass()
        cls.encryption_password = cls.config.identity_api.encryption_password
        cls.endpoint = cls.config.identity_api.authentication_endpoint
        cls.algorithm = cls.config.identity_api.algorithm
        cls.secrets_file = 'idm.secrets.properties'
        cls.config_file_path = "/tmp/encrypt_value.config"
        cls.original_file_path = "/tmp/original_value.config"
        cls.crypto_class = Crypto()
        cls.fixture_log = logging_tools.getLogger('cc.master')

    def get_configuration_file(self, hostname, username, password):
        """
        @summary: ssh to the env and copies the secrets file to local machine
        """
        linux_client = LinuxClient(
            ip_address=hostname, server_id="", os_distro="", username=username,
            password=password)
        assert linux_client.can_authenticate()
        is_present = linux_client.is_file_present('/home/gauth/config/{0}'
                                                  .format(self.secrets_file))
        assert is_present
        output = linux_client.ssh_client.exec_command(
            'cat /home/gauth/config/{0}'.format(self.secrets_file))
        text_file = open(self.config_file_path, "w")
        text_file.write("[properties]\n")
        text_file.write(output)
        text_file.close()

        self.info = SafeConfigParser()
        self.info.read(self.config_file_path)
        self.configuration = _ConfigDomainObjects.SecretsConfig(self.info)
        return self.configuration

    @unittest.skip("Not a part of current release")
    @attr('regression', type='positive')
    def test_ssh(self):
        """
        @summary:These test cases valid only for Test env not for staging. Test
         to compare the decrypted value is the same as the original value
        """
        if self.algorithm == "":
            self.fixture_log.info("Algorithm not found in file")
            self.skipTest("Can be executed only in Test env")
        else:
            # Make sure to provide in sso credentials
            parsed_url = urlparse(self.endpoint)
            hostname = parsed_url.hostname
            password = "ssoPassword"
            self.get_configuration_file(hostname, "ssoUsername", password)

            self.original_info = SafeConfigParser()
            self.original_info.read(self.original_file_path)
            self.original_configuration = _ConfigDomainObjects.SecretsConfig(
                self.original_info)

            self._value(self.configuration.ldap_bind_password,
                        self.original_configuration.ldap_bind_password)
            self._value(self.configuration.crypto_password,
                        self.original_configuration.crypto_password)
            self._value(self.configuration.crypto_salt,
                        self.original_configuration.crypto_salt)
            self._value(self.configuration.ga_password,
                        self.original_configuration.ga_password)

    def _value(self, encrypt_string, original_string):
        """
        @summary: Test that takes in the encrypted value, decrypts and compares
        with the original value
        """
        decrypted_value = self.crypto_class.decrypt_string(
            encrypt_string, self.encryption_password,
            self.algorithm, "false")
        self.fixture_log.info(decrypted_value)
        original_value = original_string
        self.assertEqual(decrypted_value, original_value,
                         msg="Decrypted and original value are not the same")
