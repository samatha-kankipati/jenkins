import time
import socket
import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import paramiko


class ComputeSSHConnector(object):
    """
    @summary: SSH connection Connector
    """
    def __init__(self, host, username, password, timeout=300):
        """
        @summary: Constructor method
        @param host: Server (IP or hostname) you are connecting to.
        @type host: string
        @param username: User Name to use for SSH connection
        @type username: string
        @param password: Password to use for SSH connection
        @type password: string
        @param timeout: Time to wait for,in seconds, before throwing AuthenticationTimeoutException
        @type timeout: int
        """
        self.host = host
        self.username = username
        self.password = password
        self.timeout = int(timeout)

    def _get_ssh_connection(self):
        """
        @summary: Returns an ssh connection to the specified host
        @return: ssh connection to the specified host
        @rtype: paramiko.SSHClient
        """
        _timeout = True
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(
            paramiko.AutoAddPolicy())
        _start_time = time.time()

        while not self._is_timed_out(self.timeout, _start_time):
            try:
                ssh.connect(self.host, username=self.username,
                    password=self.password, timeout=20)
                _timeout = False
                break
            except socket.error:
                continue
            except paramiko.AuthenticationException:
                time.sleep(15)
                continue
        if _timeout:
            # TODO(dwalleck): port over all compute exceptions
            raise 
        return ssh

    def _is_timed_out(self, timeout, start_time):
        """
        @summary: Check if the timeout period has elapsed after the start time
        @return: True if timeout period has elapsed, False otherwise.
        @rtype: bool
        """
        return (time.time() - timeout) > start_time

    def exec_command(self, cmd):
        """
        @summary: Execute the specified command on the server.
        @param cmd: Command to be executed
        @type cmd: string
        @return: Data read from standard output during execution of the command
        @rtype: string
        """
        
        ssh = self._get_ssh_connection()
        stdin, stdout, stderr = ssh.exec_command(cmd)
        stdin.flush()
        stdin.channel.shutdown_write()
        stdout.channel.settimeout(20)
        status = stdout.channel.recv_exit_status()
        try:
            output = stdout.read()
        except socket.timeout:
            if status == 0 and cmd.startswith(":(){") != True:
                # TODO(dwalleck): port over all compute exceptions
                raise
        if cmd.startswith(":(){") == True:
            output = ""    
        ssh.close()
        return output

    def upload_a_file(self, server_filepath, client_filepath):
        transport = paramiko.Transport(self.host)
        transport.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        try:
            sftp.put(client_filepath, server_filepath)
        except IOError:
            return False
        else:
            sftp.close()
            transport.close()
            return True

    def download_a_file(self, server_filepath, client_filepath):
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

    def test_connection_auth(self):
        """
        @summary: Test SSH connection to the server
        @return: True if SSH connection is successful, False otherwise
        @rtype: bool
        """
        try:
            connection = self._get_ssh_connection()
            connection.close()
        except paramiko.AuthenticationException:
            return False

        return True
