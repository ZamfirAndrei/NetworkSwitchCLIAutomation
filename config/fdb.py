import re
from Management import ssh, telnet


class FDB:

    def __init__(self, ip_session="10.2.109.178"):

        print("Clasa FDB")

        self.ip_session = ip_session
        self.session = ssh.SSH(ip_session)
        self.tn = telnet.Telnet(ip_session)

    def show_mac_addr_table(self):

        d = {
            "VLAN":"",
            "Mac Address":"",
            "Type":"",
            "Ports":""
        }
        d1 = {}
        mac_addr = list()
        self.session.connect()
        self.session.send_cmd("show mac-address-table\r\n")
        output = self.session.read()
        # print(output)
        match = re.findall(r"(\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+([\w/]+)", output)
        # print(match)

        for attribute in match:
            d1 = {}
            for key, attributes in zip(d.keys(), attribute):
                # print(key, attributes)
                d1[key] = attributes
            mac_addr.append(d1)

        print(mac_addr)
        self.session.close()

        return mac_addr

    def clear_mac_addr_table(self):

        self.session.connect()
        self.session.send_cmd("clear mac-address-table dynamic\r\n")
        # self.session.send_cmd("show mac-address-table\r\n")
        # output = self.session
        # print(output)
        self.session.close()

    def show_mac_addr_table_vlan(self, vlan=None):

        d = {
            "VLAN": "",
            "Mac Address": "",
            "Type": "",
            "Ports": ""
        }
        d1 = {}
        mac_addr = list()
        self.session.connect()
        self.session.send_cmd(f"show mac-address-table vlan {vlan}\r\n")
        output = self.session.read()
        # print(output)
        match = re.findall(r"(\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+([\w/]+)", output)
        # print(match)

        for attribute in match:
            d1 = {}
            for key, attributes in zip(d.keys(), attribute):
                # print(key, attributes)
                d1[key] = attributes
            mac_addr.append(d1)

        print(mac_addr)
        self.session.close()

        return mac_addr

    def show_mac_addr_table_interface(self, interface=None):

        d = {
            "VLAN": "",
            "Mac Address": "",
            "Type": "",
            "Ports": ""
        }
        d1 = {}
        mac_addr = list()
        self.session.connect()
        self.session.send_cmd(f"show mac-address-table interface {interface}\r\n")
        output = self.session.read()
        # print(output)
        match = re.findall(r"(\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+([\w/]+)", output)
        # print(match)

        for attribute in match:
            d1 = {}
            for key, attributes in zip(d.keys(), attribute):
                # print(key, attributes)
                d1[key] = attributes
            mac_addr.append(d1)

        print(mac_addr)
        self.session.close()

        return mac_addr


obj = FDB("10.2.109.198")


obj.clear_mac_addr_table()
obj.show_mac_addr_table()
obj.show_mac_addr_table_vlan(vlan="1")
obj.show_mac_addr_table_interface(interface="gi 0/9")