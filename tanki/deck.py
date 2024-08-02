from textual import on
from textual.containers import Grid, Horizontal, VerticalScroll
from textual.widgets import Button, Label, Static

from tanki.card import CardScreen
from tanki.widgets.container import BorderBody


class Statistic(Horizontal):
	def compose(self):
		yield Label("02", id="s_hard")
		yield Label("32", id="s_good")
		yield Label("12", id="s_easy")

class Deck(Grid):
	def __init__(self, deck_id, title, description, push_card):
		super().__init__()
		self.deck_id = deck_id
		self.title = title
		self.description = description
		self.push_card = push_card

	def compose(self):
		yield Label(self.title, id="title")
		yield Statistic()
		yield Button("Go", id="go")
		yield Label(self.description, id="description")

	@on(Button.Pressed, "#go")
	def view_card(self):
		self.push_card(CardScreen(self.deck_id))

class DeckList(VerticalScroll, BorderBody):
	def __init__(self, deck_list, push_card):
		VerticalScroll.__init__(self)
		BorderBody.__init__(self, "Decks")
		self.deck_list = deck_list
		self.push_card = push_card

	def compose(self):
		for deck in self.deck_list:
			deck_id, title, description = deck
			yield Deck(deck_id, title, description, self.push_card)
