import re

from Management import ssh, telnet
from config import ip, vlan


class STP:

    def __init__(self, ip_session="10.2.109.178"):

        print("Class STP")

        self.ip_session = ip_session
        self.session = ssh.SSH(ip_session)
        # self.vlan_obj = vlan.VLAN(ip_session)
        # self.ip_obj = ip.IP(ip_session)
        # self.tn = telnet.Telnet(ip_session)

    def check_stp_mode(self):

        d = {}
        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("set cli pagination off")
        self.session.send_cmd("do show span")

        output = self.session.read()
        match = re.findall(r"is executing the ([mstpr]+)", output)
        # print(output)
        # print(match)
        match1 = re.findall(r"Spanning Tree Enabled Protocol ([PVRST]+)", output)
        # print(match1)
        if len(match) > 0:
            d["mode"] = match[0]
        else:
            d["mode"] = match1[0]

        # print(d)

        return d

    def change_stp_mode(self, mode=None):

        self.session.connect()
        self.session.send_cmd("conf t ")
        self.session.send_cmd(f"spanning-tree mode {mode}")
        print(f"The mode of the DUT {self.ip_session} has been changed to {mode}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def stp_enable(self, port):

        self.session.connect()
        self.session.send_cmd("conf t ")
        self.session.send_cmd(f"int {port}")
        self.session.send_cmd(f"spanning-tree enable")
        print(f"The spanning-tree was enabled on the port {port} on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def stp_disable(self, port):

        self.session.connect()
        self.session.send_cmd("conf t ")
        self.session.send_cmd(f"int {port}")
        self.session.send_cmd(f"spanning-tree disable")
        print(f"The spanning-tree was disabled on the port {port} on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def add_rstp_bpdu_receive(self, port, mode):

        self.session.connect()
        self.session.send_cmd("conf t ")
        self.session.send_cmd(f"int {port}")
        self.session.send_cmd(f"spanning-tree bpdu-receive {mode}")
        print(f"The spanning-tree bpdu-receive was {mode} on the port {port} on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def add_rstp_bpdu_transmit(self, port, mode):

        self.session.connect()
        self.session.send_cmd("conf t ")
        self.session.send_cmd(f"int {port}")
        self.session.send_cmd(f"spanning-tree bpdu-transmit {mode}")
        print(f"The spanning-tree bpdu-transmit was {mode} on the port {port} on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def add_rstp_bpdu_filter(self, port, mode):

        self.session.connect()
        self.session.send_cmd("conf t ")
        self.session.send_cmd(f"int {port}")
        self.session.send_cmd(f"spanning-tree bpdufilter {mode}")
        print(f"The spanning-tree bpdufilter was {mode} on the port {port} on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def show_run_stp_bpdu_filter(self, interface):

        self.session.connect()
        self.session.send_cmd(f"show run int {interface}")
        output = self.session.read()
        # print(output)
        bpdu_receive_match = re.findall("spanning-tree bpdu-receive ([enabldis]+)", output)
        bpdu_transmit_match = re.findall("spanning-tree bpdu-transmit ([enabldis]+)", output)

        # print(bpdu_receive_match, bpdu_transmit_match)
        self.session.close()
        # print(len(bpdu_receive_match),len(bpdu_transmit_match))

        if len(bpdu_receive_match) > 0 and len(bpdu_transmit_match) > 0:
            return bpdu_receive_match[0], bpdu_transmit_match[0]

        elif len(bpdu_receive_match) == 0 and len(bpdu_transmit_match) > 0:
            return "No bpdu-receive match", bpdu_transmit_match[0]

        elif len(bpdu_receive_match) > 0 and len(bpdu_transmit_match) == 0:
            return bpdu_receive_match[0], "No bpdu-transmit match"

        else:
            return "No bpdu-receive match", "No bpdu-transmit match"



    def show_spanning_tree_root(self):

        self.session.connect()
        self.session.send_cmd("show spanning-tree root address")
        output = self.session.read()
        # print(output)
        root = re.findall(r"\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2}", output)
        # print(root)
        self.session.close()

        return root

    def add_rstp_bridge_priority(self, bridge_priority=None):

        if bridge_priority is not None:

            self.session.connect()
            self.session.send_cmd("conf t")
            self.session.send_cmd(f"spanning-tree priority {bridge_priority}")
            print(f"The bridge priority of the switch {self.ip_session} was changed to {bridge_priority}")

        else:

            print(f"The bridge priority of the switch {self.ip_session} remains the same ")
        output = self.session.read()
        # print(output)

        self.session.close()

    def remove_rstp_bridge_priority(self):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"no spanning-tree priority")
        print(f"The bridge priority of the switch {self.ip_session} was changed to default")
        output = self.session.read()
        # print(output)
        self.session.close()

    def add_rstp_port_cost(self, port=None, cost=None):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"int {port}")
        self.session.send_cmd(f"spanning-tree cost {cost}")
        self.session.send_cmd("!")
        print(f"The cost for {port} was changed to {cost} on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def remove_rstp_port_cost(self, port=None):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"int {port}")
        self.session.send_cmd(f"no spanning-tree cost")
        self.session.send_cmd("!")
        print(f"The cost for {port} has been removed from DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def add_rstp_port_priority(self, port=None, port_priority=None):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"int {port}")
        self.session.send_cmd(f"spanning-tree port-priority {port_priority}")
        self.session.send_cmd("!")
        print(f"The port-priority for {port} has been changed to {port_priority} on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def remove_rstp_port_priority(self, port=None):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"int {port}")
        self.session.send_cmd(f"no spanning-tree port-priority")
        self.session.send_cmd("!")
        print(f"The port-priority for {port} has been removed from DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def show_spanning_tree_rstp(self):

        d_root_id = {}
        d_bridge_id = {}
        dict_of_ports = {}
        d1 = {
            "Name":"",
            "Role":"",
            "State":"",
            "Cost":"",
            "Prio":"",
            "Type":""
        }
        ports = list()

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("set cli pagination off")
        self.session.send_cmd("do show span")
        output = self.session.read()
        # print(output)

        match = re.findall(r"\s+Priority\s+(\d+)\S+\s+Address\s+(\w+.\w+.\w+.\w+.\w+.\w+)", output) # Regex pentru Root ID si Bridge ID
        match1 = re.findall(r"([GEix]+\d/\d+)\s+(\w+)\s+(\w+)\s+(\d+)\s+(\d+)\s+([\w\d]+)", output) # Regex pentru porturi

        # print(match)
        # print(match1)

        # print("###################")

        d_root_id["Root Priority"] = match[0][0]
        d_root_id["Root MAC-Address"] = match[0][1]

        d_bridge_id["Bridge Priority"] = match[1][0]
        d_bridge_id["Bridge MAC-Address"] = match[1][1]

        # print(d_root_id)
        # print(d_bridge_id)

        # print("###################")

        for attributes in match1:
            # print(attributes)
            d2 = {}
            for key, attribute in zip(d1.keys(), attributes):
                # print(key,attribute)
                d2[key] = attribute
            ports.append(d2)
            dict_of_ports[d2["Name"]] = d2
        # print(ports)
        # print(dict_of_ports)
        self.session.close()

        return d_root_id, d_bridge_id, ports, dict_of_ports

    def add_pvrst_bridge_priority(self, vlan=None, brg_priority=None):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"spanning-tree vlan {vlan} brg-priority {brg_priority}")
        print(f"The brg-priority for vlan {vlan} has been changed in {brg_priority} on DUT {self.ip_session}")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def remove_pvrst_bridge_priority(self, vlan=None):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"no spanning-tree vlan {vlan} brg-priority")
        print(f"The brg-priority for vlan {vlan} has been changed to default on DUT {self.ip_session}")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def add_pvrst_port_cost(self, vlan=None, port=None, cost=None):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"int {port}")
        self.session.send_cmd(f"spanning-tree vlan {vlan} cost {cost}")
        self.session.send_cmd("!")
        print(f"The cost for {port} was changed to {cost} on DUT {self.ip_session}")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def remove_pvrst_port_cost(self, vlan=None, port=None):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"no spanning-tree vlan {vlan} cost\r\n")
        self.session.send_cmd("!")
        print(f"The cost for {port} has been removed from DUT {self.ip_session}")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def add_pvrst_port_priority(self, vlan=None, port=None, port_priority=None):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"int {port}")
        self.session.send_cmd(f"spanning-tree vlan {vlan} port-priority {port_priority}")
        self.session.send_cmd("!")
        print(f"The port-priority for {port} has been changed on DUT {self.ip_session}")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def remove_pvrst_port_priority(self, vlan=None, port=None):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"int {port}")
        self.session.send_cmd(f"no spanning-tree vlan {vlan} port-priority")
        self.session.send_cmd("!")
        print(f"The port-priority for {port} has been changed to default on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def add_prvst_root_primary_secondary(self, vlan, root):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"spanning-tree vlan {vlan} root {root}")
        print(f"The root {root} for vlan {vlan} has been configured on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def remove_pvrst_root_primary_secondary(self, vlan):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"no spanning-tree vlan {vlan} root")
        print(f"The priority for vlan {vlan} has been changed to default")
        output = self.session.read()
        # print(output)
        self.session.close()

    def mst_configuration(self, name=None, instance=None, vlan=None):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("spanning-tree mst configuration")

        if name is not None:

            self.session.send_cmd(f"name {name}\r\n")

        if instance is not None and vlan is not None:

            self.session.send_cmd(f"instance {instance} vlan {vlan}")

        print(f"The mst configuration has been made on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def add_mst_priority(self, instance=None, priority=None):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"spanning-tree mst {instance} priority {priority}")
        print(f"The priority for instance {instance} has been changed in {priority} on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def remove_mst_priority(self, instance=None):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"no spanning-tree mst {instance} priority")
        print(f"The priority for instance {instance} has been changed to default on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def add_mst_port_cost(self, instance=None, port=None, cost=None):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"int {port}")
        self.session.send_cmd(f"spanning-tree mst {instance} cost {cost}")
        self.session.send_cmd("!")
        print(f"The cost for {port} on instance {instance} was changed to {cost}")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def remove_mst_port_cost(self, instance=None, port=None):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"int {port}")
        self.session.send_cmd(f"no spanning-tree mst {instance} cost")
        self.session.send_cmd("!")
        print(f"The cost for {port} on instance {instance} has been removed on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def add_mst_port_priority(self, instance=None, port=None, port_priority=None):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"int {port}")
        self.session.send_cmd(f"spanning-tree mst {instance} port-priority {port_priority}")
        self.session.send_cmd("!")
        print(f"The port-priority for {port} on instance {instance} has been changed on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def remove_mst_port_priority(self, instance=None, port=None):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"int {port}")
        self.session.send_cmd(f"no spanning-tree mst {instance} port-priority")
        self.session.send_cmd("!")
        print(f"The port-priority for {port} on instance {instance} has been changed to default on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def add_mst_instance_with_vlans(self, *args, instance):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("spanning-tree mst configuration")

        for vlan in args:
            self.session.send_cmd(f"instance {instance} vlan {vlan}")
            print(f"The vlan {vlan} has been added to instance {instance} for DUT {self.ip_session}")

        self.session.send_cmd("!")
        output = self.session.read()
        # print(output)
        self.session.close()

    def add_mst_instances_with_vlans(self, *args, **kwargs):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("spanning-tree mst configuration")

        for instance, vlan in zip(args, kwargs.values()):
            self.session.send_cmd(f"instance {instance} vlan {vlan[0]}")
            print(f"The vlan {vlan[0]} has been added to instance {instance} for DUT {self.ip_session}")

        self.session.send_cmd("!")
        output = self.session.read()
        # print(output)
        self.session.close()

    def remove_mst_instance(self, instance):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("spanning-tree mst configuration")

        self.session.send_cmd(f"no instance {instance}")
        print(f"The instance {instance} has been removed from DUT {self.ip_session}")

        self.session.send_cmd("!")
        output = self.session.read()
        # print(output)
        self.session.close()

    def remove_mst_instances(self, *args):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("spanning-tree mst configuration")

        for instance in args:
            self.session.send_cmd(f"no instance {instance}")
            print(f"The instance {instance} has been removed from DUT {self.ip_session}")

        self.session.send_cmd("!")
        output = self.session.read()
        # print(output)
        self.session.close()

    def add_mst_region(self, region):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("spanning-tree mst configuration")
        self.session.send_cmd(f"name {region}")
        self.session.send_cmd("!")
        print(f"The region {region} has been added for DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def add_mst_root_primary_secondary(self, instance, root):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"spanning-tree mst instance-id {instance} root {root}")
        print(f"The root {root} for instance {instance} has been configured on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def remove_mst_root_primary_secondary(self, instance):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"no spanning-tree mst instance-id {instance} root")
        print(f"The priority for instance {instance} has been changed to default")
        output = self.session.read()
        # print(output)
        self.session.close()

    def show_spanning_tree_mst(self, instance=None):

        d_instance_zero = {
            "Instance": "",
            "Bridge MAC-Address": "",
            "Root MAC-Address": "",
            "IST root Address":"",
            "Priority": "",
        }
        d_ports_instance_zero = {
            "Name": "",
            "Role": "",
            "State": "",
            "Cost": "",
            "Prio": "",
            "Type": ""
        }

        d_instance = {
            "Instance":"",
            "VLANs Mapped":"",
            "Bridge ID Address":"",
            "Bridge ID Priority":"",
            "Root ID Address":"",
            "Root ID Priority":"",
        }

        d_ports_instances = {
            "Name": "",
            "Role": "",
            "State": "",
            "Cost": "",
            "Prio": "",
            "Type": ""
        }

        dict_of_ports_instance = {}

        list_ports_instance_zero = list()
        list_ports_instance = list()

        self.session.connect()

        if instance is None:

            self.session.send_cmd("show span mst\r\n")
            output = self.session.read()
            # print(output)

            match1 = re.findall(r"(MST\d+)\s+\S+Bridge\s+Address\s+(\w+.\w+.\w+.\w+.\w+.\w+)\s+Priority\s(\d+)\S+"
                                r"Root\s+Address\s+(\w+.\w+.\w+.\w+.\w+.\w+)\s+Priority\s+(\d+)\S+"
                                r".*IST\s+Root\s+Address\s+(\w+.\w+.\w+.\w+.\w+.\w+)\s+Priority\s+(\d+)", output)

            match2 = re.findall(r"([GEix]+\d/\d+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\d+)\S\d+\s+([\d\w]+)", output)
            match2 = list(set(match2))

            # print(match1) # Regex pt. MST00 root,brigde (mac-addresses and priorities)
            # print(match2) # Regex pt. MST00 ports

            # Trb sa gasesc o cale sa elimin porturile pe care le ia de la MST01 cand sunt mai putin de 4 porturi in MST00

            for key, attribute in zip(d_instance_zero.keys(), match1[0]):
                # print(key, attribute)
                d_instance_zero[key] = attribute

            # print(d_instance_zero)

            for i in range(len(match2)):

                d = {}

                for key, attribute in zip(d_ports_instance_zero.keys(), match2[i]):

                    # print(key, attribute)
                    d[key] = attribute

                # print(d)
                list_ports_instance_zero.append(d)
            # print(list_ports_instance_zero)
            # print(list_ports_instance_zero[0]["Name"])

        else:

            self.session.send_cmd(f"show span mst {instance}\r\n")
            output = self.session.read()
            # print(output)

            match1 = re.findall(r"(MST\d+)\s+\S+Vlans mapped:\s+([\d,-]+)\S+Bridge\s+Address\s+(\w+.\w+.\w+.\w+.\w+.\w+)\s+Priority\s(\d+)\S+"
                                r"Root\s+Address\s+(\w+.\w+.\w+.\w+.\w+.\w+)\s+Priority\s+(\d+)", output)

            match2 = re.findall(r"([GEix]+\d/\d+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\d+)\S\d+\s+([\d\w]+)", output)
            match2 = list(set(match2))

            # print(match1)  # Regex pt. MST root,brigde (mac-addresses and priorities)
            # print(match2)  # Regex pt. MST ports

            for key, attribute in zip(d_instance.keys(), match1[0]):

                d_instance[key] = attribute

            # print(d_instances)

            for i in range(len(match2)):

                d = {}

                for key, attribute in zip(d_ports_instances.keys(), match2[i]):

                    d[key] = attribute

                list_ports_instance.append(d)
                dict_of_ports_instance[d["Name"]] = d

            # print(list_ports_instance)
            # print(dict_of_ports_instance)

        return d_instance_zero, d_instance, dict_of_ports_instance

    def show_spanning_tree_pvrst(self, vlan=None):

        d_instance_vlan = {
            "VLAN": "",
            "Root ID Priority": "",
            "Root ID Address": "",
            "Bridge ID Priority": "",
            "Bridge ID Address": ""
        }

        d_ports_instance_vlan = {
            "Name": "",
            "Role": "",
            "State": "",
            "Cost": "",
            "Prio": "",
            "Type": ""
        }

        dict_ports_instance_vlan = {}
        list_ports_instance = list()

        self.session.connect()
        self.session.send_cmd(f"show span vlan {vlan}\r\n")

        output = self.session.read()
        # print(output)
        output1 = ""

        if "--More" in output:
            self.session.send_cmd("\r\n")
            output += self.session.read()

        # print(output)
        match1 = re.findall(r"Spanning-tree for VLAN\s+(\d+)\s+[\S\s]+Root Id\s+Priority\s+(\d+)\S+\s+"
                            r"Address\s+(\w+.\w+.\w+.\w+.\w+.\w+)[\s\S]+Bridge Id\s+Priority\s+(\d+)\S+"
                            r"\s+Address\s+(\w+.\w+.\w+.\w+.\w+.\w+)", output)

        match2 = re.findall(r"([GEix]+\d/\d+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\d{1,3})\s+([\d\w]+)", output)

        # print(match1)  # Regex for PVRST VL X root,brigde (mac-addresses and priorities)
        # print(match2)  # Regex for PVRST VL X ports

        for key, attribute in zip(d_instance_vlan.keys(), match1[0]):

            d_instance_vlan[key] = attribute

        # print(d_instance_vlan)

        for i in range(len(match2)):

            d = {}

            for key, attribute in zip(d_ports_instance_vlan.keys(), match2[i]):

                d[key] = attribute
            # print(d)

            list_ports_instance.append(d)
            dict_ports_instance_vlan[d["Name"]] = d

        # print(list_ports_instance)
        # print(dict_ports_instance_vlan)

        return d_instance_vlan, dict_ports_instance_vlan, list_ports_instance


ip_session = "10.2.109.238"
# obj = STP(ip_session=ip_session)
# obj.add_rstp_bridge_priority(bridge_priority=0)
# obj.remove_rstp_bridge_priority()
# obj.add_rstp_port_cost(port="Gi 0/3", cost="4")
# obj.remove_rstp_port_cost(port="Gi 0/3")
# obj.add_rstp_port_priority(port="Ex 0/1", port_priority= "64")
# obj.show_spanning_tree_rstp()
# obj.remove_rstp_port_priority(port="Ex 0/1")
# obj.change_stp_mode(mode="rst")
#
# obj1 = STP("10.2.109.198")
# # obj1.add_rstp_bridge_priority(bridge_priority="61440")
# # obj1.show_spanning_tree_rstp()
# print("###########################")
# obj1.change_stp_mode(mode="rst")
# obj1.check_stp_mode()
# obj.add_pvrst_bridge_priority(vlan="10",brg_priority="4096")
# obj.remove_pvrst_bridge_priority(vlan="10")
# obj.add_pvrst_port_priority(vlan="10",port="Ex 0/2",port_priority="16")
# obj.remove_pvrst_port_priority(vlan="10",port="Ex 0/2")
# obj.add_pvrst_port_cost(vlan="10",port="Ex 0/1",cost="1")
# obj.remove_pvrst_port_cost(vlan="10",port="Ex 0/1")
# obj.change_stp_mode(mode="mst")
# obj.mst_configuration(name="TETE1",instance="1",vlan="10,100")
# obj.add_mst_priority(instance="1",priority="4096")
# obj.remove_mst_priority(instance="1")
# obj.add_mst_port_cost(instance="1",port="Ex 0/1",cost="2")
# obj.remove_mst_port_cost(instance="1",port="Ex 0/1")
# obj.add_mst_port_priority(instance="1",port="Ex 0/2",port_priority="0")
# obj.remove_mst_port_priority(instance="1", port="Ex 0/1")
# obj.show_spanning_tree_rstp()
# obj.show_spanning_tree_mst()
# print("############################")
# obj.show_spanning_tree_mst(instance="1")
# obj.show_spanning_tree_pvrst(vlan="10")
