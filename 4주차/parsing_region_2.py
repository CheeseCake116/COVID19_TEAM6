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
    region_code = []
    with open("Region.csv", 'r') as file:
        file_read = csv.reader(file)

        # Use column 1(region_code), 2(province), 3(city), 4(latitude), 5(longitude), 6(elementary_school_count), 7(kindergarten_count), 8(university_count), 9(academy_ratio)
        #           10(elderly_population_ratio),11(elderly_alone_ratio), 12(nursing_home_count)
        # index = column - 1
        col_list = {
            'region_code' :0,
            'province' : 1,
            'city' : 2,
            'latitude' : 3,
            'longitude' : 4,
            'elementary_school_count' :5,
            'kindergarten_count' : 6,
            'university_count' : 7,
            'academy_ratio' : 8,
            'elderly_population_ratio' : 9,
            'elderly_alone_ratio' : 10,
            'nursing_home_count' : 11}

        for i,line in enumerate(file_read):

            #Skip first line
            if not i:
                continue

            # checking duplicate patient_id & checking patient_id == "NULL"
            if (line[col_list['region_code']] in region_code) or (line[col_list['region_code']] == "NULL") :
                continue
            else:
                region_code.append(line[col_list['region_code']])

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
            query = """INSERT INTO `region`(region_code, province, city, latitude, longitude, elementary_school_count, kindergarten_count, university_count, academy_ratio, elderly_population_ratio,elderly_alone_ratio, nursing_home_count) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            sql_data = tuple(sql_data)
            #print(sql_data)
            #for debug
            try:
                cursor.execute(query, sql_data)
                print("[OK] Inserting [%s] to region"%(line[col_list['region_code']]))
            except (pymysql.Error, pymysql.Warning) as e :
                # print("[Error]  %s"%(pymysql.IntegrityError))
                if e.args[0] == 1062: continue
                print('[Error] %s | %s'%(line[col_list['region_code']],e))
                break

    conn.commit()
    cursor.close()


if __name__ == "__main__":
    main(sys.argv)