from ccengine.providers.base_provider import BaseProvider
from ccengine.clients.loggingaas.pairing_client import PairingClient
from ccengine.domain.loggingaas.request.pairing_request import \
    WorkerRegistration, SystemInfo, DiskUsage


class PairingProvider(BaseProvider):
    def __init__(self, config):
        super(PairingProvider, self).__init__()

        self.config = config
        self.client = PairingClient(
            coordinator_url=config.loggingaas.coordinator_base_url,
            worker_url=config.loggingaas.worker_base_url,
            api_version=config.loggingaas.appver,
            api_secret=config.loggingaas.api_secret,
            personality=config.loggingaas.personality
        )

    def pair_worker(self, hostname=None, callback=None, ip_v4=None, ip_v6=None,
                    personality=None, status=None, disk_path=None,
                    disk_used=None, disk_total=None, os_type=None,
                    cpu_cores=None, load_average=None, memory_mb=None,
                    arch=None):

        if status is None:
            status = 'new'

        # Use config values
        cfg = self.config.loggingaas
        if hostname is None:
            hostname = cfg.hostname
        if callback is None:
            callback = cfg.callback
        if ip_v4 is None:
            ip_v4 = cfg.ip_address_v4
        if ip_v6 is None:
            ip_v6 = cfg.ip_address_v6
        if personality is None:
            personality = cfg.personality
        if disk_path is None:
            disk_path = cfg.disk_path
        if disk_used is None:
            disk_used = cfg.disk_used
        if disk_total is None:
            disk_total = cfg.disk_total
        if os_type is None:
            os_type = cfg.os_type
        if memory_mb is None:
            memory_mb = cfg.memory_mb
        if arch is None:
            arch = cfg.arch
        if cpu_cores is None:
            cpu_cores = cfg.cpu_cores
        if load_average is None:
            load_average = cfg.load_average

        disk_usage = DiskUsage()
        disk_usage.add_disk(path=disk_path, used=disk_used, total=disk_total)

        sys_info = SystemInfo(disk_usage=disk_usage, os_type=os_type,
                              memory_mb=memory_mb, architecture=arch,
                              cpu_cores=cpu_cores, load_average=load_average)
        registration = WorkerRegistration(hostname, callback, ip_v4, ip_v6,
                                          personality, status, sys_info)

        return self.client.pair_worker(registration)

    def load_configuration(self, worker_id, worker_token):
        return self.client.load_configuration(worker_id, worker_token)

    def register(self, worker_id, worker_token, status):
        return self.client.register(worker_id, worker_token, status)
