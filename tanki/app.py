from pathlib import Path
from textual.app import App
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Input, Label, Static

from tanki.card import CardScreen
from tanki.decks import Deck, DeckList
from tanki.repository import get_all_decks


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
		("g", "card", "Card")
	]

	def get_default_screen(self):
		self.main_screen = MainScreen(self.push_screen)
		return self.main_screen

	def action_exit(self):
		self.app.exit()
