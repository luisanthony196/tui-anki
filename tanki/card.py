from datetime import datetime
from fsrs import FSRS, Card, Rating
from textual import on
from textual.reactive import reactive
from textual.containers import Grid, Horizontal
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label, Static

from tanki import repository
from tanki.evaluation import Evaluation, QualifyButton
from tanki.repository.card import get_next_card, update_review
from tanki.widgets.buttons import CustomButton
from tanki.widgets.container import BorderBody

alg_fsrs = FSRS()

class ContentDisplay(Static):
	content = reactive("")

	def render(self):
		return self.content

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
		self.card_eval = {}
		self.deck_id = deck_id
		self.card_list = get_next_card(self.deck_id)
		self.set_card()

	def on_mount(self):
		self.query_one(ContentDisplay).content = f'{self.front_content}'

	def compose(self):
		yield Header()
		with CardBody("Card"):
			yield ContentDisplay(self.front_content)
		yield CustomButton("Show Answer", action=self.show_answer, id="show")
		yield Evaluation(self.qualify, id="btn_group", classes="lock")
		yield Footer()

	def set_card(self):
		self.front_content, self.back_content, review_id, difficulty, due, elapsed_days, scheduled_days, lapses, last_review, reps, stability, state, self.card_id = self.card_list.pop(0)

		if last_review:
			last_review = datetime.fromisoformat(last_review)

		card = Card(datetime.fromisoformat(due), stability, difficulty, elapsed_days, scheduled_days, reps, lapses, state, last_review)
		self.card_eval["hard"], _ = alg_fsrs.review_card(card, Rating.Hard)
		self.card_eval["good"], _ = alg_fsrs.review_card(card, Rating.Good)
		self.card_eval["easy"], _ = alg_fsrs.review_card(card, Rating.Easy)

	def qualify(self, value):
		# Update card review
		update_review(card=self.card_eval[value], card_id=self.card_id)
		# Set next card
		if not self.card_list:
			repository.commit() # Pushear los cambios hechos con update y obtener nuevos
			self.card_list = get_next_card(self.deck_id)
		self.set_card()
		# Update UI for next
		self.query_one("#show").remove_class("lock")
		self.query_one("#btn_group").add_class("lock")
		self.query_one(ContentDisplay).content = f'{self.front_content}'

	def show_answer(self):
		self.query_one("#show").add_class("lock")
		self.query_one("#btn_group").remove_class("lock")
		self.query_one(ContentDisplay).content = f'{self.front_content}\n\n\n{self.back_content}'
		self.query_one('#hard', QualifyButton).content = f'{self.get_space(self.card_eval["hard"])}'
		self.query_one('#good', QualifyButton).content = f'{self.get_space(self.card_eval["good"])}'
		self.query_one('#easy', QualifyButton).content = f'{self.get_space(self.card_eval["easy"])}'

	def get_space(self, card: Card):
		r = card.due - card.last_review
		d = r.days
		if d == 0:
			h = r.seconds // 3600
			if h == 0:
				m = (r.seconds % 3600) // 60
				return f'En {m} minutos'
			else:
				return f'En {h} horas'
		return f'En {d} dias'
