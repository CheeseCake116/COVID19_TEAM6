# -*- coding: utf-8 -*- 
import pymysql
import csv
import pandas as pd

#mysql server 연결, port 및 host 주의!
conn = pymysql.connect(host='localhost',
                        port = 3306,
                        user='userid',
                        password='password',
                        db='K_COVID19', 
                        charset='utf8')

# Connection 으로부터 Cursor 생성
cursor = conn.cursor()

data = pd.read_csv('K_COVID19.csv')



# Using Hashing
# get province list from "K_COVID19.csv"
# ['Seoul' 'Busan' 'Daegu' ... 'Gyeongsangnam-do' 'Jeju-do']
province_list = data['province'].unique()

# province_list에서 NULL값 제거. 지역이 NULL값인 행은 읽지 않게 됨
if 'NULL' in province_list:
    province_list.remove('NULL')

# get (province, confirmed_date) from "K_COVID19.csv" and count
# {날짜 : {지역 : 누적 수}} 로 이중 딕셔너리 사용
# {'2020-01-23': {'Seoul': 1}, '2020-01-30': {'Seoul': 3, 'Jeollabuk-do': 1}, ... }
confirmed_date = data[['province', 'confirmed_date']]
cdate_dic = {}
for index, (province, date) in confirmed_date.iterrows():
    if date in cdate_dic.keys():
        if province in cdate_dic[date].keys():
            cdate_dic[date][province] = cdate_dic[date][province] + 1
        else:
            cdate_dic[date][province] = 1
    else:
        temp = {province : 1}
        cdate_dic[date] = temp

# get (province, released_date) from "K_COVID19.csv" and count
# {'2020-01-23': {'Seoul': 1}, '2020-01-30': {'Seoul': 3, 'Jeollabuk-do': 1}, ... }
released_date = data[['province', 'released_date']]
rdate_dic = {}


for index, (province, date) in released_date.iterrows():
    if date in rdate_dic.keys():
        if province in rdate_dic[date].keys():
            rdate_dic[date][province] = rdate_dic[date][province] + 1
        else:
            rdate_dic[date][province] = 1
    else:
        temp = {province : 1}
        rdate_dic[date] = temp

# get (province, deceased_date) from "K_COVID19.csv" and count
# {'2020-01-23': {'Seoul': 1}, '2020-01-30': {'Seoul': 3, 'Jeollabuk-do': 1}, ... }
deceased_date = data[['province', 'deceased_date']]
ddate_dic = {}
for index, (province, date) in deceased_date.iterrows():
    if date in ddate_dic.keys():
        if province in ddate_dic[date].keys():
            ddate_dic[date][province] = ddate_dic[date][province] + 1
        else:
            ddate_dic[date][province] = 1
    else:
        temp = {province : 1}
        ddate_dic[date] = temp




# 중복된 case 제거를 위해 checking list & variable
date = []
total_confirmed = {}
total_released = {}
total_deceased = {}

# 지역별 누적을 위해 각 지역을 key로 가지는 dictionary 사용
for province in province_list:
    total_confirmed[province] = 0
    total_released[province] = 0
    total_deceased[province] = 0

with open("addtional_Timeinfo.csv", 'r') as file:
    file_read = csv.reader(file)

    # Use column 1(date), 2(test), 3(negative)
    # index = column - 1
    col_list = { 
        'date' :0,
        'test' :1,
        'negative' : 2}

    for i,line in enumerate(file_read):

        #Skip first line
        if not i:                           
            continue

        # checking duplicate date & checking date == "NULL"
        if (line[col_list['date']] in date) or (line[col_list['date']] == "NULL") :
            continue
        else:
            date.append(line[col_list['date']])

        #make sql data & query
        #"NULL" -> None (String -> null)
        if line[col_list['date']] == "NULL":
            line[col_list['date']] = None
        else:
            line[col_list['date']] = line[col_list['date']].strip()

        # 지역별
        for province in province_list:
            sql_data = []
            sql_data.append(line[col_list['date']]) # 'date' 값 삽입
            sql_data.append(province) # 'province' 값 삽입

            changed = 0

            if line[col_list['date']] in cdate_dic.keys():
                if province in cdate_dic[line[col_list['date']]]:
                    changed = 1
                    total_confirmed[province] = total_confirmed[province] + cdate_dic[line[col_list['date']]][province]
            sql_data.append(total_confirmed[province])

            if line[col_list['date']] in rdate_dic.keys():
                if province in rdate_dic[line[col_list['date']]]:
                    changed = 1
                    total_released[province] = total_released[province] + rdate_dic[line[col_list['date']]][province]
            sql_data.append(total_released[province])

            if line[col_list['date']] in ddate_dic.keys():
                if province in ddate_dic[line[col_list['date']]]:
                    changed = 1
                    total_deceased[province] = total_deceased[province] + ddate_dic[line[col_list['date']]][province]
            sql_data.append(total_deceased[province])

            # 해당 날짜와 지역에 변화가 없다면 스킵
            if not changed:
                continue



            # Make query & execute
            query = """INSERT INTO `timeprovince`(date, province, confirmed, released, deceased) VALUES (%s,%s,%s,%s,%s)"""
            sql_data = tuple(sql_data)

            # for debug
            try:
                cursor.execute(query, sql_data)
                print("[OK] Inserting [%s] to timeprovince" % (line[col_list['date']]))
            except (pymysql.Error, pymysql.Warning) as e:
                # print("[Error]  %s"%(pymysql.IntegrityError))
                if e.args[0] == 1062: continue
                print('[Error] %s | %s' % (line[col_list['date']], e))
                break

        

conn.commit()
cursor.close()