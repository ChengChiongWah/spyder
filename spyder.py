#-*- coding:utf-8 -*-
import urllib2
import re
import os
import sys
import sqlite3
from db import DB_Sqlite3
from bs4 import BeautifulSoup

class Spyder_Model(object):

    @staticmethod
    def init():
        MyUrl = 'http://www.zhihu.com/people/xie-ke-41'
	UserAgent = 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'
	Headers = {'User-Agent': UserAgent }
	req = urllib2.Request(MyUrl, headers=Headers)
	MyResponse = urllib2.urlopen(req)
	MyPage = MyResponse.read()
	UnicodePage = BeautifulSoup(MyPage, 'html5lib').prettify()
        
	Title_Section = re.findall(r'<div class="title-section.*?<span class="name">(.*?)</span>', UnicodePage, re.S)
	Description = re.findall(r'<span class="description unfold-item">\n\s*<span class="con.*?>\n\s*(.*?)\n', UnicodePage, re.S)
	People = re.findall(r'<a class="author-link.*?" data-tip="p\$t\$(.*?)" href=.*?people.*?" target.*?">', UnicodePage, re.S)
        conn = sqlite3.connect('spyder.db')
	cur = conn.cursor()
#	print Title_Section[:], Description[0].encode('utf-8')
	cur.execute("insert into People_Inf values(?, ?)", (Title_Section[0], Description[0]))
	for people_list in list(set(People)):
	    cur.execute("insert into People values(?)",(people_list,))
	cur.close()
	conn.commit()
	conn.close()
        
    def spyder(self, people):
        try:
	    MyUrl = 'http://www.zhihu.com/people/' + people[0]
	    UserAgent = 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'
	    Headers = {'User-Agent': UserAgent }
	    req = urllib2.Request(MyUrl, headers=Headers)
	    print "The people information with error:" + people[0]
	    MyResponse = urllib2.urlopen(req)
	    MyPage = MyResponse.read()
	    UnicodePage = BeautifulSoup(MyPage, 'html5lib').prettify()
	    Title_Section = re.findall(r'<div class="title-section.*?<span class="name">(.*?)</span>', UnicodePage, re.S)
	    Description = re.findall(r'<span class="description unfold-item">\n\s*<span class="con.*?>\n\s*(.*?)\n', UnicodePage, re.S)
	    People = re.findall(r'<a class="author-link.*?" data-tip="p\$t\$(.*?)" href=.*?people.*?" target.*?">', UnicodePage, re.S)
	    conn = sqlite3.connect('./spyder.db')
	    cur = conn.cursor()
	    if len(Description) == 0 :
	        pass
	    else:
		print Title_Section[0].encode('utf-8'), Description[0].encode('utf-8')
	        cur.execute("insert into People_Inf values(?, ?)", (Title_Section[0],  Description[0]))
	    cur.execute("delete from People where name = ?", (people))
	    cur.close()
	    conn.commit()
	    conn.close()

	    for people_list in list(set(People)):
		conn2 = sqlite3.connect("./spyder.db")
		cur2 = conn2.cursor()
		cur2.execute('select name from People_Inf where name=?', (people_list,))
		if cur2.fetchone() is None:
#		    print people_list
		    cur2.execute("insert into People values(?)", (people_list,))
	        cur2.close()
	        conn2.commit()
	        conn2.close()

	    conn1 = sqlite3.connect('./spyder.db')
	    cur1 = conn1.cursor()
	    cur1.execute('select * from People')
	    for people in cur1.fetchall():
#		print people
	        self.spyder(people)
	    cur1.close()
	    conn1.close()
	except (ValueError, IndexError, TypeError), e:
	    print ('Error:', e) 

    @classmethod
    def run(cls):
        conn = sqlite3.connect('./spyder.db')
	cur = conn.cursor()
	try:
	    cur.execute('select * from People')
	    for people in cur.fetchall():
		try:
		    Spyder_Model().spyder(people)
		except:
		   continue 
            cur.close()        
            conn.close()
        except (ValueError, TypeError), e:
	    print e


if __name__ == '__main__':
    if os.path.exists('./spyder.db'):
        pass
    else:
        DB_Sqlite3.Create_Db()
	Spyder_Model.init()
    Spyder_Model.run()
