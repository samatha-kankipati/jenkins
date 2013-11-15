import os
import shutil
from ccengine.common.tools.datagen import rand_name
import subprocess
OUTPUT_FILE_PATH = 'c:\\'
import platform
if platform.system().lower() == 'windows':
    import wmi
    import win32wnet

def create_file(filename, file_text):
    """
    @summary: Creates a local file with text content
    @param filename: The file path
    @type filename: string
    @param file_text: File contents
    @type file_text: string 
    """
    f = open(filename, "w")
    f.write(file_text)
    f.close()

class WmiHelper:
    """
    @summary: Wrapper class around WMI
    """
    def __init__(self, ip, username, password, output_file_path=OUTPUT_FILE_PATH):
        self.ip = ip
        self.username = username
        self.password = password
        self.output_file_path = output_file_path
        self.connection = None
        self.disable_firewall(ip=ip, password=password)
        try:
            self.connection = wmi.WMI(self.ip, user=self.username, password=self.password)
        except wmi.x_wmi:
            print "Could not connect to machine", self.ip


    def enable_firewall(self, ip, user="Administrator", password=None):
        """
        @summary: Enable Firewall on the server
        @param ip: IP address of the server
        @type ip: string
        @param user: Administrator user name
        @type user: string
        @param password: Administrator password
        @type password: string
        """
        ipaddr = '\\\\' + ip
        command = "netsh advfirewall set currentprofile state on"
        p = subprocess.Popen(["c:\\PsExec.exe", ipaddr , "-u", user, "-p", password, "-i", "netsh", "advfirewall", "set", "currentprofile", "state", "on"])
        p.communicate()

    def disable_firewall(self, ip, user="Administrator", password=None):
        """
        @summary: Disable Firewall on the server
        @param ip: IP address of the server
        @type ip: string
        @param user: Administrator user name
        @type user: string
        @param password: Administrator password
        @type password: string
        """
        ipaddr = '\\\\' + ip
        command = "netsh advfirewall set currentprofile state off"
        p = subprocess.Popen(["c:\\PsExec.exe", ipaddr , "-u", user, "-p", password, "-i", "netsh", "advfirewall", "set", "currentprofile", "state", "off"])
        p.communicate()

    def exec_command(self, cmd, async=False, minimized=True, output=True):
        """
        @summary: Execute a command on the server
        @param cmd: Command to be executed
        @type cmd: string
        @param async: Should run command asynchronously
        @type async: bool
        @param minimized: The command should be run minimized
        @type minimized: bool
        @param output: Should the output be captured from the server into a local file
        @type output: bool
        @return: The output of the command executed
        @rtype: string or None
        """
        output_data = None
        output_file_name = rand_name("out")
        bat_local_path = os.path.join(self.output_file_path, output_file_name + ".bat")
        bat_remote_path = os.path.join(self.output_file_path, output_file_name + ".bat")
        output_remote_path = os.path.join(self.output_file_path, output_file_name + ".out")
        output_local_path = os.path.join(self.output_file_path, output_file_name + ".out")
        text = cmd + " > " + output_remote_path
        create_file(bat_local_path, text)
        self.net_copy(bat_local_path, self.output_file_path)
        batcmd = bat_remote_path

        SW_SHOWMINIMIZED = 0
        if not minimized:
            SW_SHOWMINIMIZED = 1
        print "Executing %s" % cmd
        startup = self.connection.Win32_ProcessStartup.new (ShowWindow=SW_SHOWMINIMIZED)
        self.connection.Win32_Process.Create (CommandLine=batcmd, ProcessStartupInformation=startup)

        if output:
            self.net_copy_back(output_remote_path, output_local_path)
            output_data = open(output_local_path, 'r')
            output_data = "".join(output_data.readlines())
            self.net_delete(output_remote_path)
        self.net_delete(bat_remote_path)
        return output_data

    def net_copy(self, source, dest_dir, move=True):
        """
        @summary: Copies the file from source to destination directory
        @param source: source file path
        @type source: string
        @param dest_dir: destination file path
        @type dest_dir: string
        @param move: should the file be moved or copied 
        @type move: boolean
        """
        self._wnet_connect()
        dest_dir = self._convert_unc(dest_dir)

        # Pad a backslash to the destination directory if not provided.
        if not dest_dir[len(dest_dir) - 1] == '\\':
            dest_dir = ''.join([dest_dir, '\\'])

        # Create the destination dir if its not there.
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        if move:
            shutil.move(source, dest_dir)
        else:
                shutil.copy(source, dest_dir)

    def net_copy_back(self, source_file, dest_file):
        """
        @summary: Copies the output from source to destination file
        @param source_file: source file 
        @type source_file: string
        @param dest_file: destination file path
        @type dest_file: string
        """

        self._wnet_connect()
        source_unc = self._convert_unc(source_file)
        shutil.copyfile(source_unc, dest_file)

    def _wnet_connect(self):
        """
        @summary: Creates a connection to a network resource
        """

        unc = ''.join(['\\\\', self.ip])
        try:
            win32wnet.WNetAddConnection2(0, None, unc, None, self.username, self.password)
        except Exception, err:
            if isinstance(err, win32wnet.error):
                # Disconnect previous connections if detected, and reconnect.
                if err[0] == 1219:
                    win32wnet.WNetCancelConnection2(unc, 0, 0)
                    return self._wnet_connect(self)
            raise err

    def _convert_unc(self, path):
        """ 
        @summary: Convert a file path on a host to a UNC path
        """
        return ''.join(['\\\\', self.ip, '\\', path.replace(':', '$')])

    def copy_folder(self, local_source_folder, remote_dest_folder):
        """
        @summary: copy the folder from the source to the destination
        """
        files_to_copy = os.listdir(local_source_folder)
        for file_to_copy in files_to_copy:
            file_path = os.path.join(local_source_folder, file_to_copy)
            try:
                self.net_copy(file_path, remote_dest_folder)
            except WindowsError:
                print 'could not connect to ', self.ip
            except IOError:
                print 'One of the files is being used on ', self.ip, ', skipping the copy procedure'

    def net_delete(self, path):
        """ 
        @summary: delete the directory/file created
        """

        self._wnet_connect()
        path = self._convert_unc(path)
        if os.path.exists(path):
            # Delete directory tree if object is a directory.
            if os.path.isfile(path):
                try:
                    os.remove(path)
                except:
                    print "file could not be deleted"
            else:
                shutil.rmtree(path)
