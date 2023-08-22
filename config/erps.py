import time
import re

from Management import ssh, telnet


class ERPS:

    def __init__(self, ip_session="10.2.109.178"):

        print("Clasa ERPS")

        self.ip_session = ip_session
        self.session = ssh.SSH(ip=ip_session)

    def enable_erps_mode(self):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("aps ring enable")
        print("ERPS mode has been enabled")
        output = self.session.read()
        print(output)
        self.session.close()

    def create_erps_group(self, group_id):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"aps ring group {group_id}")
        print(f"ERPS Ring Group {group_id} has been created")
        output = self.session.read()
        print(output)
        self.session.close()

    def configure_erps_protection_type(self, group_id, protection_type):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"aps ring group {group_id}")
        self.session.send_cmd(f"aps protection-type {protection_type}")
        print(f"ERPS Protection-Type {protection_type} has been configured")
        output = self.session.read()
        print(output)
        self.session.close()

    def configure_erps_mapped_ports(self, group_id, port1, port2, vlan, local_mep1, remote_mep1, local_mep2, remote_mep2):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"aps ring group {group_id}")
        self.session.send_cmd(f"aps working {port1} {port2} vlan {vlan}")
        self.session.send_cmd(f"aps working port1 local-mep {local_mep1} remote-mep {remote_mep1}")
        self.session.send_cmd(f"aps working port2 local-mep {local_mep2} remote-mep {remote_mep2}")
        print(f"ERPS Mapped Ports {port1} and {port2} have been configured")
        output = self.session.read()
        print(output)
        self.session.close()

    def configure_erps_protected_port(self, group_id, protected_port):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"aps ring group {group_id}")
        self.session.send_cmd(f"aps protect {protected_port}")
        print(f"ERPS Protected Port {protected_port} has been configured")
        output = self.session.read()
        print(output)
        self.session.close()

    def activate_erps_group(self, group_id):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"aps ring group {group_id}")
        self.session.send_cmd("aps group active")
        print(f"ERPS Group {group_id} has been activated")
        output = self.session.read()
        print(output)
        self.session.close()

    def check_rpl_owner(self, group_id):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("set cli pagination off")
        self.session.send_cmd(f"do show aps ring group {group_id}")
        output = self.session.read()
        match = re.findall(r"This node is RPL Owner", output)
        # print(match)

        rpl_owner = False

        if len(match) != 0:
            rpl_owner = True
        else:
            rpl_owner = False

        return rpl_owner

    def check_rpl_port(self, group_id):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("set cli pagination off")
        self.session.send_cmd(f"do show aps ring group {group_id}")
        output = self.session.read()
        match = re.findall(r" RPL Port is ([GEix]{2}\d/\d+)", output)
        # print(match)

        rpl_port = ''

        if len(match) != 0:
            rpl_port = match[0]
        else:
            rpl_port = "There is no RPL Port"

        return rpl_port

    def check_erps_ports(self, group_id):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("set cli pagination off")
        self.session.send_cmd(f"do show aps ring group {group_id}")
        output = self.session.read()

        list_ports = []
        d_port = {

            'Ring Port': '',
            'Link Status': '',
            'Command': '',
            'Port Status': ''
        }

        d = dict()

        match = re.findall(r"([GEix]{2}\d/\d+)\s+(\w+)\s+(\w+)\s+(\w+)", output)
        print(match)

        for port in match:

            d = {}

            for key, value in zip(d_port.keys(), port):

                print(key, value)
                d[key] = value
            print(d)
            list_ports.append(d)

        print(list_ports)

        # SAU merge asa --> d["Port"] = match[i][0] ... daca reinitializezi mereu d-ul la inceput
        # de for astfel incat sa fie gol dictionarul si sa nu se mai suprascrie
        return list_ports


ip_session = "10.2.109.232"
erps_obj = ERPS(ip_session=ip_session)

# erps_obj.enable_erps_mode()
# erps_obj.create_erps_group("1")
# erps_obj.configure_erps_protection_type("1", "port-based")
# erps_obj.configure_erps_mapped_ports("1", "gi 0/4", "gi 0/9", "3500", "88", "8", "99", "9")
# erps_obj.configure_erps_protected_port("1", "gi 0/4")
# erps_obj.activate_erps_group("1")
# isRPLowner = erps_obj.check_rpl_owner("1")
# print(isRPLowner)
# RPLport = erps_obj.check_rpl_port("1")
# print(RPLport)
# ports_list = erps_obj.check_erps_ports("1")
# print(ports_list)

