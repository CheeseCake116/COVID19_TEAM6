# -*- coding: utf-8 -*- 
import pymysql
import csv
import pandas as pd
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
    data = pd.read_csv('K_COVID19.csv')

    # "K_COVID19.csv"로부터 province 리스트를 가져온다
    # province_list = ['Seoul' 'Busan' 'Daegu' ... 'Gyeongsangnam-do' 'Jeju-do']
    province_list = data['province'].unique()

    # province_list에서 NULL값 제거. 지역이 NULL값인 행은 읽지 않게 하기 위해
    if 'NULL' in province_list:
        province_list.remove('NULL')

    # "K_COVID19.csv"에서 (province, confirmed_date) 튜플을 가져와 누적 환자 수를 계산해둔다
    # {날짜 : {지역1 : 누적 수, 지역2 : 누적 수, ...}} 로 이중 딕셔너리 사용
    # confirmed_date = {'2020-01-23': {'Seoul': 1}, '2020-01-30': {'Seoul': 3, 'Jeollabuk-do': 1}, ... }
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

    #released_date와 deceased_date도 마찬가지
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

    # 누적량을 지역별로 계산하기 위해 각 지역을 key로 가지는 dictionary 사용
    total_confirmed = {}
    total_released = {}
    total_deceased = {}
    for province in province_list:
        total_confirmed[province] = 0
        total_released[province] = 0
        total_deceased[province] = 0

    #1/20~6/30까지 날짜정보를 받기 위해 additional_Timeinfo.csv 파일을 open
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

            # line에 들어온 현재 날짜에 있었던 각 지역별 변동사항을 얻기 위해 지역별 for문을 돌린다
            for province in province_list:
                sql_data = []
                sql_data.append(line[col_list['date']]) # sql에 'date' 값 삽입
                sql_data.append(province) # sql에 'province' 값 삽입

                if line[col_list['date']] in cdate_dic.keys():
                    if province in cdate_dic[line[col_list['date']]]:
                        total_confirmed[province] = total_confirmed[province] + cdate_dic[line[col_list['date']]][province]
                sql_data.append(total_confirmed[province])

                if line[col_list['date']] in rdate_dic.keys():
                    if province in rdate_dic[line[col_list['date']]]:
                        total_released[province] = total_released[province] + rdate_dic[line[col_list['date']]][province]
                sql_data.append(total_released[province])

                if line[col_list['date']] in ddate_dic.keys():
                    if province in ddate_dic[line[col_list['date']]]:
                        total_deceased[province] = total_deceased[province] + ddate_dic[line[col_list['date']]][province]
                sql_data.append(total_deceased[province])



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


if __name__ == "__main__":
    main(sys.argv)
