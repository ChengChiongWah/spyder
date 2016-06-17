import urllib2
import re, sys
from bs4 import BeautifulSoup

class Spider_Model(object):
    
    def __init__(self):
        self.name = []

    def GetPage(self):
        MyUrl = 'http://www.zhihu.com/people/kong-qing-xun'
	UserAgent = 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'
	Headers = {'User-Agent': UserAgent }
	req = urllib2.Request(MyUrl, headers=Headers)
	MyResponse = urllib2.urlopen(req)
	MyPage = MyResponse.read()

	UnicodePage = BeautifulSoup(MyPage, 'html5lib').prettify()
#	Text = open("txt.txt", "wb")
#	Text.write(MyPage)
#	Text.close()
        
	Title_Section = re.findall(r'<span class="name">(.*?)</span>.*?<span class="bio.*?>.*?</span>', UnicodePage, re.S)
	Location = re.findall(r'<span class="location item" title="(.*?)">', UnicodePage, re.S)
	Business_Item = re.findall(r'<span class="business item" title="(.*?)">', UnicodePage, re.S)
	Employment_Item = re.findall(r'<span class="employment item" title="(.*?)">', UnicodePage, re.S)
	Education_Item = re.findall(r'<span class="education item" title="(.*?)">', UnicodePage, re.S)
	Education_Extra_Item = re.findall(r'<span class="education-extra item" title="(.*?)">', UnicodePage, re.S)
	Description = re.findall(r'<span class="description unfold.*?">\n<span class="cont.*?>\n(.*?)\n.*?</span>', UnicodePage, re.S)
	People = re.findall(r'<a class="author-link" data-tip=.*?href=".*?people/(.*?)">', UnicodePage, re.S) 
	print MyPage, Title_Section[0], '\n', Location[0], '\n', Business_Item, '\n', Employment_Item[0], '\n', Education_Item[0], '\n', Education_Extra_Item, '\n', Description, '\n', People

Spyder = Spider_Model()

if __name__ == '__main__':
    Spyder.GetPage()
