import libsql_experimental as libsql
from dotenv import load_dotenv
import os


class Turso():
	def __init__(self, database, url, token):
		self.database = database
		self.url = url
		self.token = token
		self.connection = None

	def connect(self):
		self.connection = libsql.connect(self.database, sync_url=self.url, auth_token=self.token)
		return self.connection

load_dotenv()
database = os.getenv("DATABASE")
url = os.getenv("URL")
auth_token = os.getenv("AUTH_TOKEN")

db_instance = Turso(database, url, auth_token)
conn = db_instance.connect()
cursor = conn.cursor()
