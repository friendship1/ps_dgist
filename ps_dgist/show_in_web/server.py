import pymysql
from private import password
from flask import Flask


app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"

@app.route("/ac")
def print_ac():
    conn = pymysql.connect(host='localhost', user='root', password=password.sql_password, db='baekjoon_dgist')
    curs = conn.cursor()
    sql = "select user, pnum from solved;"
    curs.execute(sql)
    rows = curs. fetchall()
    conn.close()
    buf = ""
    for row in rows:
        buf += str(row) + "<br>"

    return buf

@app.route("/wa")
def print_wa():
    conn = pymysql.connect(host='localhost', user='root', password=password.sql_password, db='baekjoon_dgist')
    curs = conn.cursor()
    sql = "select user, pnum from wronged;"
    curs.execute(sql)
    rows = curs. fetchall()
    conn.close()
    buf = ""
    for row in rows:
        buf += str(row) + "<br>"

    return buf

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
