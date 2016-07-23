#-*- coding:utf-8 -*-
import urllib2
import re
import os
import sys, types
import logging, logging.handlers
import sqlite3
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
        conn = sqlite3.connect('./spyder.db')
        cur = conn.cursor()
        if len(Description) == 0 :
            cur.execute("insert into People_Inf values(?, ?, ?, ?, ?)", (Title_Section[0], None, people, parent, level)) 
            print Title_Section[0], None, people[:], parent, level,"-------"
        else:
            cur.execute("insert into People_Inf values(?, ?, ?, ?, ?)", (Title_Section[0], Description[0], people, parent, level))
	    print Title_Section[0], Description[0], people[:], parent, level,"--------"
#	    cur.execute("delete from People where name = ?", (people))
        cur.close()
        conn.commit()
        conn.close()

	   # print list(set(People))
        for people_list in list(set(People)):
            conn2 = sqlite3.connect("./spyder.db")
	    cur2 = conn2.cursor()
	    cur2.execute('select count(*) from People where Name=?', (people_list,))
	    cur2_len =  cur2.fetchall()[0][0]
	    if cur2_len == 0:
	        cur2.execute("insert into People values(?, ?, ?, ?)", (people, level+1, False, people_list,))
		#print people_list
	    cur2.close()
	    conn2.commit()
	    conn2.close()
	
    except BaseException, e:
        logger.debug('there is a error', exc_info=True) 

def run():
    while True:
        conn3 = sqlite3.connect("./spyder.db")
	cur3 = conn3.cursor()
	cur3.execute("select min(Level) from People")
	Min_Level = cur3.fetchall()[0]
        cur3.execute("select Name, Parent, Level from People where Level=? and Done=0", Min_Level)
	cur3_list = cur3.fetchall()
	cur3.close()
	conn3.close()
	for element in cur3_list:
	    print element[0]#, element[1], element[2]
	    conn4 = sqlite3.connect("./spyder.db")
	    cur4 = conn4.cursor()
	    cur4.execute("update People set Done=1 where Name=?", (element[0],))
	    cur4.close()
	    conn4.commit()
	    conn4.close()
	    spyder(element[0], element[1], element[2])

if __name__ == '__main__':
    if os.path.exists('./spyder.db'):
        pass
    else:
        DB_Sqlite3.Create_Db()
    spyder('li-de-long-68', 'root', 0)
    run()
