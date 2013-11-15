import time
import re
import os
import socket
import hashlib

from ccengine.common.connectors.ssh import SSHConnector
from ccengine.common.connectors.ping import PingClient
from ccengine.domain.compute.file_details import FileDetails
from ccengine.domain.compute.partition import DiskSize, Partition
from ccengine.domain.compute.response.xenstore_meta import Xenmeta
from ccengine.clients.remote_instance.linux.base_client import \
    BasePersistentLinuxClient
from ccengine.common.exceptions.compute import FileNotFoundException, \
    ServerUnreachable, SshConnectionException
from ccengine.common.tools import logging_tools, datatools


class LinuxClient(BasePersistentLinuxClient):

    def __init__(self, ip_address, server_id, os_distro,
                 username, password, ssh_timeout=300):
        self.client_log = (logging_tools
                           .getLogger(logging_tools
                                      .get_object_namespace(self.__class__)))

        self.ssh_timeout = ssh_timeout
        if ip_address is None:
            # TODO (dwalleck): Finishing porting over zodiac exceptions
            raise ServerUnreachable("None")
        self.ip_address = ip_address
        self.username = username
        if self.username is None:
            self.username = 'root'
        self.password = password
        self.server_id = server_id

        self.ssh_client = SSHConnector(self.ip_address,
                                       self.username,
                                       self.password,
                                       timeout=self.ssh_timeout)
        if not self.ssh_client.test_connection_auth():
            self.client_log.error("Ssh connection failed for: IP:{0} \
                    Username:{1} Password: {2}".format(self.ip_address,
                                                       self.username,
                                                       self.password))
            raise SshConnectionException("ssh connection failed")

    def can_connect_to_public_ip(self):
        """
        @summary: Checks if you can connect to server using public ip
        @return: True if you can connect, False otherwise
        @rtype: bool
        """
        # This returns true since the connection has already been tested in the
        # init method

        return self.ssh_client is not None

    def can_ping_public_ip(self, public_addresses, ip_address_version_for_ssh):
        """
        @summary: Checks if you can ping a public ip
        @param addresses: List of public addresses (AddrObj type)
        @type addresses: Address List
        @return: True if you can ping, False otherwise
        @rtype: bool
        """
        for public_address in public_addresses:
            if (public_address.version == 4 and not
                (PingClient.ping(public_address.addr,
                    ip_address_version_for_ssh) != 100)):
                return False
        return True

    def can_authenticate(self):
        """
        @summary: Checks if you can authenticate to the server
        @return: True if you can connect, False otherwise
        @rtype: bool
        """
        return self.ssh_client.test_connection_auth()

    def reboot(self, timeout=100):
        '''
        @timeout: max timeout for the machine to reboot
        '''
        ssh_connector = SSHConnector(self.ip_address, self.username,
                                     self.password)
        response, prompt = ssh_connector.exec_shell_command("sudo reboot")
        if prompt.find("Password") != -1:
            response, prompt = ssh_connector.exec_shell_command(self.password)
        self.client_log.info("Reboot response for %s: %s" % (self.ip_address,
                                                             response))
        max_time = time.time() + timeout
        while time.time() < max_time:
            time.sleep(5)
            if self.ssh_client.test_connection_auth():
                self.client_log.info("Reboot succesfull for %s"
                                     % (self.ip_address))
                return True

    def get_hostname(self):
        """
        @summary: Gets the host name of the server
        @return: The host name of the server
        @rtype: string
        """
        return self.ssh_client.exec_command("hostname").rstrip()

    def get_ifconfig(self):
        """
        @summary: Gets the ifconfig data of the server
        @return: The ifconfig info of the server
        @rtype: string
        """
        return self.ssh_client.exec_command("ifconfig").rstrip()

    def get_xenstore_meta(self):
        """
        @summary: Gets the host name of the server
        @return: The host name of the server
        @rtype: string
        """
        command = 'xenstore-ls vm-data'
        output = self.ssh_client.exec_command(command)
        return Xenmeta._str_to_dict(output)

    def can_remote_ping_private_ip(self, private_addresses):
        """
        @summary: Checks if you can ping a private ip from this server.
        @param private_addresses: List of private addresses (AddrObj type)
        @type private_addresses: Address List
        @return: True if you can ping, False otherwise
        @rtype: bool
        """
        for private_address in private_addresses:
            if (private_address.version == 4 and not
                (PingClient.ping_using_remote_machine(self.ssh_client,
                    private_address.addr) != 100)):
                return False
        return True

    def can_remote_ping_ips(self, ip_list, count=3):
        """
        @summary: Checks if you can ping an ip from this server.
        @param ip_list: List of IPv4 addresses (str type)
        @type: List
        @param count: Packets to transmit
        @type: int
        @return: packet loss percentages for each ip
        @rtype: list
        """
        if not isinstance(ip_list, list):
            ip_list = [ip_list]
        res = []
        for ip in ip_list:
            res.append(PingClient.ping_using_remote_machine(self.ssh_client,
                                                            ip, count))
        return res

    def get_files(self, path):
        """
        @summary: Gets the list of filenames from the path
        @param path: Path from where to get the filenames
        @type path: string
        @return: List of filenames
        @rtype: List of strings
        """
        command = "ls -m " + path
        return self.ssh_client.exec_command(command).rstrip('\n').split(', ')

    def get_ram_size_in_mb(self):
        """
        @summary: Returns the RAM size in MB
        @return: The RAM size in MB
        @rtype: string
        """
        output = self.ssh_client.exec_command('free -m | grep Mem')
        # TODO (dwalleck): We should handle the failure case here
        if output:
            return output.split()[1]

    def get_swap_size_in_mb(self):
        """
        @summary: Returns the Swap size in MB
        @return: The Swap size in MB
        @rtype: int
        """
        output = (self.ssh_client
                  .exec_command(
                  'fdisk -l /dev/xvdc1 2>/dev/null | grep "Disk.*bytes"')
                  .rstrip('\n'))
        if output:
            return int(output.split()[2])

    def get_disk_size_in_gb(self, disk_path):
        """
        @summary: Returns the disk size in GB
        @return: The disk size in GB
        @rtype: int
        """
        command = "df -k | grep '{0}'".format(disk_path)
        output = self.ssh_client.exec_command(command)
        size = float(output.split()[1])/(1024*1024)
        return size

    def get_number_of_vcpus(self):
        """
        @summary: Get the number of vcpus assigned to the server
        @return: The number of vcpus assigned to the server
        @rtype: int
        """
        command = 'cat /proc/cpuinfo | grep processor | wc -l'
        output = self.ssh_client.exec_command(command)
        return int(output)

    def get_partitions(self):
        """
        @summary: Returns the contents of /proc/partitions
        @return: The partitions attached to the instance
        @rtype: string
        """
        command = 'cat /proc/partitions'
        output = self.ssh_client.exec_command(command)
        return output

    def get_uptime(self):
        """
        @summary: Get the uptime time of the server
        @return: The uptime of the server
        """
        result = self.ssh_client.exec_command('cat /proc/uptime')
        uptime = float(result.split(' ')[0])
        return uptime

    def create_file(self, file_name, file_content, file_path=None):
        '''
        @summary: Create a new file
        @param file_name: File Name
        @type file_name: String
        @param file_content: File Content
        @type file_content: String
        @return filedetails: File details such as content, name and path
        @rtype filedetails; FileDetails
        '''
        if file_path is None:
            file_path = "/root/" + file_name
        cmd = "echo -n {0} >> {1}".format(file_content, file_path)
        self.ssh_client.exec_command(cmd)
        return FileDetails("644", file_content, file_path)

    def create_a_file_on_server(self, filepath, multiplier):
        """
        @summary: Creates a Gigabyte file on the server
        @param filepath: The filepath including filename
        @type filepath: String
        @param multiplier: A decimal number indicating the number of Gigabytes
            for example: 0.1 multiplier will create a 1.07374e8 byte file
        @type multiplier: Float
        @return: Data read from standard output during execution of the command
        @rtype: String
        """
        seek = int(1024 * 1024 * multiplier)
        cmd = ('dd if=/dev/zero of={0} count=0 bs=1024 seek={1} && '
               'echo "File created" || echo "File not created"'
               .format(filepath, str(seek)))
        output = self.ssh_client.exec_command(cmd)
        return output.rstrip('\n') == 'File created'

    def create_a_file_on_client(self, filepath, multiplier):
        """
        @summary: Creates a Gigabyte file on the client
        @param filepath: The filepath including filename
        @type filepath: String
        @param multiplier: A decimal number indicating the number of Gigabytes
            for example: 0.1 Gigabytes will create a 1.07374e8 byte file
        @type multiplier: Float
        @return: Data read from standard output during execution of the command
        @rtype: String
        """
        seek = int(1024 * 1024 * multiplier)
        cmd = ('dd if=/dev/zero of={0} count=0 bs=1024 seek={1} && '
               'echo "File created" || echo "File not created"'
               .format(filepath, str(seek)))
        output = os.system(cmd)
        # @todo: use subprocess to get real output
        return output is not None

    def get_file_details(self, filepath):
        """
        @summary: Get the file details
        @param filepath: Path to the file including file name
        @type filepath: string
        @return: File details including permissions and content
        @rtype: FileDetails
        """

        cmd = '[ -f {0} ] && echo "File exists" || ' \
              'echo "File does not exist"'.format(filepath)
        output = self.ssh_client.exec_command(cmd)
        if not output.rstrip('\n') == 'File exists':
            raise FileNotFoundException(
                "File: {0} not found on instance.".format(filepath))

        cmd = 'stat -c %a {0}'.format(filepath)
        file_permissions = self.ssh_client.exec_command(cmd).rstrip("\n")
        cmd = 'cat '.format(filepath)
        file_contents = self.ssh_client.exec_command(cmd)
        return FileDetails(file_permissions, file_contents, filepath)

    def upload_a_file(self, server_filepath, client_filepath):
        """
        @summary: Upload a file from local machine to the server.
        @param server_filepath: The path name including file name on server.
        @type server_filepath: String
        @param client_filepath: The path name including file name on client.
        @type client_filepath: String
        @return: True on successful file upload, False otherwise
        @rtype: Boolean
        """
        return self.ssh_client.upload_a_file(server_filepath, client_filepath)

    def download_a_file(self, server_filepath, client_filepath):
        """
        @summary: Download a file to local machine from the server
        @param server_filepath: The path name including file name on server.
        @type server_filepath: String
        @param client_filepath: The path name including file name on client.
        @type client_filepath: String
        @return: True on successful file download, False otherwise
        @rtype: Boolean
        """
        return self.ssh_client.download_a_file(server_filepath,
                                               client_filepath)

    def transfer_a_file(self, filepath, ip_address):
        """
        @summary: Transfer a file to another server
            identified by the ip address
        @param filepath: The path name including file name
        @type filepath: String
        @param ip_address: The IP address of the receiving server
        @type ip_address: string
        @return: The output from the scp command
        @rtype: String
        """
        if self._is_valid_ipv6_address(ip_address):
            # Jenkins is a Debian box so the ip address is formatted as:
            #  \[fe80::220:e0ff:fe8f:ea44%eth1\]:
            cmd = ('scp -o StrictHostKeyChecking=no {0} root@\[{1}\]:/root/ '
                   '&& echo "File transferred" || echo "File not transferred'
                   .format(filepath, ip_address))
            output = self.ssh_client.exec_command(cmd)
            return output.rstrip('\n') == 'File transferred'
        elif self._is_valid_ipv4_address(ip_address):
            cmd = ("scp -o StrictHostKeyChecking=no " +
                   filepath + " root@" + ip_address + ":/root/")
            cmd = ('scp -o StrictHostKeyChecking=no {0} root@{1}:/root/ '
                   '&& echo "File transferred" || echo "File not transferred"'
                   .format(filepath, ip_address))
            output = self.ssh_client.exec_command(cmd)
            return output.rstrip('\n') == 'File transferred'
        else:
            return False

    def get_md5sum(self, filepath):
        """
        @summary: Gets the md5sum of file on the server
        @param filepath: The path name including file name
        @type filepath: String
        """
        output = self.ssh_client.exec_command('md5sum ' + filepath)
        if output:
            return output.split()[0]

    def get_md5sum_on_client(self, filepath):
        """
        @summary: Gets the md5sum of file on the server
        @param filepath: The path name including file name
        @type filepath: String
        """
        fh = open(filepath, 'rb')
        file_md5 = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            file_md5.update(data)
        return file_md5.hexdigest()

    def set_file_permissions(self, filepath, mode):
        """
        @summary: Set the permissions on a file
        @param filepath: Path to the file including filename
        @type filepath: String
        @param mode: Permissions to be set on file
            (represented as three digit decimal number)
        @type mode: String
        """
        cmd = 'chmod {0} {1}'.format(mode, filepath)
        output = self.ssh_client.exec_command(cmd)
        return output

    def get_network_bytes_from_server(self, interface):
        '''
        @summary: Retrieves the byte counters from a given network interface.
        @param interface: The network interface of an instance.
        @type interface: String
        @return: The received bytes and transmitted bytes
            from the network inteface, respectively
        @rtype: Tuple
        '''
        cmd = "ifconfig {0}".format(interface)
        output = self.ssh_client.exec_command(cmd)
        rx_bytes = re.findall('RX bytes:([0-9]*) ', output)[0]
        tx_bytes = re.findall('TX bytes:([0-9]*) ', output)[0]
        return (rx_bytes, tx_bytes)

    def is_file_present(self, filepath):
        """
        @summary: Check if the given file is present
        @param filepath: Path to the file
        @type filepath: string
        @return: True if File exists, False otherwise
        """
        cmd = ('[ -f {0} ] && echo "File exists" || echo "File does not exist"'
               .format(filepath))
        output = self.ssh_client.exec_command(cmd)
        return output.rstrip('\n') == 'File exists'

    def get_partition_types(self):
        """
        @summary: Return the partition types for all partitions
        @return: The partition types for all partitions
        @rtype: Dictionary
        """
        partitions_list = self.ssh_client.exec_command(
            'blkid').rstrip('\n').split('\n')
        partition_types = {}
        for row in partitions_list:
            partition_name = row.split()[0].rstrip(':')
            partition_types[partition_name] = re.findall(
                r'TYPE="([^"]+)"', row)[0]
        return partition_types

    def get_partition_details(self):
        """
        @summary: Return the partition details
        @return: The partition details
        @rtype: Partition List
        """
        # Return a list of partition objects that each contains the name and
        # size of the partition in bytes and the type of the partition
        partition_types = self.get_partition_types()
        partition_names = ' '.join(partition_types.keys())

        partition_size_output = self.ssh_client.exec_command(
            'fdisk -l %s 2>/dev/null | grep "Disk.*bytes"'
            % (partition_names)).rstrip('\n').split('\n')
        partitions = []
        for row in partition_size_output:
            row_details = row.split()
            partition_name = row_details[1].rstrip(':')
            partition_type = partition_types[partition_name]
            if partition_type == 'swap':
                partition_size = DiskSize(
                    float(row_details[2]), row_details[3].rstrip(','))
            else:
                partition_size = DiskSize(
                    int(row_details[4]) / 1073741824, 'GB')
            partitions.append(
                Partition(partition_name, partition_size, partition_type))
        return partitions

    def verify_partitions(self, expected_disk_size, expected_swap_size,
                          server_status, actual_partitions):
        """
        @summary: Verify the partition details of the server
        @param expected_disk_size: The expected value of the Disk size in GB
        @type expected_disk_size: string
        @param expected_swap_size: The expected value of the Swap size in GB
        @type expected_swap_size: string
        @param server_status: The status of the server
        @type server_status: string
        @param actual_partitions: The actual partition details of the server
        @type actual_partitions: Partition List
        @return: The result of verification and the message to be displayed
        @rtype: Tuple (bool,string)
        """
        expected_partitions = self._get_expected_partitions(
            expected_disk_size, expected_swap_size, server_status)
        if actual_partitions is None:
            actual_partitions = self.get_partition_details()

        for partition in expected_partitions:
            if partition not in actual_partitions:
                return False, self._construct_partition_mismatch_message(
                    expected_partitions, actual_partitions)
        return True, "Partitions Matched"

    def _get_expected_partitions(self, expected_disk_size,
                                 expected_swap_size, server_status):
        """
        @summary: Returns the expected partitions for a server
            based on server status
        @param expected_disk_size: The Expected disk size of the server in GB
        @type expected_disk_size: string
        @param expected_swap_size: The Expected swap size of the server in MB
        @type expected_swap_size: string
        @param server_status: Status of the server (ACTIVE or RESCUE)
        @type server_status: string
        @return: The expected partitions
        @rtype: Partition List
        """
        # ignoring swap untill the rescue functionality is clarified

        expected_partitions = [Partition(
            '/dev/xvda1', DiskSize(expected_disk_size, 'GB'), 'ext3'),
            Partition('/dev/xvdc1',
                      DiskSize(expected_swap_size, 'MB'), 'swap')]
        if str.upper(server_status) == 'RESCUE':
            expected_partitions = [Partition(
                '/dev/xvdb1', DiskSize(expected_disk_size, 'GB'), 'ext3')]
            # expected_partitions.append(Partition('/dev/xvdd1',
            # DiskSize(expected_swap_size, 'MB'), 'swap'))
        return expected_partitions

    def _construct_partition_mismatch_message(self, expected_partitions,
                                              actual_partitions):
        """
        @summary: Constructs the partition mismatch message
            based on expected_partitions and actual_partitions
        @param expected_partitions: Expected partitions of the server
        @type expected_partitions: Partition List
        @param actual_partitions: Actual Partitions of the server
        @type actual_partitions: Partition List
        @return: The partition mismatch message
        @rtype: string
        """
        message = 'Partitions Mismatch \n Expected Partitions:\n'
        for partition in expected_partitions:
            message += str(partition) + '\n'
        message += ' Actual Partitions:\n'
        for partition in actual_partitions:
            message += str(partition) + '\n'
        return message

    def mount_file_to_destination_directory(self, source_path,
                                            destination_path):
        '''
        @summary: Mounts the file to destination directory
        @param source_path: Path to file source
        @type source_path: String
        @param destination_path: Path to mount destination
        @type destination_path: String
        '''
        cmd = 'mount {0} {1}'.format(source_path, destination_path)
        self.ssh_client.exec_command(cmd)

    def _is_valid_ipv4_address(self, address):
        '''
        @summary: Checks if a given address is ipv4.
        @param address: The IP address of an instance.
        @type address: String
        @return: True if IP address is IPV4, false otherwise
        @rtype: Boolean
        '''
        try:
            addr = socket.inet_pton(socket.AF_INET, address)
        except AttributeError:
            try:
                addr = socket.inet_aton(address)
            except socket.error:
                return False
            return address.count('.') == 3
        except socket.error:
            return False

        return True

    def _is_valid_ipv6_address(self, address):
        '''
        @summary: Checks if a given address is ipv6.
        @param address: The IP address of an instance.
        @type address: String
        @return: True if IP address is IPV6, false otherwise
        @rtype: Boolean
        '''
        try:
            addr = socket.inet_pton(socket.AF_INET6, address)
        except socket.error:
            return False
        return True

    def generate_bandwidth_from_server_to_client(self,
                                                 public_ip_address,
                                                 gb_file_size,
                                                 server_filepath,
                                                 client_filepath):
        '''
        @summary: Creates and transfers a file from server to client
        @param linux_client: A linux client for a given instance
        @type address: Instance
        @param public_ip_address: The eth0 address of the instance
        @type public_ip_address: String
        @param gb_file_size: The size of the file to be generated in Gigabytes
        @type gb_file_size: Float
        @param server_filepath: The path name including file name on server
        @type server_filepath: String
        @param client_filepath: The path name including file name on client
        @type client_filepath: String
        @return: On successful bandwidth generation, return True else False
        @rtype: Boolean
        @todo: Use json bridge to poll global db for bw_usage_cache update
            instead of sleeping on ssh_timeout
        '''
        time.sleep(self.ssh_timeout)
        # delete same filename locally if it existed in a prior run
        if os.path.exists(client_filepath):
            os.remove(client_filepath)

        # get the initial values from the network interface
        rx_bytes, tx_bytes = self.get_network_bytes_from_server('eth0')

        if not self.create_a_file_on_server(server_filepath,
                                            gb_file_size):
            raise Exception("File was not created on server: {0}, {1}"
                            .format(public_ip_address, server_filepath))

        md5sum_server = self.get_md5sum(server_filepath)
        if not md5sum_server:
            raise Exception("No md5sum from file on server: {0}, {1}"
                            .format(public_ip_address, server_filepath))

        if not self.download_a_file(server_filepath, client_filepath):
            raise Exception("The file {0} was not downloaded from "
                            "the server {1}, {2}".format(client_filepath,
                                                         public_ip_address,
                                                         server_filepath))

        if not os.path.isfile(client_filepath):
            raise Exception("The file {0} was not transferred from server "
                            "to local client: {1}".format(client_filepath,
                                                          public_ip_address))

        md5sum_client = self.get_md5sum_on_client(client_filepath)
        if (md5sum_server != md5sum_client):
            raise Exception("The md5sums did not match: {0}, {1} != {2}, {3}"
                            .format(md5sum_server, public_ip_address,
                                    md5sum_client, "localhost"))

        # clean up and delete the local file we just downloaded
        if os.path.exists(client_filepath):
            os.remove(client_filepath)

        # get the byte values after generating bandwidth and subtract
        rx_bytes_after, tx_bytes_after = \
            self.get_network_bytes_from_server('eth0')
        rx_bytes = int(rx_bytes_after) - int(rx_bytes)
        tx_bytes = int(tx_bytes_after) - int(tx_bytes)

        expected_bw_upper = int(datatools.gb_to_bytes(gb_file_size) * 1.10)
        expected_bw_lower = int(datatools.gb_to_bytes(gb_file_size) * 0.90)

        if (tx_bytes > expected_bw_upper):
            raise Exception("The amount of bandwidth reported from the "
                            "instance network interface is over 10%% of "
                            "expected. nic: {0} expected {1}"
                            .format(tx_bytes, expected_bw_upper))

        if (tx_bytes < expected_bw_lower):
            raise Exception("The amount of bandwidth reported from the "
                            "instance network interface is under 10%% of "
                            "expected. nic: {0} expected {1}"
                            .format(tx_bytes, expected_bw_lower))
        time.sleep(self.ssh_timeout)
        return True

    def remote_process_grep(self, process_name):
        '''
        @summary: Retrieves the raw text of a process search.
        @param process_name: The name of the process being searched.
        @type process_name: String
        @return: The full response for the process search
        @rtype: String
        '''
        command = "ps aux | grep {0}".format(process_name)
        return self.ssh_client.exec_command(command).rstrip('\n')

    def get_xen_user_metadata(self):
        command = 'xenstore-ls vm-data/user-metadata'
        output = self.ssh_client.exec_command(command)
        meta_list = output.split('\n')
        meta = {}
        for item in meta_list:
            # Skip any blank lines
            if item:
                meta_item = item.split("=")
                key = meta_item[0].strip()
                value = meta_item[1].strip('" ')
                meta[key] = value
        return meta

