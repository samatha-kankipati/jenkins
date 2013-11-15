import json
from ccengine.domain.base_domain import BaseDomain, BaseMarshallingDomain


class EqualityBMD(BaseMarshallingDomain):

    def __init__(self, **kwargs):
        super(EqualityBMD, self).__init__(**kwargs)

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False


class Node(EqualityBMD):

    '''
        @summary: Represents a Lava API Cluster
    '''
    def __init__(self, status, name, public_ip, private_ip, role, id,
                 sel, bookmark, **kwargs):
        super(Node, self).__init__(**kwargs)
        self.status = status
        self.name = name
        self.ip = public_ip
        self.private_ip = private_ip
        self.role = role
        self.id = id
        self.sel = sel
        self.bookmark = bookmark

    @classmethod
    def _json_to_obj(cls, serialized_str):
        response_json = json.loads(serialized_str)
        if "nodes" in response_json:
            nodes = []
            for record in response_json['nodes']:
                sel = ""
                bookmark = ""
                for link in record['links']:
                    if link['rel'] == "self":
                        sel = link['href']
                    elif link['rel'] == "bookmark":
                        bookmark = link['href']
                node = Node(record['status'],
                            record['name'],
                            record['addresses']['public'][0]['addr'],
                            record['addresses']['private'][0]['addr'],
                            record['role'],
                            record['id'],
                            sel,
                            bookmark)
                for service in record['services']:
                    if "uri" in service:
                        if "name" in service and len(service['name']) > 0:
                            service_name = "{0}_service".format(
                                service['name'].replace("-", "_"))
                        setattr(node, service_name, service['uri'])
                    else:
                        setattr(node, service_name, None)

                nodes.append(node)
            return nodes
        elif "node" in response_json:
            record = response_json['node']
            sel = ""
            bookmark = ""
            for link in record['links']:
                if link['rel'] == "self":
                    sel = link['href']
                elif link['rel'] == "bookmark":
                    bookmark = link['href']
            node = Node(record['status'],
                        record['name'],
                        record['addresses']['public'][0]['addr'],
                        record['addresses']['private'][0]['addr'],
                        record['role'],
                        record['id'],
                        sel,
                        bookmark)
            for service in record['services']:
                if "uri" in service:
                    setattr(node, service['name'], service['uri'])
                else:
                    setattr(node, service['name'], None)

            return node


class Flavor(EqualityBMD):

    '''
        @summary: Represents a Lava API Flavor
    '''
    def __init__(self, disk, vcpus, ram, id, name, **kwargs):
        super(Flavor, self).__init__(**kwargs)
        self.disk = disk
        self.vcpus = vcpus
        self.ram = ram
        self.id = id
        self.name = name

    @classmethod
    def _json_to_obj(cls, serialized_str):
        flavors = []
        response_json = json.loads(serialized_str)
        if 'flavors' in response_json:
            for record in response_json['flavors']:
                flavor = Flavor(record['disk'],
                                record['vcpus'],
                                record['ram'],
                                record['id'],
                                record['name'])
                flavors.append(flavor)
            return flavors
        elif 'flavor' in response_json:
            record = response_json['flavor']
            flavor = Flavor(record['disk'],
                            record['vcpus'],
                            record['ram'],
                            record['id'],
                            record['name'])
            return flavor


class Type(EqualityBMD):

    '''
    @summary: Represents a Lava API Type
    '''
    def __init__(self, id, name, **kwargs):
        super(Type, self).__init__(**kwargs)
        self.id = id
        self.name = name

    @classmethod
    def _json_to_obj(cls, serialized_str):
        types = []
        response_json = json.loads(serialized_str)
        for record in response_json['types']:
            type = Type(record['id'],
                        record['name'])
            types.append(type)
        return types


class Cluster(EqualityBMD):

    def __init__(self, name, count, type, flavor, progress=None, sel=None,
                 bookmark=None, status=None, id=None, username=None,
                 **kwargs):
        super(Cluster, self).__init__(**kwargs)
        self.name = name
        self.count = count
        self.type = type
        self.flavor = flavor
        self.status = status
        self.id = id
        self.username = username
        self.sel = sel
        self.bookmark = bookmark
        self.progress = progress

    # Request Serializers
    def _obj_to_json(self):
        body = {
            'cluster':
            {'nodeCount': self.count,
                'name': self.name,
                'flavorId': self.flavor,
                'clusterType': self.type,
             }
        }

        return json.dumps(body)

    # Response Deserializers
    @classmethod
    def _json_to_obj(cls, serialized_str):
        '''
        @summary: Handles both the single and list version of the Cluster
        call, obviating the need for separate domain objects for "Cluster"
        and "Lists of Clusters" responses.
        '''
        json_dict = json.loads(serialized_str)
        if 'clusters' in json_dict:
            clusters = []
            for cluster in json_dict['clusters']:
                sel = ""
                bookmark = ""
                for link in cluster['links']:
                    if link['rel'] == "self":
                        sel = link['href']
                    elif link['rel'] == "bookmark":
                        bookmark = link['href']
                if 'progress' in cluster:
                    progress = cluster['progress']
                else:
                    progress = None
                cluster_dom = Cluster(cluster.get('name'),
                                      cluster.get('nodeCount'),
                                      cluster.get('clusterType'),
                                      cluster.get('flavorId'),
                                      progress,
                                      sel,
                                      bookmark,
                                      cluster.get('status'),
                                      cluster.get('id'),
                                      cluster.get('user'))
                if "fault" in cluster:
                    setattr(cluster_dom, "fault", cluster['fault'])
                clusters.append(cluster_dom)
            return clusters
        elif 'cluster' in json_dict:
            cluster = json_dict['cluster']
            sel = ""
            bookmark = ""
            for link in cluster['links']:
                if link['rel'] == "self":
                    sel = link['href']
                elif link['rel'] == "bookmark":
                    bookmark = link['href']
            if 'progress' in cluster:
                progress = cluster['progress']
            else:
                progress = None
            cluster_dom = Cluster(cluster.get('name'),
                                  cluster.get('nodeCount'),
                                  cluster.get('clusterType'),
                                  cluster.get('flavorId'),
                                  progress,
                                  sel,
                                  bookmark,
                                  cluster.get('status'),
                                  cluster.get('id'),
                                  cluster.get('user'))
            if "fault" in cluster:
                setattr(cluster_dom, "fault", cluster['fault'])
            return cluster_dom


class Resize(EqualityBMD):

    '''
    @summary:
    '''
    def __init__(self, nodeCount):
        super(Resize, self).__init__()
        self.nodeCount = nodeCount

    def _obj_to_json(self):
        body = {
            'resize':
            {'nodeCount': self.nodeCount}
        }

        return json.dumps(body)


class SSHKey(EqualityBMD):

    def __init__(self, name, key, **kwargs):
        super(SSHKey, self).__init__(**kwargs)
        self.name = name
        self.key = key


class CloudCredentials(EqualityBMD):

    def __init__(self, username, apikey=None, **kwargs):
        super(CloudCredentials, self).__init__(**kwargs)
        self.username = username
        self.apikey = apikey

    def _obj_to_json(self):
        body = {'username': self.username,
                'apikey': self.apikey
                }
        return json.dumps(body)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        cc_json = json.loads(serialized_str)
        cc_json = cc_json['cloudCredentials']
        return CloudCredentials(cc_json['username'])


class Quota(EqualityBMD):

    def __init__(self, limit, remaining, **kwargs):
        super(Quota, self).__init__(**kwargs)
        self.limit = limit
        self.remaining = remaining


class Reset(EqualityBMD):

    def _obj_to_json(self):
        body = {
            "reset": {}
        }
        return json.dumps(body)


class Limits(EqualityBMD):

    def __init__(self, tenant_id, nodeCount, vcpus, ram, disk, **kwargs):
        super(Limits, self).__init__(**kwargs)
        self.nodeCount = nodeCount
        self.vcpus = vcpus
        self.disk = disk
        self.ram = ram
        self.tenant_id = tenant_id

    def __eq__(self, other):
        if type(other) is type(self):
            if self.nodeCount.limit != other.nodeCount.limit:
                return False
            if self.vcpus.limit != other.vcpus.limit:
                return False
            if self.disk.limit != other.disk.limit:
                return False
            if self.ram.limit != other.ram.limit:
                return False
            if self.ram.limit != other.ram.limit:
                return False
            return True
        return False

    def _obj_to_json(self):
        body = {
            "limits": {
                "tenantId": self.tenant_id,
                "absolute": {
                    "nodeCount": self.nodeCount,
                    "ram": self.ram,
                    "disk": self.disk,
                    "vcpus": self.vcpus
                }
            }
        }
        return json.dumps(body)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        def limits_json_to_obj(limits_json):
            limits_json_abs = limits_json['absolute']
            if 'tenantId' in limits_json.keys():
                tenant_id = limits_json['tenantId']
            else:
                tenant_id = None
            nodeCount = Quota(limits_json_abs['nodeCount']['limit'],
                              limits_json_abs['nodeCount']['remaining'])
            vcpus = Quota(limits_json_abs['vcpus']['limit'],
                          limits_json_abs['vcpus']['remaining'])
            disk = Quota(limits_json_abs['disk']['limit'],
                         limits_json_abs['disk']['remaining'])
            ram = Quota(limits_json_abs['ram']['limit'],
                        limits_json_abs['ram']['remaining'])
            return Limits(
                tenant_id=tenant_id,
                nodeCount=nodeCount,
                vcpus=vcpus,
                disk=disk,
                ram=ram)

        if isinstance(json.loads(serialized_str)['limits'], list):
            limits = []
            for limit in json.loads(serialized_str)['limits']:
                limits.append(
                    limits_json_to_obj(limit))
            return limits
        else:
            return limits_json_to_obj(
                json.loads(serialized_str)['limits'])


class Profile(EqualityBMD):

    def __init__(self,
                 user_id=None,
                 tenant_id=None,
                 username=None,
                 password=None,
                 ssh_keys=None,
                 cloud_credentials=None,
                 **kwargs):
        super(Profile, self).__init__(**kwargs)
        self.tenant_id = tenant_id
        self.user_id = user_id
        self.username = username
        self.password = password
        self.ssh_keys = ssh_keys
        self.cloud_credentials = cloud_credentials

    def _obj_to_json(self):
        body = {"profile": {"cloudCredentials": {}}}
        if self.username is not None:
            body['profile']['username'] = self.username
        if self.password is not None:
            body['profile']['password'] = self.password
        if self.cloud_credentials is not None:
            body['profile']['cloudCredentials'] = \
                json.loads(self.cloud_credentials.serialize("json"))
        if self.ssh_keys is not None:
            ssh_keys_list = []
            for ssh_key in self.ssh_keys:
                ssh_keys_list.append(
                    {
                        "name": ssh_key.name,
                        "publicKey": ssh_key.key
                    })
            body['profile']['sshkeys'] = ssh_keys_list
        return json.dumps(body)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        def profile_json_to_obj(profile_json):
            username = profile_json['username']
            userid = profile_json['userId']
            tenant_id = profile_json['tenantId']
            cloud_cred_dict = {"cloudCredentials":
                               profile_json['cloudCredentials']}
            cloud_creds = \
                CloudCredentials.deserialize(json.dumps(cloud_cred_dict),
                                             "json")
            ssh_keys = []
            if 'sshkeys' in profile_json.keys():
                for ssh_key_dict in profile_json['sshkeys']:
                    ssh_keys.append(
                        SSHKey(
                            ssh_key_dict['name'],
                            ssh_key_dict['publicKey']
                        )
                    )
            return Profile(
                user_id=userid,
                tenant_id=tenant_id,
                username=username,
                cloud_credentials=cloud_creds,
                ssh_keys=ssh_keys)

        json_dict = json.loads(serialized_str)
        if "profiles" in json_dict:
            profiles = []
            for profile in json_dict['profiles']:
                profiles.add(profile_json_to_obj(profile))
            return profiles
        elif "profile" in json_dict:
            return profile_json_to_obj(json_dict['profile'])
