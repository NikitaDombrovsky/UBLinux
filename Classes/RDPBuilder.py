import os


class RdpBuilder:

    def __init__(self, vm, resolution, window_title, printer, audio, shared_folder, login, password, ip, port, domain, path, file_name):
        self.vm = vm
        self.login = login
        self.password = password
        self.ip = ip
        self.port = port
        self.path = path
        self.file_name = file_name

        if resolution is None:
            self.resolution = None
        else:
            self.resolution = resolution

        if window_title == "":
            self.window_title = None
        else:
            self.window_title = window_title

        if printer is None:
            self.printer = None
        else:
            self.printer = printer

        if audio is None:
            self.audio = None
        else:
            self.audio = audio

        if shared_folder == "" or shared_folder is None:
            self.shared_folder = None
        else:
            self.shared_folder = shared_folder

        if domain is None:
            self.domain = None
        else:
            self.domain = domain

        self.assemble_command()

    def assemble_command(self):

        if not self.audio:
            self.audio = None

        cmd = str(f"VBoxManage startvm {self.vm} --type headless; ")

        if self.shared_folder is not None:
            folder_name_raw = self.shared_folder.split("/")
            folder_name = folder_name_raw[-1]
            cmd += f"VBoxManage sharedfolder add {self.vm} --name {folder_name} --hostpath {self.shared_folder} --readonly --automount;"

        cmd += f"xfreerdp /u:{self.login} /p:{self.password} /v:{self.ip}:{self.port} "

        if self.window_title != "":
            cmd += f"/t:{self.window_title} "

        if self.domain != "":
            cmd += f"/d:{self.domain} "

        if self.resolution is not None:
            if self.resolution == "/f ":
                cmd += self.resolution
            else:
                cmd += f"/bpp:{self.resolution} "

        if self.printer is not None:
            cmd += f"/a:printer, {self.printer} "

        if self.audio is not None:
            cmd += f"/sound:sys:alsa /microphone:sys:alsa "

        os.system(
            "echo \"[Desktop Entry]\n"
            f"Type= Application\n"
            f"Categories= System; Utility;\n"
            f"Exec= bash -c \'{cmd}\'\n"
            f"Terminal= true\n"
            f"StartupNotify= true\n"
            f"Name= {self.file_name}\n"
            f"Name[ru]= {self.file_name}\n"
            f"Comment= Start virtual machine\n"
            f"Comment[ru]= Запуск виртуальной машины\n"
            f"NoDisplay= false\n"
            f"Hidden= false\" > {self.path}/{self.file_name}.desktop; chmod +x  {self.path}//{self.file_name}.desktop"
        )

