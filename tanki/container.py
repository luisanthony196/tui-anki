from textual.containers import Container


class BorderBody(Container):
	def __init__(self, border_name):
		super().__init__()
		self.border_name = border_name

	def on_mount(self):
		self.border_title = self.border_name
		self.styles.border = ("round", "orange")
		self.styles.padding = (0, 2)
