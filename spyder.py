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
        
	Title_Section = re.findall(r'<span class="name">(.*?)</span>(.*?)<span class="bio.*?>(.*?)</span>', UnicodePage, re.S)
	Location = re.findall(r'<span class="location.*?><a.*?>(.*?)</a></span>', UnicodePage, re.S)
	Business_Item = re.findall(r'<span class="business item".*?><a.*?>(.*?)</a></span>', UnicodePage, re.S)
	Employment_Item = re.findall(r'<span class="employment item".*?><a.*?>(.*?)</a></span>', UnicodePage, re.S)
	Education_Item = re.findall(r'<span class="education item".*?>(.*?)</span>.|\n<span class="education-extra.*?>(.*?)</span>', UnicodePage, re.S)
	Description = re.findall(r'<span class="description unfold.*?">\n<span class="cont.*?>\n\n(.*?)\n\n</span>', UnicodePage, re.S)
	return Description, #Education_Item, Employment_Item, Business_Item, Location, ''.join(Title_Section[0])

Spyder = Spider_Model()

if __name__ == '__main__':
    print Spyder.GetPage()
