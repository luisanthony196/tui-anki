CREATE TABLE IF NOT EXISTS decks(
	id integer primary key,
	name text not null,
	description text
);

CREATE TABLE IF NOT EXISTS cards(
	id integer primary key,
	front_content text not null,
	back_content text not null,
	created_at datetime default current_timestamp,
	deck_id integer not null,
	foreign key(deck_id) references decks(id)
);

CREATE TABLE IF NOT EXISTS reviews(
	id integer primary key,
	difficulty numeric(5,6) default 0,
	due datetime not null default (datetime('now', 'utc')),
	elapsed_days integer not null default 0,
	scheduled_days integer not null default 0,
	lapses integer not null default 0,
	last_review datetime,
	reps integer not null default 0,
	stability numeric(5,6) not null default 0,
	state integer not null default 0,
	card_id integer not null,
	foreign key(card_id) references cards(id)
);
