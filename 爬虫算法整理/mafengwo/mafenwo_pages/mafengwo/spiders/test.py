import pymysql
import re

if __name__ == '__main__':
    db = pymysql.connect("rm-bp14fgqt2783fvljh0o.mysql.rds.aliyuncs.com","mc","Westbrook0","cAuth" )
    cursor = db.cursor()

    sql="SELECT * FROM places"
    cursor.execute(sql)
    data = cursor.fetchall()

    for place in data:
        city_id = re.search(r"/mafengwo/(\d+).html", place[2]).group(1)
        print(city_id)

        sql="UPDATE places SET city_id="+city_id+" where name='"+place[1]+"'"
        cursor.execute(sql)
        db.commit()

    db.close()