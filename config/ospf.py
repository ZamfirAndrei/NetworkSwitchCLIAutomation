import re
import time

from Management import ssh, telnet


class OSPF:

    def __init__(self, ip_session="10.2.109.178"):

        print("Clasa OSPF")

        self.ip_session = ip_session
        self.session = ssh.SSH(ip_session)
        self.tn = telnet.Telnet(ip_session)

    def enable_ospf(self):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router ospf\r\n")
        print("The OSPF process has been enabled")
        output = self.session.read()
        # print(output)
        self.session.close()

    def disable_ospf(self):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("no router ospf\r\n")
        print("The OSPF process has been disabled")
        output = self.session.read()
        # print(output)
        self.session.close()

    def advertise_network(self, ip_network=None, area=None):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router ospf\r\n")
        self.session.send_cmd(f"network {ip_network} area {area}\r\n")
        print("The network has been advertise in ospf")
        output = self.session.read()
        # print(output)
        self.session.close()

    def remove_network(self, ip_network=None, area=None):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router ospf\r\n")
        self.session.send_cmd(f"no network {ip_network} area {area}\r\n")
        print("The network has been removed from ospf process")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def redistribute_connected(self, metric_type=None):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router ospf\r\n")

        if metric_type is None:
            self.session.send_cmd("redistribute connected\r\n")
        else:
            self.session.send_cmd(f"redistribute connected metric-type {metric_type}\r\n")

        print("The connected networks have been redistributed into ospf process")
        # time.sleep(2)
        # output = self.session.read()
        # print(output)
        # self.session.close()

    def redistribute_static(self, metric_type=None):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router ospf\r\n")

        if metric_type is None:
            self.session.send_cmd("redistribute static\r\n")
        else:
            self.session.send_cmd(f"redistribute static metric-type {metric_type}\r\n")

        print("The static routes have been redistributed into ospf process")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def redistribute_all(self, metric_type=None):
        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router ospf\r\n")

        if metric_type is None:
            self.session.send_cmd("redistribute all\r\n")
        else:
            self.session.send_cmd(f"redistribute all metric-type {metric_type}\r\n")

        print("All routes have been redistributed into ospf process")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def redistribute_rip(self, metric_type=None):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router ospf\r\n")

        if metric_type is None:
            self.session.send_cmd("redistribute rip\r\n")
        else:
            self.session.send_cmd(f"redistribute rip metric-type {metric_type}\r\n")

        print("RIP routes have been redistributed into ospf process")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def remove_redistribute_connected(self):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router ospf\r\n")
        self.session.send_cmd("no redistribute connected\r\n")
        print("The connected networks have been removed from ospf process")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def remove_redistribute_static(self):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router ospf\r\n")
        self.session.send_cmd("no redistribute static\r\n")
        print("The static routes have been removed from ospf process")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def remove_redistribute_all(self):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router ospf\r\n")
        self.session.send_cmd("no redistribute all\r\n")
        print("All routes have been removed from ospf process")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def remove_redistribute_rip(self):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router ospf\r\n")
        self.session.send_cmd("no redistribute rip\r\n")
        print("RIP routes have been removed from ospf process")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def add_router_id(self, router_id):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router ospf\r\n")
        self.session.send_cmd(f"router-id {router_id}\r\n")
        # time.sleep(2)
        print("Router-id has been configured")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def remove_router_id(self):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router ospf\r\n")
        self.session.send_cmd(f"no router-id\r\n")
        print("Router-id has been removed")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def add_nssa_area(self, area):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router ospf\r\n")
        self.session.send_cmd(f"area {area} nssa\r\n")
        print("The nssa area has been created")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def remove_nssa_area(self, area):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router ospf\r\n")
        self.session.send_cmd(f"no area {area} nssa\r\n")
        print("The nssa area has been removed")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def add_passive_interface(self, vlan =None, interface=None):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router ospf\r\n")

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
        self.session.send_cmd("router ospf\r\n")

        if vlan is None:

            self.session.send_cmd(f"no passive-interface {interface}\r\n")

        else:

            self.session.send_cmd(f"no passive-interface vlan {vlan}\r\n")

        print("The passive-interface has been removed")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def redist_config(self, network, network_mask, metric_type=None, metric_value=None, tag =None):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router ospf\r\n")
        self.session.send_cmd(f"redist-config {network} {network_mask} tag {tag}\r\n")
        print(f"The network {network} has been redistributed with the tag {tag}")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def remove_redist_config(self, network, network_mask, metric_type=None, metric_value=None, tag=None):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router ospf\r\n")
        self.session.send_cmd(f"no redist-config {network} {network_mask}\r\n")
        print(f"The network {network} with the tag {tag} has been removed from redistribution")
        # output = self.session.read()
        # print(output)
        self.session.close()


ospf_obj = OSPF(ip_session="10.2.109.178")
# ospf_obj.enable_ospf()
# ospf_obj.disable_ospf()
# ospf_obj.advertise_network(ip_network="4.0.0.1",area="0.0.0.0")
# ospf_obj.advertise_network(ip_network="14.0.0.2",area="0.0.0.1")
# ospf_obj.remove_network(ip_network="30.0.0.1",area="0.0.0.0")
# ospf_obj.redistribute_all()
# ospf_obj.redistribute_connected(metric_type="1")
# ospf_obj.redistribute_rip(metric_type="1")
# ospf_obj.redistribute_static(metric_type="1")
# ospf_obj.remove_redistribute_rip()
# ospf_obj.remove_redistribute_connected()
# ospf_obj.remove_redistribute_static()
# ospf_obj.add_router_id(router_id="1.1.1.1")
# ospf_obj.remove_router_id()
# ospf_obj.remove_passive_interface(vlan="30")
# ospf_obj.add_passive_interface(vlan="30")
# ospf_obj.add_passive_interface(interface="gi 0/3")
# ospf_obj.remove_passive_interface(interface="gi 0/3")
# ospf_obj.remove_nssa_area(area="0.0.0.1")
# ospf_obj.add_nssa_area(area="0.0.0.1")
# ospf_obj.redist_config(network="30.0.0.0",network_mask="255.255.255.0",tag="200")
# ospf_obj.remove_redist_config(network="30.0.0.0",network_mask="255.255.255.0")