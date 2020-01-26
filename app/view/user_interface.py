from app.view import Gtk, Gdk


class UserInterface:
    builder = Gtk.Builder()
    window = None;

    def __init__(self):
        self.builder.add_from_file(f"ui/{self.__class__.__name__}.glade")
        self.window = self.builder.get_object("main_window")

        self.window.connect("key-release-event", self.key_pressed)
        self.window.connect("destroy", self.quit)

        self.window.show_all()

    def key_pressed(self, widget, event):
        if event.keyval == Gdk.KEY_Escape:
            self.quit(widget)

    def quit(self, widget=None):
        self.window.destroy()