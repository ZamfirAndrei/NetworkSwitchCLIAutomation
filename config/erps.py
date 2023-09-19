import time
import re

from Management import ssh, telnet


class ERPS:

    def __init__(self, ip_session="10.2.109.178"):

        print("Class ERPS")

        self.ip_session = ip_session
        self.session = ssh.SSH(ip=ip_session)

    def enable_erps_mode(self):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("aps ring enable")
        print(f"ERPS mode has been enabled on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def create_erps_group(self, group_id):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"aps ring group {group_id}")
        print(f"ERPS Ring Group {group_id} has been created on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def configure_erps_protection_type(self, group_id, protection_type):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"aps ring group {group_id}")
        self.session.send_cmd(f"aps protection-type {protection_type}")
        print(f"ERPS Protection-Type {protection_type} has been configured on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def configure_erps_mapped_ports(self, group_id, port1, port2, vlan, local_mep1, remote_mep1, local_mep2, remote_mep2):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"aps ring group {group_id}")
        self.session.send_cmd(f"aps working {port1} {port2} vlan {vlan}")
        self.session.send_cmd(f"aps working port1 local-mep {local_mep1} remote-mep {remote_mep1}")
        self.session.send_cmd(f"aps working port2 local-mep {local_mep2} remote-mep {remote_mep2}")
        print(f"ERPS Mapped Ports {port1} and {port2} have been configured on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def configure_erps_protected_port(self, group_id, protected_port):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"aps ring group {group_id}")
        self.session.send_cmd(f"aps protect {protected_port}")
        print(f"ERPS Protected Port {protected_port} has been configured on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def configure_erps_revertive_mode(self, group_id, wtr_timer):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"aps ring group {group_id}")
        self.session.send_cmd(f"aps revert wtr {wtr_timer}")
        print(f"ERPS Revertive Mode has been configured on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def activate_erps_group(self, group_id):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"aps ring group {group_id}")
        self.session.send_cmd("aps group active")
        print(f"ERPS Group {group_id} has been activated on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def disable_erps_mode(self):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("no aps ring enable")
        print(f"ERPS mode has been disabled on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def delete_erps_group(self, group_id):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"no aps ring group {group_id}")
        print(f"ERPS Ring Group {group_id} has been deleted on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def delete_erps_mapped_ports(self, group_id):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"aps ring group {group_id}")
        self.session.send_cmd(f"no aps working ports")
        print(f"ERPS Mapped Ports have been deleted on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def deactivate_erps_group(self, group_id):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"aps ring group {group_id}")
        self.session.send_cmd("no aps group active")
        print(f"ERPS Group {group_id} has been deactivated on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def delete_erps_protected_port(self, group_id):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"aps ring group {group_id}")
        self.session.send_cmd(f"no aps protect")
        print(f"ERPS Protected Port has been deleted on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def check_rpl_owner(self, group_id):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("set cli pagination off")
        self.session.send_cmd(f"do show aps ring group {group_id}")
        output = self.session.read()
        match = re.findall(r"This node is RPL Owner", output)
        # print(match)

        is_rpl_owner = False

        if len(match) != 0:
            is_rpl_owner = True
        else:
            is_rpl_owner = False

        self.session.close()

        return is_rpl_owner

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

        self.session.close()

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

        match = re.findall(r"([GEix]{2}\d/\d+)\s+([\sNotFailedRemoteFailure]+)\s+(\w+)\s+(\w+)", output)
        # print(match)

        for port in match:

            d = {}

            for key, value in zip(d_port.keys(), port):

                # print(key, value)
                d[key] = value.strip()

            # print(d)
            list_ports.append(d)

        # print(list_ports)

        # SAU merge asa --> d["Port"] = match[i][0] ... daca reinitializezi mereu d-ul la inceput
        # de for astfel incat sa fie gol dictionarul si sa nu se mai suprascrie
        self.session.close()

        return list_ports

    def check_erps_ports_status(self, group_id):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("set cli pagination off")
        self.session.send_cmd(f"do show aps ring group {group_id}")
        output = self.session.read()

        # print(output)
        d_ports = {
            'Port 1': '',
            'Port 2': ''
        }

        match = re.findall(r"Local MEP (\d+) - Remote MEP (\d+) \S+\s+MEP Status: (\w+)\S+\s+Last MEP change: (\d+:\d+:\d+.\d+) ago", output)
        # print(match)

        for i in range(0, 2):

            d_port = dict()

            d_port['Local MEP'] = match[i][0]
            d_port['Remote MEP'] = match[i][1]
            d_port['MEP Status'] = match[i][2]
            d_port['Last MEP change'] = match[i][3]

            # print(d_port)

            d_ports[f'Port {i+1}'] = d_port

        # print(d_ports)
        # print(d_ports['Port 2']['Last MEP change'])

        self.session.close()

        return d_ports

    def check_erps_ring_id_information(self, group_id):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("set cli pagination off")
        self.session.send_cmd(f"do show aps ring group {group_id}")
        output = self.session.read()

        # print(output)
        d_ring_info = {
            'Ring Name': '',
            'RAPS Vlan Id': '',
            'Operating Mode': '',
            'ERPS Compatible Version': '',
            'Ring State': '',
            'Status': '',
            'Wait-to-restore timer': '',
            'Hold timer': '',
            'Guard timer': ''
        }

        match = re.findall(r"Ring Name\s+:\s+(\w+)\S+RAPS Vlan Id\s+:\s+(\d+)\S+Operating Mode\s+:\s+(\w+)[\S+\s+]+ERPS Compatible Version\s+:\s+(\w+)\S+Ring State\s+:\s+(\w+)\s+\S+Status\s+:\s+(\w+)\s+\S+Wait-to-restore timer\s+:\s+([\d+\s+\w+]+)\S+Hold timer\s+:\s+([\d+\s+\w+]+)\S+Guard timer\s+:\s+([\d+\s+\w+]+)", output)

        # print(match)

        for info in match:

            d_ring_info['Ring Name'] = info[0]
            d_ring_info['RAPS Vlan Id'] = info[1]
            d_ring_info['Operating Mode'] = info[2]
            d_ring_info['ERPS Compatible Version'] = info[3]
            d_ring_info['Ring State'] = info[4]
            d_ring_info['Status'] = info[5]
            d_ring_info['Wait-to-restore timer'] = info[6]
            d_ring_info['Hold timer'] = info[7]
            d_ring_info['Guard timer'] = info[8]

        # print(d_ring_info)

        self.session.close()

        return d_ring_info



ip_session = "10.2.109.232"
# erps_obj = ERPS(ip_session=ip_session)
#
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
# erps_obj.check_erps_ports_status("1")
# erps_obj.configure_erps_revertive_mode("1","3000")
# erps_obj.check_erps_ring_id_information("1")
# erps_obj.disable_erps_mode()
# erps_obj.create_erps_group("88")
# erps_obj.delete_erps_group("88")
# erps_obj.deactivate_erps_group("1")
# erps_obj.delete_erps_mapped_ports("1")
# erps_obj.delete_erps_protected_port("1")