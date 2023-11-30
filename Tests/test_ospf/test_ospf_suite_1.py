import time
import pytest
import pytest_html
import sys

from config import interfaces
from Management import dut_objects

ip_session_1 = "10.2.109.206"
ip_session_2 = "10.2.109.83"
ip_session_3 = "10.2.109.232"
ip_session_4 = "10.2.109.100"
ip_session_5 = "10.2.109.113"

DUT1 = dut_objects.DUT_Objects(ip_session=ip_session_1)
DUT2 = dut_objects.DUT_Objects(ip_session=ip_session_2)
DUT3 = dut_objects.DUT_Objects(ip_session=ip_session_3)
DUT4 = dut_objects.DUT_Objects(ip_session=ip_session_4)
DUT5 = dut_objects.DUT_Objects(ip_session=ip_session_5)


class TestOSPFSuite1:

    def test_func_1(self):

        print("###### Test_func_1 ######")
        print("########## Verify if Connected routes are redistributed into OSPF #############")
        print("###### 2 DUTs ######")

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/5", "Gi 0/6", "Gi 0/9")

        # Adding the ports to the VLAN

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")

        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/6", vlan="100")

        # Create IP interfaces on all DUTs for the specific VLANs

        DUT1.ip.add_ip_interfaces("20", int_vlan20=["20.0.0.2", "255.255.255.0"])
        DUT1.ip.no_shut_int_vlans("20")

        DUT2.ip.add_ip_interfaces("20", "15", "100", int_vlan20=["20.0.0.1", "255.255.255.0"],int_vlan15=["15.0.0.1", "255.255.255.0"],int_vlan100=["100.0.0.1", "255.255.255.0"])
        DUT2.ip.no_shut_int_vlans("15", "20", "100")

        # Enable ospf on all DUTs and advertise the IPs

        DUT1.ospf.enable_ospf()
        DUT2.ospf.enable_ospf()

        DUT1.ospf.advertise_networks(int_vlan20=["20.0.0.2", "0.0.0.0"])
        DUT2.ospf.advertise_networks(int_vlan15=["15.0.0.1", "0.0.0.0"], int_vlan20=["20.0.0.1", "0.0.0.0"])

        # Redistributing the connected routes

        DUT2.ospf.redistribute_connected()

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        assert "100.0.0.0" in dict_of_networks.keys() and dict_of_networks["100.0.0.0"]["Protocol"] == "O E2"
        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"

        # Add another connected route

        DUT2.vl.add_ports_to_vlan(ports="Gi 0/6", vlan="60")
        DUT2.ip.add_ip_interfaces("60", int_vlan20=["60.0.0.1", "255.255.255.0"])
        DUT2.ip.no_shut_int_vlans("60")

        time.sleep(5)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        assert "100.0.0.0" in dict_of_networks.keys() and dict_of_networks["100.0.0.0"]["Protocol"] == "O E2"
        assert "60.0.0.0" in dict_of_networks.keys() and dict_of_networks["60.0.0.0"]["Protocol"] == "O E2"
        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"

        # Remove redistribution on DUT2 and check if the connected routes are not anymore in the routing table of DUT1

        DUT2.ospf.remove_redistribute_connected()

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        assert "100.0.0.0" not in dict_of_networks.keys()
        assert "60.0.0.0" not in dict_of_networks.keys()
        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"

        print("########## Removing the config #############")

        DUT1.ospf.remove_networks(int_vlan20=["20.0.0.2", "0.0.0.0"])
        DUT2.ospf.remove_networks(int_vlan15=["15.0.0.1", "0.0.0.0"], int_vlan20=["20.0.0.1", "0.0.0.0"])

        DUT1.ospf.disable_ospf()
        DUT2.ospf.disable_ospf()

        DUT1.ip.remove_int_vlan(int_vlan="20")
        DUT2.ip.remove_vlan_interfaces("20", "15", "100", "60")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5", "Gi 0/6")

        DUT1.vl.remove_vlan(vlan="20")
        DUT2.vl.remove_vlans("20", "15", "100", "60")

    def test_func_2(self):

        print("###### Test_func_2 ######")
        print("########## Verify if Static routes are redistributed into OSPF #############")
        print("###### 2 DUTs ######")

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/5", "Gi 0/6", "Gi 0/9")

        # Adding the ports to the VLAN

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")

        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")

        # Create IP interfaces on all DUTs for the specific VLANs

        DUT1.ip.add_ip_interfaces("20", int_vlan20=["20.0.0.2", "255.255.255.0"])
        DUT1.ip.no_shut_int_vlans("20")

        DUT2.ip.add_ip_interfaces("20", "15", int_vlan20=["20.0.0.1", "255.255.255.0"],int_vlan15=["15.0.0.1", "255.255.255.0"])
        DUT2.ip.no_shut_int_vlans("15", "20")

        # Creating a static route

        DUT2.ip.add_static_route(network_dest="100.0.0.0", mask_dest="255.255.0.0", next_hop="15.0.0.100")

        # Enable ospf on all DUTs and advertise the IPs

        DUT1.ospf.enable_ospf()
        DUT2.ospf.enable_ospf()

        DUT1.ospf.advertise_networks(int_vlan20=["20.0.0.2", "0.0.0.0"])
        DUT2.ospf.advertise_networks(int_vlan15=["15.0.0.1", "0.0.0.0"], int_vlan20=["20.0.0.1", "0.0.0.0"])

        # Redistributing the static routes

        DUT2.ospf.redistribute_static()

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        assert "100.0.0.0" in dict_of_networks.keys() and dict_of_networks["100.0.0.0"]["Protocol"] == "O E2"
        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"

        # Add another static route

        DUT2.ip.add_static_route(network_dest="77.0.0.0", mask_dest="255.255.0.0", next_hop="15.0.0.100")

        time.sleep(5)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        assert "100.0.0.0" in dict_of_networks.keys() and dict_of_networks["100.0.0.0"]["Protocol"] == "O E2"
        assert "77.0.0.0" in dict_of_networks.keys() and dict_of_networks["77.0.0.0"]["Protocol"] == "O E2"
        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"

        # Remove redistribution on DUT2 and check if the connected routes are not anymore in the routing table of DUT1

        DUT2.ospf.remove_redistribute_static()

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        assert "100.0.0.0" not in dict_of_networks.keys()
        assert "77.0.0.0" not in dict_of_networks.keys()
        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"

        print("########## Removing the config #############")

        DUT1.ospf.remove_networks(int_vlan20=["20.0.0.2", "0.0.0.0"])
        DUT2.ospf.remove_networks(int_vlan15=["15.0.0.1", "0.0.0.0"], int_vlan20=["20.0.0.1", "0.0.0.0"])

        DUT2.ip.remove_static_route(network_dest="100.0.0.0", mask_dest="255.255.0.0", next_hop="15.0.0.100")
        DUT2.ip.remove_static_route(network_dest="77.0.0.0", mask_dest="255.255.0.0", next_hop="15.0.0.100")

        DUT1.ospf.disable_ospf()
        DUT2.ospf.disable_ospf()

        DUT1.ip.remove_int_vlan(int_vlan="20")
        DUT2.ip.remove_vlan_interfaces("20", "15")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5", "Gi 0/6")

        DUT1.vl.remove_vlan(vlan="20")
        DUT2.vl.remove_vlans("20", "15")

    def test_func_3(self):

        print("###### Test_func_3 ######")
        print("########## Verify if a custom metric can be configured on routes redistributed into OSPF #############")
        print("###### 2 DUTs ######")

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/5", "Gi 0/6", "Gi 0/9")

        # Adding the ports to the VLAN

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")

        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/6", vlan="60")

        # Create IP interfaces on all DUTs for the specific VLANs

        DUT1.ip.add_ip_interfaces("20", int_vlan20=["20.0.0.2", "255.255.255.0"])
        DUT1.ip.no_shut_int_vlans("20")

        DUT2.ip.add_ip_interfaces("20", "15", "60", int_vlan20=["20.0.0.1", "255.255.255.0"],int_vlan15=["15.0.0.1", "255.255.255.0"],int_vlan60=["60.0.0.1", "255.255.255.0"])
        DUT2.ip.no_shut_int_vlans("15", "20", "60")

        # Creating a static route

        DUT2.ip.add_static_route(network_dest="88.0.0.0", mask_dest="255.255.0.0", next_hop="15.0.0.100")

        # Enable ospf on all DUTs and advertise the IPs

        DUT1.ospf.enable_ospf()
        DUT2.ospf.enable_ospf()

        DUT1.ospf.advertise_networks(int_vlan20=["20.0.0.2", "0.0.0.0"])
        DUT2.ospf.advertise_networks(int_vlan15=["15.0.0.1", "0.0.0.0"], int_vlan20=["20.0.0.1", "0.0.0.0"])

        # Redistributing the static routes

        DUT2.ospf.redistribute_static()

        # Redistributing connected routes

        DUT2.ospf.redistribute_connected()

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        assert "88.0.0.0" in dict_of_networks.keys() and dict_of_networks["88.0.0.0"]["Protocol"] == "O E2" and dict_of_networks["88.0.0.0"]["Metric"] == "10"
        assert "60.0.0.0" in dict_of_networks.keys() and dict_of_networks["60.0.0.0"]["Protocol"] == "O E2" and dict_of_networks["60.0.0.0"]["Metric"] == "10"
        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"

        # Redistribute with different metric

        DUT2.ospf.remove_redistribute_static()
        DUT2.ospf.redistribute_static(metric="500")

        # Redistribute with different metric

        DUT2.ospf.remove_redistribute_connected()
        DUT2.ospf.redistribute_connected(metric="500")

        time.sleep(5)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        assert "88.0.0.0" in dict_of_networks.keys() and dict_of_networks["88.0.0.0"]["Protocol"] == "O E2" and dict_of_networks["88.0.0.0"]["Metric"] == "500"
        assert "60.0.0.0" in dict_of_networks.keys() and dict_of_networks["60.0.0.0"]["Protocol"] == "O E2" and dict_of_networks["60.0.0.0"]["Metric"] == "500"
        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"

        # Remove redistribution on DUT2 and check if the connected routes are not anymore in the routing table of DUT1

        DUT2.ospf.remove_redistribute_static()
        DUT2.ospf.remove_redistribute_connected()

        time.sleep(5)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        assert "60.0.0.0" not in dict_of_networks.keys()
        assert "88.0.0.0" not in dict_of_networks.keys()
        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"

        print("########## Removing the config #############")

        DUT1.ospf.remove_networks(int_vlan20=["20.0.0.2", "0.0.0.0"])
        DUT2.ospf.remove_networks(int_vlan15=["15.0.0.1", "0.0.0.0"], int_vlan20=["20.0.0.1", "0.0.0.0"])

        DUT2.ip.remove_static_route(network_dest="88.0.0.0", mask_dest="255.255.0.0", next_hop="15.0.0.100")

        DUT1.ospf.disable_ospf()
        DUT2.ospf.disable_ospf()

        DUT1.ip.remove_int_vlan(int_vlan="20")
        DUT2.ip.remove_vlan_interfaces("20", "15", "60")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5", "Gi 0/6")

        DUT1.vl.remove_vlan(vlan="20")
        DUT2.vl.remove_vlans("20", "15", "60")

    def test_func_4(self):

        print("###### Test_func_4 ######")
        print("########## Verify if RIP routes are redistributed into OSPF #############")
        print("###### 3 DUTs ######")

        #          Topology
        #
        #  DUT1 --OSPF-- DUT2 --RIP-- DUT3 -- RIP
        #

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/4", "Gi 0/5", "Gi 0/9")
        DUT3.int.no_shut_interfaces("Gi 0/4")

        # Adding the ports to the VLAN

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")

        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/4", vlan="12")

        DUT3.vl.add_ports_to_vlan(ports="Gi 0/4", vlan="12")
        DUT3.vl.add_ports_to_vlan(ports="Gi 0/4", vlan="50")

        # Create IP interfaces on all DUTs for the specific VLANs

        DUT1.ip.add_ip_interfaces("20", int_vlan20=["20.0.0.2", "255.255.255.0"])
        DUT1.ip.no_shut_int_vlans("20")

        DUT2.ip.add_ip_interfaces("20", "15", "12", int_vlan20=["20.0.0.1", "255.255.255.0"],int_vlan15=["15.0.0.1", "255.255.255.0"],int_vlan12=["12.0.0.1", "255.255.255.0"])
        DUT2.ip.no_shut_int_vlans("12", "15", "20")

        DUT3.ip.add_ip_interfaces("50", "12", int_vlan50=["50.0.0.1", "255.255.255.0"], int_vlan12=["12.0.0.2", "255.255.255.0"])
        DUT3.ip.no_shut_int_vlans("12", "50")

        # Enable ospf on DUT1 and DUT2 and advertise the IPs

        DUT1.ospf.enable_ospf()
        DUT2.ospf.enable_ospf()

        DUT1.ospf.advertise_networks(int_vlan20=["20.0.0.2", "0.0.0.0"])
        DUT2.ospf.advertise_networks(int_vlan15=["15.0.0.1", "0.0.0.0"], int_vlan20=["20.0.0.1", "0.0.0.0"])

        # Enable rip on DUT2 and DUT3 and advertise the IPs

        DUT2.rip.enable_rip()
        DUT3.rip.enable_rip()

        DUT2.rip.advertise_networks("12.0.0.1")
        DUT3.rip.advertise_networks("12.0.0.2")
        DUT3.rip.advertise_networks("50.0.0.1")

        # Redistributing the rip routes into ospf on DUT2

        DUT2.ospf.redistribute_rip()

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        assert "50.0.0.0" in dict_of_networks.keys() and dict_of_networks["50.0.0.0"]["Protocol"] == "O E2"
        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"

        # Remove the redistribution and check that the rip routes are not present in DUT1 Routing Table

        DUT2.ospf.remove_redistribute_rip()

        time.sleep(5)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        assert "50.0.0.0" not in dict_of_networks.keys()
        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"

        print("########## Removing the config #############")

        DUT1.ospf.remove_networks(int_vlan20=["20.0.0.2", "0.0.0.0"])
        DUT2.ospf.remove_networks(int_vlan15=["15.0.0.1", "0.0.0.0"], int_vlan20=["20.0.0.1", "0.0.0.0"])

        DUT1.ospf.disable_ospf()
        DUT2.ospf.disable_ospf()

        DUT2.rip.disable_rip()
        DUT3.rip.disable_rip()

        DUT1.ip.remove_int_vlan(int_vlan="20")
        DUT2.ip.remove_vlan_interfaces("20", "15", "12")
        DUT3.ip.remove_vlan_interfaces("12", "50")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5", "Gi 0/4")
        DUT3.int.shut_interfaces("Gi 0/4")

        DUT1.vl.remove_vlan(vlan="20")
        DUT2.vl.remove_vlans("20", "15", "12")
        DUT3.vl.remove_vlans("12", "50")

    def test_func_5(self):

        print("###### Test_func_5 ######")
        print("########## Verify if a custom metric-type can be configured on routes redistributed into OSPF #############")
        print("###### 3 DUTs ######")

        #          Topology
        #
        #  DUT1 --OSPF-- DUT2 --RIP-- DUT3 -- RIP
        #

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/4", "Gi 0/5", "Gi 0/9")
        DUT3.int.no_shut_interfaces("Gi 0/4")

        # Adding the ports to the VLAN

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")

        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/4", vlan="12")

        DUT3.vl.add_ports_to_vlan(ports="Gi 0/4", vlan="12")
        DUT3.vl.add_ports_to_vlan(ports="Gi 0/4", vlan="50")

        # Create IP interfaces on all DUTs for the specific VLANs

        DUT1.ip.add_ip_interfaces("20", int_vlan20=["20.0.0.2", "255.255.255.0"])
        DUT1.ip.no_shut_int_vlans("20")

        DUT2.ip.add_ip_interfaces("20", "15", "12", int_vlan20=["20.0.0.1", "255.255.255.0"],int_vlan15=["15.0.0.1", "255.255.255.0"],int_vlan12=["12.0.0.1", "255.255.255.0"])
        DUT2.ip.no_shut_int_vlans("12", "15", "20")

        DUT3.ip.add_ip_interfaces("50", "12", int_vlan50=["50.0.0.1", "255.255.255.0"], int_vlan12=["12.0.0.2", "255.255.255.0"])
        DUT3.ip.no_shut_int_vlans("12", "50")

        # Enable ospf on all DUTs and advertise the IPs

        DUT1.ospf.enable_ospf()
        DUT2.ospf.enable_ospf()

        DUT1.ospf.advertise_networks(int_vlan20=["20.0.0.2", "0.0.0.0"])
        DUT2.ospf.advertise_networks(int_vlan15=["15.0.0.1", "0.0.0.0"], int_vlan20=["20.0.0.1", "0.0.0.0"])

        # Enable rip on DUT2 and DUT3 and advertise the IPs

        DUT2.rip.enable_rip()
        DUT3.rip.enable_rip()

        DUT2.rip.advertise_networks("12.0.0.1")
        DUT3.rip.advertise_networks("12.0.0.2")
        DUT3.rip.advertise_networks("50.0.0.1")

        # Redistributing the rip routes into ospf on DUT2 with metric-type 1

        DUT2.ospf.redistribute_rip(metric_type="1")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        assert "50.0.0.0" in dict_of_networks.keys() and dict_of_networks["50.0.0.0"]["Protocol"] == "O E1"
        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"

        # Change the metric-type of the redistributed routes to the default

        DUT2.ospf.remove_redistribute_rip()
        DUT2.ospf.redistribute_rip()

        time.sleep(5)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        assert "50.0.0.0" in dict_of_networks.keys() and dict_of_networks["50.0.0.0"]["Protocol"] == "O E2"
        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"

        # Remove the redistribution and check that the rip routes are not present in DUT1 Routing Table

        DUT2.ospf.remove_redistribute_rip()

        time.sleep(5)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        assert "50.0.0.0" not in dict_of_networks.keys()
        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"

        print("########## Removing the config #############")

        DUT1.ospf.remove_networks(int_vlan20=["20.0.0.2", "0.0.0.0"])
        DUT2.ospf.remove_networks(int_vlan15=["15.0.0.1", "0.0.0.0"], int_vlan20=["20.0.0.1", "0.0.0.0"])

        DUT1.ospf.disable_ospf()
        DUT2.ospf.disable_ospf()

        DUT2.rip.disable_rip()
        DUT3.rip.disable_rip()

        DUT1.ip.remove_int_vlan(int_vlan="20")
        DUT2.ip.remove_vlan_interfaces("20", "15", "12")
        DUT3.ip.remove_vlan_interfaces("12", "50")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5", "Gi 0/4")
        DUT3.int.shut_interfaces("Gi 0/4")

        DUT1.vl.remove_vlan(vlan="20")
        DUT2.vl.remove_vlans("20", "15", "12")
        DUT3.vl.remove_vlans("12", "50")

    def test_func_6(self):

        print("###### Test_func_6 ######")
        print("########## Verify OSPF simple text Authentication  #############")
        print("###### 2 DUTs ######")

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/5", "Gi 0/9")

        # Adding the ports to the VLAN

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")

        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")

        # Create IP interfaces on all DUTs for the specific VLANs

        DUT1.ip.add_ip_interfaces("20", int_vlan20=["20.0.0.2", "255.255.255.0"])
        DUT1.ip.no_shut_int_vlans("20")

        DUT2.ip.add_ip_interfaces("20", "15", int_vlan20=["20.0.0.1", "255.255.255.0"], int_vlan15=["15.0.0.1", "255.255.255.0"])
        DUT2.ip.no_shut_int_vlans("15", "20")

        # Enable ospf on all DUTs and advertise the IPs

        DUT1.ospf.enable_ospf()
        DUT2.ospf.enable_ospf()

        DUT1.ospf.advertise_networks(int_vlan20=["20.0.0.2", "0.0.0.0"])
        DUT2.ospf.advertise_networks(int_vlan15=["15.0.0.1", "0.0.0.0"], int_vlan20=["20.0.0.1", "0.0.0.0"])

        # Configure the authentication on the int-vlan between the DUTs and configure the key. Check that the adjancency occurs

        DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="simple",authentication_key="1234")
        DUT2.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="simple", authentication_key="1234")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"
        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2
        assert "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]

        # Change the key for DUT1 and check that there is no adjacency and the routes are not installed

        DUT1.ospf.add_ip_ospf_authentication_key(int_vlan="20", authentication_key="12345")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert "15.0.0.0" not in dict_of_networks.keys()
        assert ip_session_2 not in dict_of_ospf_neighbors.keys()

        # Change the key for DUT2 and check that there is adjacency and the routes are learned

        DUT2.ospf.add_ip_ospf_authentication_key(int_vlan="20", authentication_key="12345")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"
        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2
        assert "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]

        # Remove the authentication and authentication-keys on both DUTs and check that there is adjancency and the routes are learned

        DUT1.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20")

        DUT2.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT2.ospf.remove_ip_ospf_authentication_key(int_vlan="20")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"
        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2
        assert "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]

        print("########## Removing the config #############")

        DUT1.ospf.remove_networks(int_vlan20=["20.0.0.2", "0.0.0.0"])
        DUT2.ospf.remove_networks(int_vlan15=["15.0.0.1", "0.0.0.0"], int_vlan20=["20.0.0.1", "0.0.0.0"])

        DUT1.ospf.disable_ospf()
        DUT2.ospf.disable_ospf()

        DUT1.ip.remove_int_vlan(int_vlan="20")
        DUT2.ip.remove_vlan_interfaces("20", "15")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5")

        DUT1.vl.remove_vlan(vlan="20")
        DUT2.vl.remove_vlans("20", "15")

    def test_func_7(self):

        print("###### Test_func_7 ######")
        print("########## Verify OSPF Message-Digest Authentication  #############")
        print("###### 2 DUTs ######")

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/5", "Gi 0/9")

        # Adding the ports to the VLAN

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")

        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")

        # Create IP interfaces on all DUTs for the specific VLANs

        DUT1.ip.add_ip_interfaces("20", int_vlan20=["20.0.0.2", "255.255.255.0"])
        DUT1.ip.no_shut_int_vlans("20")

        DUT2.ip.add_ip_interfaces("20", "15", int_vlan20=["20.0.0.1", "255.255.255.0"], int_vlan15=["15.0.0.1", "255.255.255.0"])
        DUT2.ip.no_shut_int_vlans("15", "20")

        # Enable ospf on all DUTs and advertise the IPs

        DUT1.ospf.enable_ospf()
        DUT2.ospf.enable_ospf()

        DUT1.ospf.advertise_networks(int_vlan20=["20.0.0.2", "0.0.0.0"])
        DUT2.ospf.advertise_networks(int_vlan15=["15.0.0.1", "0.0.0.0"], int_vlan20=["20.0.0.1", "0.0.0.0"])

        # Configure the authentication md5 on the int-vlan between the DUTs and configure the key. Check that the adjancency occurs

        DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="md5", authentication_key="1234", message_digest_key="1", message_digest="Yes")
        DUT2.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="md5", authentication_key="1234", message_digest_key="1", message_digest="Yes")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"
        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2
        assert "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]

        # Change the key for DUT1 and check that there is no adjacency and the routes are not installed

        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")
        DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="md5", authentication_key="12345", message_digest_key="1",message_digest="Yes")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert "15.0.0.0" not in dict_of_networks.keys()
        assert ip_session_2 in dict_of_ospf_neighbors.keys() and "DOWN" in dict_of_ospf_neighbors[ip_session_2]["State"]

        # Change the key for DUT2 and check that there is adjacency and the routes are learned

        DUT2.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")
        DUT2.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="md5", authentication_key="12345",message_digest_key="1", message_digest="Yes")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"
        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2
        assert "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]

        # Remove the authentication and authentication-keys on both DUTs and check that there is adjancency and the routes are learned

        DUT1.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")

        DUT2.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT2.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"
        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2
        assert "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]

        print("########## Removing the config #############")

        DUT1.ospf.remove_networks(int_vlan20=["20.0.0.2", "0.0.0.0"])
        DUT2.ospf.remove_networks(int_vlan15=["15.0.0.1", "0.0.0.0"], int_vlan20=["20.0.0.1", "0.0.0.0"])

        DUT1.ospf.disable_ospf()
        DUT2.ospf.disable_ospf()

        DUT1.ip.remove_int_vlan(int_vlan="20")
        DUT2.ip.remove_vlan_interfaces("20", "15")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5")

        DUT1.vl.remove_vlan(vlan="20")
        DUT2.vl.remove_vlans("20", "15")

    def test_func_8(self):

        print("###### Test_func_8 ######")
        print("########## Verify OSPF  Authentication using SHA-1 algorithm  #############")
        print("###### 2 DUTs ######")

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/5", "Gi 0/9")

        # Adding the ports to the VLAN

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")

        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")

        # Create IP interfaces on all DUTs for the specific VLANs

        DUT1.ip.add_ip_interfaces("20", int_vlan20=["20.0.0.2", "255.255.255.0"])
        DUT1.ip.no_shut_int_vlans("20")

        DUT2.ip.add_ip_interfaces("20", "15", int_vlan20=["20.0.0.1", "255.255.255.0"], int_vlan15=["15.0.0.1", "255.255.255.0"])
        DUT2.ip.no_shut_int_vlans("15", "20")

        # Enable ospf on all DUTs and advertise the IPs

        DUT1.ospf.enable_ospf()
        DUT2.ospf.enable_ospf()

        DUT1.ospf.advertise_networks(int_vlan20=["20.0.0.2", "0.0.0.0"])
        DUT2.ospf.advertise_networks(int_vlan15=["15.0.0.1", "0.0.0.0"], int_vlan20=["20.0.0.1", "0.0.0.0"])

        # Configure the authentication sha-1 on the int-vlan between the DUTs and configure the key. Check that the adjancency occurs

        DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-1", authentication_key="1234", message_digest_key="1")
        DUT2.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-1", authentication_key="1234", message_digest_key="1")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"
        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2
        assert "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]

        # Change the key for DUT1 and check that there is no adjacency and the routes are not installed

        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")
        DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-1", authentication_key="12345", message_digest_key="1")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert "15.0.0.0" not in dict_of_networks.keys()
        assert ip_session_2 in dict_of_ospf_neighbors.keys() and "DOWN" in dict_of_ospf_neighbors[ip_session_2]["State"]

        # Change the key for DUT2 and check that there is adjacency and the routes are learned

        DUT2.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")
        DUT2.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-1", authentication_key="12345",message_digest_key="1")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"
        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2
        assert "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]

        # Remove the authentication and authentication-keys on both DUTs and check that there is adjancency and the routes are learned

        DUT1.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")

        DUT2.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT2.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"
        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2
        assert "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]

        print("########## Removing the config #############")

        DUT1.ospf.remove_networks(int_vlan20=["20.0.0.2", "0.0.0.0"])
        DUT2.ospf.remove_networks(int_vlan15=["15.0.0.1", "0.0.0.0"], int_vlan20=["20.0.0.1", "0.0.0.0"])

        DUT1.ospf.disable_ospf()
        DUT2.ospf.disable_ospf()

        DUT1.ip.remove_int_vlan(int_vlan="20")
        DUT2.ip.remove_vlan_interfaces("20", "15")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5")

        DUT1.vl.remove_vlan(vlan="20")
        DUT2.vl.remove_vlans("20", "15")

    def test_func_9(self):

        print("###### Test_func_9 ######")
        print("########## Verify OSPF  Authentication using SHA-224 algorithm  #############")
        print("###### 2 DUTs ######")

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/5", "Gi 0/9")

        # Adding the ports to the VLAN

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")

        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")

        # Create IP interfaces on all DUTs for the specific VLANs

        DUT1.ip.add_ip_interfaces("20", int_vlan20=["20.0.0.2", "255.255.255.0"])
        DUT1.ip.no_shut_int_vlans("20")

        DUT2.ip.add_ip_interfaces("20", "15", int_vlan20=["20.0.0.1", "255.255.255.0"], int_vlan15=["15.0.0.1", "255.255.255.0"])
        DUT2.ip.no_shut_int_vlans("15", "20")

        # Enable ospf on all DUTs and advertise the IPs

        DUT1.ospf.enable_ospf()
        DUT2.ospf.enable_ospf()

        DUT1.ospf.advertise_networks(int_vlan20=["20.0.0.2", "0.0.0.0"])
        DUT2.ospf.advertise_networks(int_vlan15=["15.0.0.1", "0.0.0.0"], int_vlan20=["20.0.0.1", "0.0.0.0"])

        # Configure the authentication sha-224 on the int-vlan between the DUTs and configure the key. Check that the adjancency occurs

        DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-224", authentication_key="1234", message_digest_key="1")
        DUT2.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-224", authentication_key="1234", message_digest_key="1")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"
        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2
        assert "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]

        # Change the key for DUT1 and check that there is no adjacency and the routes are not installed

        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")
        DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-224", authentication_key="12345", message_digest_key="1")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert "15.0.0.0" not in dict_of_networks.keys()
        assert ip_session_2 in dict_of_ospf_neighbors.keys() and "DOWN" in dict_of_ospf_neighbors[ip_session_2]["State"]

        # Change the key for DUT2 and check that there is adjacency and the routes are learned

        DUT2.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")
        DUT2.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-224", authentication_key="12345",message_digest_key="1")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"
        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2
        assert "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]

        # Remove the authentication and authentication-keys on both DUTs and check that there is adjancency and the routes are learned

        DUT1.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")

        DUT2.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT2.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"
        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2
        assert "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]

        print("########## Removing the config #############")

        DUT1.ospf.remove_networks(int_vlan20=["20.0.0.2", "0.0.0.0"])
        DUT2.ospf.remove_networks(int_vlan15=["15.0.0.1", "0.0.0.0"], int_vlan20=["20.0.0.1", "0.0.0.0"])

        DUT1.ospf.disable_ospf()
        DUT2.ospf.disable_ospf()

        DUT1.ip.remove_int_vlan(int_vlan="20")
        DUT2.ip.remove_vlan_interfaces("20", "15")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5")

        DUT1.vl.remove_vlan(vlan="20")
        DUT2.vl.remove_vlans("20", "15")

    def test_func_10(self):

        print("###### Test_func_10 ######")
        print("########## Verify OSPF  Authentication using SHA-256 algorithm  #############")
        print("###### 2 DUTs ######")

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/5", "Gi 0/9")

        # Adding the ports to the VLAN

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")

        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")

        # Create IP interfaces on all DUTs for the specific VLANs

        DUT1.ip.add_ip_interfaces("20", int_vlan20=["20.0.0.2", "255.255.255.0"])
        DUT1.ip.no_shut_int_vlans("20")

        DUT2.ip.add_ip_interfaces("20", "15", int_vlan20=["20.0.0.1", "255.255.255.0"], int_vlan15=["15.0.0.1", "255.255.255.0"])
        DUT2.ip.no_shut_int_vlans("15", "20")

        # Enable ospf on all DUTs and advertise the IPs

        DUT1.ospf.enable_ospf()
        DUT2.ospf.enable_ospf()

        DUT1.ospf.advertise_networks(int_vlan20=["20.0.0.2", "0.0.0.0"])
        DUT2.ospf.advertise_networks(int_vlan15=["15.0.0.1", "0.0.0.0"], int_vlan20=["20.0.0.1", "0.0.0.0"])

        # Configure the authentication sha-256 on the int-vlan between the DUTs and configure the key. Check that the adjancency occurs

        DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-256", authentication_key="1234", message_digest_key="1")
        DUT2.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-256", authentication_key="1234", message_digest_key="1")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"
        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2
        assert "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]

        # Change the key for DUT1 and check that there is no adjacency and the routes are not installed

        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")
        DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-256", authentication_key="12345", message_digest_key="1")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert "15.0.0.0" not in dict_of_networks.keys()
        assert ip_session_2 in dict_of_ospf_neighbors.keys() and "DOWN" in dict_of_ospf_neighbors[ip_session_2]["State"]

        # Change the key for DUT2 and check that there is adjacency and the routes are learned

        DUT2.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")
        DUT2.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-256", authentication_key="12345",message_digest_key="1")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"
        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2
        assert "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]

        # Remove the authentication and authentication-keys on both DUTs and check that there is adjancency and the routes are learned

        DUT1.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")

        DUT2.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT2.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"
        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2
        assert "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]

        print("########## Removing the config #############")

        DUT1.ospf.remove_networks(int_vlan20=["20.0.0.2", "0.0.0.0"])
        DUT2.ospf.remove_networks(int_vlan15=["15.0.0.1", "0.0.0.0"], int_vlan20=["20.0.0.1", "0.0.0.0"])

        DUT1.ospf.disable_ospf()
        DUT2.ospf.disable_ospf()

        DUT1.ip.remove_int_vlan(int_vlan="20")
        DUT2.ip.remove_vlan_interfaces("20", "15")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5")

        DUT1.vl.remove_vlan(vlan="20")
        DUT2.vl.remove_vlans("20", "15")

    def test_func_11(self):

        print("###### Test_func_11 ######")
        print("########## Verify OSPF  Authentication using SHA-384 algorithm  #############")
        print("###### 2 DUTs ######")

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/5", "Gi 0/9")

        # Adding the ports to the VLAN

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")

        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")

        # Create IP interfaces on all DUTs for the specific VLANs

        DUT1.ip.add_ip_interfaces("20", int_vlan20=["20.0.0.2", "255.255.255.0"])
        DUT1.ip.no_shut_int_vlans("20")

        DUT2.ip.add_ip_interfaces("20", "15", int_vlan20=["20.0.0.1", "255.255.255.0"], int_vlan15=["15.0.0.1", "255.255.255.0"])
        DUT2.ip.no_shut_int_vlans("15", "20")

        # Enable ospf on all DUTs and advertise the IPs

        DUT1.ospf.enable_ospf()
        DUT2.ospf.enable_ospf()

        DUT1.ospf.advertise_networks(int_vlan20=["20.0.0.2", "0.0.0.0"])
        DUT2.ospf.advertise_networks(int_vlan15=["15.0.0.1", "0.0.0.0"], int_vlan20=["20.0.0.1", "0.0.0.0"])

        # Configure the authentication sha-384 on the int-vlan between the DUTs and configure the key. Check that the adjancency occurs

        DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-384", authentication_key="1234", message_digest_key="1")
        DUT2.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-384", authentication_key="1234", message_digest_key="1")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"
        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2
        assert "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]

        # Change the key for DUT1 and check that there is no adjacency and the routes are not installed

        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")
        DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-384", authentication_key="12345", message_digest_key="1")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert "15.0.0.0" not in dict_of_networks.keys()
        assert ip_session_2 in dict_of_ospf_neighbors.keys() and "DOWN" in dict_of_ospf_neighbors[ip_session_2]["State"]

        # Change the key for DUT2 and check that there is adjacency and the routes are learned

        DUT2.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")
        DUT2.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-384", authentication_key="12345", message_digest_key="1")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"
        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2
        assert "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]

        # Remove the authentication and authentication-keys on both DUTs and check that there is adjancency and the routes are learned

        DUT1.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")

        DUT2.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT2.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"
        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2
        assert "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]

        print("########## Removing the config #############")

        DUT1.ospf.remove_networks(int_vlan20=["20.0.0.2", "0.0.0.0"])
        DUT2.ospf.remove_networks(int_vlan15=["15.0.0.1", "0.0.0.0"], int_vlan20=["20.0.0.1", "0.0.0.0"])

        DUT1.ospf.disable_ospf()
        DUT2.ospf.disable_ospf()

        DUT1.ip.remove_int_vlan(int_vlan="20")
        DUT2.ip.remove_vlan_interfaces("20", "15")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5")

        DUT1.vl.remove_vlan(vlan="20")
        DUT2.vl.remove_vlans("20", "15")

    def test_func_12(self):

        print("###### Test_func_12 ######")
        print("########## Verify OSPF  Authentication using SHA-512 algorithm  #############")
        print("###### 2 DUTs ######")

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/5", "Gi 0/9")

        # Adding the ports to the VLAN

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")

        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")

        # Create IP interfaces on all DUTs for the specific VLANs

        DUT1.ip.add_ip_interfaces("20", int_vlan20=["20.0.0.2", "255.255.255.0"])
        DUT1.ip.no_shut_int_vlans("20")

        DUT2.ip.add_ip_interfaces("20", "15", int_vlan20=["20.0.0.1", "255.255.255.0"], int_vlan15=["15.0.0.1", "255.255.255.0"])
        DUT2.ip.no_shut_int_vlans("15", "20")

        # Enable ospf on all DUTs and advertise the IPs

        DUT1.ospf.enable_ospf()
        DUT2.ospf.enable_ospf()

        DUT1.ospf.advertise_networks(int_vlan20=["20.0.0.2", "0.0.0.0"])
        DUT2.ospf.advertise_networks(int_vlan15=["15.0.0.1", "0.0.0.0"], int_vlan20=["20.0.0.1", "0.0.0.0"])

        # Configure the authentication sha-512 on the int-vlan between the DUTs and configure the key. Check that the adjancency occurs

        DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-512", authentication_key="1234", message_digest_key="1")
        DUT2.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-512", authentication_key="1234", message_digest_key="1")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"
        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2
        assert "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]

        # Change the key for DUT1 and check that there is no adjacency and the routes are not installed

        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")
        DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-512", authentication_key="12345", message_digest_key="1")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert "15.0.0.0" not in dict_of_networks.keys()
        assert ip_session_2 in dict_of_ospf_neighbors.keys() and "DOWN" in dict_of_ospf_neighbors[ip_session_2]["State"]

        # Change the key for DUT2 and check that there is adjacency and the routes are learned

        DUT2.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")
        DUT2.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-512", authentication_key="12345",message_digest_key="1")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"
        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2
        assert "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]

        # Remove the authentication and authentication-keys on both DUTs and check that there is adjancency and the routes are learned

        DUT1.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")

        DUT2.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT2.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"
        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2
        assert "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]

        print("########## Removing the config #############")

        DUT1.ospf.remove_networks(int_vlan20=["20.0.0.2", "0.0.0.0"])
        DUT2.ospf.remove_networks(int_vlan15=["15.0.0.1", "0.0.0.0"], int_vlan20=["20.0.0.1", "0.0.0.0"])

        DUT1.ospf.disable_ospf()
        DUT2.ospf.disable_ospf()

        DUT1.ip.remove_int_vlan(int_vlan="20")
        DUT2.ip.remove_vlan_interfaces("20", "15")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5")

        DUT1.vl.remove_vlan(vlan="20")
        DUT2.vl.remove_vlans("20", "15")

    def test_func_13(self):

        print("###### Test_func_13 ######")
        print("########## Verify if OSPF adjacency cannot be formed when Secret Key ID is different  #############")
        print("###### 2 DUTs ######")

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/5", "Gi 0/9")

        # Adding the ports to the VLAN

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")

        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")

        # Create IP interfaces on all DUTs for the specific VLANs

        DUT1.ip.add_ip_interfaces("20", int_vlan20=["20.0.0.2", "255.255.255.0"])
        DUT1.ip.no_shut_int_vlans("20")

        DUT2.ip.add_ip_interfaces("20", "15", int_vlan20=["20.0.0.1", "255.255.255.0"], int_vlan15=["15.0.0.1", "255.255.255.0"])
        DUT2.ip.no_shut_int_vlans("15", "20")

        # Enable ospf on all DUTs and advertise the IPs

        DUT1.ospf.enable_ospf()
        DUT2.ospf.enable_ospf()

        DUT1.ospf.advertise_networks(int_vlan20=["20.0.0.2", "0.0.0.0"])
        DUT2.ospf.advertise_networks(int_vlan15=["15.0.0.1", "0.0.0.0"], int_vlan20=["20.0.0.1", "0.0.0.0"])

        # Configure the authentication sha-384 on the int-vlan between the DUTs and configure the key. Check that the adjencency occurs

        DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-384", authentication_key="1234", message_digest_key="1")
        DUT2.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-384", authentication_key="12345", message_digest_key="1")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert "15.0.0.0" not in dict_of_networks.keys()
        assert ip_session_2 in dict_of_ospf_neighbors.keys() and "DOWN" in dict_of_ospf_neighbors[ip_session_2]["State"]

        # Change the key for DUT1 and check that the adjacency is restarted

        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")
        DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-384", authentication_key="12345", message_digest_key="1")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"
        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2
        assert "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]

        print("########## Removing the config #############")

        DUT1.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")

        DUT2.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT2.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")

        DUT1.ospf.remove_networks(int_vlan20=["20.0.0.2", "0.0.0.0"])
        DUT2.ospf.remove_networks(int_vlan15=["15.0.0.1", "0.0.0.0"], int_vlan20=["20.0.0.1", "0.0.0.0"])

        DUT1.ospf.disable_ospf()
        DUT2.ospf.disable_ospf()

        DUT1.ip.remove_int_vlan(int_vlan="20")
        DUT2.ip.remove_vlan_interfaces("20", "15")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5")

        DUT1.vl.remove_vlan(vlan="20")
        DUT2.vl.remove_vlans("20", "15")

    def test_func_14(self):

        print("###### Test_func_14 ######")
        print("########## Verify if sha-keys and md5 keys are not displayed in show running config  #############")
        print("###### 1 DUT ######")

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/9")

        # Adding the ports to the VLAN

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")

        # Create IP interfaces on all DUTs for the specific VLANs

        DUT1.ip.add_ip_interfaces("20", int_vlan20=["20.0.0.2", "255.255.255.0"])
        DUT1.ip.no_shut_int_vlans("20")

        # Enable ospf on all DUTs and advertise the IPs

        DUT1.ospf.enable_ospf()

        DUT1.ospf.advertise_networks(int_vlan20=["20.0.0.2", "0.0.0.0"])

        # Configure the authentication sha-384 on the int-vlan between the DUTs and configure the key. Check the key is not shown in the running-config

        DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-384", authentication_key="1234", message_digest_key="1")

        dict_key, dict_of_keys = DUT1.ospf.show_run_ospf_key()
        print(dict_key,  "-------", dict_of_keys)

        assert dict_of_keys['key 1']['Authentication'] == 'sha-384'
        assert "1234" not in dict_of_keys['key 1']['key_Text']

        DUT1.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20",message_digest_key="1")

        # Check the running config for md5 key

        # DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="md5", authentication_key="12345",message_digest_key="1", message_digest="Yes")

        dict_key, dict_of_keys = DUT1.ospf.show_run_ospf_key()
        print(dict_key, dict_of_keys)

        assert dict_of_keys['key 1']['Authentication'] == 'md5'
        assert "12345" not in dict_of_keys['key 1']['key_Text']

        DUT1.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")

        print("########## Removing the config #############")

        DUT1.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")

        DUT1.ospf.remove_networks(int_vlan20=["20.0.0.2", "0.0.0.0"])

        DUT1.ospf.disable_ospf()

        DUT1.ip.remove_int_vlan(int_vlan="20")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9")

        DUT1.vl.remove_vlan(vlan="20")

    def test_func_15(self):

        print("###### Test_func_15 ######")
        print("########## Verify if OSPF can use multiple keys for authentication  #############")
        print("###### 2 DUTs ######")

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/5", "Gi 0/9")

        # Adding the ports to the VLAN

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")

        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")

        # Create IP interfaces on all DUTs for the specific VLANs

        DUT1.ip.add_ip_interfaces("20", int_vlan20=["20.0.0.2", "255.255.255.0"])
        DUT1.ip.no_shut_int_vlans("20")

        DUT2.ip.add_ip_interfaces("20", "15", int_vlan20=["20.0.0.1", "255.255.255.0"], int_vlan15=["15.0.0.1", "255.255.255.0"])
        DUT2.ip.no_shut_int_vlans("15", "20")

        # Enable ospf on all DUTs and advertise the IPs

        DUT1.ospf.enable_ospf()
        DUT2.ospf.enable_ospf()

        DUT1.ospf.advertise_networks(int_vlan20=["20.0.0.2", "0.0.0.0"])
        DUT2.ospf.advertise_networks(int_vlan15=["15.0.0.1", "0.0.0.0"], int_vlan20=["20.0.0.1", "0.0.0.0"])

        # Configure 3 keys for the authentication sha-224 on the int-vlan between the DUTs. Check the keys that are installed

        DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-224", authentication_key="key1", message_digest_key="1")
        DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-224", authentication_key="key2", message_digest_key="2")
        DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-224", authentication_key="key3", message_digest_key="3")

        dict_key, dict_of_keys = DUT1.ospf.show_run_ospf_key()
        print(dict_key, dict_of_keys)

        assert "key 1" in dict_of_keys.keys()
        assert "key 2" in dict_of_keys.keys()
        assert "key 3" in dict_of_keys.keys()

        DUT2.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-224", authentication_key="key1",message_digest_key="1")
        DUT2.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-224", authentication_key="key2",message_digest_key="2")
        DUT2.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-224", authentication_key="key3",message_digest_key="3")

        dict_key, dict_of_keys = DUT1.ospf.show_run_ospf_key()
        print(dict_key, dict_of_keys)

        assert "key 1" in dict_of_keys.keys()
        assert "key 2" in dict_of_keys.keys()
        assert "key 3" in dict_of_keys.keys()

        time.sleep(45)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2 and "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]

        # Remove the third key on both DUTs and check the adjacency is established

        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20",message_digest_key="3")
        DUT2.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="3")

        time.sleep(45)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        dict_key, dict_of_keys = DUT1.ospf.show_run_ospf_key()
        print(dict_key, dict_of_keys)

        assert "key 1" in dict_of_keys.keys()
        assert "key 2" in dict_of_keys.keys()
        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2 and "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]

        # Remove the second key on both DUTs and check the adjacency is established

        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="2")
        DUT2.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="2")

        time.sleep(45)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        dict_key, dict_of_keys = DUT1.ospf.show_run_ospf_key()
        print(dict_key, dict_of_keys)

        assert "key 1" in dict_of_keys.keys()
        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2 and "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]

        print("########## Removing the config #############")

        DUT1.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")

        DUT2.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT2.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")

        DUT1.ospf.remove_networks(int_vlan20=["20.0.0.2", "0.0.0.0"])
        DUT2.ospf.remove_networks(int_vlan15=["15.0.0.1", "0.0.0.0"], int_vlan20=["20.0.0.1", "0.0.0.0"])

        DUT1.ospf.disable_ospf()
        DUT2.ospf.disable_ospf()

        DUT1.ip.remove_int_vlan(int_vlan="20")
        DUT2.ip.remove_vlan_interfaces("20", "15")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5")

        DUT1.vl.remove_vlan(vlan="20")
        DUT2.vl.remove_vlans("20", "15")

    def test_func_16(self):

        print("###### Test_func_16 ######")
        print("########## Verify that the OSPF neighbor adjacency can not be established when neighbors are in different Areas  #############")
        print("###### 2 DUTs ######")

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/5", "Gi 0/9")

        # Adding the ports to the VLAN

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")

        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")

        # Create IP interfaces on all DUTs for the specific VLANs

        DUT1.ip.add_ip_interfaces("20", int_vlan20=["20.0.0.2", "255.255.255.0"])
        DUT1.ip.no_shut_int_vlans("20")

        DUT2.ip.add_ip_interfaces("20", "15", int_vlan20=["20.0.0.1", "255.255.255.0"],int_vlan15=["15.0.0.1", "255.255.255.0"])
        DUT2.ip.no_shut_int_vlans("15", "20")

        # Enable ospf on all DUTs and advertise the IPs in different areas

        DUT1.ospf.enable_ospf()
        DUT2.ospf.enable_ospf()

        DUT1.ospf.advertise_networks(int_vlan20=["20.0.0.2", "0.0.0.1"])
        DUT2.ospf.advertise_networks(int_vlan15=["15.0.0.1", "0.0.0.0"], int_vlan20=["20.0.0.1", "0.0.0.0"])

        time.sleep(45)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        assert ip_session_2 not in dict_of_ospf_neighbors.keys()
        assert  "15.0.0.0" not in dict_of_networks.keys()

        # Configure on DUT2 area 0.0.0.1 and check the adjacency is established

        DUT2.ospf.remove_networks(int_vlan20=["20.0.0.1", "0.0.0.1"])
        DUT2.ospf.advertise_networks(int_vlan20=["20.0.0.1", "0.0.0.1"])

        time.sleep(45)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2 and "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]
        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O IA"

        print("########## Removing the config #############")

        DUT1.ospf.remove_networks(int_vlan20=["20.0.0.2", "0.0.0.1"])
        DUT2.ospf.remove_networks(int_vlan15=["15.0.0.1", "0.0.0.0"], int_vlan20=["20.0.0.1", "0.0.0.1"])

        DUT1.ospf.disable_ospf()
        DUT2.ospf.disable_ospf()

        DUT1.ip.remove_int_vlan(int_vlan="20")
        DUT2.ip.remove_vlan_interfaces("20", "15")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5")

        DUT1.vl.remove_vlan(vlan="20")
        DUT2.vl.remove_vlans("20", "15")

    def test_func_17(self):

        print("###### Test_func_17 ######")
        print("########## Verify that the OSPF neighbor adjacency can be established with both neighbors set to same hello-interval settings but different than the default values  #############")
        print("###### 2 DUTs ######")

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/5", "Gi 0/9")

        # Adding the ports to the VLAN

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")

        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")

        # Create IP interfaces on all DUTs for the specific VLANs

        DUT1.ip.add_ip_interfaces("20", int_vlan20=["20.0.0.2", "255.255.255.0"])
        DUT1.ip.no_shut_int_vlans("20")

        DUT2.ip.add_ip_interfaces("20", "15", int_vlan20=["20.0.0.1", "255.255.255.0"],int_vlan15=["15.0.0.1", "255.255.255.0"])
        DUT2.ip.no_shut_int_vlans("15", "20")

        # Enable ospf on all DUTs and advertise the IPs

        DUT1.ospf.enable_ospf()
        DUT2.ospf.enable_ospf()

        DUT1.ospf.advertise_networks(int_vlan20=["20.0.0.2", "0.0.0.0"])
        DUT2.ospf.advertise_networks(int_vlan15=["15.0.0.1", "0.0.0.0"], int_vlan20=["20.0.0.1", "0.0.0.0"])

        time.sleep(45)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2 and "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]
        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"

        # Configure on DUT1 other ospf hello interval and check that after the time expire, the connection is not established anymore

        DUT1.ospf.add_ip_ospf_hello_interval(int_vlan="20", interval="2")

        time.sleep(45)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        assert ip_session_2 not in dict_of_ospf_neighbors.keys()
        assert  "15.0.0.0" not in dict_of_networks.keys()

        # Configure on DUT2 the same ospf hello interval and check the adjacency is established.

        DUT2.ospf.add_ip_ospf_hello_interval(int_vlan="20", interval="2")

        time.sleep(45)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2 and "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]
        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"

        print("########## Removing the config #############")

        DUT1.ospf.remove_ip_ospf_hello_interval(int_vlan="20")
        DUT2.ospf.remove_ip_ospf_hello_interval(int_vlan="20")

        DUT1.ospf.remove_networks(int_vlan20=["20.0.0.2", "0.0.0.0"])
        DUT2.ospf.remove_networks(int_vlan15=["15.0.0.1", "0.0.0.0"], int_vlan20=["20.0.0.1", "0.0.0.0"])

        DUT1.ospf.disable_ospf()
        DUT2.ospf.disable_ospf()

        DUT1.ip.remove_int_vlan(int_vlan="20")
        DUT2.ip.remove_vlan_interfaces("20", "15")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5")

        DUT1.vl.remove_vlan(vlan="20")
        DUT2.vl.remove_vlans("20", "15")

    def test_func_18(self):

        # LOKI-4711 Customer - OSPF route is missing after fail over on router port

        print("###### Test_func_18 ######")
        print("########## Check if we can advertise networks into OSPF and it establish connection using routed ports  #############")
        print("###### 3 DUTs ######")

        # #      Topology
        # #
        # #        Area 0
        # #
        # # -- DUT1 ---- DUT2
        # #       \      /
        # #        \    /
        # #         DUT3
        # #
        #
        # # Creating routed ports on all DUTs
        #
        # DUT1.int.add_routed_ports("Ex 0/2", "Gi 0/10")
        # DUT2.int.add_routed_ports("Gi 0/3", "Gi 0/10")
        # DUT3.int.add_routed_ports("Gi 0/3", "Gi 0/10")
        #
        # # No shutting the interfaces
        #
        # DUT1.int.no_shut_interfaces("Ex 0/2", "Gi 0/10")
        # DUT2.int.no_shut_interfaces("Gi 0/3", "Gi 0/5", "Gi 0/10")
        # DUT3.int.no_shut_interfaces("Gi 0/3", "Gi 0/10")
        #
        # # Creating the VLAN on DUT2
        #
        # DUT2.vl.create_vlan(vlan="15")
        #
        # # Adding the ports to the VLAN
        #
        # DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
        #
        # # Create IP Routed Ports on all DUTs
        #
        # DUT1.ip.add_ip_routed_ports("Ex 0/2", "Gi 0/10", Ex_0_2=["14.0.0.2", "255.255.255.0"], Gi_0_10=["13.0.0.2", "255.255.255.0"])
        #
        # DUT2.ip.add_ip_routed_ports("Gi 0/3", "Gi 0/10", Gi_0_3=["12.0.0.1", "255.255.255.0"], Gi_0_10=["14.0.0.1", "255.255.255.0"])
        # DUT2.ip.add_ip_interface(int_vlan="15", ip="15.0.0.1", mask="255.255.255.0")
        # DUT2.ip.no_shut_int_vlan(int_vlan="15")
        #
        # DUT3.ip.add_ip_routed_ports("Gi 0/3", "Gi 0/10", Gi_0_3=["12.0.0.2", "255.255.255.0"], Gi_0_10=["13.0.0.1", "255.255.255.0"])
        #
        # # Enable OSPF on all DUTs and advertise the IPs
        #
        # DUT1.ospf.enable_ospf()
        # DUT2.ospf.enable_ospf()
        # DUT3.ospf.enable_ospf()
        #
        # DUT1.ospf.advertise_networks(Ex_0_2=["14.0.0.2", "0.0.0.0"], Gi_0_10=["13.0.0.2", "0.0.0.0"])
        # DUT2.ospf.advertise_networks(int_vlan15=["15.0.0.1", "0.0.0.0"],  Gi_0_3=["12.0.0.1", "0.0.0.0"], Gi_0_10=["14.0.0.1", "0.0.0.0"])
        # DUT3.ospf.advertise_networks(Gi_0_3=["12.0.0.2", "0.0.0.0"], Gi_0_10=["13.0.0.1", "0.0.0.0"])
        #
        # time.sleep(45)
        #
        # dict_ospf_routes_1 = DUT1.ospf.show_ip_route_ospf()
        # dict_ospf_routes_2 = DUT2.ospf.show_ip_route_ospf()
        # dict_ospf_routes_3 = DUT3.ospf.show_ip_route_ospf()
        #
        # print(dict_ospf_routes_1)
        # print(dict_ospf_routes_2)
        # print(dict_ospf_routes_3)
        #
        # # Check if the routes are learned and installed in OSPF routes
        #
        # assert "15.0.0.0" in dict_ospf_routes_1.keys() and "12.0.0.0" in dict_ospf_routes_1.keys()
        # assert "13.0.0.0" in dict_ospf_routes_2.keys()
        # assert "15.0.0.0" in dict_ospf_routes_3.keys() and "14.0.0.0" in dict_ospf_routes_3.keys()
        #
        # # Shut one port on DUT1 and check that RIP routes are not missing
        #
        # DUT1.int.shut_interface(interface="Ex 0/2")
        #
        # time.sleep(45)
        #
        # dict_ospf_routes_1 = DUT1.ospf.show_ip_route_ospf()
        # dict_ospf_routes_2 = DUT2.ospf.show_ip_route_ospf()
        # dict_ospf_routes_3 = DUT3.ospf.show_ip_route_ospf()
        #
        # print(dict_ospf_routes_1)
        # print(dict_ospf_routes_2)
        # print(dict_ospf_routes_3)
        #
        # # Check if the routes are learned and installed in OSPF routes
        #
        # assert "15.0.0.0" in dict_ospf_routes_1.keys() and "12.0.0.0" in dict_ospf_routes_1.keys() # Trb "in" in loc de "not in"
        # assert "13.0.0.0" in dict_ospf_routes_2.keys()
        # assert "15.0.0.0" in dict_ospf_routes_3.keys()
        #
        # # No shut the port on DUT1 and check that RIP routes are not missing
        #
        # DUT1.int.no_shut_interface(interface="Ex 0/2")
        #
        # time.sleep(45)
        #
        # dict_ospf_routes_1 = DUT1.ospf.show_ip_route_ospf()
        # dict_ospf_routes_2 = DUT2.ospf.show_ip_route_ospf()
        # dict_ospf_routes_3 = DUT3.ospf.show_ip_route_ospf()
        #
        # print(dict_ospf_routes_1)
        # print(dict_ospf_routes_2)
        # print(dict_ospf_routes_3)
        #
        # # Check if the routes are learned and installed in OSPF routes
        #
        # assert "15.0.0.0" in dict_ospf_routes_1.keys() and "12.0.0.0" in dict_ospf_routes_1.keys()  # Trb "in" in loc de "not in"
        # assert "13.0.0.0" in dict_ospf_routes_2.keys()
        # assert "15.0.0.0" in dict_ospf_routes_3.keys()

        print("########## Removing the config #############")

        DUT1.ospf.remove_networks(Ex_0_2=["14.0.0.2", "0.0.0.0"], Gi_0_10=["13.0.0.2", "0.0.0.0"])
        DUT2.ospf.remove_networks(int_vlan15=["15.0.0.1", "0.0.0.0"],  Gi_0_3=["12.0.0.1", "0.0.0.0"], Gi_0_10=["14.0.0.1", "0.0.0.0"])
        DUT3.ospf.remove_networks(Gi_0_3=["12.0.0.2", "0.0.0.0"], Gi_0_10=["13.0.0.1", "0.0.0.0"])

        DUT1.ospf.disable_ospf()
        DUT2.ospf.disable_ospf()
        DUT3.ospf.disable_ospf()

        DUT2.ip.remove_vlan_interfaces("15")

        DUT2.vl.remove_vlans("15")

        DUT1.int.remove_routed_ports("Ex 0/2", "Gi 0/10")
        DUT2.int.remove_routed_ports("Gi 0/3", "Gi 0/10")
        DUT3.int.remove_routed_ports("Gi 0/3", "Gi 0/10")

        DUT2.int.shut_interfaces("Gi 0/5")

    def test_func_19(self):

        print("###### Test_func_19 ######")
        print("########## Verify the DR/BRD election when only L3 interfaces are configured in a Broadcast type network ( Routed Port )  #############")
        print("###### 4 DUTs ######")

        #          Topology
        #
        #  DUT1 --- DUT3 ---- DUT2
        #             |
        #           DUT4

        # Creating routed ports on all DUTs

        DUT1.int.add_routed_ports("Gi 0/10")
        DUT2.int.add_routed_ports("Gi 0/3")
        DUT4.int.add_routed_ports("Gi 0/11")

        # No shutting the interfaces

        DUT1.int.no_shut_interfaces("Gi 0/10")
        DUT2.int.no_shut_interfaces("Gi 0/3", "Gi 0/5")
        DUT3.int.no_shut_interfaces("Gi 0/3", "Gi 0/10", "Gi 0/11")
        DUT4.int.no_shut_interfaces("Gi 0/11")

        # Creating the VLAN on DUT2

        DUT2.vl.create_vlan(vlan="15")

        # Adding the ports to the VLAN

        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")

        # Create IP Routed Ports on all DUTs except DUT3 which is the "HUB"

        DUT1.ip.add_ip_routed_ports("Gi 0/10", Gi_0_10=["9.0.0.2", "255.255.255.0"])

        DUT2.ip.add_ip_routed_ports("Gi 0/3", Gi_0_3=["9.0.0.1", "255.255.255.0"])
        DUT2.ip.add_ip_interface(int_vlan="15", ip="15.0.0.1", mask="255.255.255.0")
        DUT2.ip.no_shut_int_vlan(int_vlan="15")

        DUT4.ip.add_ip_routed_ports("Gi 0/11", Gi_0_11=["9.0.0.3", "255.255.255.0"])

        # Enable OSPF on all DUTs and advertise the IPs

        DUT1.ospf.enable_ospf()
        DUT2.ospf.enable_ospf()
        DUT4.ospf.enable_ospf()

        DUT1.ospf.advertise_networks(Gi_0_10=["9.0.0.2", "0.0.0.0"])
        DUT2.ospf.advertise_networks(int_vlan15=["15.0.0.1", "0.0.0.0"],  Gi_0_3=["9.0.0.1", "0.0.0.0"])
        DUT4.ospf.advertise_networks(Gi_0_11=["9.0.0.3", "0.0.0.0"])

        time.sleep(45)

        dict_ospf_routes_1 = DUT1.ospf.show_ip_route_ospf()
        dict_ospf_routes_2 = DUT2.ospf.show_ip_route_ospf()
        dict_ospf_routes_4 = DUT4.ospf.show_ip_route_ospf()

        print(dict_ospf_routes_1)
        print(dict_ospf_routes_2)
        print(dict_ospf_routes_4)

        list_ospf_neighbors_1, dict_of_ospf_neighbors_1 = DUT1.ospf.show_ospf_neighbors()
        list_ospf_neighbors_2, dict_of_ospf_neighbors_2 = DUT2.ospf.show_ospf_neighbors()
        list_ospf_neighbors_4, dict_of_ospf_neighbors_4 = DUT4.ospf.show_ospf_neighbors()

        print(dict_of_ospf_neighbors_1)

        print(dict_of_ospf_neighbors_2)
        print(dict_of_ospf_neighbors_4)

        # Check if the routes are learned and installed in OSPF routes

        assert "15.0.0.0" in dict_ospf_routes_1.keys()
        assert "15.0.0.0" in dict_ospf_routes_4.keys()

        # Check DR is DUT4 (the highest IP from election), BDR is DUT1 and DROthers is DUT2 (the lowest IP)

        assert dict_of_ospf_neighbors_1["9.0.0.1"]["State"] == "FULL/DR_OTHER" and dict_of_ospf_neighbors_1["9.0.0.3"]["State"] == "FULL/DR"
        assert dict_of_ospf_neighbors_2["9.0.0.2"]["State"] == "FULL/BACKUP" and dict_of_ospf_neighbors_2["9.0.0.3"]["State"] == "FULL/DR"
        assert dict_of_ospf_neighbors_4["9.0.0.1"]["State"] == "FULL/DR_OTHER" and dict_of_ospf_neighbors_4["9.0.0.2"]["State"] == "FULL/BACKUP"

        print("########## Removing the config #############")

        DUT1.ospf.remove_networks(Gi_0_10=["9.0.0.2", "0.0.0.0"])
        DUT2.ospf.remove_networks(int_vlan15=["15.0.0.1", "0.0.0.0"],  Gi_0_3=["9.0.0.1", "0.0.0.0"])
        DUT4.ospf.remove_networks(Gi_0_11=["9.0.0.3", "0.0.0.0"])

        DUT1.ospf.disable_ospf()
        DUT2.ospf.disable_ospf()
        DUT4.ospf.disable_ospf()

        DUT2.ip.remove_vlan_interfaces("15")

        DUT2.vl.remove_vlans("15")

        DUT1.int.remove_routed_ports("Gi 0/10")
        DUT2.int.remove_routed_ports("Gi 0/3")
        DUT4.int.remove_routed_ports("Gi 0/11")

        DUT2.int.shut_interfaces("Gi 0/5")
        DUT3.int.shut_interfaces("Gi 0/3", "Gi 0/10", "Gi 0/11")

    def test_func_20(self):

        print("###### Test_func_20 ######")
        print("########## Verify the DR/BRD election when only L3 interfaces are configured in a Broadcast type network ( SVI )  #############")
        print("###### 4 DUTs ######")

        #          Topology
        #
        #  DUT1 --- DUT3 ---- DUT2
        #             |
        #           DUT4


        # No shutting the interfaces

        DUT1.int.no_shut_interfaces("Gi 0/10")
        DUT2.int.no_shut_interfaces("Gi 0/3", "Gi 0/5")
        DUT3.int.no_shut_interfaces("Gi 0/3", "Gi 0/10", "Gi 0/11")
        DUT4.int.no_shut_interfaces("Gi 0/11")

        # Creating the VLAN on DUTs

        DUT1.vl.create_vlan(vlan="9")
        DUT2.vl.create_vlan(vlan="15")
        DUT2.vl.create_vlan(vlan="9")
        DUT3.vl.create_vlan(vlan="9")
        DUT4.vl.create_vlan(vlan="9")

        # Adding the ports to the VLAN

        DUT1.vl.add_ports_to_vlan(ports="Gi 0/10", vlan="9")

        DUT2.vl.add_ports_to_vlan(ports="Gi 0/3", vlan="9")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")

        DUT3.vl.add_ports_to_vlan(ports="Gi 0/3", vlan="9")
        DUT3.vl.add_ports_to_vlan(ports="Gi 0/10", vlan="9")
        DUT3.vl.add_ports_to_vlan(ports="Gi 0/11", vlan="9")

        DUT4.vl.add_ports_to_vlan(ports="Gi 0/11", vlan="9")

        # Create IP interfaces on all DUTs for the specific VLANs

        DUT1.ip.add_ip_interfaces("9", int_vlan9=["9.0.0.2", "255.255.255.0"])
        DUT1.ip.no_shut_int_vlans("9")

        DUT2.ip.add_ip_interfaces("9", "15", int_vlan9=["9.0.0.1", "255.255.255.0"], int_vlan15=["15.0.0.1", "255.255.255.0"])
        DUT2.ip.no_shut_int_vlans("15", "9")

        DUT4.ip.add_ip_interfaces("9", int_vlan9=["9.0.0.3", "255.255.255.0"])
        DUT4.ip.no_shut_int_vlans("9")

        # SHUT the UP-Link from DUT4 towards CAMBIUM-LAB to avoid STP loops

        DUT4.int.shut_interfaces("Gi 0/1")
        time.sleep(20)

        # Enable OSPF on all DUTs and advertise the IPs

        DUT1.ospf.enable_ospf()
        DUT2.ospf.enable_ospf()
        DUT4.ospf.enable_ospf()

        DUT1.ospf.advertise_networks(int_vlan9=["9.0.0.2", "0.0.0.0"])
        DUT2.ospf.advertise_networks(int_vlan15=["15.0.0.1", "0.0.0.0"],  int_vlan9=["9.0.0.1", "0.0.0.0"])
        DUT4.ospf.advertise_networks(int_vlan9=["9.0.0.3", "0.0.0.0"])

        time.sleep(45)

        dict_ospf_routes_1 = DUT1.ospf.show_ip_route_ospf()
        dict_ospf_routes_2 = DUT2.ospf.show_ip_route_ospf()
        dict_ospf_routes_4 = DUT4.ospf.show_ip_route_ospf()

        print(dict_ospf_routes_1)
        print(dict_ospf_routes_2)
        print(dict_ospf_routes_4)

        list_ospf_neighbors_1, dict_of_ospf_neighbors_1 = DUT1.ospf.show_ospf_neighbors()
        list_ospf_neighbors_2, dict_of_ospf_neighbors_2 = DUT2.ospf.show_ospf_neighbors()
        list_ospf_neighbors_4, dict_of_ospf_neighbors_4 = DUT4.ospf.show_ospf_neighbors()

        print(dict_of_ospf_neighbors_1)
        print(dict_of_ospf_neighbors_2)
        print(dict_of_ospf_neighbors_4)

        # Check if the routes are learned and installed in OSPF routes

        assert "15.0.0.0" in dict_ospf_routes_1.keys()
        assert "15.0.0.0" in dict_ospf_routes_4.keys()

        # Check DR is DUT4 (the highest IP from election), BDR is DUT1 and DROthers is DUT2 (the lowest IP)

        assert dict_of_ospf_neighbors_1["9.0.0.1"]["State"] == "FULL/DR_OTHER" and dict_of_ospf_neighbors_1["9.0.0.3"]["State"] == "FULL/DR"
        assert dict_of_ospf_neighbors_2["9.0.0.2"]["State"] == "FULL/BACKUP" and dict_of_ospf_neighbors_2["9.0.0.3"]["State"] == "FULL/DR"
        assert dict_of_ospf_neighbors_4["9.0.0.1"]["State"] == "FULL/DR_OTHER" and dict_of_ospf_neighbors_4["9.0.0.2"]["State"] == "FULL/BACKUP"

        print("########## Removing the config #############")

        DUT4.int.no_shut_interfaces("Gi 0/1")

        DUT1.ospf.remove_networks(int_vlan9=["9.0.0.2", "0.0.0.0"])
        DUT2.ospf.remove_networks(int_vlan15=["15.0.0.1", "0.0.0.0"],  int_vlan9=["9.0.0.1", "0.0.0.0"])
        DUT4.ospf.remove_networks(int_vlan9=["9.0.0.3", "0.0.0.0"])

        DUT1.ospf.disable_ospf()
        DUT2.ospf.disable_ospf()
        DUT4.ospf.disable_ospf()

        DUT1.ip.remove_vlan_interfaces("9")
        DUT2.ip.remove_vlan_interfaces("15", "9")
        DUT4.ip.remove_vlan_interfaces("9")

        DUT1.vl.remove_vlan("9")
        DUT2.vl.remove_vlans("15", "9")
        DUT3.vl.remove_vlan("9")
        DUT4.vl.remove_vlan("9")

        DUT1.int.shut_interfaces("Gi 0/10")
        DUT2.int.shut_interfaces("Gi 0/5", "Gi 0/3")
        DUT3.int.shut_interfaces("Gi 0/3", "Gi 0/10", "Gi 0/11")
        DUT4.int.shut_interfaces("Gi 0/11")

    def test_func_21(self):

        # LOKI-1457 : OSPF - ip route is not showing info about the redist-config tag command

        print("###### Test_func_21 ######")
        print("########## Verify that you can redist-config a network with route Tag  #############")
        print("###### 2 DUTs ######")

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/5", "Gi 0/9")

        # Adding the ports to the VLAN

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")

        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")

        # Create IP interfaces on all DUTs for the specific VLANs

        DUT1.ip.add_ip_interfaces("20", int_vlan20=["20.0.0.2", "255.255.255.0"])
        DUT1.ip.no_shut_int_vlans("20")

        DUT2.ip.add_ip_interfaces("20", "15", int_vlan20=["20.0.0.1", "255.255.255.0"],
                                  int_vlan15=["15.0.0.1", "255.255.255.0"])
        DUT2.ip.no_shut_int_vlans("15", "20")

        # Enable ospf on all DUTs and advertise the IPs

        DUT1.ospf.enable_ospf()
        DUT2.ospf.enable_ospf()

        DUT1.ospf.advertise_networks(int_vlan20=["20.0.0.2", "0.0.0.0"])
        DUT2.ospf.advertise_networks(int_vlan20=["20.0.0.1", "0.0.0.0"])

        # Redistribute connected so that DUT2 is an ASBR

        DUT2.ospf.redistribute_connected()

        # Redist-config the network with a Route Tag

        DUT2.ospf.redist_config(network="15.0.0.0", network_mask="255.255.255.0", tag="150")

        time.sleep(45)

        ip_route_1 = DUT1.ip.show_ip_route_tag(network="15.0.0.0")
        print(ip_route_1)

        ip_route_2 = DUT2.ip.show_ip_route_tag(network="15.0.0.0")
        print(ip_route_2)

        assert ip_route_1["Network"] == "15.0.0.0" and ip_route_1["Route Tag"] == "150" and ip_route_1["Protocol"] == "O E2"
        assert ip_route_2["Network"] == "15.0.0.0" and ip_route_2["Route Tag"] == "150" and ip_route_2["Protocol"] == "C"

        # Configure another Route Tag, and change the metric and metric-type

        DUT2.ospf.redist_config(network="15.0.0.0", network_mask="255.255.255.0", tag="200", metric_type="asExttype1", metric_value="1000")

        time.sleep(10)

        ip_route_1 = DUT1.ip.show_ip_route_tag(network="15.0.0.0")
        print(ip_route_1)

        ip_route_2 = DUT2.ip.show_ip_route_tag(network="15.0.0.0")
        print(ip_route_2)

        assert ip_route_1["Network"] == "15.0.0.0" and ip_route_1["Route Tag"] == "200" and ip_route_1["Protocol"] == "O E1" and ip_route_1["Metric"] == "1001"
        assert ip_route_2["Network"] == "15.0.0.0" and ip_route_2["Route Tag"] == "200" and ip_route_2["Protocol"] == "C"

        print("########## Removing the config #############")

        DUT2.ospf.remove_redist_config(network="15.0.0.0", network_mask="255.255.255.0", tag="200")
        DUT2.ospf.remove_redistribute_connected()

        DUT1.ospf.remove_networks(int_vlan20=["20.0.0.2", "0.0.0.0"])
        DUT2.ospf.remove_networks(int_vlan20=["20.0.0.1", "0.0.0.0"])

        DUT1.ospf.disable_ospf()
        DUT2.ospf.disable_ospf()

        DUT1.ip.remove_int_vlan(int_vlan="20")
        DUT2.ip.remove_vlan_interfaces("20", "15")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5")

        DUT1.vl.remove_vlan(vlan="20")
        DUT2.vl.remove_vlans("20", "15")

    def test_func_22(self):

        print("###### Test_func_22 ######")
        print("########## Verify if ABR sends TYPE 3 LSAs  #############")
        print("###### 2 DUTs ######")


        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/5", "Gi 0/9")

        # Adding the ports to the VLAN

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")

        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")

        # Create IP interfaces on all DUTs for the specific VLANs

        DUT1.ip.add_ip_interfaces("20", int_vlan20=["20.0.0.2", "255.255.255.0"])
        DUT1.ip.no_shut_int_vlans("20")

        DUT2.ip.add_ip_interfaces("20", "15", int_vlan20=["20.0.0.1", "255.255.255.0"],
                                  int_vlan15=["15.0.0.1", "255.255.255.0"])
        DUT2.ip.no_shut_int_vlans("15", "20")

        # Enable ospf on all DUTs and advertise the IPs

        DUT1.ospf.enable_ospf()
        DUT2.ospf.enable_ospf()

        DUT1.ospf.advertise_networks(int_vlan20=["20.0.0.2", "0.0.0.0"])
        DUT2.ospf.advertise_networks(int_vlan20=["20.0.0.1", "0.0.0.0"], int_vlan15=["15.0.0.1", "0.0.0.1"])

        # Check the OSPF database on DUT1 for LSA Type 3 (Summary Link States)

        time.sleep(45)

        dict_ospf_database_router, dict_ospf_database_network,dict_ospf_database_summary, dict_ospf_database_asbr, dict_ospf_database_nssa, dict_ospf_database_external = DUT1.ospf.show_ip_ospf_database(database="summary")

        print(dict_ospf_database_summary)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route(network="15.0.0.0")
        print(ip_route)
        print(dict_of_networks)

        assert ip_route["Network"] == "15.0.0.0" and ip_route["Protocol"] == "O IA"
        assert "15.0.0.0" in dict_ospf_database_summary.keys() and dict_ospf_database_summary["15.0.0.0"]["LS Type"] == "Summary Links(Network)"

        print("########## Removing the config #############")

        DUT1.ospf.remove_networks(int_vlan20=["20.0.0.2", "0.0.0.0"])
        DUT2.ospf.remove_networks(int_vlan20=["20.0.0.1", "0.0.0.0"], int_vlan15=["15.0.0.1", "0.0.0.1"])

        DUT1.ospf.disable_ospf()
        DUT2.ospf.disable_ospf()

        DUT1.ip.remove_int_vlan(int_vlan="20")
        DUT2.ip.remove_vlan_interfaces("20", "15")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5")

        DUT1.vl.remove_vlan(vlan="20")
        DUT2.vl.remove_vlans("20", "15")

    def test_func_23(self):

        print("###### Test_func_23 ######")
        print("########## Verify if ABR sends TYPE 4 and 5 LSAs  #############")
        print("###### 3 DUTs ######")

        #          Topology
        #
        #  OSPF -- DUT1 --OSPF-- DUT2 --RIP-- DUT3 -- RIP
        #

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/5", "Gi 0/9", "Gi 0/4")
        DUT3.int.no_shut_interfaces("Gi 0/4")

        # Adding the ports to the VLAN

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")
        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="60")

        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/4", vlan="12")

        DUT3.vl.add_ports_to_vlan(ports="Gi 0/4", vlan="12")
        DUT3.vl.add_ports_to_vlan(ports="Gi 0/4", vlan="50")

        # Create IP interfaces on all DUTs for the specific VLANs

        DUT1.ip.add_ip_interfaces("20","60", int_vlan20=["20.0.0.2", "255.255.255.0"], int_vlan60=["60.0.0.1", "255.255.255.0"])
        DUT1.ip.no_shut_int_vlans("20","60")

        DUT2.ip.add_ip_interfaces("20", "15", "12", int_vlan20=["20.0.0.1", "255.255.255.0"],
                                  int_vlan15=["15.0.0.1", "255.255.255.0"], int_vlan12=["12.0.0.1", "255.255.255.0"])
        DUT2.ip.no_shut_int_vlans("15", "20", "12")

        DUT3.ip.add_ip_interfaces("50", "12", int_vlan50=["50.0.0.1", "255.255.255.0"],
                                  int_vlan12=["12.0.0.2", "255.255.255.0"])
        DUT3.ip.no_shut_int_vlans("12", "50")

        # Enable ospf on DUT1 and DUT2 and advertise the IPs

        DUT1.ospf.enable_ospf()
        DUT2.ospf.enable_ospf()

        DUT1.ospf.advertise_networks(int_vlan20=["20.0.0.2", "0.0.0.1"], int_vlan60=["60.0.0.1", "0.0.0.0"])
        DUT2.ospf.advertise_networks(int_vlan20=["20.0.0.1", "0.0.0.1"], int_vlan15=["15.0.0.1", "0.0.0.1"])

        # Enable rip on DUT2 and DUT3 and advertise the IPs

        DUT2.rip.enable_rip()
        DUT3.rip.enable_rip()

        DUT2.rip.advertise_networks("12.0.0.1")
        DUT3.rip.advertise_networks("12.0.0.2", "50.0.0.1")

        # Redistributing the rip routes into ospf on DUT2

        DUT2.ospf.redistribute_rip()

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        # Check the routes are learned as expected

        assert "50.0.0.0" in dict_of_networks.keys() and dict_of_networks["50.0.0.0"]["Protocol"] == "O E2"
        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"

        # Check the OSPF database on DUT1 for LSA Type 4 & 5 (ASBR Summary Link States and AS External Link States)

        dict_ospf_database_router, dict_ospf_database_network, dict_ospf_database_summary, dict_ospf_database_asbr, dict_ospf_database_nssa, dict_ospf_database_external = DUT1.ospf.show_ip_ospf_database(database="asbr")
        print(dict_ospf_database_asbr)

        # ASBR Summary Link States

        assert ip_session_2 in dict_ospf_database_asbr.keys() and dict_ospf_database_asbr[ip_session_2]["LS Type"] == "Summary Links(AS Boundary Router)"

        dict_ospf_database_router, dict_ospf_database_network, dict_ospf_database_summary, dict_ospf_database_asbr, dict_ospf_database_nssa, dict_ospf_database_external = DUT1.ospf.show_ip_ospf_database(database="external")
        print(dict_ospf_database_external)

        # AS External Link States

        assert "50.0.0.0" in dict_ospf_database_external.keys() and dict_ospf_database_external["50.0.0.0"]["LS Type"] == "AS External Link"

        print("########## Removing the config #############")

        DUT1.ospf.remove_networks(int_vlan20=["20.0.0.2", "0.0.0.1"], int_vlan60=["60.0.0.1", "0.0.0.0"])
        DUT2.ospf.remove_networks(int_vlan20=["20.0.0.1", "0.0.0.1"], int_vlan15=["15.0.0.1", "0.0.0.1"])

        DUT1.ospf.disable_ospf()
        DUT2.ospf.disable_ospf()

        DUT2.rip.disable_rip()
        DUT3.rip.disable_rip()

        DUT1.ip.remove_vlan_interfaces("20", "60")
        DUT2.ip.remove_vlan_interfaces("20", "15", "12")
        DUT3.ip.remove_vlan_interfaces("50", "12")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5", "Gi 0/4")
        DUT3.int.shut_interfaces("Gi 0/4")

        DUT1.vl.remove_vlans("20", "60")
        DUT2.vl.remove_vlans("20", "15", "12")
        DUT3.vl.remove_vlans("12", "50")

    def test_func_24(self):

        print("###### Test_func_24 ######")
        print("########## Verify if ASBR sends TYPE 7  #############")
        print("###### 3 DUTs ######")

        #          Topology
        #
        #   Area 0  |  Area 1 NSSA
        #
        #  OSPF-- DUT1 --OSPF-- DUT2 --RIP-- DUT3 --RIP
        #

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/5", "Gi 0/9", "Gi 0/4")
        DUT3.int.no_shut_interfaces("Gi 0/4")

        # Adding the ports to the VLAN

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")
        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="60")

        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/4", vlan="12")

        DUT3.vl.add_ports_to_vlan(ports="Gi 0/4", vlan="12")
        DUT3.vl.add_ports_to_vlan(ports="Gi 0/4", vlan="50")

        # Create IP interfaces on all DUTs for the specific VLANs

        DUT1.ip.add_ip_interfaces("20","60", int_vlan20=["20.0.0.2", "255.255.255.0"], int_vlan60=["60.0.0.1", "255.255.255.0"])
        DUT1.ip.no_shut_int_vlans("20","60")

        DUT2.ip.add_ip_interfaces("20", "15", "12", int_vlan20=["20.0.0.1", "255.255.255.0"],
                                  int_vlan15=["15.0.0.1", "255.255.255.0"], int_vlan12=["12.0.0.1", "255.255.255.0"])
        DUT2.ip.no_shut_int_vlans("15", "20", "12")

        DUT3.ip.add_ip_interfaces("50", "12", int_vlan50=["50.0.0.1", "255.255.255.0"],
                                  int_vlan12=["12.0.0.2", "255.255.255.0"])
        DUT3.ip.no_shut_int_vlans("12", "50")

        # Enable ospf on DUT1 and DUT2 and advertise the IPs

        DUT1.ospf.enable_ospf()
        DUT2.ospf.enable_ospf()

        DUT1.ospf.advertise_networks(int_vlan20=["20.0.0.2", "0.0.0.1"], int_vlan60=["60.0.0.1", "0.0.0.0"])
        DUT2.ospf.advertise_networks(int_vlan20=["20.0.0.1", "0.0.0.1"], int_vlan15=["15.0.0.1", "0.0.0.1"])

        # Enable rip on DUT2 and DUT3 and advertise the IPs

        DUT2.rip.enable_rip()
        DUT3.rip.enable_rip()

        DUT2.rip.advertise_networks("12.0.0.1")
        DUT3.rip.advertise_networks("12.0.0.2", "50.0.0.1")

        # Redistributing the rip routes into ospf on DUT2

        DUT2.ospf.redistribute_rip()

        # Configure nssa area on DUT1 and DUT2 for area 0.0.0.1

        DUT1.ospf.add_nssa_area(area="0.0.0.1")
        DUT2.ospf.add_nssa_area(area="0.0.0.1")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        # Check the routes are learned as expected

        assert "50.0.0.0" in dict_of_networks.keys() and dict_of_networks["50.0.0.0"]["Protocol"] == "O N2"
        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"

        # Check the OSPF database on DUT1 for LSA Type 7 (NSS External Link States)

        dict_ospf_database_router, dict_ospf_database_network, dict_ospf_database_summary, dict_ospf_database_asbr, dict_ospf_database_nssa, dict_ospf_database_external = DUT1.ospf.show_ip_ospf_database(database="nssa")
        print(dict_ospf_database_nssa)

        # NSSA Link States

        assert "50.0.0.0" in dict_ospf_database_nssa.keys() and dict_ospf_database_nssa["50.0.0.0"]["LS Type"] == "NSSA External Link"

        print("########## Removing the config #############")

        DUT1.ospf.remove_nssa_area(area="0.0.0.1")
        DUT2.ospf.remove_nssa_area(area="0.0.0.1")
        DUT2.ospf.remove_redistribute_rip()

        DUT1.ospf.remove_networks(int_vlan20=["20.0.0.2", "0.0.0.1"], int_vlan60=["60.0.0.1", "0.0.0.0"])
        DUT2.ospf.remove_networks(int_vlan20=["20.0.0.1", "0.0.0.1"], int_vlan15=["15.0.0.1", "0.0.0.1"])

        DUT1.ospf.disable_ospf()
        DUT2.ospf.disable_ospf()

        DUT2.rip.disable_rip()
        DUT3.rip.disable_rip()

        DUT1.ip.remove_vlan_interfaces("20", "60")
        DUT2.ip.remove_vlan_interfaces("20", "15", "12")
        DUT3.ip.remove_vlan_interfaces("50", "12")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5", "Gi 0/4")
        DUT3.int.shut_interfaces("Gi 0/4")

        DUT1.vl.remove_vlans("20", "60")
        DUT2.vl.remove_vlans("20", "15", "12")
        DUT3.vl.remove_vlans("12", "50")

    def test_func_25(self):

        print("###### Test_func_25 ######")
        print("########## Verify ABR summarization  #############")
        print("###### 2 DUTs ######")

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/5", "Gi 0/9")

        # Adding the ports to the VLAN

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")

        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="25")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")

        # Create IP interfaces on all DUTs for the specific VLANs

        DUT1.ip.add_ip_interfaces("20", int_vlan20=["20.0.0.2", "255.255.255.0"])
        DUT1.ip.no_shut_int_vlans("20")

        DUT2.ip.add_ip_interfaces("20", "15", "25", int_vlan20=["20.0.0.1", "255.255.255.0"],int_vlan15=["15.0.0.1", "255.255.255.0"],int_vlan25=["15.0.10.1", "255.255.255.0"])
        DUT2.ip.no_shut_int_vlans("15", "20", "25")

        # Enable ospf on all DUTs and advertise the IPs

        DUT1.ospf.enable_ospf()
        DUT2.ospf.enable_ospf()

        DUT1.ospf.advertise_networks(int_vlan20=["20.0.0.2", "0.0.0.0"])
        DUT2.ospf.advertise_networks(int_vlan20=["20.0.0.1", "0.0.0.0"])

        # Redistribute connected on DUT2 so the dut becomes ABR and check the routes 15.0.0.0/24 and 15.0.10.0/24 are learned

        DUT2.ospf.redistribute_connected()

        time.sleep(45)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2 and "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]
        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O E2" and dict_of_networks["15.0.0.0"]["Mask"] == "24"
        assert "15.0.10.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O E2" and dict_of_networks["15.0.10.0"]["Mask"] == "24"

        # Summarize on DUT2 the networks 15.0.0.0/24 and 15.0.10.0/24 into 15.0.0.0/9 and check the routes are summarized in DUT1 routing table

        DUT2.ospf.add_network_summarize(network="15.0.0.0", mask="255.128.0.0", area="0.0.0.0")

        time.sleep(10)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2 and "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]
        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O E2" and dict_of_networks["15.0.0.0"]["Mask"] == "9"

        # Remove the summarization on DUT2 and check the routes are not summarized in DUT1 routing table.

        DUT2.ospf.remove_network_summarize(network="15.0.0.0", mask="255.128.0.0", area="0.0.0.0")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT1.int.no_shut_interface(interface="Ex 0/1")

        time.sleep(45)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2 and "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]
        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O E2" and dict_of_networks["15.0.0.0"]["Mask"] == "24"
        assert "15.0.10.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O E2" and dict_of_networks["15.0.10.0"]["Mask"] == "24"

        print("########## Removing the config #############")

        DUT2.ospf.remove_redistribute_connected()

        DUT1.ospf.remove_networks(int_vlan20=["20.0.0.2", "0.0.0.0"])
        DUT2.ospf.remove_networks(int_vlan20=["20.0.0.1", "0.0.0.0"])

        DUT1.ospf.disable_ospf()
        DUT2.ospf.disable_ospf()

        DUT1.ip.remove_int_vlan(int_vlan="20")
        DUT2.ip.remove_vlan_interfaces("20", "15", "25")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5")

        DUT1.vl.remove_vlan(vlan="20")
        DUT2.vl.remove_vlans("20", "15", "25")

    def test_func_26(self):

        print("###### Test_func_26 ######")
        print("########## Verify the OSPF behavior for passive interface - interface VLAN  #############")
        print("###### 2 DUTs ######")

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/5", "Gi 0/9")

        # Adding the ports to the VLAN

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")

        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")

        # Create IP interfaces on all DUTs for the specific VLANs

        DUT1.ip.add_ip_interfaces("20", int_vlan20=["20.0.0.2", "255.255.255.0"])
        DUT1.ip.no_shut_int_vlans("20")

        DUT2.ip.add_ip_interfaces("20", "15", int_vlan20=["20.0.0.1", "255.255.255.0"],int_vlan15=["15.0.0.1", "255.255.255.0"])
        DUT2.ip.no_shut_int_vlans("15", "20")

        # Enable ospf on all DUTs and advertise the IPs

        DUT1.ospf.enable_ospf()
        DUT2.ospf.enable_ospf()

        DUT1.ospf.advertise_networks(int_vlan20=["20.0.0.2", "0.0.0.0"])
        DUT2.ospf.advertise_networks(int_vlan20=["20.0.0.1", "0.0.0.0"], int_vlan15=["15.0.0.1", "0.0.0.0"])

        # Configure the int VLAN 20 on DUT1 to be a passive interface. Check there is no adjacency between DUTs

        DUT1.ospf.add_passive_interface(vlan="20")

        time.sleep(120)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        assert ip_session_2 not in dict_of_ospf_neighbors.keys()
        assert "15.0.0.0" not in dict_of_networks.keys()

        # Remove the passive interface and check that the adjacency is formed and the routes are learned

        DUT1.ospf.remove_passive_interface(vlan="20")

        time.sleep(45)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2 and "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]
        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"

        print("########## Removing the config #############")

        DUT1.ospf.remove_networks(int_vlan20=["20.0.0.2", "0.0.0.0"])
        DUT2.ospf.remove_networks(int_vlan20=["20.0.0.1", "0.0.0.0"], int_vlan15=["15.0.0.1", "0.0.0.0"])

        DUT1.ospf.disable_ospf()
        DUT2.ospf.disable_ospf()

        DUT1.ip.remove_int_vlan(int_vlan="20")
        DUT2.ip.remove_vlan_interfaces("20", "15")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5")

        DUT1.vl.remove_vlan(vlan="20")
        DUT2.vl.remove_vlans("20", "15")

    def test_func_27(self):

        print("###### Test_func_27 ######")
        print("########## Verify the OSPF behavior for passive interface - Routed Port  #############")
        print("###### 2 DUTs ######")

        # Creating the Routed Ports

        DUT1.int.add_routed_port("Ex 0/1")
        DUT2.int.add_routed_ports("Gi 0/9")

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/5", "Gi 0/9")

        # Adding the ports to the VLAN

        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")

        # Create IP interfaces on all DUTs for the specific VLANs

        DUT1.ip.add_ip_routed_ports("Ex 0/1", int_Ex01=["20.0.0.2", "255.255.255.0"])

        DUT2.ip.add_ip_routed_ports("Gi 0/9", int_Gi09=["20.0.0.1", "255.255.255.0"])
        DUT2.ip.add_ip_interfaces("15", int_vlan15=["15.0.0.1", "255.255.255.0"])
        DUT2.ip.no_shut_int_vlans("15")

        # Enable ospf on all DUTs and advertise the IPs

        DUT1.ospf.enable_ospf()
        DUT2.ospf.enable_ospf()

        DUT1.ospf.advertise_networks(int_Ex01=["20.0.0.2", "0.0.0.0"])
        DUT2.ospf.advertise_networks(int_Gi09=["20.0.0.1", "0.0.0.0"], int_vlan15=["15.0.0.1", "0.0.0.0"])

        # Configure the routed port Ex 0/1 on DUT1 to be a passive interface. Check there is no adjacency between DUTs

        DUT1.ospf.add_passive_interface(interface="Ex 0/1")

        time.sleep(120)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        assert ip_session_2 not in dict_of_ospf_neighbors.keys()
        assert "15.0.0.0" not in dict_of_networks.keys()

        # Remove the passive interface and check that the adjacency is formed and the routes are learned

        DUT1.ospf.remove_passive_interface(interface="Ex 0/1")

        time.sleep(45)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2 and "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]
        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"

        print("########## Removing the config #############")

        DUT1.ospf.remove_networks(int_Ex01=["20.0.0.2", "0.0.0.0"])
        DUT2.ospf.remove_networks(int_Gi09=["20.0.0.1", "0.0.0.0"], int_vlan15=["15.0.0.1", "0.0.0.0"])

        DUT1.ospf.disable_ospf()
        DUT2.ospf.disable_ospf()

        DUT1.int.remove_routed_ports("Ex 0/1")

        DUT2.int.remove_routed_ports("Gi 0/9")
        DUT2.ip.remove_vlan_interfaces("15")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5")

        DUT2.vl.remove_vlans("15")

    def test_func_28(self):

        print("###### Test_func_28 ######")
        print("########## Verify the default-information-originate always parameter in nssa area  #############")
        print("###### 2 DUTs ######")

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/5", "Gi 0/9")

        # Adding the ports to the VLAN

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")

        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")

        # Create IP interfaces on all DUTs for the specific VLANs

        DUT1.ip.add_ip_interfaces("20", int_vlan20=["20.0.0.2", "255.255.255.0"])
        DUT1.ip.no_shut_int_vlans("20")

        DUT2.ip.add_ip_interfaces("20", "15", int_vlan20=["20.0.0.1", "255.255.255.0"], int_vlan15=["15.0.0.1", "255.255.255.0"])
        DUT2.ip.no_shut_int_vlans("15", "20")

        # Enable ospf on all DUTs and advertise the IPs

        DUT1.ospf.enable_ospf()
        DUT2.ospf.enable_ospf()

        DUT1.ospf.advertise_networks(int_vlan20=["20.0.0.2", "0.0.0.1"])
        DUT2.ospf.advertise_networks(int_vlan20=["20.0.0.1", "0.0.0.1"], int_vlan15=["15.0.0.1", "0.0.0.0"])

        # Configure nssa area on DUT1 and DUT2 for area 0.0.0.1

        DUT1.ospf.add_nssa_area(area="0.0.0.1")
        DUT2.ospf.add_nssa_area(area="0.0.0.1")

        # Configure the default-route on DUT2

        DUT2.ospf.add_default_information_originate(nssa="Yes", area="0.0.0.1")

        time.sleep(120)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2 and "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]
        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O IA"
        assert "0.0.0.0" in dict_of_networks.keys() and dict_of_networks["0.0.0.0"]["Protocol"] == "O N2"

        # Remove the default information originate on DUT2 and check that is no longer in the routing table

        DUT2.ospf.remove_default_information_originate(nssa="Yes", area="0.0.0.1")

        time.sleep(15)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2 and "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]
        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O IA"
        assert dict_of_networks["0.0.0.0"]["Protocol"] != "O N2"

        print("########## Removing the config #############")

        DUT1.ospf.remove_nssa_area(area="0.0.0.1")
        DUT2.ospf.remove_nssa_area(area="0.0.0.1")

        DUT1.ospf.remove_networks(int_vlan20=["20.0.0.2", "0.0.0.1"])
        DUT2.ospf.remove_networks(int_vlan20=["20.0.0.1", "0.0.0.1"], int_vlan15=["15.0.0.1", "0.0.0.0"])

        DUT1.ospf.disable_ospf()
        DUT2.ospf.disable_ospf()

        DUT1.ip.remove_int_vlan(int_vlan="20")
        DUT2.ip.remove_vlan_interfaces("20", "15")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5")

        DUT1.vl.remove_vlan(vlan="20")
        DUT2.vl.remove_vlans("20", "15")

    def test_func_29(self):

        print("###### Test_func_29 ######")
        print("########## Verify the default-information-originate metric-type 1/2 parameter in nssa area  #############")
        print("###### 2 DUTs ######")

        # LOKI-3582 - Incorrect metric-type value for nssa default-information-originate command

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/5", "Gi 0/9")

        # Adding the ports to the VLAN

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")

        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")

        # Create IP interfaces on all DUTs for the specific VLANs

        DUT1.ip.add_ip_interfaces("20", int_vlan20=["20.0.0.2", "255.255.255.0"])
        DUT1.ip.no_shut_int_vlans("20")

        DUT2.ip.add_ip_interfaces("20", "15", int_vlan20=["20.0.0.1", "255.255.255.0"], int_vlan15=["15.0.0.1", "255.255.255.0"])
        DUT2.ip.no_shut_int_vlans("15", "20")

        # Enable ospf on all DUTs and advertise the IPs

        DUT1.ospf.enable_ospf()
        DUT2.ospf.enable_ospf()

        DUT1.ospf.advertise_networks(int_vlan20=["20.0.0.2", "0.0.0.1"])
        DUT2.ospf.advertise_networks(int_vlan20=["20.0.0.1", "0.0.0.1"], int_vlan15=["15.0.0.1", "0.0.0.0"])

        # Configure nssa area on DUT1 and DUT2 for area 0.0.0.1

        DUT1.ospf.add_nssa_area(area="0.0.0.1")
        DUT2.ospf.add_nssa_area(area="0.0.0.1")

        # Configure the default-route on DUT2

        DUT2.ospf.add_default_information_originate(nssa="Yes", area="0.0.0.1")

        time.sleep(120)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2 and "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]
        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O IA"
        assert "0.0.0.0" in dict_of_networks.keys() and dict_of_networks["0.0.0.0"]["Protocol"] == "O N2"

        # Change the metric-type to 1 for the default route

        DUT2.ospf.add_default_information_originate(nssa="Yes", area="0.0.0.1", metric_type="1")

        time.sleep(15)

        list_ospf_neighbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2 and "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]
        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O IA"
        assert dict_of_networks["0.0.0.0"]["Protocol"] == "O N1" # aici trebuie == O N1

        print("########## Removing the config #############")

        DUT2.ospf.remove_default_information_originate(nssa="Yes", area="0.0.0.1")

        DUT1.ospf.remove_nssa_area(area="0.0.0.1")
        DUT2.ospf.remove_nssa_area(area="0.0.0.1")

        DUT1.ospf.remove_networks(int_vlan20=["20.0.0.2", "0.0.0.1"])
        DUT2.ospf.remove_networks(int_vlan20=["20.0.0.1", "0.0.0.1"], int_vlan15=["15.0.0.1", "0.0.0.0"])

        DUT1.ospf.disable_ospf()
        DUT2.ospf.disable_ospf()

        DUT1.ip.remove_int_vlan(int_vlan="20")
        DUT2.ip.remove_vlan_interfaces("20", "15")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5")

        DUT1.vl.remove_vlan(vlan="20")
        DUT2.vl.remove_vlans("20", "15")

    def test_func_30(self):

        print("###### Test_func_30 ######")
        print("########## Verify that the redistribute metric-type 1/2 is working in nssa area  #############")
        print("###### 3 DUTs ######")

        #          Topology
        #
        #      Area 1 NSSA |     Area 0
        #
        #  DUT1 --OSPF-- DUT2 --OSPF-- DUT3
        #

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/4", "Gi 0/5", "Gi 0/9")
        DUT3.int.no_shut_interfaces("Gi 0/4")

        # Adding the ports to the VLAN

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")

        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/4", vlan="12")

        DUT3.vl.add_ports_to_vlan(ports="Gi 0/4", vlan="12")

        # Create IP interfaces on all DUTs for the specific VLANs

        DUT1.ip.add_ip_interfaces("20", int_vlan20=["20.0.0.2", "255.255.255.0"])
        DUT1.ip.no_shut_int_vlans("20")

        DUT2.ip.add_ip_interfaces("20", "15", "12", int_vlan20=["20.0.0.1", "255.255.255.0"],int_vlan15=["15.0.0.1", "255.255.255.0"], int_vlan12=["12.0.0.1", "255.255.255.0"])
        DUT2.ip.no_shut_int_vlans("12", "15", "20")

        DUT3.ip.add_ip_interfaces("12", int_vlan12=["12.0.0.2", "255.255.255.0"])
        DUT3.ip.no_shut_int_vlans("12")

        # Enable ospf on all DUTs and advertise the IPs

        DUT1.ospf.enable_ospf()
        DUT2.ospf.enable_ospf()
        DUT3.ospf.enable_ospf()

        DUT1.ospf.advertise_networks(int_vlan20=["20.0.0.2", "0.0.0.1"])
        DUT2.ospf.advertise_networks(int_vlan20=["20.0.0.1", "0.0.0.1"], int_vlan12=["12.0.0.1", "0.0.0.0"])
        DUT3.ospf.advertise_networks(int_vlan20=["12.0.0.2", "0.0.0.0"])

        # Configure nssa area on DUT1 and DUT2 for area 0.0.0.1

        DUT1.ospf.add_nssa_area(area="0.0.0.1")
        DUT2.ospf.add_nssa_area(area="0.0.0.1")

        # Create a static route and redistribute static and connected on DUT2 and check that on DUT3 and DUT1 the routes are learned accordingly (E2 for DUT3 and N2 for DUT1)

        DUT2.ip.add_static_route(network_dest="100.0.0.0", mask_dest="255.255.255.0", next_hop="20.0.0.2")

        DUT2.ospf.redistribute_connected()
        DUT2.ospf.redistribute_static()

        time.sleep(120)

        list_ospf_neighbors_2, dict_of_ospf_neighbors_2 = DUT2.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors_2)

        ip_route_1, networks_1, networks_connected_1, dict_of_networks_1 = DUT1.ip.show_ip_route()
        print(dict_of_networks_1)

        ip_route_3, networks_3, networks_connected_3, dict_of_networks_3 = DUT3.ip.show_ip_route()
        print(dict_of_networks_3)

        assert ip_session_1 in dict_of_ospf_neighbors_2.keys() and dict_of_ospf_neighbors_2[ip_session_1]["Neighbor-ID"] == ip_session_1 and "FULL" in dict_of_ospf_neighbors_2[ip_session_1]["State"]
        assert ip_session_3 in dict_of_ospf_neighbors_2.keys() and dict_of_ospf_neighbors_2[ip_session_3]["Neighbor-ID"] == ip_session_3 and "FULL" in dict_of_ospf_neighbors_2[ip_session_3]["State"]
        assert "15.0.0.0" in dict_of_networks_1.keys() and dict_of_networks_1["15.0.0.0"]["Protocol"] == "O N2"
        assert "100.0.0.0" in dict_of_networks_1.keys() and dict_of_networks_1["100.0.0.0"]["Protocol"] == "O N2"

        assert "15.0.0.0" in dict_of_networks_3.keys() and dict_of_networks_3["15.0.0.0"]["Protocol"] == "O E2"
        assert "100.0.0.0" in dict_of_networks_3.keys() and dict_of_networks_3["100.0.0.0"]["Protocol"] == "O E2"

        # Remove the redistribution of static/connected

        DUT2.ospf.remove_redistribute_connected()
        DUT2.ospf.remove_redistribute_static()
        #
        # Configure metric-type 1 for the static/connected routes and check that on DUT3 and DUT1 the routes are learned accordingly (E1 for DUT3 and N1 for DUT1)

        DUT2.ospf.redistribute_connected(metric_type="1")
        DUT2.ospf.redistribute_static(metric_type="1")

        time.sleep(40)

        list_ospf_neighbors_2, dict_of_ospf_neighbors_2 = DUT2.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors_2)

        ip_route_1, networks_1, networks_connected_1, dict_of_networks_1 = DUT1.ip.show_ip_route()
        print(dict_of_networks_1)

        ip_route_3, networks_3, networks_connected_3, dict_of_networks_3 = DUT3.ip.show_ip_route()
        print(dict_of_networks_3)

        assert ip_session_1 in dict_of_ospf_neighbors_2.keys() and dict_of_ospf_neighbors_2[ip_session_1]["Neighbor-ID"] == ip_session_1 and "FULL" in dict_of_ospf_neighbors_2[ip_session_1]["State"]
        assert ip_session_3 in dict_of_ospf_neighbors_2.keys() and dict_of_ospf_neighbors_2[ip_session_3]["Neighbor-ID"] == ip_session_3 and "FULL" in dict_of_ospf_neighbors_2[ip_session_3]["State"]
        assert "15.0.0.0" in dict_of_networks_1.keys() and dict_of_networks_1["15.0.0.0"]["Protocol"] == "O N1"
        assert "100.0.0.0" in dict_of_networks_1.keys() and dict_of_networks_1["100.0.0.0"]["Protocol"] == "O N1"

        assert "15.0.0.0" in dict_of_networks_3.keys() and dict_of_networks_3["15.0.0.0"]["Protocol"] == "O E1"
        assert "100.0.0.0" in dict_of_networks_3.keys() and dict_of_networks_3["100.0.0.0"]["Protocol"] == "O E1"

        print("########## Removing the config #############")

        DUT2.ip.remove_static_route(network_dest="100.0.0.0", mask_dest="255.255.255.0", next_hop="20.0.0.2")

        DUT2.ospf.remove_redistribute_connected()
        DUT2.ospf.remove_redistribute_static()

        DUT1.ospf.remove_nssa_area(area="0.0.0.1")
        DUT2.ospf.remove_nssa_area(area="0.0.0.1")

        DUT1.ospf.remove_networks(int_vlan20=["20.0.0.2", "0.0.0.1"])
        DUT2.ospf.remove_networks(int_vlan20=["20.0.0.1", "0.0.0.1"], int_vlan12=["12.0.0.1", "0.0.0.0"])
        DUT3.ospf.remove_networks(int_vlan12=["12.0.0.2", "0.0.0.0"])

        DUT1.ospf.disable_ospf()
        DUT2.ospf.disable_ospf()
        DUT3.ospf.disable_ospf()

        DUT1.ip.remove_int_vlan(int_vlan="20")
        DUT2.ip.remove_vlan_interfaces("20", "15", "12")
        DUT3.ip.remove_vlan_interfaces("12")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5", "Gi 0/4")
        DUT1.int.shut_interface(interface="Gi 0/4")

        DUT1.vl.remove_vlan(vlan="20")
        DUT2.vl.remove_vlans("20", "15", "12")
        DUT3.vl.remove_vlans("12")

    def test_func_31(self):

        print("###### Test_func_31 ######")
        print("########## Verify that the OSPF neighbor adjacency can be established with default paramenters. Check with four neighbors with Area 0 and Area 1 configured  #############")
        print("###### 5 DUTs ######")

        #          Topology
        #
        #                  Area 0      |   Area 1
        #
        # VL15 -- DUT2 --- DUT3 ---- DUT1 --VL20-- DUT5
        #                   VL9
        #                   |
        #                  DUT4

        # No shutting the interfaces

        DUT1.int.no_shut_interfaces("Gi 0/10", "Gi 0/21")
        DUT2.int.no_shut_interfaces("Gi 0/3", "Gi 0/5")
        DUT3.int.no_shut_interfaces("Gi 0/3", "Gi 0/10", "Gi 0/11")
        DUT4.int.no_shut_interfaces("Gi 0/11")
        DUT5.int.no_shut_interfaces("Gi 0/21")

        # Creating the VLAN on DUTs

        DUT1.vl.create_vlan(vlan="9")
        DUT1.vl.create_vlan(vlan="20")

        DUT2.vl.create_vlan(vlan="15")
        DUT2.vl.create_vlan(vlan="9")

        DUT3.vl.create_vlan(vlan="9")

        DUT4.vl.create_vlan(vlan="9")

        DUT5.vl.create_vlan(vlan="20")

        # Adding the ports to the VLAN

        DUT1.vl.add_ports_to_vlan(ports="Gi 0/10", vlan="9")
        DUT1.vl.add_ports_to_vlan(ports="Gi 0/21", vlan="20")

        DUT2.vl.add_ports_to_vlan(ports="Gi 0/3", vlan="9")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")

        DUT3.vl.add_ports_to_vlan(ports="Gi 0/3", vlan="9")
        DUT3.vl.add_ports_to_vlan(ports="Gi 0/10", vlan="9")
        DUT3.vl.add_ports_to_vlan(ports="Gi 0/11", vlan="9")

        DUT4.vl.add_ports_to_vlan(ports="Gi 0/11", vlan="9")

        DUT5.vl.add_ports_to_vlan(ports="Gi 0/21", vlan="20")

        # Create IP interfaces on all DUTs for the specific VLANs

        DUT1.ip.add_ip_interfaces("9", "20", int_vlan9=["9.0.0.2", "255.255.255.0"], int_vlan20=["20.0.0.2", "255.255.255.0"])
        DUT1.ip.no_shut_int_vlans("9", "20")

        DUT2.ip.add_ip_interfaces("9", "15", int_vlan9=["9.0.0.1", "255.255.255.0"], int_vlan15=["15.0.0.1", "255.255.255.0"])
        DUT2.ip.no_shut_int_vlans("15", "9")

        DUT4.ip.add_ip_interfaces("9", int_vlan9=["9.0.0.3", "255.255.255.0"])
        DUT4.ip.no_shut_int_vlans("9")

        DUT5.ip.add_ip_interfaces("20", int_vlan20=["20.0.0.1", "255.255.255.0"])
        DUT5.ip.no_shut_int_vlans("20")

        # SHUT the UP-Link from DUT4 & DUT5 towards CAMBIUM-LAB to avoid STP loops

        DUT4.int.shut_interfaces("Gi 0/1")
        DUT5.int.shut_interfaces("Gi 0/24")

        time.sleep(20)

        # Enable OSPF on all DUTs and advertise the IPs

        DUT1.ospf.enable_ospf()
        DUT2.ospf.enable_ospf()
        DUT4.ospf.enable_ospf()
        DUT5.ospf.enable_ospf()

        DUT1.ospf.advertise_networks(int_vlan9=["9.0.0.2", "0.0.0.0"], int_vlan20=["20.0.0.2", "0.0.0.1"])
        DUT2.ospf.advertise_networks(int_vlan15=["15.0.0.1", "0.0.0.0"],  int_vlan9=["9.0.0.1", "0.0.0.0"])
        DUT4.ospf.advertise_networks(int_vlan9=["9.0.0.3", "0.0.0.0"])
        DUT5.ospf.advertise_networks(int_vlan20=["20.0.0.1", "0.0.0.1"])

        time.sleep(45)

        ip_route_1, networks_1, networks_connected_1, dict_of_networks_1 = DUT1.ip.show_ip_route()
        ip_route_2, networks_2, networks_connected_2, dict_of_networks_2 = DUT2.ip.show_ip_route()
        ip_route_4, networks_4, networks_connected_4, dict_of_networks_4 = DUT4.ip.show_ip_route()
        ip_route_5, networks_5, networks_connected_5, dict_of_networks_5 = DUT5.ip.show_ip_route()

        print("######## DUT 1 Routing Table ########")
        print(dict_of_networks_1)
        print("######## DUT 2 Routing Table ########")
        print(dict_of_networks_2)
        print("######## DUT 4 Routing Table ########")
        print(dict_of_networks_4)
        print("######## DUT 5 Routing Table ########")
        print(dict_of_networks_5)

        list_ospf_neighbors_1, dict_of_ospf_neighbors_1 = DUT1.ospf.show_ospf_neighbors()
        list_ospf_neighbors_2, dict_of_ospf_neighbors_2 = DUT2.ospf.show_ospf_neighbors()
        list_ospf_neighbors_4, dict_of_ospf_neighbors_4 = DUT4.ospf.show_ospf_neighbors()
        list_ospf_neighbors_5, dict_of_ospf_neighbors_5 = DUT5.ospf.show_ospf_neighbors()

        print("######## DUT 1 Neighbor Table ########")
        print(dict_of_ospf_neighbors_1)
        print("######## DUT 2 Neighbor Table ########")
        print(dict_of_ospf_neighbors_2)
        print("######## DUT 4 Neighbor Table ########")
        print(dict_of_ospf_neighbors_4)
        print("######## DUT 5 Neighbor Table ########")
        print(dict_of_ospf_neighbors_5)

        # Check if the routes are learned and installed in OSPF routes

        # DUT 1
        assert "15.0.0.0" in dict_of_networks_1.keys() and dict_of_networks_1["15.0.0.0"]["Protocol"] == "O"

        # DUT 2
        assert "20.0.0.0" in dict_of_networks_2.keys() and dict_of_networks_2["20.0.0.0"]["Protocol"] == "O IA"

        # DUT 4
        assert "15.0.0.0" in dict_of_networks_4.keys() and dict_of_networks_4["15.0.0.0"]["Protocol"] == "O"
        assert "20.0.0.0" in dict_of_networks_4.keys() and dict_of_networks_4["20.0.0.0"]["Protocol"] == "O IA"

        # DUT 5
        assert "15.0.0.0" in dict_of_networks_5.keys() and dict_of_networks_5["15.0.0.0"]["Protocol"] == "O IA"
        assert "9.0.0.0" in dict_of_networks_5.keys() and dict_of_networks_5["9.0.0.0"]["Protocol"] == "O IA"

        # Check DR is DUT4 (the highest IP from election), BDR is DUT1 and DROthers is DUT2 (the lowest IP)

        assert dict_of_ospf_neighbors_1["9.0.0.1"]["State"] == "FULL/DR_OTHER" and dict_of_ospf_neighbors_1["9.0.0.3"]["State"] == "FULL/DR"
        assert dict_of_ospf_neighbors_2["9.0.0.2"]["State"] == "FULL/BACKUP" and dict_of_ospf_neighbors_2["9.0.0.3"]["State"] == "FULL/DR"
        assert dict_of_ospf_neighbors_4["9.0.0.1"]["State"] == "FULL/DR_OTHER" and dict_of_ospf_neighbors_4["9.0.0.2"]["State"] == "FULL/BACKUP"
        assert dict_of_ospf_neighbors_5["9.0.0.2"]["State"] == "FULL/BACKUP" and dict_of_ospf_neighbors_1[ip_session_5]["State"] == "FULL/DR"

        print("########## Removing the config #############")

        DUT4.int.no_shut_interfaces("Gi 0/1")
        DUT5.int.no_shut_interfaces("Gi 0/24")

        DUT1.ospf.remove_networks(int_vlan9=["9.0.0.2", "0.0.0.0"],int_vlan20=["20.0.0.2", "0.0.0.1"])
        DUT2.ospf.remove_networks(int_vlan15=["15.0.0.1", "0.0.0.0"],  int_vlan9=["9.0.0.1", "0.0.0.0"])
        DUT4.ospf.remove_networks(int_vlan9=["9.0.0.3", "0.0.0.0"])
        DUT5.ospf.remove_networks(int_vlan20=["20.0.0.1", "0.0.0.1"])

        DUT1.ospf.disable_ospf()
        DUT2.ospf.disable_ospf()
        DUT4.ospf.disable_ospf()
        DUT5.ospf.disable_ospf()

        DUT1.ip.remove_vlan_interfaces("9", "20")
        DUT2.ip.remove_vlan_interfaces("15", "9")
        DUT4.ip.remove_vlan_interfaces("9")
        DUT5.ip.remove_vlan_interfaces("20")

        DUT1.vl.remove_vlans("9", "20")
        DUT2.vl.remove_vlans("15", "9")
        DUT3.vl.remove_vlan("9")
        DUT4.vl.remove_vlan("9")
        DUT5.vl.remove_vlan("20")

        DUT1.int.shut_interfaces("Gi 0/10", "Gi 0/21")
        DUT2.int.shut_interfaces("Gi 0/5", "Gi 0/3")
        DUT3.int.shut_interfaces("Gi 0/3", "Gi 0/10", "Gi 0/11")
        DUT4.int.shut_interfaces("Gi 0/11")
        DUT5.int.shut_interfaces("Gi 0/21")

    def test_func_32(self):

        print("###### Test_func_32 ######")
        print("########## Verify the network type Non-Broadcast ( SVI )  #############")
        print("###### 4 DUTs ######")

        #          Topology
        #
        #  DUT1 --- DUT3 ---- DUT2 -- VL15
        #             |
        #           DUT4

        # No shutting the interfaces

        DUT1.int.no_shut_interfaces("Gi 0/10")
        DUT2.int.no_shut_interfaces("Gi 0/3", "Gi 0/5")
        DUT3.int.no_shut_interfaces("Gi 0/3", "Gi 0/10", "Gi 0/11")
        DUT4.int.no_shut_interfaces("Gi 0/11")

        # Creating the VLAN on DUTs

        DUT1.vl.create_vlan(vlan="9")
        DUT2.vl.create_vlan(vlan="15")
        DUT2.vl.create_vlan(vlan="9")
        DUT3.vl.create_vlan(vlan="9")
        DUT4.vl.create_vlan(vlan="9")

        # Adding the ports to the VLAN

        DUT1.vl.add_ports_to_vlan(ports="Gi 0/10", vlan="9")

        DUT2.vl.add_ports_to_vlan(ports="Gi 0/3", vlan="9")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")

        DUT3.vl.add_ports_to_vlan(ports="Gi 0/3", vlan="9")
        DUT3.vl.add_ports_to_vlan(ports="Gi 0/10", vlan="9")
        DUT3.vl.add_ports_to_vlan(ports="Gi 0/11", vlan="9")

        DUT4.vl.add_ports_to_vlan(ports="Gi 0/11", vlan="9")

        # Create IP interfaces on all DUTs for the specific VLANs

        DUT1.ip.add_ip_interfaces("9", int_vlan9=["9.0.0.2", "255.255.255.0"])
        DUT1.ip.no_shut_int_vlans("9")

        DUT2.ip.add_ip_interfaces("9", "15", int_vlan9=["9.0.0.1", "255.255.255.0"], int_vlan15=["15.0.0.1", "255.255.255.0"])
        DUT2.ip.no_shut_int_vlans("15", "9")

        DUT4.ip.add_ip_interfaces("9", int_vlan9=["9.0.0.3", "255.255.255.0"])
        DUT4.ip.no_shut_int_vlans("9")

        # SHUT the UP-Link from DUT4 towards CAMBIUM-LAB to avoid STP loops

        DUT4.int.shut_interfaces("Gi 0/1")
        time.sleep(20)

        # Enable OSPF on all DUTs and advertise the IPs

        DUT1.ospf.enable_ospf()
        DUT2.ospf.enable_ospf()
        DUT4.ospf.enable_ospf()

        DUT1.ospf.advertise_networks(int_vlan9=["9.0.0.2", "0.0.0.0"])
        DUT2.ospf.advertise_networks(int_vlan15=["15.0.0.1", "0.0.0.0"],  int_vlan9=["9.0.0.1", "0.0.0.0"])
        DUT4.ospf.advertise_networks(int_vlan9=["9.0.0.3", "0.0.0.0"])

        # Configure the int VLAN between the DUTs to be Non-Broadcast and advertise the neighbors

        DUT1.ospf.configure_network_type(int_vlan="9", network_type="non-broadcast")
        DUT2.ospf.configure_network_type(int_vlan="9", network_type="non-broadcast")
        DUT4.ospf.configure_network_type(int_vlan="9", network_type="non-broadcast")

        DUT1.ospf.configure_neighbors("9.0.0.1", "9.0.0.3")
        DUT2.ospf.configure_neighbors("9.0.0.2", "9.0.0.3")
        DUT4.ospf.configure_neighbors("9.0.0.1", "9.0.0.2")

        # Shut/No-shut the ports from DUT3 to redo the election of DR/BDR

        DUT3.int.shut_interfaces("Gi 0/3", "Gi 0/10", "Gi 0/11")
        DUT3.int.no_shut_interfaces("Gi 0/3", "Gi 0/10", "Gi 0/11")

        time.sleep(45)

        network_type_1 = DUT1.ospf.show_ip_ospf_interface(int_vlan="9")
        network_type_2 = DUT2.ospf.show_ip_ospf_interface(int_vlan="9")
        network_type_4 = DUT4.ospf.show_ip_ospf_interface(int_vlan="9")

        print(network_type_1)
        print(network_type_2)
        print(network_type_4)

        # Check the network type of the interfaces to be NBMA

        assert "NBMA" in network_type_1
        assert "NBMA" in network_type_2
        assert "NBMA" in network_type_4

        ip_route_1, networks_1, networks_connected_1, dict_of_networks_1 = DUT1.ip.show_ip_route()
        ip_route_2, networks_2, networks_connected_2, dict_of_networks_2 = DUT2.ip.show_ip_route()
        ip_route_4, networks_4, networks_connected_4, dict_of_networks_4 = DUT4.ip.show_ip_route()

        print("######## DUT 1 Routing Table ########")
        print(dict_of_networks_1)
        print("######## DUT 2 Routing Table ########")
        print(dict_of_networks_2)
        print("######## DUT 4 Routing Table ########")
        print(dict_of_networks_4)

        list_ospf_neighbors_1, dict_of_ospf_neighbors_1 = DUT1.ospf.show_ospf_neighbors()
        list_ospf_neighbors_2, dict_of_ospf_neighbors_2 = DUT2.ospf.show_ospf_neighbors()
        list_ospf_neighbors_4, dict_of_ospf_neighbors_4 = DUT4.ospf.show_ospf_neighbors()

        print("######## DUT 1 Neighbor Table ########")
        print(dict_of_ospf_neighbors_1)
        print("######## DUT 2 Neighbor Table ########")
        print(dict_of_ospf_neighbors_2)
        print("######## DUT 4 Neighbor Table ########")
        print(dict_of_ospf_neighbors_4)

        # Check if the routes are learned and installed in OSPF routes

        # DUT 1
        assert "15.0.0.0" in dict_of_networks_1.keys() and dict_of_networks_1["15.0.0.0"]["Protocol"] == "O"

        # DUT 4
        assert "15.0.0.0" in dict_of_networks_4.keys() and dict_of_networks_4["15.0.0.0"]["Protocol"] == "O"

        # Check DR is DUT4 (the highest IP from election), BDR is DUT1 and DROthers is DUT2 (the lowest IP)

        assert dict_of_ospf_neighbors_1["9.0.0.1"]["State"] == "FULL/DR_OTHER" and dict_of_ospf_neighbors_1["9.0.0.3"]["State"] == "FULL/DR"
        assert dict_of_ospf_neighbors_2["9.0.0.2"]["State"] == "FULL/BACKUP" and dict_of_ospf_neighbors_2["9.0.0.3"]["State"] == "FULL/DR"
        assert dict_of_ospf_neighbors_4["9.0.0.1"]["State"] == "FULL/DR_OTHER" and dict_of_ospf_neighbors_4["9.0.0.2"]["State"] == "FULL/BACKUP"

        print("########## Removing the config #############")

        DUT4.int.no_shut_interfaces("Gi 0/1")

        DUT1.ospf.remove_neighbors("9.0.0.1", "9.0.0.3")
        DUT2.ospf.remove_neighbors("9.0.0.2", "9.0.0.3")
        DUT4.ospf.remove_neighbors("9.0.0.1", "9.0.0.2")

        DUT1.ospf.remove_network_type(int_vlan="9")
        DUT2.ospf.remove_network_type(int_vlan="9")
        DUT4.ospf.remove_network_type(int_vlan="9")

        DUT1.ospf.remove_networks(int_vlan9=["9.0.0.2", "0.0.0.0"])
        DUT2.ospf.remove_networks(int_vlan15=["15.0.0.1", "0.0.0.0"],  int_vlan9=["9.0.0.1", "0.0.0.0"])
        DUT4.ospf.remove_networks(int_vlan9=["9.0.0.3", "0.0.0.0"])

        DUT1.ospf.disable_ospf()
        DUT2.ospf.disable_ospf()
        DUT4.ospf.disable_ospf()

        DUT1.ip.remove_vlan_interfaces("9")
        DUT2.ip.remove_vlan_interfaces("15", "9")
        DUT4.ip.remove_vlan_interfaces("9")

        DUT1.vl.remove_vlan("9")
        DUT2.vl.remove_vlans("15","9")
        DUT3.vl.remove_vlan("9")
        DUT4.vl.remove_vlan("9")

        DUT1.int.shut_interfaces("Gi 0/10")
        DUT2.int.shut_interfaces("Gi 0/5", "Gi 0/3")
        DUT3.int.shut_interfaces("Gi 0/3", "Gi 0/10", "Gi 0/11")
        DUT4.int.shut_interfaces("Gi 0/11")

    def test_func_33(self):

        print("###### Test_func_33 ######")
        print("########## Verify the network type Point-To-Multipoint Non-Broadcast ( SVI )  #############")
        print("###### 4 DUTs ######")

        #          Topology
        #
        #  DUT1 --- DUT3 ---- DUT2 -- VL15
        #             |
        #           DUT4

        # No shutting the interfaces

        DUT1.int.no_shut_interfaces("Gi 0/10")
        DUT2.int.no_shut_interfaces("Gi 0/3", "Gi 0/5")
        DUT3.int.no_shut_interfaces("Gi 0/3", "Gi 0/10", "Gi 0/11")
        DUT4.int.no_shut_interfaces("Gi 0/11")

        # Creating the VLAN on DUTs

        DUT1.vl.create_vlan(vlan="9")
        DUT2.vl.create_vlan(vlan="15")
        DUT2.vl.create_vlan(vlan="9")
        DUT3.vl.create_vlan(vlan="9")
        DUT4.vl.create_vlan(vlan="9")

        # Adding the ports to the VLAN

        DUT1.vl.add_ports_to_vlan(ports="Gi 0/10", vlan="9")

        DUT2.vl.add_ports_to_vlan(ports="Gi 0/3", vlan="9")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")

        DUT3.vl.add_ports_to_vlan(ports="Gi 0/3", vlan="9")
        DUT3.vl.add_ports_to_vlan(ports="Gi 0/10", vlan="9")
        DUT3.vl.add_ports_to_vlan(ports="Gi 0/11", vlan="9")

        DUT4.vl.add_ports_to_vlan(ports="Gi 0/11", vlan="9")

        # Create IP interfaces on all DUTs for the specific VLANs

        DUT1.ip.add_ip_interfaces("9", int_vlan9=["9.0.0.2", "255.255.255.0"])
        DUT1.ip.no_shut_int_vlans("9")

        DUT2.ip.add_ip_interfaces("9", "15", int_vlan9=["9.0.0.1", "255.255.255.0"], int_vlan15=["15.0.0.1", "255.255.255.0"])
        DUT2.ip.no_shut_int_vlans("15", "9")

        DUT4.ip.add_ip_interfaces("9", int_vlan9=["9.0.0.3", "255.255.255.0"])
        DUT4.ip.no_shut_int_vlans("9")

        # SHUT the UP-Link from DUT4 towards CAMBIUM-LAB to avoid STP loops

        DUT4.int.shut_interfaces("Gi 0/1")
        time.sleep(20)

        # Enable OSPF on all DUTs and advertise the IPs

        DUT1.ospf.enable_ospf()
        DUT2.ospf.enable_ospf()
        DUT4.ospf.enable_ospf()

        DUT1.ospf.advertise_networks(int_vlan9=["9.0.0.2", "0.0.0.0"])
        DUT2.ospf.advertise_networks(int_vlan15=["15.0.0.1", "0.0.0.0"],  int_vlan9=["9.0.0.1", "0.0.0.0"])
        DUT4.ospf.advertise_networks(int_vlan9=["9.0.0.3", "0.0.0.0"])

        # Configure the int VLAN between the DUTs to be Point-to-Multipoint non-broadcast and advertise the neighbors

        DUT1.ospf.configure_network_type(int_vlan="9", network_type="point-to-multipoint non-broadcast ")
        DUT2.ospf.configure_network_type(int_vlan="9", network_type="point-to-multipoint non-broadcast ")
        DUT4.ospf.configure_network_type(int_vlan="9", network_type="point-to-multipoint non-broadcast ")

        DUT1.ospf.configure_neighbors("9.0.0.1", "9.0.0.3")
        DUT2.ospf.configure_neighbors("9.0.0.2", "9.0.0.3")
        DUT4.ospf.configure_neighbors("9.0.0.1", "9.0.0.2")

        # Shut/No-shut the ports from DUT3

        DUT3.int.shut_interfaces("Gi 0/3", "Gi 0/10", "Gi 0/11")
        DUT3.int.no_shut_interfaces("Gi 0/3", "Gi 0/10", "Gi 0/11")

        time.sleep(45)

        network_type_1 = DUT1.ospf.show_ip_ospf_interface(int_vlan="9")
        network_type_2 = DUT2.ospf.show_ip_ospf_interface(int_vlan="9")
        network_type_4 = DUT4.ospf.show_ip_ospf_interface(int_vlan="9")

        print(network_type_1)
        print(network_type_2)
        print(network_type_4)

        # Check the network type of the interfaces to be Point-to-Multipoint

        assert "PointToMultiPoint" in network_type_1
        assert "PointToMultiPoint" in network_type_2
        assert "PointToMultiPoint" in network_type_4

        ip_route_1, networks_1, networks_connected_1, dict_of_networks_1 = DUT1.ip.show_ip_route()
        ip_route_2, networks_2, networks_connected_2, dict_of_networks_2 = DUT2.ip.show_ip_route()
        ip_route_4, networks_4, networks_connected_4, dict_of_networks_4 = DUT4.ip.show_ip_route()

        print("######## DUT 1 Routing Table ########")
        print(dict_of_networks_1)
        print("######## DUT 2 Routing Table ########")
        print(dict_of_networks_2)
        print("######## DUT 4 Routing Table ########")
        print(dict_of_networks_4)

        list_ospf_neighbors_1, dict_of_ospf_neighbors_1 = DUT1.ospf.show_ospf_neighbors()
        list_ospf_neighbors_2, dict_of_ospf_neighbors_2 = DUT2.ospf.show_ospf_neighbors()
        list_ospf_neighbors_4, dict_of_ospf_neighbors_4 = DUT4.ospf.show_ospf_neighbors()

        print("######## DUT 1 Neighbor Table ########")
        print(dict_of_ospf_neighbors_1)
        print("######## DUT 2 Neighbor Table ########")
        print(dict_of_ospf_neighbors_2)
        print("######## DUT 4 Neighbor Table ########")
        print(dict_of_ospf_neighbors_4)

        # Check if the routes are learned and installed in OSPF routes

        # DUT 1
        assert "15.0.0.0" in dict_of_networks_1.keys() and dict_of_networks_1["15.0.0.0"]["Protocol"] == "O"

        # DUT 4
        assert "15.0.0.0" in dict_of_networks_4.keys() and dict_of_networks_4["15.0.0.0"]["Protocol"] == "O"

        # Check all neighbors are PTOP

        assert dict_of_ospf_neighbors_1["9.0.0.1"]["State"] == "FULL/PTOP" and dict_of_ospf_neighbors_1["9.0.0.3"]["State"] == "FULL/PTOP"
        assert dict_of_ospf_neighbors_2["9.0.0.2"]["State"] == "FULL/PTOP" and dict_of_ospf_neighbors_2["9.0.0.3"]["State"] == "FULL/PTOP"
        assert dict_of_ospf_neighbors_4["9.0.0.1"]["State"] == "FULL/PTOP" and dict_of_ospf_neighbors_4["9.0.0.2"]["State"] == "FULL/PTOP"

        print("########## Removing the config #############")

        DUT4.int.no_shut_interfaces("Gi 0/1")

        DUT1.ospf.remove_neighbors("9.0.0.1", "9.0.0.3")
        DUT2.ospf.remove_neighbors("9.0.0.2", "9.0.0.3")
        DUT4.ospf.remove_neighbors("9.0.0.1", "9.0.0.2")

        DUT1.ospf.remove_network_type(int_vlan="9")
        DUT2.ospf.remove_network_type(int_vlan="9")
        DUT4.ospf.remove_network_type(int_vlan="9")

        DUT1.ospf.remove_networks(int_vlan9=["9.0.0.2", "0.0.0.0"])
        DUT2.ospf.remove_networks(int_vlan15=["15.0.0.1", "0.0.0.0"],  int_vlan9=["9.0.0.1", "0.0.0.0"])
        DUT4.ospf.remove_networks(int_vlan9=["9.0.0.3", "0.0.0.0"])

        DUT1.ospf.disable_ospf()
        DUT2.ospf.disable_ospf()
        DUT4.ospf.disable_ospf()

        DUT1.ip.remove_vlan_interfaces("9")
        DUT2.ip.remove_vlan_interfaces("15", "9")
        DUT4.ip.remove_vlan_interfaces("9")

        DUT1.vl.remove_vlan("9")
        DUT2.vl.remove_vlans("15","9")
        DUT3.vl.remove_vlan("9")
        DUT4.vl.remove_vlan("9")

        DUT1.int.shut_interfaces("Gi 0/10")
        DUT2.int.shut_interfaces("Gi 0/5", "Gi 0/3")
        DUT3.int.shut_interfaces("Gi 0/3", "Gi 0/10", "Gi 0/11")
        DUT4.int.shut_interfaces("Gi 0/11")

    def test_func_34(self):

        print("###### Test_func_34 ######")
        print("########## Verify the network type Point-To-Point ( SVI )  #############")
        print("###### 2 DUTs ######")

        #          Topology
        #
        #  DUT1 ---- DUT2 -- VL15
        #

        # No shutting the interfaces

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/9", "Gi 0/5")

        # Creating the VLAN on DUTs

        DUT1.vl.create_vlan(vlan="9")
        DUT2.vl.create_vlan(vlan="15")
        DUT2.vl.create_vlan(vlan="9")

        # Adding the ports to the VLAN

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="9")

        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="9")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")

        # Create IP interfaces on all DUTs for the specific VLANs

        DUT1.ip.add_ip_interfaces("9", int_vlan9=["9.0.0.2", "255.255.255.0"])
        DUT1.ip.no_shut_int_vlans("9")

        DUT2.ip.add_ip_interfaces("9", "15", int_vlan9=["9.0.0.1", "255.255.255.0"], int_vlan15=["15.0.0.1", "255.255.255.0"])
        DUT2.ip.no_shut_int_vlans("15", "9")

        # Enable OSPF on all DUTs and advertise the IPs

        DUT1.ospf.enable_ospf()
        DUT2.ospf.enable_ospf()

        DUT1.ospf.advertise_networks(int_vlan9=["9.0.0.2", "0.0.0.0"])
        DUT2.ospf.advertise_networks(int_vlan15=["15.0.0.1", "0.0.0.0"],  int_vlan9=["9.0.0.1", "0.0.0.0"])

        # Configure the int VLAN between the DUTs to be Point-to-point

        DUT1.ospf.configure_network_type(int_vlan="9", network_type="point-to-point")
        DUT2.ospf.configure_network_type(int_vlan="9", network_type="point-to-point")

        time.sleep(45)

        network_type_1 = DUT1.ospf.show_ip_ospf_interface(int_vlan="9")
        network_type_2 = DUT2.ospf.show_ip_ospf_interface(int_vlan="9")

        print(network_type_1)
        print(network_type_2)

        # Check the network type of the interfaces to be Point-to-point

        assert "PointToPoint" in network_type_1
        assert "PointToPoint" in network_type_2

        ip_route_1, networks_1, networks_connected_1, dict_of_networks_1 = DUT1.ip.show_ip_route()
        ip_route_2, networks_2, networks_connected_2, dict_of_networks_2 = DUT2.ip.show_ip_route()

        print("######## DUT 1 Routing Table ########")
        print(dict_of_networks_1)
        print("######## DUT 2 Routing Table ########")
        print(dict_of_networks_2)

        list_ospf_neighbors_1, dict_of_ospf_neighbors_1 = DUT1.ospf.show_ospf_neighbors()
        list_ospf_neighbors_2, dict_of_ospf_neighbors_2 = DUT2.ospf.show_ospf_neighbors()

        print("######## DUT 1 Neighbor Table ########")
        print(dict_of_ospf_neighbors_1)
        print("######## DUT 2 Neighbor Table ########")
        print(dict_of_ospf_neighbors_2)

        # Check if the routes are learned and installed in OSPF routes

        # DUT 1
        assert "15.0.0.0" in dict_of_networks_1.keys() and dict_of_networks_1["15.0.0.0"]["Protocol"] == "O"

        # Check all neighbors are PTOP

        assert dict_of_ospf_neighbors_1["9.0.0.1"]["State"] == "FULL/PTOP"
        assert dict_of_ospf_neighbors_2["9.0.0.2"]["State"] == "FULL/PTOP"

        print("########## Removing the config #############")

        DUT1.ospf.remove_network_type(int_vlan="9")
        DUT2.ospf.remove_network_type(int_vlan="9")

        DUT1.ospf.remove_networks(int_vlan9=["9.0.0.2", "0.0.0.0"])
        DUT2.ospf.remove_networks(int_vlan15=["15.0.0.1", "0.0.0.0"],  int_vlan9=["9.0.0.1", "0.0.0.0"])

        DUT1.ospf.disable_ospf()
        DUT2.ospf.disable_ospf()

        DUT1.ip.remove_vlan_interfaces("9")
        DUT2.ip.remove_vlan_interfaces("15", "9")

        DUT1.vl.remove_vlan("9")
        DUT2.vl.remove_vlans("15", "9")

        DUT1.int.shut_interfaces("Gi 0/10")
        DUT2.int.shut_interfaces("Gi 0/5", "Gi 0/3")

    def test_func_35(self):

        print("###### Test_func_35 ######")
        print("########## Verify the network type Non-Broadcast ( Routed Ports )  #############")
        print("###### 4 DUTs ######")

        #          Topology
        #
        #  DUT1 --- DUT3 ---- DUT2 -- VL15
        #             |
        #           DUT4

        # Creating routed ports on all DUTs

        DUT1.int.add_routed_ports("Gi 0/10")
        DUT2.int.add_routed_ports("Gi 0/3")
        DUT4.int.add_routed_ports("Gi 0/11")

        # No shutting the interfaces

        DUT1.int.no_shut_interfaces("Gi 0/10")
        DUT2.int.no_shut_interfaces("Gi 0/3", "Gi 0/5")
        DUT3.int.no_shut_interfaces("Gi 0/3", "Gi 0/10", "Gi 0/11")
        DUT4.int.no_shut_interfaces("Gi 0/11")

        # Creating the VLAN on DUT2

        DUT2.vl.create_vlan(vlan="15")

        # Adding the ports to the VLAN

        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")

        # Create IP Routed Ports on all DUTs except DUT3 which is the "HUB"

        DUT1.ip.add_ip_routed_ports("Gi 0/10", Gi_0_10=["9.0.0.2", "255.255.255.0"])

        DUT2.ip.add_ip_routed_ports("Gi 0/3", Gi_0_3=["9.0.0.1", "255.255.255.0"])
        DUT2.ip.add_ip_interface(int_vlan="15", ip="15.0.0.1", mask="255.255.255.0")
        DUT2.ip.no_shut_int_vlan(int_vlan="15")

        DUT4.ip.add_ip_routed_ports("Gi 0/11", Gi_0_11=["9.0.0.3", "255.255.255.0"])

        # Enable OSPF on all DUTs and advertise the IPs

        DUT1.ospf.enable_ospf()
        DUT2.ospf.enable_ospf()
        DUT4.ospf.enable_ospf()

        DUT1.ospf.advertise_networks(Gi_0_10=["9.0.0.2", "0.0.0.0"])
        DUT2.ospf.advertise_networks(int_vlan15=["15.0.0.1", "0.0.0.0"], Gi_0_3=["9.0.0.1", "0.0.0.0"])
        DUT4.ospf.advertise_networks(Gi_0_11=["9.0.0.3", "0.0.0.0"])

        # Configure the Routed Ports between the DUTs to be Non-Broadcast and advertise the neighbors

        DUT1.ospf.configure_network_type(interface="Gi 0/10", network_type="non-broadcast")
        DUT2.ospf.configure_network_type(interface="Gi 0/3", network_type="non-broadcast")
        DUT4.ospf.configure_network_type(interface="Gi 0/11", network_type="non-broadcast")

        DUT1.ospf.configure_neighbors("9.0.0.1", "9.0.0.3")
        DUT2.ospf.configure_neighbors("9.0.0.2", "9.0.0.3")
        DUT4.ospf.configure_neighbors("9.0.0.1", "9.0.0.2")

        # Shut/No-shut the ports from DUT3 to redo the election of DR/BDR

        DUT3.int.shut_interfaces("Gi 0/3", "Gi 0/10", "Gi 0/11")
        DUT3.int.no_shut_interfaces("Gi 0/3", "Gi 0/10", "Gi 0/11")

        time.sleep(45)

        network_type_1 = DUT1.ospf.show_ip_ospf_interface(interface="Gi 0/10")
        network_type_2 = DUT2.ospf.show_ip_ospf_interface(interface="Gi 0/3")
        network_type_4 = DUT4.ospf.show_ip_ospf_interface(interface="Gi 0/11")

        print(network_type_1)
        print(network_type_2)
        print(network_type_4)

        # Check the network type of the interfaces to be NBMA

        assert "NBMA" in network_type_1
        assert "NBMA" in network_type_2
        assert "NBMA" in network_type_4

        ip_route_1, networks_1, networks_connected_1, dict_of_networks_1 = DUT1.ip.show_ip_route()
        ip_route_2, networks_2, networks_connected_2, dict_of_networks_2 = DUT2.ip.show_ip_route()
        ip_route_4, networks_4, networks_connected_4, dict_of_networks_4 = DUT4.ip.show_ip_route()

        print("######## DUT 1 Routing Table ########")
        print(dict_of_networks_1)
        print("######## DUT 2 Routing Table ########")
        print(dict_of_networks_2)
        print("######## DUT 4 Routing Table ########")
        print(dict_of_networks_4)

        list_ospf_neighbors_1, dict_of_ospf_neighbors_1 = DUT1.ospf.show_ospf_neighbors()
        list_ospf_neighbors_2, dict_of_ospf_neighbors_2 = DUT2.ospf.show_ospf_neighbors()
        list_ospf_neighbors_4, dict_of_ospf_neighbors_4 = DUT4.ospf.show_ospf_neighbors()

        print("######## DUT 1 Neighbor Table ########")
        print(dict_of_ospf_neighbors_1)
        print("######## DUT 2 Neighbor Table ########")
        print(dict_of_ospf_neighbors_2)
        print("######## DUT 4 Neighbor Table ########")
        print(dict_of_ospf_neighbors_4)

        # Check if the routes are learned and installed in OSPF routes

        # DUT 1
        assert "15.0.0.0" in dict_of_networks_1.keys() and dict_of_networks_1["15.0.0.0"]["Protocol"] == "O"

        # DUT 4
        assert "15.0.0.0" in dict_of_networks_4.keys() and dict_of_networks_4["15.0.0.0"]["Protocol"] == "O"

        # Check DR is DUT4 (the highest IP from election), BDR is DUT1 and DROthers is DUT2 (the lowest IP)

        assert dict_of_ospf_neighbors_1["9.0.0.1"]["State"] == "FULL/DR_OTHER" and dict_of_ospf_neighbors_1["9.0.0.3"]["State"] == "FULL/DR"
        assert dict_of_ospf_neighbors_2["9.0.0.2"]["State"] == "FULL/BACKUP" and dict_of_ospf_neighbors_2["9.0.0.3"]["State"] == "FULL/DR"
        assert dict_of_ospf_neighbors_4["9.0.0.1"]["State"] == "FULL/DR_OTHER" and dict_of_ospf_neighbors_4["9.0.0.2"]["State"] == "FULL/BACKUP"

        print("########## Removing the config #############")

        DUT1.ospf.remove_neighbors("9.0.0.1", "9.0.0.3")
        DUT2.ospf.remove_neighbors("9.0.0.2", "9.0.0.3")
        DUT4.ospf.remove_neighbors("9.0.0.1", "9.0.0.2")

        DUT1.ospf.remove_network_type(interface="Gi 0/10")
        DUT2.ospf.remove_network_type(interface="Gi 0/3")
        DUT4.ospf.remove_network_type(interface="Gi 0/11")

        DUT1.ospf.remove_networks(Gi_0_10=["9.0.0.2", "0.0.0.0"])
        DUT2.ospf.remove_networks(int_vlan15=["15.0.0.1", "0.0.0.0"], Gi_0_3=["9.0.0.1", "0.0.0.0"])
        DUT4.ospf.remove_networks(Gi_0_11=["9.0.0.3", "0.0.0.0"])

        DUT1.ospf.disable_ospf()
        DUT2.ospf.disable_ospf()
        DUT4.ospf.disable_ospf()

        DUT2.ip.remove_vlan_interfaces("15")

        DUT2.vl.remove_vlans("15")

        DUT1.int.remove_routed_ports("Gi 0/10")
        DUT2.int.remove_routed_ports("Gi 0/3")
        DUT4.int.remove_routed_ports("Gi 0/11")

        DUT2.int.shut_interfaces("Gi 0/5")
        DUT3.int.shut_interfaces("Gi 0/3", "Gi 0/10", "Gi 0/11")

    def test_func_36(self):

        print("###### Test_func_36 ######")
        print("########## Verify the network type Point-To-Multipoint Non-Broadcast ( Routed Ports )  #############")
        print("###### 4 DUTs ######")

        #          Topology
        #
        #  DUT1 --- DUT3 ---- DUT2 -- VL15
        #             |
        #           DUT4

        # Creating routed ports on all DUTs

        DUT1.int.add_routed_ports("Gi 0/10")
        DUT2.int.add_routed_ports("Gi 0/3")
        DUT4.int.add_routed_ports("Gi 0/11")

        # No shutting the interfaces

        DUT1.int.no_shut_interfaces("Gi 0/10")
        DUT2.int.no_shut_interfaces("Gi 0/3", "Gi 0/5")
        DUT3.int.no_shut_interfaces("Gi 0/3", "Gi 0/10", "Gi 0/11")
        DUT4.int.no_shut_interfaces("Gi 0/11")

        # Creating the VLAN on DUT2

        DUT2.vl.create_vlan(vlan="15")

        # Adding the ports to the VLAN

        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")

        # Create IP Routed Ports on all DUTs except DUT3 which is the "HUB"

        DUT1.ip.add_ip_routed_ports("Gi 0/10", Gi_0_10=["9.0.0.2", "255.255.255.0"])

        DUT2.ip.add_ip_routed_ports("Gi 0/3", Gi_0_3=["9.0.0.1", "255.255.255.0"])
        DUT2.ip.add_ip_interface(int_vlan="15", ip="15.0.0.1", mask="255.255.255.0")
        DUT2.ip.no_shut_int_vlan(int_vlan="15")

        DUT4.ip.add_ip_routed_ports("Gi 0/11", Gi_0_11=["9.0.0.3", "255.255.255.0"])

        # Enable OSPF on all DUTs and advertise the IPs

        DUT1.ospf.enable_ospf()
        DUT2.ospf.enable_ospf()
        DUT4.ospf.enable_ospf()

        DUT1.ospf.advertise_networks(Gi_0_10=["9.0.0.2", "0.0.0.0"])
        DUT2.ospf.advertise_networks(int_vlan15=["15.0.0.1", "0.0.0.0"], Gi_0_3=["9.0.0.1", "0.0.0.0"])
        DUT4.ospf.advertise_networks(Gi_0_11=["9.0.0.3", "0.0.0.0"])

        # Configure the Routed Ports between the DUTs to be Point-to-Multipoint Non-broadcast and advertise the neighbors

        DUT1.ospf.configure_network_type(interface="Gi 0/10", network_type="point-to-multipoint non-broadcast")
        DUT2.ospf.configure_network_type(interface="Gi 0/3", network_type="point-to-multipoint non-broadcast")
        DUT4.ospf.configure_network_type(interface="Gi 0/11", network_type="point-to-multipoint non-broadcast")

        DUT1.ospf.configure_neighbors("9.0.0.1", "9.0.0.3")
        DUT2.ospf.configure_neighbors("9.0.0.2", "9.0.0.3")
        DUT4.ospf.configure_neighbors("9.0.0.1", "9.0.0.2")

        # Shut/No-shut the ports from DUT3

        DUT3.int.shut_interfaces("Gi 0/10", "Gi 0/3", "Gi 0/11")
        DUT3.int.no_shut_interfaces("Gi 0/10", "Gi 0/3", "Gi 0/11")

        time.sleep(45)

        network_type_1 = DUT1.ospf.show_ip_ospf_interface(interface="Gi 0/10")
        network_type_2 = DUT2.ospf.show_ip_ospf_interface(interface="Gi 0/3")
        network_type_4 = DUT4.ospf.show_ip_ospf_interface(interface="Gi 0/11")

        print(network_type_1)
        print(network_type_2)
        print(network_type_4)

        # Check the network type of the interfaces to be PointToMultiPoint

        assert "PointToMultiPoint" in network_type_1
        assert "PointToMultiPoint" in network_type_2
        assert "PointToMultiPoint" in network_type_4

        ip_route_1, networks_1, networks_connected_1, dict_of_networks_1 = DUT1.ip.show_ip_route()
        ip_route_2, networks_2, networks_connected_2, dict_of_networks_2 = DUT2.ip.show_ip_route()
        ip_route_4, networks_4, networks_connected_4, dict_of_networks_4 = DUT4.ip.show_ip_route()

        print("######## DUT 1 Routing Table ########")
        print(dict_of_networks_1)
        print("######## DUT 2 Routing Table ########")
        print(dict_of_networks_2)
        print("######## DUT 4 Routing Table ########")
        print(dict_of_networks_4)

        list_ospf_neighbors_1, dict_of_ospf_neighbors_1 = DUT1.ospf.show_ospf_neighbors()
        list_ospf_neighbors_2, dict_of_ospf_neighbors_2 = DUT2.ospf.show_ospf_neighbors()
        list_ospf_neighbors_4, dict_of_ospf_neighbors_4 = DUT4.ospf.show_ospf_neighbors()

        print("######## DUT 1 Neighbor Table ########")
        print(dict_of_ospf_neighbors_1)
        print("######## DUT 2 Neighbor Table ########")
        print(dict_of_ospf_neighbors_2)
        print("######## DUT 4 Neighbor Table ########")
        print(dict_of_ospf_neighbors_4)

        # Check if the routes are learned and installed in OSPF routes

        # DUT 1
        assert "15.0.0.0" in dict_of_networks_1.keys() and dict_of_networks_1["15.0.0.0"]["Protocol"] == "O"

        # DUT 4
        assert "15.0.0.0" in dict_of_networks_4.keys() and dict_of_networks_4["15.0.0.0"]["Protocol"] == "O"

        # Check all neighbors are PTOP

        assert dict_of_ospf_neighbors_1["9.0.0.1"]["State"] == "FULL/PTOP" and dict_of_ospf_neighbors_1["9.0.0.3"][
            "State"] == "FULL/PTOP"
        assert dict_of_ospf_neighbors_2["9.0.0.2"]["State"] == "FULL/PTOP" and dict_of_ospf_neighbors_2["9.0.0.3"][
            "State"] == "FULL/PTOP"
        assert dict_of_ospf_neighbors_4["9.0.0.1"]["State"] == "FULL/PTOP" and dict_of_ospf_neighbors_4["9.0.0.2"][
            "State"] == "FULL/PTOP"

        print("########## Removing the config #############")

        DUT1.ospf.remove_neighbors("9.0.0.1", "9.0.0.3")
        DUT2.ospf.remove_neighbors("9.0.0.2", "9.0.0.3")
        DUT4.ospf.remove_neighbors("9.0.0.1", "9.0.0.2")

        DUT1.ospf.remove_network_type(interface="Gi 0/10")
        DUT2.ospf.remove_network_type(interface="Gi 0/3")
        DUT4.ospf.remove_network_type(interface="Gi 0/11")

        DUT1.ospf.remove_networks(Gi_0_10=["9.0.0.2", "0.0.0.0"])
        DUT2.ospf.remove_networks(int_vlan15=["15.0.0.1", "0.0.0.0"], Gi_0_3=["9.0.0.1", "0.0.0.0"])
        DUT4.ospf.remove_networks(Gi_0_11=["9.0.0.3", "0.0.0.0"])

        DUT1.ospf.disable_ospf()
        DUT2.ospf.disable_ospf()
        DUT4.ospf.disable_ospf()

        DUT2.ip.remove_vlan_interfaces("15")

        DUT2.vl.remove_vlans("15")

        DUT1.int.remove_routed_ports("Gi 0/10")
        DUT2.int.remove_routed_ports("Gi 0/3")
        DUT4.int.remove_routed_ports("Gi 0/11")

        DUT2.int.shut_interfaces("Gi 0/5")
        DUT3.int.shut_interfaces("Gi 0/3", "Gi 0/10", "Gi 0/11")

    def test_func_37(self):

        print("###### Test_func_37 ######")
        print("########## Verify the network type Point-To-Point ( Routed Ports )  #############")
        print("###### 2 DUTs ######")

        #          Topology
        #
        #  DUT1 ---- DUT2 -- VL15

        # Creating routed ports on all DUTs

        DUT1.int.add_routed_ports("Ex 0/1")
        DUT2.int.add_routed_ports("Gi 0/9")

        # No shutting the interfaces

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/9", "Gi 0/5")

        # Creating the VLAN on DUT2

        DUT2.vl.create_vlan(vlan="15")

        # Adding the ports to the VLAN

        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")

        # Create IP Routed Ports on all DUTs except DUT3 which is the "HUB"

        DUT1.ip.add_ip_routed_ports("Ex 0/1", Ex_0_1=["9.0.0.2", "255.255.255.0"])

        DUT2.ip.add_ip_routed_ports("Gi 0/9", Gi_0_9=["9.0.0.1", "255.255.255.0"])
        DUT2.ip.add_ip_interface(int_vlan="15", ip="15.0.0.1", mask="255.255.255.0")
        DUT2.ip.no_shut_int_vlan(int_vlan="15")

        # Enable OSPF on all DUTs and advertise the IPs

        DUT1.ospf.enable_ospf()
        DUT2.ospf.enable_ospf()

        DUT1.ospf.advertise_networks(Ex_0_1=["9.0.0.2", "0.0.0.0"])
        DUT2.ospf.advertise_networks(int_vlan15=["15.0.0.1", "0.0.0.0"], Gi_0_9=["9.0.0.1", "0.0.0.0"])

        # Configure the Routed Ports between the DUTs to be Point-to-Point

        DUT1.ospf.configure_network_type(interface="Ex 0/1", network_type="point-to-point")
        DUT2.ospf.configure_network_type(interface="Gi 0/9", network_type="point-to-point")

        time.sleep(45)

        network_type_1 = DUT1.ospf.show_ip_ospf_interface(interface="Ex 0/1")
        network_type_2 = DUT2.ospf.show_ip_ospf_interface(interface="Gi 0/9")

        print(network_type_1)
        print(network_type_2)

        # Check the network type of the interfaces to be Point-to-point

        assert "PointToPoint" in network_type_1
        assert "PointToPoint" in network_type_2

        ip_route_1, networks_1, networks_connected_1, dict_of_networks_1 = DUT1.ip.show_ip_route()
        ip_route_2, networks_2, networks_connected_2, dict_of_networks_2 = DUT2.ip.show_ip_route()

        print("######## DUT 1 Routing Table ########")
        print(dict_of_networks_1)
        print("######## DUT 2 Routing Table ########")
        print(dict_of_networks_2)

        list_ospf_neighbors_1, dict_of_ospf_neighbors_1 = DUT1.ospf.show_ospf_neighbors()
        list_ospf_neighbors_2, dict_of_ospf_neighbors_2 = DUT2.ospf.show_ospf_neighbors()

        print("######## DUT 1 Neighbor Table ########")
        print(dict_of_ospf_neighbors_1)
        print("######## DUT 2 Neighbor Table ########")
        print(dict_of_ospf_neighbors_2)

        # Check if the routes are learned and installed in OSPF routes

        # DUT 1
        assert "15.0.0.0" in dict_of_networks_1.keys() and dict_of_networks_1["15.0.0.0"]["Protocol"] == "O"

        # Check all neighbors are PTOP

        assert dict_of_ospf_neighbors_1["9.0.0.1"]["State"] == "FULL/PTOP"
        assert dict_of_ospf_neighbors_2["9.0.0.2"]["State"] == "FULL/PTOP"

        print("########## Removing the config #############")

        DUT1.ospf.remove_network_type(interface="Ex 0/1")
        DUT2.ospf.remove_network_type(interface="Gi 0/9")

        DUT1.ospf.remove_networks(Ex_0_1=["9.0.0.2", "0.0.0.0"])
        DUT2.ospf.remove_networks(int_vlan15=["15.0.0.1", "0.0.0.0"], Gi_0_9=["9.0.0.1", "0.0.0.0"])

        DUT1.ospf.disable_ospf()
        DUT2.ospf.disable_ospf()

        DUT2.ip.remove_vlan_interfaces("15")

        DUT2.vl.remove_vlans("15")

        DUT1.int.remove_routed_ports("Ex 0/1")
        DUT2.int.remove_routed_ports("Gi 0/9")

        DUT2.int.shut_interfaces("Gi 0/5")