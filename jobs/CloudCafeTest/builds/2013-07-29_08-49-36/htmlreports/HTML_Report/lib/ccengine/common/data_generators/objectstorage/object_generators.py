import cStringIO
import datetime
import json
import tarfile
import math
import time
import urllib

from ccengine.clients.base_client import BaseRESTClient
from ccengine.common.tools import datagen
from ccengine.common.tools.datatools import CLOUDCAFE_TEMP_DIRECTORY
from ccengine.common.tools.filetools import get_md5_hash
from ccengine.domain.objectstorage.responses import ContainerObjectsList
from ccengine.domain.objectstorage.responses import AccountContainersList

SWIFT_CONTENT_TYPE_TEXT = 'text/plain; charset=UTF-8'
SWIFT_CONTENT_TYPE_HTML = 'text/html; charset=UTF-8'
SWIFT_CONTENT_TYPE_JSON = 'application/json; charset=UTF-8'
SWIFT_CONTENT_TYPE_XML = 'application/xml; charset=UTF-8'


def generate_data_from_pattern(pattern, size):
    """
    Generates a string given a specific pattern and size to use.
    """
    count = int(math.ceil(size / len(pattern))) + 1
    data = (pattern * count)[:size]

    return data


def generate_md5sum_from_pattern(pattern, size):
    """
    Generates a string given a specific pattern and size to use.
    """
    count = int(math.ceil(size / len(pattern)))
    data = (pattern * count)[:size]
    md5sum = get_md5_hash(data)

    return md5sum


def generate_static_large_object(
        client, slo_container_name, slo_name, manifest, slo_headers=None,
        slo_params=None):
    """
    Generats a SLO based on the manifest provieded.  The only difference
    between this manifest and the one that is uploaded to create a SLO is
    that the manifest provided to this function will not have the 'etag'
    parameter.

    @type  client: object
    @param client: use to when making the requests.
    @type  slo_container_name: string
    @param slo_container_name: name of the container to create the SLO in.  If
        the container does not exist, it will be created.
    @type  slo_name: string
    @param slo_name: name of the object to create the SLO as.
    @type  manifest: list of dictionaries
    @param manifest: dictionaries contain info on segments path
        (container/object) and size_bytes to generate and upload.
        The provided manifest should have the following format:

        [{"container_name": <container name>",
          "name": <segment name>",'
          "size_bytes": <size>,
          "headers": <optional dictionary of headers>,
          "params" : <optional dictionary of params>,
          "data_pattern" : <optional data to be used to populate the segment>},
          ...}]

        Where:
        container_name: the container to place the generated object into.
            if the container does not already exist, it will be created.
        name: the name to be given to the object representing the segment to
            be generated.
        size_bytes: The size of the object to be created.
        headers (optional): headers to be sent with the request to create
            the segment's object.
        params (optional): query parameters to be sent with the request
            to create the segment's object.
        data_pattern (optional): used to populate the segment's data.  If
            data_pattern is not provided then the md5sum of the name field
            will be used as the data pattern.
    @type  slo_headers: dictionary
    @param slo_headers: optional headers to be sent with the request
        to create the SLOs manifest object.
    @type  slo_params: dictionary
    @param slo_params: optional params to be sent with the request to
        create the SLOs manifest object.

    @rtype:  (list of dictionarys, object)
    @return: The first item in the returned tuple is a list of dictionarys
        containing the results from uploading all the segments.  The dictionary
        contains the following format:

        [{'container_name': '<segment_container_name>',
          'name': <segment_object_name>',
          'etag': '<segment_etag>',
          'responses': [<response_object>, ...]}

        Where:
        segment_container_name: The name of the container the segment was added
            to.
        segment_object_name: The name of the object that represents the
            segment.
        responses: a list of requests objects representing the responses
            returned from creating the container/

        If a non 2xx HTTP response code is encountered before the SLO can be
        created, the responses up to that point are returned.
    """
    if client is None:
        raise TypeError('client is required.')

    if slo_name is None or slo_name is '':
        raise TypeError('slo_name is required.')

    if manifest is None:
        raise TypeError('manifest is required.')

    if slo_headers is None:
        slo_headers = {}

    if slo_params is None:
        slo_params = {}

    results = {}
    slo_manifest = []
    slo_etag = ''

    for segment in manifest:
        if 'container_name' not in segment:
            raise TypeError('manifest requires container_name parameter.')
        segment_container_name = segment['container_name']

        if 'name' not in segment:
            raise TypeError('manifest requires name parameter.')
        segment_name = segment['name']

        if 'size_bytes' not in segment:
            raise TypeError('manifest requires size parameter.')
        segment_size = segment['size_bytes']

        if 'headers' in segment:
            segment_headers = segment['headers']
        else:
            segment_headers = {}

        if 'params' in segment:
            segment_params = segment['params']
        else:
            segment_params = {}

        if 'data_pattern' in segment:
            data_pattern = segment['data_pattern']
        else:
            data_pattern = get_md5_hash(segment_name)

        segment_key = '{0}/{1}'.format(segment_container_name, segment_name)

        segment_data = generate_data_from_pattern(data_pattern, segment_size)

        segment_etag = get_md5_hash(segment_data)

        segment_result = {
            'container_response': None, 'object_response': None,
            'etag': segment_etag}

        # NOTE: The manifest sent will not be the manifest stored.  The system
        #   will take the manifest, parse it, and generate a new manifest to
        #   store.
        slo_manifest.append({
            'path': segment_key,
            'etag': segment_etag,
            'size_bytes': segment_size})
        slo_etag = '{0}{1}'.format(slo_etag, segment_etag)

        if client.container_exists(segment_container_name) is False:
            response = client.create_container(segment_container_name)
            segment_result['container_response'] = response

            if response.ok is not True:
                results[segment_key] = segment_result
                return (results, None)

        response = client.set_storage_object(
            segment_container_name, segment_name, content_length=segment_size,
            headers=segment_headers, params=segment_params,
            payload=segment_data)
        segment_result['object_response'] = response

        if response.ok is not True:
            results[segment_key] = segment_result
            return (results, None)

        results[segment_key] = segment_result

    slo_data = json.dumps(slo_manifest)
    slo_size = str(len(slo_data))
    slo_params['multipart-manifest'] = 'put'
    slo_etag = get_md5_hash(slo_etag)

    if 'content-type' not in slo_headers:
        slo_headers['content-type'] = SWIFT_CONTENT_TYPE_TEXT

    slo_results = {
        'container_response': None, 'object_response': None,
        'etag': slo_etag}

    if client.container_exists(slo_container_name) is False:
        response = client.create_container(slo_container_name)
        slo_results['container_response'] = response

        if response.ok is not True:
            return (results, slo_results)

    # Send the static large object manifest
    # NOTE: The manifest sent will not be the manifest stored.  The system
    #   will take the manifest, parse it, and generate a new manifest to
    #   store.
    slo_results['object_response'] = client.set_storage_object(
        slo_container_name, slo_name, content_length=slo_size,
        payload=slo_data, headers=slo_headers, params=slo_params)

    return (results, slo_results)
