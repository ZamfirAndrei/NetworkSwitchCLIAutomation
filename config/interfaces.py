import time
import re

from Management import ssh, telnet


class Interface:

    def __init__(self, ip_session="10.2.109.178"):

        print("Clasa Interface")

        self.ip_session = ip_session
        self.session = ssh.SSH(ip=ip_session)
        self.tn = telnet.Telnet(ip=ip_session)

    def shut_interface(self, interface):

        self.session.connect()
        self.session.send_cmd(cmd="conf t\r\n")
        self.session.send_cmd(cmd=f"int {interface}\r\n")
        self.session.send_cmd(cmd="shut\r\n")
        output = self.session.read()
        # print(output)
        self.session.close()

    def no_shut_interface(self, interface):

        self.session.connect()
        self.session.send_cmd(cmd="conf t\r\n")
        self.session.send_cmd(cmd=f"int {interface}\r\n")
        self.session.send_cmd(cmd="no shut\r\n")
        output = self.session.read()
        # print(output)
        self.session.close()

    def add_routed_port(self, interface):

        self.session.connect()
        self.session.send_cmd(cmd="conf t\r\n")
        self.session.send_cmd(cmd=f"int {interface}\r\n")
        self.session.send_cmd(cmd="shut\r\n")
        self.session.send_cmd(cmd="no sw\r\n")
        output = self.session.read()
        print(output)
        self.session.close()

    def remove_routed_port(self, interface):

        self.session.connect()
        self.session.send_cmd(cmd="conf t\r\n")
        self.session.send_cmd(cmd=f"int {interface}\r\n")
        self.session.send_cmd(cmd="shut\r\n")
        self.session.send_cmd(cmd="sw\r\n")
        output = self.session.read()
        print(output)
        self.session.close()


obj = Interface(ip_session="10.2.109.136")
# obj.shut_interface(interface="Gi 0/4")
# obj.no_shut_interface(interface="Gi 0/4")
# obj.add_routed_port(interface="Gi 0/5")
# obj.remove_routed_port(interface="Gi 0/5")