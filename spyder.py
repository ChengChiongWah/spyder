#-*- coding:utf-8 -*-
import urllib2
import re
import os
import sys, types
import logging, logging.handlers
import sqlite3
from db import DB_Sqlite3
from bs4 import BeautifulSoup


def spyder(people):
    
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
        People = re.findall(r'<a class="author-link.*?" data-tip="p\$t\$(.*?)" href=.*?people.*?" target.*?">', UnicodePage, re.S)
        conn = sqlite3.connect('./spyder.db')
        cur = conn.cursor()
        if len(Description) == 0 :
            cur.execute("insert into People_Inf values(?, ?, ?)", (Title_Section[0], None, people)) 
#   	print Title_Section[0], None, people[:]
        else:
            cur.execute("insert into People_Inf values(?, ?, ?)", (Title_Section[0], Description[0], people))
#		print Title_Section[0], Description[0], people[:]
#	    cur.execute("delete from People where name = ?", (people))
        cur.close()
        conn.commit()
        conn.close()

	   # print list(set(People))
        for people_list in list(set(People)):
            conn2 = sqlite3.connect("./spyder.db")
	    cur2 = conn2.cursor()
	    cur2.execute('select count(*) from People_Inf where Name_Url=?', (people_list,))
	    cur2_len =  cur2.fetchall()[0][0]
	    if cur2_len == 0:
	#	    cur2.execute("insert into People values(?)", (people_list,))
	        cur2.close()
	        conn2.commit()
	        conn2.close()
		yield  people_list
	        for element in spyder(people_list):
	            yield element
    except BaseException, e:
        logger.debug('there is a error', exc_info=True) 

if __name__ == '__main__':
    if os.path.exists('./spyder.db'):
        pass
    else:
        DB_Sqlite3.Create_Db()
    for gen in spyder('xie-ke-41'):
        print gen
    
