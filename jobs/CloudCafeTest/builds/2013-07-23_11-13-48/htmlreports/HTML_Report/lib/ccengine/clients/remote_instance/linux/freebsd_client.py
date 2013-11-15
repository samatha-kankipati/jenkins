import time
import re
from ccengine.clients.remote_instance.linux.linux_instance_client import LinuxClient
from ccengine.common.constants.compute_constants import Constants


class FreeBSDClient(LinuxClient):
    def get_boot_time(self):
        """
        @summary: Get the boot time of the server
        @return: The boot time of the server
        @rtype: time.struct_time
        """
        uptime_string = self.ssh_client.exec_command('uptime')
        uptime = uptime_string.replace('\n', '').split(',')[0].split()[2]
        uptime_unit = uptime_string.replace('\n', '').split(',')[0].split()[3]
        if (uptime_unit == 'mins'):
            uptime_unit_format = 'M'
        else:
            uptime_unit_format = 'S'

        reboot_time = self.ssh_client.exec_command('date -v -' + uptime + uptime_unit_format + ' "+%Y-%m-%d %H:%M"').replace('\n', '')

        return time.strptime(reboot_time, Constants.LAST_REBOOT_TIME_FORMAT)

    def get_disk_size_in_gb(self):
        """
        @summary: Returns the disk size in GB
        @return: The disk size in GB
        @rtype: int
        """
        output = self.ssh_client.exec_command('gpart show -p | grep "GPT"').replace('\n', '')
        disk_size = re.search(r'([0-9]+)G', output).group(1)
        return int(disk_size)
