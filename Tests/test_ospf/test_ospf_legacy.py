import time
import pytest
import pytest_html
import sys

from Management import dut_objects
from test_beds import test_bed_1
from flows import ospf_flow, rip_flow

DUT2 = test_bed_1.DUT2
DUT1 = test_bed_1.DUT1
DUT3 = test_bed_1.DUT3

DUT2 = dut_objects.DUT_Objects_TestBed(DUT2)
DUT1 = dut_objects.DUT_Objects_TestBed(DUT1)
DUT3 = dut_objects.DUT_Objects_TestBed(DUT3)

ospf_flow_ = ospf_flow.OSPFflow()
rip_flow_ = rip_flow.RIPflow()


class TestOSPFLegacy:

    def test_func_1(self):

        print("###### Test_func_1 ######")
        print("########## Verify if Connected routes are redistributed into OSPF #############")
        print("###### 2 DUTs ######")

        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT1, port=DUT1.ports["v1"],vlan="20",
                                                                                   ip="20.0.0.2", mask="255.255.255.0")

        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["v1"],vlan="20",
                                                                                   ip="20.0.0.1", mask="255.255.255.0")
        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["h4"],vlan="15",
                                                                                   ip="15.0.0.1", mask="255.255.255.0")
        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["h4"],vlan="99",
                                                                                   ip="99.0.0.1", mask="255.255.255.0")
        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["h4"],vlan="100",
                                                                                   ip="100.0.0.1", mask="255.255.255.0")

        ospf_flow_.enable_and_advertise_networks(DUT1, int_vlan20=["20.0.0.2", "0.0.0.0"])
        ospf_flow_.enable_and_advertise_networks(DUT2, int_vlan20=["20.0.0.1", "0.0.0.0"],
                                                 int_vlan99=["99.0.0.1", "0.0.0.0"])

        # Redistributing the connected networks on DUT2 and installing them on DUT1

        DUT2.ospf.redistribute_connected()

        time.sleep(45)

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="O E",
                                                                metric_type="2")
        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="99.0.0.0", protocol="O")
        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="100.0.0.0", protocol="O E",
                                                                metric_type="2")

        # Add another connected route

        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["h4"],
                                                                                   vlan="60", ip="60.0.0.1",
                                                                                   mask="255.255.255.0")

        time.sleep(5)

        # Check if the new route is learned

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="60.0.0.0", protocol="O E",
                                                                metric_type="2")

        # Remove redistribution on DUT2 and check if the connected routes are not anymore in the routing table of DUT1

        DUT2.ospf.remove_redistribute_connected()

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(45)

        ospf_flow_.confirm_network_not_in_the_routing_table(DUT1, network="15.0.0.0")
        ospf_flow_.confirm_network_not_in_the_routing_table(DUT1, network="100.0.0.0")
        ospf_flow_.confirm_network_not_in_the_routing_table(DUT1, network="60.0.0.0")
        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="99.0.0.0", protocol="O")

        print("########## Removing the config #############")

        ospf_flow_.remove_networks(DUT1, int_vlan20=["20.0.0.2", "0.0.0.0"])
        ospf_flow_.remove_networks(DUT2, int_vlan20=["20.0.0.1", "0.0.0.0"], int_vlan99=["99.0.0.1", "0.0.0.0"])

        ospf_flow_.disable_OSPF(DUT1)
        ospf_flow_.disable_OSPF(DUT2)

        ospf_flow_.remove_vlans_and_interfaces_vlan(DUT1, "20")
        ospf_flow_.remove_vlans_and_interfaces_vlan(DUT2, "20", "99", "15", "100", "60")

        ospf_flow_.shut_interfaces(DUT1, DUT1.ports["v1"])
        ospf_flow_.shut_interfaces(DUT2, DUT2.ports["v1"], DUT2.ports["h4"])

    def test_func_2(self):

        print("###### Test_func_2 ######")
        print("########## Verify if Static routes are redistributed into OSPF #############")
        print("###### 2 DUTs ######")

        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT1, port=DUT1.ports["v1"],vlan="20",
                                                                                   ip="20.0.0.2", mask="255.255.255.0")

        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["v1"],vlan="20",
                                                                                   ip="20.0.0.1", mask="255.255.255.0")
        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["h4"],vlan="99",
                                                                                   ip="99.0.0.1", mask="255.255.255.0")

        ospf_flow_.enable_and_advertise_networks(DUT1, int_vlan20=["20.0.0.2", "0.0.0.0"])
        ospf_flow_.enable_and_advertise_networks(DUT2, int_vlan20=["20.0.0.1", "0.0.0.0"], int_vlan99=["99.0.0.1", "0.0.0.0"])

        # Creating a static route

        DUT2.ip.add_static_route(network_dest="100.0.0.0", mask_dest="255.255.0.0", next_hop="99.0.0.100")

        # Redistributing the static network on DUT2 and installing it on DUT1

        DUT2.ospf.redistribute_static()

        time.sleep(45)

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="99.0.0.0", protocol="O")
        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="100.0.0.0", protocol="O E",
                                                                metric_type="2")

        # Add another static route

        DUT2.ip.add_static_route(network_dest="77.0.0.0", mask_dest="255.255.0.0", next_hop="99.0.0.100")

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="99.0.0.0", protocol="O")
        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="100.0.0.0", protocol="O E",
                                                                metric_type="2")
        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="77.0.0.0", protocol="O E",
                                                                metric_type="2")

        # Remove the static route on DUT2 and check if the route is not anymore in the routing table of DUT1

        DUT2.ospf.remove_redistribute_static()

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(45)

        ospf_flow_.confirm_network_not_in_the_routing_table(DUT1, network="100.0.0.0")
        ospf_flow_.confirm_network_not_in_the_routing_table(DUT1, network="77.0.0.0")
        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="99.0.0.0", protocol="O")

        print("########## Removing the config #############")

        DUT2.ip.remove_static_route(network_dest="100.0.0.0", mask_dest="255.255.0.0", next_hop="99.0.0.100")
        DUT2.ip.remove_static_route(network_dest="77.0.0.0", mask_dest="255.255.0.0", next_hop="99.0.0.100")

        ospf_flow_.remove_networks(DUT1, int_vlan20=["20.0.0.2", "0.0.0.0"])
        ospf_flow_.remove_networks(DUT2, int_vlan20=["20.0.0.1", "0.0.0.0"], int_vlan99=["99.0.0.1", "0.0.0.0"])

        ospf_flow_.disable_OSPF(DUT1)
        ospf_flow_.disable_OSPF(DUT2)

        ospf_flow_.remove_vlans_and_interfaces_vlan(DUT1, "20")
        ospf_flow_.remove_vlans_and_interfaces_vlan(DUT2, "20", "99")

        ospf_flow_.shut_interfaces(DUT1, DUT1.ports["v1"])
        ospf_flow_.shut_interfaces(DUT2, DUT2.ports["v1"], DUT2.ports["h4"])

    def test_func_3(self):

        print("###### Test_func_3 ######")
        print("########## Verify if a custom metric can be configured on routes redistributed into OSPF #############")
        print("###### 2 DUTs ######")

        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT1, port=DUT1.ports["v1"],vlan="20",
                                                                                   ip="20.0.0.2", mask="255.255.255.0")

        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["v1"],vlan="20",
                                                                                   ip="20.0.0.1", mask="255.255.255.0")
        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["h4"], vlan="99",
                                                                                   ip="99.0.0.1", mask="255.255.255.0")
        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["h4"],vlan="60",
                                                                                   ip="60.0.0.1", mask="255.255.255.0")

        ospf_flow_.enable_and_advertise_networks(DUT1, int_vlan20=["20.0.0.2", "0.0.0.0"])
        ospf_flow_.enable_and_advertise_networks(DUT2, int_vlan20=["20.0.0.1", "0.0.0.0"],
                                                 int_vlan99=["99.0.0.1", "0.0.0.0"])

        # Creating a static route

        DUT2.ip.add_static_route(network_dest="100.0.0.0", mask_dest="255.255.0.0", next_hop="99.0.0.100")

        # Redistributing the static network on DUT2 and installing it on DUT1

        DUT2.ospf.redistribute_static()

        # Redistributing connected routes on DUT2 and installing it on DUT1

        DUT2.ospf.redistribute_connected()

        time.sleep(45)

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="99.0.0.0", protocol="O")
        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="60.0.0.0", protocol="O E",
                                                                metric_type="2", metric="10")
        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="100.0.0.0", protocol="O E",
                                                                metric_type="2", metric="10")

        # Redistribute with different metric

        DUT2.ospf.remove_redistribute_static()
        DUT2.ospf.redistribute_static(metric="500")

        # Redistribute with different metric

        DUT2.ospf.remove_redistribute_connected()
        DUT2.ospf.redistribute_connected(metric="500")

        time.sleep(5)

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="99.0.0.0", protocol="O")
        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="60.0.0.0", protocol="O E",
                                                                metric_type="2", metric="500")
        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="100.0.0.0", protocol="O E",
                                                                metric_type="2", metric="500")

        # Remove redistribution on DUT2 and check if the connected/static routes are not anymore in the routing table of DUT1

        DUT2.ospf.remove_redistribute_static()
        DUT2.ospf.remove_redistribute_connected()

        time.sleep(5)

        ospf_flow_.confirm_network_not_in_the_routing_table(DUT1, network="100.0.0.0")
        ospf_flow_.confirm_network_not_in_the_routing_table(DUT1, network="77.0.0.0")
        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="99.0.0.0", protocol="O")

        print("########## Removing the config #############")

        DUT2.ip.remove_static_route(network_dest="100.0.0.0", mask_dest="255.255.0.0", next_hop="99.0.0.100")

        ospf_flow_.remove_networks(DUT1, int_vlan20=["20.0.0.2", "0.0.0.0"])
        ospf_flow_.remove_networks(DUT2, int_vlan20=["20.0.0.1", "0.0.0.0"], int_vlan99=["99.0.0.1", "0.0.0.0"])

        ospf_flow_.disable_OSPF(DUT1)
        ospf_flow_.disable_OSPF(DUT2)

        ospf_flow_.remove_vlans_and_interfaces_vlan(DUT1, "20")
        ospf_flow_.remove_vlans_and_interfaces_vlan(DUT2, "20", "99", "60")

        ospf_flow_.shut_interfaces(DUT1, DUT1.ports["v1"])
        ospf_flow_.shut_interfaces(DUT2, DUT2.ports["v1"], DUT2.ports["h4"])

    def test_func_4(self):

        print("###### Test_func_4 ######")
        print("########## Verify if RIP routes are redistributed into OSPF #############")
        print("###### 3 DUTs ######")

        #          Topology
        #
        #  DUT1 --OSPF-- DUT2 --RIP-- DUT3 -- RIP

        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT1, port=DUT1.ports["v1"],vlan="20",
                                                                                   ip="20.0.0.2", mask="255.255.255.0")

        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["v1"],vlan="20",
                                                                                   ip="20.0.0.1", mask="255.255.255.0")
        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["h4"],vlan="15",
                                                                                   ip="15.0.0.1", mask="255.255.255.0")
        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["h2"],vlan="30",
                                                                                   ip="30.0.0.1", mask="255.255.255.0")

        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT3, port=DUT3.ports["h2"],vlan="30",
                                                                                   ip="30.0.0.2", mask="255.255.255.0")
        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT3, port=DUT3.ports["h2"],vlan="50",
                                                                                   ip="50.0.0.1", mask="255.255.255.0")

        # Enable ospf on DUT1 and DUT2 and advertise the IPs

        ospf_flow_.enable_and_advertise_networks(DUT1, int_vlan20=["20.0.0.2", "0.0.0.0"])
        ospf_flow_.enable_and_advertise_networks(DUT2, int_vlan20=["20.0.0.1", "0.0.0.0"],
                                                       int_vlan15=["15.0.0.1", "0.0.0.0"])

        # Enable rip on DUT2 and DUT3 and advertise the IPs

        rip_flow_.enable_and_advertise_networks(DUT2, "30.0.0.1")
        rip_flow_.enable_and_advertise_networks(DUT3, "30.0.0.2", "50.0.0.1")

        # Redistributing the rip routes into ospf on DUT2

        DUT2.ospf.redistribute_rip()

        time.sleep(45)

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="O")
        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="50.0.0.0", protocol="O E2")

        # Remove the redistribution and check that the rip routes are not present in DUT1 Routing Table

        DUT2.ospf.remove_redistribute_rip()

        time.sleep(5)

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="O")
        ospf_flow_.confirm_network_not_in_the_routing_table(DUT1, network="50.0.0.0")

        print("########## Removing the config #############")

        ospf_flow_.remove_networks(DUT1, int_vlan20=["20.0.0.2", "0.0.0.0"])
        ospf_flow_.remove_networks(DUT2, int_vlan20=["20.0.0.1", "0.0.0.0"], int_vlan99=["15.0.0.1", "0.0.0.0"])

        ospf_flow_.disable_OSPF(DUT1)
        ospf_flow_.disable_OSPF(DUT2)

        rip_flow_.disable_RIP(DUT2)
        rip_flow_.disable_RIP(DUT3)

        ospf_flow_.remove_vlans_and_interfaces_vlan(DUT1, "20")
        ospf_flow_.remove_vlans_and_interfaces_vlan(DUT2, "15", "20", "30")
        ospf_flow_.remove_vlans_and_interfaces_vlan(DUT3, "30", "50")

        ospf_flow_.shut_interfaces(DUT1, DUT1.ports["v1"])
        ospf_flow_.shut_interfaces(DUT2, DUT2.ports["v1"], DUT2.ports["h4"], DUT2.ports["h2"])
        ospf_flow_.shut_interfaces(DUT3, DUT3.ports["h2"])

    def test_func_6(self):

        print("###### Test_func_6 ######")
        print("########## Verify OSPF simple text Authentication  #############")
        print("###### 2 DUTs ######")

        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT1, port=DUT1.ports["v1"],vlan="20",
                                                                                   ip="20.0.0.2", mask="255.255.255.0")

        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["v1"], vlan="20",
                                                                                   ip="20.0.0.1", mask="255.255.255.0")
        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["h4"],vlan="15",
                                                                                   ip="15.0.0.1", mask="255.255.255.0")

        ospf_flow_.enable_and_advertise_networks(DUT1, int_vlan20=["20.0.0.2", "0.0.0.0"])
        ospf_flow_.enable_and_advertise_networks(DUT2, int_vlan20=["20.0.0.1", "0.0.0.0"],
                                                 int_vlan15=["15.0.0.1", "0.0.0.0"])

        # Configure the authentication on the int-vlan between the DUTs and configure the key. Check that the adjacency occurs

        DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="simple", authentication_key="1234")
        DUT2.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="simple", authentication_key="1234")

        time.sleep(45)

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="O")
        ospf_flow_.confirm_ospf_neighbors(DUT1, neighbor_id=DUT2.ip_session, state="FULL")

        # Change the key for DUT1 and check that there is no adjacency and the routes are not installed

        DUT1.ospf.add_ip_ospf_authentication_key(int_vlan="20", authentication_key="12345")

        time.sleep(45)

        ospf_flow_.confirm_network_not_in_the_routing_table(DUT1, network="15.0.0.0")
        ospf_flow_.confirm_neighbor_not_present(DUT1,neighbor_id=DUT2.ip_session)

        DUT2.ospf.add_ip_ospf_authentication_key(int_vlan="20", authentication_key="12345")

        time.sleep(45)

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="O")
        ospf_flow_.confirm_ospf_neighbors(DUT1, neighbor_id=DUT2.ip_session, state="FULL")

        # Remove the authentication and authentication-keys on both DUTs and check that there is adjacency and the routes are learned

        DUT1.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20")

        DUT2.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT2.ospf.remove_ip_ospf_authentication_key(int_vlan="20")

        time.sleep(45)

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="O")
        ospf_flow_.confirm_ospf_neighbors(DUT1, neighbor_id=DUT2.ip_session, state="FULL")

        print("########## Removing the config #############")

        ospf_flow_.remove_networks(DUT1, int_vlan20=["20.0.0.2", "0.0.0.0"])
        ospf_flow_.remove_networks(DUT2, int_vlan20=["20.0.0.1", "0.0.0.0"], int_vlan99=["15.0.0.1", "0.0.0.0"])

        ospf_flow_.disable_OSPF(DUT1)
        ospf_flow_.disable_OSPF(DUT2)

        ospf_flow_.remove_vlans_and_interfaces_vlan(DUT1, "20")
        ospf_flow_.remove_vlans_and_interfaces_vlan(DUT2, "20", "15")

        ospf_flow_.shut_interfaces(DUT1, DUT1.ports["v1"])
        ospf_flow_.shut_interfaces(DUT2, DUT2.ports["v1"], DUT2.ports["h4"])

    def test_func_7(self):

        print("###### Test_func_7 ######")
        print("########## Verify OSPF Message-Digest Authentication  #############")
        print("###### 2 DUTs ######")

        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT1, port=DUT1.ports["v1"],vlan="20",
                                                                                   ip="20.0.0.2", mask="255.255.255.0")

        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["v1"], vlan="20",
                                                                                   ip="20.0.0.1", mask="255.255.255.0")
        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["h4"],vlan="15",
                                                                                   ip="15.0.0.1", mask="255.255.255.0")

        ospf_flow_.enable_and_advertise_networks(DUT1, int_vlan20=["20.0.0.2", "0.0.0.0"])
        ospf_flow_.enable_and_advertise_networks(DUT2, int_vlan20=["20.0.0.1", "0.0.0.0"],
                                                 int_vlan15=["15.0.0.1", "0.0.0.0"])

        # Configure the authentication on the int-vlan between the DUTs and configure the key. Check that the adjacency occurs

        DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="md5", authentication_key="1234",
                                             message_digest_key="1", message_digest="Yes")
        DUT2.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="md5", authentication_key="1234",
                                             message_digest_key="1", message_digest="Yes")

        time.sleep(45)

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="O")
        ospf_flow_.confirm_ospf_neighbors(DUT1, neighbor_id=DUT2.ip_session, state="FULL")

        # Change the key for DUT1 and check that there is no adjacency and the routes are not installed

        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")
        DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="md5", authentication_key="12345",
                                             message_digest_key="1", message_digest="Yes")

        time.sleep(45)

        ospf_flow_.confirm_network_not_in_the_routing_table(DUT1, network="15.0.0.0")
        ospf_flow_.confirm_ospf_neighbors(DUT1, neighbor_id=DUT2.ip_session, state="DOWN")

        # Remove the authentication and authentication-keys on both DUTs and check that there is adjacency and the routes are learned

        DUT1.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")

        DUT2.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT2.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")

        time.sleep(45)

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="O")
        ospf_flow_.confirm_ospf_neighbors(DUT1, neighbor_id=DUT2.ip_session, state="FULL")

        print("########## Removing the config #############")

        ospf_flow_.remove_networks(DUT1, int_vlan20=["20.0.0.2", "0.0.0.0"])
        ospf_flow_.remove_networks(DUT2, int_vlan20=["20.0.0.1", "0.0.0.0"], int_vlan99=["15.0.0.1", "0.0.0.0"])

        ospf_flow_.disable_OSPF(DUT1)
        ospf_flow_.disable_OSPF(DUT2)

        ospf_flow_.remove_vlans_and_interfaces_vlan(DUT1, "20")
        ospf_flow_.remove_vlans_and_interfaces_vlan(DUT2, "20", "15")

        ospf_flow_.shut_interfaces(DUT1, DUT1.ports["v1"])
        ospf_flow_.shut_interfaces(DUT2, DUT2.ports["v1"], DUT2.ports["h4"])

    def test_func_8(self):

        print("###### Test_func_8 ######")
        print("########## Verify OSPF  Authentication using SHA-1 algorithm  #############")
        print("###### 2 DUTs ######")

        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT1, port=DUT1.ports["v1"],vlan="20",
                                                                                   ip="20.0.0.2", mask="255.255.255.0")

        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["v1"], vlan="20",
                                                                                   ip="20.0.0.1", mask="255.255.255.0")
        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["h4"],vlan="15",
                                                                                   ip="15.0.0.1", mask="255.255.255.0")

        ospf_flow_.enable_and_advertise_networks(DUT1, int_vlan20=["20.0.0.2", "0.0.0.0"])
        ospf_flow_.enable_and_advertise_networks(DUT2, int_vlan20=["20.0.0.1", "0.0.0.0"],
                                                 int_vlan15=["15.0.0.1", "0.0.0.0"])

        # Configure the authentication on the int-vlan between the DUTs and configure the key. Check that the adjacency occurs

        DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-1", authentication_key="1234",
                                             message_digest_key="1")
        DUT2.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-1", authentication_key="1234",
                                             message_digest_key="1")

        time.sleep(45)

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="O")
        ospf_flow_.confirm_ospf_neighbors(DUT1, neighbor_id=DUT2.ip_session, state="FULL")

        # Change the key for DUT1 and check that there is no adjacency and the routes are not installed

        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")
        DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-1", authentication_key="12345",
                                             message_digest_key="1")

        time.sleep(45)

        ospf_flow_.confirm_network_not_in_the_routing_table(DUT1, network="15.0.0.0")
        ospf_flow_.confirm_ospf_neighbors(DUT1, neighbor_id=DUT2.ip_session, state="DOWN")

        # Change the key for DUT2 and check that there is adjacency and the routes are learned

        DUT2.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")
        DUT2.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-1", authentication_key="12345",
                                             message_digest_key="1")
        time.sleep(45)

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="O")
        ospf_flow_.confirm_ospf_neighbors(DUT1, neighbor_id=DUT2.ip_session, state="FULL")

        # Remove the authentication and authentication-keys on both DUTs and check that there is adjacency and the routes are learned

        DUT1.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")

        DUT2.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT2.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")

        time.sleep(45)

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="O")
        ospf_flow_.confirm_ospf_neighbors(DUT1, neighbor_id=DUT2.ip_session, state="FULL")

        print("########## Removing the config #############")

        ospf_flow_.remove_networks(DUT1, int_vlan20=["20.0.0.2", "0.0.0.0"])
        ospf_flow_.remove_networks(DUT2, int_vlan20=["20.0.0.1", "0.0.0.0"], int_vlan99=["15.0.0.1", "0.0.0.0"])

        ospf_flow_.disable_OSPF(DUT1)
        ospf_flow_.disable_OSPF(DUT2)

        ospf_flow_.remove_vlans_and_interfaces_vlan(DUT1, "20")
        ospf_flow_.remove_vlans_and_interfaces_vlan(DUT2, "20", "15")

        ospf_flow_.shut_interfaces(DUT1, DUT1.ports["v1"])
        ospf_flow_.shut_interfaces(DUT2, DUT2.ports["v1"], DUT2.ports["h4"])

    def test_func_9(self):

        print("###### Test_func_9 ######")
        print("########## Verify OSPF  Authentication using SHA-224 algorithm  #############")
        print("###### 2 DUTs ######")

        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT1, port=DUT1.ports["v1"],vlan="20",
                                                                                   ip="20.0.0.2", mask="255.255.255.0")

        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["v1"], vlan="20",
                                                                                   ip="20.0.0.1", mask="255.255.255.0")
        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["h4"],vlan="15",
                                                                                   ip="15.0.0.1", mask="255.255.255.0")

        ospf_flow_.enable_and_advertise_networks(DUT1, int_vlan20=["20.0.0.2", "0.0.0.0"])
        ospf_flow_.enable_and_advertise_networks(DUT2, int_vlan20=["20.0.0.1", "0.0.0.0"],
                                                 int_vlan15=["15.0.0.1", "0.0.0.0"])

        # Configure the authentication on the int-vlan between the DUTs and configure the key. Check that the adjacency occurs

        DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-224", authentication_key="1234",
                                             message_digest_key="1")
        DUT2.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-224", authentication_key="1234",
                                             message_digest_key="1")

        time.sleep(45)

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="O")
        ospf_flow_.confirm_ospf_neighbors(DUT1, neighbor_id=DUT2.ip_session, state="FULL")

        # Change the key for DUT1 and check that there is no adjacency and the routes are not installed

        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")
        DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-224", authentication_key="12345",
                                             message_digest_key="1")

        time.sleep(45)

        ospf_flow_.confirm_network_not_in_the_routing_table(DUT1, network="15.0.0.0")
        ospf_flow_.confirm_ospf_neighbors(DUT1, neighbor_id=DUT2.ip_session, state="DOWN")

        # Change the key for DUT2 and check that there is adjacency and the routes are learned

        DUT2.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")
        DUT2.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-224", authentication_key="12345",
                                             message_digest_key="1")
        time.sleep(45)

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="O")
        ospf_flow_.confirm_ospf_neighbors(DUT1, neighbor_id=DUT2.ip_session, state="FULL")

        # Remove the authentication and authentication-keys on both DUTs and check that there is adjacency and the routes are learned

        DUT1.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")

        DUT2.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT2.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")

        time.sleep(45)

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="O")
        ospf_flow_.confirm_ospf_neighbors(DUT1, neighbor_id=DUT2.ip_session, state="FULL")

        print("########## Removing the config #############")

        ospf_flow_.remove_networks(DUT1, int_vlan20=["20.0.0.2", "0.0.0.0"])
        ospf_flow_.remove_networks(DUT2, int_vlan20=["20.0.0.1", "0.0.0.0"], int_vlan99=["15.0.0.1", "0.0.0.0"])

        ospf_flow_.disable_OSPF(DUT1)
        ospf_flow_.disable_OSPF(DUT2)

        ospf_flow_.remove_vlans_and_interfaces_vlan(DUT1, "20")
        ospf_flow_.remove_vlans_and_interfaces_vlan(DUT2, "20", "15")

        ospf_flow_.shut_interfaces(DUT1, DUT1.ports["v1"])
        ospf_flow_.shut_interfaces(DUT2, DUT2.ports["v1"], DUT2.ports["h4"])

    def test_func_10(self):

        print("###### Test_func_10 ######")
        print("########## Verify OSPF  Authentication using SHA-256 algorithm  #############")
        print("###### 2 DUTs ######")

        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT1, port=DUT1.ports["v1"],vlan="20",
                                                                                   ip="20.0.0.2", mask="255.255.255.0")

        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["v1"], vlan="20",
                                                                                   ip="20.0.0.1", mask="255.255.255.0")
        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["h4"],vlan="15",
                                                                                   ip="15.0.0.1", mask="255.255.255.0")

        ospf_flow_.enable_and_advertise_networks(DUT1, int_vlan20=["20.0.0.2", "0.0.0.0"])
        ospf_flow_.enable_and_advertise_networks(DUT2, int_vlan20=["20.0.0.1", "0.0.0.0"],
                                                 int_vlan15=["15.0.0.1", "0.0.0.0"])

        # Configure the authentication on the int-vlan between the DUTs and configure the key. Check that the adjacency occurs

        DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-256", authentication_key="1234",
                                             message_digest_key="1")
        DUT2.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-256", authentication_key="1234",
                                             message_digest_key="1")

        time.sleep(45)

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="O")
        ospf_flow_.confirm_ospf_neighbors(DUT1, neighbor_id=DUT2.ip_session, state="FULL")

        # Change the key for DUT1 and check that there is no adjacency and the routes are not installed

        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")
        DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-256", authentication_key="12345",
                                             message_digest_key="1")

        time.sleep(45)

        ospf_flow_.confirm_network_not_in_the_routing_table(DUT1, network="15.0.0.0")
        ospf_flow_.confirm_ospf_neighbors(DUT1, neighbor_id=DUT2.ip_session, state="DOWN")

        # Change the key for DUT2 and check that there is adjacency and the routes are learned

        DUT2.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")
        DUT2.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-256", authentication_key="12345",
                                             message_digest_key="1")
        time.sleep(45)

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="O")
        ospf_flow_.confirm_ospf_neighbors(DUT1, neighbor_id=DUT2.ip_session, state="FULL")

        # Remove the authentication and authentication-keys on both DUTs and check that there is adjacency and the routes are learned

        DUT1.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")

        DUT2.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT2.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")

        time.sleep(45)

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="O")
        ospf_flow_.confirm_ospf_neighbors(DUT1, neighbor_id=DUT2.ip_session, state="FULL")

        print("########## Removing the config #############")

        ospf_flow_.remove_networks(DUT1, int_vlan20=["20.0.0.2", "0.0.0.0"])
        ospf_flow_.remove_networks(DUT2, int_vlan20=["20.0.0.1", "0.0.0.0"], int_vlan99=["15.0.0.1", "0.0.0.0"])

        ospf_flow_.disable_OSPF(DUT1)
        ospf_flow_.disable_OSPF(DUT2)

        ospf_flow_.remove_vlans_and_interfaces_vlan(DUT1, "20")
        ospf_flow_.remove_vlans_and_interfaces_vlan(DUT2, "20", "15")

        ospf_flow_.shut_interfaces(DUT1, DUT1.ports["v1"])
        ospf_flow_.shut_interfaces(DUT2, DUT2.ports["v1"], DUT2.ports["h4"])
    def test_func_11(self):

        print("###### Test_func_11 ######")
        print("########## Verify OSPF  Authentication using SHA-384 algorithm  #############")
        print("###### 2 DUTs ######")

        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT1, port=DUT1.ports["v1"],vlan="20",
                                                                                   ip="20.0.0.2", mask="255.255.255.0")

        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["v1"], vlan="20",
                                                                                   ip="20.0.0.1", mask="255.255.255.0")
        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["h4"],vlan="15",
                                                                                   ip="15.0.0.1", mask="255.255.255.0")

        ospf_flow_.enable_and_advertise_networks(DUT1, int_vlan20=["20.0.0.2", "0.0.0.0"])
        ospf_flow_.enable_and_advertise_networks(DUT2, int_vlan20=["20.0.0.1", "0.0.0.0"],
                                                 int_vlan15=["15.0.0.1", "0.0.0.0"])

        # Configure the authentication on the int-vlan between the DUTs and configure the key. Check that the adjacency occurs

        DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-384", authentication_key="1234",
                                             message_digest_key="1")
        DUT2.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-384", authentication_key="1234",
                                             message_digest_key="1")

        time.sleep(45)

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="O")
        ospf_flow_.confirm_ospf_neighbors(DUT1, neighbor_id=DUT2.ip_session, state="FULL")

        # Change the key for DUT1 and check that there is no adjacency and the routes are not installed

        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")
        DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-384", authentication_key="12345",
                                             message_digest_key="1")

        time.sleep(45)

        ospf_flow_.confirm_network_not_in_the_routing_table(DUT1, network="15.0.0.0")
        ospf_flow_.confirm_ospf_neighbors(DUT1, neighbor_id=DUT2.ip_session, state="DOWN")

        # Change the key for DUT2 and check that there is adjacency and the routes are learned

        DUT2.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")
        DUT2.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-384", authentication_key="12345",
                                             message_digest_key="1")
        time.sleep(45)

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="O")
        ospf_flow_.confirm_ospf_neighbors(DUT1, neighbor_id=DUT2.ip_session, state="FULL")

        # Remove the authentication and authentication-keys on both DUTs and check that there is adjacency and the routes are learned

        DUT1.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")

        DUT2.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT2.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")

        time.sleep(45)

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="O")
        ospf_flow_.confirm_ospf_neighbors(DUT1, neighbor_id=DUT2.ip_session, state="FULL")

        print("########## Removing the config #############")

        ospf_flow_.remove_networks(DUT1, int_vlan20=["20.0.0.2", "0.0.0.0"])
        ospf_flow_.remove_networks(DUT2, int_vlan20=["20.0.0.1", "0.0.0.0"], int_vlan99=["15.0.0.1", "0.0.0.0"])

        ospf_flow_.disable_OSPF(DUT1)
        ospf_flow_.disable_OSPF(DUT2)

        ospf_flow_.remove_vlans_and_interfaces_vlan(DUT1, "20")
        ospf_flow_.remove_vlans_and_interfaces_vlan(DUT2, "20", "15")

        ospf_flow_.shut_interfaces(DUT1, DUT1.ports["v1"])
        ospf_flow_.shut_interfaces(DUT2, DUT2.ports["v1"], DUT2.ports["h4"])

    def test_func_12(self):

        print("###### Test_func_12 ######")
        print("########## Verify OSPF  Authentication using SHA-512 algorithm  #############")
        print("###### 2 DUTs ######")

        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT1, port=DUT1.ports["v1"],vlan="20",
                                                                                   ip="20.0.0.2", mask="255.255.255.0")

        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["v1"], vlan="20",
                                                                                   ip="20.0.0.1", mask="255.255.255.0")
        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["h4"],vlan="15",
                                                                                   ip="15.0.0.1", mask="255.255.255.0")

        ospf_flow_.enable_and_advertise_networks(DUT1, int_vlan20=["20.0.0.2", "0.0.0.0"])
        ospf_flow_.enable_and_advertise_networks(DUT2, int_vlan20=["20.0.0.1", "0.0.0.0"],
                                                 int_vlan15=["15.0.0.1", "0.0.0.0"])

        # Configure the authentication on the int-vlan between the DUTs and configure the key. Check that the adjacency occurs

        DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-512", authentication_key="1234",
                                             message_digest_key="1")
        DUT2.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-512", authentication_key="1234",
                                             message_digest_key="1")

        time.sleep(45)

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="O")
        ospf_flow_.confirm_ospf_neighbors(DUT1, neighbor_id=DUT2.ip_session, state="FULL")

        # Change the key for DUT1 and check that there is no adjacency and the routes are not installed

        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")
        DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-512", authentication_key="12345",
                                             message_digest_key="1")

        time.sleep(45)

        ospf_flow_.confirm_network_not_in_the_routing_table(DUT1, network="15.0.0.0")
        ospf_flow_.confirm_ospf_neighbors(DUT1, neighbor_id=DUT2.ip_session, state="DOWN")

        # Change the key for DUT2 and check that there is adjacency and the routes are learned

        DUT2.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")
        DUT2.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-512", authentication_key="12345",
                                             message_digest_key="1")
        time.sleep(45)

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="O")
        ospf_flow_.confirm_ospf_neighbors(DUT1, neighbor_id=DUT2.ip_session, state="FULL")

        # Remove the authentication and authentication-keys on both DUTs and check that there is adjacency and the routes are learned

        DUT1.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")

        DUT2.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT2.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")

        time.sleep(45)

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="O")
        ospf_flow_.confirm_ospf_neighbors(DUT1, neighbor_id=DUT2.ip_session, state="FULL")

        print("########## Removing the config #############")

        ospf_flow_.remove_networks(DUT1, int_vlan20=["20.0.0.2", "0.0.0.0"])
        ospf_flow_.remove_networks(DUT2, int_vlan20=["20.0.0.1", "0.0.0.0"], int_vlan99=["15.0.0.1", "0.0.0.0"])

        ospf_flow_.disable_OSPF(DUT1)
        ospf_flow_.disable_OSPF(DUT2)

        ospf_flow_.remove_vlans_and_interfaces_vlan(DUT1, "20")
        ospf_flow_.remove_vlans_and_interfaces_vlan(DUT2, "20", "15")

        ospf_flow_.shut_interfaces(DUT1, DUT1.ports["v1"])
        ospf_flow_.shut_interfaces(DUT2, DUT2.ports["v1"], DUT2.ports["h4"])

    def test_func_13(self):

        print("###### Test_func_13 ######")
        print("########## Verify if OSPF adjacency cannot be formed when Secret Key ID is different  #############")
        print("###### 2 DUTs ######")

        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT1, port=DUT1.ports["v1"],vlan="20",
                                                                                   ip="20.0.0.2", mask="255.255.255.0")

        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["v1"], vlan="20",
                                                                                   ip="20.0.0.1", mask="255.255.255.0")
        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT2, port=DUT2.ports["h4"],vlan="15",
                                                                                   ip="15.0.0.1", mask="255.255.255.0")

        ospf_flow_.enable_and_advertise_networks(DUT1, int_vlan20=["20.0.0.2", "0.0.0.0"])
        ospf_flow_.enable_and_advertise_networks(DUT2, int_vlan20=["20.0.0.1", "0.0.0.0"],
                                                 int_vlan15=["15.0.0.1", "0.0.0.0"])

        # Configure different authentication keys on the int-vlan between the DUTs and configure the key. Check that the
        # adjacency does not occur

        DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-384", authentication_key="1234",
                                             message_digest_key="1")
        DUT2.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-384", authentication_key="12345",
                                             message_digest_key="1")

        time.sleep(45)

        ospf_flow_.confirm_network_not_in_the_routing_table(DUT1, network="15.0.0.0")
        ospf_flow_.confirm_ospf_neighbors(DUT1, neighbor_id=DUT2.ip_session, state="DOWN")

        # Change the key for DUT1 and check that there is adjacency and the routes are learned

        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")
        DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-384", authentication_key="12345",
                                             message_digest_key="1")
        time.sleep(45)

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="O")
        ospf_flow_.confirm_ospf_neighbors(DUT1, neighbor_id=DUT2.ip_session, state="FULL")

        # Remove the authentication and authentication-keys on both DUTs and check that there is adjacency and the routes are learned

        DUT1.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")

        DUT2.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT2.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")

        time.sleep(45)

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT1, network="15.0.0.0", protocol="O")
        ospf_flow_.confirm_ospf_neighbors(DUT1, neighbor_id=DUT2.ip_session, state="FULL")

        print("########## Removing the config #############")

        ospf_flow_.remove_networks(DUT1, int_vlan20=["20.0.0.2", "0.0.0.0"])
        ospf_flow_.remove_networks(DUT2, int_vlan20=["20.0.0.1", "0.0.0.0"], int_vlan99=["15.0.0.1", "0.0.0.0"])

        ospf_flow_.disable_OSPF(DUT1)
        ospf_flow_.disable_OSPF(DUT2)

        ospf_flow_.remove_vlans_and_interfaces_vlan(DUT1, "20")
        ospf_flow_.remove_vlans_and_interfaces_vlan(DUT2, "20", "15")

        ospf_flow_.shut_interfaces(DUT1, DUT1.ports["v1"])
        ospf_flow_.shut_interfaces(DUT2, DUT2.ports["v1"], DUT2.ports["h4"])

    def test_func_14(self):

        print("###### Test_func_14 ######")
        print("########## Verify if sha keys and md5 keys are not displayed in show running config  #############")
        print("###### 1 DUTs ######")

        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT1, port=DUT1.ports["v1"],vlan="20",
                                                                                   ip="20.0.0.2", mask="255.255.255.0")

        ospf_flow_.no_shut_interfaces(DUT2, DUT2.ports["v1"])
        ospf_flow_.enable_and_advertise_networks(DUT1, int_vlan20=["20.0.0.2", "0.0.0.0"])

        # Configure a key for ospf authentication on DUT1

        DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-384", authentication_key="1234",
                                             message_digest_key="1")
        time.sleep(5)

        ospf_flow_.check_authentication_key_in_running_config(DUT1, authentication="sha-384", authentication_key="1234",
                                             message_digest_key="1")

        # Configure another key for ospf authentication on DUT1

        DUT1.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")
        DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="md5", authentication_key="12345",message_digest_key="1", message_digest="Yes")

        time.sleep(5)

        ospf_flow_.check_authentication_key_in_running_config(DUT1, authentication="md5", authentication_key="12345",message_digest_key="1")

        # Remove the authentication and authentication-keys on both DUTs and check that there is adjacency and the routes are learned

        DUT1.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")

        print("########## Removing the config #############")

        ospf_flow_.remove_networks(DUT1, int_vlan20=["20.0.0.2", "0.0.0.0"])
        ospf_flow_.disable_OSPF(DUT1)
        ospf_flow_.remove_vlans_and_interfaces_vlan(DUT1, "20")

        ospf_flow_.shut_interfaces(DUT1, DUT1.ports["v1"])
        ospf_flow_.shut_interfaces(DUT2, DUT2.ports["v1"])




    def test_func_100(self):

        # LOKI-4711 Customer - OSPF route is missing after fail over on router port

        print("###### Test_func_100 ######")
        print(
            "########## Check if we can advertise networks into OSPF and it establish connection using routed ports  #############")
        print("###### 3 DUTs ######")

        #       Topology
        #
        #        Area 0
        #
        # -- DUT1 ---- DUT3
        #       \      /
        #        \    /
        #         DUT2
        #

        ospf_flow_.create_routed_port_and_add_ip(DUT1, interface=DUT1.ports["v1"], ip="20.0.0.2", mask="255.255.255.0")
        ospf_flow_.create_routed_port_and_add_ip(DUT1, interface=DUT1.ports["x1"], ip="40.0.0.1", mask="255.255.255.0")

        ospf_flow_.create_routed_port_and_add_ip(DUT3, interface=DUT3.ports["h2"], ip="30.0.0.2", mask="255.255.255.0")
        ospf_flow_.create_routed_port_and_add_ip(DUT3, interface=DUT3.ports["x1"], ip="40.0.0.2", mask="255.255.255.0")

        ospf_flow_.create_routed_port_and_add_ip(DUT2, interface=DUT2.ports["h2"], ip="30.0.0.1", mask="255.255.255.0")
        ospf_flow_.create_routed_port_and_add_ip(DUT2, interface=DUT2.ports["v1"], ip="20.0.0.1", mask="255.255.255.0")

        ospf_flow_.create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(DUT1, port=DUT1.ports["h3"],
                                                                                   vlan="15",
                                                                                   ip="15.0.0.1", mask="255.255.255.0")

        ospf_flow_.enable_and_advertise_networks(DUT1, int_vlan15=["15.0.0.1", "0.0.0.0"],
                                                 interface1=["20.0.0.2", "0.0.0.0"], interface2=["40.0.0.1", "0.0.0.0"])
        ospf_flow_.enable_and_advertise_networks(DUT3, interface1=["30.0.0.2", "0.0.0.0"],
                                                 interface2=["40.0.0.2", "0.0.0.0"])
        ospf_flow_.enable_and_advertise_networks(DUT2, interface1=["30.0.0.1", "0.0.0.0"],
                                                 interface2=["20.0.0.1", "0.0.0.0"])

        time.sleep(45)

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT2, network="15.0.0.0", protocol="O")
        ospf_flow_.confirm_network_details_in_the_routing_table(DUT2, network="40.0.0.0", protocol="O")

        # Shut one port on DUT1 and check that OSPF routes are not missing

        DUT1.int.shut_interface(interface=DUT1.ports["v1"])

        time.sleep(45)

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT2, network="15.0.0.0", protocol="O")
        ospf_flow_.confirm_network_details_in_the_routing_table(DUT2, network="40.0.0.0", protocol="O")

        # No shut the port on DUT1 and check that RIP routes are not missing

        DUT1.int.no_shut_interface(interface=DUT1.ports["v1"])

        time.sleep(45)

        ospf_flow_.confirm_network_details_in_the_routing_table(DUT2, network="15.0.0.0", protocol="O")
        ospf_flow_.confirm_network_details_in_the_routing_table(DUT2, network="40.0.0.0", protocol="O")

        print("########## Removing the config #############")

        ospf_flow_.remove_networks(DUT1, int_vlan15=["15.0.0.1", "0.0.0.0"], interface1=["20.0.0.2", "0.0.0.0"],
                                   interface2=["40.0.0.1", "0.0.0.0"])
        ospf_flow_.remove_networks(DUT3, interface1=["30.0.0.2", "0.0.0.0"], interface2=["40.0.0.2", "0.0.0.0"])
        ospf_flow_.remove_networks(DUT2, interface1=["30.0.0.1", "0.0.0.0"], interface2=["20.0.0.1", "0.0.0.0"])

        ospf_flow_.disable_OSPF(DUT1)
        ospf_flow_.disable_OSPF(DUT3)
        ospf_flow_.disable_OSPF(DUT2)

        ospf_flow_.remove_vlans_and_interfaces_vlan(DUT1, "15")

        ospf_flow_.remove_routed_port(DUT1, DUT1.ports["v1"], DUT1.ports["x1"])
        ospf_flow_.remove_routed_port(DUT3, DUT3.ports["h2"], DUT3.ports["x1"])
        ospf_flow_.remove_routed_port(DUT2, DUT2.ports["h2"], DUT2.ports["v1"])

        ospf_flow_.shut_interfaces(DUT1, DUT1.ports["h3"])

