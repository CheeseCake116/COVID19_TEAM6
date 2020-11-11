# -*- coding: utf-8 -*- 
import pymysql
import csv
import pandas as pd

#mysql server 연결, port 및 host 주의!
conn = pymysql.connect(host='localhost',
                        port = 8889,
                        user='root', 
                        password='@ehdgml12', 
                        db='K_COVID19', 
                        charset='utf8')

# Connection 으로부터 Cursor 생성
cursor = conn.cursor()

data = pd.read_csv('../combine/K_COVID19.csv')




# Using Hashing
# get confirmed_date from "K_COVID19.csv" and count
confirmed_date = data['confirmed_date']
cdate_dic = {}
for date in list(confirmed_date):
    if date in cdate_dic.keys():
        cdate_dic[date] = cdate_dic[date] + 1
    else:
        cdate_dic[date] = 1

# get released_date from "K_COVID19.csv" and count
released_date = data['released_date']
rdate_dic = {}
for date in list(released_date):
    if date in rdate_dic.keys():
        rdate_dic[date] = rdate_dic[date] + 1
    else:
        rdate_dic[date] = 1

# get deceased_date from "K_COVID19.csv" and count
deceased_date = data['deceased_date']
ddate_dic = {}
for date in list(deceased_date):
    if date in ddate_dic.keys():
        ddate_dic[date]= ddate_dic[date]+1
    else:
        ddate_dic[date] = 1







# 중복된 case 제거를 위해 checking list & variable
date = []
total_confirmed = 0
total_released = 0
total_deceased = 0
with open("./addtional_Timeinfo.csv", 'r') as file:
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

        # checking duplicate case_id & checking case_id == "NULL"
        if (line[col_list['date']] in date) or (line[col_list['date']] == "NULL") :
            continue
        else:
            date.append(line[col_list['date']])

        #make sql data & query
        sql_data = []
        #"NULL" -> None (String -> null)
        for idx in col_list.values() :
            if line[idx] == "NULL" :
                line[idx] = None
            else:
                line[idx] = line[idx].strip()

            sql_data.append(line[idx])
        

        
        # append "total number from confirmed_date" to sql_date list
        if line[col_list['date']] in cdate_dic.keys():
            total_confirmed = total_confirmed + cdate_dic[line[col_list['date']]]
        sql_data.append(total_confirmed)
        # append "total number from released_date" to sql_date list
        if line[col_list['date']] in rdate_dic.keys():
            total_released = total_released + rdate_dic[line[col_list['date']]]
        sql_data.append(total_released)
        # append "total number from deceased_date" to sql_date list
        if line[col_list['date']] in ddate_dic.keys():
            total_deceased = total_deceased + ddate_dic[line[col_list['date']]]
        sql_data.append(total_deceased)
        
    





        #Make query & execute
        query = """INSERT INTO `timeInfo`(date, test, negative, confirmed, released, deceased) VALUES (%s,%s,%s,%s,%s,%s)"""
        sql_data = tuple(sql_data)

        #for debug
        try:
            cursor.execute(query, sql_data)
            print("[OK] Inserting [%s] to timeInfo"%(line[col_list['date']]))
        except (pymysql.Error, pymysql.Warning) as e :
            # print("[Error]  %s"%(pymysql.IntegrityError))
            if e.args[0] == 1062: continue
            print('[Error] %s | %s'%(line[col_list['date']],e))
            break

conn.commit()
cursor.close()