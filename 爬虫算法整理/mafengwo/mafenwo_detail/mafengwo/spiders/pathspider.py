import scrapy
import re
import bs4
import json
import time
import pymysql

class PathSpider(scrapy.Spider):

    name = "mafengwo"
    start_urls = []

    db = pymysql.connect("rm-bp14fgqt2783fvljh0o.mysql.rds.aliyuncs.com","mc","Westbrook0","cAuth" )
    cursor = db.cursor()

    start = 300000
    end=start+25000
    sql="SELECT * FROM articles where id>="+str(start)+" AND id<"+str(end)+" and exist=0"
    cursor.execute(sql)
    articles = cursor.fetchall()

    for article in articles:
        start_urls.append(article[8])
    
    db.close()

    def parse_dest_html(self, response):
        html = bs4.BeautifulSoup(response, "html5lib")
        res = []
        mddid = 0
        for dest in html.find_all("div", class_="_j_cityitem"):
            mddid = dest['data-mddid']
            if "待完善" in dest.prettify():
                res.append({
                    "city":
                    dest.find(
                        "div",
                        class_="vertical").find("p").get_text(strip=True)[:-3],
                    "city_poi": []
                })
            else:
                city = dest.find("h3").find("span").get_text()
                dests = []
                for poi in dest.find_all("h4"):
                    dests = poi.get_text(strip=True)
                res.append({
                    "city": city,
                    "city_poi": dests,
                })
        return (res, mddid)

    def parse_art(self, response):
        # response_html = json.loads(response.body_as_unicode())
        print(response)
    
    def parse_paragraph(self,paragraph):
        paragraph = re.sub(r'</a>', "", paragraph)
        paragraph = re.sub(r'<img.*/>', "", paragraph)
        paragraph = re.sub(r'<br>', "thisisanewline", paragraph)
        paragraph = re.sub(r'<.*>', "", paragraph)
        paragraph = re.sub(r' ', "", paragraph)
        paragraph = re.sub(r'\n', "", paragraph)
        paragraph = re.sub(r'thisisanewline', "\n", paragraph)
        paragraph = paragraph + "\n"
        return paragraph


    def parse(self, response):

        db = pymysql.connect("rm-bp14fgqt2783fvljh0o.mysql.rds.aliyuncs.com","mc","Westbrook0","cAuth" )
        cursor = db.cursor()

        title = response.xpath(
            "//title/text()").extract()

        name_url = response.xpath(
            "//a[@class='per_name']/@href").extract()

        publish_time = response.xpath(
            "//span[@class='time']/text()").extract()

        mdd = response.xpath(
            "//div[@class='mdd_info']/a/strong/text()").extract()
        
        print(title,name_url,publish_time,mdd)
        print(len(mdd))
        print(str(self.start),"-",str(self.end))
        if(len(mdd)>0):
            uid_re = re.search(r"/u/(\d+).html", name_url[0])
        
            uid = -1
            if uid_re:
                uid=uid_re.group(1)
        
            content = response.xpath(
                "//div[@class='_j_content_box']/*").extract()

            sql="SELECT * FROM articles where url='"+response.url+"'"
            cursor.execute(sql)
            articles = cursor.fetchall()

            if len(articles)>0:
                article_id=articles[0][0]
                print(article_id)

                for paragraph in content:
                    soup=bs4.BeautifulSoup(paragraph)
                    if len(soup.find_all("p",class_="_j_note_content _j_seqitem"))>0:
                        sql="INSERT INTO article_content(article_id,content_type,content) \
                        VALUES (%s,'%s','%s')" % \
                        (article_id,'text',self.parse_paragraph(paragraph))
                        cursor.execute(sql)
                        db.commit()
                    else:
                        img_res=soup.find_all("img")
                        if len(img_res)>0:
                            sql="INSERT INTO article_content(article_id,content_type,content) \
                            VALUES (%s,'%s','%s')" % \
                            (article_id,'image',img_res[0].get('data-src'))
                            cursor.execute(sql)
                            db.commit()
        
                sql="UPDATE articles SET author_id="+str(uid)+",publish_time='"+publish_time[0]+"',exist=1 where id="+str(article_id)
                print(sql)
                cursor.execute(sql)
                db.commit()
        
    
            db.close()
        
        else:
            time.sleep(300)