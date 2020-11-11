import pymysql
import csv
import time
time.strftime('%Y-%m-%d %H:%M:%S')

conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='juhyoung98',
                       password='0000',
                       db='K_COVID19',
                       charset='utf8')

cursor = conn.cursor()
timeage_dic = {}
deceased_dic = {}
confirmed_dic = {}

total_deceased = {}
total_confirmed = {}
try:
    with conn.cursor() as cur:

        cur.execute('SELECT DISTINCT age from Patientinfo')
        rows = cur.fetchall()
        for r in rows:
            if r[0]:
                total_deceased[r[0]] = 0
                total_confirmed[r[0]] = 0

        cur.execute('SELECT confirmed_date, age, COUNT(*) from Patientinfo where state=\'deceased\' group by age, confirmed_date order by confirmed_date')
        deceased_rows = cur.fetchall()
        for row in deceased_rows:
            if not row[0] or not row[1]:
                continue
            if str(row[0]) not in deceased_dic:
                deceased_dic[str(row[0])] = []
            deceased_dic[str(row[0])].append((row[1], row[2]))

        cur.execute('SELECT confirmed_date, age, count(*) from Patientinfo where state!=\'deceased\' group by age, confirmed_date order by confirmed_date')
        confirmed_rows = cur.fetchall()
        for row in confirmed_rows:
            if not row[0] or not row[1]:
                continue
            if str(row[0]) not in confirmed_dic:
                confirmed_dic[str(row[0])] = []
            confirmed_dic[str(row[0])].append((row[1], row[2]))

        with open("./addtional_Timeinfo.csv", 'r') as file:
            file_read = csv.reader(file)

            for i, line in enumerate(file_read):
                if not i:
                    continue
                today = line[0]
                timeage_dic[today] = {}

                if today in deceased_dic:
                    for (age, num) in deceased_dic[today]:
                        total_deceased[age] += num
                if today in confirmed_dic:
                    for (age, num) in confirmed_dic[today]:
                        total_confirmed[age] += num

                for age in list(total_deceased.keys()):
                    timeage_dic[today][age] = (total_confirmed[age], total_deceased[age])

                query = "INSERT INTO `TimeAge`(date, age, confirmed, deceased) VALUES (%s, %s, %s, %s)"
                for key, val in tuple(timeage_dic[today].items()):
                    try:
                        cur.execute(query, (today, key, val[0], val[1]))
                        print(f"[OK] {today}, {key} to TimeAge")
                    except (pymysql.Error, pymysql.Warning) as e:
                        print(e)

            # print(timeage_dic)
finally:
    conn.commit()
    conn.close()