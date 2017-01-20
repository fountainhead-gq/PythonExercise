#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os, time, sys
from qiniu import Auth, put_file
from ctypes import *
from datetime import datetime


access_key = '******'  # Access key'
secret_key = '******'  # Secret Key

bucket_name = 'blog'  # 七牛空间名
url = "http://******.com1.z0.glb.clouddn.com"  # 七牛域名

q = Auth(access_key, secret_key)


# upload picture to qiniu
def upload_qiniu(path):
    dirname, filename = os.path.split(path)
    key = 'markdown/%s' % filename  # 指定文件夹，上传到文件夹markdown
    token = q.upload_token(bucket_name, key)
    ret, info = put_file(token, key, path, check_crc=True)
    return ret != None and ret['key'] == key


if __name__ == "__main__":
    path = sys.argv[1]
    ret = upload_qiniu(path)

    if ret:
        filename = os.path.split(path)[1]  # picture's name
        img_format = filename.split('.', 1)  # [img_name, img_format]
        markdown_url = "![%s](%s/%s)" % (img_format[0], url,  "markdown/"+filename)
        ahk = cdll.AutoHotkey   # load AutoHotkey
        ahk.ahktextdll("")  # start script in persistent mode (wait for action)
        while not ahk.ahkReady():  # Wait for AutoHotkey.dll to start
            time.sleep(0.01)
        ahk.ahkExec(u"clipboard = %s" % markdown_url)
    else:
        print("图片上传失败!!")
