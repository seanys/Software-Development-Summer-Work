# coding=utf-8

import requests
import json
import time
import traceback
import os
import pymysql
import random
import sys
import datetime
# reload(sys)
# sys.setdefaultencoding('utf8')

def StringListSave(res):
    save_path = u"机票"
    filename = u"7月19日 上海-北京"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    path ="Airticket/"+ save_path+"/"+filename+".txt"
    
    with open(path,"w") as f:
        f.write(res)


class FlightsCtrip(object):
    ''' 获取携程机票数据 '''

    def __init__(self):
        self.init_url = 'https://flights.ctrip.com/'
        self.city_data_url = 'https://flights.ctrip.com/domestic/poi'
        self.ss = requests.session()
        self.is_init_page = self.load_init_page()
        self.sr_day=0

    def load_init_page(self):
        ''' 请求初始页面 '''
        headers = self.make_headers()
        rp = self.back_reponse(self.init_url, headers=headers)
        if not rp:
            return False
        return True

    
    def get_city_data(self, city_name):
        ''' 获取城市信息 '''
        params = {
            'channel': '1',
            'mode': '1',
            'f': '2',
            'key': city_name,
            'v': '0'           
        }
        headers = self.make_headers()
        headers['accept'] = '*/*'
        headers['referer'] = 'https://flights.ctrip.com/'
        rp = self.back_reponse(self.city_data_url, headers=headers, params=params)
        if not rp:
            return None
        city_text = rp.text
        equal_index = city_text.find('=')
        if equal_index == -1:
            return None
        city_json = city_text[equal_index+1:]
        city_data = json.loads(city_json)
        return city_data 
    
    def get_city_code(self, city_name):
        ''' 获取城市的code '''
        if not city_name:
            return None
        city_data = self.get_city_data(city_name)
        if not city_data:
            return None
        Datas = city_data.get('Data', '') 
        if (not Datas) and isinstance(Datas, list):
            return None
        Data = Datas[0]
        city_code = Data.get('Code', '')
        return city_code

    def load_flight_page(self, city1_code, city2_code, url):
        ''' 加载机票产品页面 '''
        date_str = time.strftime("%Y-%m-%d", time.localtime(time.time() + 3600 * 24 * self.sr_day))
        if (not city1_code) and (not city2_code) and (not url):
            return None 
        headers = self.make_headers()
        headers['cache-control'] = 'max-age=0'
        headers['content-type'] = 'application/x-www-form-urlencoded'
        headers['origin'] = 'https://flights.ctrip.com'
        headers['referer'] = 'https://flights.ctrip.com/'

        form_data = {
            'DCity1': city1_code, 
            'ACity1': city2_code, 
            'DDate1': date_str, 
            'DCity2': '',
            'ACity2': '',
            'DDate2': '',
            'TransitCity': '',
            'DCityName1': '(unable to decode value)',
            'DCityName2': '',
            'ACityName1': '(unable to decode value)',
            'ACityName2': '',
            'IsSingleSearchPost': 'T',
            'SEOAirlineDibitCode': '',
            'FlightSearchType': 'S',
            'ClassType': ''
        }
        rp = self.back_reponse(url, headers=headers, form_data=form_data, is_get=False)
        if not rp:
            return False
        return True
        
    def get_fligth_product(self, city1_name, city2_name,day):
        ''' 获取机票信息 '''
        #  判断是否加载首页
        is_init_page = self.is_init_page
        if not self.is_init_page:
            if not self.load_init_page():
                return None
        
        time.sleep(random.randint(2,6))

        self.sr_day=day-18

        date_str = time.strftime("%Y-%m-%d", time.localtime(time.time() + 3600 * 24 * self.sr_day))        
        cities={
            '上海':'SHA',
            '北京':'BJS',
            '西安':'SIA'
        }
        city1_code=cities[city1_name]
        city2_code=cities[city2_name]
        flight_page_url = 'https://flights.ctrip.com/booking/%s-%s-day-1.html?ddate1=%s'%(city1_code, city2_code, date_str)
        print(flight_page_url)
        if not self.load_flight_page(city1_code, city2_code, flight_page_url):
            return None
        headers = self.make_headers()
        headers['accept'] = '*/*'
        headers['content-type'] = 'application/json'
        headers['origin'] = 'https://flights.ctrip.com'
        headers['referer'] = flight_page_url 
        
        products_url = 'https://flights.ctrip.com/itinerary/api/12808/products'
        payload_data = {
            "flightWay":"Oneway",
            "classType":"ALL",
            "hasChild":False,
            # "hasBaby":False,
            "hasBaby":False,
            "searchIndex":1,
            "airportParams":[{
                "dcity":city1_code,
                "acity":city2_code,
                "dcityname":city1_name,
                "acityname":city2_name,
                "date":date_str,
                "dcityid":32,
                "acityid":1
                }]
            }
        rp = self.back_reponse(products_url, headers=headers, json_data=payload_data, is_get=False)
        if not rp:
            return None
        try:
            products_data = json.loads(rp.text)
            route_data = self.get_select_flight_data(products_data)
           
            tickts=json.dumps(route_data,ensure_ascii=False)

            StringListSave(tickts)

            db = pymysql.connect("rm-bp14fgqt2783fvljh0o.mysql.rds.aliyuncs.com","mc","Westbrook0","cAuth" )

            cursor = db.cursor()

            for route in route_data:

                print(route)
                print(route['flight']['flightNumber'])

                try:
                    # 执行直接检索
                    flight=route['flight']
                    sql="INSERT INTO flights(flightNumber,airlineName,craftTypeCode,craftTypeName,craftTypeKindDisplayName,departureDate,arrivalDate,punctualityRate,departureCityName,departureTerminalName,arrivalCityName,arrivalTerminalName) \
                    VALUES ('%s','%s',%s,'%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
                    (flight['flightNumber'],flight['airlineName'],flight['craftTypeCode'],flight['craftTypeName'],flight['craftTypeKindDisplayName'],flight['departureDate'],flight['arrivalDate'],flight['punctualityRate'],flight['departureCityName'],flight['departureTerminalName'],flight['arrivalCityName'],flight['arrivalTerminalName'])
                    cursor.execute(sql)
                    flight_id=cursor.lastrowid
                    db.commit()

                    cabins=flight['cabins']

                    # 执行插入cabin的算法
                    for cabin in cabins:
                        sql="INSERT INTO canbins(flight_id,price,seatCount,cabinClass) \
                        VALUES (%s,%s,%s,'%s')" % \
                        (flight_id,cabin['price'],cabin['seatCount'],cabin['cabinClass'])
                        # print(sql)
                        cursor.execute(sql)
                        db.commit()

                except:
                    db.rollback()

            db.close()

        except:
            return None
        return products_data 

    def get_select_flight_data(self, original_data):
        ''' 筛选飞机票数据 '''

        route_data = []
        # routeType: 路线类型; Flight(飞机直达), FlightTrain(飞机转火车)
        Flight = 'Flight'
        FlightTrain = 'FlightTrain'
        route_kw_data = 'data'
        routeList = 'routeList'
        routeType = 'routeType'
        legs = 'legs'
        legs_flight = 'flight'
        flight_keyword_list = ['flightNumber', 'airlineName', 'craftTypeCode', 'craftTypeName',\
            'craftTypeKindDisplayName', 'departureDate', 'arrivalDate', 'punctualityRate',\
            'departureAirportInfo', 'arrivalAirportInfo']
        departureAirportInfo = 'departureAirportInfo'
        arrivalAirportInfo = 'arrivalAirportInfo'
        cityName = 'cityName'
        airportName = 'airportName'
        terminal = 'terminal'
        name = 'name'
        departure_cityname = 'departureCityName'
        departure_terminalname = 'departureTerminalName'
        arrival_cityname = 'arrivalCityName'
        arrival_terminalname = 'arrivalTerminalName'
        cabins = 'cabins'
        cabins_price = 'price'
        cabins_rate = 'rate'
        cabinClass = 'cabinClass'
        '''
        cabinClass: Y(经济舱)
        cabinClass: C(公务舱)
        cabinClass: F(头等舱)
        '''
        seatecount = 'seatCount'
        childPolicy = 'childPolicy'
        babyPolicy = 'babyPolicy'
        additionalProductGroups = 'additionalProductGroups'
        additional_product = 'products'

        try:
            routeList_data = original_data[route_kw_data][routeList]
            print('route_num:', len(routeList_data))
            for route in routeList_data:
                air_data = {}
                flight = {} 
                new_cabins_list = []
                if route[routeType] == Flight:
                    legs0_data = route[legs][0]
                    air_data[routeType] = Flight
                    legs_flight_data = legs0_data[legs_flight]
                    for f_kw in flight_keyword_list:
                        if f_kw == departureAirportInfo:
                            departure_data = legs_flight_data[f_kw]
                            flight[departure_cityname] = departure_data[airportName]
                            flight[departure_terminalname] = departure_data[terminal][name]
                            continue
                        if f_kw == arrivalAirportInfo:
                            arrival_data = legs_flight_data[f_kw]
                            flight[arrival_cityname] = arrival_data[airportName]
                            flight[arrival_terminalname] = arrival_data[terminal][name]
                            continue
                        flight[f_kw] = legs_flight_data[f_kw]

                    cabins_list = legs0_data[cabins]
                    for cabin in cabins_list:
                        price_dict = {}
                        price_dict[cabins_price] = cabin[cabins_price][cabins_price]
                        price_dict[cabins_rate] = cabin[cabins_price][cabins_rate]
                        price_dict[seatecount] = cabin[seatecount]
                        price_dict[cabinClass] = cabin[cabinClass]
                        childPolicy_data = cabin.get(childPolicy, '')
                        babyPolicy_data = cabin.get(babyPolicy, '')
                        if not childPolicy_data:
                            price_dict[childPolicy + cabins_price] = childPolicy_data
                        else:
                            price_dict[childPolicy + cabins_price] = childPolicy_data[cabins_price]
                        
                        if not babyPolicy_data:
                            price_dict[babyPolicy + cabins_price] = babyPolicy_data 
                        else:
                            price_dict[babyPolicy + cabins_price] = babyPolicy_data[cabins_price]

                        new_cabins_list.append(price_dict)

                    flight[cabins] = new_cabins_list
                    air_data[legs_flight] = flight
                if routeType == FlightTrain:
                    air_data[routeType] = FlightTrain
                    pass
                route_data.append(air_data)
            return route_data 
        except:
            traceback.print_exc()
            return route_data 

    def make_headers(self):
        ''' 制作请求头 '''
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu\
                Chromium/71.0.3578.98 Chrome/71.0.3578.98 Safari/537.36'            
        }
        return headers

    def back_reponse(self, url, headers, params=None, form_data=None, json_data=None, is_get=True):
        ''' 操作requests模块 '''
        try:
            proxies = { "http": "http://47.90.73.118:3128","https":"178.32.59.233:53281"}
            if is_get:
                # rp = self.ss.get(url, headers=headers, params=params)
                rp = self.ss.get(url, headers=headers, params=params,proxies=proxies)
            else:
                # rp = self.ss.post(url, headers=headers, params=params, data=form_data, json=json_data)
                rp = self.ss.post(url, headers=headers, params=params, data=form_data, json=json_data,proxies=proxies)
            if rp.status_code == 200:
                return rp 
            else:
                None
        except:
            return None
        
if __name__ == '__main__':
    fc = FlightsCtrip()
    city1_name = u'上海'
    city2_name = u'北京'

    cities={
            '上海':'SHA',
            '北京':'BJS',
            '西安':'SIA'
        }
    
    city1_name = u'西安'
    city2_name = u'上海'    
    # i=28
    # while i< 90 :
    #     fc.get_fligth_product(city1_name, city2_name,i)
    #     time.sleep(random.randint(30,60))
    #     i=i+1

    db = pymysql.connect("rm-bp14fgqt2783fvljh0o.mysql.rds.aliyuncs.com","mc","Westbrook0","cAuth" )
    cursor = db.cursor()
    fc.get_fligth_product(city1_name, city2_name,80)



    i=19
    while i< 90 :
        real_date=i-18
        i=i+1
        cursor = db.cursor()
        date_start = time.strftime("%Y-%m-%d", time.localtime(time.time() + 3600 * 24 * real_date))
        date_end = time.strftime("%Y-%m-%d", time.localtime(time.time() + 3600 * 24 * (real_date+1)))
        # 北京-上海
        sql="SELECT * FROM flights where departureDate > '" + date_start + "' AND departureDate < '" + date_end + "' AND (arrivalCityName='虹桥国际机场' OR arrivalCityName='浦东国际机场') AND departureCityName='首都国际机场'"
        cursor.execute(sql)
        data = cursor.fetchall()
        if len(data)>0:
            sql="UPDATE available_date SET exist=1 where date='" + date_start +"' AND departureCityName='北京' AND arrivalCityName='上海'"
        cursor.execute(sql)
        db.commit()
        # 西安-上海
        sql="SELECT * FROM flights where departureDate > '" + date_start + "' AND departureDate < '" + date_end + "' AND (arrivalCityName='虹桥国际机场' OR arrivalCityName='浦东国际机场') AND departureCityName='咸阳国际机场'"
        cursor.execute(sql)
        data = cursor.fetchall()
        if len(data)>0:
            sql="UPDATE available_date SET exist=1 where date='" + date_start +"' AND departureCityName='西安' AND arrivalCityName='上海'"
        cursor.execute(sql)
        db.commit()
        # 上海-西安
        sql="SELECT * FROM flights where departureDate > '" + date_start + "' AND departureDate < '" + date_end + "' AND (departureCityName='虹桥国际机场' OR departureCityName='浦东国际机场') AND arrivalCityName='咸阳国际机场'"
        cursor.execute(sql)
        data = cursor.fetchall()
        if len(data)>0:
            sql="UPDATE available_date SET exist=1 where date='" + date_start +"' AND arrivalCityName='西安' AND departureCityName='上海'"
        cursor.execute(sql)
        db.commit()
        # 上海-北京
        sql="SELECT * FROM flights where departureDate > '" + date_start + "' AND departureDate < '" + date_end + "' AND (departureCityName='虹桥国际机场' OR departureCityName='浦东国际机场') AND arrivalCityName='首都国际机场'"
        cursor.execute(sql)
        data = cursor.fetchall()
        if len(data)>0:
            sql="UPDATE available_date SET exist=1 where date='" + date_start +"' AND arrivalCityName='北京' AND departureCityName='上海'"
        cursor.execute(sql)
        db.commit()

    db.close()
