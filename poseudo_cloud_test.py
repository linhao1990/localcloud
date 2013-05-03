#!/usr/bin/env python
#coding=utf8

from poseudo_cloud_api import *

HOST="localhost"
ACCESS_ID = "linhao"
SECRET_ACCESS_KEY = "linhao_passwd"
HOSTNAME = "linhao-Lab"
UUID = "c3d81ebe-3daa-4864-b753-526e536cb9cb" 

if __name__ == "__main__":
  if len(ACCESS_ID) == 0 or len(SECRET_ACCESS_KEY) == 0:
    print "Please make sure ACCESS_ID and SECRET_ACCESS_KEY are correct in ", __file__ , ", init are empty!"
    exit(0)
  pc = PCAPI(HOST, ACCESS_ID, SECRET_ACCESS_KEY, UUID, HOSTNAME)
  ############################################## 
  object_name = 'e234567'
  object_content = 'Hi, this is the first file of poseudo cloud.'
  
  # Test for put
  status, reason, content = pc.put_object(object_name, object_content)
  print status, reason, content 

  # Test for get
  status, reason, content = pc.get_object(object_name)
  print status, reason, content 
  
  status, reason, content = pc.get_object('e123')
  print status, reason, content 

  status, reason, attributes = pc.list_objects("e")
  print status, reason, attributes

  status, reason, message = pc.delete_object(object_name)
  print status, reason, message
  
  status, reason, attributes = pc.list_objects("e")
  print status, reason, attributes

  status, reason, attributes = pc.list_objects("e23")
  print status, reason, attributes
  
  # Test for put
  status, reason, content = pc.put_object(object_name, object_content)
  print status, reason, content 

  # Test for if-modified-since
#  timeStr  = "Sat, 20 Apr 2013 22:15:18 +0800"
#  for attribute in attributes:
#    if attribute["filename"] == object_name:
#      lastModifiedTime = attribute["lastModifiedTime"]
#  headers = {}
#  headers["lcIfModifiedSince"] = timeStr 
#  status, reason, content = pc.get_object(object_name, headers)
#  print status, reason, content
  # Test for range get 
  headers = {}
  headers["lcRange"] = "bytes=0-10"
  status, reason, content = pc.get_object(object_name, headers)
  print status, reason, content

  headers = {}
  headers["lcRange"] = "bytes=10-20"
  status, reason, content = pc.get_object(object_name, headers)
  print status, reason, content
  
  headers = {}
  headers["lcRange"] = "bytes=10-"
  status, reason, content = pc.get_object(object_name, headers)
  print status, reason, content
  
  headers = {}
  headers["lcRange"] = "bytes=-20"
  status, reason, content = pc.get_object(object_name, headers)
  print status, reason, content

  #Test for range put
  object_name = 'f234567'
  headers = {}
  headers["Offset"] = "5";
  status, reason, content = pc.put_object(object_name, "xxxxx", headers)
  print status, reason, content

  status, reason, content = pc.get_object(object_name)
  print status, reason, content
  
  headers = {}
  headers["Offset"] = "0";
  status, reason, content = pc.put_object(object_name, "yyyyy", headers)
  print status, reason, content

  status, reason, content = pc.get_object(object_name)
  print status, reason, content
  
  headers = {}
  headers["Offset"] = "7";
  status, reason, content = pc.put_object(object_name, "zzzzz", headers)
  print status, reason, content

  status, reason, content = pc.get_object(object_name)
  print status, reason, content
