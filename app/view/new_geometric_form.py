from app.view import UserInterface, Dialog
from app import domain


class NewGeometricFormView(UserInterface):

    def __init__(self):
        super().__init__()

        self.name_entry = self.builder.get_object("name_entry")
        self.color_button = self.builder.get_object("color_button")
        self.type_option_group = self.builder.get_object("Point_radio").get_group()
        self.axis_entries = [self.builder.get_object(f"{axis}_entry") for axis in ('x', 'y', 'z')]
        self.coordinate_list = self.builder.get_object("coordinate_list")

        self.builder.get_object("insert_button").connect("clicked", self.insert)
        self.builder.get_object("load_button").connect("file-set", self.load)
        self.builder.get_object("create_button").connect("clicked", self.create)

    def insert(self, widget):
        self.coordinate_list.append(self.axis)
        [entry.set_text("") for entry in self.axis_entries]

    def load(self, widget):
        path = widget.get_filename()
        domain.load(path)

        self.quit()

    def create(self, widget):
        try:
            domain.create(
                name=self.name,
                type=self.type,
                coordinates=self.coordinates,
                color=self.color
            )
        except AssertionError as e:
            Dialog(f"Error creating {self.type}", f"{e}")
        else:
            self.quit()

    @property
    def name(self):
        return self.name_entry.get_text()

    @property
    def color(self):
        rgba = self.color_button.get_rgba()
        return (rgba.red, rgba.green, rgba.blue)

    @property
    def type(self):
        return next((
            option for option in
            self.type_option_group
            if option.get_active()
        )).get_label()

    @property
    def axis(self):
        return [int(entry.get_text()) for entry in self.axis_entries]

    @property
    def coordinates(self):
        return [(row[0], row[1], row[2]) for row in self.coordinate_list]