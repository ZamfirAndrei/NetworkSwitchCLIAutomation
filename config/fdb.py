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

    def show_mac_addr_table_static(self):

        d = {
            "VLAN":"",
            "Mac Address":"",
            "Type":"",
            "Ports":""
        }
        d1 = {}
        mac_addr = list()
        self.session.connect()
        self.session.send_cmd("show mac-address-table static unicast\r\n")
        output = self.session.read()
        # print(output)
        match = re.findall(r"(\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+)\s+(\w+)\s+!\s+([\w/]+)", output)
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

    def create_static_mac_addr(self, static_mac, vlan, interface):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"mac static unicast {static_mac}  vlan {vlan} interface {interface}\r\n")
        # self.session.send_cmd("show mac-address-table\r\n")
        # output = self.session
        # print(output)
        self.session.close()

    def remove_static_mac_addr(self, static_mac, vlan):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"no mac static unicast {static_mac} vlan {vlan}\r\n")
        # self.session.send_cmd("show mac-address-table\r\n")
        # output = self.session
        # print(output)
        self.session.close()


obj = FDB("10.2.109.178")

# obj.clear_mac_addr_table()
# obj.show_mac_addr_table()
# obj.show_mac_addr_table_vlan(vlan="15")
# obj.show_mac_addr_table_interface(interface="gi 0/5")
# obj.show_mac_addr_table_static()
# obj.create_static_mac_addr(static_mac="cc:bb:00:00:00:00",vlan="1",interface="gi 0/5")
# obj.remove_static_mac_addr(static_mac="cc:bb:00:00:00:00",vlan="10")