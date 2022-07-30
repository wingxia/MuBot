import pymysql as pymysql


def run_sql(sql):
    db = pymysql.connect(host="182.61.2.44",port=2306, user="qqbot",
                         password="baETzJf5tTy3SfR8", database="qqbot")
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
