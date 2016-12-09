import sqlite3 as lite

def wrapper(list_tuples):
	db_connect = lite.connect('cittadini.db')
	db_name = "Citizens"
	cur = db_connect.cursor()
	cur.execute("DROP TABLE " + db_name)
	cur.execute("CREATE TABLE Citizens(Id INT, Nome TEXT, Age INT, Sex TEXT, Civ TEXT)")

	for entry in list_tuples:
		cur.execute("INSERT INTO Citizens(Id, Nome, Age, Sex, Civ) VALUES " + str(entry))
	db_connect.commit()
