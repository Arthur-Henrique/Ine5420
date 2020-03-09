from app import model
from core.projection import Projection


class DrawingAreaComponent(Projection):
    painter = None

    def __init__(self, builder):
        super().__init__()

        self.drawing_area = builder.get_object("drawing-area")
        self.painter = self.drawing_area.get_window().cairo_create()

        self.drawing_area.connect("draw", self.draw)

        rect = self.drawing_area.get_allocation()
        model.LANDSCAPE.resize((rect.width, rect.height))

        self.draw(None, self.painter)

    def draw(self, widget, painter):
        painter.set_source_rgb(0, 0, 0)
        painter.paint()

        painter.set_source_rgb(.5, .5, .5)
        painter.rectangle(20, 20, 710, 710)
        painter.stroke()

        def dot(coordinates, color=(.5, .5, .5)):
            [(x, y, z)] = coordinates
            painter.set_source_rgb(*color)

            painter.arc(x, y, 2, 0, 6)
            painter.fill()

        def trace(coordinates, color=(.5, .5, .5)):
            (x0, y0, z0), (x1, y1, z1) = coordinates
            painter.set_source_rgb(*color)

            painter.move_to(x0, y0)
            painter.line_to(x1, y1)
            painter.stroke()

        def face(coordinates, color=(.5, .5, .5)):
            painter.set_source_rgb(*color)

            painter.move_to(*coordinates[0][:2])
            [painter.line_to(x, y) for x, y, z in coordinates]
            painter.fill()

        draft = model.DESIGNER.draft @ model.LANDSCAPE
        draft.per_dot(dot)
        draft.per_trace(trace)
        draft.per_face(face)
        dot([(375, 375, 0)])

    def refresh(self, *args, **kwargs):
        if {signal for signal in args if signal in [
            "display_file",
            "transformation",
            "landscape"
        ]}:
            self.draw(None, self.painter)