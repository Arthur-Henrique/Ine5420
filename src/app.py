import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, cairo

import model
import app

def init():
    global APP_VIEW
    APP_VIEW = AppView()

def run():
    Gtk.main()

class UserInterface:
    builder = Gtk.Builder()
    window = None;

    def __init__(self, filename):
        self.builder.add_from_file("ui/" + filename)
        self.window = self.builder.get_object("main_window")
        self.builder.connect_signals(self)
        self.window.show_all()

class Projection():
    def __init__(self):
        model.PROJECTIONS.append(self);

    def refresh(self, change):
        raise NotImplementedError()

class AppView(UserInterface):
    object_tree_view = None

    object_list = None
    drawing_area = None
    transformation = None

    def __init__(self):
        super().__init__("AppView.glade")

        self.object_tree_view = self.builder.get_object("object_tree_view")

        self.object_list = ObjectListComponent(self.builder)
        self.drawing_area = DrawingAreaComponent(self.builder)
        self.transformation = TransformationComponent(self.builder)

    @property
    def selected_object_id(self):
        (model, path) = self.object_tree_view.get_selection().get_selected_rows()
        return None if not path else int(model.get_value(model.get_iter(path[0]), 0))

    def selection_changed(self, widget):
        self.transformation.set_target(self.selected_object_id)

    def quit(self, widget):
        Gtk.main_quit();

class ObjectListComponent(Projection):
    object_list = None

    def __init__(self, builder):
        super().__init__()

        self.object_list = builder.get_object("object_list")

        builder.get_object("new_object").connect("clicked", self.new_object)
        builder.get_object("delete").connect("clicked", self.delete)
        builder.get_object("clear").connect("clicked", self.clear)

    def new_object(self, widget):
        NewObjectView()

    def delete(self, widget):
        model.OBJECT_MANAGER.delete(APP_VIEW.selected_object_id)

    def clear(self, widget):
        model.OBJECT_MANAGER.clear()

    def refresh(self, change):
        if change == "display_file":
            self.object_list.clear()

            for object in model.OBJECT_MANAGER:
                self.object_list.append([object.id, object.name, object.type])

class NewObjectView(UserInterface):
    def __init__(self):
        super().__init__("NewObjectView.glade")

        self.name_entry = self.builder.get_object("name_entry")
        self.color_button = self.builder.get_object("color_button")
        self.x_entry = self.builder.get_object("x_entry")
        self.y_entry = self.builder.get_object("y_entry")
        self.coordenate_list = self.builder.get_object("coordenate_list")

    def insert(self, widget):
        self.coordenate_list.append([
            int(self.x_entry.get_text()),
            int(self.y_entry.get_text())
        ])

        self.x_entry.set_text("")
        self.y_entry.set_text("")

    def delete_all(self, widget):
        self.coordenate_list.clear()

    def create(self, widget):
        model.OBJECT_MANAGER.create(self.name, self.color, self.coordenates)
        self.window.destroy()

    @property
    def name(self):
        return self.name_entry.get_text()

    @property
    def color(self):
        rgba = self.color_button.get_rgba()
        return (rgba.red, rgba.green, rgba.blue)

    @property
    def coordenates(self):
        return list(tuple(row[:]) for row in self.coordenate_list)

class DrawingAreaComponent(Projection):
    drawing_area = None
    painter = None

    def __init__(self, builder):
        super().__init__()

        self.drawing_area = builder.get_object("drawing_area")
        self.painter = self.drawing_area.get_window().cairo_create()

        self.drawing_area.connect("draw", self.draw)

        area = self.drawing_area.get_allocation()
        model.WINDOW = model.Window((0, 0), (area.width, area.height))
        model.VIEWPORT = model.Viewport() #(50, 50), (area.width-50, area.height-50))

    def draw(self, widget, painter):
        painter.save()
        painter.set_source_rgb(0, 0, 0)
        painter.paint()

        for object in model.OBJECT_MANAGER:
            painter.set_source_rgb(*object.color)

            representation = model.VIEWPORT.ajust(object.coordenates)
            painter.move_to(
                representation[0][0],
                representation[0][1] + 0.5
            )

            for coordenate in representation:
                painter.line_to(*coordenate)

            painter.stroke()

        painter.restore()

    def refresh(self, change):
        self.drawing_area.draw(self.painter)

class TransformationComponent:
    target = None
    measure_entry = None
    reference_option_group = None

    def __init__(self, builder):
        super().__init__()

        self.measure_entry = builder.get_object("transformation_measure_entry")
        self.reference_option_group = builder.get_object("window_reference_radio").get_group()
        self.set_target(None)

        builder.get_object("move_up").connect("clicked", self.move, model.Direction.UP)
        builder.get_object("move_left").connect("clicked", self.move, model.Direction.LEFT)
        builder.get_object("move_down").connect("clicked", self.move, model.Direction.DOWN)
        builder.get_object("move_right").connect("clicked", self.move, model.Direction.RIGHT)

        builder.get_object("turn_left").connect("clicked", self.turn, model.Direction.LEFT)
        builder.get_object("turn_right").connect("clicked", self.turn, model.Direction.RIGHT)

        builder.get_object("zoom_in").connect("clicked", self.zoom, model.Direction.DOWN)
        builder.get_object("zoom_out").connect("clicked", self.zoom, model.Direction.UP)

    def move(self, widget, direction):
        if not self.target:
            model.WINDOW.move(self.measure, model.WINDOW.guidance(direction))
        else:
            reference = None if self.reference in ["Object", "World"] \
                        else model.WINDOW.angle
            model.OBJECT_MANAGER.move(self.target, self.measure, direction, reference)

    def turn(self, widget, direction):
        if not self.target:
            model.WINDOW.turn(self.measure, direction)
        else:
            reference = None if self.reference == "Object" \
                        else model.WINDOW.center if self.reference == "Window" \
                        else (0, 0)
            model.OBJECT_MANAGER.turn(self.target, self.measure, direction, reference)

    def zoom(self, widget, direction):
        if not self.target:
            model.WINDOW.zoom(self.measure, direction)
        else:
            reference = None if self.reference == "Object" \
                        else model.WINDOW.center if self.reference == "Window" \
                        else (0, 0)
            model.OBJECT_MANAGER.zoom(self.target, self.measure, direction, reference)

    def set_target(self, target):
        for option in self.reference_option_group:
            option.hide() if not target else option.show()
        self.target = target

    @property
    def measure(self):
        return float(self.measure_entry.get_text())

    @property
    def reference(self):
        return next((
            option for option in
            self.reference_option_group
            if option.get_active()
        )).get_label()
