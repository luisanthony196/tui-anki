from pathlib import Path
from textual import on
from textual.app import App
from textual.color import Color
from textual.screen import Screen
from textual.containers import Center, Horizontal, ScrollableContainer, Vertical, VerticalScroll
from textual.widgets import Button, Footer, Header, Label, Static
from tanki.repository import get_all_decks, get_cards_by_deck

class CardScreen(Screen):
	def __init__(self, deck_id):
		self.card = get_cards_by_deck(deck_id)[0]
		self.deck_id = deck_id
		super().__init__()

	def compose(self):
		yield Header(show_clock=True)
		yield Footer()
		yield Label(self.card[1])
		with Horizontal():
			yield Button("Hard", id="hard")
			yield Button("Mid", id="mid")
			yield Button("Easy", id="easy")

class Statistic(Horizontal):
	def compose(self):
		yield Label("01", id="hard")
		yield Label("10", id="mid")
		yield Label("15", id="easy")

class Deck(Static):
	def __init__(self, deck_id, title, description, active_card):
		self.deck_id = deck_id
		self.title = title
		self.active_card = active_card
		self.description = description
		super().__init__()

	@on(Button.Pressed, "#go")
	def open_card(self):
		self.active_card(self.deck_id)

	def compose(self):
		yield Label(self.title, id="title")
		yield Statistic()
		yield Button("Go", id="go")
		yield Label(self.description, id="description")

class Decklist(VerticalScroll):
	def __init__(self, active_card):
		self.decks = get_all_decks()
		self.active_card = active_card
		super().__init__(id="decklist")

	def compose(self):
		for deck in self.decks:
			deck_id, title, description = deck
			yield Deck(deck_id, title, description, self.active_card)

	def on_mount(self):
		self.border_title = "Decks"
		self.styles.border = ("round", "orange")

class Tanki(App):
	TITLE = "TANKI"
	CSS_PATH = Path(__file__).parent / "tanki.scss"
	BINDINGS = [
		("q", "exit", "Exit")
	]

	def compose(self):
		yield Header(show_clock=True)
		yield Footer()
		yield Decklist(self.active_card_screen)

	def active_card_screen(self, deck_id):
		self.push_screen(CardScreen(deck_id))


	def action_exit(self):
		self.app.exit()
