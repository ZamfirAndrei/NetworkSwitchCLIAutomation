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

    def show_ospf_neighbors(self):

        d_ospf_neighbors = {

            "Neighbor-ID": "",
            "Pri": "",
            "State": "",
            "DeadTime": "",
            "Address": "",
            "Interface": "",

        }

        list_ospf_neigbors = list()

        self.session.connect()
        self.session.send_cmd("show ip ospf neighbor\r\n")
        output = self.session.read()
        print(output)

        match = re.findall(r"(\d+.\d+.\d+.\d+)\s+(\d+)\s+(\w+/\w+)\s+(\d+)\s+(\d+.\d+.\d+.\d+)\s+([\w\d]+)", output)
        print(match)

        for attribute in match:

            d = {}

            for key, value in zip(d_ospf_neighbors.keys(), attribute):

                d[key] = value

            list_ospf_neigbors.append(d)
        print(list_ospf_neigbors)

        self.session.close()

        return list_ospf_neigbors

    def show_ospf_database(self, database=None):

        list_ospf_database = list()
        list_ospf_database_router = list()
        list_ospf_database_network = list()
        list_ospf_database_summary = list()
        list_ospf_database_asbr = list()
        list_ospf_database_nssa = list()
        list_ospf_database_external = list()

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("set cli pagination off\r\n")

        if database == "router":

            self.session.send_cmd(f"do show ip ospf database {database}\r\n")
            output = self.session.read()
            # print(output)

            area = re.findall(r"Router Link States\s\SArea\s+(\d+.\d+.\d+.\d+)", output)
            link_state_id = re.findall(r"Link State ID\s+:\s+(\d+.\d+.\d+.\d+)", output)
            adv_router = re.findall(r"Advertising Router\s+:\s+(\d+.\d+.\d+.\d+)", output)

            print(area)
            print(link_state_id)
            print(adv_router)

            d = {}

            for attribute, id, adv in zip(area, link_state_id, adv_router):

                d["Area"] = attribute
                d["Link State ID"] = id
                d["Advertising Router"] = adv

                # print(d)
                list_ospf_database_router.append(d)
                d = {}

            print(list_ospf_database_router)

        elif database == "network":

            self.session.send_cmd(f"do show ip ospf database {database}\r\n")
            output = self.session.read()
            # print(output)

            area = re.findall(r"Network Link States\s\SArea\s+(\d+.\d+.\d+.\d+)", output)
            link_state_id = re.findall(r"Link State ID\s+:\s+(\d+.\d+.\d+.\d+)", output)
            adv_router = re.findall(r"Advertising Router\s+:\s+(\d+.\d+.\d+.\d+)", output)

            print(area)
            print(link_state_id)
            print(adv_router)

            d = {}

            for attribute, id, adv in zip(area, link_state_id, adv_router):

                d["Area"] = attribute
                d["Link State ID"] = id
                d["Advertising Router"] = adv

                # print(d)
                list_ospf_database_network.append(d)
                d = {}

            print(list_ospf_database_network)

        elif database == "summary":

            self.session.send_cmd(f"do show ip ospf database {database}\r\n")
            output = self.session.read()
            # print(output)

            area = re.findall(r"Summary Link States\s\SArea\s+(\d+.\d+.\d+.\d+)", output)
            link_state_id = re.findall(r"Link State ID\s+:\s+(\d+.\d+.\d+.\d+)", output)
            adv_router = re.findall(r"Advertising Router\s+:\s+(\d+.\d+.\d+.\d+)", output)

            print(area)
            print(link_state_id)
            print(adv_router)

            d = {}

            for attribute, id, adv in zip(area, link_state_id, adv_router):

                d["Area"] = attribute
                d["Link State ID"] = id
                d["Advertising Router"] = adv

                # print(d)
                list_ospf_database_summary.append(d)
                d = {}

            print(list_ospf_database_summary)

        elif database == "asbr":

            self.session.send_cmd(f"do show ip ospf database {database}\r\n")
            output = self.session.read()
            # print(output)

            router_id = re.findall(r"Router with ID\s+\S(\d+.\d+.\d+.\d+)", output)
            print(router_id)

            d = {}

            d["Router ID"] = router_id[0]
            # print(d)
            list_ospf_database_asbr.append(d)

            print(list_ospf_database_asbr)

        elif database == "nssa":

            self.session.send_cmd(f"do show ip ospf database {database}\r\n")
            output = self.session.read()
            # print(output)

            area = re.findall(r"NSSA External Link States\s\SArea\s+(\d+.\d+.\d+.\d+)", output)
            link_state_id = re.findall(r"Link State ID\s+:\s+(\d+.\d+.\d+.\d+)", output)
            adv_router = re.findall(r"Advertising Router\s+:\s+(\d+.\d+.\d+.\d+)", output)

            print(area)
            print(link_state_id)
            print(adv_router)

            d = {}

            for attribute, id, adv in zip(area, link_state_id, adv_router):

                d["Area"] = attribute
                d["Link State ID"] = id
                d["Advertising Router"] = adv

                # print(d)
                list_ospf_database_nssa.append(d)
                d = {}

            print(list_ospf_database_nssa)

        elif database == "external":

            self.session.send_cmd(f"do show ip ospf database {database}\r\n")
            output = self.session.read()
            # print(output)


            link_state_id = re.findall(r"Link State ID\s+:\s+(\d+.\d+.\d+.\d+)", output)
            adv_router = re.findall(r"Advertising Router\s+:\s+(\d+.\d+.\d+.\d+)", output)


            print(link_state_id)
            print(adv_router)

            d = {}

            for id, adv in zip(link_state_id, adv_router):

                d["Link State ID"] = id
                d["Advertising Router"] = adv

                # print(d)
                list_ospf_database_external.append(d)
                d = {}

            print(list_ospf_database_external)

        else:

            self.session.send_cmd(f"do show ip ospf database\r\n")
            output = self.session.read()
            # print(output)

        self.session.close()

        return list_ospf_database_router, list_ospf_database_network, list_ospf_database_summary, list_ospf_database_asbr, list_ospf_database_nssa, list_ospf_database_external


ip = "10.2.109.238"

# ospf_obj = OSPF(ip_session=ip)
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
# ospf_obj.show_ospf_neighbors()
# ospf_obj.show_ospf_database(database="summary")