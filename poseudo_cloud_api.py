#!/usr/bin/env python
#coding=utf-8

import httplib
import urllib
import time
import md5
import re
import json

from poseudo_cloud_util import *

FORMAT = ".json"
WEBROOT = "/html/cakephp-2.3.1/object/"

class PCAPI:
  '''
  An API for PseudoCloud.
  '''

  def __init__(self, host, access_id, secret_access_key, uuid, hostname, port=80):
    self.host = host
    self.port = port
    self.access_id = access_id                   #username
    self.secret_access_key = secret_access_key   #private key used for signature.
    self.lcDevice = hostname + "@" + uuid

  def get_connection(self):
    host = ''
    port = 80
    timeout = 10
    host_port_list = self.host.split(":")
    if len(host_port_list) == 1:
      host = host_port_list[0].strip() 
    elif len(host_port_list) == 2:
      host = host_port_list[0].strip() 
      port = int(host_port_list[1].strip())

    return httplib.HTTPConnection(host=host, port=port, timeout=timeout)

  @keepDefault
  def _create_sign_for_normal_auth(self, method, object_name, headers={}):
    '''
    NOT public API
    Create the authorization for OSS based on header input.
    it should be put into "Authorization" parameter of header.

    :type method: string
    :param:one of PUT, GET, DELETE, HEAD 
    
    :type headers: dict
    :param: HTTP header

    :type object_name: string
    :param: 

    Returns:
        signature string
    '''
    auth_value = "%s:%s" % (self.access_id, get_assign(self.secret_access_key, method, object_name, headers))
    return auth_value

  @keepDefault
  def http_request(self, method, object_name, headers={}, body='', params={}):
    '''
    Send http request of operation

    :type method: string
    :param method: one of PUT, GET, DELETE, HEAD, POST

    :type bucket: string
    :param

    :type object_name: string
    :param

    :type headers: dict
    :param: HTTP header

    :type body: string
    :param

    Returns:
        HTTP Response
    '''
    #if isinstance(object_name, unicode):
    #    object_name = object_name.encode('utf-8')
    #if len(bucket) == 0:
    #    resource = "/"
    #    headers['Host'] = self.host
    #else:
    #    headers['Host'] = bucket + "." + self.host
    #    resource = "/" + bucket + "/"
    #resource = resource.encode('utf-8') + object_name + get_resource(params) 
    url_object_name = urllib.quote(object_name)
    url = WEBROOT + url_object_name + FORMAT
    #if is_ip(self.host):
    #    url = "/%s/%s" % (bucket, object_name)
    #    if len(bucket) == 0:
    #        url = "/%s" % object_name
    #    headers['Host'] = self.host
    url = append_param(url, params)
    date = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
    headers['Date'] = date
    headers['lcAuth'] = self._create_sign_for_normal_auth(method, object_name, headers) 
    conn = self.get_connection()
    conn.request(method, url, body, headers)
    response = conn.getresponse()
    return self.parse_response(response)
  
  def parse_response(self, response):
    data = response.read()
    json_re = '{"content":.+}'
    m = re.search(json_re, data)
    json_str = m.group(0) if m else '{"content":""}'
    content = json.loads(json_str)['content']
    print data
    return response.status, response.reason, content

  def set_device(self, headers):
    headers["lcDevice"] = self.lcDevice
  
  @keepDefault
  def put_object(self, object_name, content, headers={}, params={}):
    '''
    Put object to cloud.
    TODO: Support range put.

    Returns:
      [200, 'OK']           if success
      [ErrCode, ErrMsg]     if error
    '''
    method = 'PUT'
    self.set_device(headers)
		# Calculate and set MD5 Headers
    content_md5 = md5.new(content).hexdigest()
    headers["Content-MD5"] = content_md5
    status, reason, content = \
        self.http_request(method, object_name, headers, content, params)
    return status, reason, content

  @keepDefault
  def get_object(self, object_name, headers={}, params={}):
    '''
    Get object content from cloud.
    TODO: Support range get
    TODO: Support If-Modified-Since

    Returns:
      [200, content]       if success
      [304, "Not Modified"] if not modified 
      [ErrCode, ErrMsg]    if server error
    '''
    method = 'GET'
    self.set_device(headers)
    body = ''
    status, reason, content = \
        self.http_request(method, object_name, headers, body, params)
    return status, reason, content
    
  @keepDefault
  def delete_object(self, object_name, headers={}, params={}):
    '''
    Delete object.

    Returns:
      [200, 'OK']           if success
      [ErrCode, ErrMsg]    if error
    '''
    method = 'DELETE'
    self.set_device(headers)
    body = ''
    status, reason, content = \
        self.http_request(method, object_name, headers, body, params)
    return status, reason, content

  @keepDefault
  def list_objects(self, object_prefix, headers={}, params={}):
    '''
    List objects matches prefix.
    Attention: object_prefix must have the format: [a-fA-F0-9]*\*
      We will append a '*' to your prefix if it dose not contains one.
        
    Returns:
      [200, [matched objects' attributes]]           if success
        each object's attribute includes [filename, filesize, md5, lastModifiedTime]
        and the attributes will be a list of dict, 
        example: attributes = [{u'lastModifiedTime': 1365569290, u'md5': u'6f2bf1936557136f0dfc74ff40ab6385', u'filesize': 20, u'filename': u'e1/4'}, {u'lastModifiedTime': 1366290890, u'md5': u'ca111a7e55ee247056e7590b4197de3c', u'filesize': 44, u'filename': u'e2/34567'}]
        The list will be empty if no match is found.
      [ErrCode, ErrMsg]    if error
    '''
    method = 'GET'
    self.set_device(headers)
    object_prefix = object_prefix if object_prefix.endswith('*') else object_prefix + '*'
    body = ''
    status, reason, content = \
        self.http_request(method, object_prefix, headers, body, params)
    return status, reason, content
