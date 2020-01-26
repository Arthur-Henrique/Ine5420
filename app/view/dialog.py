from app.view import UserInterface


class Dialog(UserInterface):
    def __init__(self, title, text):
        super().__init__()

        self.window.set_title(title)
        self.builder.get_object("text").set_text(text)
        self.builder.get_object("ok_button").connect("clicked", self.quit)
