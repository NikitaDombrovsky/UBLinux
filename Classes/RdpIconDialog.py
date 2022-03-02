import tkinter
from tkinter import filedialog

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Dialog:

    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("Classes/IconDialog.glade")

        self.dialog = self.builder.get_object("create_icon_dialog")

        self.dialog_result = None
        self.directory_path = None
        self.fn = None

        self.btn_ok = self.builder.get_object("dg_ok_button")
        self.btn_cancel = self.builder.get_object("dg_cancel_button")
        self.dg_btn_browse = self.builder.get_object("dg_browse_button")
        self.file_name_entry = self.builder.get_object("dg_name_entry")
        self.path_entry = self.builder.get_object("gd_folder_entry")

        self.btn_ok.connect("clicked", self.ok_click)
        self.btn_cancel.connect("clicked", self.cancel_click)
        self.dg_btn_browse.connect("clicked", self.show_explorer)

    def show_explorer(self, widget):
        dialog_t = tkinter.Tk()
        dialog_t.withdraw()
        self.directory_path = filedialog.askdirectory(parent=dialog_t, initialdir="/")
        self.path_entry.set_text(self.directory_path)

    def run_dialog(self):
        self.dialog.set_title("Создание ярлыка подключения")
        self.dialog_result = self.dialog.run()

        if self.dialog_result == Gtk.ResponseType.OK:
            self.dialog_result = True
        if self.dialog_result == Gtk.ResponseType.CANCEL:
            self.dialog_result = False

        return self.dialog_result

    def get_file_name(self):
        return self.fn

    def get_folder(self):
        return self.directory_path

    def ok_click(self, widget):
        self.fn = self.file_name_entry.get_text()
        self.dialog.destroy()

    def cancel_click(self, widget):
        self.dialog.destroy()
