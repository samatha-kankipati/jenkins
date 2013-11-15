import json
from ccengine.domain.base_domain import BaseMarshallingDomain


class WorkerRegistration(BaseMarshallingDomain):
    def __init__(self, hostname=None, callback=None, ip_address_v4=None,
                 ip_address_v6=None, personality=None, status=None,
                 system_info=None):
        super(WorkerRegistration, self).__init__()

        self.hostname = hostname
        self.callback = callback
        self.ip_address_v4 = ip_address_v4
        self.ip_address_v6 = ip_address_v6
        self.personality = personality
        self.status = status
        self.system_info = system_info

    def get_obj_body(self):
        body = {
            'worker_registration': {
                'hostname': self.hostname,
                'callback': self.callback,
                'ip_address_v4': self.ip_address_v4,
                'ip_address_v6': self.ip_address_v6,
                'personality': self.personality,
                'status': self.status,
                'system_info': self.system_info.get_obj_body()
            }
        }
        return body

    def _obj_to_json(self):
        return json.dumps(self.get_obj_body())


class SystemInfo(BaseMarshallingDomain):
    def __init__(self, disk_usage=None, os_type=None, memory_mb=None,
                 architecture=None, cpu_cores=None, load_average=None):
        super(SystemInfo, self).__init__()

        self.os_type = os_type
        self.memory_mb = memory_mb
        self.architecture = architecture
        self.cpu_cores = cpu_cores
        self.load_average = load_average
        self.disk_usage = disk_usage

    def get_obj_body(self):
        body = {
            'os_type': self.os_type,
            'memory_mb': self.memory_mb,
            'architecture': self.architecture,
            'cpu_cores': self.cpu_cores,
            'load_average': self.load_average,
            'disk_usage': self.disk_usage.get_obj_body()
        }
        return body

    def _obj_to_json(self):
        return json.dumps(self.get_obj_body())


class DiskUsage(BaseMarshallingDomain):
    def __init__(self, disks=None):
        super(DiskUsage, self).__init__()
        self.disks = disks

    def add_disk(self, path, used, total):
        if self.disks is None:
            self.disks = []

        disk = {
            'path': path,
            'used': used,
            'total': total
        }
        self.disks.append(disk)

    def get_obj_body(self):
        body = {}
        for disk in self.disks:
            body[disk['path']] = {
                'used': disk['used'],
                'total': disk['total']
            }
        return body

    def _obj_to_json(self):
        return json.dumps(self.get_obj_body())


class WorkerStatus(BaseMarshallingDomain):
    def __init__(self, worker_status=None):
        super(WorkerStatus, self).__init__()
        self.worker_status = worker_status

    def get_obj_body(self):
        body = {
            'worker_status': self.worker_status
        }
        return body

    def _obj_to_json(self):
        return json.dumps(self.get_obj_body())
