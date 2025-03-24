import sqlite3

lis = [559, 483, 502]

def check_db(dbname):
    con = sqlite3.connect(dbname)
    cur = con.cursor()

    cur.execute("SELECT file,name FROM object WHERE id IN ({})".format(",".join("?" * 3)), lis)

    for row in cur:
        print(row)

    cur.close()
    con.close()   

dbname = "Llama3.db"


check_db(dbname)