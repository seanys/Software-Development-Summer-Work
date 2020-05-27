import scrapy
import re
import bs4
import json
import random
import pymysql

class PathSpider(scrapy.Spider):
    name = "mafengwo"

    first_load=True

    current_id=39
    current_place="南京"
    
    start_urls = [
        "https://www.mafengwo.cn/travel-scenic-spot/mafengwo/10065.html"
    ]

    custom_settings = {
        "origin": "https://www.mafengwo.cn",
    }
    
    def parse_articles_html(self, response,city_name):
        html = bs4.BeautifulSoup(response, "html5lib")
        all_title=html.find_all("a", class_="title-link")

        db = pymysql.connect("rm-bp14fgqt2783fvljh0o.mysql.rds.aliyuncs.com","mc","Westbrook0","cAuth" )
        cursor = db.cursor()

        i=0
        while i<len(all_title):
            url="http://www.mafengwo.cn"+all_title[i]['href']
            title=all_title[i].get_text()
            print(url,city_name,title)

            try:
                sql="INSERT INTO articles(title,place,url) \
                VALUES ('%s','%s','%s')" % \
                (title,city_name,url)

                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()

            i=i+1

        db.close()  

    def parse_dests(self, response):
        response_html = json.loads(response.body_as_unicode())['list']
        if response_html == "":
            print("请求页面超额",self.current_place)
        else:
            print(1)
            # self.parse_articles_html(response_html,response.meta['current_place'])       

    def get_all_cities(self):
        print("开始请求")
        urls = response.xpath(
            "//div[@class='row row-hot']/div[@class='wrapper']/div/div/div[@class='col']/dl/dd/a/@href").extract()

        places = response.xpath(
            "//div[@class='row row-hot']/div[@class='wrapper']/div/div/div[@class='col']/dl/dd/a/text()").extract()
        
        db = pymysql.connect("rm-bp14fgqt2783fvljh0o.mysql.rds.aliyuncs.com","mc","Westbrook0","cAuth" )
        cursor = db.cursor()
 
        for index,place in enumerate(places):
            url="http://www.mafengwo.cn"+urls[index]

            try:
                sql="INSERT INTO places(name,url) \
                VALUES ('%s','%s')" % \
                (place,url)

                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()

        db.close()       

    def read_file(self):
        f = open('/Users/sean/Documents/MyProjects/Python/mfw_spider/cities.txt','r')

        line = f.readline()
        while line:
            print (line)
            line = f.readline()
        f.close()

        # page_num = response.xpath(
        #     "//div[@class='_pagebar']/div[@class='m-pagination']/span[@class='count']/span[1]/text()").extract()
    
    def get_article_url(self,response):
        print("开始请求：", self.current_place,"...")
        db = pymysql.connect("rm-bp14fgqt2783fvljh0o.mysql.rds.aliyuncs.com","mc","Westbrook0","cAuth" )
        cursor = db.cursor()

        print ("确认城市ID...")
        sql="SELECT * FROM places where id="+ str(self.current_id)
        cursor.execute(sql)
        data = cursor.fetchall()
        city_id=data[0][3]
        self.current_place=data[0][1]

        page_id=1
        # while i<int(page_num[0]):
        while page_id<2:
            yield scrapy.Request(
                "http://www.mafengwo.cn/gonglve/ajax.php?act=get_travellist&pageid=mdd_index&sort=1&cost=0&days=0&month=0&tagid=0&mddid={}&page={}".
                format(city_id,page_id),
                callback=self.parse_dests
                )
            i=i+random.randint(1,2)
        
        print("请求结束")

        db.close()

    def parse(self, response):
        print("开始执行")

        db = pymysql.connect("rm-bp14fgqt2783fvljh0o.mysql.rds.aliyuncs.com","mc","Westbrook0","cAuth" )
        cursor = db.cursor()

        while self.current_id<=50:
            print("开始请求：", self.current_place,"...")            
            sql="SELECT * FROM places where id="+ str(self.current_id)
            cursor.execute(sql)
            data = cursor.fetchall()
            self.current_place=data[0][1]
            city_id=data[0][3]

            page_id=1
            while page_id<=300:
                yield scrapy.Request(
                    "http://www.mafengwo.cn/gonglve/ajax.php?act=get_travellist&pageid=mdd_index&sort=1&cost=0&days=0&month=0&tagid=0&mddid={}&page={}".
                    format(city_id,page_id),
                    callback=self.parse_dests,
                    meta={
                        "current_place": self.current_place
                    }
                )
                page_id=page_id+1
            
            print("请求结束")

            self.current_id=self.current_id+1

        db.close()