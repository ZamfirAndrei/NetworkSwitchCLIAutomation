import time
import pytest
import pytest_html
import sys

from Management import dut_objects
from test_beds import test_bed_1
from flows import rip_flow, ospf_flow

dut1 = test_bed_1.DUT1
dut2 = test_bed_1.DUT2
dut3 = test_bed_1.DUT3

DUT1 = dut_objects.DUT_Objects_TestBed(dut1)
DUT2 = dut_objects.DUT_Objects_TestBed(dut2)
DUT3 = dut_objects.DUT_Objects_TestBed(dut3)

rip_flow_ = rip_flow.RIPflow()
ospf_flow_ = ospf_flow.OSPFflow()

class TestRIPLegacy:

    def test_func_1(self):

        print("###### Test_func_1 ######")
        print( "########## Check if we can advertise networks into RIP and it establish connection using int vlans #############")
        print("###### 2 DUTs ######")

        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT1, port=DUT1.ports["v1"],vlan="20",
                                                                                  ip="20.0.0.2", mask="255.255.255.0")
        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT1, port=DUT1.ports["h3"],vlan="30",
                                                                                  ip="30.0.0.1", mask="255.255.255.0")

        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["v1"], vlan="20",
                                                                                  ip="20.0.0.1",  mask="255.255.255.0")
        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["h4"], vlan="15",
                                                                                  ip="15.0.0.1", mask="255.255.255.0")

        rip_flow_.enable_and_advertise_networks(DUT1, "20.0.0.2", "30.0.0.1")
        rip_flow_.enable_and_advertise_networks(DUT2, "20.0.0.1", "15.0.0.1")

        time.sleep(30)

        rip_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="R")
        rip_flow_.confirm_network_details_in_the_routing_table(DUT2, network="30.0.0.0", protocol="R")

        print("########## Removing the config #############")

        rip_flow_.disable_RIP(DUT1)
        rip_flow_.disable_RIP(DUT2)

        rip_flow_.remove_vlans_and_interfaces_vlan(DUT1, "20", "30")
        rip_flow_.remove_vlans_and_interfaces_vlan(DUT2, "20", "15")

        rip_flow_.shut_interfaces(DUT1, DUT1.ports["v1"], DUT1.ports["h3"])
        rip_flow_.shut_interfaces(DUT2, DUT2.ports["v1"], DUT2.ports["h4"])


    def test_func_2(self):

        print("###### Test_func_2 ######")
        print("########## Verify a DUT sends a default route if the default-information originate is configured on a RIP enabled interface.#############")
        print("###### 2 DUTs ######")

        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT1, port=DUT1.ports["v1"], vlan="20",
                                                                                  ip="20.0.0.2", mask="255.255.255.0")

        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["v1"], vlan="20",
                                                                                  ip="20.0.0.1", mask="255.255.255.0")
        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["h4"], vlan="99",
                                                                                  ip="99.0.0.1", mask="255.255.255.0")
        #
        rip_flow_.enable_and_advertise_networks(DUT1, "20.0.0.2")
        rip_flow_.enable_and_advertise_networks(DUT2, "20.0.0.1", "99.0.0.1")

        # Advertising the default route on DUT2 and installing the route on DUT1

        DUT2.rip.add_default_information_originate(int_vlan="20")
        DUT1.rip.add_ip_default_route_install(int_vlan="20")

        time.sleep(30)

        rip_flow_.confirm_network_details_in_the_routing_table(DUT1, network="0.0.0.0", protocol="R")
        rip_flow_.confirm_network_details_in_the_routing_table(DUT1, network="99.0.0.0", protocol="R")

        # Remove the route install and check if the default route is not in the routing table

        DUT1.rip.remove_ip_default_route_install(int_vlan="20")

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(30)

        rip_flow_.confirm_network_details_in_the_routing_table(DUT1, network="0.0.0.0", protocol=" ")
        rip_flow_.confirm_network_details_in_the_routing_table(DUT1, network="99.0.0.0", protocol="R")

        print("########## Removing the config #############")

        DUT2.rip.remove_default_information_originate(int_vlan="20")

        rip_flow_.disable_RIP(DUT1)
        rip_flow_.disable_RIP(DUT2)

        rip_flow_.remove_vlans_and_interfaces_vlan(DUT1, "20")
        rip_flow_.remove_vlans_and_interfaces_vlan(DUT2, "20", "99")

        rip_flow_.shut_interfaces(DUT1, DUT1.ports["v1"])
        rip_flow_.shut_interfaces(DUT2, DUT2.ports["v1"], DUT2.ports["h4"])

    def test_func_3(self):

        print("###### Test_func_3 ######")
        print("########## Verify functionality for redistribute connected #############")
        print("###### 2 DUTs ######")

        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT1, port=DUT1.ports["v1"],
                                                                                   vlan="20",ip="20.0.0.2", mask="255.255.255.0")

        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["v1"],
                                                                                   vlan="20", ip="20.0.0.1", mask="255.255.255.0")
        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["h4"],
                                                                                   vlan="15", ip="15.0.0.1", mask="255.255.255.0")
        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["h4"],
                                                                                   vlan="99", ip="99.0.0.1", mask="255.255.255.0")
        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["h4"],
                                                                                   vlan="100", ip="100.0.0.1", mask="255.255.255.0")

        rip_flow_.enable_and_advertise_networks(DUT1, "20.0.0.2")
        rip_flow_.enable_and_advertise_networks(DUT2, "20.0.0.1", "99.0.0.1")

        # Redistributing the connected networks on DUT2 and installing them on DUT1

        DUT2.rip.redistribute_connected()

        time.sleep(30)

        rip_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="R")
        rip_flow_.confirm_network_details_in_the_routing_table(DUT1, network="99.0.0.0", protocol="R")
        rip_flow_.confirm_network_details_in_the_routing_table(DUT1, network="100.0.0.0", protocol="R")

        # Remove redistribution on DUT2 and check if the connected routes are not anymore in the routing table of DUT1

        DUT2.rip.remove_redistribute_connected()

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(30)

        rip_flow_.confirm_network_not_in_the_routing_table(DUT1, network="15.0.0.0")
        rip_flow_.confirm_network_not_in_the_routing_table(DUT1, network="100.0.0.0")
        rip_flow_.confirm_network_details_in_the_routing_table(DUT1, network="99.0.0.0", protocol="R")

        print("########## Removing the config #############")

        rip_flow_.disable_RIP(DUT1)
        rip_flow_.disable_RIP(DUT2)

        rip_flow_.remove_vlans_and_interfaces_vlan(DUT1, "20")
        rip_flow_.remove_vlans_and_interfaces_vlan(DUT2, "20", "99", "15", "100")

        rip_flow_.shut_interfaces(DUT1, DUT1.ports["v1"])
        rip_flow_.shut_interfaces(DUT2, DUT2.ports["v1"], DUT2.ports["h4"])

    def test_func_4(self):

        print("###### Test_func_4 ######")
        print("########## Verify functionality for redistribute static #############")
        print("###### 2 DUTs ######")

        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT1, port=DUT1.ports["v1"], vlan="20",
                                                                                  ip="20.0.0.2", mask="255.255.255.0")

        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["v1"], vlan="20",
                                                                                  ip="20.0.0.1", mask="255.255.255.0")
        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["h4"], vlan="99",
                                                                                  ip="99.0.0.1", mask="255.255.255.0")

        rip_flow_.enable_and_advertise_networks(DUT1, "20.0.0.2")
        rip_flow_.enable_and_advertise_networks(DUT2, "20.0.0.1", "99.0.0.1")

        # Creating a static route

        DUT2.ip.add_static_route(network_dest="100.0.0.0", mask_dest="255.255.0.0", next_hop="99.0.0.100")

        # Redistributing the static network on DUT2 and installing it on DUT1

        DUT2.rip.redistribute_static()

        time.sleep(30)

        rip_flow_.confirm_network_details_in_the_routing_table(DUT1, network="99.0.0.0", protocol="R")
        rip_flow_.confirm_network_details_in_the_routing_table(DUT1, network="100.0.0.0", protocol="R")

        # Remove the static route on DUT2 and check if the route is not anymore in the routing table of DUT1

        DUT2.rip.remove_redistribute_static()

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(30)

        rip_flow_.confirm_network_not_in_the_routing_table(DUT1, network="100.0.0.0")
        rip_flow_.confirm_network_details_in_the_routing_table(DUT1, network="99.0.0.0", protocol="R")

        print("########## Removing the config #############")

        rip_flow_.disable_RIP(DUT1)
        rip_flow_.disable_RIP(DUT2)

        DUT2.ip.remove_static_route(network_dest="100.0.0.0", mask_dest="255.255.0.0", next_hop="99.0.0.100")

        rip_flow_.remove_vlans_and_interfaces_vlan(DUT1, "20")
        rip_flow_.remove_vlans_and_interfaces_vlan(DUT2, "20", "99")

        rip_flow_.shut_interfaces(DUT1, DUT1.ports["v1"])
        rip_flow_.shut_interfaces(DUT2, DUT2.ports["v1"], DUT2.ports["h4"])

    def test_func_5(self):

        print("###### Test_func_5 ######")
        print("########## Verify auto-summary #############")
        print("###### 2 DUTs ######")

        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT1, port=DUT1.ports["v1"], vlan="20",
                                                                                  ip="20.0.0.2", mask="255.255.255.0")

        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["v1"], vlan="20",
                                                                                  ip="20.0.0.1", mask="255.255.255.0")
        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["h4"], vlan="15",
                                                                                  ip="15.0.0.1", mask="255.255.255.0")

        rip_flow_.enable_and_advertise_networks(DUT1, "20.0.0.2")
        rip_flow_.enable_and_advertise_networks(DUT2, "20.0.0.1", "15.0.0.1")

        # Creating a static route

        DUT2.ip.add_static_route(network_dest="88.88.88.0", mask_dest="255.255.255.128", next_hop="15.0.0.100")

        # Disabling no-auto summary on DUT2, so it will redistribute classless subnets

        DUT2.rip.remove_auto_summary()

        # Redistributing the static network on DUT2 and installing it on DUT1

        DUT2.rip.redistribute_static()

        # Checking if the routes are installed and that are classless

        time.sleep(30)

        rip_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="R", mask="24")
        rip_flow_.confirm_network_details_in_the_routing_table(DUT1, network="88.88.88.0", protocol="R", mask="25")

        # Enable the auto-summary on DUT2 and check if the route is classfull and is present in the routing table of DUT1

        DUT2.rip.auto_summary()

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(30)

        rip_flow_.confirm_network_not_in_the_routing_table(DUT1, network="88.88.88.0")
        rip_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="R", mask="8")
        rip_flow_.confirm_network_details_in_the_routing_table(DUT1, network="88.0.0.0", protocol="R", mask="8")

        print("########## Removing the config #############")

        rip_flow_.disable_RIP(DUT1)
        rip_flow_.disable_RIP(DUT2)

        DUT2.ip.remove_static_route(network_dest="88.88.88.0", mask_dest="255.255.255.128", next_hop="15.0.0.100")

        rip_flow_.remove_vlans_and_interfaces_vlan(DUT1, "20")
        rip_flow_.remove_vlans_and_interfaces_vlan(DUT2, "20", "15")

        rip_flow_.shut_interfaces(DUT1, DUT1.ports["v1"])
        rip_flow_.shut_interfaces(DUT2, DUT2.ports["v1"], DUT2.ports["h4"])

    def test_func_6(self):

        print("###### Test_func_6 ######")
        print("########## Verify that administrative RIP distance can be changed to other value #############")
        print("###### 2 DUTs ######")

        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT1, port=DUT1.ports["v1"],vlan="20",
                                                                                  ip="20.0.0.2", mask="255.255.255.0")

        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["v1"], vlan="20",
                                                                                  ip="20.0.0.1", mask="255.255.255.0")
        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["h4"],vlan="15",
                                                                                  ip="15.0.0.1", mask="255.255.255.0")

        rip_flow_.enable_and_advertise_networks(DUT1, "20.0.0.2")
        rip_flow_.enable_and_advertise_networks(DUT2, "20.0.0.1", "15.0.0.1")

        ospf_flow_.enable_and_advertise_networks(DUT1, int_vlan20=["20.0.0.2", "0.0.0.0"])
        ospf_flow_.enable_and_advertise_networks(DUT2, int_vlan20=["20.0.0.1", "0.0.0.0"],
                                                       int_vlan15=["15.0.0.1", "0.0.0.0"])

        # Disabling no-auto summary on DUT2 so it will redistribute classless subnets

        DUT2.rip.remove_auto_summary()

        # Configuring the Distance on DUT1 so to routes are learned using RIP

        DUT1.rip.add_distance(distance="99")

        # Checking if the routes are installed and that are learned via RIP

        time.sleep(30)

        rip_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="R", mask="24")

        # Remove the distance and check that the routes are learned via OSPF

        DUT1.rip.remove_distance()

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(45)

        rip_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="O", mask="24")

        print("########## Removing the config #############")

        rip_flow_.disable_RIP(DUT1)
        rip_flow_.disable_RIP(DUT2)

        ospf_flow_.remove_networks(DUT1, int_vlan20=["20.0.0.2", "0.0.0.0"])
        ospf_flow_.remove_networks(DUT2, int_vlan20=["20.0.0.1", "0.0.0.0"], int_vlan15=["15.0.0.1", "0.0.0.0"])

        ospf_flow_.disable_OSPF(DUT1)
        ospf_flow_.disable_OSPF(DUT2)

        rip_flow_.remove_vlans_and_interfaces_vlan(DUT1, "20")
        rip_flow_.remove_vlans_and_interfaces_vlan(DUT2, "20", "15")

        rip_flow_.shut_interfaces(DUT1, DUT1.ports["v1"])
        rip_flow_.shut_interfaces(DUT2, DUT2.ports["v1"], DUT2.ports["h4"])

    def test_func_7(self):

        print("###### Test_func_7 ######")
        print("########## Verify functionality for passive-interface #############")
        print("###### 2 DUTs ######")

        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT1, port=DUT1.ports["v1"],
                                                                                  vlan="20",
                                                                                  ip="20.0.0.2", mask="255.255.255.0")

        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["v1"],
                                                                                  vlan="20",
                                                                                  ip="20.0.0.1", mask="255.255.255.0")
        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["h4"],
                                                                                  vlan="15",
                                                                                  ip="15.0.0.1", mask="255.255.255.0")

        rip_flow_.enable_and_advertise_networks(DUT1, "20.0.0.2")
        rip_flow_.enable_and_advertise_networks(DUT2, "20.0.0.1", "15.0.0.1")

        # Enable passive interface on the int VLAN between the DUTs and shut/no shut the int VLAN between them

        DUT2.rip.add_passive_interface(vlan="20")

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        # Checking if the routes are not installed on DUT1 and that are classless

        time.sleep(45)

        rip_flow_.confirm_network_not_in_the_routing_table(DUT1, network="15.0.0.0")

        # Disable the passive interface and check that the routes are installed on DUT1

        DUT2.rip.remove_passive_interface(vlan="20")

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(45)

        rip_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="R")

        print("########## Removing the config #############")

        rip_flow_.disable_RIP(DUT1)
        rip_flow_.disable_RIP(DUT2)

        rip_flow_.remove_vlans_and_interfaces_vlan(DUT1, "20")
        rip_flow_.remove_vlans_and_interfaces_vlan(DUT2, "20", "15")

        rip_flow_.shut_interfaces(DUT1, DUT1.ports["v1"])
        rip_flow_.shut_interfaces(DUT2, DUT2.ports["v1"], DUT2.ports["h4"])

    def test_func_8(self):

        print("###### Test_func_8 ######")
        print("########## Verify functionality for default-metric #############")
        print("###### 2 DUTs ######")

        default_metric = 3
        metric = 5
        metric_high = 16

        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT1, port=DUT1.ports["v1"],
                                                                                  vlan="20",
                                                                                  ip="20.0.0.2", mask="255.255.255.0")

        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["v1"],
                                                                                  vlan="20",
                                                                                  ip="20.0.0.1", mask="255.255.255.0")
        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["h4"],
                                                                                  vlan="15",
                                                                                  ip="15.0.0.1", mask="255.255.255.0")

        rip_flow_.enable_and_advertise_networks(DUT1, "20.0.0.2")
        rip_flow_.enable_and_advertise_networks(DUT2, "20.0.0.1")

        # Changing the metric for redistributed routes

        DUT2.rip.default_metric(metric=metric)

        # Configuring static routes, redistribute static and redistribute connected on DUT2 towards DUT1

        DUT2.ip.add_static_route(network_dest="88.0.0.0", mask_dest="255.255.255.0", next_hop="15.0.0.100")

        DUT2.rip.redistribute_static()
        DUT2.rip.redistribute_connected()

        # Checking if the routes are installed and that are learned via RIP

        time.sleep(30)

        rip_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="R", metric=str(metric + 1))
        rip_flow_.confirm_network_details_in_the_routing_table(DUT1, network="88.0.0.0", protocol="R", metric=str(metric + 1))

        # Changing the metric for redistributed routes

        DUT2.rip.default_metric(metric=metric_high)

        # Remove the redistribution of static/connected and add them back

        DUT2.rip.remove_redistribute_static()
        DUT2.rip.remove_redistribute_connected()

        DUT2.rip.redistribute_static()
        DUT2.rip.redistribute_connected()

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(45)

        rip_flow_.confirm_network_not_in_the_routing_table(DUT1, network="15.0.0.0")
        rip_flow_.confirm_network_not_in_the_routing_table(DUT1, network="88.0.0.0")

        # Remove the default metric

        DUT2.rip.remove_default_metric()

        # Remove the redistribution of static/connected and add them back

        DUT2.rip.remove_redistribute_static()
        DUT2.rip.remove_redistribute_connected()

        DUT2.rip.redistribute_static()
        DUT2.rip.redistribute_connected()

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(45)

        rip_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="R", metric=str(default_metric + 1))
        rip_flow_.confirm_network_details_in_the_routing_table(DUT1, network="88.0.0.0", protocol="R", metric=str(default_metric + 1))

        print("########## Removing the config #############")

        rip_flow_.disable_RIP(DUT1)
        rip_flow_.disable_RIP(DUT2)

        DUT2.ip.remove_static_route(network_dest="88.0.0.0", mask_dest="255.255.255.0", next_hop="15.0.0.100")

        rip_flow_.remove_vlans_and_interfaces_vlan(DUT1, "20")
        rip_flow_.remove_vlans_and_interfaces_vlan(DUT2, "20", "15")

        rip_flow_.shut_interfaces(DUT1, DUT1.ports["v1"])
        rip_flow_.shut_interfaces(DUT2, DUT2.ports["v1"], DUT2.ports["h4"])

    def test_func_9(self):

        print("###### Test_func_9 ######")
        print("########## Verify that the text mode authentication option works as expected. #############")
        print("###### 2 DUTs ######")

        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT1, port=DUT1.ports["v1"],
                                                                                  vlan="20",
                                                                                  ip="20.0.0.2", mask="255.255.255.0")

        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["v1"],
                                                                                  vlan="20",
                                                                                  ip="20.0.0.1", mask="255.255.255.0")
        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["h4"],
                                                                                  vlan="15",
                                                                                  ip="15.0.0.1", mask="255.255.255.0")

        rip_flow_.enable_and_advertise_networks(DUT1, "20.0.0.2")
        rip_flow_.enable_and_advertise_networks(DUT2, "20.0.0.1", "15.0.0.1")

        # Enable authentication key on the int VLAN between the DUTs on DUT2 and shut/no shut the int VLAN between them

        DUT2.rip.add_ip_rip_authentication_mode(int_vlan="20", mode="text", key_chain="12345")

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        # Checking if the routes are not installed

        time.sleep(45)

        rip_flow_.confirm_network_not_in_the_routing_table(DUT1, network="15.0.0.0")
        rip_flow_.confirm_rip_authentication_and_key(DUT1, int_vlan="20", authentication_mode="none")
        rip_flow_.confirm_rip_authentication_and_key(DUT2, int_vlan="20", authentication_mode="simple text")

        # Enable the same authentication key on DUT1 and check that routes are installed

        DUT1.rip.add_ip_rip_authentication_mode(int_vlan="20", mode="text", key_chain="12345")

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(30)

        rip_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="R")
        rip_flow_.confirm_rip_authentication_and_key(DUT1, int_vlan="20", authentication_mode="simple text")
        rip_flow_.confirm_rip_authentication_and_key(DUT2, int_vlan="20", authentication_mode="simple text")

        # Disable the authentication and check that the routes are installed on DUT1

        DUT1.rip.remove_ip_rip_authentication_mode(int_vlan="20")
        DUT2.rip.remove_ip_rip_authentication_mode(int_vlan="20")

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(35)

        rip_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="R")
        rip_flow_.confirm_rip_authentication_and_key(DUT1, int_vlan="20", authentication_mode="none")
        rip_flow_.confirm_rip_authentication_and_key(DUT2, int_vlan="20", authentication_mode="none")

        print("########## Removing the config #############")

        rip_flow_.disable_RIP(DUT1)
        rip_flow_.disable_RIP(DUT2)

        rip_flow_.remove_vlans_and_interfaces_vlan(DUT1, "20")
        rip_flow_.remove_vlans_and_interfaces_vlan(DUT2, "20", "15")

        rip_flow_.shut_interfaces(DUT1, DUT1.ports["v1"])
        rip_flow_.shut_interfaces(DUT2, DUT2.ports["v1"], DUT2.ports["h4"])

    def test_func_10(self):

        print("###### Test_func_10 ######")
        print("########## Verify that md5 Authentication with the authentication type for crypto authentication md5 | sha-1 | sha-256 works as expected.#############")
        print("###### 2 DUTs ######")

        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT1, port=DUT1.ports["v1"],
                                                                                  vlan="20",
                                                                                  ip="20.0.0.2", mask="255.255.255.0")

        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["v1"],
                                                                                  vlan="20",
                                                                                  ip="20.0.0.1", mask="255.255.255.0")
        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["h4"],
                                                                                  vlan="15",
                                                                                  ip="15.0.0.1", mask="255.255.255.0")

        rip_flow_.enable_and_advertise_networks(DUT1, "20.0.0.2")
        rip_flow_.enable_and_advertise_networks(DUT2, "20.0.0.1", "15.0.0.1")

        # Enable authentication key on the int VLAN between the DUTs on DUT2 and shut/no shut the int VLAN between them

        DUT2.rip.add_ip_rip_authentication_mode(int_vlan="20", mode="md5", key_chain="12345")
        DUT2.rip.add_ip_rip_auth_type_mode(int_vlan="20", mode="md5", key_id="1", key="12345")

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        # Checking if the routes are not installed

        time.sleep(45)

        rip_flow_.confirm_network_not_in_the_routing_table(DUT1, network="15.0.0.0")
        rip_flow_.confirm_rip_authentication_and_key(DUT1, int_vlan="20", authentication_mode="none")
        rip_flow_.confirm_rip_authentication_and_key(DUT2, int_vlan="20", authentication_mode="md5")

        # Enable the same authentication key on DUT1 and check that routes are installed

        DUT1.rip.add_ip_rip_authentication_mode(int_vlan="20", mode="md5", key_chain="12345")
        DUT1.rip.add_ip_rip_auth_type_mode(int_vlan="20", mode="md5", key_id="1", key="12345")

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(30)

        rip_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="R")
        rip_flow_.confirm_rip_authentication_and_key(DUT1, int_vlan="20", authentication_mode="md5", key_id="1")
        rip_flow_.confirm_rip_authentication_and_key(DUT2, int_vlan="20", authentication_mode="md5", key_id="1")

        # Disable the authentication and check that the routes are installed on DUT1

        DUT1.rip.remove_ip_rip_authentication_mode(int_vlan="20")
        DUT2.rip.remove_ip_rip_authentication_mode(int_vlan="20")

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(35)

        rip_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="R")
        rip_flow_.confirm_rip_authentication_and_key(DUT1, int_vlan="20", authentication_mode="none")
        rip_flow_.confirm_rip_authentication_and_key(DUT2, int_vlan="20", authentication_mode="none")

        print("########## Removing the config #############")

        rip_flow_.disable_RIP(DUT1)
        rip_flow_.disable_RIP(DUT2)

        rip_flow_.remove_vlans_and_interfaces_vlan(DUT1, "20")
        rip_flow_.remove_vlans_and_interfaces_vlan(DUT2, "20", "15")

        rip_flow_.shut_interfaces(DUT1, DUT1.ports["v1"])
        rip_flow_.shut_interfaces(DUT2, DUT2.ports["v1"], DUT2.ports["h4"])

    def test_func_11(self):

        print("###### Test_func_11 ######")
        print("########## Verify that sha-1 Authentication with the authentication type for crypto authentication sha-1 works as expected.#############")
        print("###### 2 DUTs ######")

        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT1, port=DUT1.ports["v1"],
                                                                                  vlan="20",
                                                                                  ip="20.0.0.2", mask="255.255.255.0")

        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["v1"],
                                                                                  vlan="20",
                                                                                  ip="20.0.0.1", mask="255.255.255.0")
        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["h4"],
                                                                                  vlan="15",
                                                                                  ip="15.0.0.1", mask="255.255.255.0")

        rip_flow_.enable_and_advertise_networks(DUT1, "20.0.0.2")
        rip_flow_.enable_and_advertise_networks(DUT2, "20.0.0.1", "15.0.0.1")

        # Enable authentication key on the int VLAN between the DUTs on DUT2 and shut/no shut the int VLAN between them

        DUT2.rip.add_ip_rip_auth_type_mode(int_vlan="20", mode="sha-1", key_id="1", key="12345")

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        # Checking if the routes are not installed

        time.sleep(45)

        rip_flow_.confirm_network_not_in_the_routing_table(DUT1, network="15.0.0.0")
        rip_flow_.confirm_rip_authentication_and_key(DUT1, int_vlan="20", authentication_mode="none")
        rip_flow_.confirm_rip_authentication_and_key(DUT2, int_vlan="20", authentication_mode="sha1")

        # Enable the same authentication key on DUT1 and check that routes are installed

        DUT1.rip.add_ip_rip_auth_type_mode(int_vlan="20", mode="sha-1", key_id="1", key="12345")

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(30)

        rip_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="R")
        rip_flow_.confirm_rip_authentication_and_key(DUT1, int_vlan="20", authentication_mode="sha1", key_id="1")
        rip_flow_.confirm_rip_authentication_and_key(DUT2, int_vlan="20", authentication_mode="sha1", key_id="1")

        # Disable the authentication and check that the routes are installed on DUT1

        DUT1.rip.remove_ip_rip_authentication_mode(int_vlan="20")
        DUT2.rip.remove_ip_rip_authentication_mode(int_vlan="20")

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(35)

        rip_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="R")
        rip_flow_.confirm_rip_authentication_and_key(DUT1, int_vlan="20", authentication_mode="none")
        rip_flow_.confirm_rip_authentication_and_key(DUT2, int_vlan="20", authentication_mode="none")

        print("########## Removing the config #############")

        rip_flow_.disable_RIP(DUT1)
        rip_flow_.disable_RIP(DUT2)

        rip_flow_.remove_vlans_and_interfaces_vlan(DUT1, "20")
        rip_flow_.remove_vlans_and_interfaces_vlan(DUT2, "20", "15")

        rip_flow_.shut_interfaces(DUT1, DUT1.ports["v1"])
        rip_flow_.shut_interfaces(DUT2, DUT2.ports["v1"], DUT2.ports["h4"])

    def test_func_12(self):

        print("###### Test_func_12 ######")
        print("########## Verify that sha-256 Authentication with the authentication type for crypto authentication sha-256 works as expected.#############")
        print("###### 2 DUTs ######")

        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT1, port=DUT1.ports["v1"],
                                                                                  vlan="20",
                                                                                  ip="20.0.0.2", mask="255.255.255.0")

        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["v1"],
                                                                                  vlan="20",
                                                                                  ip="20.0.0.1", mask="255.255.255.0")
        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["h4"],
                                                                                  vlan="15",
                                                                                  ip="15.0.0.1", mask="255.255.255.0")

        rip_flow_.enable_and_advertise_networks(DUT1, "20.0.0.2")
        rip_flow_.enable_and_advertise_networks(DUT2, "20.0.0.1", "15.0.0.1")

        # Enable authentication key on the int VLAN between the DUTs on DUT2 and shut/no shut the int VLAN between them

        DUT2.rip.add_ip_rip_auth_type_mode(int_vlan="20", mode="sha-256", key_id="1", key="12345")

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        # Checking if the routes are not installed

        time.sleep(45)

        rip_flow_.confirm_network_not_in_the_routing_table(DUT1, network="15.0.0.0")
        rip_flow_.confirm_rip_authentication_and_key(DUT1, int_vlan="20", authentication_mode="none")
        rip_flow_.confirm_rip_authentication_and_key(DUT2, int_vlan="20", authentication_mode="sha256")

        # Enable the same authentication key on DUT1 and check that routes are installed

        DUT1.rip.add_ip_rip_auth_type_mode(int_vlan="20", mode="sha-256", key_id="1", key="12345")

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(30)

        rip_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="R")
        rip_flow_.confirm_rip_authentication_and_key(DUT1, int_vlan="20", authentication_mode="sha256", key_id="1")
        rip_flow_.confirm_rip_authentication_and_key(DUT2, int_vlan="20", authentication_mode="sha256", key_id="1")

        # Disable the authentication and check that the routes are installed on DUT1

        DUT1.rip.remove_ip_rip_authentication_mode(int_vlan="20")
        DUT2.rip.remove_ip_rip_authentication_mode(int_vlan="20")

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(35)

        rip_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="R")
        rip_flow_.confirm_rip_authentication_and_key(DUT1, int_vlan="20", authentication_mode="none")
        rip_flow_.confirm_rip_authentication_and_key(DUT2, int_vlan="20", authentication_mode="none")

        print("########## Removing the config #############")

        rip_flow_.disable_RIP(DUT1)
        rip_flow_.disable_RIP(DUT2)

        rip_flow_.remove_vlans_and_interfaces_vlan(DUT1, "20")
        rip_flow_.remove_vlans_and_interfaces_vlan(DUT2, "20", "15")

        rip_flow_.shut_interfaces(DUT1, DUT1.ports["v1"])
        rip_flow_.shut_interfaces(DUT2, DUT2.ports["v1"], DUT2.ports["h4"])

    def test_func_13(self):

        print("###### Test_func_13 ######")
        print("########## Verify that multiple authentication keys can be configured on a DUT.#############")
        print("###### 2 DUTs ######")

        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT1, port=DUT1.ports["v1"],
                                                                                  vlan="20",
                                                                                  ip="20.0.0.2", mask="255.255.255.0")

        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["v1"],
                                                                                  vlan="20",
                                                                                  ip="20.0.0.1", mask="255.255.255.0")
        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["h4"],
                                                                                  vlan="15",
                                                                                  ip="15.0.0.1", mask="255.255.255.0")

        rip_flow_.enable_and_advertise_networks(DUT1, "20.0.0.2")
        rip_flow_.enable_and_advertise_networks(DUT2, "20.0.0.1", "15.0.0.1")

        # Enable authentication key on the int VLAN between the DUTs on DUT2 and shut/no shut the int VLAN between them

        DUT2.rip.add_ip_rip_auth_type_mode(int_vlan="20", mode="md5", key_id="1", key="12345")
        DUT2.rip.add_ip_rip_auth_type_mode(int_vlan="20", mode="md5", key_id="2", key="123456")

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        # Checking if the routes are not installed

        time.sleep(45)

        rip_flow_.confirm_network_not_in_the_routing_table(DUT1, network="15.0.0.0")
        rip_flow_.confirm_rip_authentication_and_key(DUT1, int_vlan="20", authentication_mode="none")
        rip_flow_.confirm_rip_authentication_and_key(DUT2, int_vlan="20", authentication_mode="md5")

        # Enable the same authentication key on DUT1 and check that routes are installed

        DUT1.rip.add_ip_rip_auth_type_mode(int_vlan="20", mode="md5", key_id="1", key="12345")
        DUT1.rip.add_ip_rip_auth_type_mode(int_vlan="20", mode="md5", key_id="2", key="123456")

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(30)

        rip_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="R")
        rip_flow_.confirm_rip_authentication_and_key(DUT1, int_vlan="20", authentication_mode="md5", key_id="2")
        rip_flow_.confirm_rip_authentication_and_key(DUT2, int_vlan="20", authentication_mode="md5", key_id="2")

        # Disable the last authentication key on both DUTs and check that the routes are installed on DUT1 with key-id 1

        DUT1.rip.remove_ip_rip_authentication_key(int_vlan="20", key_id="2")
        DUT2.rip.remove_ip_rip_authentication_key(int_vlan="20", key_id="2")

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(35)

        rip_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="R")
        rip_flow_.confirm_rip_authentication_and_key(DUT1, int_vlan="20", authentication_mode="md5", key_id="1")
        rip_flow_.confirm_rip_authentication_and_key(DUT2, int_vlan="20", authentication_mode="md5", key_id="1")

        # Remove the authentication on both DUTs and check that the routes are installed

        DUT1.rip.remove_ip_rip_authentication_mode(int_vlan="20")
        DUT2.rip.remove_ip_rip_authentication_mode(int_vlan="20")

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(35)

        rip_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="R")
        rip_flow_.confirm_rip_authentication_and_key(DUT1, int_vlan="20", authentication_mode="none")
        rip_flow_.confirm_rip_authentication_and_key(DUT2, int_vlan="20", authentication_mode="none")

        print("########## Removing the config #############")

        rip_flow_.disable_RIP(DUT1)
        rip_flow_.disable_RIP(DUT2)

        rip_flow_.remove_vlans_and_interfaces_vlan(DUT1, "20")
        rip_flow_.remove_vlans_and_interfaces_vlan(DUT2, "20", "15")

        rip_flow_.shut_interfaces(DUT1, DUT1.ports["v1"])
        rip_flow_.shut_interfaces(DUT2, DUT2.ports["v1"], DUT2.ports["h4"])

    def test_func_14(self):

        print("###### Test_func_14 ######")
        print("########## Check if we can advertise networks into RIP and it establish connection using int vlans.#############")
        print("###### 2 DUTs ######")

        #       Topology
        #
        #         RIP
        #
        # -- DUT1 ---- DUT2
        #       \      /
        #        \    /
        #         DUT3
        #

        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT1, port=DUT1.ports["v1"], vlan="20",
                                                                                  ip="20.0.0.2", mask="255.255.255.0")
        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT1, port=DUT1.ports["x1"], vlan="40",
                                                                                  ip="40.0.0.1", mask="255.255.255.0")
        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT1, port=DUT1.ports["h3"], vlan="15",
                                                                                  ip="15.0.0.1", mask="255.255.255.0")

        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["h2"], vlan="30",
                                                                                  ip="30.0.0.1", mask="255.255.255.0")
        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["v1"], vlan="20",
                                                                                  ip="20.0.0.1", mask="255.255.255.0")

        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT3, port=DUT3.ports["h2"], vlan="30",
                                                                                  ip="30.0.0.2", mask="255.255.255.0")
        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT3, port=DUT3.ports["x1"], vlan="40",
                                                                                  ip="40.0.0.2", mask="255.255.255.0")

        rip_flow_.enable_and_advertise_networks(DUT1, "15.0.0.1", "20.0.0.2", "40.0.0.1")
        rip_flow_.enable_and_advertise_networks(DUT2, "30.0.0.1", "20.0.0.1")
        rip_flow_.enable_and_advertise_networks(DUT3, "30.0.0.2", "40.0.0.2")

        time.sleep(45)

        rip_flow_.confirm_network_details_in_the_routing_table(DUT2, network="15.0.0.0", protocol="R")
        rip_flow_.confirm_network_details_in_the_routing_table(DUT2, network="40.0.0.0", protocol="R")

        # Shut one port on DUT1 and check that RIP routes are not missing

        DUT1.int.shut_interface(interface=DUT1.ports["v1"])

        time.sleep(45)

        rip_flow_.confirm_network_details_in_the_routing_table(DUT2, network="15.0.0.0", protocol="R")
        rip_flow_.confirm_network_details_in_the_routing_table(DUT2, network="40.0.0.0", protocol="R")

        # No shut the port on DUT1 and check that RIP routes are not missing

        DUT1.int.no_shut_interface(interface=DUT1.ports["v1"])

        time.sleep(45)

        rip_flow_.confirm_network_details_in_the_routing_table(DUT2, network="15.0.0.0", protocol="R")
        rip_flow_.confirm_network_details_in_the_routing_table(DUT2, network="40.0.0.0", protocol="R")

        print("########## Removing the config #############")

        rip_flow_.disable_RIP(DUT1)
        rip_flow_.disable_RIP(DUT2)
        rip_flow_.disable_RIP(DUT3)

        rip_flow_.remove_vlans_and_interfaces_vlan(DUT1, "15", "20", "40")
        rip_flow_.remove_vlans_and_interfaces_vlan(DUT2, "20", "30")
        rip_flow_.remove_vlans_and_interfaces_vlan(DUT3, "30", "40")

        rip_flow_.shut_interfaces(DUT1, DUT1.ports["v1"], DUT1.ports["x1"], DUT1.ports["h3"])
        rip_flow_.shut_interfaces(DUT2, DUT2.ports["v1"], DUT2.ports["h2"])
        rip_flow_.shut_interfaces(DUT3, DUT3.ports["x1"], DUT3.ports["h2"])



    def test_func_15(self):

        # LOKI-4876 - Missing routes with Routed Ports

        print("###### Test_func_15 ######")
        print("########## Check if we can advertise networks into RIP and it establish connection using routed ports #############")
        print("###### 3 DUTs ######")

        #       Topology
        #
        #         RIP
        #
        # -- DUT1 ---- DUT2
        #       \      /
        #        \    /
        #         DUT3


        rip_flow_.create_routed_port_and_add_ip(DUT1, interface=DUT1.ports["v1"], ip="20.0.0.2", mask="255.255.255.0")
        rip_flow_.create_routed_port_and_add_ip(DUT1, interface=DUT1.ports["x1"], ip="40.0.0.1", mask="255.255.255.0")

        rip_flow_.create_routed_port_and_add_ip(DUT3, interface=DUT3.ports["h2"], ip="30.0.0.2", mask="255.255.255.0")
        rip_flow_.create_routed_port_and_add_ip(DUT3, interface=DUT3.ports["x1"], ip="40.0.0.2", mask="255.255.255.0")

        rip_flow_.create_routed_port_and_add_ip(DUT2, interface=DUT2.ports["h2"], ip="30.0.0.1", mask="255.255.255.0")
        rip_flow_.create_routed_port_and_add_ip(DUT2, interface=DUT2.ports["v1"], ip="20.0.0.1", mask="255.255.255.0")

        rip_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT1, port=DUT1.ports["h3"], vlan="15",
                                                                                   ip="15.0.0.1", mask="255.255.255.0")

        rip_flow_.enable_and_advertise_networks(DUT1, "15.0.0.1", "20.0.0.2", "40.0.0.1")
        rip_flow_.enable_and_advertise_networks(DUT3, "30.0.0.2", "40.0.0.2")
        rip_flow_.enable_and_advertise_networks(DUT2, "30.0.0.1", "20.0.0.1")

        time.sleep(45)

        rip_flow_.confirm_network_details_in_the_routing_table(DUT2, network="15.0.0.0", protocol="R")
        rip_flow_.confirm_network_details_in_the_routing_table(DUT2, network="40.0.0.0", protocol="R")

        # Shut one port on DUT1 and check that RIP routes are not missing

        DUT1.int.shut_interface(interface=DUT1.ports["v1"])

        time.sleep(45)

        rip_flow_.confirm_network_details_in_the_routing_table(DUT2, network="15.0.0.0", protocol="R")
        rip_flow_.confirm_network_details_in_the_routing_table(DUT2, network="40.0.0.0", protocol="R")

        # No shut the port on DUT1 and check that RIP routes are not missing

        DUT1.int.no_shut_interface(interface=DUT1.ports["v1"])

        time.sleep(45)

        rip_flow_.confirm_network_details_in_the_routing_table(DUT2, network="15.0.0.0", protocol="R")
        rip_flow_.confirm_network_details_in_the_routing_table(DUT2, network="40.0.0.0", protocol="R")

        print("########## Removing the config #############")

        rip_flow_.disable_RIP(DUT1)
        rip_flow_.disable_RIP(DUT2)
        rip_flow_.disable_RIP(DUT3)

        rip_flow_.remove_vlans_and_interfaces_vlan(DUT1, "15")

        rip_flow_.remove_routed_port(DUT1, DUT1.ports["v1"], DUT1.ports["x1"])
        rip_flow_.remove_routed_port(DUT3, DUT3.ports["h2"], DUT3.ports["x1"])
        rip_flow_.remove_routed_port(DUT2, DUT2.ports["h2"], DUT2.ports["v1"])

        rip_flow_.shut_interfaces(DUT1, DUT1.ports["h3"])