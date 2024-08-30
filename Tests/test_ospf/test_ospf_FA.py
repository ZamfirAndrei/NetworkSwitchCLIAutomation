import time
import pytest
import pytest_html
import sys

from Management import dut_objects
from test_beds import test_bed_1
from flows import ospf_flow

dut6 = test_bed_1.DUT6
dut4 = test_bed_1.DUT4
dut5 = test_bed_1.DUT5

DUT6 = dut_objects.DUT_Objects_TestBed(dut6)
DUT4 = dut_objects.DUT_Objects_TestBed(dut4)
DUT5 = dut_objects.DUT_Objects_TestBed(dut5)

ospf_flow_ = ospf_flow.OSPFflow()

class TestOSPFFASuite1:

    def test_func_1(self):

        print("###### Test_func_1 ######")
        print("########## Verify if Connected routes are redistributed into OSPF #############")
        print("###### 2 DUTs ######")

        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT4, port=DUT4.ports["v4"], vlan="20",
                                                                      ip="20.0.0.2", mask="255.255.255.0")

        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT6, port=DUT6.ports["v3"], vlan="20",
                                                                      ip="20.0.0.1", mask="255.255.255.0")
        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT6, port=DUT6.ports["v1"], vlan="15",
                                                                      ip="15.0.0.1", mask="255.255.255.0")
        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT6, port=DUT6.ports["v1"], vlan="99",
                                                                      ip="99.0.0.1", mask="255.255.255.0")
        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT6, port=DUT6.ports["v1"], vlan="100",
                                                                      ip="100.0.0.1", mask="255.255.255.0")

        ospf_flow_.enable_and_advertise_networks(DUT4, int_vlan20=["20.0.0.2","0.0.0.0"])
        ospf_flow_.enable_and_advertise_networks(DUT6, int_vlan20=["20.0.0.1","0.0.0.0"], int_vlan99=["99.0.0.1","0.0.0.0"])

        # Redistributing the connected networks on DUT6 and installing them on DUT4

        DUT6.ospf.redistribute_connected()

        time.sleep(45)

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT4, network="15.0.0.0", protocol="O E", metric_type="2")
        ospf_flow_.confirm_network_details_in_the_routing_table(DUT4, network="99.0.0.0", protocol="O")
        ospf_flow_.confirm_network_details_in_the_routing_table(DUT4, network="100.0.0.0", protocol="O E", metric_type="2")

        # Add another connected route

        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT6, port=DUT6.ports["v1"], vlan="60", ip="60.0.0.1", mask="255.255.255.0")

        time.sleep(5)

        # Check if the new route is learned

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT4, network="60.0.0.0", protocol="O E",metric_type="2")

        # Remove redistribution on DUT6 and check if the connected routes are not anymore in the routing table of DUT4

        DUT6.ospf.remove_redistribute_connected()

        DUT4.ip.shut_int_vlan(int_vlan="20")
        DUT4.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(45)

        ospf_flow_.confirm_network_not_in_the_routing_table(DUT4, network="15.0.0.0")
        ospf_flow_.confirm_network_not_in_the_routing_table(DUT4, network="100.0.0.0")
        ospf_flow_.confirm_network_not_in_the_routing_table(DUT4, network="60.0.0.0")
        ospf_flow_.confirm_network_details_in_the_routing_table(DUT4, network="99.0.0.0", protocol="O")

        print("########## Removing the config #############")

        ospf_flow_.remove_networks(DUT4, int_vlan20=["20.0.0.2", "0.0.0.0"])
        ospf_flow_.remove_networks(DUT6, int_vlan20=["20.0.0.1", "0.0.0.0"], int_vlan99=["99.0.0.1", "0.0.0.0"])

        ospf_flow_.disable_OSPF(DUT4)
        ospf_flow_.disable_OSPF(DUT6)

        ospf_flow_.remove_vlans_and_interfaces_vlan(DUT4, "20")
        ospf_flow_.remove_vlans_and_interfaces_vlan(DUT6, "20", "99", "15", "100", "60")

        ospf_flow_.shut_interfaces(DUT4, DUT4.ports["v4"])
        ospf_flow_.shut_interfaces(DUT6, DUT6.ports["v3"], DUT6.ports["v1"])
    
    def test_func_2(self):

        print("###### Test_func_2 ######")
        print("########## Verify if Static routes are redistributed into OSPF #############")
        print("###### 2 DUTs ######")

        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT4, port=DUT4.ports["v4"], vlan="20",
                                                                                   ip="20.0.0.2", mask="255.255.255.0")

        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT6, port=DUT6.ports["v3"], vlan="20",
                                                                                   ip="20.0.0.1", mask="255.255.255.0")
        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT6, port=DUT6.ports["v1"], vlan="99",
                                                                                  ip="99.0.0.1", mask="255.255.255.0")

        ospf_flow_.enable_and_advertise_networks(DUT4, int_vlan20=["20.0.0.2", "0.0.0.0"])
        ospf_flow_.enable_and_advertise_networks(DUT6, int_vlan20=["20.0.0.1", "0.0.0.0"], int_vlan99=["99.0.0.1", "0.0.0.0"])

        # Creating a static route

        DUT6.ip.add_static_route(network_dest="100.0.0.0", mask_dest="255.255.0.0", next_hop="99.0.0.100")

        # Redistributing the static network on DUT6 and installing it on DUT4

        DUT6.ospf.redistribute_static()

        time.sleep(45)

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT4, network="99.0.0.0", protocol="O")
        ospf_flow_.confirm_network_details_in_the_routing_table(DUT4, network="100.0.0.0", protocol="O E",metric_type="2")

        # Add another static route

        DUT6.ip.add_static_route(network_dest="77.0.0.0", mask_dest="255.255.0.0", next_hop="99.0.0.100")

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT4, network="99.0.0.0", protocol="O")
        ospf_flow_.confirm_network_details_in_the_routing_table(DUT4, network="100.0.0.0", protocol="O E",metric_type="2")
        ospf_flow_.confirm_network_details_in_the_routing_table(DUT4, network="77.0.0.0", protocol="O E", metric_type="2")

        # Remove the static route on DUT6 and check if the route is not anymore in the routing table of DUT4

        DUT6.ospf.remove_redistribute_static()

        DUT4.ip.shut_int_vlan(int_vlan="20")
        DUT4.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(45)

        ospf_flow_.confirm_network_not_in_the_routing_table(DUT4, network="100.0.0.0")
        ospf_flow_.confirm_network_not_in_the_routing_table(DUT4, network="77.0.0.0")
        ospf_flow_.confirm_network_details_in_the_routing_table(DUT4, network="99.0.0.0", protocol="O")

        print("########## Removing the config #############")

        DUT6.ip.remove_static_route(network_dest="100.0.0.0", mask_dest="255.255.0.0", next_hop="99.0.0.100")
        DUT6.ip.remove_static_route(network_dest="77.0.0.0", mask_dest="255.255.0.0", next_hop="99.0.0.100")

        ospf_flow_.remove_networks(DUT4, int_vlan20=["20.0.0.2", "0.0.0.0"])
        ospf_flow_.remove_networks(DUT6, int_vlan20=["20.0.0.1", "0.0.0.0"], int_vlan99=["99.0.0.1", "0.0.0.0"])

        ospf_flow_.disable_OSPF(DUT4)
        ospf_flow_.disable_OSPF(DUT6)

        ospf_flow_.remove_vlans_and_interfaces_vlan(DUT4, "20")
        ospf_flow_.remove_vlans_and_interfaces_vlan(DUT6, "20", "99")

        ospf_flow_.shut_interfaces(DUT4, DUT4.ports["v4"])
        ospf_flow_.shut_interfaces(DUT6, DUT6.ports["v3"], DUT6.ports["v1"])
    
    def test_func_3(self):

        print("###### Test_func_3 ######")
        print("########## Verify if a custom metric can be configured on routes redistributed into OSPF #############")
        print("###### 2 DUTs ######")

        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT4, port=DUT4.ports["v4"],  vlan="20",
                                                                                   ip="20.0.0.2", mask="255.255.255.0")

        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT6, port=DUT6.ports["v3"], vlan="20",
                                                                                   ip="20.0.0.1", mask="255.255.255.0")
        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT6, port=DUT6.ports["v1"],vlan="99",
                                                                                   ip="99.0.0.1", mask="255.255.255.0")
        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT6, port=DUT6.ports["v1"],vlan="60",
                                                                                   ip="60.0.0.1", mask="255.255.255.0")

        ospf_flow_.enable_and_advertise_networks(DUT4, int_vlan20=["20.0.0.2", "0.0.0.0"])
        ospf_flow_.enable_and_advertise_networks(DUT6, int_vlan20=["20.0.0.1", "0.0.0.0"], int_vlan99=["99.0.0.1", "0.0.0.0"])

        # Creating a static route

        DUT6.ip.add_static_route(network_dest="100.0.0.0", mask_dest="255.255.0.0", next_hop="99.0.0.100")

        # Redistributing the static network on DUT6 and installing it on DUT4

        DUT6.ospf.redistribute_static()

        # Redistributing connected routes on DUT6 and installing it on DUT4

        DUT6.ospf.redistribute_connected()

        time.sleep(45)

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT4, network="99.0.0.0", protocol="O")
        ospf_flow_.confirm_network_details_in_the_routing_table(DUT4, network="60.0.0.0", protocol="O E", metric_type="2", metric="10")
        ospf_flow_.confirm_network_details_in_the_routing_table(DUT4, network="100.0.0.0", protocol="O E", metric_type="2",  metric="10")

        # Redistribute with different metric

        DUT6.ospf.remove_redistribute_static()
        DUT6.ospf.redistribute_static(metric="500")

        # Redistribute with different metric

        DUT6.ospf.remove_redistribute_connected()
        DUT6.ospf.redistribute_connected(metric="500")

        time.sleep(5)

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT4, network="99.0.0.0", protocol="O")
        ospf_flow_.confirm_network_details_in_the_routing_table(DUT4, network="60.0.0.0", protocol="O E", metric_type="2", metric="500")
        ospf_flow_.confirm_network_details_in_the_routing_table(DUT4, network="100.0.0.0", protocol="O E", metric_type="2", metric="500")

        # Remove redistribution on DUT6 and check if the connected/static routes are not anymore in the routing table of DUT4

        DUT6.ospf.remove_redistribute_static()
        DUT6.ospf.remove_redistribute_connected()

        time.sleep(5)

        ospf_flow_.confirm_network_not_in_the_routing_table(DUT4, network="100.0.0.0")
        ospf_flow_.confirm_network_not_in_the_routing_table(DUT4, network="77.0.0.0")
        ospf_flow_.confirm_network_details_in_the_routing_table(DUT4, network="99.0.0.0", protocol="O")

        print("########## Removing the config #############")

        DUT6.ip.remove_static_route(network_dest="100.0.0.0", mask_dest="255.255.0.0", next_hop="99.0.0.100")

        ospf_flow_.remove_networks(DUT4, int_vlan20=["20.0.0.2", "0.0.0.0"])
        ospf_flow_.remove_networks(DUT6, int_vlan20=["20.0.0.1", "0.0.0.0"], int_vlan99=["99.0.0.1", "0.0.0.0"])

        ospf_flow_.disable_OSPF(DUT4)
        ospf_flow_.disable_OSPF(DUT6)

        ospf_flow_.remove_vlans_and_interfaces_vlan(DUT4, "20")
        ospf_flow_.remove_vlans_and_interfaces_vlan(DUT6, "20", "99", "60")

        ospf_flow_.shut_interfaces(DUT4, DUT4.ports["v4"])
        ospf_flow_.shut_interfaces(DUT6, DUT6.ports["v3"], DUT6.ports["v1"])

    def test_func_100(self):

        # LOKI-4711 Customer - OSPF route is missing after fail over on router port

        print("###### Test_func_100 ######")
        print("########## Check if we can advertise networks into OSPF and it establish connection using routed ports  #############")
        print("###### 3 DUTs ######")

        #       Topology
        #
        #        Area 0
        #
        # -- DUT4 ---- DUT5
        #       \      /
        #        \    /
        #         DUT6 (FA)
        #

        ospf_flow_.create_routed_port_and_add_ip(DUT4, interface=DUT4.ports["v4"], ip="20.0.0.2", mask="255.255.255.0")
        ospf_flow_.create_routed_port_and_add_ip(DUT4, interface=DUT4.ports["v6"], ip="40.0.0.1", mask="255.255.255.0")

        ospf_flow_.create_routed_port_and_add_ip(DUT5, interface=DUT5.ports["x1"], ip="30.0.0.2", mask="255.255.255.0")
        ospf_flow_.create_routed_port_and_add_ip(DUT5, interface=DUT5.ports["v4"], ip="40.0.0.2", mask="255.255.255.0")

        ospf_flow_.create_routed_port_and_add_ip(DUT6, interface=DUT6.ports["x1"], ip="30.0.0.1", mask="255.255.255.0")
        ospf_flow_.create_routed_port_and_add_ip(DUT6, interface=DUT6.ports["v3"], ip="20.0.0.1", mask="255.255.255.0")

        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT4, port=DUT4.ports["v1"],  vlan="15",
                                                                                   ip="15.0.0.1", mask="255.255.255.0")

        ospf_flow_.enable_and_advertise_networks(DUT4, int_vlan15=["15.0.0.1", "0.0.0.0"], interface1=["20.0.0.2", "0.0.0.0"], interface2=["40.0.0.1", "0.0.0.0"])
        ospf_flow_.enable_and_advertise_networks(DUT5, interface1=["30.0.0.2", "0.0.0.0"], interface2=["40.0.0.2", "0.0.0.0"])
        ospf_flow_.enable_and_advertise_networks(DUT6, interface1=["30.0.0.1", "0.0.0.0"], interface2=["20.0.0.1", "0.0.0.0"])

        time.sleep(45)

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT6, network="15.0.0.0", protocol="O")
        ospf_flow_.confirm_network_details_in_the_routing_table(DUT6, network="40.0.0.0", protocol="O")

        # Shut one port on DUT1 and check that RIP routes are not missing

        DUT6.int.shut_interface(interface=DUT6.ports["x1"])

        time.sleep(45)

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT6, network="15.0.0.0", protocol="O")
        ospf_flow_.confirm_network_details_in_the_routing_table(DUT6, network="40.0.0.0", protocol="O")

        # No shut the port on DUT6 and check that OSPF routes are not missing

        DUT6.int.no_shut_interface(interface=DUT6.ports["x1"])

        time.sleep(45)

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT6, network="15.0.0.0", protocol="O")
        ospf_flow_.confirm_network_details_in_the_routing_table(DUT6, network="40.0.0.0", protocol="O")

        print("########## Removing the config #############")

        ospf_flow_.remove_networks(DUT4,  int_vlan15=["15.0.0.1", "0.0.0.0"], interface1=["20.0.0.2", "0.0.0.0"], interface2=["40.0.0.1", "0.0.0.0"])
        ospf_flow_.remove_networks(DUT5, interface1=["30.0.0.2", "0.0.0.0"], interface2=["40.0.0.2", "0.0.0.0"])
        ospf_flow_.remove_networks(DUT6, interface1=["30.0.0.1", "0.0.0.0"], interface2=["20.0.0.1", "0.0.0.0"])

        ospf_flow_.disable_OSPF(DUT4)
        ospf_flow_.disable_OSPF(DUT5)
        ospf_flow_.disable_OSPF(DUT6)

        ospf_flow_.remove_vlans_and_interfaces_vlan(DUT4, "15")

        ospf_flow_.remove_routed_port(DUT4, DUT4.ports["v4"], DUT4.ports["v6"])
        ospf_flow_.remove_routed_port(DUT5, DUT5.ports["v4"], DUT5.ports["x1"])
        ospf_flow_.remove_routed_port(DUT6, DUT6.ports["v3"], DUT6.ports["x1"])

        ospf_flow_.shut_interfaces(DUT4, DUT4.ports["v1"])

