from ccengine.common.connectors.ssh import SSHConnector


def attempt_ssh_from_server_to_server(from_ip, from_password,
                                      to_ip, to_password,
                                      from_user='root', to_user='root'):
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
    ssh = SSHConnector(from_ip, from_user, from_password, timeout=10)
    ssh.start_shell()
    ip_login = '@'.join([to_user, to_ip])
    ip_ssh_comm = ''.join(['ssh -o StrictHostKeyChecking=no ',
                            ip_login, '\n'])
    prompt = ssh.exec_shell_command(ip_ssh_comm)[1]
    ssh.end_shell()
    if prompt.find('password') == -1:
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
    ssh = SSHConnector(from_ip, from_user, from_password, timeout=10)
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
        output, prompt = ssh.exec_shell_command_wait_for_prompt(to_password +\
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
                                          remote_user='root'):
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
    ssh = SSHConnector(gw_ip, gw_user, gw_password, timeout=10)
    ssh.start_shell()
    ip_login = '@'.join([remote_user, remote_ip])
    ip_ssh_comm = ''.join(['ssh -o StrictHostKeyChecking=no ', ip_login, '\n'])
    prompt = ssh.exec_shell_command(ip_ssh_comm)[1]
    if prompt.find('password') == -1:
        return False
    output, prompt = ssh.exec_shell_command(remote_password + '\n')
    if prompt.find('~#') == -1:
        return False
    for command in command_list:
        output, prompt = ssh.exec_shell_command(command + '\n')
    ssh.end_shell()
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
    ssh = SSHConnector(ip, user, password, timeout=10)
    return ssh.exec_command(command)
