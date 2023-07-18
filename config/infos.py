import time
import re

from Management import ssh, telnet


class INFOs:

    def __init__(self,ip_session="10.2.109.178"):

        print("Clasa INFOs")

        self.ip_session = ip_session
        self.session = ssh.SSH(ip=ip_session)
        self.tn = telnet.Telnet(ip=ip_session)

    def show_system_info(self):

        self.session.connect()
        self.session.send_cmd(cmd="conf t\r\n")
        self.session.send_cmd(cmd="set cli pagination off\r\n")
        self.session.send_cmd(cmd="do show system info\r\n")
        output = self.session.read()
        # print(output)

        software_version = re.findall(r"CNS Software Version\s+:\s+([\w.-]+)", output)
        model_name = re.findall(r"Model Name\s+:\s+([\w-]+)", output)
        switch_mac_address =  re.findall(r"Switch MAC Address\s+:\s+(\w+.\w+.\w+.\w+.\w+.\w+)", output)
        serial_number = re.findall(r"Serial Number\s+:\s+(\w+)", output)
        system_name = re.findall(r"System Name\s+:\s+([\w-]+)", output)

        print(software_version)
        print(model_name)
        print(switch_mac_address)
        print(serial_number)
        print(system_name)

        return software_version, model_name, switch_mac_address, serial_number, system_name

    def show_run(self, protocol=None):

        self.session.connect()
        self.session.send_cmd(cmd="conf t\r\n")
        self.session.send_cmd(cmd="set cli pagination off\r\n")
        self.session.send_cmd(cmd=f"do show run {protocol}\r\n")
        output = self.session.read()
        print(output)


obj = INFOs(ip_session="10.2.109.136")
obj.show_system_info()
obj.show_run()

