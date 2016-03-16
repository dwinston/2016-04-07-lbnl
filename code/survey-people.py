import sqlite3
connection = sqlite3.connect("survey.db")
cursor = connection.cursor()
cursor.execute("SELECT Personal || ' ' || Family FROM Person WHERE Personal=?;", ['Frank'])
results = cursor.fetchall()
for r in results:
    print(r)
cursor.close()
connection.close()
