from pathlib import Path
from textual.app import App
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Input, Label, Static

from tanki import repository
from tanki.card import CardScreen
from tanki.deck import Deck, DeckList
from tanki.repository.deck import get_all_decks

repository.sync()
repository.create_tables()

class MainScreen(Screen[None]):
	decks = []

	def __init__(self, push_card):
		super().__init__()
		self.decks = get_all_decks()
		self.push_card = push_card

	def compose(self):
		yield Header()
		with Vertical():
			yield Input()
			yield DeckList(self.decks, self.push_card)
		yield Footer()

class TankiApp(App[None]):
	def __init__(self):
		super().__init__()

class Tanki(TankiApp):
	CSS_PATH = Path(__file__).parent / "tanki.scss"
	BINDINGS = [
		("q", "exit", "Exit"),
		("s", "sync_and_commit", "Save progress")
	]

	def get_default_screen(self):
		self.main_screen = MainScreen(self.push_screen)
		return self.main_screen

	def action_sync_and_commit(self):
		repository.commit()

	def action_exit(self):
		repository.commit()
		self.app.exit()
