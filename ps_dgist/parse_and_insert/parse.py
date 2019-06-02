#-*- coding: utf-8 -*-

import requests
import re
import pymysql
from private import password

url = "http://www.acmicpc.net/school/ranklist/246" #dgist url
url2 = "https://www.acmicpc.net/user/"
r = requests.get(url)
# print(r.content)

conn = pymysql.connect(host='localhost', user='root', password=password.sql_password, db='baekjoon_dgist' )
curs = conn.cursor()
ac_insert_sql = "INSERT IGNORE INTO solved (user, pnum, updated_date) VALUES (%s, %s, NOW())"
wa_insert_sql = "INSERT IGNORE INTO wronged (user, pnum, updated_date) VALUES (%s, %s, NOW())"
# curs.execute(sql)
#rows = curs.fetchall()
# print(rows)

try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
html = r.content
parsed_html = BeautifulSoup(html, from_encoding='utf-8')
outter = parsed_html.body.find('div', attrs={'class':'table-responsive'})
# print(outter)
outter_text = str(outter)
# print(outter_text)
outter_text_parsed = BeautifulSoup(outter_text, from_encoding='utf-8')
# print(outter_text_parsed)
ids = outter_text_parsed.body.findAll('a', attrs={'href' : re.compile(r'/user/\S*')})
for id_ in ids:
#     break
    print(id_.text)
    base_url = url2 + id_.text
    r = requests.get(base_url)
    html = r.content
    parsed_html = BeautifulSoup(html, from_encoding='utf-8')
    acs = parsed_html.body.find('h3', text='푼 문제').find_parent('div').find_parent('div').findAll('span', attrs={'class' : 'problem_number'})
    was = parsed_html.body.find('h3', text='시도했지만 풀지 못한 문제').find_parent('div').find_parent('div').findAll('span', attrs={'class' : 'problem_number'})
    print(len(acs), len(was))
    for ac in acs: 
        curs.execute(ac_insert_sql, (id_.text, ac.text))
    for wa in was:
        curs.execute(wa_insert_sql, (id_.text, wa.text))
#    outter = parsed_html.body.find('span', attrs={'class' : 'problem_number'}) # .find('a', attrs={'class' : 'result-ac'})
# print(ac)
conn.commit()
conn.close()
