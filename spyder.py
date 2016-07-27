#-*- coding:utf-8 -*-
import urllib2
import re
import os
import sys, types
import logging, logging.handlers
#import sqlite3
import psycopg2
from db import DB_Sqlite3
from bs4 import BeautifulSoup


def spyder(people, parent, level):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    fh=logging.handlers.RotatingFileHandler('log.txt', maxBytes=1024*1024, backupCount=1)
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    MyUrl = 'http://www.zhihu.com/people/' + people
    UserAgent = 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'
    Headers = {'User-Agent': UserAgent }
    req = urllib2.Request(MyUrl, headers=Headers)
    try:
        MyResponse = urllib2.urlopen(req)
        MyPage = MyResponse.read()
        UnicodePage = BeautifulSoup(MyPage, 'html5lib').prettify()
        Title_Section = re.findall(r'<div class="title-section ellipsis">[\s\S]*?"name">\n[ ]{10}(.*?)\n', UnicodePage, re.S)
        Description = re.findall(r'<span class="description unfold-item">\n\s*<span class="con.*?>\n\s*(.*?)\n', UnicodePage, re.S)
        People = re.findall(r'<a class="author-link.*?" data-hovercard="p\$t\$(.*?)" href=.*?people.*?" target.*?">', UnicodePage, re.S)
        conn = psycopg2.connect(database="spyderdb", user="dbuser", password="dbuser", host="127.0.0.1", port="5432") 
        cur = conn.cursor()
        if len(Description) == 0 :
            cur.execute("insert into People_Inf values(%s, %s, %s, %s, %s);", (Title_Section[0], None, people, parent, level)); 
            print Title_Section[0], None, people[:], parent, level,"-------"
        else:
            cur.execute("INSERT INTO People_Inf VALUES(%s, %s, %s, %s, %s);", (Title_Section[0], Description[0], people, parent, level));
	    print Title_Section[0], Description[0], people[:], parent, level,"--------"
#	    cur.execute("delete from People where name = ?", (people))
        cur.close()
        conn.commit()
        conn.close()

	   # print list(set(People))
        for people_list in list(set(People)):
	  #  print people_list, type(people_list)
            conn2 = psycopg2.connect(database="spyderdb", user="dbuser", password="dbuser", host="127.0.0.1", port="5432") 
	    cur2 = conn2.cursor()
	    cur2.execute('select count(*) from People where Name=(%s);', (people_list,));
	    cur2_len =  cur2.fetchall()[0][0]
	    if cur2_len == 0:
	        cur2.execute("INSERT INTO People VALUES(%s, %s, %s, %s);", (people, level+1, False, people_list,));
		#print people_list
	    cur2.close()
	    conn2.commit()
	    conn2.close()
	
    except BaseException, e:
        logger.debug('there is a error', exc_info=True) 

def run():
    while True:
        conn3 = psycopg2.connect(database="spyderdb", user="dbuser", password="dbuser", host="127.0.0.1", port="5432") 
	cur3 = conn3.cursor()
	cur3.execute("select min(Level) from People where Done=False;")
	Min_Level = cur3.fetchall()[0]
        cur3.execute("select Name, Parent, Level from People where  Done=False;", Min_Level)
	cur3_list = cur3.fetchall()
	cur3.close()
	conn3.close()
	for element in cur3_list:
#	    print element[0], element[1], element[2]
	    conn4 = psycopg2.connect(database="spyderdb", user="dbuser", password="dbuser", host="127.0.0.1", port="5432")
	    cur4 = conn4.cursor()
	    cur4.execute("update People set Done=True where Name=(%s);", (element[0],))
	    cur4.close()
	    conn4.commit()
	    conn4.close()
	    spyder(element[0], element[1], element[2])

if __name__ == '__main__':
#    if os.path.exists('./spyder.db'):
#        pass
#    else:
#        DB_Sqlite3.Create_Db()
    spyder('xie-ke-41', 'root', 0)
    run()
