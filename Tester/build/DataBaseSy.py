def sql_do_something(db, z):
    import sqlite3

    con = sqlite3.connect(db)
    cur = con.cursor()
    res = cur.execute(z).fetchall()
    con.commit()
    con.close()
    return res
