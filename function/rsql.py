import pymysql as pymysql


def run_sql(sql):
    db = pymysql.connect(host="10.144.118.78", user="qqbot",
                         password="baETzJf5tTy3SfR8", database="qqbot")
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
        print(sql)
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
if run_sql(f"select * from special_title where qqid = 123 and groupid = 123123") == []:
    print(1)