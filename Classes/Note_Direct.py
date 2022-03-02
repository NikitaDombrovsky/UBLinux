# import subprocess
#
# import gi
#
# ##################################################
# ##################################################
# ##############Все что нужно было лежит в Main, но это на всякий оставил если тут нет ничего нужного можешь удалить##############
# ##############Все что нужно было лежит в Main, но это на всякий оставил если тут нет ничего нужного можешь удалить##############
# ##############Все что нужно было лежит в Main, но это на всякий оставил если тут нет ничего нужного можешь удалить##############
# ##############Все что нужно было лежит в Main, но это на всякий оставил если тут нет ничего нужного можешь удалить##############
# ##############Все что нужно было лежит в Main, но это на всякий оставил если тут нет ничего нужного можешь удалить##############
# ##############Все что нужно было лежит в Main, но это на всякий оставил если тут нет ничего нужного можешь удалить##############
# ##############Все что нужно было лежит в Main, но это на всякий оставил если тут нет ничего нужного можешь удалить##############
# ##############Все что нужно было лежит в Main, но это на всякий оставил если тут нет ничего нужного можешь удалить##############
# ##############Все что нужно было лежит в Main, но это на всякий оставил если тут нет ничего нужного можешь удалить##############
# ##############Все что нужно было лежит в Main, но это на всякий оставил если тут нет ничего нужного можешь удалить##############
# ##############Все что нужно было лежит в Main, но это на всякий оставил если тут нет ничего нужного можешь удалить##############
# ##############Все что нвужно было лежит в Main, но это на всякий оставил если тут нет ничего нужного можешь удалить##############
# ##################################################
# ##################################################
#
#
# gi.require_version("Gtk", "3.0")
# from gi.repository import Gtk
#
#
# class SignalHandler:
#     @staticmethod
#     def onDestroy(self, *args):
#         Gtk.main_quit()
#
#
# class UsbDevice:
#     def __init__(self, index, active, filter_name, vendor_id, product_id, product_name):
#         self.index = index
#         self.active = active
#         self.filter_name = filter_name
#         self.vendor_id = vendor_id
#         self.product_id = product_id
#         self.product_name = product_name
#
#
# class Note_Direct:
#     def __init__(self, ctx):
#         self.ctx = ctx
#         # self.builder = builder
#         # self.Direct_TreeView_USB = self.builder.get_object("Direct_TreeView_USB")
#         # self.Direct_TreeView_USB_List = Gtk.ListStore(bool, str)
#         # self.Direct_Button_1 = self.builder.get_object("Direct_Button_1")
#         # self.Direct_Button_2 = self.builder.get_object("Direct_Button_2")
#         # self.Direct_Button_3 = self.builder.get_object("Direct_Button_3")
#         # self.Direct_Button_4 = self.builder.get_object("Direct_Button_4")
#         # self.Direct_Button_5 = self.builder.get_object("Direct_Button_5")
#         #self.Direct_TreeView_Generator()
#
#     # def Direct_TreeView_Generator(self, *args):
#     #     self.Direct_TreeView_Second()
#     #
#     #     one_column = Gtk.TreeViewColumn(title="Активно", cell_renderer=Gtk.CellRendererToggle(), active=0)
#     #     two_column = Gtk.TreeViewColumn(title="Устройство", cell_renderer=Gtk.CellRendererText(), text=1)
#     #
#     #     self.Direct_TreeView.append_column(one_column)
#     #     self.Direct_TreeView.append_column(two_column)
#     #
#     #     self.Direct_TreeView.set_model(self.Direct_TreeView_List)
#
#
#     def Direct_TreeView_USB_Generator(self, Name_VM):
#         usb_list = self.get_usb_list(name_vm=Name_VM)
#         print(usb_list)
#         for el in usb_list:
#             # self.Direct_TreeView_USB_List.append([True, el.filter_name, el.product_id, el.vendor_id, int(el.index)])
#             self.ctx.getcontext().Direct_TreeView_USB_List.append([True, el.filter_name, el.product_id, el.vendor_id, int(el.index)])
#
#         # bool_renderer = Gtk.CellRendererToggle()
#         # text_renderer = Gtk.CellRendererText()
#         active_column = Gtk.TreeViewColumn(title="Активно", cell_renderer=Gtk.CellRendererToggle(), active=0)
#         device_column = Gtk.TreeViewColumn(title="Устройство", cell_renderer=Gtk.CellRendererText(), text=1)
#         active_column.set_sort_column_id(0)
#
#         self.ctx.getcontext().Direct_TreeView_USB.append_column(active_column)
#         self.ctx.getcontext().Direct_TreeView_USB.append_column(device_column)
#
#         self.ctx.getcontext().Direct_TreeView_USB.set_model(self.ctx.getcontext().Direct_TreeView_USB_List)
#
#
#
#     def get_usb_list(self, name_vm):
#         usb_lst = subprocess.getoutput(
#             "v=$(echo $(VBoxManage showvminfo " + name_vm + "));awk -F \'USB Device Filters: | Bandwidth groups:\' \'{print $2}\'  <<< $v").split(
#             "Index: ")  # получаем полный список usb для машины test1
#         usb_lst_ok = list()
#         i = 1
#         while i < len(usb_lst):  # в цикле проходим по всем устройствам
#             tempIndex = usb_lst[i][0]
#             tempActive = usb_lst[i][usb_lst[i].index("Active:"):usb_lst[i].find("Name:")].split(": ")[1]  # yes
#             tempFilterName = usb_lst[i][usb_lst[i].index("Name:"):usb_lst[i].find("VendorId:")].split(": ")[1]
#             tempVendorId = usb_lst[i][usb_lst[i].index("VendorId:"):usb_lst[i].find("ProductId:")].split(": ")[1]
#             tempProductId = usb_lst[i][usb_lst[i].index("ProductId:"):usb_lst[i].find("Revision:")].split(": ")[1]
#             tempProductName = usb_lst[i][usb_lst[i].index("Product:"):usb_lst[i].find("Remote:")].split(": ")[1]
#             reliseObject = UsbDevice(tempIndex, tempActive, tempFilterName, tempVendorId, tempProductId,
#                                      tempProductName)  # заполняем временный объект
#
#             usb_lst_ok.append(reliseObject)
#             i += 1
#         return usb_lst_ok  # возврат списка обьектов UsbDevice
#
#     # Продолжение заполнения
#     # def Direct_TreeView_Second(self):
#     #     USB_List = subprocess.getoutput('VBoxManage list usbhost').split("\n")
#         # Out_All_Name = subprocess.getoutput('v=$(VBoxManage list vms);awk -F\'\"|\\"\' \'{print $2}\' <<< $v').split("\n")
#         # Out_All_Hash = subprocess.getoutput('v=$(VBoxManage list vms);awk -F\'\"|\\"\' \'{print $3}\' <<< $v').split("\n")
#         # Out_ON_Hash = subprocess.getoutput('v=$(VBoxManage list runningvms);awk -F\'\"|\\"\' \'{print $3}\' <<< $v').split("\n")
#         # self.Main_Array = [[0] * 3 for i in range(len(Out_All_Name))]
#         # # self.arg = [0 for x in range(len(Out_All_Name))]
#         # for i in range(len(Out_All_Name)):
#         #     Out_Bool = False
#         #     for v in range(len(Out_ON_Hash)):
#         #         if Out_All_Hash[i] == Out_ON_Hash[v]:
#         #             Out_Bool = True
#         #     Out_IP = re.split('"|<', subprocess.getoutput(f'VBoxManage showvminfo "{Out_All_Name[i]}" | grep TCP/Address '))
#         #     if Out_IP[0] == "" or Out_IP[1] == 'not set>':
#         #         self.Virtual_TreeView_List.append([Out_All_Name[i], Out_Bool, "0.0.0.0"])
#         #         self.Main_Array[i][0] = Out_All_Name[i]
#         #         self.Main_Array[i][1] = Out_Bool
#         #         self.Main_Array[i][2] = "0.0.0.0"
#         #     else:
#         #         self.Virtual_TreeView_List.append([Out_All_Name[i], Out_Bool, Out_IP[i]])
#         #         self.Main_Array[i][0] = Out_All_Name[i]
#         #         self.Main_Array[i][1] = Out_Bool
#         #         self.Main_Array[i][2] = Out_IP[1]
#
#
#     def btn_add_usb_clicked(self, *args):
#         try:
#             dialog = DialogAddUsb()
#
#             if dialog.response_type == Gtk.ResponseType.OK:
#                 for el in dialog.get_result():
#                     model, treeiter = self.get_current_vm()
#                     if treeiter is not None:
#                         last_iter = self.get_iter_last(self.treeview_usb_list)
#                         id = 0 if last_iter is None else self.treeview_usb_list[last_iter][4] + 1
#
#                         SendingCommand.add_usb_filter(id, model[treeiter][0], el)
#                         self.treeview_usb_list.append([el[0], el[1], el[2], el[3], id])
#                         dialog = Gtk.MessageDialog(
#                             transient_for=self.window,
#                             flags=0,
#                             message_type=Gtk.MessageType.INFO,
#                             buttons=Gtk.ButtonsType.OK,
#                             text="Успех!",
#                         )
#                         dialog.format_secondary_text(
#                             "USB-устройство успешно добавлено"
#                         )
#                         dialog.run()
#                         dialog.destroy()
#         except:
#             return
#
#
# # if __name__ == '__main__':
# #     main = Note_Direct()
# #     Gtk.main()
