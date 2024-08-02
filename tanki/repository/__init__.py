import os
from tanki.database.turso import conn


def create_tables():
	path = os.path.join(os.getcwd(), 'tanki', 'database', 'statements.sql')
	with open(path, 'r') as file:
		script = file.read()

	conn.executescript(script)
	conn.commit()

def commit():
	if conn.in_transaction:
		conn.commit()

def sync():
	conn.sync()
