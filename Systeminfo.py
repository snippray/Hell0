import subprocess
import re
import errno, os, winreg

class SystemInfo:
    def __init__(self):
        self.host_name = self.get_host_name()
        self.os_name = self.get_os_name()
        self.os_architecture = self.get_os_architecture()
        self.os_version = self.get_os_version()
        self.cpu_name = self.get_cpu_name()
        self.cpu_cores = self.get_cpu_cores()
        self.gpu = self.get_gpu()
        self.bios_name = self.get_bios_name()
        self.bios_version = self.get_bios_version()
        self.bios_manufacturer = self.get_bios_manufacturer()
        self.softwares = list()


    def get_system_softwares(self):
        """
        description:
        ------------
        return system all installed programs, apps or packages
        by search in registry key

        args:
        ------------

        return:
        ------------
        :list like [[software1_name,version],[software2_name,version],...] or None if error occured

        """
        try:
            proc_arch = os.environ['PROCESSOR_ARCHITECTURE'].lower()
        except:
            pass
        try:
            proc_arch64 = os.environ['PROCESSOR_ARCHITEW6432'].lower()
        except:
            pass
        if proc_arch == 'x86' and not proc_arch64:
            arch_keys = {0}
        elif proc_arch == 'x86' or proc_arch == 'amd64':
            arch_keys = {winreg.KEY_WOW64_32KEY, winreg.KEY_WOW64_64KEY}
        else:
            raise Exception("Unhandled arch: %s" % proc_arch)
        for arch_key in arch_keys:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", 0, winreg.KEY_READ | arch_key)
            for i in range(0, winreg.QueryInfoKey(key)[0]):
                skey_name = winreg.EnumKey(key, i)
                skey = winreg.OpenKey(key, skey_name)
                software_name = None
                software_version = None
                try:
                    software_name = winreg.QueryValueEx(skey, 'DisplayName')[0]
                except OSError as e:
                    if e.errno == errno.ENOENT:
                        pass
                try:
                    software_version = winreg.QueryValueEx(skey, 'DisplayVersion')[0]
                except OSError as e:
                    if e.errno == errno.ENOENT:
                        pass
                finally:
                    skey.Close()
                if software_name is not None:
                    self.softwares.append([software_name,software_version])

        return self.softwares

    def get_host_name(self):
        """
        description:
        ------------
        get system host name

        args:
        ------------

        return:
        ------------
        system host name 

        """
        process = subprocess.Popen(["wmic", "computersystem", "get", "name"], stdout=subprocess.PIPE)
        stdout, err = process.communicate() 
        self.host_name = str(stdout).split('\\r\\r\\n')[1].strip()
        return self.host_name
    
    def get_os_name(self):
        """
        description:
        ------------
        get system os name

        args:
        ------------

        return:
        ------------
        system os name 

        """
        process = subprocess.Popen(["wmic", "os", "get", "name"], stdout=subprocess.PIPE)
        stdout, err = process.communicate() 
        self.os_name = str(stdout).split('\\r\\r\\n')[1].strip().split('|')[0]
        return self.os_name

    def get_os_version(self):
        """
        description:
        ------------
        get system os version

        args:
        ------------

        return:
        ------------
        system os version 

        """
        process = subprocess.Popen(["wmic", "os", "get", "version"], stdout=subprocess.PIPE)
        stdout, err = process.communicate() 
        self.os_version = str(stdout).split('\\r\\r\\n')[1].strip()
        return self.os_version


    def get_os_architecture(self):
        """
        description:
        ------------
        get system os architecture

        args:
        ------------

        return:
        ------------
        system os architecture 

        """
        process = subprocess.Popen(["wmic", "os", "get", "OSArchitecture"], stdout=subprocess.PIPE)
        stdout, err = process.communicate() 
        self.os_architecture = str(stdout).split('\\r\\r\\n')[1].strip()
        return self.os_architecture

    def get_cpu_name(self):
        """
        description:
        ------------
        get system cpu name

        args:
        ------------

        return:
        ------------
        system cpu name 

        """
        process = subprocess.Popen(["wmic", "cpu", "get", "name"], stdout=subprocess.PIPE)
        stdout, err = process.communicate() 
        self.cpu_name = str(stdout).split('\\r\\r\\n')[1].strip()
        return self.cpu_name

    def get_gpu(self):
        """
        description:
        ------------
        get system number of cpu cores

        args:
        ------------

        return:
        ------------
        system number of cpu cores 

        """
        process = subprocess.Popen(["wmic", "cpu", "get", "NumberOfCores"], stdout=subprocess.PIPE)
        stdout, err = process.communicate() 
        self.cpu_cores = str(stdout).split('\\r\\r\\n')[1].strip()
        return self.cpu_cores

    def get_cpu_cores(self):
        """
        description:
        ------------
        get system number of cpu cores

        args:
        ------------

        return:
        ------------
        system number of cpu cores 

        """
        process = subprocess.Popen(["wmic", "cpu", "get", "NumberOfCores"], stdout=subprocess.PIPE)
        stdout, err = process.communicate() 
        self.cpu_cores = str(stdout).split('\\r\\r\\n')[1].strip()
        return self.cpu_cores

    def get_gpu(self):
        """
        description:
        ------------
        get system gpu informations

        args:
        ------------

        return:
        ------------
        system gpu informations

        """
        process = subprocess.Popen(["wmic" ,"path" ,"win32_VideoController", "get" ,"name"], stdout=subprocess.PIPE)
        stdout, err = process.communicate() 
        self.gpu = [item for item in re.sub(' +','',str(stdout)).split('\\r\\r\\n')[1:] if len(item)>2]
        return self.gpu

    def get_bios_name(self):
        """
        description:
        ------------
        get system bios name

        args:
        ------------

        return:
        ------------
        system bios name 

        """
        process = subprocess.Popen(["wmic" ,"bios" ,"get", "name"], stdout=subprocess.PIPE)
        stdout, err = process.communicate() 
        self.bios_name = str(stdout).split('\\r\\r\\n')[1].strip()
        return self.bios_name
    
    def get_bios_version(self):
        """
        description:
        ------------
        get system bios version

        args:
        ------------

        return:
        ------------
        system bios version 

        """
        process = subprocess.Popen(["wmic" ,"bios" ,"get", "version"], stdout=subprocess.PIPE)
        stdout, err = process.communicate() 
        self.bios_version = str(stdout).split('\\r\\r\\n')[1].strip()
        return self.bios_name


    def get_bios_manufacturer(self):
        """
        description:
        ------------
        get system bios manufacturer

        args:
        ------------

        return:
        ------------
        system bios manufacturer 

        """
        process = subprocess.Popen(["wmic" ,"bios" ,"get", "Manufacturer"], stdout=subprocess.PIPE)
        stdout, err = process.communicate() 
        self.bios_manufacturer = str(stdout).split('\\r\\r\\n')[1].strip()
        return self.bios_manufacturer