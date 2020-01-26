import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

from app.view.user_interface import UserInterface
from app.view.major import MajorView


def run():
    MajorView()
    Gtk.main()




