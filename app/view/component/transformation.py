from app import model
from app.util import Direction
from core import Projection


class TransformationComponent(Projection):
    target = None
    measure_entry = None
    transformation_reference_group = None

    def __init__(self, builder):
        super().__init__()

        self.measure_entry = builder.get_object("transformation_measure_entry")
        self.transformation_reference_group = builder.get_object("transformation_reference_group")
        self.transformation_reference_group.hide()

        builder.get_object("move_up").connect("clicked", self.move, Direction.UP)
        builder.get_object("move_left").connect("clicked", self.move, Direction.LEFT)
        builder.get_object("move_down").connect("clicked", self.move, Direction.DOWN)
        builder.get_object("move_right").connect("clicked", self.move, Direction.RIGHT)

        builder.get_object("turn_left").connect("clicked", self.turn, Direction.LEFT)
        builder.get_object("turn_right").connect("clicked", self.turn, Direction.RIGHT)

        builder.get_object("zoom_in").connect("clicked", self.zoom, Direction.DOWN)
        builder.get_object("zoom_out").connect("clicked", self.zoom, Direction.UP)

    def move(self, widget, direction):
        if not self.target:
            model.LANDSCAPE.window.move(self.measure, direction)
        else:
            reference = None if self.reference in ["Object", "World"] \
                else model.LANDSCAPE.window.angle
            model.OBJECT_MANAGER.move(self.target, self.measure, direction, reference)

    def turn(self, widget, direction):
        if not self.target:
            model.LANDSCAPE.window.turn(self.measure, direction)
        else:
            reference = None if self.reference == "Object" \
                else model.LANDSCAPE.window.center if self.reference == "Window" \
                else (0, 0, 0)
            model.OBJECT_MANAGER.turn(self.target, self.measure, direction, reference)

    def zoom(self, widget, direction):
        if not self.target:
            model.LANDSCAPE.window.zoom(self.measure, direction)
        else:
            reference = None if self.reference == "Object" \
                else model.LANDSCAPE.window.center if self.reference == "Window" \
                else (0, 0, 0)
            model.OBJECT_MANAGER.zoom(self.target, self.measure, direction, reference)

    @property
    def reference(self):
        return next(
            radio.get_label() for radio in self.transformation_reference_group.get_children()
            if radio.get_active()
        )

    @property
    def measure(self):
        return float(self.measure_entry.get_text())

    def refresh(self, *args, **kwargs):
        if "object_selection" in args:
            self.target = kwargs['id']
            self.transformation_reference_group.hide() \
                if not self.target else \
                self.transformation_reference_group.show()