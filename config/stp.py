import re

from Management import ssh, telnet
from config import ip, vlan


class STP:

    def __init__(self, ip_session="10.2.109.178"):

        print("Clasa STP")

        self.ip_session = ip_session
        self.session = ssh.SSH(ip_session)
        # self.vlan_obj = vlan.VLAN(ip_session)
        # self.ip_obj = ip.IP(ip_session)
        self.tn = telnet.Telnet(ip_session)

    def check_stp_mode(self):

        d = {}
        self.session.connect()
        self.session.send_cmd("show span\r\n")
        output = self.session.read()
        match = re.findall(r"is executing the ([mstpr]+)", output)
        print(output)
        print(match)
        match1 = re.findall(r"Spanning Tree Enabled Protocol ([PVRST]+)", output)
        print(match1)
        if len(match) > 0:
            d["mode"] = match[0]
        else:
            d["mode"] = match1[0]

        print(d)

        return d

    def changing_stp_mode(self, mode=None):

        self.session.connect()
        self.session.send_cmd("conf t \r\n")
        self.session.send_cmd(f"spanning-tree mode {mode}\r\n")
        print(f"The mode of the DUT {self.ip_session} has been changed to {mode}")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def add_rstp_bridge_priority(self, bridge_priority=None):

        if bridge_priority is not None:

            self.session.connect()
            self.session.send_cmd("conf t\r\n")
            self.session.send_cmd(f"spanning-tree priority {bridge_priority}\r\n")
            print(f"The bridge priority of the switch {self.ip_session} was changed to {bridge_priority}")

        else:

            print(f"The bridge priority of the swtich {self.ip_session} remains the same ")
        # output = self.session.read()
        # print(output)

        self.session.close()

    def remove_rstp_bridge_priority(self):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"no spanning-tree priority \r\n")
        print(f"The bridge priority of the switch {self.ip_session} was changed to default")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def add_rstp_port_cost(self, port=None, cost=None):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"spanning-tree cost {cost}\r\n")
        self.session.send_cmd("!")
        print(f"The cost for {port} was changed to {cost}")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def remove_rstp_port_cost(self, port=None):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"no spanning-tree cost\r\n")
        self.session.send_cmd("!")
        print(f"The cost for {port} has been removed")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def add_rstp_port_priority(self, port=None, port_priority=None):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"spanning-tree port-priority {port_priority}\r\n")
        self.session.send_cmd("!")
        print(f"The port-priority for {port} has been changed to {port_priority}")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def remove_rstp_port_priority(self, port=None):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"no spanning-tree port-priority\r\n")
        self.session.send_cmd("!")
        print(f"The port-priority for {port} has been removed")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def show_spanning_tree_rstp(self):

        d_root_id = {}
        d_bridge_id = {}
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
        self.session.send_cmd("show span\r\n")
        output = self.session.read()
        print(output)

        match = re.findall(r"\s+Priority\s+(\d+)\S+\s+Address\s+(\w+.\w+.\w+.\w+.\w+.\w+)", output) # Regex pentru Root ID si Bridge ID
        match1 = re.findall(r"([GExi\d/]+)\s+(\w+)\s+(\w+)\s+(\d+)\s+(\d+)\s+([\w\d]+)", output) # Regex pentru porturi

        print(match)
        print(match1)

        print("###################")

        d_root_id["Root Priority"] = match[0][0]
        d_root_id["Root MAC-Address"] = match[0][1]

        d_bridge_id["Bridge Priority"] = match[1][0]
        d_bridge_id["Bridge MAC-Address"] = match[1][1]

        print(d_root_id)
        print(d_bridge_id)

        print("###################")

        for attributes in match1:
            # print(attributes)
            d2 = {}
            for key, attribute in zip(d1.keys(), attributes):
                # print(key,attribute)
                d2[key] = attribute
            ports.append(d2)
        print(ports)
        self.session.close()

        return d_root_id, d_bridge_id, ports

    def add_pvrst_bridge_priority(self, vlan=None, brg_priority=None):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"spanning-tree vlan {vlan} brg-priority {brg_priority}\r\n")
        print(f"The brg-priority for vlan {vlan} has been changed in {brg_priority}")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def remove_pvrst_bridge_priority(self, vlan=None):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"no spanning-tree vlan {vlan} brg-priority\r\n")
        print(f"The brg-priority for vlan {vlan} has been changed to default")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def add_pvrst_port_cost(self, vlan=None, port=None, cost=None):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"spanning-tree vlan {vlan} cost {cost}\r\n")
        self.session.send_cmd("!")
        print(f"The cost for {port} was changed to {cost}")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def remove_pvrst_port_cost(self, vlan=None, port=None):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"no spanning-tree vlan {vlan} cost\r\n")
        self.session.send_cmd("!")
        print(f"The cost for {port} has been removed")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def add_pvrst_port_priority(self, vlan=None, port=None, port_priority=None):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"spanning-tree vlan {vlan} port-priority {port_priority}\r\n")
        self.session.send_cmd("!")
        print(f"The port-priority for {port} has been changed")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def remove_pvrst_port_priority(self, vlan=None, port=None):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"no spanning-tree vlan {vlan} port-priority\r\n")
        self.session.send_cmd("!")
        print(f"The port-priority for {port} has been changed to default")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def mst_configuration(self, name=None, instance=None, vlan=None):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd("spanning-tree mst configuration\r\n")

        if name is not None:

            self.session.send_cmd(f"name {name}\r\n")

        if instance is not None and vlan is not None:

            self.session.send_cmd(f"instance {instance} vlan {vlan}\r\n")

        print("The mst configuration has been made")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def add_mst_priority(self, instance=None, priority=None):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"spanning-tree mst {instance} priority {priority}\r\n")
        print(f"The priority for instance {instance} has been changed in {priority}")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def remove_mst_priority(self, instance=None):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"no spanning-tree mst {instance} priority\r\n")
        print(f"The priority for instance {instance} has been changed to default")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def add_mst_port_cost(self, instance=None, port=None, cost=None):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"spanning-tree mst {instance} cost {cost}\r\n")
        self.session.send_cmd("!")
        print(f"The cost for {port} was changed to {cost}")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def remove_mst_port_cost(self, instance=None, port=None):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"no spanning-tree mst {instance} cost\r\n")
        self.session.send_cmd("!")
        print(f"The cost for {port} has been removed")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def add_mst_port_priority(self, instance=None, port=None, port_priority=None):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"spanning-tree mst {instance} port-priority {port_priority}\r\n")
        self.session.send_cmd("!")
        print(f"The port-priority for {port} has been changed")
        # output = self.session.read()
        # print(output)
        self.session.close()

    def remove_mst_port_priority(self, instance=None, port=None):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"no spanning-tree mst {instance} port-priority\r\n")
        self.session.send_cmd("!")
        print(f"The port-priority for {port} has been changed to default")
        # output = self.session.read()
        # print(output)
        self.session.close()


obj = STP("10.2.109.178")
# obj.add_rstp_bridge_priority(bridge_priority=0)
# obj.remove_rstp_bridge_priority()
# obj.add_rstp_port_cost(port="Gi 0/3", cost="4")
# obj.remove_rstp_port_cost(port="Gi 0/3")
# obj.add_rstp_port_priority(port="Ex 0/1", port_priority= "64")
# obj.show_spanning_tree_rstp()
# obj.remove_rstp_port_priority(port="Ex 0/1")
# obj.changing_stp_mode(mode="rst")
#
# obj1 = STP("10.2.109.198")
# # obj1.add_rstp_bridge_priority(bridge_priority="61440")
# # obj1.show_spanning_tree_rstp()
# print("###########################")
# obj1.changing_stp_mode(mode="rst")
# obj1.check_stp_mode()
# obj.add_pvrst_bridge_priority(vlan="10",brg_priority="4096")
# obj.remove_pvrst_bridge_priority(vlan="10")
# obj.add_pvrst_port_priority(vlan="10",port="Ex 0/2",port_priority="16")
# obj.remove_pvrst_port_priority(vlan="10",port="Ex 0/2")
# obj.add_pvrst_port_cost(vlan="10",port="Ex 0/1",cost="1")
# obj.remove_pvrst_port_cost(vlan="10",port="Ex 0/1")
# obj.changing_stp_mode(mode="mst")
# obj.mst_configuration(name="TETE",instance="1",vlan="10,100")
# obj.add_mst_priority(instance="1",priority="4096")
# obj.remove_mst_priority(instance="1")
# obj.add_mst_port_cost(instance="1",port="Ex 0/1",cost="2")
# obj.remove_mst_port_cost(instance="1",port="Ex 0/1")
# obj.add_mst_port_priority(instance="1",port="Ex 0/2",port_priority="0")
# obj.remove_mst_port_priority(instance="1", port="Ex 0/1")