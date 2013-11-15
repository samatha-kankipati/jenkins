import time
from ccengine.clients.remote_instance.linux.linux_instance_client import LinuxClient
from ccengine.common.constants.compute_constants import Constants


class GentooArchClient(LinuxClient):
    def get_boot_time(self):
        """
        @summary: Get the boot time of the server
        @return: The boot time of the server
        @rtype: time.struct_time
        """
        boot_time_string = self.ssh_client.exec_command('who -b | grep -o "[A-Za-z]* [0-9].*"').replace('\n', ' ')
        year = self.ssh_client.exec_command('date | grep -o "[0-9]\{4\}$"').replace('\n', '')
        boot_time = boot_time_string + year

        return time.strptime(boot_time, Constants.LAST_REBOOT_TIME_FORMAT_GENTOO)
