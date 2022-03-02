import multiprocessing as mp
import os
import re
import subprocess
from threading import Thread
from time import sleep
import gi

import array
#import current as current

import main
from main import Main


gi.require_version("Gtk", "3.0")

from gi.repository import Gtk


class Main_Thread_Class():
    flag = True

    def __init__(self, Main_Array, ctx):

        self.Main_Array = Main_Array
        self.Checker_Changer = 0
        self.select = None
        self.ctx = ctx


    def Start_Thread(self):
        self.arg1 = "Test"
        self.arg2 = "False"
        self.arg3 = "Test"
        self.Mutex = 0
        t1 = Thread(target=self.Spring, daemon=True)
        t1.start()
        self.Update_Arg()



    def Spring(self):
        while self.flag:
            if self.Mutex == 0:
                Out_All_Name = subprocess.getoutput(
                    'v=$(VBoxManage list vms);awk -F\'\"|\\"\' \'{print $2}\' <<< $v').split("\n")
                Out_All_Hash = subprocess.getoutput(
                    'v=$(VBoxManage list vms);awk -F\'\"|\\"\' \'{print $3}\' <<< $v').split("\n")
                Out_ON_Hash = subprocess.getoutput(
                    'v=$(VBoxManage list runningvms);awk -F\'\"|\\"\' \'{print $3}\' <<< $v').split("\n")
                self.Second_Array = [[0] * 3 for i in range(len(Out_All_Name))]
                for i in range(len(Out_All_Name)):
                    Out_Bool = False
                    for v in range(len(Out_ON_Hash)):
                        if Out_All_Hash[i] == Out_ON_Hash[v]:
                            Out_Bool = True
                    Out_IP = re.split('"|<', subprocess.getoutput(
                        f'VBoxManage showvminfo "{Out_All_Name[i]}" | grep TCP/Address '))
                    if Out_IP[0] == "" or Out_IP[1] == 'not set>':
                        self.Second_Array[i][0] = Out_All_Name[i]
                        self.Second_Array[i][1] = Out_Bool
                        self.Second_Array[i][2] = "0.0.0.0"
                    else:
                        self.Second_Array[i][0] = Out_All_Name[i]
                        self.Second_Array[i][1] = Out_Bool
                        self.Second_Array[i][2] = Out_IP[1]

                for i in range(3):
                    if self.Main_Array[i][1] != self.Second_Array[i][1]:
                        print("Произошли изменения")
                        if self.treeiter is not None:
                            self.arg1 = self.Second_Array[i][0]
                            self.arg2 = bool(self.Second_Array[i][1])
                            self.arg3 = self.Second_Array[i][2]
                            self.Checker_Changer = 1
                            self.Main_Array[i][0] = self.Second_Array[i][0]
                            self.Main_Array[i][1] = self.Second_Array[i][1]
                            self.Main_Array[i][2] = self.Second_Array[i][2]
                if self.select != None:
                    self.ctx.getcontext().Virtual_TreeView_Changed(self.select)
                #self.af_event()
                #main.Main.Virtual_TreeView_Changed(main, self.select)
                #main.Main.CRINGE(main, self.select)
            #print("Поток")
            sleep(5)
    # def af_event(event):
    #
    #     main.object.Virtual_TreeView_Changed(event.select)
    #     print("1")
    def Update_Arg(self):
        self.arg1_1 = self.arg1
        self.arg1_2 = self.arg2
        self.arg1_3 = self.arg3

    def Checker(self):
        if self.Checker_Changer == 1:
            self.Update_Arg()

    def Constructor(self, iter, model, Selection):
        self.treeiter = iter
        self.model = model
        self.select = Selection  # Зачем

    def Stop_Thread(self):
        self.flag = False
    # def after_event(event):
    #     event.arg1 = 0
    #     event.Update_Arg()
    #     #event.Virtual_TreeView_Changed()
    #     print("!вв1Ё")
