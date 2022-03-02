import subprocess
import tkinter
from tkinter import filedialog

import gi
import re
import Classes.VM
from Classes import Main_Thread, RdpIconDialog, RDPBuilder, VM
from Classes.Sending_Command import SendingCommand


from Classes.dialog_add_usb import DialogAddUsb
from Classes.dialog_delete import DialogDelete
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


# object = None
class SignalHandler:
    @staticmethod
    def onDestroy(self, *args):
        Gtk.main_quit()

class UsbDevice:
    def __init__(self, index, active, filter_name, vendor_id, product_id, product_name):
        self.index = index
        self.active = active
        self.filter_name = filter_name
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.product_name = product_name
memes = 0

class Main:
    def __init__(self, folder):
        # try:
        # self.set_size_request(200, 150)

        self.vm_name = None
        self.resolution = None
        self.window_title = None
        self.printer = None
        self.audio = None
        self.shared_folder = None
        self.login = None
        self.password = None
        self.ip = None
        self.port = None
        self.domain = None
        self.path = None
        self.file_name = None
        self.hashes = None

        self.builder = Gtk.Builder()
        self.builder.add_from_file("New.glade")
        self.Main_Window = self.builder.get_object("Main_Window")
        self.builder.connect_signals(self)
        self.NoteBook = self.builder.get_object("NoteBook")
        self.Virtual_On_Button = self.builder.get_object("Virtual_On_Button")
        self.Virtual_Off_Button = self.builder.get_object("Virtual_Off_Button")
        self.Virtual_Save_Button = self.builder.get_object("Virtual_Save_Button")
        self.Virtual_Reset_Button = self.builder.get_object("Virtual_Reset_Button")
        self.Virtual_Create_Button = self.builder.get_object("Virtual_Create_Button")
        self.Virtual_Combo = self.builder.get_object("Virtual_Combo")

        self.Float_TreeView = self.builder.get_object("Floats_TreeView")
        self.Float_TreeView_List = Gtk.ListStore(str, str, str, bool, str)

        self.Virtual_TreeView = self.builder.get_object("Virtual_TreeView")
        self.Virtual_TreeView_List = Gtk.ListStore(str, bool, str)

        self.Direct_TreeView_USB = self.builder.get_object("Direct_TreeView_USB")
        self.Direct_TreeView_USB_List = Gtk.ListStore(bool, str, str, str, int)
        self.Direct_Button_1_Filter = self.builder.get_object("Direct_Button_1_Filter")
        self.Direct_Button_2_Add = self.builder.get_object("Direct_Button_2_Add")
        self.Direct_Button_3 = self.builder.get_object("Direct_Button_3")
        self.Direct_Button_4_Remove = self.builder.get_object("Direct_Button_4_Remove")
        self.Direct_Button_5_Up = self.builder.get_object("Direct_Button_5_Up")
        self.Direct_Button_6_Down = self.builder.get_object("Direct_Button_6_Down")

        self.RA_Connect_Button = self.builder.get_object("RA_Connect_Button")
        self.rdp_ip = self.builder.get_object("rdp_ip")
        self.rdp_password = self.builder.get_object("rdp_password")
        self.rdp_login = self.builder.get_object("rdp_login")
        self.rdp_domain = self.builder.get_object("rdp_domain")
        self.rdp_port = self.builder.get_object("rdp_port")
        self.rdp_rb_default = self.builder.get_object("rdp_rb_default")
        self.rdp_rb_client = self.builder.get_object("rdp_rb_client")
        self.rdp_rb_manual = self.builder.get_object("rdp_rb_manual")
        self.rdp_cmb_color = self.builder.get_object("cmb_color")
        self.rdp_window_title = self.builder.get_object("rdp_window_title")
        self.rdp_shared_folder_cb = self.builder.get_object("rdp_shared_folder_cb")
        self.rdp_shared_folder = self.builder.get_object("rdp_shared_folder")
        self.rdp_printer_cb = self.builder.get_object("rdp_printer_cb")
        self.rdp_printer_cmb = self.builder.get_object("rdp_printer_cmb")
        self.rdp_sound_cb = self.builder.get_object("rdp_sound_cb")
        self.rdp_show_password_btn = self.builder.get_object("rdp_show_password_btn")
        self.rdp_browse_btn = self.builder.get_object("rdp_browse_btn")
        self.rdp_create_conn_btn = self.builder.get_object("rdp_create_conn_btn")

        self.rdp_rb_default.set_active(True)
        self.rdp_cmb_color.set_sensitive(False)
        self.fill_color_cmb()
        self.detect_printers()
        self.rdp_password.set_visibility(False)
        self.rdp_password.set_invisible_char('*')
        self.rdp_shared_folder_cb.set_active(True)
        self.rdp_sound_cb.set_active(True)

        self.rdp_show_password_btn.connect("clicked", self.on_show_password_click)
        self.rdp_browse_btn.connect("clicked", self.on_browse_click)
        self.rdp_shared_folder_cb.connect("toggled", self.on_shared_checked)
        self.rdp_create_conn_btn.connect("clicked", self.create_rdp)
        self.rdp_rb_default.connect("toggled", self.on_rb_default_toggled)
        self.rdp_rb_client.connect("toggled", self.on_rb_client_toggled)
        self.rdp_rb_manual.connect("toggled", self.on_rb_manual_toggled)
        self.rdp_cmb_color.connect("changed", self.on_color_selection_changed)


        self.RA_IP = self.builder.get_object("RA_IP")
        self.Direct_Dialog_USB = self.builder.get_object("list_usb")
        self.Direct_IP = self.builder.get_object("entry_ip_remote")
        self.Direct_Dialog_USB_List = Gtk.ListStore(bool, str)
        self.Select_USB = None

        self.Combo_Changed = None
        self.Block = 0
        self.Virtual_TreeView_Generator()
        self.Spring_Obj = Main_Thread.Main_Thread_Class(Main_Array=self.Main_Array, ctx=self)
        self.Spring_Obj.Start_Thread()
        self.folder = folder
        self.Main_Window.show_all()

    def printSharedFolder(self):
        test1 = Classes.VM.VirtualMachines()
        vm = self.Change_Name
        test = Classes.VM.SharedFolders(name=self.Change_Name)
        self.rez = test.shared_folders_list
        print(self.rez)
        print(vm)

    def TreeView_Gen(self):

        self.TreeView_Gener()

        text_renderer = Gtk.CellRendererText()
        bool_renderer = Gtk.CellRendererToggle()

        f_name = Gtk.TreeViewColumn(title="Имя", cell_renderer=text_renderer, text=0)
        f_direction = Gtk.TreeViewColumn(title="Путь", cell_renderer=text_renderer, text=1)
        f_accept = Gtk.TreeViewColumn(title="Дооступ", cell_renderer=text_renderer, text=2)
        f_auto_m = Gtk.TreeViewColumn(title="Авто-монтирование", cell_renderer=bool_renderer, active=3)
        f_place_m = Gtk.TreeViewColumn(title="Точка монтирования", cell_renderer=text_renderer, text=4)

        self.Float_TreeView.append_column(f_name)
        self.Float_TreeView.append_column(f_direction)
        self.Float_TreeView.append_column(f_accept)
        self.Float_TreeView.append_column(f_auto_m)
        self.Float_TreeView.append_column(f_place_m)

        self.Float_TreeView.set_model(self.Float_TreeView_List)

    def TreeView_Gener(self):
        # self.printSharedFolder()
        i = 0
        while i != len(self.rez):
            text = self.rez[i]
            self.Float_TreeView_List.append([text.folder_name, text.folder_path, text.folder_access,
                                             text.folder_automount, text.folder_mount_point])
            print(text.folder_name, text.folder_path, text.folder_access, text.folder_automount,
                  text.folder_mount_point)
            i += 1

    def Add_fold_clicked_cb(self, button):
        Dialog(self)

    def Change_fload_clicked_cb(self, button):
        temp = VM.SharedFolder(folder_name=self.selected_fload, folder_path=self.selected_fload_way,
                               folder_access=self.selected_fload_access, folder_automount=self.selected_fload_automount,
                               folder_mount_point=self.selected_fload_mont)
        DialogChange(temp)

    def get_ctx(self):
        return self

    def Re_gen(self):
        self.Float_TreeView_List.clear()
        self.TreeView_Gener()
        self.Float_TreeView.set_model(self.Float_TreeView_List)

    def change_fload_tree(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            self.selected_fload = model[treeiter][0]
            self.selected_fload_way = model[treeiter][1]
            self.selected_fload_access = model[treeiter][2]
            self.selected_fload_automount = model[treeiter][3]
            self.selected_fload_mont = model[treeiter][4]
            print(self.selected_fload, self.selected_fload_way)

    def Del_fload_clicked_cb(self, button):
        machines = VM.VirtualMachines()
        vmm = machines.vm_list[0]
        vmms = vmm.getname()
        subprocess.getoutput(f"VBoxManage sharedfolder remove '{vmms}' --name {self.selected_fload}")
        self.Re_gen()
        print(vmm)

    def getcontext(self):
        return self

    # Заполнение TreeView данными
    def Virtual_TreeView_Generator(self, *args):
        # try:
        self.Virtual_TreeView_Second()

        vm_column = Gtk.TreeViewColumn(title="Виртуальная машина", cell_renderer=Gtk.CellRendererText(), text=0)
        st_column = Gtk.TreeViewColumn(title="Статус", cell_renderer=Gtk.CellRendererToggle(), active=1)
        ip_column = Gtk.TreeViewColumn(title="IP-адрес", cell_renderer=Gtk.CellRendererText(), text=2)

        self.Virtual_TreeView.append_column(vm_column)
        self.Virtual_TreeView.append_column(st_column)
        self.Virtual_TreeView.append_column(ip_column)

        self.Virtual_TreeView.set_model(self.Virtual_TreeView_List)



    # Продолжение заполнения
    def Virtual_TreeView_Second(self):
        # try:
        Out_All_Name = subprocess.getoutput(
            'v=$(VBoxManage list vms);awk -F\'\"|\\"\' \'{print $2}\' <<< $v').split("\n")
        Out_All_Hash = subprocess.getoutput(
            'v=$(VBoxManage list vms);awk -F\'\"|\\"\' \'{print $3}\' <<< $v').split("\n")
        Out_ON_Hash = subprocess.getoutput(
            'v=$(VBoxManage list runningvms);awk -F\'\"|\\"\' \'{print $3}\' <<< $v').split("\n")

        self.hashes = Out_All_Hash

        self.Main_Array = [[0] * 3 for i in range(len(Out_All_Name))]

        for i in range(len(Out_All_Name)):

            Out_Bool = False
            for v in range(len(Out_ON_Hash)):
                if Out_All_Hash[i] == Out_ON_Hash[v]:
                    Out_Bool = True
            Out_IP = re.split('"|<', subprocess.getoutput(
                f'VBoxManage showvminfo "{Out_All_Name[i]}" | grep TCP/Address '))
            if Out_IP[0] == "" or Out_IP[1] == 'not set>' or Out_IP[1] == '0.0.0.0':
                self.Virtual_TreeView_List.append([Out_All_Name[i], Out_Bool, "0.0.0.0"])
                self.Main_Array[i][0] = Out_All_Name[i]
                self.Main_Array[i][1] = Out_Bool
                self.Main_Array[i][2] = "0.0.0.0"
            else:
                self.Virtual_TreeView_List.append([Out_All_Name[i], Out_Bool, Out_IP[i]])
                self.Main_Array[i][0] = Out_All_Name[i]
                self.Main_Array[i][1] = Out_Bool
                self.Main_Array[i][2] = Out_IP[1]


    # Выбор элемента TreeView
    def Virtual_TreeView_Changed(self, Selection):
        # try:

        if self.Block == 0:
            self.Virtual_On_Button.set_sensitive(True)
            Model, Treeiter = Selection.get_selected()
            self.Akagi = Model, Treeiter
            self.Belfast = Model[Treeiter][0]
            row_num_raw = Model.get_path(Treeiter)
            row_num = int(row_num_raw.to_string())
            self.vm_name = self.hashes[row_num]
            self.Select = Selection
            if Treeiter is not None:
                self.Spring_Obj.Constructor(Model[Treeiter], Model, Selection)
                self.Change_Name = Model[Treeiter][0]
                self.Change_IP = Model[Treeiter][2]
                self.Column_ID = self.Virtual_TreeView.get_selection().get_selected_rows()[1][0][0]
                if Model[Treeiter][1] == True:
                    Main.Virtual_Change_Button(self, 0)
                if Model[Treeiter][1] == False:
                    Main.Virtual_Change_Button(self, 1)
                self.Spring_Obj.Checker()
                self.Spring_Obj.Mutex = 1
                if self.Spring_Obj.Checker_Changer == 1:
                    if Model[Treeiter][2] == self.Spring_Obj.arg1_3:
                        if self.Change_Name == self.Spring_Obj.arg1_1:
                            self.Block = 1
                            self.Spring_Obj.Checker_Changer = 0
                            Model.remove(Treeiter)
                            self.Virtual_TreeView_List.insert(self.Column_ID, (
                                str(self.Spring_Obj.arg1_1), bool(self.Spring_Obj.arg1_2),
                                str(self.Spring_Obj.arg1_3)))
                            self.Block = 0
                        else:
                            print("Ну типа заработало")
                self.Spring_Obj.Mutex = 0



    # Нажатие на кнопку Включить
    def Virtual_On_Button_Clicked(self, button):
        try:
            SendingCommand.VM_ON(self.Change_Name)
            # os.system("VBoxManage startvm %a -type headless " % self.Change_Name)
            Main.Virtual_Change_Button(self, 0)
        except Exception:
            print("Exception Virtual_On_Button_Clicked - ", Exception)

    # Нажатие на кнопку Выключить
    def Virtual_Off_Button_Clicked(self, button):
        try:
            SendingCommand.VM_OFF(self.Change_Name)

            Main.Virtual_Change_Button(self, 1)
            print("Выключение", self.Change_Name)
        except Exception:
            print("Exception Virtual_Off_Button_Clicked - ", Exception)

    # Нажатие на кнопку Сохранить Состояние
    def Virtual_Save_Button_Clicked(self, button):
        try:
            SendingCommand.VM_SAVE(self.Change_Name)

        except Exception:
            print("Exception Virtual_Save_Button_Clicked - ", Exception)

    # Нажатие на кнопку Перезагрузить
    def Virtual_Reset_Button_Clicked(self, button):
        try:
            SendingCommand.VM_RESET(self.Change_Name)

        except Exception:
            print("Exception Virtual_Reset_Button_Clicked - ", Exception)

    #
    def Virtual_Create_Button_Clicked(self, button):
        Num_Page = self.Virtual_Combo.get_active()
        if Num_Page is not None:
            self.NoteBook.set_current_page(Num_Page + 1)
            if Num_Page == 0:
                self.Direct_IP.set_text(self.Change_IP)
                self.Direct_TreeView_USB_Generator(Name_VM=self.Change_Name)
            if Num_Page == 1:
                self.rdp_ip.set_text(self.Change_IP)
            if Num_Page == 2:
                self.RA_IP.set_text(self.Change_IP)

        print(self.Change_IP)
        print(self.Change_Name)
        self.printSharedFolder()
        self.TreeView_Gen()




    # Изменение доступности к кнопкам в зависимости от состояния машины
    def Virtual_Change_Button(self, on):
        try:
            if on == 0:
                self.Virtual_Off_Button.set_sensitive(True)
                self.Virtual_Save_Button.set_sensitive(True)
                self.Virtual_Reset_Button.set_sensitive(True)
                self.Virtual_Create_Button.set_sensitive(True)
                self.Virtual_Combo.set_sensitive(True)
                self.Virtual_On_Button.set_sensitive(False)
            else:
                self.Virtual_Off_Button.set_sensitive(False)
                self.Virtual_Save_Button.set_sensitive(False)
                self.Virtual_Reset_Button.set_sensitive(False)
                self.Virtual_Create_Button.set_sensitive(False)
                self.Virtual_Combo.set_sensitive(False)
                self.Virtual_On_Button.set_sensitive(True)
        except Exception:
            print("Exception Virtual_Change_Button - ", Exception)

    # Закрытие приложения и потока
    def Main_Close(self, e):
        try:
            self.Spring_Obj.Stop_Thread()
        except Exception:
            print("Exception Main_Close - ", Exception)

    def Direct_TreeView_USB_Generator(self, Name_VM):
        usb_list = self.Get_USB_List(name_vm=Name_VM)
        print(usb_list)
        for el in usb_list:
            self.Direct_TreeView_USB_List.append([True, el.filter_name, el.product_id, el.vendor_id, int(el.index)])

        active_column = Gtk.TreeViewColumn(title="Активно", cell_renderer=Gtk.CellRendererToggle(), active=0)
        device_column = Gtk.TreeViewColumn(title="Устройство", cell_renderer=Gtk.CellRendererText(), text=1)
        active_column.set_sort_column_id(0)

        self.Direct_TreeView_USB.append_column(active_column)
        self.Direct_TreeView_USB.append_column(device_column)

        self.Direct_TreeView_USB.set_model(self.Direct_TreeView_USB_List)

    def Get_USB_List(self, name_vm):
        usb_lst = subprocess.getoutput("v=$(echo $(VBoxManage showvminfo " + name_vm + "));awk -F \'USB Device Filters: | Bandwidth groups:\' \'{print $2}\'  <<< $v").split("Index: ")  # получаем полный список usb для машины test1
        usb_lst_ok = list()
        i = 1
        while i < len(usb_lst):  # в цикле проходим по всем устройствам
            tempIndex = usb_lst[i][0]
            tempActive = usb_lst[i][usb_lst[i].index("Active:"):usb_lst[i].find("Name:")].split(": ")[1]  # yes
            tempFilterName = usb_lst[i][usb_lst[i].index("Name:"):usb_lst[i].find("VendorId:")].split(": ")[1]
            tempVendorId = usb_lst[i][usb_lst[i].index("VendorId:"):usb_lst[i].find("ProductId:")].split(": ")[1]
            tempProductId = usb_lst[i][usb_lst[i].index("ProductId:"):usb_lst[i].find("Revision:")].split(": ")[1]
            tempProductName = usb_lst[i][usb_lst[i].index("Product:"):usb_lst[i].find("Remote:")].split(": ")[1]
            reliseObject = UsbDevice(tempIndex, tempActive, tempFilterName, tempVendorId, tempProductId,tempProductName)  # заполняем временный объект

            usb_lst_ok.append(reliseObject)
            i += 1
        return usb_lst_ok  # возврат списка обьектов UsbDevice

    def get_iter_last(self, mdl):
        print("Че")
        itr = mdl.get_iter_first()
        print("Че")
        last = None
        while itr:
            last = itr
            itr = mdl.iter_next(itr)
        return last

    def Direct_TreeView_Changed(self, Selected):
        self.Select_USB = Selected
        print("", self.Select_USB)
        print("sex")

    def Direct_Button_1_Filter_Clicked(self, *args):
        # try:
            last_iter = self.get_iter_last(self.Direct_TreeView_USB_List)
            id = 0 if last_iter is None else self.Direct_TreeView_USB_List[last_iter][4] + 1
            subprocess.getoutput(
                f"VBoxManage usbfilter add {id} --target {self.Belfast} --name 'Новый фильтр {id}'  --action hold")
            self.Direct_TreeView_USB_List.append([True, f'Новый фильтр {id}', '', '', id])
            dialog = Gtk.MessageDialog(
                transient_for=self.Main_Window,
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text="Успех!",
            )
            dialog.format_secondary_text(
                "USB-устройство успешно добавлено"
            )
            dialog.run()
            dialog.destroy()
        # except:
            return
    def Direct_Button_2_Add_Clicked(self, *args):
        dialog = DialogAddUsb()
        if dialog.response_type == Gtk.ResponseType.OK:
            for el in dialog.get_result():
                # print("" + self.Select_USB)
                last_iter = self.get_iter_last(self.Direct_TreeView_USB_List)
                print("1")
                id = 0 if last_iter is None else self.Direct_TreeView_USB_List[last_iter][4] + 1
                print("1")

                subprocess.getoutput(
                    f"VBoxManage usbfilter add {id} --target {self.Belfast} --name '{el[1]}' --action hold --vendorid {el[3]} --productid {el[2]}")

                self.Direct_TreeView_USB_List.append([el[0], el[1], el[2], el[3], id])
                dialog = Gtk.MessageDialog(
                    transient_for=self.Main_Window,
                    flags=0,
                    message_type=Gtk.MessageType.INFO,
                    buttons=Gtk.ButtonsType.OK,
                    text="Успех!",
                )
                dialog.format_secondary_text(
                    "USB-устройство успешно добавлено"
                )
                dialog.run()
                dialog.destroy()
        return

    def Direct_Button_4_Remove_Clicked(self, *args):

        model, treeiter  = self.Select_USB.get_selected()
        model_vm, treeiter_vm = self.Select.get_selected()

        if treeiter is not None:
            dialog = DialogDelete(self.Main_Window, model[treeiter][1])
            response = dialog.run()
            id = model[treeiter][4]
            if response == Gtk.ResponseType.OK:
                self.Direct_TreeView_USB_List.remove(treeiter)
                # SendingCommand.remove_usb_filter(id, model_vm[treeiter_vm][0])
                subprocess.getoutput(
                    f"VBoxManage usbfilter remove {id} --target {model_vm[treeiter_vm][0]}")

            dialog.destroy()
    def Direct_Button_5_Up_Clicked(self, *args):
        selections, model = self.Select_USB.get_selected_rows()
        model_vm, treeiter_vm = self.Select.get_selected()

        for row in selections:
            if self.Select_USB.iter_is_selected(row.iter) and row.previous is not None:
                usb_object = self.Direct_TreeView_USB_List[row.iter]
                previous_usb_object = self.Direct_TreeView_USB_List[row.previous.iter]

                subprocess.getoutput(
                    f"VBoxManage usbfilter remove {usb_object[4]} --target {model_vm[treeiter_vm][0]}")
                subprocess.getoutput(
                    f"VBoxManage usbfilter remove {previous_usb_object[4]} --target {model_vm[treeiter_vm][0]}")

                previous_usb_object[4], usb_object[4] = usb_object[4], previous_usb_object[4]

                if usb_object[2] == '':
                    self.usb_empty_filter(previous_usb_object[4], model_vm[treeiter_vm][0])
                else:
                    subprocess.getoutput(
                        f"VBoxManage usbfilter add {previous_usb_object[4]} --target {model_vm[treeiter_vm][0]} --name '{usb_object[1]}' --action hold --vendorid {usb_object[3]} --productid {usb_object[2]}")
                if previous_usb_object[2] == '':
                    self.usb_empty_filter(usb_object[4], model_vm[treeiter_vm][0])
                else:
                    subprocess.getoutput(
                        f"VBoxManage usbfilter add {usb_object[4]} --target {model_vm[treeiter_vm][0]} --name '{previous_usb_object[1]}' --action hold --vendorid {previous_usb_object[3]} --productid {previous_usb_object[2]}")

                self.Direct_TreeView_USB_List.move_before(row.iter, row.previous.iter)

    @staticmethod
    def usb_empty_filter(index, name_vm):
        subprocess.getoutput(
            f"VBoxManage usbfilter add {index} --target {name_vm} --name 'Новый фильтр {index}'  --action hold")


    def Direct_Button_6_Down_Clicked(self, *args):
        selections, model = self.Select_USB.get_selected_rows()
        model_vm, treeiter_vm = self.Select.get_selected()

        for i in range(len(selections) - 1, -1, -1):
            row = selections[i]
            if self.Select_USB.iter_is_selected(row.iter) and row.next is not None:
                usb_object = self.Direct_TreeView_USB_List[row.iter]
                next_usb_object = self.Direct_TreeView_USB_List[row.next.iter]

                subprocess.getoutput(
                    f"VBoxManage usbfilter remove {next_usb_object[4]} --target {model_vm[treeiter_vm][0]}")
                subprocess.getoutput(
                    f"VBoxManage usbfilter remove {usb_object[4]} --target {model_vm[treeiter_vm][0]}")

                next_usb_object[4], usb_object[4] = usb_object[4], next_usb_object[4]

                if next_usb_object[2] == '':
                    self.usb_empty_filter(usb_object[4], model_vm[treeiter_vm][0])
                else:
                    subprocess.getoutput(
                        f"VBoxManage usbfilter add {usb_object[4]} --target {model_vm[treeiter_vm][0]} --name '{next_usb_object[1]}' --action hold --vendorid {next_usb_object[3]} --productid {next_usb_object[2]}")
                if usb_object[2] == '':
                    self.usb_empty_filter(next_usb_object[4], model_vm[treeiter_vm][0])
                else:
                    subprocess.getoutput(
                        f"VBoxManage usbfilter add {next_usb_object[4]} --target {model_vm[treeiter_vm][0]} --name '{usb_object[1]}' --action hold --vendorid {usb_object[3]} --productid {usb_object[2]}")

                self.Direct_TreeView_USB_List.move_after(row.iter, row.next.iter)

    ####################################################RDP############################################################
    def fill_color_cmb(self):
        colors = [
            "256 цветов",
            "High Color 15 бит",
            "High Color 16 бит",
            "True color 24 бит",
            "True color 32 бит",
            "Remote FX 32 бит",
            "GFX RFX Progressive 32 бит",
            "GFX RFX 32 бит",
            "GFX AVC420 32 бит"
            "GFX AVC444 32 бит"
        ]

        self.rdp_cmb_color.remove_all()

        for i in range(len(colors)):
            self.rdp_cmb_color.append(i.__str__(), colors[i])

    def detect_printers(self):
        usb_devices = subprocess.getoutput("VBoxManage list usbhost | grep Product").split("\n")
        self.rdp_printer_cmb.remove_all()

        for item in usb_devices:
            if item.__contains__("Printer") or item.__contains__("printer"):
                self.rdp_printer_cmb.append(usb_devices.index(item).__str__(), item[slice(20, None)])

            if self.rdp_printer_cmb.is_sensitive:
                self.rdp_printer_cb.set_active(False)
                self.rdp_printer_cb.set_sensitive(False)
            else:
                self.rdp_printer_cb.set_sensitive(True)

    def on_show_password_click(self, widget):
        if self.rdp_password.get_visibility():
            self.rdp_password.set_visibility(False)
        else:
            self.rdp_password.set_visibility(True)

    def on_browse_click(self, widget):
        self.rdp_shared_folder.set_text(self.show_explorer())

    def show_explorer(self):
        dialog = tkinter.Tk()
        dialog.withdraw()
        directory_path = filedialog.askdirectory(parent=dialog, initialdir="/")
        return directory_path

    def on_shared_checked(self, widget):
        if self.rdp_shared_folder_cb.get_active():
            self.rdp_shared_folder.set_sensitive(True)
            self.rdp_browse_btn.set_sensitive(True)
        else:
            self.rdp_shared_folder.set_sensitive(False)
            self.rdp_browse_btn.set_sensitive(False)

    def on_rb_default_toggled(self, widget):
        self.rdp_cmb_color.set_sensitive(False)
        self.resolution = None

    def on_rb_client_toggled(self, widget):
        if self.rdp_rb_client.get_active():
            self.resolution = "/f "
            print(self.resolution)
        else:
            self.resolution = None
        self.rdp_cmb_color.set_sensitive(False)

    def on_rb_manual_toggled(self, widget):
        if self.rdp_rb_manual.get_active():
            self.rdp_cmb_color.set_sensitive(True)
        else:
            self.resolution = None

    def on_color_selection_changed(self, widget):

        if self.rdp_cmb_color.get_active_text().__contains__("15"):
            self.resolution = "15"

        if self.rdp_cmb_color.get_active_text().__contains__("16"):
            self.resolution = "16"

        if self.rdp_cmb_color.get_active_text().__contains__("24"):
            self.resolution = "24"

        if self.rdp_cmb_color.get_active_text().__contains__("32"):
            self.resolution = "32"

    def create_rdp(self, widget):
        dialog = RdpIconDialog.Dialog()
        result = dialog.run_dialog()

        self.window_title = self.rdp_window_title.get_text()
        self.printer = self.rdp_printer_cmb.get_active_text()
        self.audio = self.rdp_sound_cb.get_active()
        self.shared_folder = self.rdp_shared_folder.get_text()
        self.login = self.rdp_login.get_text()
        self.password = self.rdp_password.get_text()
        self.ip = self.rdp_ip.get_text()
        self.port = self.rdp_port.get_text()
        self.domain = self.rdp_domain.get_text()
        self.path = dialog.get_folder()
        self.file_name = dialog.get_file_name()

        if result:
            RDPBuilder.RdpBuilder(
                self.vm_name,
                self.resolution,
                self.window_title,
                self.printer,
                self.audio,
                self.shared_folder,
                self.login,
                self.password,
                self.ip,
                self.port,
                self.domain,
                self.path,
                self.file_name)


class Dialog:
    def __init__(self, owner):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("New.glade")
        self.Second_Window = self.builder.get_object("window2")
        self.builder.connect_signals(self)
        self.Derecrion = self.builder.get_object("Derection_box")
        self.Name_d = self.builder.get_object("Name_directory")
        self.Read_t = self.builder.get_object("Read_only_tog")
        self.Auto_t = self.builder.get_object("Auto_mont_tog")
        self.Mont_place = self.builder.get_object("Mont_Place")
        self.Second_Window.run()
        self.owner = owner

    # def metod(self):
    #     print("destroy!!!!!!")

    def Add_shared_folder(self, button):
        self.Name = self.Name_d.get_text()
        self.place = self.Mont_place.get_text()
        self.true_not_true()

        shared = VM.SharedFolder(str(self.Name), str(self.dirname), self.RO, self.AM, str(self.place))
        machines = VM.VirtualMachines()
        vmm = machines.vm_list[0]
        machines.add_shared_folder(shared, vmm)

        print(self.dirname)
        print(self.Name)
        print(self.RO)
        print(self.AM)
        print(self.place)
        main.Re_gen()
        self.Second_Window.destroy()

    def cancel_clicked_cb(self, button):
        self.Second_Window.destroy()

    def true_not_true(self):
        if self.Read_t.get_active():
            self.RO = True
        else:
            self.RO = False
        if self.Auto_t.get_active():
            self.AM = True
        else:
            self.AM = False

    def Search_butt(self, button):
        root = tkinter.Tk()
        root.withdraw()
        self.dirname = filedialog.askdirectory(parent=root, initialdir="/", title='Please select a directory')
        self.Derecrion.set_text(self.dirname)
        self.papka = self.dirname.split('/')
        self.Name_d.set_text(self.papka[len(self.papka) - 1])

    def RA_Connect_Button_Clicked(self, *args):
        ip = self.entry_ip_remote.get_text().strip()
        login = self.entry_login_remote.get_text().strip()
        password = self.entry_password_remote.get_text().strip()
        domain = self.entry_domain_remote.get_text().strip()
        app_name = self.entry_app_remote.get_text().strip()
        port = self.entry_port_remote.get_text().strip()
        if port == '':
            return
        if 1000 <= int(port) <= 65536 \
                and ip != '' \
                and login != '' \
                and app_name != '':
            execute = f'xfreerdp /u:{login}{f" /p:{password}" if password != "" else ""} /v:{ip}:{port}'
            execute += '' if domain == '' else f' /d:{domain}'

            path = f"'/home/superadmin/Рабочий стол/{app_name}.desktop'"
            SendingCommand.create_connection_shortcut(execute, path)


class DialogChange:

    def __init__(self, folder):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("New.glade")
        self.Third_windows = self.builder.get_object("window3")
        self.builder.connect_signals(self)
        self.DerecrionC = self.builder.get_object("Derection_box1")
        self.Name_dC = self.builder.get_object("Name_directory1")
        self.Read_tC = self.builder.get_object("Read_only_tog1")
        self.Auto_tC = self.builder.get_object("Auto_mont_tog1")
        self.Mont_placeC = self.builder.get_object("Mont_Place1")
        self.folder = folder

        self.DerecrionC.set_text(folder.folder_path)
        self.Name_dC.set_text(folder.folder_name)
        self.Read_tC.set_active(folder.folder_access)
        self.Auto_tC.set_active(folder.folder_automount)
        self.Mont_placeC.set_text(folder.folder_mount_point)

        if self.Mont_placeC == " --auto-mount-point=True":
            # if "--auto-mount-point=True" in self.Mont_placeC:
            self.Mont_placeC = "auto"

        self.Third_windows.run()

    def Search_butt(self, button):
        root = tkinter.Tk()
        root.withdraw()
        self.dirname = filedialog.askdirectory(parent=root, initialdir="/", title='Please select a directory')
        self.DerecrionC.set_text(self.dirname)
        self.papka = self.dirname.split('/')
        self.Name_dC.set_text(self.papka[len(self.papka) - 1])

    def Change(self, button):

        if self.Read_tC.get_active():
            self.RO = True
        else:
            self.RO = False
        if self.Auto_tC.get_active():
            self.AM = True
        else:
            self.AM = False

        self.Name = self.Name_dC.get_text()
        self.place = self.Mont_placeC.get_text()
        self.dirname = self.DerecrionC.get_text()

        shared = VM.SharedFolder(str(self.Name), str(self.dirname), self.RO, self.AM, str(self.place))
        machines = VM.VirtualMachines()
        vmm = machines.vm_list[0]
        vmms = vmm.getname()
        subprocess.getoutput(f"VBoxManage sharedfolder remove '{vmms}' --name {self.folder.folder_name}")
        machines.add_shared_folder(shared, vmm)

        print(self.Name_dC)
        print(self.DerecrionC)
        print(self.Read_tC)
        print(self.Auto_tC)
        print(self.Mont_placeC)

        self.Third_windows.destroy()

        main.Re_gen()

    def Cancel(self, button):
        self.Third_windows.destroy()


if __name__ == '__main__':
    main = Main(folder=Main)
    Gtk.main()
