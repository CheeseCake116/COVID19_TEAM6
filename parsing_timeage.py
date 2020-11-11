import pymysql
import csv
import pandas as pd
import time
import pprint
time.strftime('%Y-%m-%d %H:%M:%S')

conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='juhyoung98',
                       password='0000',
                       db='K_COVID19',
                       charset='utf8')

cursor = conn.cursor()
timeage_dic = {}
try:
    with conn.cursor() as cur:
        cur.execute('SELECT confirmed_date, age, COUNT(*) from Patientinfo where state=\'deceased\' group by age, confirmed_date order by confirmed_date')
        rows = cur.fetchall()
        for row in rows:
            if not row[0] or not row[1]:
                continue
            elif (row[0], row[1]) not in timeage_dic:
                timeage_dic[(row[0], row[1])] = {'deceased_num': row[2], 'confirmed_num' : 0}

        cur.execute('SELECT confirmed_date, age, count(*) from Patientinfo where state!=\'deceased\' group by age, confirmed_date order by confirmed_date')
        rows = cur.fetchall()
        for row in rows:
            if not row[0] or not row[1]:
                continue
            elif (row[0], row[1]) not in timeage_dic:
                timeage_dic[(row[0], row[1])] = {'deceased_num': 0, 'confirmed_num' : row[2]}
            else:
                timeage_dic[((row[0], row[1]))]['confirmed_num'] = row[2]

        for key, val in timeage_dic.items():
            query = "INSERT INTO `TimeAge`(date, age, confirmed, deceased) values (%s, %s, %s, %s)"
            sqldata = (str(key[0]), key[1], val['confirmed_num'], val['deceased_num'])
            try:
                cur.execute(query, sqldata)
                print(f"[OK] Inserting {key}to TimeAge")
            except (pymysql.Error, pymysql.Warning) as e:
                if e.args[0] == 1062:
                    continue
                print(e)

        cur.execute("SELECT * from `TimeAge`")
        rows = cur.fetchall()
        pprint.pprint(rows)


finally:
    conn.commit()
    conn.close()