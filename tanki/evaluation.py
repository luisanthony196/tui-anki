from fsrs import Card, Rating
from fsrs.fsrs import FSRS
from textual.app import log
from textual.reactive import reactive
from textual.containers import Grid
from textual.widgets import Static

from tanki.repository.card import update_review

alg_fsrs = FSRS()

class QualifyButton(Static):
	content=reactive("")

	def __init__(self, action, id, border_name):
		self.param = id
		self.action = action
		self.border_name = border_name
		super().__init__(id=id, classes="custom_btm")

	def render(self):
		return self.content

	def on_mount(self):
		self.styles.content_align = ("center", "middle")
		self.border_title = self.border_name

	def on_click(self):
		self.action(self.param)

class Evaluation(Grid):
	def __init__(self, qualify, id, classes):
		self.qualify = qualify
		super().__init__(id=id, classes=classes)

	def compose(self):
		yield QualifyButton(action=self.qualify, id="hard", border_name="Hard")
		yield QualifyButton(action=self.qualify, id="good", border_name="Good")
		yield QualifyButton(action=self.qualify, id="easy", border_name="Easy")
