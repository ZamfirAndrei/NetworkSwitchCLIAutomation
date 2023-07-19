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
        print(f"The interface {interface} has been shut")
        self.session.close()

    def no_shut_interface(self, interface):

        self.session.connect()
        self.session.send_cmd(cmd="conf t\r\n")
        self.session.send_cmd(cmd=f"int {interface}\r\n")
        self.session.send_cmd(cmd="no shut\r\n")
        output = self.session.read()
        # print(output)
        print(f"The interface {interface} has been no-shut")
        self.session.close()

    def add_routed_port(self, interface):

        self.session.connect()
        self.session.send_cmd(cmd="conf t\r\n")
        self.session.send_cmd(cmd=f"int {interface}\r\n")
        self.session.send_cmd(cmd="shut\r\n")
        self.session.send_cmd(cmd="no sw\r\n")
        output = self.session.read()
        # print(output)
        print(f"The routed port {interface} has been created")
        self.session.close()

    def remove_routed_port(self, interface):

        self.session.connect()
        self.session.send_cmd(cmd="conf t\r\n")
        self.session.send_cmd(cmd=f"int {interface}\r\n")
        self.session.send_cmd(cmd="shut\r\n")
        self.session.send_cmd(cmd="sw\r\n")
        output = self.session.read()
        # print(output)
        print(f"The routed port {interface} has been removed")
        self.session.close()

    def show_int_description(self):

        list_of_ports = list()
        list_of_ports_connected_to_others = list()
        list_of_int_vlans = list()

        self.session.connect()
        self.session.send_cmd(cmd="conf t\r\n")
        self.session.send_cmd(cmd="set cli pagination off\r\n")
        self.session.send_cmd(cmd="do sh int desc\r\n")
        output = self.session.read()
        # print(output)

        match = re.findall(r"([GExi]+\d/\d+)\s+([DownUp]+)\s+([DownUp]+)", output)
        match1 = re.findall(r"([GExi]+\d/\d+)\s+([DownUp]+)\s+([DownUp]+)\s+([\w-]+)", output)
        match2 = re.findall(r"(vlan\d+)\s+([DownUp]+)\s+([DownUp]+)", output)

        # print(match)
        # print(match1)
        # print(match2)

        for i in range(len(match)):

            d = {}

            for value in range(len(match[i])):

                d["Interface"] = match[i][0]
                d["Status"] = match[i][1]
                d["Protocol"] = match[i][2]

            list_of_ports.append(d)
            # print(d)

        print(list_of_ports)
        # print(len(list_of_ports))

        for i in range(len(match1)):

            d = {}

            for value in range(len(match1[i])):

                d["Interface"] = match1[i][0]
                d["Status"] = match1[i][1]
                d["Protocol"] = match1[i][2]
                d["Description"] = match1[i][3]

            list_of_ports_connected_to_others.append(d)
            # print(d)

        print(list_of_ports_connected_to_others)
        # print(len(list_of_ports_connected_to_others))

        for i in range(len(match2)):

            d = {}

            for value in range(len(match2[i])):

                d["Interface"] = match2[i][0]
                d["Status"] = match2[i][1]
                d["Protocol"] = match2[i][2]

            list_of_int_vlans.append(d)
            # print(d)

        print(list_of_int_vlans)
        # print(len(list_of_int_vlans))

        self.session.close()

        return list_of_ports, list_of_ports_connected_to_others, list_of_int_vlans


obj = Interface(ip_session="10.2.109.136")
# obj.shut_interface(interface="Gi 0/4")
# obj.no_shut_interface(interface="Gi 0/4")
# obj.add_routed_port(interface="Gi 0/5")
# obj.remove_routed_port(interface="Gi 0/5")
obj.show_int_description()
