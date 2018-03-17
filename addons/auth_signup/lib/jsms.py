#!/usr/bin/env python
# -*- coding: utf-8 -*-




import json
import time
import requests
import base64


SEND_MSG_URL = 'https://api.sms.jpush.cn/v1/codes'


class JSMSPy(object):
    """jpush's python client"""

    _sendno = None

    def __init__(self, app_key, master_secret):
        self._app_key = app_key
        self._master_secret = master_secret



    def very_code(self,phonenumber):
        base64_auth_string=base64.encodestring(self._app_key+":"+self._master_secret)
        url = 'https://api.github.com/some/endpoint'
        payload = {'mobile': phonenumber,"temp_id":1}
        headers = {'content-type': 'application/json',"Authorization":"Basic "+base64_auth_string}

        try:
            data = requests.post(SEND_MSG_URL, data=json.dumps(payload), headers=headers)
        except Exception, e:
            return dict(
                sendno=new_params['sendno'],
                errcode=-1001,
                errmsg=u'网络错误',
            )

        try:
            jdata = json.loads(data)
        except Exception, e:
            logger.error('exception occur.msg[%s], traceback[%s]' % (str(e), __import__('traceback').format_exc()))
            return dict(
                sendno=new_params['sendno'],
                errcode=-1002,
                errmsg=u'返回包解析错误',
            )

        return jdata

        # r = requests.post(SEND_MSG_URL, data=json.dumps(payload), headers=headers)
        # print r.text

