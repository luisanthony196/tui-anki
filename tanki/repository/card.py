from datetime import datetime, timezone

from tanki.database.turso import conn, cursor

def insert_card(front_content, back_content, deck_id):
	created_at = datetime.now(timezone.utc)
	card_data = cursor.execute(f'INSERT INTO cards (front_content, back_content, created_at, deck_id) VALUES ("{front_content}","{back_content}","{created_at}",{deck_id})')
	review_data = cursor.execute(f'INSERT INTO reviews (difficulty, due, lapses, reps, elapsed_days, scheduled_days, stability, state, card_id) VALUES ({0},"{created_at}",{0},{0},{0},{0},{0},{0},{cursor.lastrowid})')
	conn.commit()

# insert_card("In the meantime", "Mientras tanto", 1)
# insert_card("By the way", "Por cierto", 1)
# insert_card("Therefore", "Por lo tanto", 1)
# insert_card("Unless", "A menos que", 1)
# insert_card("In spite of", "A pesar de", 1)

def get_cards_by_deck(deck_id):
	cursor.execute(f'SELECT * from cards WHERE deck_id={deck_id}')
	results = cursor.fetchall()
	return results

def get_next_card(deck_id):
	cursor.execute(f'SELECT cards.front_content, cards.back_content, reviews.* FROM cards INNER JOIN reviews ON cards.id = reviews.card_id WHERE cards.deck_id={deck_id} ORDER BY reviews.due')
	results = cursor.fetchall()
	return results

def update_review(card, card_id):
	cursor.execute(f'UPDATE reviews SET due="{card.due}",stability={card.stability},difficulty={card.difficulty},elapsed_days={card.elapsed_days},scheduled_days={card.scheduled_days},reps={card.reps},lapses={card.lapses},state={card.state},last_review="{card.last_review}" WHERE card_id={card_id}')
