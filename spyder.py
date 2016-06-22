import urllib2
import re, sys
from bs4 import BeautifulSoup

class Spider_Model(object):

    def GetPage(self):
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
	print Title_Section[:], '\n', Location, '\n', Business_Item, '\n', Employment_Item, '\n', Education_Item, '\n', Education_Extra_Item, '\n', Description, '\n', list(set(People))
	print '----------------------------'

Spyder = Spider_Model()

if __name__ == '__main__':
    Spyder.GetPage()
