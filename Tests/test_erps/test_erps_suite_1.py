import time
import pytest
import pytest_html
import sys


from config import vlan, interfaces, erps, fdb
from Management import ssh

ip_session_1 = "10.2.109.206"
ip_session_2 = "10.2.109.83"
ip_session_3 = "10.2.109.232"

# DUT 1 Objects

int1 = interfaces.Interface(ip_session=ip_session_1)
vl1 = vlan.VLAN(ip_session=ip_session_1)
erps1 = erps.ERPS(ip_session=ip_session_1)
fdb1 = fdb.FDB(ip_session=ip_session_1)

# DUT 2 Objects

int2 = interfaces.Interface(ip_session=ip_session_2)
vl2 = vlan.VLAN(ip_session=ip_session_2)
erps2 = erps.ERPS(ip_session=ip_session_2)
fdb2 = fdb.FDB(ip_session=ip_session_2)

# DUT 3 Objects

int3 = interfaces.Interface(ip_session=ip_session_3)
vl3 = vlan.VLAN(ip_session=ip_session_3)
erps3 = erps.ERPS(ip_session=ip_session_3)
fdb3 = fdb.FDB(ip_session=ip_session_3)


class TestERPSSuite1:

    def test_func_1(self):

        print("###### ERPS_G.8032_Functionality_01 ######")
        print("########## Verify a Port Based single ring ERPS configuration can be succesfully established in a minimum 3 switches topology. #############")

        # < VLAN configuration >

        # Creating ERPS dedicated traffic VLAN on each DUT
        vl1.create_vlan("3500")
        vl2.create_vlan("3500")
        vl3.create_vlan("3500")

        # Adding the ports to the ERPS dedicated traffic VLAN on each DUT
        vl1.add_ports_to_vlan("Ex 0/1", vlan="3500")
        vl1.add_ports_to_vlan("Gi 0/9", vlan="3500")

        vl2.add_ports_to_vlan("Gi 0/4", vlan="3500")
        vl2.add_ports_to_vlan("Gi 0/9", vlan="3500")

        vl3.add_ports_to_vlan("Gi 0/4", vlan="3500")
        vl3.add_ports_to_vlan("Gi 0/9", vlan="3500")

        # < Interfaces configuration >

        # No shutting the ports for the ERPS dedicated traffic VLAN on each DUT
        int1.no_shut_interfaces("Ex 0/1", "Gi 0/9")
        int2.no_shut_interfaces("Gi 0/4", "Gi 0/9")
        int3.no_shut_interfaces("Gi 0/4", "Gi 0/9")

        # < ERPS configuration >

        # ERPS configuration for DUT 1, which will be the RPL Owner
        erps1.enable_erps_mode()
        erps1.create_erps_group("1")
        erps1.configure_erps_protection_type("1", "port-based")
        erps1.configure_erps_mapped_ports("1", "ex 0/1", "gi 0/9", "3500", "88", "8", "99", "9")
        erps1.configure_erps_protected_port("1", "gi 0/4")
        erps1.activate_erps_group("1")

        # ERPS configuration for DUT 2
        erps2.enable_erps_mode()
        erps2.create_erps_group("1")
        erps2.configure_erps_protection_type("1", "port-based")
        erps2.configure_erps_mapped_ports("1", "gi 0/4", "gi 0/9", "3500", "77", "7", "88", "8")
        erps2.activate_erps_group("1")

        # ERPS configuration for DUT 3
        erps3.enable_erps_mode()
        erps3.create_erps_group("1")
        erps3.configure_erps_protection_type("1", "port-based")
        erps3.configure_erps_mapped_ports("1", "gi 0/4", "gi 0/9", "3500", "7", "77", "9", "99")
        erps3.activate_erps_group("1")


