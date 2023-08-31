import time
import pytest
import pytest_html
import sys


from config import vlan, interfaces, stp, fdb, ip, rip, ping
from Management import ssh

ip_session_1 = "10.2.109.206"
ip_session_2 = "10.2.109.83"
ip_session_3 = "10.2.109.232"

# DUT 1 Objects

int1 = interfaces.Interface(ip_session=ip_session_1)
vl1 = vlan.VLAN(ip_session=ip_session_1)
stp1 = stp.STP(ip_session=ip_session_1)
fdb1 = fdb.FDB(ip_session=ip_session_1)
ip1 = ip.IP(ip_session=ip_session_1)
rip1 = rip.RIP(ip_session=ip_session_1)
ping1 = ping.PING(ip_session=ip_session_1)

# DUT 2 Objects

int2 = interfaces.Interface(ip_session=ip_session_2)
vl2 = vlan.VLAN(ip_session=ip_session_2)
stp2 = stp.STP(ip_session=ip_session_2)
fdb2 = fdb.FDB(ip_session=ip_session_2)
ip2 = ip.IP(ip_session=ip_session_2)
rip2 = rip.RIP(ip_session=ip_session_2)
ping2 = ping.PING(ip_session=ip_session_2)

# DUT 3 Objects

int3 = interfaces.Interface(ip_session=ip_session_3)
vl3 = vlan.VLAN(ip_session=ip_session_3)
stp3 = stp.STP(ip_session=ip_session_3)
fdb3 = fdb.FDB(ip_session=ip_session_3)
ip3 = ip.IP(ip_session=ip_session_3)
rip3 = rip.RIP(ip_session=ip_session_3)
ping3 = ping.PING(ip_session=ip_session_3)


class TestRIPSuite1:

    def test_func_1(self):

        print("###### Test_func_1 ######")
        print("########## Check if we can advertise networks into RIP and it establish connection #############")
        print("###### 2 DUTs ######")

        int1.no_shut_interfaces("Gi 0/3", "Gi 0/4", "Ex 0/1", "Gi 0/9")
        int2.no_shut_interfaces("Gi 0/4", "Gi 0/5", "Gi 0/6", "Gi 0/9")
        # int3.no_shut_interfaces("Gi 0/4", "Gi 0/9")

        # Creating the VLAN on all DUTs

        vl1.create_vlan(vlan="30")
        vl1.create_vlan(vlan="14")
        vl1.create_vlan(vlan="11")

        vl2.create_vlan(vlan="15")
        vl2.create_vlan(vlan="14")
        vl2.create_vlan(vlan="12")

        # vl3.create_vlan(vlan="11")
        # vl3.create_vlan(vlan="12")
        # vl3.create_vlan(vlan="20")

        # Adding the ports to the VLAN

        vl1.add_ports_to_vlan(ports="Gi 0/3", vlan="30")
        # vl1.add_ports_to_vlan(ports="Gi 0/9", vlan="11")
        vl1.add_ports_to_vlan(ports="Ex 0/1", vlan="14")

        vl2.add_ports_to_vlan(ports="Gi 0/5", vlan= "15")
        vl2.add_ports_to_vlan(ports="Gi 0/9", vlan="14")
        # vl2.add_ports_to_vlan(ports="Gi 0/4", vlan="12")

        # vl3.add_ports_to_vlan(ports="Gi 0/4", vlan="20")
        # vl3.add_ports_to_vlan(ports="Gi 0/9", vlan="11")
        # vl3.add_ports_to_vlan(ports="Gi 0/4", vlan="12")

        # Create IP interfaces on all DUTs for the specific VLANs

        ip1.add_ip_interfaces("14", "30", int_vlan14 = ["14.0.0.2", "255.255.255.0"], int_vlan30 = ["30.0.0.1", "255.255.255.0"])
        ip1.no_shut_int_vlans("14", "30")

        ip2.add_ip_interfaces("14", "15", int_vlan14=["14.0.0.1", "255.255.255.0"], int_vlan15=["15.0.0.1", "255.255.255.0"])
        ip2.no_shut_int_vlans("14", "15")

        # Enable rip on all DUTs and advertise the IPs

        rip1.enable_rip()
        rip1.advertise_networks("14.0.0.2", "30.0.0.1")

        rip2.enable_rip()
        rip2.advertise_networks("14.0.0.1", "15.0.0.1")
