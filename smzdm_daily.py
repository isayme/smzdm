#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
import requests
import re

SMZDM_USERNAME = '' # username or email
SMZDM_PASSWORD = '' # password

class SMZDMDailyException(Exception):
    def __init__(self, req):
        self.req = req
    
    def __str__(self):
        return str(req)
    
class SMZDMDaily(object):
    BASE_URL = 'http://www.smzdm.com'
    LOGIN_URL = BASE_URL + '/user/login/jsonp_check'
    CHECKIN_URL = BASE_URL + '/user/qiandao/jsonp_checkin'
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()
        
    def checkin(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:20.0) Gecko/20100101 Firefox/20.0',
            'Host': 'www.smzdm.com',
        }
        
        params = {
            'user_login': self.username,
            'user_pass': self.password,
        }
        
        r = self.session.get(self.BASE_URL, headers=headers)
        
        # 处理值得买防爬虫机制
        if r.status_code == 521:
            # find cookie
            m = re.findall(r'push\("([^"]+)"\)', r.text)
            cookies = dict(__jsl_clearance=''.join(m))
            r = self.session.get(self.LOGIN_URL, params=params, cookies=cookies, headers=headers)

        if r.status_code != 200:
            raise SMZDMDailyException(r)
        
        r = self.session.get(self.CHECKIN_URL, headers=headers, cookies=cookies)
        if r.status_code != 200:
            raise SMZDMDailyException(r)
            
        data = r.text[1:-1]
        jdata = json.loads(data)
        
        return jdata
        
if __name__ == '__main__':
    try:
        smzdm = SMZDMDaily(SMZDM_USERNAME, SMZDM_PASSWORD)
        result = smzdm.checkin()
    except SMZDMDailyException as e:
        print e
    except Exception as e:
        print e
    else:
        print result
        
