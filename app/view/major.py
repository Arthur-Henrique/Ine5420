from app.view import UserInterface, Gtk
from app.view.component import *
from core import __project__


class MajorView(UserInterface):
    object_list = None
    drawing_area = None
    transformation = None
    logger = None

    def __init__(self):
        super().__init__()

        self.object_list = ObjectListComponent(self.builder)
        self.drawing_area = DrawingAreaComponent(self.builder)
        self.transformation = TransformationComponent(self.builder)
        self.logger = LogComponent(self.builder)

        __project__("log", welcome="""
            Interactive graphic system project
            
            Arthur Henrique Della Fraga
            Federal University of Santa Catarina""")

    def key_pressed(self, widget, event):
        super(MajorView, self).key_pressed(widget, event)

    def quit(self, widget):
        super(MajorView, self).quit()
        Gtk.main_quit();