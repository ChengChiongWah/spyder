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
    def init():    #初始化,MyUrl是第一个知乎用户URL
        MyUrl = 'http://www.zhihu.com/people/xie-ke-41'
	UserAgent = 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'
	Headers = {'User-Agent': UserAgent }
	req = urllib2.Request(MyUrl, headers=Headers)
	MyResponse = urllib2.urlopen(req)
	MyPage = MyResponse.read()
	UnicodePage = BeautifulSoup(MyPage, 'html5lib').prettify()
        
	Title_Section = re.findall(r'<div class="title-section ellipsis">[\s\S]*?"name">\n[ ]{10}(.*?)\n', UnicodePage, re.S)   #Title_Section:用户昵称
	Description = re.findall(r'<span class="description unfold-item">\n\s*<span class="con.*?>\n\s*(.*?)\n', UnicodePage, re.S)   #用户签名
	People = re.findall(r'<a class="author-link.*?" data-tip="p\$t\$(.*?)" href=.*?people.*?" target.*?">', UnicodePage, re.S)    #Peopel:用户账号下面赞同其他回答的答主列表 
        conn = sqlite3.connect('spyder.db')
	cur = conn.cursor()
#	print Title_Section[0].encode('utf-8'),'\n', Description[0].encode('utf-8')
	cur.execute("insert into People_Inf values(?, ?, ?)", (Title_Section[0], Description[0], "xie-ke-41"))
	for people_list in list(set(People)):
	    cur.execute("insert into People values(?)",(people_list,))
	cur.close()
	conn.commit()
	conn.close()
        
    def spyder(self, people):
	MyUrl = 'http://www.zhihu.com/people/' + people[0]
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
	        cur.execute("insert into People_Inf values(?, ?, ?)", (Title_Section[0], None, people[0])) 
#		print Title_Section[0]
	    else:
	        cur.execute("insert into People_Inf values(?, ?, ?)", (Title_Section[0], Description[0], people[0]))
#		print Title_Section[0], Description[0], people[0]
	    cur.execute("delete from People where name = ?", (people))
	    cur.close()
	    conn.commit()
	    conn.close()

#	    print list(set(People))
	    for people_list in list(set(People)):
		conn2 = sqlite3.connect("./spyder.db")
		cur2 = conn2.cursor()
		cur2.execute('select count(*) from People_Inf where Name_Url=?', (people_list,))
		cur2_len =  cur2.fetchall()[0][0]
		if cur2_len == 0:
		    cur2.execute("insert into People values(?)", (people_list,))
		    cur2.close()
		    conn2.commit()
		    conn2.close()
		    self.spyder((people_list,))
	except :
	    print people,  "there is a error occored" 
	     

    @classmethod
    def run(cls):
        conn = sqlite3.connect('./spyder.db')
	cur = conn.cursor()
	cur.execute('select * from People')
	cur_feall = cur.fetchall()
	cur.close()
	conn.close()
	for people in cur_feall:
	    Spyder_Model().spyder(people)

if __name__ == '__main__':
    if os.path.exists('./spyder.db'):
        pass
    else:
        DB_Sqlite3.Create_Db()
	Spyder_Model.init()
    Spyder_Model.run()
