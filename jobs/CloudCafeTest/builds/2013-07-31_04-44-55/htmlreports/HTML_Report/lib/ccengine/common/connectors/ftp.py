from ftplib import FTP
import ftplib
from ccengine.common.connectors.base_connector import BaseConnector
from ccengine.common.connectors.ssh import SSHConnector

class FTPConnector(BaseConnector):
    """
    @summary: Client for ftp operations 
    """

    def __init__(self, host, username, password, timeout=10, port = 22):
        super(FTPConnector, self).__init__()
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.timeout = int(timeout)
        self._chan = None
        self.connector_log.info("FTP connection created at %s:%s" 
                                %(host, port))
        
    def disableService(self,cluster_type):
        ssh_connector = SSHConnector(self.host,
                                     self.username,
                                     self.password)
        response = ''
        if cluster_type == 'hadoop_hdp_1_1':
            command = 'sudo chkconfig --del ftpsvc'
            ssh_connector.exec_shell_command(command)
            response,prompt = ssh_connector.exec_shell_command(self.password)
        elif cluster_type ==  'hadoop_cdh3':
            command = "sudo update-rc.d ftpsvc disable"
            ssh_connector.exec_shell_command(command)
            response,prompt = ssh_connector.exec_shell_command(self.password)
        message = "FTP disable response for %s:%s"%(self.host, response)
        self.connector_log.info(message)
        
    def enableService(self,cluster_type):
        ssh_connector = SSHConnector(self.host,
                                     self.username,
                                     self.password)
        if cluster_type == 'hadoop_hdp_1_1':
            command = 'sudo chkconfig --add ftpsvc'
            ssh_connector.exec_shell_command(command)
            response,prompt = ssh_connector.exec_shell_command(self.password)
        elif cluster_type ==  'hadoop_cdh3':
            command = 'sudo update-rc.d ftpsvc enable'
            ssh_connector.exec_shell_command(command)
            response,prompt = ssh_connector.exec_shell_command(self.password)
        message = "FTP connection enable response for %s:%s"%(self.host, 
                                                              response)
        self.connector_log.info(message)
            
    def stopService(self):
        ssh_connector = SSHConnector(self.host,
                                     self.username,
                                     self.password)
        ssh_connector.exec_shell_command('sudo service ftpsvc stop')
        response,prompt = ssh_connector.exec_shell_command(self.password)
        self.connector_log.info("FTP connection stop response for %s:%s"
                                 % (self.host, response))
           
    def upload_a_file(self,client_file_path):
        ftp_client = FTP()
        try:
            ftp_client.connect(self.host,self.port)
            ftp_client.login(self.username, self.password)
            file_to_be_uploaded = open(client_file_path, "rb")
            file_name = client_file_path.split("/")[-1]
            self.connector_log.debug("Uploading File: %s"
                                      % client_file_path)
            response = ftp_client.storbinary('STOR %s'%(file_name), 
                                             file_to_be_uploaded,
                                             1024)
            self.connector_log.info("Response for file: %s is %s"
                                    %(client_file_path,response))
            file_to_be_uploaded.close()
            if response.find("Transfer complete") != -1:
                self.connector_log.info("File: %s uploaded to hdfs")
                return True
        except Exception,e:
            self.connector_log.error("%s times out for upload"
                                     %(client_file_path))
            return False

    def browse(self):
        try:
            ftp_client = FTP()
            ftp_client.connect(self.host,self.port)
            ftp_client.login(self.username, self.password)
            response = ftp_client.nlst()
            self.connector_log.info("NLST Response: '%s'" % response)
            return response
        except ftplib.error_perm, resp:
            if str(resp) == "550 No files found":
                message = "There are no files in this directory!"
                self.connector_log.warning(message)
            else:
                raise


       

