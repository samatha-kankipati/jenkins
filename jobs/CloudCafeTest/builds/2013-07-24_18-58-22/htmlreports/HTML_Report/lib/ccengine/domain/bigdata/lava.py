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

    def _obj_to_json(self):
        body = {"name": self.name,
                "key": self.key}
        return json.dumps(body)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        ssh_keys = []
        for record in json_dict['sshkeys']:
            key = SSHKey(record['name'], record['key'])
            ssh_keys.append(key)
        if len(ssh_keys) >= 1:
            return ssh_keys
        else:
            return None


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


class Limits(EqualityBMD):
    def __init__(self, nodeCount, vcpus, ram, disk, **kwargs):
        super(Limits, self).__init__(**kwargs)
        self.nodeCount = nodeCount
        self.vcpus = vcpus
        self.disk = disk
        self.ram = ram

    @classmethod
    def _json_to_obj(cls, serialized_str):
        limits_json = json.loads(serialized_str)['limits']['absolute']
        nodeCount = Quota(limits_json['nodeCount']['limit'],
                          limits_json['nodeCount']['remaining'])
        vcpus = Quota(limits_json['vcpus']['limit'],
                      limits_json['vcpus']['remaining'])
        disk = Quota(limits_json['disk']['limit'],
                     limits_json['disk']['remaining'])
        ram = Quota(limits_json['ram']['limit'],
                    limits_json['ram']['remaining'])
        return Limits(nodeCount=nodeCount,
                      vcpus=vcpus,
                      disk=disk,
                      ram=ram)


class Profile(EqualityBMD):
    def __init__(self,
                 email=None,
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
        self.email = email

    def _obj_to_json(self):
        body = {"profile": {"cloudCredentials": {}}}
        if self.email is not None:
            body['profile']['email'] = self.email
        if self.username is not None:
            body['profile']['username'] = self.username
        if self.password is not None:
            body['profile']['password'] = self.password
        if self.cloud_credentials is not None:
            body['profile']['cloudCredentials'] = \
                json.loads(self.cloud_credentials.serialize("json"))
        return json.dumps(body)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        if "profiles" in json_dict:
            profiles = []
            for profile in json_dict['profiles']:
                if 'email' in profile.keys():
                    email = profile['email']
                userid = profile['user_id']
                tenant_id = profile['tenant_id']
                cloud_cred_dict = {"cloudCredentials":
                                   profile['cloudCredentials']}
                cloud_creds = \
                    CloudCredentials.deserialize(json.dumps(cloud_cred_dict),
                                                 "json")
                cur_profile = Profile(email=email,
                                      user_id=userid,
                                      tenant_id=tenant_id,
                                      usPername=username,
                                      cloud_credentials=cloud_creds)
                profiles.add(cur_profile)
            return profiles
        elif "profile" in json_dict:
            profile = json_dict['profile']
            email = None
            if 'email' in profile.keys():
                email = profile['email']
            username = profile['username']
            cloud_cred_dict = {"cloudCredentials":
                               profile['cloudCredentials']}
            cloud_creds = \
                CloudCredentials.deserialize(json.dumps(cloud_cred_dict),
                                             "json")
            return Profile(email=email,
                           username=username,
                           cloud_credentials=cloud_creds)
