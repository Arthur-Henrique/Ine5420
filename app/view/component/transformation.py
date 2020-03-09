from app import model
from app.util import Direction, WORLD_CENTER
from core import Projection


class TransformationComponent(Projection):
    target = None

    def __init__(self, builder):
        super().__init__()

        self.measure_entry = builder.get_object("transformation_measure_entry")

        self.center_reference_group = builder.get_object("center_reference_group")
        self.axis_reference_group = builder.get_object("axis_reference_group")
        self.center_reference_group.hide()
        self.axis_reference_group.hide()

        builder.get_object("move_up").connect("clicked", self.move, Direction.UP)
        builder.get_object("move_left").connect("clicked", self.move, Direction.LEFT)
        builder.get_object("move_down").connect("clicked", self.move, Direction.DOWN)
        builder.get_object("move_right").connect("clicked", self.move, Direction.RIGHT)

        builder.get_object("zoom_in").connect("clicked", self.zoom, Direction.FORWARD)
        builder.get_object("zoom_out").connect("clicked", self.zoom, Direction.BACKWARD)

        builder.get_object("turn_left").connect("clicked", self.turn, Direction.LEFT)
        builder.get_object("turn_right").connect("clicked", self.turn, Direction.RIGHT)

    def move(self, widget, direction):
        if not self.target:
            model.LANDSCAPE.move(self.measure, direction)
        else:
            reference = None if self.reference in ["Object", "World"] \
                else model.LANDSCAPE.angle
            model.DESIGNER.move(self.target, self.measure, direction, reference)

    def turn(self, widget, direction):
        if not self.target:
            model.LANDSCAPE.turn(self.measure, direction)
        else:
            reference = None if self.reference == "Object" \
                else model.LANDSCAPE.center if self.reference == "Window" \
                else WORLD_CENTER
            model.DESIGNER.turn(self.target, self.measure, direction, reference, self.axis)

    def zoom(self, widget, direction):
        if not self.target:
            model.LANDSCAPE.zoom(self.measure, direction)
        else:
            reference = None if self.reference == "Object" \
                else model.LANDSCAPE.center if self.reference == "Window" \
                else WORLD_CENTER
            model.DESIGNER.zoom(self.target, self.measure, direction, reference)

    @property
    def measure(self):
        return float(self.measure_entry.get_text())

    @property
    def reference(self):
        return self.get_active_radio(self.center_reference_group)

    @property
    def axis(self):
        return self.get_active_radio(self.axis_reference_group)

    def get_active_radio(self, group):
        return next(radio.get_label() for radio in group.get_children() if radio.get_active())

    def refresh(self, *args, **kwargs):
        if "object_selection" in args:
            self.target = kwargs['id']

            [
                group.show()
                if self.target else
                group.hide()
                for group in
                [self.center_reference_group, self.axis_reference_group]
            ]
