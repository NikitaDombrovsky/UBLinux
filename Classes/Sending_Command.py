import os
import subprocess


class SendingCommand:

    @staticmethod
    def VM_ON(name):
        # os.system("VBoxManage startvm %a -type headless " % name)
        subprocess.getoutput("VBoxManage startvm %a -type headless " % name)

    @staticmethod
    def VM_OFF(name):
        subprocess.getoutput("VBoxManage controlvm %a acpipowerbutton" % name)

    @staticmethod
    def VM_SAVE(name):
        subprocess.getoutput("VBoxManage controlvm %a savestate" % name)

    @staticmethod
    def VM_RESET(name):
        subprocess.getoutput("VBoxManage controlvm %a reset" % name)

    # @staticmethod
    # def VM_OUT_ALL_NAME(Out):
    #     Out = subprocess.getoutput('v=$(VBoxManage list vms);awk -F\'\"|\\"\' \'{print $2}\' <<< $v').split("\n")
    #     return Out