'''
@summary: Client to execute Hadoop commands on a node
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from ccengine.clients.base_client import BaseClient
from ccengine.common.connectors.ssh import SSHConnector


class HadoopClient(BaseClient):
    '''
    @summary: Each field is an instance of a sub client to execute hadoop,
    each with a different option.
    '''
    def __init__(self, username, password, host):
        super(HadoopClient, self).__init__()
        self.filesystem = _FileSystem(username, password, host)
        self.dfs_admin = _DfsAdmin(username, password, host)


class _BaseHadoopClient(BaseClient):
    '''
    @summary: Base client for calling hadoop commands.
    '''
    def __init__(self, username, password, host):
        super(_BaseHadoopClient, self).__init__()
        self.ssh_connector = SSHConnector(host,
                                          username,
                                          password)
        self.base_command = 'hadoop'
        self.username = username
        self.password = password
        self.host = host


class _FileSystem(_BaseHadoopClient):
    '''
    @summary: Client to call "hadoop fs" commands
    '''
    def __init__(self, username, password, host):
        '''
        @summary: adds 'fs' option to hadoop command
        '''
        super(_FileSystem, self).__init__(username, password, host)
        self.base_command += ' fs'

    def get(self, source, destination="."):
        '''
        @summary: Gets source file from hdfs and copies it to destination on node
        '''
        command = "%s -get %s/ %s" % (self.base_command, source, destination)
        return self.ssh_connector.exec_command(command)

    def list(self, folder=''):
        '''
        @summary: Lists files in folder
        '''
        command = "%s -ls %s" % (self.base_command, folder)
        return self.ssh_connector.exec_command(command)

    def put(self, source, destination="."):
        '''
        @summary: Gets source file from node and copies it to destination on hdfs
        '''
        command = "%s -put %s %s" % (self.base_command, source, destination)
        return self.ssh_connector.exec_command(command)

    def rmr(self, directory, skip_trash=False):
        '''
        @summary: Gets source file from node and copies it to destination on hdfs
        '''
        if not skip_trash:
            command = "%s -rmr %s" % (self.base_command, directory)
        else:
            command = "%s -rmr -skipTrash %s" % (self.base_command, directory)
        response = self.ssh_connector.exec_command(command)
        result = response.find(response) != - 1
        return result

    def mkdir(self, directory_name):
        command = "{0} -mkdir {1}".format(self.base_command, directory_name)
        response = self.ssh_connector.exec_command(command)
        result = response.find(response) != -1
        return result


class _DfsAdmin(_BaseHadoopClient):
    '''
    @summary: Client to call "hadoop dfsadmin" commands
    '''
    def __init__(self, username, password, host):
        '''
        @summary: Adds 'dfsadmin' option to hadoop command
        '''
        super(_DfsAdmin, self).__init__(username, password, host)
        self.base_command += ' dfsadmin'

    def report(self, timeout=20):
        '''
        @summary: Prints out stats on all datanodes
        '''
        command = "%s -report" % self.base_command
        output, prompt = self.ssh_connector.exec_shell_command("sudo su hdfs")
        if prompt.find("Password") != -1:
            output, prompt = self.ssh_connector.exec_shell_command(
                self.password)
            if prompt.find("$") != -1:
                output, prompt = self.ssh_connector.\
                    exec_shell_command_wait_for_prompt(
                        command, "$", timeout=timeout)
                return output
        elif prompt.find("$") != -1:
            output, prompt = self.ssh_connector.\
                exec_shell_command_wait_for_prompt(
                    command, "$", timeout=timeout)
            return output
