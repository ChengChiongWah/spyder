1.这是项目“Python爬虫程序”(https://github.com/ChengChiongWah/spyder)
  克隆版本库操作实例(# git clone git@github.com:ChengChiongWah/spyder.git)
  该程序只在linux平台下做过测试，建议在linux下使用。

2.本程序使用Python2.7,分别使用两种数据库Sqlite3 和postgresql，要使用哪一种数据库只需要选择对应的程序（spyder_postgresql.py 或 spyder_sqlite3)运行即可.

3.使用BeautifulSoup 解析网页，正则表达式做匹配，使用广度优先算法进行遍历*乎网站。

4.原理：每一个用户页面都有对应的一个URL：zhihu.com/people/somebody,同时每一个页面都有该用户关注用户的动态，所以，爬下该用户页下面的被关注用户的ID，按zhihu.com/people/**ID**进行递归遍历即可。

5.该程序目前只爬了用户的：昵称， 个性签名。
