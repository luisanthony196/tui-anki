from tanki.database import conn, cursor

def create_table():
			conn.execute("""CREATE TABLE IF NOT EXISTS decks(
				id integer primary key,
				name text,
				description text
				)""")

			conn.execute("""CREATE TABLE IF NOT EXISTS cards(
				id integer primary key,
				front_content text not null,
				back_content text not null,
				created_at datetime not null,
				decks_id integer not null,
				foreign key(decks_id) references decks(id)
				)""")

create_table()

def get_all_decks():
	cursor.execute('SELECT * from decks')
	results = cursor.fetchall()
	return results

def insert_deck():
	cursor.execute('INSERT INTO cards VALUES (?,?,?,?,?)',(1,"Can I get that","Puedo tenerlo?","fecha",1))
	conn.sync()
	conn.commit()

def insert_card():
	cursor.execute('INSERT INTO decks VALUES (4, "part 4", "Cuarta parte de los decks")')
	conn.sync()
	conn.commit()


def get_cards_by_deck(deck_id):
	cursor.execute('SELECT * from cards WHERE decks_id=?', (deck_id,))
	results = cursor.fetchall()
	return results

print(get_cards_by_deck(1))

def commit():
	conn.commit()
