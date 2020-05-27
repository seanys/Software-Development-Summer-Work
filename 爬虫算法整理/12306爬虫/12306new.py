import requests
import json
import time
import random

# 关闭https证书验证警告
requests.urllib3.disable_warnings()
from stations import stations_dict
from cities import cities_dict#城市编号
from city import station_of_city
from no import train_list

# 反转k，v形成新的字典
code_dict = {v: k for k, v in stations_dict.items()}
cities_dict2 = {v: k for k, v in cities_dict.items()}

# def query_train_detail(train_code,from_station_code,to_station_code):
#     print(0)
#     date='2018-12-22'
#     url = (
#         'https://kyfw.12306.cn/otn/leftTicket/query?'
#         'leftTicketDTO.train_date={}&'
#         'leftTicketDTO.from_station={}&'
#         'leftTicketDTO.to_station={}&'
#         'purpose_codes=ADULT'
#     ).format(date, from_station_code, to_station_code)
#     print(url)
#     r = requests.get(url, verify=False)
#     raw_trains = r.json()['data']['result']
#     for raw_train in raw_trains:
#         print(1)
#         data_list = raw_train.split('|')
#         train_n = data_list[2]
#         if train_n==train_code:
#             from_station_no= data_list[16]
#             to_station_no = data_list[17]
#             time_cost = data_list[10]
#             seat_types=data_list[35]
#             try:
#                 price=query_train_price(train_n,from_station_no,to_station_no,seat_types)
#             except:
#                 price=[9999,9999,9999,9999]
#         else:
#             continue
#         print(price)
#         info_list.append(info)
#     text_save(info_list)
#     return 0
tempi=0

def query_train_price(train_n,from_station_no, to_station_no):
    global tempi
    stype=['OM9', 'O9M', 'OMO', 'OOM', '1413', 'O9MP', '14613', 'F4', 'O4', '113', '1431', '131', '14163', 'FO', 'O9MO', 'O9OM', 'OM', 'OMOP', 'OP9OM', '43', 'OOMP', 'OMP', '113', 'O9OMP', 'AOF', '14123', 'FOAO', 'OF', '141623', '87', '87E', '112']
    url = (
        'https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?'
        'train_no={}&'
        'from_station_no={}&'
        'to_station_no={}&'
        'seat_types={}&'
        'train_date=2018-12-24'
    ).format(train_n, from_station_no,to_station_no,stype[tempi])
    r=requests.get(url, verify=False)
    raw_trains = r.json()['data']
    try:
        yz=raw_trains['A1'] 
    except:
        yz='09999'
    try:
        ze=raw_trains['O'] 
    except:
        ze='09999'
    try:
        yw=raw_trains['A3'] 
    except:
        yw='09999'
    try:
        rw=raw_trains['A4'] 
    except:
        rw='09999'
    try:
        zy=raw_trains['M'] 
    except:
        zy='09999'
    try:
        zy=raw_trains['M'] 
    except:
        zy='09999'
    price=[eval(yz[1:]),eval(yw[1:]),eval(rw[1:]),eval(ze[1:]),eval(zy[1:])]
    if price!=[9999,9999,9999,9999,9999]:
        return price 
    else:
        for i in range(0,len(stype)):
            print(i)
            try:
                url = (
                    'https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?'
                    'train_no={}&'
                    'from_station_no={}&'
                    'to_station_no={}&'
                    'seat_types={}&'
                    'train_date=2018-12-24'
                ).format(train_n, from_station_no,to_station_no,stype[i])
                #print(url)
                r=requests.get(url, verify=False)
                raw_trains = r.json()['data']
                #print(raw_trains)
                try:
                    yz=raw_trains['A1'] 
                except:
                    yz='09999'
                try:
                    ze=raw_trains['O'] 
                except:
                    ze='09999'
                try:
                    yw=raw_trains['A3'] 
                except:
                    yw='09999'
                try:
                    rw=raw_trains['A4'] 
                except:
                    rw='09999'
                try:
                    zy=raw_trains['M'] 
                except:
                    zy='09999'
                try:
                    zy=raw_trains['M'] 
                except:
                    zy='09999'
                price=[eval(yz[1:]),eval(yw[1:]),eval(rw[1:]),eval(ze[1:]),eval(zy[1:])]
                if price==[9999,9999,9999,9999,9999]:
                    continue
                tempi=i
                return price
            except:
                if i==len(stype):
                    return [9999,9999,9999,9999,9999]
                else:
                    continue

def text_save(data):
    file = open('t4.txt','a')
    #for i in range(len(data)):
    s = str(data).replace('[','').replace(']','')
    s = s.replace("'",'')
    s = s + '\n' 
    file.write(s)
    file.close()
    #print("保存文件成功") 

def query_train_info(train):
    url=('https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no={}&from_station_telecode=VNP&to_station_telecode=SHH&depart_date=2018-12-24').format(train)
    start=0
    arrive=0
    try:
        line1=True
        r = requests.get(url, verify=False)
        raw_trains = r.json()['data']['data']
        for raw_train in raw_trains:
            train_dict=dict(raw_train)
            if line1==True:
                train_code=train_dict['station_train_code']
                start_name=train_dict['station_name']
                try:
                    start=1
                    start_code=station_of_city[stations_dict[start_name]]
                    start_no=train_dict['station_no']
                    start_time=train_dict['start_time']
                    line1=False
                except:
                    print(train_code,"跳过")
                    break
            else:
                try:
                    arrive=start+1
                    arrive_name=train_dict['station_name']
                    arrive_code=station_of_city[stations_dict[arrive_name]]
                    arrive_time=train_dict['arrive_time']
                    arrive_no=train_dict['station_no']
                    price=query_train_price(train,start_no,arrive_no)
                    info=[train,train_code,start,arrive,start_no,arrive_no,start_code,arrive_code,start_name,arrive_name,start_time,arrive_time,price[0],price[1],price[2],price[3],price[4]]
                    #print(train_code,start_no,arrive_no,start_code,arrive_code,start_name,arrive_name,start_time,arrive_time)
                    #此处查询区间票价，写文件
                    #info_list.append(info)
                    print(info)
                    text_save(info)
                    start_name=arrive_name
                    start_code=station_of_city[stations_dict[start_name]]
                    start_no=arrive_no
                    start_time=train_dict['start_time']
                    start=arrive
                except:
                    continue

        return 0
    except:
        return 'Error'

def get_station(city):
    url="https://www.12306.cn/index/otn/index12306/queryScSname"
    try:
        telecode=stations_dict[city]
        d = {'station_telecode':telecode}
        r = requests.post(url, data=d)
        city_no=cities_dict[city]
        try:
            stations=r.json()['data']
        except:
            station_of_city[telecode]=city_no
            print(telecode)
        for station in stations:
            try:
                if stations_dict[station] in station_of_city:
                    continue
                else:
                    station_of_city[stations_dict[station]]=city_no
            except:
                continue
            print(station)
        return station_of_city
    except:
        return station_of_city

def get_station_of_city():
    for i in range(0,336):
        print(i)
        temp=get_station(cities_dict2[i])
        f = open('city.py','w')
        f.write("station_of_city=")
        f.write(str(temp))
        f.close()
        time.sleep(random.uniform(2,5))

#for i in range(2658,len(train_list)):
for i in range(0,2658):
        temp=dict(train_list[i])
        query_train_info(temp['train_no'])
        time.sleep(random.uniform(2,5))

#query_train_info('330000Z2670B')
#query_train_price('5l000G137560','01', '02')



