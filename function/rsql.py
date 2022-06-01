import pymysql as pymysql


def run_sql(sql):
    db = pymysql.connect(host="10.144.70.132", user="qqbot",
                         password="CPmL7rTj5a8iBxm8", database="qqbot")
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
        results = cursor.fetchall()
        value = []
        if len(results) == 1:
            cols = results[0]
            for col in cols:
                if col is not None:
                    value.append(col)
            return value
        else:
            for row in results:
                value.append(row[0])
            return value
    except Exception as e:
        print(e)
    db.close()


print(run_sql("select * from keywords_reply where keywords = '早'"))
