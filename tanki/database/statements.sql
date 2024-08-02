CREATE TABLE IF NOT EXISTS decks(
	id integer primary key,
	name text not null,
	description text
);

CREATE TABLE IF NOT EXISTS cards(
	id integer primary key,
	front_content text not null,
	back_content text not null,
	created_at datetime,
	deck_id integer not null,
	foreign key(deck_id) references decks(id)
);

CREATE TABLE IF NOT EXISTS reviews(
	id integer primary key,
	difficulty numeric(5,6) not null,
	due datetime not null,
	elapsed_days integer not null,
	scheduled_days integer not null,
	lapses integer not null,
	last_review datetime,
	reps integer not null,
	stability numeric(5,6) not null,
	state integer not null,
	card_id integer not null,
	foreign key(card_id) references cards(id)
);
