import os.path
import subprocess

from ccengine.common.connectors.base_connector import BaseConnector
from ccengine.common.tools import logging_tools


class Crypto(BaseConnector):
    """
    @summary: Class to provide encryption and decryption functionality
    @note: Intended to encrypt and decrypt string
    """
    def __init__(self, base_command=None):
        """
        @param base_command: This processes base command string
        @type base_command: C{str}
        """
        super(Crypto, self).__init__()
        self.base_command = base_command
        self.decryption_class = ('org.jasypt.intf.cli'
                                 '.JasyptPBEStringDecryptionCLI')
        self.encryption_class = ('org.jasypt.intf.cli'
                                 '.JasyptPBEStringEncryptionCLI')
        lib_dir = '/Users/shan0433/Downloads/jasypt-1.9.0/lib'
        self.fixture_log = logging_tools.getLogger('cc.master')
        self.exec_classpath = "."
        jasypt_classpath = os.environ.get('JASYPT_HOME')
        java_home = os.environ.get('JAVA_HOME')

        if jasypt_classpath is not None:
            self.exec_classpath = "{0}:{1}".format(
                self.exec_classpath, jasypt_classpath)

        for root, _, files in os.walk(lib_dir):
            for in_file in files:
                fullpath = os.path.join(root, in_file)
                self.exec_classpath = "{0}:{1}".format(
                    self.exec_classpath, fullpath)

        self.java_executable = 'java'
        if java_home is not None:
            self.java_executable = "{0}/bin/java".format(java_home)

    def execute(self, crypto_class, script_name, input_string, password,
                algorithm, verbose):
        """
        Concatenate the command and execute on the command line
        """
        cmd = ('{executable} -classpath {classpath} {encryption_class}'
               ' {script} input="{input}" password={password}'
               ' algorithm={algorithm} verbose={verbosity}')
        cmd = cmd.format(executable=self.java_executable,
                         classpath=self.exec_classpath,
                         encryption_class=crypto_class,
                         script=script_name,
                         input=input_string,
                         password=password,
                         algorithm=algorithm,
                         verbosity=verbose)
        value = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=None,
                                 shell=True)
        out, err = value.communicate()
        if err is not None:
            self.fixture_log.error('Error in encrypting/decrypting the string')
            self.fixture_log.error(err)
        return out.replace('\n', '')

    def encrypt_string(self, input_string, password,
                       algorithm=None, verbose="false"):
        """
        Encrypts the string using specified algorithm
        """
        script_name = 'encrypt.py'
        output = self.execute(crypto_class=self.encryption_class,
                              script_name=script_name,
                              input_string=input_string,
                              password=password,
                              algorithm=algorithm,
                              verbose=verbose)
        self.fixture_log.info('Encrypted value: {0}'.format(output))

    def extract_value(self, encapsuled_string):
        """
        Extract the value from properties file encapsuled in ENC
        """
        start = encapsuled_string.index("ENC(") + len("ENC(")
        end = encapsuled_string.index(")", start)
        return encapsuled_string[start:end]

    def decrypt_string(self, input_string, password,
                       algorithm=None, verbose="false"):
        """
        Decrypts the string using specified algorithm
        """
        script_name = 'decrypt.py'
        extracted_string = self.extract_value(input_string)
        output = self.execute(crypto_class=self.decryption_class,
                              script_name=script_name,
                              input_string=extracted_string,
                              password=password,
                              algorithm=algorithm,
                              verbose=verbose)
        self.fixture_log.info('Decrypted value: {0}'.format(output))
        return output
