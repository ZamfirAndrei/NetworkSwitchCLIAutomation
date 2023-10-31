import re
import time

from Management import ssh, telnet


class RIP:

    def __init__(self, ip_session):

        print("Class RIP")

        self.ip_session = ip_session
        self.session = ssh.SSH(ip_session)
        self.tn = telnet.Telnet(ip_session)

    def enable_rip(self):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router rip\r\n")
        print(f"The RIP process has been enabled for DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def disable_rip(self):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("no router rip\r\n")
        print(f"The RIP process has been disabled for DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def advertise_network(self, ip_network=None):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router rip\r\n")
        self.session.send_cmd(f"network {ip_network}\r\n")
        self.session.send_cmd("version 2")
        self.session.send_cmd("exit")
        print(f"The network {ip_network} has been advertise in rip")
        output = self.session.read()
        # print(output)
        self.session.close()

    def advertise_networks(self, *args):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router rip\r\n")
        for ip_network in args:

            self.session.send_cmd(f"network {ip_network}\r\n")
            self.session.send_cmd("version 2")
            print(f"The network {ip_network} has been advertise in rip on DUT {self.ip_session}")
        self.session.send_cmd("exit")
        output = self.session.read()
        # print(output)
        self.session.close()

    def remove_network(self, ip_network=None):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router rip\r\n")
        self.session.send_cmd(f"no network {ip_network}\r\n")
        self.session.send_cmd("exit")
        print(f"The network {ip_network} has been removed from rip process on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def remove_networks(self, *args):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router rip\r\n")
        for ip_network in args:
            self.session.send_cmd(f"no network {ip_network}\r\n")
            print(f"The network {ip_network} has been removed from rip process")
        self.session.send_cmd("exit")
        output = self.session.read()
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
        self.session.send_cmd("exit")
        print(f"The passive-interface has been created on vlan {vlan} on DUT {self.ip_session}")
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
        self.session.send_cmd("exit")
        print(f"The passive-interface {vlan} has been removed from DUT {self.ip_session}")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def redistribute_connected(self):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router rip\r\n")
        self.session.send_cmd("redistribute connected\r\n")
        self.session.send_cmd("exit")
        print(f"The connected networks have been redistributed into RIP process on DUT {self.ip_session}")
        # time.sleep(2)
        # output = self.session.read()
        # print(output)
        self.session.close()

    def redistribute_static(self):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router rip\r\n")
        self.session.send_cmd("redistribute static\r\n")
        self.session.send_cmd("exit")
        print(f"The static routes have been redistributed into RIP process on DUT {self.ip_session}")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def redistribute_all(self):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router rip\r\n")
        self.session.send_cmd("redistribute all\r\n")
        self.session.send_cmd("exit")
        print(f"All routes have been redistributed into RIP process on DUT {self.ip_session}")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def redistribute_ospf(self):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router rip\r\n")
        self.session.send_cmd("redistribute ospf\r\n")
        self.session.send_cmd("exit")
        print(f"OSPF routes have been redistributed into RIP process on DUT {self.ip_session}")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def remove_redistribute_connected(self):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router rip\r\n")
        self.session.send_cmd("no redistribute connected\r\n")
        self.session.send_cmd("exit")
        print(f"The connected networks have been removed from RIP process on DUT {self.ip_session}")
        # time.sleep(2)
        # output = self.session.read()
        # print(output)
        # self.session.close()
        self.session.close()

    def remove_redistribute_static(self):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router rip\r\n")
        self.session.send_cmd("no redistribute static\r\n")
        self.session.send_cmd("exit")
        print(f"The static routes have been removed from RIP process on DUT {self.ip_session}")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def remove_redistribute_all(self):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router rip\r\n")
        self.session.send_cmd("no redistribute all\r\n")
        self.session.send_cmd("exit")
        print(f"All routes have been removed from RIP process on DUT {self.ip_session}")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def remove_redistribute_ospf(self):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router rip\r\n")
        self.session.send_cmd("no redistribute ospf\r\n")
        self.session.send_cmd("exit")
        print(f"OSPF routes have been removed from RIP process on DUT {self.ip_session}")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def default_metric(self, metric):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router rip\r\n")
        self.session.send_cmd(f"default-metric {metric}\r\n")
        self.session.send_cmd("exit")
        print(f"Default metric {metric} has been configured on DUT {self.ip_session}")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def remove_default_metric(self):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router rip\r\n")
        self.session.send_cmd(f"no default-metric\r\n")
        self.session.send_cmd("exit")
        print(f"Default metric has been removed on DUT {self.ip_session}")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def add_distance(self, distance):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router rip\r\n")
        self.session.send_cmd(f"distance {distance}\r\n")
        self.session.send_cmd("exit")
        print(f"AD {distance} has been added")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def remove_distance(self):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router rip\r\n")
        self.session.send_cmd(f"no distance\r\n")
        self.session.send_cmd("exit")
        print(f"The configured AD has been removed")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def auto_summary(self):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router rip\r\n")
        self.session.send_cmd(f"auto-summary enable\r\n")
        self.session.send_cmd("exit")
        print(f"The auto-summary has been added")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def remove_auto_summary(self):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("router rip\r\n")
        self.session.send_cmd(f"auto-summary disable\r\n")
        self.session.send_cmd("exit")
        print(f"The auto-summary has been removed on dut {self.ip_session}")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def add_default_information_originate(self, int_vlan=None, interface=None, metric="1"):

        self.session.connect()
        self.session.send_cmd("conf t")
        if int_vlan is not None:

            self.session.send_cmd(f"int vlan {int_vlan}")
            self.session.send_cmd(f"default-information originate {metric}")
            print(f"The default-information originate has been advertise on the interface vlan {int_vlan}")

        elif interface is not None:

            self.session.send_cmd(f"int {interface}")
            self.session.send_cmd(f"default-information originate {metric}")
            print(f"The default-information originate has been advertise on the interface {interface}")

        else:

            print("You have to specify an int_vlan/interface")
        self.session.send_cmd("exit")
        output = self.session.read()
        # print(output)
        self.session.close()

        return output

    def remove_default_information_originate(self, int_vlan=None, interface=None):

        self.session.connect()
        self.session.send_cmd("conf t")
        if int_vlan is not None:

            self.session.send_cmd(f"int vlan {int_vlan}")
            self.session.send_cmd(f"no default-information originate")
            print(f"The default-information originate has been removed on the interface vlan {int_vlan}")

        elif interface is not None:

            self.session.send_cmd(f"int {interface}")
            self.session.send_cmd(f"no default-information originate")
            print(f"The default-information originate has been removed on the interface {interface}")

        else:

            print("You have to specify an int_vlan/interface")
        self.session.send_cmd("exit")
        output = self.session.read()
        # print(output)
        self.session.close()

        return output

    def add_ip_default_route_install(self, int_vlan=None, interface=None):

        self.session.connect()
        self.session.send_cmd("conf t")
        if int_vlan is not None:

            self.session.send_cmd(f"int vlan {int_vlan}")
            self.session.send_cmd(f"ip rip default route install")
            print(f"The ip rip default route install has been activated on the interface vlan {int_vlan}")

        elif interface is not None:

            self.session.send_cmd(f"int {interface}")
            self.session.send_cmd(f"ip rip default route install")
            print(f"The ip rip default route install has been activated on the interface {interface}")

        else:

            print("You have to specify an int_vlan/interface")
        self.session.send_cmd("exit")
        output = self.session.read()
        # print(output)
        self.session.close()

        return output

    def remove_ip_default_route_install(self, int_vlan=None, interface=None):

        self.session.connect()
        self.session.send_cmd("conf t")
        if int_vlan is not None:

            self.session.send_cmd(f"int vlan {int_vlan}")
            self.session.send_cmd(f"no ip rip default route install")
            print(f"The ip rip default route install has been deactivated on the interface vlan {int_vlan}")

        elif interface is not None:

            self.session.send_cmd(f"int {interface}")
            self.session.send_cmd(f"no ip rip default route install")
            print(f"The ip rip default route install has been deactivated on the interface {interface}")

        else:

            print("You have to specify an int_vlan/interface")
        self.session.send_cmd("exit")
        output = self.session.read()
        # print(output)
        self.session.close()

        return output

    def add_ip_rip_auth_type_mode(self, int_vlan, mode=None, key_chain=None, key_id=None, key=None):

        self.session.connect()
        self.session.send_cmd(cmd="conf t")
        self.session.send_cmd(cmd=f"int vlan {int_vlan}")
        self.session.send_cmd(cmd=f"ip rip auth-type {mode}")

        if key_chain is not None:
            self.session.send_cmd(cmd=f"ip rip authentication key-chain {key_chain}")
            print(f"The mode {mode} and key-chain {key_chain} have been configured on int_vlan {int_vlan} on DUT {self.ip_session}")

        if key_id is not None:
            if key is not None:
                self.session.send_cmd(cmd=f"ip rip authentication key-id {key_id} key {key}")
                print(f"The mode {mode}, key_id {key_id} and key {key} have been configured on int_vlan {int_vlan} on DUT {self.ip_session}")
        self.session.send_cmd("exit")
        output = self.session.read()
        # print(output)

        self.session.close()

    def remove_ip_rip_authentication_mode(self, int_vlan):

        self.session.connect()
        self.session.send_cmd(cmd="conf t")
        self.session.send_cmd(cmd=f"int vlan {int_vlan}")
        self.session.send_cmd(cmd=f"no ip rip authentication")
        self.session.send_cmd("exit")
        print(f"The RIP authentication have been removed from int_vlan {int_vlan} on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)

        self.session.close()

    def add_ip_rip_authentication_mode(self, int_vlan, mode=None, key_chain=None, key_id=None):

        self.session.connect()
        self.session.send_cmd(cmd="conf t")
        self.session.send_cmd(cmd=f"int vlan {int_vlan}")
        self.session.send_cmd(cmd=f"ip rip authentication mode {mode}")

        if key_chain is not None:
            self.session.send_cmd(cmd=f"ip rip authentication key-chain {key_chain}")
            print(f"The mode {mode} and key-chain {key_chain} have been configured on int_vlan {int_vlan} on DUT {self.ip_session}")
        self.session.send_cmd("exit")
        output = self.session.read()
        # print(output)

        self.session.close()

    def remove_ip_rip_authentication_key(self, int_vlan, key_id):

        self.session.connect()
        self.session.send_cmd(cmd="conf t")
        self.session.send_cmd(cmd=f"int vlan {int_vlan}")
        self.session.send_cmd(cmd=f"no ip rip authentication key-id {key_id}")
        self.session.send_cmd("exit")
        print(f"The RIP authentication key-id {key_id} have been removed from int_vlan {int_vlan} on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)

        self.session.close()

    def configure_rip_timers(self, int_vlan, update_timer,  routage_timer, garbage_timer):

        self.session.connect()
        self.session.send_cmd(cmd="conf t")
        self.session.send_cmd(cmd=f"int vlan {int_vlan}")
        self.session.send_cmd(cmd=f"timers basic {update_timer} {routage_timer} {garbage_timer}")
        self.session.send_cmd("exit")
        print(f"The timers of int_vlan {int_vlan} have been configured to {update_timer},{routage_timer},{garbage_timer} on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)

        self.session.close()

    def remove_rip_timers(self, int_vlan):

        self.session.connect()
        self.session.send_cmd(cmd="conf t")
        self.session.send_cmd(cmd=f"int vlan {int_vlan}")
        self.session.send_cmd(cmd=f"no timers basic")
        self.session.send_cmd("exit")
        print(f"The timers of int_vlan {int_vlan} have been removed to from DUT {self.ip_session}")
        output = self.session.read()
        # print(output)

        self.session.close()

    def show_ip_rip_authentication(self):

        dict_of_int_vlans = {}
        d = {}

        self.session.connect()
        self.session.send_cmd(cmd="show ip rip authentication")
        self.session.send_cmd("exit")
        output = self.session.read()
        # print(output)

        match1 = re.findall(r'Interface Name\s+vlan(\d+)\S+Authentication type is\s+([\w\s]+)', output)
        match2 = re.findall(r'Authentication KeyId in use:\s+(\d+)\S+Authentication Last key status:\s+(\w+)', output)

        # print(match1)
        # print(match2)

        for item in match1:

            d["Interface Name"] = item[0]
            d["Authentication Type"] = item[1]

            if len(match2) == 0:

                dict_of_int_vlans[item[0]] = d
                d = {}

            else:

                for item2 in match2:

                    d["Authentication KeyId in use"] = item2[0]
                    d["Authentication Last key status"] = item2[1]
                    dict_of_int_vlans[item[0]] = d
                    d = {}

        # print(dict_of_int_vlans)

        self.session.close()

        return  dict_of_int_vlans

    def show_rip_database(self):

        dict_of_via = {}
        dict_of_directly_connected = {}
        dict_of_auto_summary = {}
        list_rip_database = list()
        list_of_auto_summary = list()
        list_of_directly_connected = list()
        list_of_via = list()

        self.session.connect()
        self.session.send_cmd("show ip rip database\r\n")
        self.session.send_cmd("exit")
        output = self.session.read()
        # print(output)

        match_total_count = re.findall(r"Total Count :\s+(\d+)", output)
        match_auto_summary = re.findall(r"(\d+.\d+.\d+.\d+)/(\d+)\s+\S(\d+)\S\s+(auto-summary)", output)
        match_directly_connected = re.findall(r"(\d+.\d+.\d+.\d+)/(\d+)\s+\S(\d+)\S\s+(directly connected)\S+\s+([vlanGimgt]+)([/\d]+)", output)
        match_via = re.findall(r"(\d+.\d+.\d+.\d+)/(\d+)\s+\S(\d+)\S\s+via\s+(\d+.\d+.\d+.\d+)\S+\s+([vlanGimgt]+)([/\d]+)", output)

        # print(match_total_count)
        # print(match_auto_summary)
        # print(match_directly_connected)
        # print(match_via)

        print("#############################")

        d = {}

        for attribute in match_auto_summary:

            d["Network"] = attribute[0]
            d["Mask"] = attribute[1]
            d["Metric"] = attribute[2]
            d["Type"] = attribute[3]
            # print(d)
            list_of_auto_summary.append(d)
            dict_of_auto_summary[attribute[0]] = d
            d = {}

        # print(len(list_of_auto_summary))
        # print(list_of_auto_summary)
        print(dict_of_auto_summary)

        for attribute in match_directly_connected:

            d["Network"] = attribute[0]
            d["Mask"] = attribute[1]
            d["Metric"] = attribute[2]
            d["Type"] = attribute[3]
            d["Interface"] = attribute[4]+attribute[5]
            # print(d)
            list_of_directly_connected.append(d)
            dict_of_directly_connected[attribute[0]] = d
            d = {}

        # print(len(list_of_directly_connected))
        # print(list_of_directly_connected)
        print(dict_of_directly_connected)

        for attribute in match_via:

            d["Network"] = attribute[0]
            d["Mask"] = attribute[1]
            d["Metric"] = attribute[2]
            d["via Network"] = attribute[3]
            d["via Interface"] = attribute[4]+attribute[5]
            # print(d)
            list_of_via.append(d)
            dict_of_via[attribute[0]] = d
            d = {}

        # print(len(list_of_via))
        # print(list_of_via)
        print(dict_of_via)

        self.session.close()

        return match_total_count,  dict_of_auto_summary, dict_of_directly_connected, dict_of_via

    def show_ip_route_rip(self):

        dict_rip_routes = {}

        self.session.connect()
        self.session.send_cmd(cmd="show ip route rip")
        self.session.send_cmd(cmd="exit")
        output = self.session.read()
        # print(output)

        match = re.findall(r"(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})/(\d{1,2})\s+\S(\d{1,3})/(\d+)\S\s+via\s+(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})", output)
        # print(match)

        for item in match:

            dict_rip_route = {}

            dict_rip_route["Network"] = item[0]
            dict_rip_route["Mask"] = item[1]
            dict_rip_route["AD"] = item[2]
            dict_rip_route["Metric"] = item[3]
            dict_rip_route["Learned From"] = item[4]

            # print(dict_rip_route)
            dict_rip_routes[item[0]] = dict_rip_route

        # print(dict_rip_routes)
        self.session.close()

        return dict_rip_routes

    def show_ip_rip_statistics(self):

        dict_rip_statistics = {}

        self.session.connect()
        self.session.send_cmd(cmd="conf t")
        self.session.send_cmd(cmd="set cli pagination off")
        self.session.send_cmd(cmd="do sh ip rip statistics")
        self.session.send_cmd(cmd="exit")
        output = self.session.read()
        # print(output)

        # updates_sent = re.findall(r'Periodic Updates Sent\s+:\s+(\d+)', output)
        # updates_received = re.findall(r'Response Received\s+:\s+(\d+)',output)

        match = re.findall(r'(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})\s+(\d+)', output)

        # print(updates_sent)
        # print(updates_received)
        # print(match)

        d = {}

        for item in match:

            d["Interface VLAN"] = item[0]
            d["Updates Sent"] = item[1]
            dict_rip_statistics[item[0]] = d
            d = {}
        print(dict_rip_statistics)
        self.session.close()

        return dict_rip_statistics


ip_session = "10.2.109.238"

# obj_rip = RIP(ip_session=ip_session)
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
# obj_rip.show_rip_database()
