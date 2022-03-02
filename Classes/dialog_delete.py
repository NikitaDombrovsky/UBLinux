import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class DialogDelete(Gtk.Dialog):
    def __init__(self, parent, device):
        super().__init__(title="Удаление", transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        self.set_default_size(150, 100)

        label = Gtk.Label(label=f"Вы действительно хотите удалить устройство: {device}?")

        box = self.get_content_area()
        box.add(label)
        self.show_all()
