import time
import socket
import warnings
from ccengine.common.connectors.base_connector import BaseConnector

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from paramiko.resource import ResourceManager
    from paramiko.client import SSHClient
    import paramiko

DEFAULT_MAX_ATTEMPTS = 5


class SSHConnectorTimeoutException(Exception):
    pass


class SSHConnector(BaseConnector):

    def __init__(
            self, host, username, password, timeout=20, port=22):
        super(SSHConnector, self).__init__()
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.timeout = int(timeout)
        self._chan = None

    def _get_ssh_connection(self, max_attempts=DEFAULT_MAX_ATTEMPTS):
        """
        @summary: Returns an ssh connection to the specified host

        """
        ssh = SSHClient()
        ##ssh.set_missing_host_key_policy(paramiko.RejectPolicy())
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        saved_exception = SSHConnectorTimeoutException
        _attempts = 0

        self.connector_log.debug(
            "Attempting to create ssh connection to {0} as {1}".format(
                self.host, self.username))

        while _attempts <= (max_attempts):

            if _attempts > 0:
                self.connector_log.debug(
                    "Attempt {0} of {1} to create ssh connection to "
                    "{2} as {3} using password={4}".format(
                        _attempts, max_attempts, self.host, self.username,
                        self.password))
            _attempts += 1

            try:
                ssh.connect(
                    hostname=self.host, username=self.username,
                    password=self.password, timeout=self.timeout,
                    key_filename=[], look_for_keys=False, allow_agent=False)

                break

            except (socket.error, paramiko.AuthenticationException,
                    paramiko.SSHException) as expected_exception:
                self.connector_log.exception(expected_exception)
                saved_exception = expected_exception

            except Exception as exception:
                self.connector_log.exception(exception)
                raise exception
        else:
            self.connector_log.critical(
                "SSHConnector surpassed timeout while trying to establish a"
                " connection")
            raise saved_exception

        #This MUST be done because the transport gets garbage collected if it
        #is not done here, which causes the connection to close on invoke_shell
        #which is needed for exec_shell_command
        ResourceManager.register(self, ssh.get_transport())
        return ssh

    def connect_until_closed(self, max_attempts=DEFAULT_MAX_ATTEMPTS):
        """
        @summary: Connect to the server and wait until connection is lost

        """
        try:
            ssh = self._get_ssh_connection(max_attempts=max_attempts)
            _transport = ssh.get_transport()
            _start_time = time.time()
            _timed_out = self._is_timed_out(self.timeout, _start_time)
            while _transport.is_active() and not _timed_out:
                time.sleep(5)
                _timed_out = self._is_timed_out(self.timeout, _start_time)
            ssh.close()
        except (EOFError, paramiko.AuthenticationException, socket.error):
            return

    def exec_command(self, cmd):
        """
        @summary: Execute the specified command on the server.

        @return: Returns data read from standard output of the command

        """
        self.connector_log.debug('EXECing: %s' % str(cmd))
        ssh = self._get_ssh_connection()
        stdin, stdout, stderr = ssh.exec_command(cmd)

        stdout_data = stdout.read()
        try:
            stderr_data = stderr.read()
            self.connector_log.debug('EXEC-STDOUT: %s' % str(stdout_data))
            self.connector_log.debug('EXEC-STDERR: %s' % str(stderr_data))
        except Exception as ex:
            self.connector_log.exception(ex)
            pass

        ssh.close()

        return stdout_data

    def test_connection_auth(self, max_attempts=DEFAULT_MAX_ATTEMPTS):
        """
        @summary: Returns true if ssh can connect to server

        """
        try:
            connection = self._get_ssh_connection(max_attempts=max_attempts)
            connection.close()
        except paramiko.AuthenticationException:
            return False

        return True

    def start_shell(self, max_attempts=DEFAULT_MAX_ATTEMPTS):
        """
        @summary: Starts a shell instance of SSH to use with multiple commands.

        """
        #large width and height because of need to parse output of commands
        #in exec_shell_command
        self._chan = self._get_ssh_connection().invoke_shell(width=9999999,
                                                             height=9999999)
        #wait until buffer has data
        while not self._chan.recv_ready():
            time.sleep(1)
        #clearing initial buffer, usually login information
        while self._chan.recv_ready():
            self._chan.recv(1024)

    def exec_shell_command(self, cmd, stop_after_send=False):
        """
        @summary: Executes a command in shell mode and receives all of the
            response.  Parses the response and returns the output of the
            command and the prompt.
        @return: Returns the output of the command and the prompt.
        """
        if not cmd.endswith('\n'):
            cmd = '%s\n' % cmd
        self.connector_log.debug('EXEC-SHELLing: %s' % cmd)
        if self._chan is None or self._chan.closed:
            self.start_shell()
        while not self._chan.send_ready():
            time.sleep(1)
        self._chan.send(cmd)
        if stop_after_send:
            self._chan.get_transport().set_keepalive(1000)
            return None
        while not self._chan.recv_ready():
            time.sleep(1)
        output = ''
        while self._chan.recv_ready():
            output += self._chan.recv(1024)
        self.connector_log.debug('SHELL-COMMAND-RETURN: \n%s' % output)
        prompt = output[output.rfind('\r\n') + 2:]
        output = output[output.find('\r\n') + 2:output.rfind('\r\n')]
        self._chan.get_transport().set_keepalive(1000)
        return output, prompt

    def exec_shell_command_wait_for_prompt(self, cmd, prompt='#', timeout=300):
        """
        @summary: Executes a command in shell mode and receives all of
            the response.  Parses the response and returns the output
            of the command and the prompt.
        @return: Returns the output of the command and the prompt.

        """
        if not cmd.endswith('\n'):
            cmd = '%s\n' % cmd
        self.connector_log.debug('EXEC-SHELLing: %s' % cmd)
        if self._chan is None or self._chan.closed:
            self.start_shell()
        while not self._chan.send_ready():
            time.sleep(1)
        self._chan.send(cmd)
        while not self._chan.recv_ready():
            time.sleep(1)
        output = ''
        max_time = time.time() + timeout
        while time.time() < max_time:
            current = self._chan.recv(1024)
            output += current
            if current.find(prompt) != -1:
                self.connector_log.debug('SHELL-PROMPT-FOUND: %s' % prompt)
                break
            self.connector_log.debug('Current response: %s' % current)
            self.connector_log.debug('Looking for prompt: %s. ' \
                                     'Time remaining until timeout: %s'
                                     % (prompt, max_time - time.time()))
            while not self._chan.recv_ready() and time.time() < max_time:
                time.sleep(5)
            self._chan.get_transport().set_keepalive(1000)
        self.connector_log.debug('SHELL-COMMAND-RETURN: %s' % output)
        prompt = output[output.rfind('\r\n') + 2:]
        output = output[output.find('\r\n') + 2:output.rfind('\r\n')]
        return output, prompt

    def make_directory(self, directory_name):
        """
        @summary: Makes directory on instance.
        @param directory_name: Fully qualified path of directory.
        @type directory_name: String
        @return: True if directory creation successful, otherwise False.
        @rtype: Boolean

        """
        self.connector_log.info('Making a Directory')
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        try:
            sftp.mkdir(directory_name)
        except IOError, exception:
            self.connector_log.warning("Exception in making a directory: {0}"
                                       .format(exception))
            return False
        else:
            sftp.close()
            transport.close()
            return True

    def browse_folder(self):
        """
        @summary: Lists current directory contents.
        @return: True if list directory successful, otherwise False.
        @rtype: Boolean

        """
        self.connector_log.info('Browsing a folder')
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        try:
            sftp.listdir()
        except IOError, exception:
            self.connector_log.warning("Exception in browsing folder file: {0}"
                                       .format(exception))
            return False
        else:
            sftp.close()
            transport.close()
            return True

    def upload_a_file(self, server_file_path, client_file_path):
        """
        @summary: Uploads a local file to server.
        @param server_file_path: Fully qualified path of directory
            including filename on server.
        @type server_file_path: String
        @param client_file_path: Fully qualified path of directory.
            including filename on localhost.
        @type client_file_path: String
        @return: True if file upload successful, otherwise False.
        @rtype: Boolean

        """
        self.connector_log.info("uploading file from {0} to {1}"
                                .format(client_file_path, server_file_path))
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        try:
            sftp.put(client_file_path, server_file_path)
        except IOError, exception:
            self.connector_log.warning("Exception in uploading file: {0}"
                                       .format(exception))
            return False
        else:
            sftp.close()
            transport.close()
            return True

    def download_a_file(self, server_filepath, client_filepath):
        """
        @summary: Downloads a file from a server to local system
        @param server_file_path: Fully qualified path of directory
            including filename on server.
        @type server_file_path: String
        @param client_file_path: Fully qualified path of directory.
            including filename on localhost.
        @type client_file_path: String
        @return: True if file download successful, otherwise False.
        @rtype: Boolean

        """
        transport = paramiko.Transport(self.host)
        transport.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        try:
            sftp.get(server_filepath, client_filepath)
        except IOError:
                return False
        else:
            sftp.close()
            transport.close()
            return True

    def end_shell(self):
        if not self._chan.closed:
            self._chan.close()
        self._chan = None
