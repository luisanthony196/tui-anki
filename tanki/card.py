from datetime import datetime
from fsrs import *
from textual import on
from textual.reactive import reactive
from textual.containers import Grid, Horizontal
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label, Static

from tanki.buttons import CustomButton, QualifyButton
from tanki.container import BorderBody
from tanki.repository import get_cards_by_deck, get_next_card, update_card_review


f = FSRS()

class ContentDisplay(Static):
	DEFAULT_CSS = """
	ContentDisplay {
		text-style: bold;
	}
	"""
	content = reactive("")

	def watch_content(self):
		self.update(self.content)

class CardBody(Grid, BorderBody):
	def __init__(self, border_name):
		Grid().__init__(self)
		BorderBody.__init__(self, border_name)

class CardScreen(Screen[None]):
	BINDINGS = [
		("escape", "dismiss('')", "Return")
	]
	front_content = ""
	back_content = ""
	def __init__(self, deck_id):
		super().__init__()
		self.deck_id = deck_id
		self.count = 0
		# TODO Crear un metodo que pida la siguiente carta
		self.cards = get_next_card(self.deck_id)
		self.set_card()

	def set_card(self):
		self.front_content, self.back_content, review_id, difficulty, due, elapsed_days, scheduled_days, lapses, last_review, reps, stability, state, self.card_id = self.cards[self.count]
		self.card = Card(datetime.fromisoformat(due), stability, difficulty, elapsed_days, scheduled_days, reps, lapses, state, datetime.fromisoformat(last_review))

	def compose(self):
		yield Header()
		with CardBody("Card"):
			yield ContentDisplay(self.front_content)
		yield CustomButton("Show Answer", action=self.show_answer, id="show")
		with Grid(id="btn_group", classes="lock"):
			yield QualifyButton("1 day", border_name="Hard", action=self.qualify, rating=Rating.Hard, id="hard")
			yield QualifyButton("1 month", border_name="Good", action=self.qualify, rating=Rating.Good, id="good")
			yield QualifyButton("1 year", border_name="Easy", action=self.qualify, rating=Rating.Easy, id="easy")
		yield Footer()

	def on_mount(self):
		self.query_one(ContentDisplay).content = f'{self.front_content}'

	def qualify(self, rating):
		# Update card review
		card, review_log = f.review_card(self.card, rating)
		update_card_review(card=card, card_id=self.card_id)
		# Set next card
		self.count = self.count + 1
		if self.count >= len(self.cards):
			self.cards = get_next_card(self.deck_id)
			self.count = 0
		self.set_card()
		# Update UI for next
		self.query_one("#show").remove_class("lock")
		self.query_one("#btn_group").add_class("lock")
		self.query_one(ContentDisplay).content = f'{self.front_content}'

	def show_answer(self):
		self.query_one("#show").add_class("lock")
		self.query_one("#btn_group").remove_class("lock")
		# self.qanda = f'{self.qanda}\n\n{self.card[2]}'
		self.query_one(ContentDisplay).content = f'{self.front_content}\n\n\n{self.back_content}'
