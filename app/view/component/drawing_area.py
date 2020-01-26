from app import model, domain
from app.model import Landscape
from core.projection import Projection


class DrawingAreaComponent(Projection):
    drawing_area = None
    painter = None

    def __init__(self, builder):
        super().__init__()

        self.drawing_area = builder.get_object("drawing-area")
        self.painter = self.drawing_area.get_window().cairo_create()

        self.drawing_area.connect("draw", self.draw)

        area = self.drawing_area.get_allocation()
        model.LANDSCAPE = Landscape((0, 0), (area.width, area.height))

        self.drawing_area.draw(self.painter)

    def draw(self, widget, painter):
        self.set(painter)

        for object in domain.DISPLAY_FILE:
            painter.set_source_rgb(*object.color)

            self.scribe(object.draft, painter)

            painter.stroke()

    def set(self, painter):
        painter.set_source_rgb(0, 0, 0)
        painter.paint()

        for rectangle in model.LANDSCAPE.draft():
            painter.set_source_rgb(0.5, 0.5, 0.5)
            painter.rectangle(*rectangle.description)
            painter.stroke()

        self.scribe([model.LANDSCAPE.window.center], painter)

    def scribe(self, draft, painter):
        representation = draft @ model.LANDSCAPE

        if len(representation) == 1:
            painter.arc(*representation[0], 2, 0, 6)
            painter.fill()
        else:
            for i, draft in enumerate(representation):
                if i != 0:
                    (begin, end) = representation[i - 1:i + 1]
                    if begin and end:
                        painter.move_to(*begin)
                        painter.line_to(*end)

    def refresh(self, *args, **kwargs):
        if {signal for signal in args if signal in [
            "display_file",
            "object_transformation",
            "window_transformation"
        ]}:
            self.drawing_area.draw(self.painter)