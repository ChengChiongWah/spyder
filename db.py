import sqlite3

class DB_Sqlite3(object):

    @staticmethod
    def Create_Db():
        conn = sqlite3.connect('./spyder.db')
	cur = conn.cursor()
	cur.execute('''CREATE TABLE People_Inf
	               (name text,
		        location text,
			business_item text,
			employ_item text,
			education_item text,
			education_extra_item text,
			description text
			)''')
	cur.execute('''CREATE TABLE People
	               (name text
		       )''')
        conn.commit()
	conn.close
