from app import model, domain
from app.model import Landscape
from app.util import WORLD_CENTER
from core.projection import Projection


class DrawingAreaComponent(Projection):
    painter = None

    def __init__(self, builder):
        super().__init__()

        drawing_area = builder.get_object("drawing-area")
        self.painter = drawing_area.get_window().cairo_create()

        drawing_area.connect("draw", self.draw)

        model.LANDSCAPE.resize(drawing_area.get_allocation())

        self.draw(None, self.painter)

    def draw(self, widget, painter):
        painter.set_source_rgb(0, 0, 0)
        painter.paint()
        painter.set_source_rgb(1, 1, 1)

        def dot(point):
            [(x, y, z)] = point

            painter.arc(x, y, 2, 0, 6)
            painter.fill()

        def trace(line):
            (x0, y0, z0), (x1, y1, z1) = line

            painter.move_to(x0, y0)
            painter.line_to(x1, y1)

        draft = model.DESIGNER.draft @ model.LANDSCAPE
        draft.per_dot(dot)
        draft.per_trace(trace)

        painter.stroke()

    def refresh(self, *args, **kwargs):
        if {signal for signal in args if signal in [
            "display_file",
            "object_transformation",
            "window_transformation"
        ]}:
            self.draw(None, self.painter)