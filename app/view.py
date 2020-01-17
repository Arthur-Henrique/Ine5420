import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from core.projection import Projection
import app.model as model


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


class AppView(UserInterface):
    object_tree_view = None

    object_list = None
    drawing_area = None
    transformation = None
    logger = None

    def __init__(self):
        super().__init__("AppView.glade")

        self.object_tree_view = self.builder.get_object("object_tree_view")

        self.object_list = ObjectListComponent(self.builder)
        self.drawing_area = DrawingAreaComponent(self.builder)
        self.transformation = TransformationComponent(self.builder)
        self.logger = LogComponent(self.builder)

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
        builder.get_object("describe").connect("clicked", self.describe)
        builder.get_object("delete").connect("clicked", self.delete)

    def new_object(self, widget):
        NewObjectView()

    def delete(self, widget):
        model.OBJECT_MANAGER.delete(APP_VIEW.selected_object_id)

    # def clear(self, widget):
    #     model.OBJECT_MANAGER.clear()

    def describe(self, widget):
        model.OBJECT_MANAGER.describe(APP_VIEW.selected_object_id)

    def refresh(self, *args, **kwargs):
        if "display_file" in args:
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

        self.drawing_area = builder.get_object("drawing-area")
        self.painter = self.drawing_area.get_window().cairo_create()

        self.drawing_area.connect("draw", self.draw)

        area = self.drawing_area.get_allocation()
        model.WINDOW = model.Window((0, 0), (area.width, area.height))
        model.VIEWPORT = model.Viewport((20, 20), (area.width-40, area.height-40))
        model.CLIPPING = model.Clipping((40, 40), (area.width-80, area.height-80))

    def draw(self, widget, painter):
        painter.save()
        painter.set_source_rgb(0, 0, 0)
        painter.paint()

        painter.set_source_rgb(1, 1, 1)
        painter.rectangle(*model.VIEWPORT.rectangle)
        painter.stroke()

        painter.set_source_rgb(0, 1, 1)
        painter.rectangle(*model.CLIPPING.rectangle)
        painter.stroke()

        for object in model.OBJECT_MANAGER:
            painter.set_source_rgb(*object.color)

            representation = object.coordenates \
                             @ model.VIEWPORT \
                             @ model.WINDOW \
                             @ model.CLIPPING

            if len(representation) == 1:
                painter.arc(*representation[0], 2, 0, 6)
                painter.fill()
            else:
                for i, draft in enumerate(representation):
                    if i != 0:
                        (begin, end) = representation[i-1:i+1]
                        if begin and end:
                            painter.move_to(*begin)
                            painter.line_to(*end)

            painter.stroke()
        painter.restore()

    def refresh(self, *args, **kwargs):
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
            model.WINDOW.move(self.measure, direction)
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


class LogComponent(Projection):
    text_view_buffer = None
    scrolled_window_vadjustment = None

    active_sessions = ["log"]

    def __init__(self, builder):
        super().__init__()

        self.text_view_buffer = builder.get_object("log_text_view").get_buffer()
        self.scrolled_window_vadjustment = builder.get_object("log_scrolled_window").get_vadjustment()

    def refresh(self, *args, **kwargs):
        it = self.text_view_buffer.get_iter_at_offset(-1)

        if "log" in args:
            for session, text in kwargs.items():
                if session in self.active_sessions:
                    self.text_view_buffer.insert(it, f"{session}:\t {text}\n", -1)

        self.scroll()

    def scroll(self):
        adjustment = self.scrolled_window_vadjustment
        adjustment.set_value(
            adjustment.get_upper() - adjustment.get_page_size()
        )