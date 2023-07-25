import time
import re

from Management import ssh, telnet


class INFOs:

    def __init__(self,ip_session="10.2.109.178"):

        print("Clasa INFOs")

        self.ip_session = ip_session
        self.session = ssh.SSH(ip=ip_session)
        self.tn = telnet.Telnet(ip=ip_session)

    def show_system_info(self):

        self.session.connect()
        self.session.send_cmd(cmd="conf t\r\n")
        self.session.send_cmd(cmd="set cli pagination off\r\n")
        self.session.send_cmd(cmd="do show system info\r\n")
        output = self.session.read()
        # print(output)

        software_version = re.findall(r"CNS Software Version\s+:\s+([\w.-]+)", output)
        model_name = re.findall(r"Model Name\s+:\s+([\w-]+)", output)
        switch_mac_address =  re.findall(r"Switch MAC Address\s+:\s+(\w+.\w+.\w+.\w+.\w+.\w+)", output)
        serial_number = re.findall(r"Serial Number\s+:\s+(\w+)", output)
        system_name = re.findall(r"System Name\s+:\s+([\w-]+)", output)

        print(software_version)
        print(model_name)
        print(switch_mac_address)
        print(serial_number)
        print(system_name)

        return software_version, model_name, switch_mac_address, serial_number, system_name

    def show_run(self, protocol=None):

        self.session.connect()
        self.session.send_cmd(cmd="conf t\r\n")
        self.session.send_cmd(cmd="set cli pagination off\r\n")
        self.session.send_cmd(cmd=f"do show run {protocol}\r\n")
        output = self.session.read()
        print(output)

    def show_env_cpu(self):

        self.session.connect()
        self.session.send_cmd(cmd="show env all\r\n")
        output = self.session.read()
        # print(output)

        ram_threshold = re.findall(r"RAM Threshold\s+:\s+(\d+%)", output)
        ram_usage = re.findall(r"Current RAM Usage\s+:\s+(\d+%)", output)
        cpu_threshold = re.findall(r"CPU Threshold\s+:\s+(\d+%)", output)
        cpu_usage = re.findall(r"Current CPU Usage\s+:\s+(\d+%)", output)
        current_temperature = re.findall(r"Current Temperature\s+:\s+(\d+\w)", output)
        flash_threshold = re.findall(r"Flash Threshold\s+:\s+(\d+%)", output)
        current_flash_usage = re.findall(r"Current Flash Usage\s+:\s+(\d+%)", output)

        print(ram_threshold)
        print(ram_usage)
        print(cpu_threshold)
        print(cpu_usage)
        print(current_temperature)
        print(flash_threshold)
        print(current_flash_usage)

        return ram_threshold, ram_usage, cpu_threshold, cpu_usage, current_temperature, flash_threshold, current_flash_usage

    def show_env_cpu_counters(self):

        self.session.connect()
        self.session.send_cmd(cmd="show cpu-counters\r\n")
        output = self.session.read()
        print(output)

        unicast_packets = re.findall(r"Unicast Packets\s+:\s+(\d+)", output)
        multicast_packets = re.findall(r"Multicast Packets\s+:\s+(\d+)", output)
        broadcast_packets = re.findall(r"Broadcast Packets\s+:\s+(\d+)", output)
        arp_packets = re.findall(r"ARP Packets\s+:\s+(\d+)", output)
        igmp_packets = re.findall(r"IGMP Packets\s+:\s+(\d+)", output)
        ip_multicast_packets = re.findall(r"IP Multicast Packets\s+:\s+(\d+)", output)
        stp_packets = re.findall(r"STP Packets\s+:\s+(\d+)", output)
        lldp_packets = re.findall(r"LLDP Packets\s+:\s+(\d+)", output)
        dhcp_packets = re.findall(r"DHCP Packets\s+:\s+(\d+)", output)
        others_packets = re.findall(r"Other Packets\s+:\s+(\d+)", output)

        print(unicast_packets)
        print(multicast_packets)
        print(broadcast_packets)
        print(arp_packets)
        print(igmp_packets)
        print(ip_multicast_packets)
        print(stp_packets)
        print(lldp_packets)
        print(dhcp_packets)
        print(others_packets)

        return unicast_packets, multicast_packets[0], broadcast_packets, arp_packets, igmp_packets, ip_multicast_packets, stp_packets, lldp_packets, dhcp_packets, others_packets


ip = "10.2.109.238"
# obj = INFOs(ip_session=ip)
# obj.show_system_info()
# obj.show_run()
# obj.show_env_cpu()
# obj.show_env_cpu_counters()
