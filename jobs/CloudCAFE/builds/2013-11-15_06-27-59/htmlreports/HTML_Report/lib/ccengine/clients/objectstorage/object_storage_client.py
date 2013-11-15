import cStringIO
import datetime
import json
import tarfile
from time import time
from time import mktime
import urllib
import hmac
from hashlib import sha1

from ccengine.clients.base_client import BaseRESTClient
from ccengine.common.tools import datagen
from ccengine.common.tools.datatools import CLOUDCAFE_TEMP_DIRECTORY
from ccengine.common.tools.filetools import get_md5_hash
from ccengine.domain.objectstorage.responses import ContainerObjectsList
from ccengine.domain.objectstorage.responses import AccountContainersList


def _deserialize(response_entity_type):
    """
    Auto-deserializes the response from any decorated client method call
    that has a 'format' key in it's 'params' dictionary argument, where
    'format' value is either 'json' or 'xml'.

    Deserializes the response into response_entity_type domain object

    response_entity_type must be a Domain Object with a <format>_to_obj()
    classmethod defined for every supported format or this won't work.
    """

    def decorator(f):
        def wrapper(*args, **kwargs):
            response = f(*args, **kwargs)
            response.request.__dict__['entity'] = None
            response.__dict__['entity'] = None
            deserialize_format = None
            if isinstance(kwargs, dict):
                if isinstance(kwargs.get('params'), dict):
                    deserialize_format = kwargs['params'].get('format')

            if deserialize_format is not None:
                response.__dict__['entity'] = \
                    response_entity_type.deserialize(
                        response.content, deserialize_format)
            return response
        return wrapper
    return decorator


class ObjectStorageAPIClient(BaseRESTClient):
    def __init__(
            self, storage_url, snet_url, auth_token, base_container_name=None,
            base_object_name=None):
        """
        """
        super(ObjectStorageAPIClient, self).__init__()

        self.storage_url = storage_url
        self.snet_url = snet_url
        self.auth_token = auth_token
        self.base_container_name = base_container_name
        self.base_object_name = base_object_name

        #Defined in BaseRESTClient init, and used by request()
        self.default_headers['X-Auth-Token'] = self.auth_token

    def __add_object_metadata_to_headers(self, metadata=None, headers=None):
        """
        Call to __build_metadata specifically for object headers
        """

        return self.__build_metadata('X-Object-Meta-', metadata, headers)

    def __add_container_metadata_to_headers(self, metadata=None, headers=None):
        """
        Call to __build_metadata specifically for container headers
        """

        return self.__build_metadata('X-Container-Meta-', metadata, headers)

    def __add_account_metadata_to_headers(self, metadata=None, headers=None):
        """
        Call to __build_metadata specifically for account headers
        """
        return self.__build_metadata('X-Account-Meta-', metadata, headers)

    def __build_metadata(self, prefix, metadata, headers):
        """
        Prepends the prefix to all keys in metadata dict, and then joins
        the metadata and header dictionaries together. When a conflict
        arises between two header keys, the key in headers wins over the
        key in metadata.

        Returns a dict composed of the provided headers and the new
        prefixed-metadata headers.

        @param prefix: Appended to all keys in metadata dict
        @type prefix: String
        @param metadata: Expects a dict with strings as keys and values
        @type metadata: Dict
        @rtype: Dict
        """
        if metadata is None:
            return headers

        headers = headers if headers is not None else {}
        metadata = metadata if metadata is not None else {}
        metadata_headers = {}

        for key in metadata:
            try:
                meta_key = ''.join([prefix, key])
            except TypeError as e:
                self.client_log.error(
                    'Non-string prefix OR metadata dict value was passed '
                    'to __build_metadata() in object_storage_client.py')
                self.client_log.exception(e)
                raise
            except:
                raise
            metadata_headers[meta_key] = metadata[key]

        return dict(metadata_headers, **headers)

    @_deserialize(ContainerObjectsList)
    def list_objects(
            self, container_name, headers=None, params=None,
            requestslib_kwargs=None):
        """
        Lists all objects in the specified container.

        If the 'format' variable is passed as part of the 'params'
        dictionary, an object representing the deserialized version of
        that format (either xml or json) will be appended to the response
        as the 'entity' attribute. (ie, response.entity)
        """
        url = '/'.join([self.storage_url, container_name])

        return self.request(
            'GET', url, headers=headers, params=params,
            requestslib_kwargs=requestslib_kwargs)

    @_deserialize(AccountContainersList)
    def list_containers(
            self, headers=None, params=None, requestslib_kwargs=None):
        """
        Lists all containers for the account.

        If the 'format' variable is passed as part of the 'params'
        dictionary, an object representing the deserialized version of
        that format (either xml or json) will be appended to the response
        as the 'entity' attribute. (ie, response.entity)
        """

        return self.request(
            'GET', self.storage_url, headers=headers, params=params,
            requestslib_kwargs=requestslib_kwargs)

    def container_exists(self, container_name):
        """
        Checks if a container exists

        @type  container_name: string
        @param container_name: the container to check for the existance of.

        @rtype:  boolean
        @return: True if the container exists, False otherwise.
        """
        if container_name is None or container_name is '':
            raise TypeError("container_name is required.")

        url = '{0}/{1}'.format(self.storage_url, container_name)

        response = self.request('HEAD', url)

        return response.ok

    def get_object_count(self, container_name):
        """
        Returns the number of objects in a container.
        """
        r = self.get_container_metadata(container_name)
        count = int(r.headers['x-container-object-count'])

        return count

    #This the correct way of creating methods so that they provide proper
    #passthrough to the underlying requests library via requestslib_kwargs
    def create_storage_object(
            self, container_name, object_name, data=None, metadata=None,
            headers=None, use_snet=False, requestslib_kwargs=None):
        """
        Creates a storage object in a container via PUT
        Optionally adds 'X-Object-Metadata-' prefix to any key in the
        metadata dictionary, and then adds that metadata to the headers
        dictionary.
        """
        headers = self.__add_object_metadata_to_headers(metadata, headers)
        storage_endpoint = self.storage_url
        if use_snet is True:
            storage_endpoint = self.snet_url

        url = '/'.join([storage_endpoint, container_name, object_name])

        return self.request(
            'PUT', url, headers=headers, data=data,
            requestslib_kwargs=requestslib_kwargs)

    def create_container(
            self, container_name, metadata=None, headers=None, use_snet=False,
            requestslib_kwargs=None):

        #Add proper prefix to metadata and add that metadata to headers
        headers = self.__add_container_metadata_to_headers(metadata, headers)

        storage_endpoint = self.storage_url
        if use_snet is True:
            storage_endpoint = self.snet_url

        url = '/'.join([storage_endpoint, container_name])

        #Make HTTP call and return result
        return self.request(
            'PUT', url, headers=headers, requestslib_kwargs=requestslib_kwargs)

    def set_storage_object_metadata(
            self, container_name, object_name, metadata, headers=None,
            params=None, use_snet=False, requestslib_kwargs=None):

        headers = self.__add_object_metadata_to_headers(metadata, headers)

        storage_endpoint = self.storage_url
        if use_snet is True:
            storage_endpoint = self.snet_url

        url = '/'.join([storage_endpoint, container_name, object_name])
        return self.request(
            'POST', url, headers=headers, params=params,
            requestslib_kwargs=requestslib_kwargs)

    def get_storage_object_metadata(
            self, container_name, object_name, headers=None, params=None,
            use_snet=False, requestslib_kwargs=None):

        storage_endpoint = self.storage_url
        if use_snet is True:
            storage_endpoint = self.snet_url

        url = '/'.join([storage_endpoint, container_name, object_name])

        return self.request(
            'HEAD', url, headers=headers, params=params,
            requestslib_kwargs=requestslib_kwargs)

    def get_storage_object(
            self, container_name, object_name, headers=None, params=None,
            prefetch=True, use_snet=False, requestslib_kwargs=None):
        """
        optional headers

        If-Match
        If-None-Match
        If-Modified-Since
        If-Unmodified-Since
        Range

        If-Match and If-None-Match check the ETag header
        200 on 'If' header success
        If none of the entity tags match, or if "*" is given and no current
        entity exists, the server MUST NOT perform the requested method, and
        MUST return a 412 (Precondition Failed) response.

        206 (Partial content) for successful range request
        If the entity tag does not match, then the server SHOULD
        return the entire entity using a 200 (OK) response
        see RFC2616

        If prefetch=False, body download is delayed until response.content is
        accessed either directly, via response.iter_content() or .iter_lines()
        """
        #Setup prefetch with proper overriding
        if requestslib_kwargs is None:
            requestslib_kwargs = {}

        # TODO(rich5317): check requests version for prefetch vs stream

        if requestslib_kwargs.get('prefetch') is None:
            requestslib_kwargs['prefetch'] = prefetch

        storage_endpoint = self.storage_url
        if use_snet is True:
            storage_endpoint = self.snet_url

        url = '/'.join([storage_endpoint, container_name, object_name])
        return self.request(
            'GET', url, headers=headers, params=params,
            requestslib_kwargs=requestslib_kwargs)

    def get_container_options(
            self, container_name, headers=None, use_snet=False,
            requestslib_kwargs=None):

        storage_endpoint = self.storage_url
        if use_snet is True:
            storage_endpoint = self.snet_url

        url = ''.join([storage_endpoint, '/', container_name])

        return self.request(
            'OPTIONS', url, headers=headers,
            requestslib_kwargs=requestslib_kwargs)

    def get_crossdomain_xml(
            self, headers=None, params=None, requestslib_kwargs=None):
        # TODO(rich5317): This method call contains test-specific data and
        #   should be refactored to take that as a paramater.  This is also
        #   probably better implemented as a provider or tool method.

        data = self.storage_url.rsplit('/')
        url = data[0] + '//' + data[2] + '/crossdomain.xml'

        return self.request(
            'GET', url, headers=headers, params=params,
            requestslib_kwargs=requestslib_kwargs)

    def retrieve_account_metadata(
            self, use_snet=False, requestslib_kwargs=None):

        storage_endpoint = self.storage_url
        if use_snet is True:
            storage_endpoint = self.snet_url

        return self.request(
            'HEAD', storage_endpoint, requestslib_kwargs=requestslib_kwargs)

    def update_container(
            self, container_name, headers=None, use_snet=False,
            requestslib_kwargs=None):
        storage_endpoint = self.storage_url
        if use_snet is True:
            storage_endpoint = self.snet_url

        url = '/'.join([storage_endpoint, container_name])

        return self.request(
            'PUT', url, headers=headers, requestslib_kwargs=requestslib_kwargs)

    def delete_container(
            self, container_name, headers=None, use_snet=False,
            requestslib_kwargs=None):
        storage_endpoint = self.storage_url
        if use_snet is True:
            storage_endpoint = self.snet_url

        url = '/'.join([storage_endpoint, container_name])

        return self.request(
            'DELETE', url, headers=headers,
            requestslib_kwargs=requestslib_kwargs)

    def get_container_metadata(
            self, container_name, headers=None, use_snet=False,
            requestslib_kwargs=None):
        storage_endpoint = self.storage_url
        if use_snet is True:
            storage_endpoint = self.snet_url

        url = '/'.join([storage_endpoint, container_name])

        return self.request(
            'HEAD', url, headers=headers,
            requestslib_kwargs=requestslib_kwargs)

    def set_container_metadata(
            self, container_name, metadata, headers=None, use_snet=False,
            requestslib_kwargs=None):
        headers = self.__add_container_metadata_to_headers(metadata, headers)

        storage_endpoint = self.storage_url
        if use_snet is True:
            storage_endpoint = self.snet_url

        url = '/'.join([storage_endpoint, container_name])

        return self.request(
            'POST', url, headers=headers,
            requestslib_kwargs=requestslib_kwargs)

    def delete_storage_object(
            self, container_name, object_name, headers=None, use_snet=False,
            requestslib_kwargs=None):

        storage_endpoint = self.storage_url
        if use_snet is True:
            storage_endpoint = self.snet_url

        url = '/'.join([storage_endpoint, container_name, object_name])

        return self.request(
            'DELETE', url, headers=headers,
            requestslib_kwargs=requestslib_kwargs)

    def set_storage_object(
            self, container_name, object_name, content_length='0',
            content_type=None, chunked=False, headers=None, params=None,
            payload=None, use_snet=False):
        """
        TODO: 1) Replace all instances of the use of this method with calls to
                 create_storage_object()

              2) Modify create_storage_object() to satisfy all requirements

        required headers:
        Content-Length
        Content-Type

        optional headers:
        X-Object-Meta
        ETag
        X-Delete-At
        X-Delete-After
        """
        hdrs = {}
        hdrs['X-Auth-Token'] = self.auth_token

        # TODO(rich5317): This needs to be refactored.
        if chunked is False:
            hdrs['Content-Length'] = str(content_length)
            if content_type is not None:
                hdrs['Content-Type'] = content_type
        else:
            #tmp_hdrs['Content-Type'] = content_type
            hdrs['Transfer-Encoding'] = 'chunked'

        if headers is not None:
            hdrs.update(headers)

        storage_endpoint = self.storage_url
        if use_snet is True:
            storage_endpoint = self.snet_url

        object_string = '/'.join(
            [storage_endpoint, container_name, object_name])

        return self.put(
            object_string, headers=hdrs, params=params, data=payload)

    def chunked_transfer(
            self, container_name, object_name, payload, headers=None):
        """
        The 'chunked' transfer-coding MUST NOT be applied more
        than once to a message-body RFC 2616 section 3.6
        Each chunk starts with the number of octets of the data
        and a terminating CRLF sequence, followed by the chunk data.
        The chunk is terminated by CRLF.
        The last-chunk is a regular chunk, with the exception that its length
        is zero.
        """
        # TODO(rich5317): This needs to be fixed. it works but its not correct
        #   a connection must be made and chunks must be sent one by one until
        #   the end token is seen.

        end_token = '0\r\n\r\n'
        body = ''
        hdrs = {}
        hdrs['X-Auth-Token'] = self.auth_token
        hdrs['Transfer-Encoding'] = 'chunked'
        if headers is not None:
            hdrs.update(headers)

        for chunk in payload:
            if chunk == '0':
                body = ''.join([body, end_token])
            else:
                body = ''.join([body, '%X\r\n%s\r\n' % (len(chunk), chunk)])

        object_string = '/'.join(
            [self.storage_url, container_name, object_name])

        return self.put(object_string, headers=hdrs, data=body)

    def copy_storage_object(
            self, src_container, src_object, dst_container=None,
            dst_object=None, headers=None, use_snet=False):
        hdrs = {}
        hdrs['X-Auth-Token'] = self.auth_token

        if dst_container is None:
            dst_container = src_container

        if dst_object is None:
            dst_object = src_object

        tmp = '/'.join([dst_container, dst_object])
        destination = ''.join(['/', tmp])

        hdrs['Destination'] = destination
        if headers is not None:
            hdrs.update(headers)

        storage_endpoint = self.storage_url
        if use_snet is True:
            storage_endpoint = self.snet_url

        object_string = '/'.join(
            [storage_endpoint, src_container, src_object])

        return self.copy(object_string, headers=hdrs)

    def putcopy_storage_object(
            self, src_container, src_object, dst_container=None,
            dst_object=None, headers=None, use_snet=False):
        hdrs = {}
        hdrs['X-Auth-Token'] = self.auth_token
        hdrs['Content-Length'] = '0'

        if dst_container is None:
            dst_container = src_container

        if src_object is None:
            dst_object = src_object

        tmp = '/'.join([src_container, src_object])
        src = ''.join(['/', tmp])

        hdrs['X-Copy-From'] = src
        if headers is not None:
            hdrs.update(headers)

        storage_endpoint = self.storage_url
        if use_snet is True:
            storage_endpoint = self.snet_url

        object_string = '/'.join(
            [storage_endpoint, dst_container, dst_object])

        return self.put(object_string, headers=hdrs)

    def __generate_name(
            self, prefix='', infix='', postfix='', separator='_',
            include_date=True, date_separator='/', include_random=True):
        # prefix date infix random postfix
        tokens = []

        if prefix is not '':
            tokens.append(prefix)

        if include_date is True:
            d = datetime.datetime.now()
            token = []
            token.append(str(d.year))
            token.append(str(d.month))
            token.append(str(d.day))
            token.append(str(d.hour))
            token.append(str(d.minute))
            tokens.append(date_separator.join(token))

        if infix is not '':
            tokens.append(infix)

        if include_random is True:
            tokens.append(datagen.random_string())

        if postfix is not '':
            tokens.append(postfix)

        name = separator.join(tokens)
        return name

    def generate_unique_container_name(
            self, prefix='', infix='', postfix='', separator='_',
            include_date=True, date_separator='-', include_base=True,
            include_random=True):
        if include_base is True:
            tokens = []
            tokens.append(self.base_container_name)
            if infix is not '':
                tokens.append(infix)
            infix = separator.join(tokens)

        name = self.__generate_name(
            prefix, infix, postfix, separator, include_date, date_separator,
            include_random)

        return name

    def generate_unique_object_name(
            self, prefix='', infix='', postfix='', separator='_',
            include_date=True, date_separator='-', include_base=True,
            include_random=True):
        # prefix date base infix random postfix

        if include_base is True:
            tokens = []
            tokens.append(self.base_object_name)
            if infix is not '':
                tokens.append(infix)
            infix = separator.join(tokens)

        name = self.__generate_name(
            prefix, infix, postfix, separator, include_date, date_separator,
            include_random)

        return name

    def _delete_container(self, container_name):
        params = {'format': 'json'}
        r = self.list_objects(container_name, params=params)
        try:
            json_data = json.loads(r.content)
            for entry in json_data:
                self.delete_storage_object(container_name, entry['name'])
        except Exception:
            pass

        return self.delete_container(container_name)

    def force_delete_containers(self, container_list):
        for container_name in container_list:
            return self._delete_container(container_name)

    def create_private_container(self, container_name, access_logging=True):
        r = self.create_container(container_name)
        return r

    def extract_archive(
            self, data, data_format='tar', container_name=None, headers=None,
            requestslib_kwargs=None):
        """
        Uploads a archive file to Swift for the files to be extracted as
        objects.

        @type  data: string
        @param data: The data read in from a archive file.
        @type  data_format: string
        @param data_format: The format of the archive (tar|tar.gz|tar.bz2)
        @type  data_format: string
        @param data_format: The container to extract the archive to.
            If None, containers will be created based on the first directory
            of the file listing.

        @rtype:  object
        @return: The requests response object returned from the call.
        """
        url = self.storage_url
        if container_name is not None:
            url = '{0}/{1}'.format(url, container_name)
        params = {'extract-archive': data_format}

        r = self.request(
            'PUT', url, data=data, params=params, headers=headers,
            requestslib_kwargs=requestslib_kwargs)

        return r

    def bulk_delete(self, targets, headers=None, requestslib_kwargs=None):
        """
        Deletes container/objetcs from an account.

        @type  targets: list of strings
        @param targets: A list of the '/container/object' or '/container' to be
            bulk deleted.  Note, bulk delete will not remove containers that
            have objects in them, and there is limit of 1000 containers/objects
            per delete.

        @rtype:  object
        @return: The requests response object returned from the call.
        """
        if headers is None:
            headers = {}

        url = '{0}{1}'.format(self.storage_url, '?bulk-delete')
        data = '\n'.join([urllib.quote(x) for x in targets])
        headers['content-type'] = 'text/plain'

        return self.request(
            'DELETE', url, data=data, headers=headers,
            requestslib_kwargs=requestslib_kwargs)

    def create_bulk_objects(
            self, container_name, objects, headers=None,
            requestslib_kwargs=None):
        """
        Bulk creates objects in a container.  Each object's data will be the
        md5sum of the object's name.

        @type  container_name: strings
        @param container_name: The name of the container to create the objects
            in.

        @rtype:  boolean
        @return: Returns true if the opperation was successful, and False
            otherwise.
        """
        if container_name is None or container_name is '':
            raise TypeError("container_name is required.")

        archive_name = 'bulk_objects.tar.gz'
        archive_dir = CLOUDCAFE_TEMP_DIRECTORY
        archive_filename = '{0}/{1}'.format(archive_dir, archive_name)
        archive = tarfile.open(archive_filename, 'w:gz')

        for object_name in objects:
            object_data = get_md5_hash(object_name)
            object_size = len(object_data)
            object_time = int(mktime(datetime.datetime.now().timetuple()))

            object_buffer = cStringIO.StringIO(object_data)
            object_buffer.seek(0)

            object_info = tarfile.TarInfo(name=object_name)
            object_info.size = object_size
            object_info.mtime = object_time

            archive.addfile(tarinfo=object_info, fileobj=object_buffer)

        archive.close()
        archive_file = open(archive_filename, 'r')
        archive_data = archive_file.read()
        archive_file.close()

        response = self.extract_archive(
            archive_data, data_format='tar.gz', container_name=container_name,
            headers=headers, requestslib_kwargs=requestslib_kwargs)

        return response.ok

    def set_account_temp_url_key(self, headers=None, requestslib_kwargs=None):
        """
        6.1.1
        """
        return self.post(self.storage_url, headers=headers)

    def create_temp_url(self, method, container, obj, seconds, key,
                        headers=None, requestslib_kwargs=None):
        """
        6.2
        """
        method = method.upper()
        base_url = '{0}/{1}/{2}'.format(self.storage_url, container, obj)
        account_hash = self.storage_url.split('/v1/')[1]
        object_path = '/v1/{0}/{1}/{2}'.format(account_hash, container, obj)
        seconds = int(seconds)
        expires = int(time() + seconds)
        hmac_body = '{0}\n{1}\n{2}'.format(method, expires, object_path)
        sig = hmac.new(key, hmac_body, sha1).hexdigest()
        temp_url = '{0}?temp_url_sig={1}&temp_url_expires={2}'.format(
            base_url, sig, expires)

        return temp_url

    def temp_url_get(self, url, file_name=None):
        if file_name is not None:
            url = '{0}&filename={1}'.format(url, file_name)

        return self.get(url)

    def temp_url_put(self, url):
        return self.put(url)
