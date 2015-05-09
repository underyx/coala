from gi.repository import Gtk


class coalaProject(Gtk.ApplicationWindow):

    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(self,
                                       application=app,
                                       title="project")

        self._ui = Gtk.Builder()
        self._ui.add_from_resource("/coala/coalaProject.ui")

        self.header_bar = self._ui.get_object("header-bar")
        self.set_titlebar(self.header_bar)
        self.show_all()