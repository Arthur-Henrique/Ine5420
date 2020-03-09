from core.projection import Projection


# TODO: Differ core.__log__ action and app.view.component name
class LogComponent(Projection):
    text_view = None
    scrolled_window_vadjustment = None

    active_sessions = ["new_object", "object", "welcome"]

    def __init__(self, builder):
        super().__init__()

        self.text_view = builder.get_object("log_text_view")
        self.scrolled_window_vadjustment = builder.get_object("log_scrolled_window").get_vadjustment()

    def scroll(self):
        insert = self.text_view.get_buffer().get_insert()
        self.text_view.scroll_to_mark(insert, 0, True, 0, 0)

    @property
    def cursor(self):
        return self.text_view.get_buffer().get_iter_at_offset(-1)

    def refresh(self, *args, **kwargs):

        if "log" in args:
            for session, text in kwargs.items():
                # if session in self.active_sessions:
                    self.text_view.get_buffer().insert(self.cursor, f"{session}:\t{text}\n\n", -1)

        self.scroll()
