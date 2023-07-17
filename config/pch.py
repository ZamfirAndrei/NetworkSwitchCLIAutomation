import time
import re

from Management import ssh, telnet


class PCH:

    def __init__(self, ip_session="10.2.109.178"):

        print("Clasa PCH")

        self.ip_session = ip_session
        self.session = ssh.SSH(ip=ip_session)
        self.tn = telnet.Telnet(ip=ip_session)

    def create_pch(self, id):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int po {id}\r\n")
        self.session.send_cmd("no shut\r\n")
        output = self.session.read()
        # print(output)
        print(f"The pch {id} has been created")
        self.session.close()

    def remove_pch(self, id):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"no int po {id}\r\n")
        output = self.session.read()
        # print(output)
        print(f"The pch {id} has been removed")
        self.session.close()

    def add_port_to_pch(self, id, port, mode):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd("no shut\r\n")
        self.session.send_cmd(f"channel-group {id} mode {mode}\r\n")
        output = self.session.read()
        # print(output)
        print(f"The port {port} has been added to pch {id}")
        self.session.close()

    def remove_port_to_pch(self, port):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int {port}\r\n")
        self.session.send_cmd("no shut\r\n")
        self.session.send_cmd(f"no channel-group\r\n")
        output = self.session.read()
        # print(output)
        print(f"The port {port} has been removed from pch")
        self.session.close()

    def show_pch_summary(self, id):

        d_port_channel_system = {

            "System Identifier": "",
            "System Priority"  : ""
        }

        d_port_channel_details = {

            "Group": "",
            "Port-channel": "",
            "Protocol": "",
            "Ports": []
        }

        self.session.connect()
        self.session.send_cmd(f"show etherchannel {id} summary\r\n")
        output = self.session.read()
        # print(output)

        match = re.findall(r"Port-channel\s+System\s+Identifier\s+is\s+(\w+.\w+.\w+.\w+.\w+.\w+)[\s\S]+LACP\sSystem\sPriority:\s+(\d+)", output)
        match1 = re.findall(r"(\d+)\s+(Po\d+[(UEIDR\S]+[\SAU,OD]+)\s+(\w+)\s", output)
        ports = re.findall(r"[GExi]+\d/\d+", output)

        # print(match)
        # print(match1)
        # print(ports)

        for i in match:
            for key, value in zip(d_port_channel_system.keys(), i):

                d_port_channel_system[key] = value

        print(d_port_channel_system)

        d_port_channel_details["Group"] = match1[0][0]
        d_port_channel_details["Port-channel"] = match1[0][1]
        d_port_channel_details["Protocol"] = match1[0][2]

        for port in ports:
            # print(port)
            d_port_channel_details["Ports"].append(port)

        print(d_port_channel_details)
        # print(d_port_channel_details["Ports"][1])
        self.session.close()

        return d_port_channel_system, d_port_channel_details

    def change_mode_pch(self, id, mode):

        self.session.connect()
        self.session.send_cmd("conf t\r\n")
        self.session.send_cmd(f"int po {id}\r\n")
        self.session.send_cmd(f"sw mode {mode}\r\n")
        output = self.session.read()
        print(output)
        print(f"The mode of pch {id} has been change to {mode}")
        self.session.close()


obj_pch = PCH(ip_session="10.2.109.195")
# obj_pch.create_pch(id="100")
# obj_pch.create_pch(id="10")
# obj_pch.remove_pch(id="100")
# obj_pch.add_port_to_pch(id="10",port="Ex 0/1",mode="active")
# obj_pch.add_port_to_pch(id="10",port="Ex 0/2",mode="active")
# obj_pch.remove_port_to_pch(port="Gi 0/9")
obj_pch.show_pch_summary(id="1")
# obj_pch.change_mode_pch(id="10",mode="hybrid")




