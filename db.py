#-*- coding:utf-8 -*-
import sqlite3
import psycopg2

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

class DB_PostgreSql(object):

    @staticmethod
    def Create_Db():
        conn = psycopg2.connect(database="spyderdb", user="dbuser", password="dbuser", host="127.0.0.1", port="5432")
#	print "connect database successfully"

	cur = conn.cursor()
	cur.execute("""Create table People_Inf
	        (Id  text,
		 Description text,
		 Name_Url text,
		 Parent text,
		 Level int);""")
        cur.execute("""Create table People
	        (Parent text,
		Level int,
		Done boolean,
		Name text);""")
#	print "Create table successfully"

	conn.commit()
	conn.close()

