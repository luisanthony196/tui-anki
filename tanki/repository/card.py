from datetime import datetime, timezone

from tanki.database.turso import conn, cursor

def insert_card(front_content, back_content, deck_id):
	created_at = datetime.now(timezone.utc)
	card_data = cursor.execute(f'INSERT INTO cards (front_content, back_content, deck_id) VALUES ("{front_content}","{back_content}",{deck_id})')
	review_data = cursor.execute(f'INSERT INTO reviews (card_id) VALUES ({cursor.lastrowid})')
	conn.commit()

def get_cards_by_deck(deck_id):
	cursor.execute(f'SELECT * from cards WHERE deck_id={deck_id}')
	results = cursor.fetchall()
	return results

def get_next_card(deck_id):
	cursor.execute(f'SELECT c.front_content, c.back_content, r.* FROM cards as c INNER JOIN reviews as r ON c.id = r.card_id WHERE c.deck_id={deck_id} ORDER BY r.due')
	results = cursor.fetchall()
	return results

def update_review(card, card_id):
	cursor.execute(f'UPDATE reviews SET due="{card.due}",stability={card.stability},difficulty={card.difficulty},elapsed_days={card.elapsed_days},scheduled_days={card.scheduled_days},reps={card.reps},lapses={card.lapses},state={card.state},last_review="{card.last_review}" WHERE card_id={card_id}')

def get_difficulty(deck_id):
	cursor.execute(f'SELECT r.difficulty FROM cards AS c INNER JOIN reviews AS r ON c.id = r.card_id WHERE c.deck_id = {deck_id}')
	results = cursor.fetchall()
	return results
