import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

from app.view.user_interface import UserInterface
from app.view.dialog import Dialog
from app.view.new_geometric_form import NewGeometricFormView
from app.view.major import MajorView


def run():
	MajorView()
	Gtk.main()