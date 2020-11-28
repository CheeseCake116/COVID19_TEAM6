# -*- coding: utf-8 -*- 
import pymysql
import csv
import sys

#mysql server 연결, port 및 host 주의!
def main(argv):
    conn = pymysql.connect(host=argv[1],
                           port=3306,
                           user=argv[2],
                           password=argv[3],
                           db='K_COVID19',
                           charset='utf8')

    # Connection 으로부터 Cursor 생성
    cursor = conn.cursor()

    # 중복된 case 제거를 위해 checking list
    patient_id = []
    with open("K_COVID19.csv", 'r') as file:
        file_read = csv.reader(file)

        # Use column 1(patient_id), 2(sex), 3(age), 4(country), 5(province), 6(city), 7(infection_case), 8(infected_by), 9(contact_number)
        #           10(symptom_onset_date),11(confirmed_date), 12(released_date),13(deceased_date), 14(state)
        # index = column - 1
        col_list = {
            'patient_id' :0,
            'sex' :1,
            'age' : 2,
            'country' : 3,
            'province' : 4,
            'city' :5,
            'infection_case' : 6,
            'infected_by' : 7,
            'contact_number' : 8,
            'symptom_onset_date' : 9,
            'confirmed_date' : 10,
            'released_date' : 11,
            'deceased_date' : 12,
            'state' : 13}

        for i,line in enumerate(file_read):

            #Skip first line
            if not i:
                continue

            # checking duplicate patient_id & checking patient_id == "NULL"
            if (line[col_list['patient_id']] in patient_id) or (line[col_list['patient_id']] == "NULL") :
                continue
            else:
                patient_id.append(line[col_list['patient_id']])

            #make sql data & query
            sql_data = []
            print(line)
            #"NULL" -> None (String -> null)
            print(col_list.values())
            for idx in col_list.values() :
                if line[idx] == "NULL" :
                    line[idx] = None
                else:
                    line[idx] = line[idx].strip()

                sql_data.append(line[idx])
            print(sql_data)
            query = """INSERT INTO `patientInfo`(patient_id,sex,age,country,province,city,infection_case,infected_by,contact_number,symptom_onset_date,confirmed_date,released_date,deceased_date,state) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            sql_data = tuple(sql_data)
            #print(sql_data)
            #for debug
            try:
                cursor.execute(query, sql_data)
                print("[OK] Inserting [%s] to patientInfo"%(line[col_list['patient_id']]))
            except (pymysql.Error, pymysql.Warning) as e :
                # print("[Error]  %s"%(pymysql.IntegrityError))
                if e.args[0] == 1062: continue
                print('[Error] %s | %s'%(line[col_list['patient_id']],e))
                break

    conn.commit()
    cursor.close()


if __name__ == "__main__":
    main(sys.argv)