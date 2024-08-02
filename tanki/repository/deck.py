from tanki.database.turso import conn, cursor

def get_all_decks():
	cursor.execute('SELECT * from decks')
	results = cursor.fetchall()
	return results

def insert_deck(name, desc):
	cursor.execute(f'INSERT INTO decks (name, description) VALUES ("{name}", "{desc}")')
	conn.commit()
