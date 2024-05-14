import time
import pytest
import pytest_html
import sys

from Management import dut_objects
from test_beds import test_bed_1
from flows import rip_flow

dut6 = test_bed_1.DUT6
dut4 = test_bed_1.DUT4

DUT6 = dut_objects.DUT_Objects_TestBed(dut6)
DUT4 = dut_objects.DUT_Objects_TestBed(dut4)

rip_flow_ = rip_flow.RIPflow()

class TestRIPFASuite1:

    def test_func_1(self):

        print("###### Test_func_1 ######")
        print( "########## Check if we can advertise networks into RIP and it establish connection using int vlans #############")
        print("###### 2 DUTs ######")

        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT4, port=DUT4.ports["v4"],vlan="20",
                                                                                  ip="20.0.0.2", mask="255.255.255.0")
        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT4, port=DUT4.ports["v1"],vlan="30",
                                                                                  ip="30.0.0.1", mask="255.255.255.0")

        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT6, port=DUT6.ports["v3"], vlan="20",
                                                                                  ip="20.0.0.1",  mask="255.255.255.0")
        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT6, port=DUT6.ports["v1"], vlan="15",
                                                                                  ip="15.0.0.1", mask="255.255.255.0")

        rip_flow_.enable_and_advertise_networks(DUT4, "20.0.0.2", "30.0.0.1")
        rip_flow_.enable_and_advertise_networks(DUT6, "20.0.0.1", "15.0.0.1")

        time.sleep(30)

        rip_flow_.confirm_network_details_in_the_routing_table(DUT4, network="15.0.0.0", protocol="R")
        rip_flow_.confirm_network_details_in_the_routing_table(DUT6, network="30.0.0.0", protocol="R")

        print("########## Removing the config #############")

        rip_flow_.disable_RIP(DUT4)
        rip_flow_.disable_RIP(DUT6)

        rip_flow_.remove_vlans_and_interfaces_vlan(DUT4, "20", "30")
        rip_flow_.remove_vlans_and_interfaces_vlan(DUT6, "20", "15")

        rip_flow_.shut_interfaces(DUT4, DUT4.ports["v4"], DUT4.ports["v1"])
        rip_flow_.shut_interfaces(DUT6, DUT6.ports["v3"], DUT6.ports["v1"])


    def test_func_2(self):

        print("###### Test_func_2 ######")
        print("########## Verify a DUT sends a default route if the default-information originate is configured on a RIP enabled interface.#############")
        print("###### 2 DUTs ######")

        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT4, port=DUT4.ports["v4"], vlan="20",
                                                                                  ip="20.0.0.2", mask="255.255.255.0")

        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT6, port=DUT6.ports["v3"], vlan="20",
                                                                                  ip="20.0.0.1", mask="255.255.255.0")
        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT6, port=DUT6.ports["v1"], vlan="99",
                                                                                  ip="99.0.0.1", mask="255.255.255.0")

        rip_flow_.enable_and_advertise_networks(DUT4, "20.0.0.2")
        rip_flow_.enable_and_advertise_networks(DUT6, "20.0.0.1", "99.0.0.1")

        # Advertising the default route on DUT6 and installing the route on DUT4

        DUT6.rip.add_default_information_originate(int_vlan="20")
        DUT4.rip.add_ip_default_route_install(int_vlan="20")

        time.sleep(30)

        rip_flow_.confirm_network_details_in_the_routing_table(DUT4, network="0.0.0.0", protocol="R")
        rip_flow_.confirm_network_details_in_the_routing_table(DUT4, network="99.0.0.0", protocol="R")

        # Remove the route install and check if the default route is not in the routing table

        DUT4.rip.remove_ip_default_route_install(int_vlan="20")

        DUT4.ip.shut_int_vlan(int_vlan="20")
        DUT4.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(30)

        rip_flow_.confirm_network_details_in_the_routing_table(DUT4, network="0.0.0.0", protocol=" ")
        rip_flow_.confirm_network_details_in_the_routing_table(DUT4, network="99.0.0.0", protocol="R")

        print("########## Removing the config #############")

        DUT6.rip.remove_default_information_originate(int_vlan="20")

        rip_flow_.disable_RIP(DUT4)
        rip_flow_.disable_RIP(DUT6)

        rip_flow_.remove_vlans_and_interfaces_vlan(DUT4, "20")
        rip_flow_.remove_vlans_and_interfaces_vlan(DUT6, "20", "99")

        rip_flow_.shut_interfaces(DUT4, DUT4.ports["v4"])
        rip_flow_.shut_interfaces(DUT6, DUT6.ports["v3"], DUT6.ports["v1"])

    def test_func_3(self):

        print("###### Test_func_3 ######")
        print("########## Verify functionality for redistribute connected #############")
        print("###### 2 DUTs ######")

        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT4, port=DUT4.ports["v4"],
                                                                                   vlan="20",ip="20.0.0.2", mask="255.255.255.0")

        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT6, port=DUT6.ports["v3"],
                                                                                   vlan="20", ip="20.0.0.1", mask="255.255.255.0")
        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT6, port=DUT6.ports["v1"],
                                                                                   vlan="15", ip="15.0.0.1", mask="255.255.255.0")
        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT6, port=DUT6.ports["v1"],
                                                                                   vlan="99", ip="99.0.0.1", mask="255.255.255.0")
        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT6, port=DUT6.ports["v1"],
                                                                                   vlan="100", ip="100.0.0.1", mask="255.255.255.0")

        rip_flow_.enable_and_advertise_networks(DUT4, "20.0.0.2")
        rip_flow_.enable_and_advertise_networks(DUT6, "20.0.0.1", "99.0.0.1")

        # Redistributing the connected networks on DUT6 and installing them on DUT4

        DUT6.rip.redistribute_connected()

        time.sleep(30)

        rip_flow_.confirm_network_details_in_the_routing_table(DUT4, network="15.0.0.0", protocol="R")
        rip_flow_.confirm_network_details_in_the_routing_table(DUT4, network="99.0.0.0", protocol="R")
        rip_flow_.confirm_network_details_in_the_routing_table(DUT4, network="100.0.0.0", protocol="R")

        # Remove redistribution on DUT6 and check if the connected routes are not anymore in the routing table of DUT4

        DUT6.rip.remove_redistribute_connected()

        DUT4.ip.shut_int_vlan(int_vlan="20")
        DUT4.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(30)

        rip_flow_.confirm_network_not_in_the_routing_table(DUT4, network="15.0.0.0")
        rip_flow_.confirm_network_not_in_the_routing_table(DUT4, network="100.0.0.0")
        rip_flow_.confirm_network_details_in_the_routing_table(DUT4, network="99.0.0.0", protocol="R")

        print("########## Removing the config #############")

        rip_flow_.disable_RIP(DUT4)
        rip_flow_.disable_RIP(DUT6)

        rip_flow_.remove_vlans_and_interfaces_vlan(DUT4, "20")
        rip_flow_.remove_vlans_and_interfaces_vlan(DUT6, "20", "99", "15", "100")

        rip_flow_.shut_interfaces(DUT4, DUT4.ports["v4"])
        rip_flow_.shut_interfaces(DUT6, DUT6.ports["v3"], DUT6.ports["v1"])

    def test_func_4(self):

        print("###### Test_func_4 ######")
        print("########## Verify functionality for redistribute static #############")
        print("###### 2 DUTs ######")

        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT4, port=DUT4.ports["v4"], vlan="20",
                                                                                  ip="20.0.0.2", mask="255.255.255.0")

        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT6, port=DUT6.ports["v3"], vlan="20",
                                                                                  ip="20.0.0.1", mask="255.255.255.0")
        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT6, port=DUT6.ports["v1"], vlan="99",
                                                                                  ip="99.0.0.1", mask="255.255.255.0")

        rip_flow_.enable_and_advertise_networks(DUT4, "20.0.0.2")
        rip_flow_.enable_and_advertise_networks(DUT6, "20.0.0.1", "99.0.0.1")

        # Creating a static route

        DUT6.ip.add_static_route(network_dest="100.0.0.0", mask_dest="255.255.0.0", next_hop="99.0.0.100")

        # Redistributing the static network on DUT6 and installing it on DUT4

        DUT6.rip.redistribute_static()

        time.sleep(30)

        rip_flow_.confirm_network_details_in_the_routing_table(DUT4, network="99.0.0.0", protocol="R")
        rip_flow_.confirm_network_details_in_the_routing_table(DUT4, network="100.0.0.0", protocol="R")

        # Remove the static route on DUT6 and check if the route is not anymore in the routing table of DUT4

        DUT6.rip.remove_redistribute_static()

        DUT4.ip.shut_int_vlan(int_vlan="20")
        DUT4.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(30)

        rip_flow_.confirm_network_not_in_the_routing_table(DUT4, network="100.0.0.0")
        rip_flow_.confirm_network_details_in_the_routing_table(DUT4, network="99.0.0.0", protocol="R")

        print("########## Removing the config #############")

        rip_flow_.disable_RIP(DUT4)
        rip_flow_.disable_RIP(DUT6)

        DUT6.ip.remove_static_route(network_dest="100.0.0.0", mask_dest="255.255.0.0", next_hop="99.0.0.100")

        rip_flow_.remove_vlans_and_interfaces_vlan(DUT4, "20")
        rip_flow_.remove_vlans_and_interfaces_vlan(DUT6, "20", "99")

        rip_flow_.shut_interfaces(DUT4, DUT4.ports["v4"])
        rip_flow_.shut_interfaces(DUT6, DUT6.ports["v3"], DUT6.ports["v1"])


