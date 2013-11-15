from ccengine.common.connectors.compute_ssh import ComputeSSHConnector
from ccengine.common.connectors.ping import PingClient
import time
from ccengine.common.exceptions.compute import FileNotFoundException, \
    ServerUnreachable
from ccengine.domain.compute.file_details import FileDetails
from ccengine.domain.compute.partition import DiskSize, Partition
import re
from ccengine.common.tools.wmi_helper import WmiHelper
from ccengine.common.tools.datagen import bytes_to_mb, bytes_to_gb


class WindowsClient(object):

    def __init__(self, ip_address, server_id, os_distro, username, password):
        ssh_timeout = 1200
        self.username = username
        if self.username is None:
            self.username = 'administrator'
        if ip_address is None:
            # TODO (dwalleck): Finishing porting over zodiac exceptions
            raise ServerUnreachable("None")
        self.ip_address = ip_address
        self.password = password
        self.server_id = server_id
        self.wmi = WmiHelper(self.ip_address, self.username, self.password)

    def can_connect_to_public_ip(self):
        """
        @summary: Checks if you can connect to server using public ip
        @return: True if you can connect, False otherwise
        @rtype: bool
        """
        return self.wmi.connection is not None

    def get_hostname(self):
        """
        @summary: Gets the host name of the server
        @return: The host name of the server
        @rtype: string
        """
        actual_hostname = self.wmi.exec_command('hostname')
        return actual_hostname.rstrip()

    def can_remote_ping_private_ip(self, private_addresses):
        """
        @summary: Checks if you can ping a private ip from this server.
        @param private_addresses: List of private addresses
        @type private_addresses: Address List
        @return: True if you can ping, False otherwise
        @rtype: bool
        """
        for private_address in private_addresses:
            if private_address.version == 4 and not PingClient.ping_using_remote_machine(self.wmi, private_address.ip):
                return False
        return True

    def get_files(self, path):
        """
        @summary: Gets the list of filenames from the path
        @param path: Path from where to get the filenames
        @type path: string
        @return: List of filenames
        @rtype: List of strings
        """
        command = "dir /B "
        file_list = self.wmi.exec_command(command)
        return file_list.split("\r\n")

    def go_to_folder(self, folder):
        """
        @summary: Go to a particular path in the server
        @param folder: path to a folder.
        @type folder: String
        @return: Data read from standard output during execution of the command
        @rtype: String
        """
        command = "cd " + folder
        self.wmi.exec_command(command)

    def get_boot_time(self):
        """
        @summary: Get the boot time of the server
        @return: The boot time of the server
        @rtype: time.struct_time
        """
        os = self.wmi.connection.Win32_OperatingSystem()[0]
        return os.LastBootUpTime

    def create_file(self, file_name, file_content):
        '''
        @summary: Create a new file
        @param file_name: File Name
        @type file_name: String
        @param file_content: File Content
        @type file_content: String
        @return filedetails: File details such as content, name and path
        @rtype filedetails; FileDetails
        '''
        file_path = "C:\\Users\\Administrator\\" + file_name
        self.ssh_client.exec_command('echo' + file_content + '>>' + file_path)
        return FileDetails("666", file_content, file_path)

    def get_file_details(self, filepath):
        """
        @summary: Get the file details
        @param filepath: Path to the file
        @type filepath: string
        @return: File details including permissions and content
        @rtype: FileDetails
        """
        file_permissions = self.wmi.exec_command('cacls ' + filepath)
        file_contents = self.wmi.exec_command('type ' + filepath)
        return FileDetails(file_permissions.rstrip("\n"), file_contents.rstrip("\n"), filepath)

    def is_file_present(self, filepath):
        """
        @summary: Check if the given file is present
        @param filepath: Path to the file
        @type filepath: string
        @return: True if File exists, False otherwise
        """
        command = '(if exist ' + filepath + ' (echo True) else (echo False))'
        file_exists = self.wmi.exec_command(command)
        return file_exists.rstrip('\n') == "True"

    def get_ram_size_in_mb(self):
        """
        @summary: Returns the RAM size in MB
        @return: The RAM size in MB
        @rtype: string
        """
        os = self.wmi.connection.Win32_OperatingSystem()[0]
        return bytes_to_mb(os.TotalVisibleMemorySize)

    def get_swap_size_in_mb(self):
        """
        @summary: Returns the Swap size in MB
        @return: The Swap size in MB
        @rtype: string
        """
        return str(0)

    def get_disk_size_in_gb(self):
        """
        @summary: Returns the disk size in GB
        @return: The disk size in GB
        @rtype: int
        """
        disk = self.wmi.connection.Win32_DiskDrive()[0]
        return bytes_to_gb(disk.size)

    def get_partition_details(self):
        """
        @summary: Return the partition details
        @return: The partition details
        @rtype: Partition List
        """
        disk_partitions = self.wmi.connection.Win32_DiskPartition()
        partitions = []
        index = 0
        for partition in disk_partitions:
            # if self.wmi.connection.Win32_DiskPartition()[index].diskindex == 0 :
            partitions.append(Partition(partition.Name, DiskSize(bytes_to_gb(partition.Size), "GB"), partition.Type))
            # index = index + 1
        return partitions

    def verify_partitions(self, expected_disk_size, expected_swap_size, server_status, actual_partitions):
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
        expected_partitions = self._get_expected_partitions(expected_disk_size, expected_swap_size, server_status)
        if actual_partitions is None:
            actual_partitions = self.get_partition_details()

        for partition in expected_partitions:
            if partition not in actual_partitions:
                return False, self._construct_partition_mismatch_message(expected_partitions, actual_partitions)
        return True, "Partitions Matched"

    def get_number_of_vcpus(self):
        """
        @summary: Get the number of vcpus assigned to the server
        @return: The number of vcpus assigned to the server
        @rtype: int
        """
        return len(self.wmi.connection.Win32_Processor())

    def _get_expected_partitions(self, expected_disk_size, expected_swap_size, server_status):
        """
        @summary: Returns the expected partitions for a server based on server status
        @param expected_disk_size: The Expected disk size of the server in GB
        @type expected_disk_size: string
        @param expected_swap_size: The Expected swap size of the server in MB
        @type expected_swap_size: string
        @param server_status: Status of the server (ACTIVE or RESCUE)
        @type server_status: string
        @return: The expected partitions
        @rtype: Partition List
        """
        expected_partitions = [Partition('disk #0, partition #1', DiskSize(expected_disk_size, 'GB'), 'Installable File System')]

        if str.upper(server_status) == 'RESCUE':
            expected_partitions.append(Partition('disk #2, partition #0', DiskSize(expected_disk_size, 'GB'), 'Installable File System'))
        return expected_partitions

    def _construct_partition_mismatch_message(self, expected_partitions, actual_partitions):
        """
        @summary: Constructs the partition mismatch message based on expected_partitions and actual_partitions
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
