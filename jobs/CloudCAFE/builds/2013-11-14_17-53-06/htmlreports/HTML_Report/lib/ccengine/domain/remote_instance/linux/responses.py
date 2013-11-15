import re
from ccengine.domain.base_domain import BaseDomain


class Stat(BaseDomain):

    def __init__(self, file_name=None, size=None, blocks=None, io_block=None,
                 device=None, inode=None, links=None, permissions_oct=None,
                 permissions_rwx=None, uid_num=None, uid_name=None,
                 gid_num=None, gid_name=None, access_timestamp=None,
                 modify_timestamp=None, change_timestamp=None,
                 birth_timestamp=None):

        self.file_name = file_name
        self.size = size
        self.blocks = blocks
        self.io_block = io_block
        self.device = device
        self.inode = inode
        self.links = links
        self.permissions_oct = permissions_oct
        self.permissions_rwx = permissions_rwx
        self.uid_num = uid_num
        self.uid_name = uid_name
        self.gid_num = gid_num
        self.gid_name = gid_name
        self.access_timestamp = access_timestamp
        self.modify_timestamp = modify_timestamp
        self.change_timestamp = change_timestamp
        self.birth_timestamp = birth_timestamp

    def __repr__(self):
        return str(vars(self))

    @staticmethod
    def str_to_obj(str_):

        def _find(regex, resp_string):
            #This should probably go in a a base linux response domain obj
            search_result = None
            try:
                search_result = (re.search(regex, resp_string)).groups(0)[0]
                return search_result
            except:
                pass
            return None

        resp = Stat()
        resp.file_name = _find("File:\s\`(.*)\'", str_)
        resp.size = _find("Size:\s([0-9]+)", str_)
        resp.blocks = _find("Blocks:\s([0-9]+)", str_)
        resp.io_block = _find("IO Block:\s([0-9]+)", str_)
        resp.device = _find("Device:\s(\S*)Inode", str_)
        resp.inode = _find("Inode:\s([0-9]+)", str_)
        resp.links = _find("Links:\s([0-9]+)", str_)
        resp.permissions_oct = _find("Access:\s\(\s*([0-9]+)/", str_)
        resp.permissions_rwx = _find("Access:\s\(\s*[0-9]+/(\S+)\)", str_)
        resp.uid_num = _find("Uid:\s\(\s*([0-9]+)/", str_)
        resp.uid_name = _find("Uid:\s\(\s*[0-9]+/(\S+)\)", str_)
        resp.gid_num = _find("Gid:\s\(\s*([0-9]+)/", str_)
        resp.gid_name = _find("Gid:\s\(\s*[0-9]+/(\S+)\)", str_)
        resp.access_timestamp = _find("Access:\s([0-9\-]+.*)", str_)
        resp.modify_timestamp = _find("Modify:\s([0-9\-]+.*)", str_)
        resp.change_timestamp = _find("Change:\s([0-9\-]+.*)", str_)
        resp.birth_timestamp = _find("Birth:\s(.*)", str_)

        return resp
