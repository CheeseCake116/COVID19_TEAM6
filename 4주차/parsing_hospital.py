# -*- coding: utf-8 -*-
import pymysql
import csv
def get_dist(pat_lat, pat_long, hos_lat, hos_long):
    return (hos_lat-pat_lat)**2 + (hos_long-pat_long)**2

#mysql server 연결, port 및 host 주의!
conn = pymysql.connect(host='127.0.0.1',
                        port = 3306,
                        user='juhyoung98',
                        password='0000',
                        db='K_COVID19',
                        charset='utf8')

# Connection 으로부터 Cursor 생성
cursor = conn.cursor()

# 중복된 case 제거를 위해 checking list
hospital_code = [None]
with open("../Hospital.csv", 'r') as file:
    file_read = csv.reader(file)

    # Use column 1 : Hospital_id, 2:Hospital name, 3 : Hospital_province, 4 : Hospital_city, 5 : Hospital_latitude,
    # 6 : Hospital_longitude,7 : capacity, 8 : now
    # index = column - 1
    col_list = {
        'Hospital_id' : 0,
        'Hospital_name' : 1,
        'Hospital_province' : 2,
        'Hospital_city' : 3,
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
            # hospital_code.append(line[col_list['Hospital_id']])
            hospital_code.append([float(line[col_list['Hospital_latitude']]), float(line[col_list['Hospital_longitude']]), int(line[col_list['capacity']]), int(line[col_list['now']])])

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

###

cursor.execute("SELECT patient_id, province, city FROM patientinfo")
patient_row = cursor.fetchall()
patient_col_list = {
    'patient_id' : 0,
    'province' : 1,
    'city' : 2
}
for row in patient_row:
    row = list(row)
    min_dist = 1000000
    min_dist_idx = 0
    if row[patient_col_list['city']] == 'etc' or row[patient_col_list['city']] is None:
        row[patient_col_list['city']] = row[patient_col_list['province']]
    cursor.execute(f"SELECT latitude, longitude from Region where province='{row[patient_col_list['province']]}' and city='{row[patient_col_list['city']]}'")
    patient_loca = cursor.fetchone()
    if not patient_loca: # Region의 province, city의 이름과 PatientInfo의 province, city의 이름이 일치하지 않아서 환자의 지역을 구할수가 없다. 그래서 걸러냈다.
        continue

    for i, hospital in enumerate(hospital_code):

        if not i:
            continue
        if hospital[3] >= hospital[2]: # 수용인원 다 차면 continue
            continue
        tmp = get_dist(patient_loca[0], patient_loca[1], hospital[0], hospital[1])
        if tmp <= min_dist:
            min_dist = tmp
            min_dist_idx = i

    cursor.execute(f"UPDATE patientInfo SET hospital_id={min_dist_idx} where patient_id={row[patient_col_list['patient_id']]}")
    hospital_code[min_dist_idx][3] += 1

for i, hospital in enumerate(hospital_code):
    if not i:
        continue
    cursor.execute(f"UPDATE hospital SET now={hospital[3]} where Hospital_id={i}")
conn.commit()
cursor.close()
