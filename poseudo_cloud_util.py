#!/usr/bin/env python
#coding=utf-8

import urllib
import base64
import hmac
from hashlib import sha1 as sha
import hashlib
import md5
import copy

DEBUG = False 

def keepDefault(f):
  defArgs = f.__defaults__          
  def keeper(*args,**kwArgs):      
    f.__defaults__ = copy.deepcopy(defArgs)
    return f(*args,**kwArgs)
  keeper.__name__ = f.__name__
  return keeper

@keepDefault
def get_assign(secret_access_key, method, object_name, headers = {}, result = []):
  '''
  Create the authorization for OSS based on header input.
  You should put it into "Authorization" parameter of header.
  '''
  content_md5 = ""
  content_type = ""
  date = ""
  canonicalized_headers = ""
  #if DEBUG:
  #  print "secret_access_key", secret_access_key
  content_md5 = safe_get_element('Content-MD5', headers)
  content_type = safe_get_element('Content-Type', headers)
  date = safe_get_element('Date', headers)
  tmp_headers = headers
  if len(tmp_headers) > 0:
    x_header_list = tmp_headers.keys() 
    x_header_list.sort()
    for k in x_header_list: 
      canonicalized_headers += k + ":" + tmp_headers[k] + "\n"
  
  string_to_sign = method + "\n" + content_md5.strip() + "\n" + content_type + "\n" + date + "\n" + canonicalized_headers + object_name
  result.append(string_to_sign)
  if DEBUG:
    #print "method:%s, content_md5:%s, content_type:%s, data:%s, canonicalized_headers:%s, object_name:%s"\
		#		% (method, content_md5, content_type, date, canonicalized_headers, object_name)
    print "string_to_sign", string_to_sign, "string_to_sign_size", len(string_to_sign)
  
  h = hmac.new(secret_access_key, string_to_sign, sha)
  #result = hmac.new(secret_access_key, string_to_sign, hashlib.sha256).hexdigest()

  return base64.encodestring(h.digest()).strip()

def safe_get_element(name, container):
  for k, v in container.items():
    if k.strip().lower() == name.strip().lower():
      return v
  return ""


def append_param(url, params):
	'''
	convert the parameters to query string of URI.
	'''
	l = []
	for k,v in params.items():
		k = k.replace('_', '-')
		if  k == 'maxkeys':
			k = 'max-keys'
		if isinstance(v, unicode):
			v = v.encode('utf-8')
		if v is not None and v != '':
			l.append('%s=%s' % (urllib.quote(k), urllib.quote(str(v))))
		elif k == 'acl':
			l.append('%s' % (urllib.quote(k)))
		elif v is None or v == '':
			l.append('%s' % (urllib.quote(k)))
	if len(l):
		url = url + '?' + '&'.join(l)
	return url

