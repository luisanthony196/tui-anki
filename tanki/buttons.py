from textual.color import Color
from textual.widgets import Button, Static


class CustomButton(Static):
	DEFAULT_CSS = """
		CustomButtom {
			min-width: 4;
			height: 3;
			display: block;
		}
	"""
	def __init__(self, label, action, id):
		self.label = label
		self.action = action
		super().__init__(self.label, id=id)

	def on_mount(self):
		self.styles.content_align = ("center", "middle")

	def on_click(self):
		self.action()


class QualifyButton(Static):
	DEFAULT_CSS = """
		CustomButtom {
			min-width: 4;
			height: 3;
			display: block;
		}
	"""
	def __init__(self, label, action, rating, id, border_name):
		self.label = label
		self.action = action
		self.rating = rating
		self.border_name = border_name
		super().__init__(self.label, id=id)

	def on_mount(self):
		self.styles.content_align = ("center", "middle")
		self.border_title = self.border_name

	def on_click(self):
		self.action(self.rating)
