#-*- coding:utf-8 -*-
import sqlite3

class DB_Sqlite3(object):

    @staticmethod
    def Create_Db():
        conn = sqlite3.connect('./spyder.db')
	cur = conn.cursor()
	cur.execute('''CREATE TABLE People_Inf
	               (ID text,           
		        Description text,
			Name_Url text,
			Parent texe,
			Level integer
			)''')
	cur.execute('''CREATE TABLE People
	               (Parent text,
			Level integer,
			Done boolean,
		        Name text
		       )''')
        conn.commit()
	conn.close
