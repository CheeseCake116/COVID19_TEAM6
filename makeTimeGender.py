"""
작성자 : 곽승규
"""
# -*- coding: utf-8 -*-
import pymysql
import csv
import pandas as pd
import sys

def main(argv):
    # mysql server 연결, port 및 host 주의!
    conn = pymysql.connect(host=argv[1],
                            port = 3306,
                            user= argv[2],
                            password= argv[3],
                            db='K_COVID19',
                            charset='utf8')

    # Connection 으로부터 Cursor 생성
    cursor = conn.cursor()

    data = pd.read_csv('K_COVID19.csv')

    # Using Hashing
    # get confirmed_date from "K_COVID19.csv" and count, 확진자 날짜별 수
    confirmed_date = data[['confirmed_date','sex']]
    cdate_dic = {} # 딕셔너리 생성!
    for index, (date, sex) in confirmed_date.iterrows():
        if date in cdate_dic.keys():
            if sex in cdate_dic[date].keys():
                cdate_dic[date][sex] = cdate_dic[date][sex] + 1
            else:
                cdate_dic[date][sex] = 1
        else:
            temp = {sex : 1}
            cdate_dic[date] = temp
    print(cdate_dic)
    # get deceased_date from "K_COVID19.csv" and count, 사망자 날짜별 수
    deceased_date = data[['deceased_date','sex']]
    ddate_dic = {}
    for index,(date,sex) in deceased_date.iterrows():
        if date in ddate_dic.keys():
            if sex in ddate_dic[date].keys():
                ddate_dic[date][sex] = ddate_dic[date][sex] + 1
            else:
                ddate_dic[date][sex] = 1
        else:
            temp = {sex : 1}
            ddate_dic[date] = temp
    print(ddate_dic)

    # 중복된 case 제거를 위해 checking list & variable
    date = [] # checking을 하기위한 리스트
    total_confirmed = {}
    total_confirmed = {
        'male': 0,
        'female' : 0
    }
    total_deceased = {}
    total_deceased = {
        'male': 0,
        'female' : 0
    }
    # total_male_confirmed = 0 # 남자 확진자 수
    # total_female_confirmed = 0 # 여자 확진자 수
    # total_released = 0


    with open("addtional_Timeinfo.csv", 'r') as file: # addtional_Timeinfo.csv 파일 오픈
        file_read = csv.reader(file) # file_read 에 파일 저장

        # Use column 1(date), 2(test), 3(negative)
        # index = column - 1
        col_list = {
            'date': 0
            }

        # 반복문 사용 시 몇 번째 반복문인지 확인이 필요할 수 있습니다. 이때 사용합니다.
        # 인덱스 번호와 컬렉션의 원소를 tuple형태로 반환합니다.
        for i, line in enumerate(file_read): # file_read 의 한줄 씩 ( 한줄은 tuple임 ex(date: 2020.1.20	test: 1	negative : 0) )
            # Skip first line
            if not i:
                continue

            # checking duplicate case_id & checking case_id == "NULL"
            if (line[col_list['date']] in date) or (line[col_list['date']] == "NULL"): # 한 line의 date가 (date 리스트)에 있거나, line의 date값이 null일 때
                continue
            else:
                date.append(line[col_list['date']]) # col_list['date']는 0이다. 따라서 line[0]값들을 date리스트에 넣는다.

            # make sql data & query
            # "NULL" -> None (String -> null)
            if line[col_list['date']] == "NULL":
                line[col_list['date']] = None
            else:
                line[col_list['date']] = line[col_list['date']].strip() # 양쪽 공백 제거

            for sex in ('male','female'):
                sql_data = []
                sql_data.append(line[col_list['date']])  # 여기에서 date 를 넣는다.
                sql_data.append(sex) # 여기에서 sex를 넣는다.
                if line[col_list['date']] in cdate_dic.keys():
                    if sex in cdate_dic[line[col_list['date']]]:
                        total_confirmed[sex] = total_confirmed[sex] + cdate_dic[line[col_list['date']]][sex]
                sql_data.append(total_confirmed[sex])  # 여기에서 confirmed를 넣는다.
                # append "total number from deceased_date" to sql_date list
                if line[col_list['date']] in ddate_dic.keys():
                    if sex in ddate_dic[line[col_list['date']]]:
                        total_deceased[sex] = total_deceased[sex] + ddate_dic[line[col_list['date']]][sex]
                sql_data.append(total_deceased[sex]) # 여기에서 deceased를 넣는다.

                print(sql_data)
                # Make query & execute
                query = """INSERT INTO `timeGender`(date, sex, confirmed, deceased) VALUES (%s,%s,%s,%s)"""
                sql_data = tuple(sql_data)

                # for debug
                try:
                    cursor.execute(query, sql_data)
                    print("[OK] Inserting [%s] to timegender" % (line[col_list['date']]))
                except (pymysql.Error, pymysql.Warning) as e:
                    # print("[Error]  %s"%(pymysql.IntegrityError))
                    if e.args[0] == 1062: continue
                    print('[Error] %s | %s' % (line[col_list['date']], e))
                    break

    conn.commit()
    cursor.close()

if __name__ == "__main__":
    main(sys.argv)