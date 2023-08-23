import re
import time

from Management import ssh, telnet


class QinQ:

    def __init__(self, ip_session="10.2.109.178"):

        print("Class QinQ")

        self.ip_session = ip_session
        self.session = ssh.SSH(ip=ip_session)
        # self.tn = telnet.Telnet(ip=ip_session)

    def change_bridge_mode(self, bridge_mode):

        self.session.connect()
        self.session.send_cmd(f"boot default bridge-mode {bridge_mode} --y")
        self.session.close()
        print("The bridge-mode has been changed")
        # time.sleep(100)
        # self.session.connect(username="admin",password="admin")
        # output1 = self.session.read()
        # print(output1)
        # time.sleep(2)
        # self.session.send_cmd("Admin1234!\r\n")
        # time.sleep(2)
        # self.session.send_cmd("Admin1234!\r\n")
        # output = self.session.read()
        # print(output)

    def change_bridge_port_type(self, port, bridge_port_type):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"bridge port-type {bridge_port_type}\r\n")
        self.session.send_cmd("shut\r\n")
        self.session.send_cmd("no shut\r\n")
        print(f"The bridge port-typ has been changed to {bridge_port_type}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def add_cvlan_to_svlan(self, port, cvlan, svlan):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"switchport customer-vlan {cvlan} service-vlan {svlan}\r\n")
        print(f"Added customer vlan {cvlan} to svlan {svlan}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def remove_cvlan_to_svlan(self, port, cvlan):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"no switchport customer-vlan {cvlan} service-vlan\r\n")
        print(f"Removed customer vlan {cvlan} from svlan")
        output = self.session.read()
        # print(output)
        self.session.close()

    def add_default_service_vlan(self, port, svlan):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"switchport service-vlan {svlan}\r\n")
        print(f"Added default svlan {svlan}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def remove_default_service_vlan(self, port):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"no switchport service-vlan\r\n")
        print(f"Removed default svlan")
        output = self.session.read()
        # print(output)
        self.session.close()

    def add_customer_vlan_pvid(self, port, pvid):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"switchport customer-vlan pvid {pvid}\r\n")
        print(f"Added customer vlan pvid {pvid}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def remove_customer_vlan_pvid(self, port):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"switchport customer-vlan pvid disable\r\n")
        print(f"Removed customer vlan pvid")
        output = self.session.read()
        # print(output)
        self.session.close()

    def add_service_vlan_pvid(self, port, svlan, pvid):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"service-vlan {svlan} pvid {pvid}\r\n")
        print(f"Added pvid {pvid} for the service-vlan {svlan} ")
        output = self.session.read()
        # print(output)
        self.session.close()

    def remove_service_vlan_pvid(self, port, svlan):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"service-vlan {svlan} pvid disable\r\n")
        print(f"Removed pvid for service-vlan {svlan}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def add_svlan_prio(self, port, svlan_prio):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"switchport svlan-prio {svlan_prio}\r\n")
        print(f"Added default service-vlan svlan-prio {svlan_prio}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def remove_svlan_prio(self, port):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd("switchport svlan-prio none\r\n")
        print(f"Removed svlan-prio of default service-vlan ")
        output = self.session.read()
        # print(output)
        self.session.close()

    def add_customer_vlan_svlan_prio(self, port, cvlan, svlan_prio):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"switchport customer-vlan {cvlan} svlan-prio {svlan_prio}\r\n")
        print(f"Added svlan-prio {svlan_prio} to the customer-vlan {cvlan}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def remove_customer_vlan_svlan_prio(self, port, cvlan):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"switchport customer-vlan {cvlan} svlan-prio none\r\n")
        print(f"Removed svlan-prio of the customer-vlan {cvlan}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def add_def_user_priority(self, port, svlan, def_user_priority):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"service-vlan {svlan} def-user-priority {def_user_priority}\r\n")
        print(f"Added def-user priority {def_user_priority} for service-vlan {svlan}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def remove_def_user_priority(self, port, svlan, def_user_priority):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"service-vlan {svlan} def-user-priority {def_user_priority}\r\n")
        print(f"Added def-user priority {def_user_priority} for service-vlan {svlan}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def add_egress_ethertype(self, port, ethertype="x88a8"):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"switchport egress ether-type {ethertype}\r\n")
        print(f"Added egress ether-type {ethertype} for {port}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def remove_egress_ethertype(self, port):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"no switchport egress ether-type\r\n")
        print(f"Removed egress ether-type for {port}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def add_ingress_ethertype(self, port, ethertype="x9100"):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"switchport ingress ether-type {ethertype}\r\n")
        print(f"Added ingress ether-type {ethertype} for {port}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def remove_ingress_ethertype(self, port):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd(f"no switchport ingress ether-type\r\n")
        print(f"Removed ingress ether-type for {port}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def show_service_vlan_customer_vlan_id(self):

        d_customer_vlan = {

            "Service VLAN":"",
            "Port":"",
            "Customer VLAN":"",
            "SVLAN Priority":""
        }

        list_of_customer_vlan = list()

        self.session.connect()
        self.session.send_cmd("show service-vlan cvlan\r\n")
        output = self.session.read()
        # print(output)

        match = re.findall(r"\s+(\d+)\s+([GEix]+\d+/\d+)\s+([\d\w]+)\s+([\d\w]+)", output)
        # print(match)
        # print(len(match))

        for i in match:

            d = {}

            for key, value in zip(d_customer_vlan.keys(), i):

                d[key] = value
            # print(d)
            list_of_customer_vlan.append(d)
        print(list_of_customer_vlan)
        self.session.close()

        return list_of_customer_vlan

    def show_service_vlan_provider_edge_configuration(self):

        d_provider_edge = {

            "Service VLAN": "",
            "Port": "",
            "PVID": "",
            "Default Prio": ""
        }

        list_of_provider_edge = list()

        self.session.connect()
        self.session.send_cmd("show service-vlan pvid\r\n")
        output = self.session.read()
        # print(output)

        match = re.findall(r"\s+(\d+)\s+([GEix]+\d+/\d+)\s+([\d\w]+)\s+([\d\w]+)", output)
        # print(match)
        # print(len(match))

        for i in match:

            d = {}

            for key, value in zip(d_provider_edge.keys(), i):

                d[key] = value
            # print(d)
            list_of_provider_edge.append(d)
        print(list_of_provider_edge)
        self.session.close()

        return list_of_provider_edge

    def show_bridge_mode(self):

        d_bridge_mode = {
            "Bridge Mode": ""
        }

        self.session.connect()
        self.session.send_cmd("show running-config")

        output = self.session.read()
        # print(output)

        match = re.findall("Bridge Mode\s+:\s+(\w+-edge)", output)
        # print(match)

        d_bridge_mode["Bridge Mode"] = match[0]
        # print(d_bridge_mode)

        return d_bridge_mode

    def show_bridge_port_type(self, interface):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("set cli pagination off")
        self.session.send_cmd(f"do show interface bridge port-type {interface}")

        output = self.session.read()
        # print(output)

        match = re.findall(r"[GEix]{2}\d/\d+\s+(\w+)", output)
        # print(match)
        port_type = match[0]+"-edge"
        # print(port_type)
        return port_type

    def show_ingress_ethertype(self, interface):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("set cli pagination off")
        self.session.send_cmd(f"do show running-config interface {interface}")

        default_ingress_ethertype = "x88a8"

        output = self.session.read()
        # print(output)
        match = re.findall(r"switchport ingress ether-type\s+(\w+)", output)
        # print(match)
        if len(match) != 0:
            ingress_ethertype = match[0]
        else:
            ingress_ethertype = default_ingress_ethertype
        # print(ingress_ethertype)

        return ingress_ethertype

    def show_egress_ethertype(self, interface):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("set cli pagination off")
        self.session.send_cmd(f"do show running-config interface {interface}")

        default_egress_ethertype = "x88a8"

        output = self.session.read()
        # print(output)
        match = re.findall(r"switchport egress ether-type\s+(\w+)", output)
        # print(match)
        if len(match) != 0:
            egress_ethertype = match[0]
        else:
            egress_ethertype = default_egress_ethertype
        # print(egress_ethertype)

        return egress_ethertype





ip_session = "10.2.109.203"

# obj_qinq = QinQ(ip_session=ip_session)
# obj_qinq.change_bridge_mode(bridge_mode="provider-edge")
# obj_qinq.change_bridge_port_type(port="Gi 0/10",bridge_port_type="provider")
# obj_qinq.add_cvlan_to_svlan(port="Gi 0/5", cvlan="20",svlan="2000")
# obj_qinq.remove_cvlan_to_svlan(port="Gi 0/5",cvlan="20")
# obj_qinq.add_default_service_vlan(port="Gi 0/5",svlan="3000")
# obj_qinq.remove_default_service_vlan(port="Gi 0/5")
# obj_qinq.add_customer_vlan_pvid(port="Gi 0/5",pvid="99")
# obj_qinq.remove_customer_vlan_pvid(port="Gi 0/5")
# obj_qinq.remove_service_vlan_pvid(port="Gi 0/5",svlan="1000")
# obj_qinq.add_service_vlan_pvid(port="Gi 0/5",svlan="1000",pvid="77")
# obj_qinq.add_svlan_prio(port="Gi 0/5", svlan_prio="3")
# obj_qinq.remove_svlan_prio(port="Gi 0/5")
# obj_qinq.add_customer_vlan_svlan_prio(port="Gi 0/5", cvlan="10", svlan_prio="7")
# obj_qinq.remove_customer_vlan_svlan_prio(port="Gi 0/5", cvlan="10")
# obj_qinq.add_def_user_priority(port="Gi 0/5",svlan="1000",def_user_priority="7")
# obj_qinq.remove_def_user_priority(port="Gi 0/5",svlan="2000",def_user_priority="0")
# obj_qinq.add_egress_ethertype(port="Gi 0/6",ethertype="x9100")
# obj_qinq.remove_egress_ethertype(port="Gi 0/6")
# obj_qinq.add_ingress_ethertype(port="Gi 0/6",ethertype="x8100")
# obj_qinq.remove_ingress_ethertype(port="Gi 0/6")
# obj_qinq.show_service_vlan_customer_vlan_id()
# obj_qinq.show_service_vlan_provider_edge_configuration()
# obj_qinq.show_bridge_mode()
# obj_qinq.show_bridge_port_type("gi 0/3")
# obj_qinq.show_ingress_ethertype("gi 0/3")
# obj_qinq.show_egress_ethertype("gi 0/3")