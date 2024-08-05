from textual import on
from textual.containers import Grid, Horizontal, VerticalScroll
from textual.widgets import Button, Label, Static

from tanki.card import CardScreen
from tanki.repository.card import get_difficulty
from tanki.widgets.container import BorderBody


class Statistic(Horizontal):
	def __init__(self, distribution):
		super().__init__()
		self.distribution = distribution

	def compose(self):
		yield Label('{:02d}'.format(self.distribution["hard"]), id="s_hard")
		yield Label('{:02d}'.format(self.distribution["good"]), id="s_good")
		yield Label('{:02d}'.format(self.distribution["easy"]), id="s_easy")

class Deck(Grid):
	def __init__(self, deck_id, title, description, push_card):
		super().__init__()
		self.deck_id = deck_id
		self.title = title
		self.description = description
		self.push_card = push_card
		self.statistic = get_difficulty(deck_id)

	def compose(self):
		yield Label(self.title, id="title")
		yield Statistic(self.get_distribution())
		yield Button("Go", id="go")
		yield Label(self.description, id="description")

	@on(Button.Pressed, "#go")
	def view_card(self):
		self.push_card(CardScreen(self.deck_id))

	def get_distribution(self):
		distribution = {"hard": 0, "good": 0, "easy": 0}
		for item in self.statistic:
			if item[0] <= 4:
				distribution["easy"] = distribution["easy"] + 1
			elif item[0] >= 7:
				distribution["hard"] = distribution["hard"] + 1
			else:
				distribution["good"] = distribution["good"] + 1
		return distribution


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
