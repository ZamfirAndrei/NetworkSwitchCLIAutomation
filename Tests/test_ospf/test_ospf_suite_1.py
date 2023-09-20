import time
import pytest
import pytest_html
import sys

from config import interfaces
from Management import dut_objects

ip_session_1 = "10.2.109.206"
ip_session_2 = "10.2.109.83"
ip_session_3 = "10.2.109.232"

DUT1 = dut_objects.DUT_Objects(ip_session=ip_session_1)
DUT2 = dut_objects.DUT_Objects(ip_session=ip_session_2)
DUT3 = dut_objects.DUT_Objects(ip_session=ip_session_3)

# int1 = interfaces.Interface(ip_session=ip_session_1)


class TestOSPFSuite1:

    def test_func_1(self):

        print("###### Test_func_1 ######")
        print("########## Verify if Connected routes are redistributed into OSPF #############")

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/5", "Gi 0/9")

        # Adding the ports to the VLAN

        DUT1.vl.add_ports_to_vlan(ports="Ex0/1", vlan="20")

        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")

        # Create IP interfaces on all DUTs for the specific VLANs

        DUT1.ip.add_ip_interfaces("20", int_vlan20=["20.0.0.2", "255.255.255.0"])
        DUT1.vl.no_shut_int_vlans("30")

        DUT2.ip.add_ip_interfaces("20", "15", int_vlan20=["20.0.0.1", "255.255.255.0"],int_vlan15=["15.0.0.1", "255.255.255.0"])
        DUT2.ip.no_shut_int_vlans("15", "20")

        # Enable ospf on all DUTs and advertise the IPs

        DUT1.ospf.enable_ospf()
        DUT2.ospf.enable_ospf()

        DUT2.ospf.advertise_networks(int_vlan20=["20.0.0.2", "0.0.0.0"])
        DUT2.ospf.advertise_networks(int_vlan15=["15.0.0.1", "0.0.0.0"],int_vlan20=["20.0.0.1", "0.0.0.0"])

        time.sleep(30)

