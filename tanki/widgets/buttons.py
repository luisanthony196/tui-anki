from textual.color import Color
from textual.widgets import Button, Static


class CustomButton(Static):
	def __init__(self, label, action, id):
		self.label = label
		self.action = action
		super().__init__(self.label, id=id, classes="custom_btm")

	def on_mount(self):
		self.styles.content_align = ("center", "middle")

	def on_click(self):
		self.action()
