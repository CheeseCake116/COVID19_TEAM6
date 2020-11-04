import pymysql as sql
import csv

conn = sql.connect(host='localhost',
                   port=3306,
                   user='juhyoung98',
                   password='0000',
                   db='K_COVID19',
                   charset='utf8')

cursor = conn.cursor()

primary_set = []
with open("K_COVID19.csv", 'r') as file:
    file_read = csv.reader(file)

    col_list = {
        'region_code': 23,
        'province': 4,
        'confirmed_date': 10, # wdate
        'avg_temp': 14,
        'min_temp': 15,
        'max_temp': 16
    }

    for i, line in enumerate(file_read):

        if not i:
            continue

        if (line[col_list['region_code']], line[col_list['confirmed_date']]) in primary_set or line[col_list['region_code']] == "NULL" or line[col_list['confirmed_date']] == "NULL":
            continue
        else:
            primary_set.append((line[col_list['region_code']], line[col_list['confirmed_date']]))

        sql_data = []
        for idx in col_list.values():
            if line[idx] == "NULL":
                line[idx] = None
            else:
                line[idx] = line[idx].strip()
            sql_data.append(line[idx])

        print(sql_data)
        query = """INSERT INTO `Weather`(region_code, province, wdate, avg_temp, min_temp, max_temp) VALUES (%s, %s, %s, %s, %s, %s)"""
        sql_data = tuple(sql_data)

        try:
            cursor.execute(query, sql_data)
            print("[OK] Inserting [%s, %s] to Weather" % (line[col_list['region_code']], line[col_list['confirmed_date']]))
        except (sql.Error, sql.Warning) as e:
            if e.args[0] == 1062:
                continue
            print("[Error] %s | %s" % (line[col_list['region_code']], e))

conn.commit()
cursor.close()
