import sqlite3



conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()


conn2 = sqlite3.connect('db2.sqlite3')
cursor2 = conn2.cursor()


for i in cursor2.execute("SELECT id, num, title, pub_date, book_id, txt FROM home_chapter"):
	print(i[3])
	s = f"""INSERT INTO home_chapter(id, num, title, pub_date, book_id, txt) 
					  VALUES (?, ?, ?, ?, ?, ?)"""
	print(s.find("!"))
	try:
		cursor.execute(s, i)
	except Exception as e:
		print(e)
		break
	conn.commit()