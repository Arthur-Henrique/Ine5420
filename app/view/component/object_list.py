from app import domain
from core import Projection, __project__
from app.view.new_geometric_form import NewGeometricFormView


class ObjectListComponent(Projection):
    def __init__(self, builder):
        super().__init__()

        self.object_list = builder.get_object("object_list")
        self.object_selection = builder.get_object("object_selection")

        builder.get_object("new_object").connect("clicked", self.new_object)
        builder.get_object("describe").connect("clicked", self.describe)
        builder.get_object("delete").connect("clicked", self.delete)
        self.object_selection.connect("changed", self.selection_changed)

        self.refresh('display_file')

    def new_object(self, widget):
        NewGeometricFormView()

    def describe(self, widget):
        if self.selected_object_id:
            domain.describe(self.selected_object_id)

    def delete(self, widget):
        domain.delete(self.selected_object_id)

    def selection_changed(self, widget):
        __project__("object_selection", id=self.selected_object_id)

    @property
    def selected_object_id(self):
        (m, path) = self.object_selection.get_selected_rows()
        return None if not path else int(m.get_value(m.get_iter(path[0]), 0))

    def refresh(self, *args, **kwargs):
        if "display_file" in args:
            self.object_list.clear()

            for object in domain.DISPLAY_FILE:
                self.object_list.append([object.id, object.name, object.type])