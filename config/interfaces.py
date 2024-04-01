import time
import re

from Management import ssh, telnet


class Interface:

    def __init__(self, ip_session="10.2.109.178"):

        print("Class Interface")

        self.ip_session = ip_session
        self.session = ssh.SSH(ip=ip_session)
        self.tn = telnet.Telnet(ip=ip_session)

    def add_port_configuration(self, port, mode=None, pvid=None, acceptable_frame_type=None):

        self.session.connect()
        self.session.send_cmd(cmd="conf t")
        self.session.send_cmd(cmd=f"int {port}")

        if mode is not None:

            self.session.send_cmd(cmd=f"sw mode {mode}")
            print(f"The mode {mode} has been configured on port {port}, on DUT {self.ip_session}")

        if pvid is not None:

            self.session.send_cmd(cmd=f"sw pvid {pvid}")
            print(f"The pvid {pvid} has been configured on port {port}, on DUT {self.ip_session}")

        if acceptable_frame_type is not None:

            self.session.send_cmd(cmd=f"sw acceptable-frame-type {acceptable_frame_type}")
            print(f"The acceptable-frame-type {acceptable_frame_type} has been configured on port {port}, on DUT {self.ip_session}")

        self.session.send_cmd(cmd="exit")
        output = self.session.read()
        # print(output)

        self.session.close()

    def remove_port_configuration(self, port):

        self.session.connect()
        self.session.send_cmd(cmd="conf t")
        self.session.send_cmd(cmd=f"int {port}")
        self.session.send_cmd(cmd="shut; no sw; sw")

        print(f"The configuration for the port {port} has been changed to default on DUT {self.ip_session}")

        self.session.send_cmd(cmd="exit")
        output = self.session.read()
        # print(output)

        self.session.close()

    def shut_interface(self, interface):

        self.session.connect()
        self.session.send_cmd(cmd="conf t")
        self.session.send_cmd(cmd=f"int {interface}")
        self.session.send_cmd(cmd="shut")
        self.session.send_cmd("exit")
        output = self.session.read()
        # print(output)
        print(f"The interface {interface} has been shut on DUT {self.ip_session}")
        self.session.close()

    def shut_interfaces(self, *args):

        self.session.connect()
        self.session.send_cmd(cmd="conf t")

        for interface in args:

            self.session.send_cmd(cmd=f"int {interface}")
            self.session.send_cmd(cmd="shut")
            self.session.send_cmd(cmd="!")
            print(f"The interface {interface} has been shut on DUT {self.ip_session}")
        self.session.send_cmd("exit")
        output = self.session.read()
        # print(output)
        self.session.close()

    def no_shut_interface(self, interface):

        self.session.connect()
        self.session.send_cmd(cmd="conf t")
        self.session.send_cmd(cmd=f"int {interface}")
        self.session.send_cmd(cmd="no shut")
        self.session.send_cmd("exit")
        output = self.session.read()
        # print(output)
        print(f"The interface {interface} has been no-shut on DUT {self.ip_session}")
        self.session.close()

    def no_shut_interfaces(self, *args):

        self.session.connect()
        self.session.send_cmd(cmd="conf t")

        for interface in args:

            self.session.send_cmd(cmd=f"int {interface}")
            self.session.send_cmd(cmd="no shut")
            self.session.send_cmd(cmd="!")
            print(f"The interface {interface} has been no-shut on DUT {self.ip_session}")
        self.session.send_cmd("exit")
        output = self.session.read()
        # print(output)
        self.session.close()

    def add_routed_port(self, interface):

        self.session.connect()
        self.session.send_cmd(cmd="conf t")
        self.session.send_cmd(cmd=f"int {interface}")
        self.session.send_cmd(cmd="shut")
        self.session.send_cmd(cmd="no sw")
        self.session.send_cmd("exit")
        output = self.session.read()
        # print(output)
        print(f"The routed port {interface} has been created on DUT {self.ip_session}")
        self.session.close()

    def remove_routed_port(self, interface):

        self.session.connect()
        self.session.send_cmd(cmd="conf t")
        self.session.send_cmd(cmd=f"int {interface}")
        self.session.send_cmd(cmd="shut")
        self.session.send_cmd(cmd="sw")
        self.session.send_cmd("exit")
        output = self.session.read()
        # print(output)
        print(f"The routed port {interface} has been removed from DUT {self.ip_session}")
        self.session.close()

    def add_routed_ports(self, *args):

        self.session.connect()
        self.session.send_cmd(cmd="conf t")

        for interface in args:

            self.session.send_cmd(cmd=f"int {interface}")
            self.session.send_cmd(cmd="shut")
            self.session.send_cmd(cmd="no sw")
            print(f"The routed port {interface} has been created on DUT {self.ip_session}")
        self.session.send_cmd("exit")
        output = self.session.read()
        # print(output)

        self.session.close()

    def remove_routed_ports(self, *args):

        self.session.connect()
        self.session.send_cmd(cmd="conf t")

        for interface in args:

            self.session.send_cmd(cmd=f"int {interface}")
            self.session.send_cmd(cmd="shut")
            self.session.send_cmd(cmd="sw")
            print(f"The routed port {interface} has been removed from DUT {self.ip_session}")
        self.session.send_cmd("exit")
        output = self.session.read()
        # print(output)

        self.session.close()

    def show_int_description(self):

        list_of_ports = list()
        list_of_ports_connected_to_others = list()
        list_of_int_vlans = list()

        self.session.connect()
        self.session.send_cmd(cmd="conf t")
        self.session.send_cmd(cmd="set cli pagination off")
        self.session.send_cmd(cmd="do sh int desc")
        output = self.session.read()
        # print(output)

        match = re.findall(r"([GExi]+\d/\d+)\s+([DownUp]+)\s+([DownUp]+)", output)
        match1 = re.findall(r"([GExi]+\d/\d+)\s+([DownUp]+)\s+([DownUp]+)\s+([\w./-]+)", output)
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

        # print(list_of_ports)
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

        # print(list_of_int_vlans)
        # print(len(list_of_int_vlans))

        self.session.close()

        return list_of_ports, list_of_ports_connected_to_others, list_of_int_vlans

        # Need to add clear int counter/show interface counters



ip = "10.2.109.238"

# obj = Interface(ip_session=ip)
# obj.shut_interface(interface="Gi 0/4")
# obj.no_shut_interface(interface="Gi 0/4")
# obj.add_routed_port(interface="Gi 0/5")
# obj.remove_routed_port(interface="Gi 0/5")
# obj.show_int_description()
