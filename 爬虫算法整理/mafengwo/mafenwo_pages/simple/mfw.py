import scrapy
import re
import bs4
import json


class MaFengWo():
    name = "mafengwo"
                
    def back_reponse(self, url, headers, params=None, form_data=None, json_data=None, is_get=True):
        ''' 操作requests模块 '''
        try:
            proxies = { "http": "http://47.90.73.118:3128","https":"178.32.59.233:53281"}
            if is_get:
                rp = self.ss.get(url, headers=headers, params=params)
                # rp = self.ss.get(url, headers=headers, params=params,proxies=proxies)
            else:
                rp = self.ss.post(url, headers=headers, params=params, data=form_data, json=json_data)
                # rp = self.ss.post(url, headers=headers, params=params, data=form_data, json=json_data,proxies=proxies)
            if rp.status_code == 200:
                return rp 
            else:
                None
        except:
            return None
    
    def make_headers(self):
        ''' 制作请求头 '''
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'upgrade-insecure-requests': '1',
            # 'host':'www.mafengwo.cn',
            # 'cookie':'__jsluid_h=75a9b01e4ba3bf2cde2c1bab5386a927; PHPSESSID=gm129tg3g3t49n0ci0144ud1d7; mfw_uuid=5d3dc24a-a027-6350-baf3-a30eec237088; oad_n=a%3A3%3A%7Bs%3A3%3A%22oid%22%3Bi%3A1029%3Bs%3A2%3A%22dm%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A2%3A%22ft%22%3Bs%3A19%3A%222019-07-28+23%3A42%3A02%22%3B%7D; __mfwc=direct; uva=s%3A91%3A%22a%3A3%3A%7Bs%3A2%3A%22lt%22%3Bi%3A1564328544%3Bs%3A10%3A%22last_refer%22%3Bs%3A23%3A%22http%3A%2F%2Fwww.mafengwo.cn%2F%22%3Bs%3A5%3A%22rhost%22%3BN%3B%7D%22%3B; __mfwurd=a%3A3%3A%7Bs%3A6%3A%22f_time%22%3Bi%3A1564328544%3Bs%3A9%3A%22f_rdomain%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A6%3A%22f_host%22%3Bs%3A3%3A%22www%22%3B%7D; __mfwuuid=5d3dc24a-a027-6350-baf3-a30eec237088; __jsluid_s=c5625848645afe3b0b3e83338c391df7; __omc_chl=; __omc_r=; __mfwlv=1564382593; __mfwvn=5; __mfwa=1564328544334.76626.7.1564382593458.1564385423322; ad_hide=1; ad_close_num=1; __mfwb=fbb55a591893.11.direct; __mfwlt=1564387431',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu\
                Chromium/71.0.3578.98 Chrome/71.0.3578.98 Safari/537.36'            
        }
        return headers

    def get_test(self):

        url='https://www.mafengwo.cn/travel-scenic-spot/mafengwo/10065.html' 

        headers = self.make_headers()
        headers['accept'] = '*/*'
        headers['content-type'] = 'application/json'
        headers['origin'] = 'https://www.mafengwo.cn'
        headers['referer'] = url

        city_load_data = {
            "mddid": 10065,
            "pageid": "mdd_index",
            "sort": 1,
            "cost": 0,
            "days": 0,
            "month": 0,
            "tagid": 0,
            "page": 3
            # "_ts": 1564387444589,
            # "_sn": 'fba1e40d45'
        }

        print("开始请求")
        rp = self.back_reponse("https://www.mafengwo.cn/gonglve/ajax.php?act=get_travellist", headers=headers, json_data=city_load_data)

        print("输出请求结果")
        print(rp)

        if not rp:
            print("请求失败")
            return None
        try:
            data = json.loads(rp.text)
            print(data)
        except:
            return None
        return data 

        
if __name__ == '__main__':
    mfw = MaFengWo()
    mfw.get_test()
