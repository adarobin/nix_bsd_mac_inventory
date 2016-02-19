# -*- coding: utf-8 -*-
import sys
import requests
import base64

try:
    requests.packages.urllib3.disable_warnings()
except AttributeError:
    pass

# To upload, or not to upload, question is now?
DRY_RUN = False


class Rest():
    def __init__(self, BASE_URL, USERNAME, SECRET, DEBUG):
        self.base_url   = BASE_URL
        self.username   = USERNAME
        self.password   = SECRET
        self.debug      = DEBUG
        self.headers    = {
                'Authorization': 'Basic ' + base64.b64encode(self.username + ':' + self.password),
                'Content-Type': 'application/x-www-form-urlencoded'
            }

    def uploader(self, data, url):
            payload = data
            r = requests.post(url, data=payload, headers=self.headers, verify=False)
            msg =  unicode(payload)
            if self.debug:
                print msg
            msg = 'Status code: %s' % str(r.status_code)
            print msg
            msg = str(r.text)
            if self.debug:
                print msg
            return r.json()

    def fetcher(self, url):
        r   = requests.get(url, headers=self.headers, verify=False)
        status_code = r.status_code

        if status_code == 200:
            if self.debug:
                msg = '%d\t%s' % (status_code, str(r.text))
                print msg
            return r.json()
        else:
            return status_code

    def deleter(self, url):
        r   = requests.delete(url, headers=self.headers, verify=False)
        status_code = r.status_code
        if status_code == 200:
            if self.debug:
                msg = '%d\t%s' % (status_code, str(r.text))
                print msg
            return r.json()
        else:
            return status_code
        
    def post_device(self, data):
        if DRY_RUN == False:
            url = self.base_url+'/api/device/'
            msg =  '\r\nPosting data to %s ' % url
            print msg
            result = self.uploader(data, url)
            return result

    def post_multinodes(self, data):
        if DRY_RUN == False:
            url = self.base_url+'/api/1.0/multinodes/'
            msg =  '\r\nPosting multidata to %s ' % url
            print msg
            self.uploader(data, url)

    def post_ip(self, data):
        if DRY_RUN == False:
            url = self.base_url+'/api/ip/'
            msg =  '\r\nPosting IP data to %s ' % url
            print msg
            self.uploader(data, url)

    def post_mac(self, data):
        if DRY_RUN == False:
            url = self.base_url+'/api/1.0/macs/'
            msg = '\r\nPosting MAC data to %s ' % url
            print msg
            self.uploader(data, url)

    def post_parts(self, data):
        if DRY_RUN == False:
            url = self.base_url+'/api/1.0/parts/'
            msg = '\r\nPosting HDD parts to %s ' % url
            print msg
            self.uploader(data, url)

    def get_device_by_name(self, name):
        if DRY_RUN == False:
            url = self.base_url + '/api/1.0/devices/name/%s/?include_cols=ip_addresses' % name
            msg = '\r\nFetching IP addresses for device:  %s ' % name
            print msg
            response = self.fetcher(url)
            if isinstance(response, dict) and 'ip_addresses' in response:
                fetched_ips = [x['ip'] for x in response['ip_addresses'] if 'ip' in x]
                return fetched_ips

    def delete_ip(self, ip):
        if DRY_RUN == False:
            url =self.base_url+ '/api/1.0/ips/?ip=%s' % ip
            response = self.fetcher(url)
            ip_ids = [x['id'] for x in response['ips']]
            for ip_id in ip_ids:
                url = self.base_url + '/api/1.0/ips/%s' % ip_id
                response = self.deleter(url)








