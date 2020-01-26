from app import domain
from app.view import UserInterface
from app.view.dialog import Dialog


class NewObjectView(UserInterface):

    def __init__(self):
        super().__init__()

        self.name_entry = self.builder.get_object("name_entry")
        self.color_button = self.builder.get_object("color_button")
        self.x_entry = self.builder.get_object("x_entry")
        self.y_entry = self.builder.get_object("y_entry")
        self.coordinate_list = self.builder.get_object("coordinate_list")
        self.type_option_group = self.builder.get_object("Dot_radio").get_group()

        self.builder.get_object("insert_button").connect("clicked", self.insert)
        self.builder.get_object("create_button").connect("clicked", self.create)

    def insert(self, widget):
        self.coordinate_list.append([
            int(self.x_entry.get_text()),
            int(self.y_entry.get_text())
        ])

        self.x_entry.set_text("")
        self.y_entry.set_text("")

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
    def coordinates(self):
        return [(row[0], row[1]) for row in self.coordinate_list]

    @property
    def type(self):
        return next((
            option for option in
            self.type_option_group
            if option.get_active()
        )).get_label()