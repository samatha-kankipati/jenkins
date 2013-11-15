from ccengine.common.connectors.ssh import SSHConnector
from ccengine.common.exceptions.compute import SshConnectionException
from ccengine.common.connectors.commandline import CommandLineConnector

import random
import os

def attempt_ssh_from_server_to_server(from_ip, from_password,
                                      to_ip, to_password,
                                      from_user='root', to_user='root',
                                      retry=5):
    '''
    @summary: Tests connectivity from pub_ip to many servers
    @param from_ip: Server IP to try an ssh connection from
    @type from_ip: C{str}
    @param from_password: ssh password of from_server
    @type from_password: C{str}
    @param to_server: Server IP ot try an ssh connection to
    @type to_server: C{str}
    @param to_password: ssh password of to_server
    @type to_password: C{str}
    @param from_user: user to ssh into from_ip
    @type from_user: C{str}
    @param to_user: user to ssh into from from_ip
    @type to_user: C{str}
    @return: If ssh was successful
    @rtype:  C{bool}
    '''
    msg = '{0} SSH connection failed with username:{1} and password: {2}'

    ssh = SSHConnector(from_ip, from_user, from_password, tcp_timeout=10)
    if not ssh.test_connection_auth():
        raise SshConnectionException(msg.format(from_ip, from_user,
                                                from_password))

    # adding retries to be able to get only reproducible failures
    count = 0
    while count < retry:
        ssh.start_shell()
        ssh_cmd = 'ssh -o StrictHostKeyChecking=no {0}@{1}\n'.format(to_user,
                                                                     to_ip)
        prompt = ssh.exec_shell_command(ssh_cmd)[1]
        ssh.end_shell()
        if prompt.find('password') != -1:
            break
        count += 1
    else:
        return False
    return True


def send_file_from_server_to_server(from_ip, from_password,
                                    to_ip, to_password,
                                    from_user='root', to_user='root',
                                    wait_for_completion=True,
                                    close_on_finish=True,
                                    out_file_name='output.txt'):
    '''
    @summary: SSH's into a server, creates a file, then sends that file to
              another server
    @param from_ip: Server IP to send a file from
    @type from_ip: C{str}
    @param from_password: ssh password of from_server
    @type from_password: C{str}
    @param to_server: Server IP ot try an ssh connection to
    @type to_server: C{str}
    @param to_password: ssh password of to_server
    @type to_password: C{str}
    @param from_user: user to ssh into from_ip
    @type from_user: C{str}
    @param to_user: user to ssh into from from_ip
    @type to_user: C{str}
    @return: None
    @rtype:  None
    '''
    scp_log_dir = 'scpLogFiles'
    ssh = SSHConnector(from_ip, from_user, from_password, tcp_timeout=10)
#    dd_command = "dd if=/dev/zero of=send_file.iso count=1048576 bs=1024"
#    output = ssh.exec_command(dd_command)
    output = ssh.exec_command('ls')
    if output.find(scp_log_dir) == -1:
        ssh.exec_command('mkdir %s' % scp_log_dir)
    ssh.start_shell()
    ssh.exec_shell_command('cd %s\n' % scp_log_dir)
    ip_login = '@'.join([to_user, to_ip])
    ip_ssh_comm = ''.join([
        'nohup scp -v -o StrictHostKeyChecking=no ../send_file.iso ',
        ip_login, ':send_file.iso > ./%s 2>&1\n' % out_file_name])
    output, prompt = ssh.exec_shell_command(ip_ssh_comm)
    if prompt.find('password') == -1:
        return False
    if wait_for_completion:
        output, prompt = ssh.exec_shell_command_wait_for_prompt(to_password +
                                                                '\n', 'scpLogFiles#')
    else:
        ssh.exec_shell_command(to_password + '\n', stop_after_send=True)
        ssh.exec_shell_command(chr(26))
        ssh.exec_shell_command('bg\n')
    if close_on_finish:
        ssh.end_shell()


def execute_remote_command_through_gateway(gw_ip, gw_password,
                                          remote_ip, remote_password,
                                          command_list, gw_user='root',
                                          remote_user='root', retry=5,
                                          timeout=10):
    '''
    @summary: SSH's into a gateway server then SSH's into another remote server
              from that server, then executes a command.
    @param gw_ip: Server IP to send a file from
    @type gw_ip: C{str}
    @param gw_password: ssh password of from_server
    @type gw_password: C{str}
    @param remote_server: Server IP ot try an ssh connection to
    @type remote_server: C{str}
    @param remote_password: ssh password of to_server
    @type remote_password: C{str}
    @param command_list: commands to run on to_ip
    @type command_list: C{list} of C{str}
    @param gw_user: User to ssh into from_ip. Defaults to root.
    @type gw_user: C{str}
    @param remote_user: User to ssh into from from_ip. Defualts to root.
    @type remote_user: C{str}
    @return: The last output of the last command in command_list
    @rtype:  C{str}
    '''
#    print 'remote_ip: %s' % remote_ip
#    print 'remote_password: %s' % remote_password
    msg = '{0} SSH connection failed with username:{1} and password: {2}'

    ssh = SSHConnector(gw_ip, gw_user, gw_password, tcp_timeout=10)

    if not ssh.test_connection_auth():
        raise SshConnectionException(msg.format(gw_ip, gw_user, gw_password))

    # adding retries to be able to get only reproducible failures
    count = 0
    output = False
    while count < retry:
        ssh.start_shell()
        ssh_cmd = 'ssh -o StrictHostKeyChecking=no {0}@{1}\n'.format(
            remote_user, remote_ip)
        output, prompt = ssh.exec_shell_command_wait_for_prompt(cmd=ssh_cmd,
            prompt='password', timeout=timeout)
        if prompt.find('password') != -1:
            output, prompt = ssh.exec_shell_command_wait_for_prompt(
                remote_password + '\n', timeout=timeout)
            if prompt.find('~#') != -1:
                for command in command_list:
                    output, prompt = ssh.exec_shell_command_wait_for_prompt(
                        command + '\n', timeout=timeout)
                break
        ssh.end_shell()
        count += 1
    else:
        return False

    return output


def execute_remote_command(ip, password, command, user='root'):
    '''
    @summary: Executes command on remote ip and returns the output..
    @param ip: IP of remote server
    @type ip: C{str}
    @param password: Password of user on remote server
    @type password: C{str}
    @param command: Command to be executed on remote server.
    @type command: C{str}
    @param user: User on remote server
    @type user: C{str}
    @return: The oputput of the command
    @rtype:  C{str}
    '''
    ssh = SSHConnector(ip, user, password, tcp_timeout=10)
    return ssh.exec_command(command)


def generate_ssh_keys(keyfilename,
                      keyfilepath,
                      key_size=1024,
                      pass_phrase="",
                      encryption="dsa"):
    '''
    @summary: Generates a pair of ssh keys using the ssh-keygen.
    @param keyfilename: Key file name.
    @type keyfilename: C{str}
    @param keyfilepath: Location for the key file.
    @type keyfilepath: C{str}
    @param key_size: Byte size for ssh keys
    @type key_size: C{str}
    @param pass_phrase: Pass phrase
    @type pass_phrase: C{str}
    @param encryption: Encryption algo
    @type encryption: C{str}
    '''
    if os.path.isfile("{0}/{1}".format(
        keyfilepath, keyfilename)):
        os.remove("{0}/{1}".format(keyfilepath, keyfilename))
    if os.path.isfile("{0}/{1}.pub".format(keyfilepath, keyfilename)):
        os.remove("{0}/{1}.pub".format(keyfilepath, keyfilename))
    key_file_full_path = "{0}/{1}".format(keyfilepath, keyfilename)
    command_line_connector = CommandLineConnector(base_command="ssh-keygen")
    command = "-t {0} -b {1} -f {2} -P '{3}'".format(
        encryption,
        key_size,
        key_file_full_path,
        pass_phrase)
    response = command_line_connector.__send__(command)
    if not os.path.isfile("{0}/{1}".format(keyfilepath, keyfilename)):
        return False, "No private key file found"
    if not os.path.isfile("{0}/{1}.pub".format(keyfilepath, keyfilename)):
        return False, "No public key file found"
    return True, ""


def add_public_key_to_authorized_keys(public_key,
                                      host,
                                      username,
                                      password):
    '''
    @summary: Adds an ssh key to the authorized_keys file on a server.
              So it takes a username and password to connect to a server.
    @param public_key: Key file name.
    @type public_key: C{str}
    @param host: Server ip/url
    @type host: C{str}
    @param username: username for the server
    @type username: C{str}
    @param password: password for the server
    @type password: C{str}
    '''
    ssh_connector = SSHConnector(
        host, username, password)
    result = ssh_connector.exec_command(
        "echo '{0}' >> /home/{1}/.ssh/authorized_keys".format(
            public_key, username))
    check = ssh_connector.exec_command(
        "cat /home/{0}/.ssh/authorized_keys".format(username))
    if check.find(public_key) == -1:
        return False
    else:
        return True
