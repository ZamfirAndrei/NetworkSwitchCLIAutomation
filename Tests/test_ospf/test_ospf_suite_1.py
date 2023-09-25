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

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/4","Gi 0/5", "Gi 0/9")
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

        # Configure the authentication on the int-vlan between the DUTs and configure the key. Check that the adjencency occurs

        DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="simple",authentication_key="1234")
        DUT2.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="simple", authentication_key="1234")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neigbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"
        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2
        assert "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]

        # Change the key for DUT1 and check that there is no adjencency and the routes are not installed

        DUT1.ospf.add_ip_ospf_authentication_key(int_vlan="20", authentication_key="12345")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neigbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert "15.0.0.0" not in dict_of_networks.keys()
        assert ip_session_2 not in dict_of_ospf_neighbors.keys()

        # Change the key for DUT2 and check that there is adjencency and the routes are learned

        DUT2.ospf.add_ip_ospf_authentication_key(int_vlan="20", authentication_key="12345")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neigbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"
        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2
        assert "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]

        # Remove the authentication and authentication-keys on both DUTs and check that there is adjencency and the routes are learned

        DUT1.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20")

        DUT2.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT2.ospf.remove_ip_ospf_authentication_key(int_vlan="20")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neigbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
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

        # Configure the authentication md5 on the int-vlan between the DUTs and configure the key. Check that the adjencency occurs

        DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="md5", authentication_key="1234", message_digest_key="1", message_digest="Yes")
        DUT2.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="md5", authentication_key="1234", message_digest_key="1", message_digest="Yes")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neigbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"
        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2
        assert "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]

        # Change the key for DUT1 and check that there is no adjencency and the routes are not installed

        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")
        DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="md5", authentication_key="12345", message_digest_key="1",message_digest="Yes")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neigbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert "15.0.0.0" not in dict_of_networks.keys()
        assert ip_session_2 in dict_of_ospf_neighbors.keys() and "DOWN" in dict_of_ospf_neighbors[ip_session_2]["State"]

        # Change the key for DUT2 and check that there is adjencency and the routes are learned

        DUT2.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")
        DUT2.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="md5", authentication_key="12345",message_digest_key="1", message_digest="Yes")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neigbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"
        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2
        assert "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]

        # Remove the authentication and authentication-keys on both DUTs and check that there is adjencency and the routes are learned

        DUT1.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")

        DUT2.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT2.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neigbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
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

        # Configure the authentication sha-1 on the int-vlan between the DUTs and configure the key. Check that the adjencency occurs

        DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-1", authentication_key="1234", message_digest_key="1")
        DUT2.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-1", authentication_key="1234", message_digest_key="1")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neigbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"
        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2
        assert "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]

        # Change the key for DUT1 and check that there is no adjencency and the routes are not installed

        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")
        DUT1.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-1", authentication_key="12345", message_digest_key="1")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neigbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert "15.0.0.0" not in dict_of_networks.keys()
        assert ip_session_2 in dict_of_ospf_neighbors.keys() and "DOWN" in dict_of_ospf_neighbors[ip_session_2]["State"]

        # Change the key for DUT2 and check that there is adjencency and the routes are learned

        DUT2.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")
        DUT2.ospf.add_ip_ospf_authentication(int_vlan="20", authentication="sha-1", authentication_key="12345",message_digest_key="1")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neigbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
        print(dict_of_ospf_neighbors)

        assert "15.0.0.0" in dict_of_networks.keys() and dict_of_networks["15.0.0.0"]["Protocol"] == "O"
        assert ip_session_2 in dict_of_ospf_neighbors.keys() and dict_of_ospf_neighbors[ip_session_2]["Neighbor-ID"] == ip_session_2
        assert "FULL" in dict_of_ospf_neighbors[ip_session_2]["State"]

        # Remove the authentication and authentication-keys on both DUTs and check that there is adjencency and the routes are learned

        DUT1.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT1.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")

        DUT2.ospf.remove_ip_ospf_authentication(int_vlan="20")
        DUT2.ospf.remove_ip_ospf_authentication_key(int_vlan="20", message_digest_key="1")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        list_ospf_neigbors, dict_of_ospf_neighbors = DUT1.ospf.show_ospf_neighbors()
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