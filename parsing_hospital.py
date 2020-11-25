# -*- coding: utf-8 -*-
import pymysql
import csv

#mysql server 연결, port 및 host 주의!
conn = pymysql.connect(host='localhost',
                        port = 3306,
                        user='tmdrb0912',
                        password='0206',
                        db='K_COVID19',
                        charset='utf8')

# Connection 으로부터 Cursor 생성
cursor = conn.cursor()

# 중복된 case 제거를 위해 checking list
hospital_code = []
with open("Hospital.csv", 'r') as file:
    file_read = csv.reader(file)

    # Use column 1 : Hospital_id, 2:Hospital name, 3 : Hospital_province, 4 : Hospital_city, 5 : Hospital_latitude,
    # 6 : Hospital_longitude,7 : capacity, 8 : now
    # index = column - 1
    col_list = {
        'Hospital_id' : 0,
        'Hospital_name' : 1,
        'Hospital_province' : 2,
        'lHospital_city' : 3,
        'Hospital_latitude' : 4,
        'Hospital_longitude' : 5,
        'capacity' : 6,
        'now' : 7}

    for i,line in enumerate(file_read):

        #Skip first line
        if not i:
            continue

        # checking duplicate patient_id & checking patient_id == "NULL"
        if (line[col_list['Hospital_id']] in hospital_code) or (line[col_list['Hospital_id']] == "NULL") :
            continue
        else:
            hospital_code.append(line[col_list['Hospital_id']])

        #make sql data & query
        sql_data = []
        # print(line)
        #"NULL" -> None (String -> null)
        # print(col_list.values())
        for idx in col_list.values() :
            if line[idx] == "NULL" :
                line[idx] = None
            else:
                line[idx] = line[idx].strip()

            sql_data.append(line[idx])
       #  print(sql_data)
        query = """INSERT INTO `hospital`(Hospital_id,Hospital_name,Hospital_province,Hospital_city,Hospital_latitude,Hospital_longitude,capacity,now) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
        sql_data = tuple(sql_data)
        #print(sql_data)
        #for debug
        try:
            cursor.execute(query, sql_data)
            print("[OK] Inserting [%s] to hospital"%(line[col_list['Hospital_id']]))
        except (pymysql.Error, pymysql.Warning) as e :
            # print("[Error]  %s"%(pymysql.IntegrityError))
            if e.args[0] == 1062: continue
            print('[Error] %s | %s'%(line[col_list['Hospital_id']],e))
            break

conn.commit()
cursor.close()
