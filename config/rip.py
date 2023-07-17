import re
import time

from Management import ssh, telnet


class RIP:

    def __init__(self, ip_session):

        print("Clasa RIP")
        self.ip_session = ip_session
        self.session = ssh.SSH(ip_session)
        self.tn = telnet.Telnet(ip_session)

    def enable_rip(self):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router rip\r\n")
        print("The RIP process has been enabled")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def disable_rip(self):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("no router rip\r\n")
        print("The RIP process has been disabled")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def advertise_network(self, ip_network=None):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router rip\r\n")
        self.session.send_cmd(f"network {ip_network}\r\n")
        self.session.send_cmd("version 2")
        print("The network has been advertise in rip")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def remove_network(self, ip_network=None):
        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router rip\r\n")
        self.session.send_cmd(f"no network {ip_network}\r\n")
        print("The network has been removed from rip process")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def add_passive_interface(self, vlan =None, interface=None):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router rip\r\n")

        if vlan is None:

            self.session.send_cmd(f"passive-interface {interface}\r\n")

        else:

            self.session.send_cmd(f"passive-interface vlan {vlan}\r\n")

        print("The passive-interface has been created")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def remove_passive_interface(self, vlan=None, interface=None):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router rip\r\n")

        if vlan is None:

            self.session.send_cmd(f"no passive-interface {interface}\r\n")

        else:

            self.session.send_cmd(f"no passive-interface vlan {vlan}\r\n")

        print("The passive-interface has been removed")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def redistribute_connected(self):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router rip\r\n")
        self.session.send_cmd("redistribute connected\r\n")
        print("The connected networks have been redistributed into RIP process")
        # time.sleep(2)
        # output = self.session.read()
        # print(output)
        # self.session.close()

    def redistribute_static(self):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router rip\r\n")
        self.session.send_cmd("redistribute static\r\n")
        print("The static routes have been redistributed into RIP process")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def redistribute_all(self):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router rip\r\n")
        self.session.send_cmd("redistribute all\r\n")
        print("All routes have been redistributed into RIP process")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def redistribute_ospf(self):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router rip\r\n")
        self.session.send_cmd("redistribute ospf\r\n")
        print("OSPF routes have been redistributed into RIP process")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def remove_redistribute_connected(self):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router rip\r\n")
        self.session.send_cmd("no redistribute connected\r\n")
        print("The connected networks have been removed from RIP process")
        # time.sleep(2)
        # output = self.session.read()
        # print(output)
        # self.session.close()

    def remove_redistribute_static(self):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router rip\r\n")
        self.session.send_cmd("no redistribute static\r\n")
        print("The static routes have been removed from RIP process")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def remove_redistribute_all(self):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router rip\r\n")
        self.session.send_cmd("no redistribute all\r\n")
        print("All routes have been removed RIP process")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def remove_redistribute_ospf(self):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router rip\r\n")
        self.session.send_cmd("no redistribute ospf\r\n")
        print("OSPF routes have been removed from RIP process")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def default_metric(self, metric):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router rip\r\n")
        self.session.send_cmd(f"default-metric {metric}\r\n")
        print(f"Default metric {metric} has been configured")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def remove_default_metric(self):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router rip\r\n")
        self.session.send_cmd(f"no default-metric\r\n")
        print(f"Default metric has been removed")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def add_distance(self, distance):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router rip\r\n")
        self.session.send_cmd(f"distance {distance}\r\n")
        print(f"AD {distance} has been added")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def remove_distance(self):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router rip\r\n")
        self.session.send_cmd(f"no distance\r\n")
        print(f"The configured AD has been removed")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def auto_summary(self):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router rip\r\n")
        self.session.send_cmd(f"auto-summary enable\r\n")
        print(f"The auto-summary has been added")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def remove_auto_summary(self):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router rip\r\n")
        self.session.send_cmd(f"auto-summary disable\r\n")
        print(f"The auto-summary has been removed")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def show_rip_database(self):

        self.session.connect()
        self.session.send_cmd("show ip rip database\r\n")
        output = self.session.read()
        print(output)

        match_total_count = re.findall(r"Total Count :\s+(\d+)", output)
        match_auto_summary = re.findall(r"(\d+.\d+.\d+.\d+)/(\d+)\s+\S(\d+)\S\s+(auto-summary)", output)
        match_directly_connected = re.findall(r"(\d+.\d+.\d+.\d+)/(\d+)\s+\S(\d+)\S\s+(directly connected)\S+\s+([vlanGimgt]+)([/\d]+)", output)
        match_via = re.findall(r"(\d+.\d+.\d+.\d+)/(\d+)\s+\S(\d+)\S\s+via\s+(\d+.\d+.\d+.\d+)\S+\s+([vlanGimgt]+)([/\d]+)", output)

        print(match_total_count)
        print(match_auto_summary)
        print(match_directly_connected)
        print(match_via)


obj_rip = RIP(ip_session="10.2.109.88")
# obj_rip.disable_rip()
# obj_rip.enable_rip()
# obj_rip.advertise_network(ip_network="14.0.0.2")
# obj_rip.advertise_network(ip_network="4.0.0.1")
# obj_rip.remove_network(ip_network="4.0.0.1")
# obj_rip.add_passive_interface(vlan="30")
# obj_rip.add_passive_interface(interface="gi 0/3")
# obj_rip.remove_passive_interface(vlan="30")
# obj_rip.remove_passive_interface(interface="gi 0/3")
# obj_rip.redistribute_all()
# obj_rip.redistribute_static()
# obj_rip.redistribute_connected()
# obj_rip.redistribute_ospf()
# obj_rip.remove_redistribute_all()
# obj_rip.remove_redistribute_static()
# obj_rip.remove_redistribute_connected()
# obj_rip.remove_redistribute_ospf()
# obj_rip.default_metric(metric="10")
# obj_rip.remove_default_metric()
# obj_rip.add_distance(distance="99")
# obj_rip.remove_distance()
# obj_rip.remove_auto_summary()
# obj_rip.auto_summary()
obj_rip.show_rip_database()
