import urllib2
import re, sys

class Spider_Model(object):
    
    def __init__(self):
        self.name = []

    def GetPage(self):
        MyUrl = 'https://www.zhihu.com/people/xie-ke-41'
	UserAgent = 'Mozilla/4.0(compatible; MSIE 5.5; Windows NT)'
	Headers = {'User-Agent': UserAgent }
	req = urllib2.Request(MyUrl, headers=Headers)
	MyResponse = urllib2.urlopen(req)
	MyPage = MyResponse.read()

	UnicodePage = MyPage.decode('utf-8')
        
	MyItems1 = re.findall('<span class="name">(.*?)</span>', UnicodePage, re.S)
	MyItems2 = re.findall('<span class="bio">(.*?)</span>', UnicodePage, re.S)
	LocationItem = re.findall('<span class="location item" title="(.*?)"></span>', UnicodePage, re.S)
	return LocationItem[0].encode('utf-8') 

Spyder = Spider_Model()

if __name__ == '__main__':
    print Spyder.GetPage()
