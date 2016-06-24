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
        MyUrl = 'http://www.zhihu.com/people/kong-qing-xun'
	UserAgent = 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'
	Headers = {'User-Agent': UserAgent }
	req = urllib2.Request(MyUrl, headers=Headers)
	MyResponse = urllib2.urlopen(req)
	MyPage = MyResponse.read()
	UnicodePage = BeautifulSoup(MyPage, 'html5lib').prettify()
        
	Title_Section = re.findall(r'<div class="title-section.*?<span class="name">(.*?)</span>', UnicodePage, re.S)
	Location = re.findall(r'<span class="location item" title="(.*?)">', UnicodePage, re.S)
	Business_Item = re.findall(r'<span class="business item" title="(.*?)">', UnicodePage, re.S)
	Employment_Item = re.findall(r'<span class="employment item" title="(.*?)">', UnicodePage, re.S)
	Education_Item = re.findall(r'<span class="education item" title="(.*?)">.*?</span>', UnicodePage, re.S)
	Education_Extra_Item = re.findall(r'<span class="education-extra item" title=["\'](.*?)[\'"]>.*?</span>', UnicodePage, re.S)
	Description = re.findall(r'<span class="description unfold-item">\n\s*<span class="con.*?>\n\s*(.*?)\n', UnicodePage, re.S)
	People = re.findall(r'<a class="author-link.*?" data-tip="p\$t\$(.*?)" href=.*?people.*?" target.*?">', UnicodePage, re.S)
#	print Title_Section[:], '\n', Location, '\n', Business_Item, '\n', Employment_Item, '\n', Education_Item, '\n', Education_Extra_Item, '\n', Description, '\n', list(set(People))
        conn = sqlite3.connect('spyder.db')
	cur = conn.cursor()
	sql = "insert into People_Inf values('%s', '%s', '%s', '%s', '%s', '%s', '%s')" %(Title_Section[0], Location[0], Business_Item[0], Employment_Item[0], Education_Item[0], Education_Extra_Item[0], Description[0])
	cur.execute(sql)
	for people_list in list(set(People)):
	    cur.execute("insert into People values('%s')" %(people_list))
	cur.close()
	conn.commit()
	conn.close()
        
    def spyder(self, people):
        try:
	    MyUrl = 'http://www.zhihu.com/people/' + people[0]
	    UserAgent = 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'
	    Headers = {'User-Agent': UserAgent }
	    req = urllib2.Request(MyUrl, headers=Headers)
	    MyResponse = urllib2.urlopen(req)
	    MyPage = MyResponse.read()
	    UnicodePage = BeautifulSoup(MyPage, 'html5lib').prettify()
	    Title_Section = re.findall(r'<div class="title-section.*?<span class="name">(.*?)</span>', UnicodePage, re.S)
	    Location = re.findall(r'<span class="location item" title="(.*?)">', UnicodePage, re.S)
	    Business_Item = re.findall(r'<span class="business item" title="(.*?)">', UnicodePage, re.S)
	    Employment_Item = re.findall(r'<span class="employment item" title="(.*?)">', UnicodePage, re.S)
	    Education_Item = re.findall(r'<span class="education item" title="(.*?)">.*?</span>', UnicodePage, re.S)
	    Education_Extra_Item = re.findall(r'<span class="education-extra item" title=["\'](.*?)[\'"]>.*?</span>', UnicodePage, re.S)
	    Description = re.findall(r'<span class="description unfold-item">\n\s*<span class="con.*?>\n\s*(.*?)\n', UnicodePage, re.S)
	    People = re.findall(r'<a class="author-link.*?" data-tip="p\$t\$(.*?)" href=.*?people.*?" target.*?">', UnicodePage, re.S)
	    conn = sqlite3.connect('./spyder.db')
	    cur = conn.cursor()
	    sql = "insert into People_Inf values('%s', '%s', '%s', '%s', '%s', '%s', '%s')" %(Title_Section[0], Location[0], Business_Item[0], Employment_Item[0], Education_Item[0], Education_Extra_Item[0], Description[0]) 
	    cur.execute(sql)
	    print list(set(People))
	    for people_list in list(set(People)):
		cur.execute('select name from People where name=?', (people_list,))
		print people_list
		if cur.fetchone() is None:
		    cur.execute("insert into People values('%s')"(people_list,))
	    cur.close()
	    conn.commit()
	    conn.close()
	except (ValueError, IndexError, TypeError), e:
	    print ('Error:', e)

    @classmethod
    def run(cls):
        conn = sqlite3.connect('./spyder.db')
	cur = conn.cursor()
	try:
	    cur.execute('select * from People')
	    for people in cur.fetchall():
	        Spyder_Model().spyder(people)
        except (ValueError, TypeError), e:
	    print e


if __name__ == '__main__':
    if os.path.exists('./spyder.db'):
        pass
    else:
        DB_Sqlite3.Create_Db()
	Spyder_Model.init()
    Spyder_Model.run()
