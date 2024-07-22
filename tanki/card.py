from textual import on
from textual.reactive import reactive
from textual.containers import Grid, Horizontal
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label, Static

from tanki.buttons import CustomButton
from tanki.container import BorderBody
from tanki.repository import get_cards_by_deck


class ContentDisplay(Static):
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
	def __init__(self, deck_id):
		super().__init__()
		self.deck_id = deck_id
		# TODO Crear un metodo que pida la siguiente carta
		self.card = get_cards_by_deck(self.deck_id)[0]

	def compose(self):
		yield Header()
		with CardBody("Card"):
			yield ContentDisplay(self.card[1])
		yield CustomButton("Show Answer", action=self.show_answer, id="show")
		with Grid(id="btn_group", classes="lock"):
			yield CustomButton("1 day", border_name="Hard", action=None, id="hard")
			yield CustomButton("1 month", border_name="Mid", action=None, id="mid")
			yield CustomButton("1 year", border_name="Easy", action=None, id="easy")
		yield Footer()

	def on_mount(self):
		self.query_one(ContentDisplay).content = f'{self.card[1]}'

	def show_answer(self):
		self.query_one("#show").add_class("lock")
		self.query_one("#btn_group").remove_class("lock")
		# self.qanda = f'{self.qanda}\n\n{self.card[2]}'
		self.query_one(ContentDisplay).content = f'{self.card[1]}\n\n\n{self.card[2]}'
