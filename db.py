#-*- coding:utf-8 -*-
import sqlite3

class DB_Sqlite3(object):

    @staticmethod
    def Create_Db():
        conn = sqlite3.connect('./spyder.db')
	cur = conn.cursor()
	cur.execute('''CREATE TABLE People_Inf
	               (ID text,
		        description text,
			Name_Url text
			)''')
	cur.execute('''CREATE TABLE People
	               (name text
		       )''')
        conn.commit()
	conn.close
