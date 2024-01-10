import time
import pytest
import pytest_html
import sys

from Management import dut_objects
from config import vlan, interfaces, stp, fdb, ip, rip, ping, ospf
from config.stp import STP

from Management import ssh

ip_session_1 = "10.2.109.206"
ip_session_2 = "10.2.109.83"
ip_session_3 = "10.2.109.98"

DUT1 = dut_objects.DUT_Objects(ip_session=ip_session_1)
DUT2 = dut_objects.DUT_Objects(ip_session=ip_session_2)
DUT3 = dut_objects.DUT_Objects(ip_session=ip_session_3)

# DUT 1 Objects
# class SWconfig:
#     _int = []
#
#     def __init__(self,, ip_session_1):
#         int = interfaces.Interface(ip_session=ip_session_1)
#         vl = vlan.VLAN(ip_session=ip_session_1)
#         stp = STP(ip_session=ip_session_1)
#         fdb = fdb.FDB(ip_session=ip_session_1)
#         ip = ip.IP(ip_session=ip_session_1)
#         rip = rip.RIP(ip_session=ip_session_1)
#         ping = ping.PING(ip_session=ip_session_1)
#         ospf = ospf.OSPF(ip_session=ip_session_1)
#
#     def SWconfig(self, ip_session_1):
#         int = interfaces.Interface(ip_session=ip_session_1)
#         vl = vlan.VLAN(ip_session=ip_session_1)
#         stp = stp.STP(ip_session=ip_session_1)
#         fdb = fdb.FDB(ip_session=ip_session_1)
#         ip = ip.IP(ip_session=ip_session_1)
#         rip = rip.RIP(ip_session=ip_session_1)
#         ping = ping.PING(ip_session=ip_session_1)
#         ospf = ospf.OSPF(ip_session=ip_session_1)

    # def int(interface):
    #     try:
    #         return _int[interface]
    #     except ex:
    #         # return None
#
#
# dut_1 = SWconfig(ip_session_1)

# # DUT 1 Objects
#
# DUT1.int = interfaces.Interface(ip_session=ip_session_1)
# DUT1.vl = vlan.VLAN(ip_session=ip_session_1)
# DUT1.stp = stp.STP(ip_session=ip_session_1)
# DUT1.fdb = fdb.FDB(ip_session=ip_session_1)
# DUT1.ip = ip.IP(ip_session=ip_session_1)
# DUT1.rip = rip.RIP(ip_session=ip_session_1)
# DUT1.ping = ping.PING(ip_session=ip_session_1)
# DUT1.ospf = ospf.OSPF(ip_session=ip_session_1)
#
# # DUT 2 Objects
#
# DUT2.int = interfaces.Interface(ip_session=ip_session_2)
# DUT2.vl = vlan.VLAN(ip_session=ip_session_2)
# DUT2.stp = stp.STP(ip_session=ip_session_2)
# DUT2.fdb = fdb.FDB(ip_session=ip_session_2)
# DUT2.ip = ip.IP(ip_session=ip_session_2)
# DUT2.rip = rip.RIP(ip_session=ip_session_2)
# DUT2.ping = ping.PING(ip_session=ip_session_2)
# DUT2.ospf = ospf.OSPF(ip_session=ip_session_2)
#
# # DUT 3 Objects
#
# DUT3.int = interfaces.Interface(ip_session=ip_session_3)
# DUT3.vl = vlan.VLAN(ip_session=ip_session_3)
# DUT3.stp = stp.STP(ip_session=ip_session_3)
# DUT3.fdb = fdb.FDB(ip_session=ip_session_3)
# DUT3.ip = ip.IP(ip_session=ip_session_3)
# DUT3.rip = rip.RIP(ip_session=ip_session_3)
# DUT3.ping = ping.PING(ip_session=ip_session_3)
# DUT3.ospf = ospf.OSPF(ip_session=ip_session_3)


class TestRIPSuite1:

    def test_func_1(self):

        print("###### Test_func_1 ######")
        print( "########## Check if we can advertise networks into RIP and it establish connection using int vlans #############")
        print("###### 2 DUTs ######")

        DUT1.int.no_shut_interfaces("Gi 0/3", "Gi 0/4", "Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/5", "Gi 0/6", "Gi 0/9")

        # Creating the VLAN on all DUTs

        DUT1.vl.create_vlan(vlan="30")
        DUT1.vl.create_vlan(vlan="14")

        DUT2.vl.create_vlan(vlan="15")
        DUT2.vl.create_vlan(vlan="14")

        # Adding the ports to the VLAN

        DUT1.vl.add_ports_to_vlan(ports="Gi 0/3", vlan="30")
        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="14")

        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="14")

        # Create IP interfaces on all DUTs for the specific VLANs

        DUT1.ip.add_ip_interfaces("14", "30", int_vlan14=["14.0.0.2", "255.255.255.0"],
                              int_vlan30=["30.0.0.1", "255.255.255.0"])
        DUT1.ip.no_shut_int_vlans("14", "30")

        DUT2.ip.add_ip_interfaces("14", "15", int_vlan14=["14.0.0.1", "255.255.255.0"],
                              int_vlan15=["15.0.0.1", "255.255.255.0"])
        DUT2.ip.no_shut_int_vlans("14", "15")

        # Enable rip on all DUTs and advertise the IPs

        DUT1.rip.enable_rip()
        DUT1.rip.advertise_networks("14.0.0.2", "30.0.0.1")

        DUT2.rip.enable_rip()
        DUT2.rip.advertise_networks("14.0.0.1", "15.0.0.1")

        time.sleep(30)

        dict_rip_routes_1 = DUT1.rip.show_ip_route_rip()
        dict_rip_routes_2 = DUT2.rip.show_ip_route_rip()

        print(dict_rip_routes_1)
        print(dict_rip_routes_2)
        # print(dict_rip_routes_1["15.0.0.0"]["Learned From"])

        # Check if the routes are learned and instaled in RIP routes

        assert "15.0.0.0" in dict_rip_routes_1.keys()
        assert "30.0.0.0" in dict_rip_routes_2.keys()

        print("########## Removing the config #############")

        DUT1.rip.disable_rip()
        DUT2.rip.disable_rip()

        DUT1.ip.remove_vlan_interfaces("14", "30")
        DUT2.ip.remove_vlan_interfaces("14", "15")

        DUT1.vl.remove_vlans("14", "30")
        DUT2.vl.remove_vlans("14", "15")

        DUT1.int.shut_interfaces("Gi 0/3", "Gi 0/4", "Ex 0/1", "Gi 0/9")
        DUT2.int.shut_interfaces("Gi 0/4", "Gi 0/5", "Gi 0/6", "Gi 0/9")

    def test_func_2(self):

        print("###### Test_func_2 ######")
        print("########## Verify a DUT sends a default route if the default-information originate is configured on a RIP enabled interface.#############")
        print("###### 2 DUTs ######")

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/9", "Gi 0/5")

        # Creating VLANs

        DUT1.vl.create_vlan(vlan="20")
        DUT2.vl.create_vlan(vlan="20")
        DUT2.vl.create_vlan(vlan="15")

        # Adding the ports to the VLANs

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")

        # Adding IPs on the interfaces

        DUT1.ip.add_ip_interface(int_vlan="20", ip="20.0.0.2", mask="255.255.255.0")
        DUT2.ip.add_ip_interface(int_vlan="20", ip="20.0.0.1", mask="255.255.255.0")
        DUT2.ip.add_ip_interface(int_vlan="15", ip="15.0.0.1", mask="255.255.255.0")

        DUT1.ip.no_shut_int_vlans("20")
        DUT2.ip.no_shut_int_vlans("20", "15")

        # Enabling RIP and advertising the interfaces in RIP

        DUT1.rip.enable_rip()
        DUT2.rip.enable_rip()

        DUT1.rip.advertise_network(ip_network="20.0.0.2")
        DUT2.rip.advertise_networks("20.0.0.1", "15.0.0.1")

        # Advertising the default route on DUT2 and installing the route on DUT1

        DUT2.rip.add_default_information_originate(int_vlan="20")
        DUT1.rip.add_ip_default_route_install(int_vlan="20")

        # Checking if the route is installed

        time.sleep(30)

        dict_rip_routes_1 = DUT1.rip.show_ip_route_rip()
        print(dict_rip_routes_1)

        assert "0.0.0.0" in dict_rip_routes_1.keys()

        # Remove the route install and check if the default route is not in the routing table

        DUT1.rip.remove_ip_default_route_install(int_vlan="20")

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(30)

        dict_rip_routes_1 = DUT1.rip.show_ip_route_rip()
        print(dict_rip_routes_1)

        assert "0.0.0.0" not in dict_rip_routes_1.keys()

        print("########## Removing the config #############")

        DUT2.rip.remove_default_information_originate(int_vlan="20")

        DUT1.rip.disable_rip()
        DUT2.rip.disable_rip()

        DUT1.ip.remove_int_vlan(int_vlan="20")
        DUT2.ip.remove_vlan_interfaces("20", "15")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5")

        DUT1.vl.remove_vlan(vlan="20")
        DUT2.vl.remove_vlans("20", "15")

    def test_func_3(self):

        print("###### Test_func_3 ######")
        print("########## Verify functionality for redistribute connected #############")
        print("###### 2 DUTs ######")

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/9", "Gi 0/5", "Gi 0/6")

        # Creating VLANs

        DUT1.vl.create_vlan(vlan="20")
        DUT2.vl.create_vlans("15", "20", "16", "100")

        # Adding the ports to the VLANs

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/6", vlan="16")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="100")

        # Adding IPs on the interfaces

        DUT1.ip.add_ip_interface(int_vlan="20", ip="20.0.0.2", mask="255.255.255.0")
        DUT2.ip.add_ip_interfaces("16", "15", "20", "100", int_vlan16=["16.0.0.1", "255.255.255.0"],
                              int_vlan15=["15.0.0.1", "255.255.255.0"], int_vlan20=["20.0.0.1", "255.255.255.0"],
                              int_vlan100=["100.0.0.1", "255.255.255.0"])

        DUT1.ip.no_shut_int_vlans("20")
        DUT2.ip.no_shut_int_vlans("20", "15", "16", "100")

        # Enabling RIP and advertising the interfaces in RIP

        DUT1.rip.enable_rip()
        DUT2.rip.enable_rip()

        DUT1.rip.advertise_network(ip_network="20.0.0.2")
        DUT2.rip.advertise_networks("20.0.0.1", "100.0.0.1")

        # Redistributing the connected networks on DUT2 and installing them on DUT1

        DUT2.rip.redistribute_connected()

        # Checking if the routes are installed

        time.sleep(30)

        dict_rip_routes_1 = DUT1.rip.show_ip_route_rip()
        print(dict_rip_routes_1)

        assert "15.0.0.0" in dict_rip_routes_1.keys()
        assert "16.0.0.0" in dict_rip_routes_1.keys()
        assert "100.0.0.0" in dict_rip_routes_1.keys()

        # Remove redistribution on DUT2 and check if the connected routes are not anymore in the routing table of DUT1

        DUT2.rip.remove_redistribute_connected()

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(30)

        dict_rip_routes_1 = DUT1.rip.show_ip_route_rip()
        print(dict_rip_routes_1)

        assert "15.0.0.0" not in dict_rip_routes_1.keys()
        assert "16.0.0.0" not in dict_rip_routes_1.keys()
        assert "100.0.0.0" in dict_rip_routes_1.keys()

        print("########## Removing the config #############")

        DUT1.rip.disable_rip()
        DUT2.rip.disable_rip()

        DUT1.ip.remove_int_vlan(int_vlan="20")
        DUT2.ip.remove_vlan_interfaces("20", "15", "16", "100")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5", "Gi 0/6")

        DUT1.vl.remove_vlan(vlan="20")
        DUT2.vl.remove_vlans("20", "15", "16", "100")

    def test_func_4(self):

        print("###### Test_func_4 ######")
        print("########## Verify functionality for redistribute static #############")
        print("###### 2 DUTs ######")

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/9", "Gi 0/5")

        # Creating VLANs

        DUT1.vl.create_vlan(vlan="20")
        DUT2.vl.create_vlans("15", "20")

        # Adding the ports to the VLANs

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")

        # Adding IPs on the interfaces

        DUT1.ip.add_ip_interface(int_vlan="20", ip="20.0.0.2", mask="255.255.255.0")
        DUT2.ip.add_ip_interfaces("15", "20", int_vlan15=["15.0.0.1", "255.255.255.0"],
                              int_vlan20=["20.0.0.1", "255.255.255.0"])

        DUT1.ip.no_shut_int_vlans("20")
        DUT2.ip.no_shut_int_vlans("20", "15")

        # Enabling RIP and advertising the interfaces in RIP

        DUT1.rip.enable_rip()
        DUT2.rip.enable_rip()

        DUT1.rip.advertise_network(ip_network="20.0.0.2")
        DUT2.rip.advertise_networks("20.0.0.1", "15.0.0.1")

        # Creating a static route

        DUT2.ip.add_static_route(network_dest="100.0.0.0", mask_dest="255.255.0.0", next_hop="15.0.0.100")

        # Redistributing the static network on DUT2 and installing it on DUT1

        DUT2.rip.redistribute_static()

        # Checking if the routes are installed

        time.sleep(30)

        dict_rip_routes_1 = DUT1.rip.show_ip_route_rip()
        print(dict_rip_routes_1)

        assert "15.0.0.0" in dict_rip_routes_1.keys()
        assert "100.0.0.0" in dict_rip_routes_1.keys()

        # Remove the static route on DUT2 and check if the route is not anymore in the routing table of DUT1

        DUT2.rip.remove_redistribute_static()

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(30)

        dict_rip_routes_1 = DUT1.rip.show_ip_route_rip()
        print(dict_rip_routes_1)

        assert "15.0.0.0" in dict_rip_routes_1.keys()
        assert "100.0.0.0" not in dict_rip_routes_1.keys()

        print("########## Removing the config #############")

        DUT1.rip.disable_rip()
        DUT2.rip.disable_rip()

        DUT2.ip.remove_static_route(network_dest="100.0.0.0", mask_dest="255.255.0.0", next_hop="15.0.0.100")

        DUT1.ip.remove_int_vlan(int_vlan="20")
        DUT2.ip.remove_vlan_interfaces("20", "15")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5")

        DUT1.vl.remove_vlan(vlan="20")
        DUT2.vl.remove_vlans("20", "15")

    def test_func_5(self):

        print("###### Test_func_5 ######")
        print("########## Verify auto-summary #############")
        print("###### 2 DUTs ######")

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/9", "Gi 0/5")

        # Creating VLANs

        DUT1.vl.create_vlan(vlan="20")
        DUT2.vl.create_vlans("15", "20")

        # Adding the ports to the VLANs

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")

        # Adding IPs on the interfaces

        DUT1.ip.add_ip_interface(int_vlan="20", ip="20.0.0.2", mask="255.255.255.0")
        DUT2.ip.add_ip_interfaces("15", "20", int_vlan15=["15.0.0.1", "255.255.255.0"],
                              int_vlan20=["20.0.0.1", "255.255.255.0"])

        DUT1.ip.no_shut_int_vlans("20")
        DUT2.ip.no_shut_int_vlans("20", "15")

        # Enabling RIP and advertising the interfaces into RIP

        DUT1.rip.enable_rip()
        DUT2.rip.enable_rip()

        DUT1.rip.advertise_network(ip_network="20.0.0.2")
        DUT2.rip.advertise_networks("20.0.0.1", "15.0.0.1")

        # Creating a static route

        DUT2.ip.add_static_route(network_dest="88.88.88.0", mask_dest="255.255.255.128", next_hop="15.0.0.100")

        # Disabling no-auto summary on DUT2, so it will redistribute classless subnets

        DUT2.rip.remove_auto_summary()

        # Redistributing the static network on DUT2 and installing it on DUT1

        DUT2.rip.redistribute_static()

        # Checking if the routes are installed and that are classless

        time.sleep(30)

        dict_rip_routes_1 = DUT1.rip.show_ip_route_rip()
        # print(dict_rip_routes_1)

        assert "88.88.88.0" in dict_rip_routes_1.keys() and dict_rip_routes_1["88.88.88.0"]["Mask"] == "25"

        # Enable the auto-summary on DUT2 and check if the route is classfull and is present in the routing table of DUT1

        DUT2.rip.auto_summary()

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(45)

        dict_rip_routes_1 = DUT1.rip.show_ip_route_rip()
        # print(dict_rip_routes_1)

        assert "88.88.88.0" not in dict_rip_routes_1.keys()
        assert "88.0.0.0" in dict_rip_routes_1.keys()

        print("########## Removing the config #############")

        DUT1.rip.disable_rip()
        DUT2.rip.disable_rip()

        DUT2.ip.remove_static_route(network_dest="88.88.88.0", mask_dest="255.255.255.128", next_hop="15.0.0.100")

        DUT1.ip.remove_int_vlan(int_vlan="20")
        DUT2.ip.remove_vlan_interfaces("20", "15")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5")

        DUT1.vl.remove_vlan(vlan="20")
        DUT2.vl.remove_vlans("20", "15")

    def test_func_6(self):

        print("###### Test_func_6 ######")
        print("########## Verify that administrative RIP distance can be changed to other value #############")
        print("###### 2 DUTs ######")

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/9", "Gi 0/5")

        # Creating VLANs

        DUT1.vl.create_vlan(vlan="20")
        DUT2.vl.create_vlans("15", "20")

        # Adding the ports to the VLANs

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")

        # Adding IPs on the interfaces

        DUT1.ip.add_ip_interface(int_vlan="20", ip="20.0.0.2", mask="255.255.255.0")
        DUT2.ip.add_ip_interfaces("15", "20", int_vlan15=["15.0.0.1", "255.255.255.0"],
                              int_vlan20=["20.0.0.1", "255.255.255.0"])

        DUT1.ip.no_shut_int_vlans("20")
        DUT2.ip.no_shut_int_vlans("20", "15")

        # Enabling RIP and advertising the interfaces into RIP

        DUT1.rip.enable_rip()
        DUT2.rip.enable_rip()

        DUT1.rip.advertise_network(ip_network="20.0.0.2")
        DUT2.rip.advertise_networks("20.0.0.1", "15.0.0.1")

        # Enabling OSPF and advertising the interfaces into OSPF

        DUT1.ospf.enable_ospf()
        DUT2.ospf.enable_ospf()

        DUT1.ospf.advertise_network(ip_network="20.0.0.2", area="0.0.0.0")
        DUT2.ospf.advertise_network(ip_network="15.0.0.1", area="0.0.0.0")
        DUT2.ospf.advertise_network(ip_network="20.0.0.1", area="0.0.0.0")

        # Disabling no-autosummary on DUT2 so it will redistribute classless subnets

        DUT2.rip.remove_auto_summary()

        # Configuring the Distance on DUT1 so to routes are learned using RIP

        DUT1.rip.add_distance(distance="99")

        # Checking if the routes are installed and that are learned via RIP

        time.sleep(30)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        assert "15.0.0.0" in dict_of_networks and dict_of_networks["15.0.0.0"]["Protocol"] == "R"

        # Remove the distance and check that the routes are learned via OSPF

        DUT1.rip.remove_distance()

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        assert "15.0.0.0" in dict_of_networks and dict_of_networks["15.0.0.0"]["Protocol"] == "O"

        print("########## Removing the config #############")

        DUT1.rip.disable_rip()
        DUT2.rip.disable_rip()

        DUT1.ospf.remove_network(ip_network="20.0.0.2", area="0.0.0.0")
        DUT2.ospf.remove_network(ip_network="15.0.0.1", area="0.0.0.0")
        DUT2.ospf.remove_network(ip_network="20.0.0.1", area="0.0.0.0")

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
        print("########## Verify functionality for passive-interface #############")
        print("###### 2 DUTs ######")

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/9", "Gi 0/5")

        # Creating VLANs

        DUT1.vl.create_vlan(vlan="20")
        DUT2.vl.create_vlans("15", "20")

        # Adding the ports to the VLANs

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")

        # Adding IPs on the interfaces

        DUT1.ip.add_ip_interface(int_vlan="20", ip="20.0.0.2", mask="255.255.255.0")
        DUT2.ip.add_ip_interfaces("15", "20", int_vlan15=["15.0.0.1", "255.255.255.0"],
                              int_vlan20=["20.0.0.1", "255.255.255.0"])

        DUT1.ip.no_shut_int_vlans("20")
        DUT2.ip.no_shut_int_vlans("20", "15")

        # Enabling RIP and advertising the interfaces into RIP

        DUT1.rip.enable_rip()
        DUT2.rip.enable_rip()

        DUT1.rip.advertise_network(ip_network="20.0.0.2")
        DUT2.rip.advertise_networks("20.0.0.1", "15.0.0.1")

        # Enable passive interface on the int VLAN between the DUTs and shut/no shut the int VLAN between them

        DUT2.rip.add_passive_interface(vlan="20")

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        # Checking if the routes are not installed on DUT1 and that are classless

        time.sleep(45)

        dict_rip_routes_1 = DUT1.rip.show_ip_route_rip()
        print(dict_rip_routes_1)

        assert "15.0.0.0" not in dict_rip_routes_1.keys()

        # Disable the passive interface and check that the routes are installed on DUT1

        DUT2.rip.remove_passive_interface(vlan="20")

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(45)

        dict_rip_routes_1 = DUT1.rip.show_ip_route_rip()
        print(dict_rip_routes_1)

        assert "15.0.0.0" in dict_rip_routes_1.keys()

        print("########## Removing the config #############")

        DUT1.rip.disable_rip()
        DUT2.rip.disable_rip()

        DUT1.ip.remove_int_vlan(int_vlan="20")
        DUT2.ip.remove_vlan_interfaces("20", "15")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5")

        DUT1.vl.remove_vlan(vlan="20")
        DUT2.vl.remove_vlans("20", "15")

    def test_func_8(self):

        print("###### Test_func_8 ######")
        print("########## Verify functionality for default-metric #############")
        print("###### 2 DUTs ######")

        default_metric = 3
        metric = 5
        metric_high = 16

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/9", "Gi 0/5")

        # Creating VLANs

        DUT1.vl.create_vlan(vlan="20")
        DUT2.vl.create_vlans("15", "20")

        # Adding the ports to the VLANs

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")

        # Adding IPs on the interfaces

        DUT1.ip.add_ip_interface(int_vlan="20", ip="20.0.0.2", mask="255.255.255.0")
        DUT2.ip.add_ip_interfaces("15", "20", int_vlan15=["15.0.0.1", "255.255.255.0"],
                              int_vlan20=["20.0.0.1", "255.255.255.0"])

        DUT1.ip.no_shut_int_vlans("20")
        DUT2.ip.no_shut_int_vlans("20", "15")

        # Enabling RIP and advertising the interfaces into RIP

        DUT1.rip.enable_rip()
        DUT2.rip.enable_rip()

        DUT1.rip.advertise_network(ip_network="20.0.0.2")
        DUT2.rip.advertise_networks("20.0.0.1")

        # Changing the metric for redistributed routes

        DUT2.rip.default_metric(metric=metric)

        # Configuring static routes, redistribute static and redistribute connected on DUT2 towards DUT1

        DUT2.ip.add_static_route(network_dest="88.0.0.0", mask_dest="255.255.255.0", next_hop="15.0.0.100")

        DUT2.rip.redistribute_static()
        DUT2.rip.redistribute_connected()

        # Checking if the routes are installed and that are learned via RIP

        time.sleep(30)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        assert "15.0.0.0" in dict_of_networks and dict_of_networks["15.0.0.0"]["Metric"] == str(metric + 1)
        assert "88.0.0.0" in dict_of_networks and dict_of_networks["88.0.0.0"]["Metric"] == str(metric + 1)

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

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        # Checking that the routes are not installed because they have a metric higher than 15

        assert "15.0.0.0" not in dict_of_networks
        assert "88.0.0.0" not in dict_of_networks

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

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        assert "15.0.0.0" in dict_of_networks and dict_of_networks["15.0.0.0"]["Metric"] == str(default_metric + 1)
        assert "88.0.0.0" in dict_of_networks and dict_of_networks["88.0.0.0"]["Metric"] == str(default_metric + 1)

        print("########## Removing the config #############")

        DUT1.rip.disable_rip()
        DUT2.rip.disable_rip()

        DUT1.ip.remove_int_vlan(int_vlan="20")
        DUT2.ip.remove_vlan_interfaces("20", "15")

        DUT2.ip.remove_static_route(network_dest="88.0.0.0", mask_dest="255.255.255.0", next_hop="15.0.0.100")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5")

        DUT1.vl.remove_vlan(vlan="20")
        DUT2.vl.remove_vlans("20", "15")

    def test_func_9(self):

        print("###### Test_func_9 ######")
        print("########## Verify that the text mode authentication option works as expected. #############")
        print("###### 2 DUTs ######")

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/9", "Gi 0/5")

        # Creating VLANs

        DUT1.vl.create_vlan(vlan="20")
        DUT2.vl.create_vlans("15", "20")

        # Adding the ports to the VLANs

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")

        # Adding IPs on the interfaces

        DUT1.ip.add_ip_interface(int_vlan="20", ip="20.0.0.2", mask="255.255.255.0")
        DUT2.ip.add_ip_interfaces("15", "20", int_vlan15=["15.0.0.1", "255.255.255.0"],
                              int_vlan20=["20.0.0.1", "255.255.255.0"])

        DUT1.ip.no_shut_int_vlans("20")
        DUT2.ip.no_shut_int_vlans("20", "15")

        # Enabling RIP and advertising the interfaces into RIP

        DUT1.rip.enable_rip()
        DUT2.rip.enable_rip()

        DUT1.rip.advertise_network(ip_network="20.0.0.2")
        DUT2.rip.advertise_networks("20.0.0.1", "15.0.0.1")

        # Enable authentication key on the int VLAN between the DUTs on DUT2 and shut/no shut the int VLAN between them

        DUT2.rip.add_ip_rip_authentication_mode(int_vlan="20", mode="text", key_chain="12345")

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        # Checking if the routes are not installed

        time.sleep(45)

        dict_rip_routes_1 = DUT1.rip.show_ip_route_rip()
        print(dict_rip_routes_1)
        dict_of_int_vlans_authentication_2 = DUT2.rip.show_ip_rip_authentication()
        dict_of_int_vlans_authentication_1 = DUT1.rip.show_ip_rip_authentication()
        print(dict_of_int_vlans_authentication_2)
        print(dict_of_int_vlans_authentication_1)

        assert "15.0.0.0" not in dict_rip_routes_1.keys()
        assert "20" in dict_of_int_vlans_authentication_2 and dict_of_int_vlans_authentication_2["20"]["Authentication Type"] == "simple text"
        assert "20" in dict_of_int_vlans_authentication_1 and dict_of_int_vlans_authentication_1["20"]["Authentication Type"] == "none"

        # Enable the same authentication key on DUT1 and check that routes are installed

        DUT1.rip.add_ip_rip_authentication_mode(int_vlan="20", mode="text", key_chain="12345")

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(30)

        dict_rip_routes_1 = DUT1.rip.show_ip_route_rip()
        print(dict_rip_routes_1)
        dict_of_int_vlans_authentication_2 = DUT2.rip.show_ip_rip_authentication()
        dict_of_int_vlans_authentication_1 = DUT1.rip.show_ip_rip_authentication()
        print(dict_of_int_vlans_authentication_2)
        print(dict_of_int_vlans_authentication_1)

        assert "15.0.0.0" in dict_rip_routes_1.keys()
        assert "20" in dict_of_int_vlans_authentication_2 and dict_of_int_vlans_authentication_2["20"]["Authentication Type"] == "simple text"
        assert "20" in dict_of_int_vlans_authentication_1 and dict_of_int_vlans_authentication_1["20"]["Authentication Type"] == "simple text"

        # Disable the authentication and check that the routes are installed on DUT1

        DUT1.rip.remove_ip_rip_authentication_mode(int_vlan="20")
        DUT2.rip.remove_ip_rip_authentication_mode(int_vlan="20")

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(35)

        dict_rip_routes_1 = DUT1.rip.show_ip_route_rip()
        # print(dict_rip_routes_1)
        dict_of_int_vlans_authentication_2 = DUT2.rip.show_ip_rip_authentication()
        dict_of_int_vlans_authentication_1 = DUT1.rip.show_ip_rip_authentication()
        print(dict_of_int_vlans_authentication_2)
        print(dict_of_int_vlans_authentication_1)

        assert "15.0.0.0" in dict_rip_routes_1.keys()
        assert "20" in dict_of_int_vlans_authentication_2 and dict_of_int_vlans_authentication_2["20"]["Authentication Type"] == "none"
        assert "20" in dict_of_int_vlans_authentication_1 and dict_of_int_vlans_authentication_1["20"]["Authentication Type"] == "none"

        print("########## Removing the config #############")

        DUT1.rip.disable_rip()
        DUT2.rip.disable_rip()

        DUT1.ip.remove_int_vlan(int_vlan="20")
        DUT2.ip.remove_vlan_interfaces("20", "15")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5")

        DUT1.vl.remove_vlan(vlan="20")
        DUT2.vl.remove_vlans("20", "15")

    def test_func_10(self):

        print("###### Test_func_10 ######")
        print("########## Verify that md5 Authentication with the authentication type for crypto authentication md5 | sha-1 | sha-256 works as expected.#############")
        print("###### 2 DUTs ######")

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/9", "Gi 0/5")

        # Creating VLANs

        DUT1.vl.create_vlan(vlan="20")
        DUT2.vl.create_vlans("15", "20")

        # Adding the ports to the VLANs

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")

        # Adding IPs on the interfaces

        DUT1.ip.add_ip_interface(int_vlan="20", ip="20.0.0.2", mask="255.255.255.0")
        DUT2.ip.add_ip_interfaces("15", "20", int_vlan15=["15.0.0.1", "255.255.255.0"],
                              int_vlan20=["20.0.0.1", "255.255.255.0"])

        DUT1.ip.no_shut_int_vlans("20")
        DUT2.ip.no_shut_int_vlans("20", "15")

        # Enabling RIP and advertising the interfaces into RIP

        DUT1.rip.enable_rip()
        DUT2.rip.enable_rip()

        DUT1.rip.advertise_network(ip_network="20.0.0.2")
        DUT2.rip.advertise_networks("20.0.0.1", "15.0.0.1")

        # Enable authentication key on the int VLAN between the DUTs on DUT2 and shut/no shut the int VLAN between them

        DUT2.rip.add_ip_rip_authentication_mode(int_vlan="20", mode="md5", key_chain="12345")
        DUT2.rip.add_ip_rip_auth_type_mode(int_vlan="20", mode="md5", key_id="1", key="12345")

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        # Checking if the routes are not installed

        time.sleep(45)

        dict_rip_routes_1 = DUT1.rip.show_ip_route_rip()
        print(dict_rip_routes_1)
        dict_of_int_vlans_authentication_2 = DUT2.rip.show_ip_rip_authentication()
        dict_of_int_vlans_authentication_1 = DUT1.rip.show_ip_rip_authentication()
        print(dict_of_int_vlans_authentication_2)
        print(dict_of_int_vlans_authentication_1)

        assert "15.0.0.0" not in dict_rip_routes_1.keys()
        assert "20" in dict_of_int_vlans_authentication_2 and dict_of_int_vlans_authentication_2["20"]["Authentication Type"] == "md5"
        assert "20" in dict_of_int_vlans_authentication_1 and dict_of_int_vlans_authentication_1["20"]["Authentication Type"] == "none"

        # Enable the same authentication key on DUT1 and check that routes are installed

        DUT1.rip.add_ip_rip_authentication_mode(int_vlan="20", mode="md5", key_chain="12345")
        DUT1.rip.add_ip_rip_auth_type_mode(int_vlan="20", mode="md5", key_id="1", key="12345")

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(30)

        dict_rip_routes_1 = DUT1.rip.show_ip_route_rip()
        print(dict_rip_routes_1)
        dict_of_int_vlans_authentication_2 = DUT2.rip.show_ip_rip_authentication()
        dict_of_int_vlans_authentication_1 = DUT1.rip.show_ip_rip_authentication()
        print(dict_of_int_vlans_authentication_2)
        print(dict_of_int_vlans_authentication_1)

        assert "15.0.0.0" in dict_rip_routes_1.keys()
        assert "20" in dict_of_int_vlans_authentication_2 and dict_of_int_vlans_authentication_2["20"]["Authentication Type"] == "md5"
        assert "20" in dict_of_int_vlans_authentication_1 and dict_of_int_vlans_authentication_1["20"]["Authentication Type"] == "md5"
        assert dict_of_int_vlans_authentication_2["20"]['Authentication KeyId in use'] == dict_of_int_vlans_authentication_1["20"]['Authentication KeyId in use'] == "1"

        # Disable the authentication and check that the routes are installed on DUT1

        DUT1.rip.remove_ip_rip_authentication_mode(int_vlan="20")
        DUT2.rip.remove_ip_rip_authentication_mode(int_vlan="20")

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(35)

        dict_rip_routes_1 = DUT1.rip.show_ip_route_rip()
        print(dict_rip_routes_1)
        dict_of_int_vlans_authentication_2 = DUT2.rip.show_ip_rip_authentication()
        dict_of_int_vlans_authentication_1 = DUT1.rip.show_ip_rip_authentication()
        print(dict_of_int_vlans_authentication_2)
        print(dict_of_int_vlans_authentication_1)

        assert "15.0.0.0" in dict_rip_routes_1.keys()
        assert "20" in dict_of_int_vlans_authentication_2 and dict_of_int_vlans_authentication_2["20"]["Authentication Type"] == "none"
        assert "20" in dict_of_int_vlans_authentication_1 and dict_of_int_vlans_authentication_1["20"]["Authentication Type"] == "none"

        print("########## Removing the config #############")

        DUT1.rip.disable_rip()
        DUT2.rip.disable_rip()

        DUT1.ip.remove_int_vlan(int_vlan="20")
        DUT2.ip.remove_vlan_interfaces("20", "15")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5")

        DUT1.vl.remove_vlan(vlan="20")
        DUT2.vl.remove_vlans("20", "15")

    def test_func_11(self):

        print("###### Test_func_11 ######")
        print("########## Verify that sha-1 Authentication with the authentication type for crypto authentication sha-1 works as expected.#############")
        print("###### 2 DUTs ######")

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/9", "Gi 0/5")

        # Creating VLANs

        DUT1.vl.create_vlan(vlan="20")
        DUT2.vl.create_vlans("15", "20")

        # Adding the ports to the VLANs

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")

        # Adding IPs on the interfaces

        DUT1.ip.add_ip_interface(int_vlan="20", ip="20.0.0.2", mask="255.255.255.0")
        DUT2.ip.add_ip_interfaces("15", "20", int_vlan15=["15.0.0.1", "255.255.255.0"],
                              int_vlan20=["20.0.0.1", "255.255.255.0"])

        DUT1.ip.no_shut_int_vlans("20")
        DUT2.ip.no_shut_int_vlans("20", "15")

        # Enabling RIP and advertising the interfaces into RIP

        DUT1.rip.enable_rip()
        DUT2.rip.enable_rip()

        DUT1.rip.advertise_network(ip_network="20.0.0.2")
        DUT2.rip.advertise_networks("20.0.0.1", "15.0.0.1")

        # Enable authentication key on the int VLAN between the DUTs on DUT2 and shut/no shut the int VLAN between them

        DUT2.rip.add_ip_rip_auth_type_mode(int_vlan="20", mode="sha-1", key_id="1", key="12345")

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        # Checking if the routes are not installed

        time.sleep(45)

        dict_rip_routes_1 = DUT1.rip.show_ip_route_rip()
        print(dict_rip_routes_1)
        dict_of_int_vlans_authentication_2 = DUT2.rip.show_ip_rip_authentication()
        dict_of_int_vlans_authentication_1 = DUT1.rip.show_ip_rip_authentication()
        print(dict_of_int_vlans_authentication_2)
        print(dict_of_int_vlans_authentication_1)

        assert "15.0.0.0" not in dict_rip_routes_1.keys()
        assert "20" in dict_of_int_vlans_authentication_2 and dict_of_int_vlans_authentication_2["20"]["Authentication Type"] == "sha1"
        assert "20" in dict_of_int_vlans_authentication_1 and dict_of_int_vlans_authentication_1["20"]["Authentication Type"] == "none"

        # Enable the same authentication key on DUT1 and check that routes are installed

        DUT1.rip.add_ip_rip_auth_type_mode(int_vlan="20", mode="sha-1", key_id="1", key="12345")

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(30)

        dict_rip_routes_1 = DUT1.rip.show_ip_route_rip()
        print(dict_rip_routes_1)
        dict_of_int_vlans_authentication_2 = DUT2.rip.show_ip_rip_authentication()
        dict_of_int_vlans_authentication_1 = DUT1.rip.show_ip_rip_authentication()
        print(dict_of_int_vlans_authentication_2)
        print(dict_of_int_vlans_authentication_1)

        assert "15.0.0.0" in dict_rip_routes_1.keys()
        assert "20" in dict_of_int_vlans_authentication_2 and dict_of_int_vlans_authentication_2["20"]["Authentication Type"] == "sha1"
        assert "20" in dict_of_int_vlans_authentication_1 and dict_of_int_vlans_authentication_1["20"]["Authentication Type"] == "sha1"
        assert dict_of_int_vlans_authentication_2["20"]['Authentication KeyId in use'] == dict_of_int_vlans_authentication_1["20"]['Authentication KeyId in use'] == "1"

        # Disable the authentication and check that the routes are installed on DUT1

        DUT1.rip.remove_ip_rip_authentication_mode(int_vlan="20")
        DUT2.rip.remove_ip_rip_authentication_mode(int_vlan="20")

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(35)

        dict_rip_routes_1 = DUT1.rip.show_ip_route_rip()
        print(dict_rip_routes_1)
        dict_of_int_vlans_authentication_2 = DUT2.rip.show_ip_rip_authentication()
        dict_of_int_vlans_authentication_1 = DUT1.rip.show_ip_rip_authentication()
        print(dict_of_int_vlans_authentication_2)
        print(dict_of_int_vlans_authentication_1)

        assert "15.0.0.0" in dict_rip_routes_1.keys()
        assert "20" in dict_of_int_vlans_authentication_2 and dict_of_int_vlans_authentication_2["20"]["Authentication Type"] == "none"
        assert "20" in dict_of_int_vlans_authentication_1 and dict_of_int_vlans_authentication_1["20"]["Authentication Type"] == "none"

        print("########## Removing the config #############")

        DUT1.rip.disable_rip()
        DUT2.rip.disable_rip()

        DUT1.ip.remove_int_vlan(int_vlan="20")
        DUT2.ip.remove_vlan_interfaces("20", "15")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5")

        DUT1.vl.remove_vlan(vlan="20")
        DUT2.vl.remove_vlans("20", "15")

    def test_func_12(self):

        print("###### Test_func_12 ######")
        print("########## Verify that sha-256 Authentication with the authentication type for crypto authentication sha-256 works as expected.#############")
        print("###### 2 DUTs ######")

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/9", "Gi 0/5")

        # Creating VLANs

        DUT1.vl.create_vlan(vlan="20")
        DUT2.vl.create_vlans("15", "20")

        # Adding the ports to the VLANs

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")

        # Adding IPs on the interfaces

        DUT1.ip.add_ip_interface(int_vlan="20", ip="20.0.0.2", mask="255.255.255.0")
        DUT2.ip.add_ip_interfaces("15", "20", int_vlan15=["15.0.0.1", "255.255.255.0"],
                              int_vlan20=["20.0.0.1", "255.255.255.0"])

        DUT1.ip.no_shut_int_vlans("20")
        DUT2.ip.no_shut_int_vlans("20", "15")

        # Enabling RIP and advertising the interfaces into RIP

        DUT1.rip.enable_rip()
        DUT2.rip.enable_rip()

        DUT1.rip.advertise_network(ip_network="20.0.0.2")
        DUT2.rip.advertise_networks("20.0.0.1", "15.0.0.1")

        # Enable authentication key on the int VLAN between the DUTs on DUT2 and shut/no shut the int VLAN between them

        DUT2.rip.add_ip_rip_auth_type_mode(int_vlan="20", mode="sha-256", key_id="1", key="12345")

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        # Checking if the routes are not installed

        time.sleep(45)

        dict_rip_routes_1 = DUT1.rip.show_ip_route_rip()
        # print(dict_rip_routes_1)
        dict_of_int_vlans_authentication_2 = DUT2.rip.show_ip_rip_authentication()
        dict_of_int_vlans_authentication_1 = DUT1.rip.show_ip_rip_authentication()
        print(dict_of_int_vlans_authentication_2)
        print(dict_of_int_vlans_authentication_1)

        assert "15.0.0.0" not in dict_rip_routes_1.keys()
        assert "20" in dict_of_int_vlans_authentication_2 and dict_of_int_vlans_authentication_2["20"]["Authentication Type"] == "sha256"
        assert "20" in dict_of_int_vlans_authentication_1 and dict_of_int_vlans_authentication_1["20"]["Authentication Type"] == "none"

        # Enable the same authentication key on DUT1 and check that routes are installed

        DUT1.rip.add_ip_rip_auth_type_mode(int_vlan="20", mode="sha-256", key_id="1", key="12345")

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(30)

        dict_rip_routes_1 = DUT1.rip.show_ip_route_rip()
        print(dict_rip_routes_1)
        dict_of_int_vlans_authentication_2 = DUT2.rip.show_ip_rip_authentication()
        dict_of_int_vlans_authentication_1 = DUT1.rip.show_ip_rip_authentication()
        print(dict_of_int_vlans_authentication_2)
        print(dict_of_int_vlans_authentication_1)

        assert "15.0.0.0" in dict_rip_routes_1.keys()
        assert "20" in dict_of_int_vlans_authentication_2 and dict_of_int_vlans_authentication_2["20"]["Authentication Type"] == "sha256"
        assert "20" in dict_of_int_vlans_authentication_1 and dict_of_int_vlans_authentication_1["20"]["Authentication Type"] == "sha256"
        assert dict_of_int_vlans_authentication_2["20"]['Authentication KeyId in use'] == dict_of_int_vlans_authentication_1["20"]['Authentication KeyId in use'] == "1"

        # Disable the authentication and check that the routes are installed on DUT1

        DUT1.rip.remove_ip_rip_authentication_mode(int_vlan="20")
        DUT2.rip.remove_ip_rip_authentication_mode(int_vlan="20")

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(35)

        dict_rip_routes_1 = DUT1.rip.show_ip_route_rip()
        print(dict_rip_routes_1)
        dict_of_int_vlans_authentication_2 = DUT2.rip.show_ip_rip_authentication()
        dict_of_int_vlans_authentication_1 = DUT1.rip.show_ip_rip_authentication()
        print(dict_of_int_vlans_authentication_2)
        print(dict_of_int_vlans_authentication_1)

        assert "15.0.0.0" in dict_rip_routes_1.keys()
        assert "20" in dict_of_int_vlans_authentication_2 and dict_of_int_vlans_authentication_2["20"]["Authentication Type"] == "none"
        assert "20" in dict_of_int_vlans_authentication_1 and dict_of_int_vlans_authentication_1["20"]["Authentication Type"] == "none"

        print("########## Removing the config #############")

        DUT1.rip.disable_rip()
        DUT2.rip.disable_rip()

        DUT1.ip.remove_int_vlan(int_vlan="20")
        DUT2.ip.remove_vlan_interfaces("20", "15")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5")

        DUT1.vl.remove_vlan(vlan="20")
        DUT2.vl.remove_vlans("20", "15")

    def test_func_13(self):

        print("###### Test_func_13 ######")
        print("########## Verify that multiple authentication keys can be configured on a DUT.#############")
        print("###### 2 DUTs ######")

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/9", "Gi 0/5")

        # Creating VLANs

        DUT1.vl.create_vlan(vlan="20")
        DUT2.vl.create_vlans("15", "20")

        # Adding the ports to the VLANs

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")

        # Adding IPs on the interfaces

        DUT1.ip.add_ip_interface(int_vlan="20", ip="20.0.0.2", mask="255.255.255.0")
        DUT2.ip.add_ip_interfaces("15", "20", int_vlan15=["15.0.0.1", "255.255.255.0"],
                              int_vlan20=["20.0.0.1", "255.255.255.0"])

        DUT1.ip.no_shut_int_vlans("20")
        DUT2.ip.no_shut_int_vlans("20", "15")

        # Enabling RIP and advertising the interfaces into RIP

        DUT1.rip.enable_rip()
        DUT2.rip.enable_rip()

        DUT1.rip.advertise_network(ip_network="20.0.0.2")
        DUT2.rip.advertise_networks("20.0.0.1", "15.0.0.1")

        # Enable authentication key on the int VLAN between the DUTs on DUT2 and shut/no shut the int VLAN between them

        DUT2.rip.add_ip_rip_auth_type_mode(int_vlan="20", mode="md5", key_id="1", key="12345")
        DUT2.rip.add_ip_rip_auth_type_mode(int_vlan="20", mode="md5", key_id="2", key="123456")

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        # Checking if the routes are not installed

        time.sleep(35)

        dict_rip_routes_1 = DUT1.rip.show_ip_route_rip()
        print(dict_rip_routes_1)
        dict_of_int_vlans_authentication_2 = DUT2.rip.show_ip_rip_authentication()
        dict_of_int_vlans_authentication_1 = DUT1.rip.show_ip_rip_authentication()
        print(dict_of_int_vlans_authentication_2)
        print(dict_of_int_vlans_authentication_1)

        assert "15.0.0.0" not in dict_rip_routes_1.keys()
        assert "20" in dict_of_int_vlans_authentication_2 and dict_of_int_vlans_authentication_2["20"]["Authentication Type"] == "md5"
        assert "20" in dict_of_int_vlans_authentication_1 and dict_of_int_vlans_authentication_1["20"]["Authentication Type"] == "none"

        # Enable the same authentication key on DUT1 and check that routes are installed

        DUT1.rip.add_ip_rip_auth_type_mode(int_vlan="20", mode="md5", key_id="1", key="12345")
        DUT1.rip.add_ip_rip_auth_type_mode(int_vlan="20", mode="md5", key_id="2", key="123456")

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(30)

        dict_rip_routes_1 = DUT1.rip.show_ip_route_rip()
        print(dict_rip_routes_1)
        dict_of_int_vlans_authentication_2 = DUT2.rip.show_ip_rip_authentication()
        dict_of_int_vlans_authentication_1 = DUT1.rip.show_ip_rip_authentication()
        print(dict_of_int_vlans_authentication_2)
        print(dict_of_int_vlans_authentication_1)

        assert "15.0.0.0" in dict_rip_routes_1.keys()
        assert "20" in dict_of_int_vlans_authentication_2 and dict_of_int_vlans_authentication_2["20"]["Authentication Type"] == "md5"
        assert "20" in dict_of_int_vlans_authentication_1 and dict_of_int_vlans_authentication_1["20"]["Authentication Type"] == "md5"
        assert dict_of_int_vlans_authentication_2["20"]['Authentication KeyId in use'] == dict_of_int_vlans_authentication_1["20"]['Authentication KeyId in use'] == "2"

        # Disable the last authentication key on both DUTs and check that the routes are installed on DUT1 with key-id 1

        DUT1.rip.remove_ip_rip_authentication_key(int_vlan="20",key_id="2")
        DUT2.rip.remove_ip_rip_authentication_key(int_vlan="20",key_id="2")

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(35)

        dict_rip_routes_1 = DUT1.rip.show_ip_route_rip()
        print(dict_rip_routes_1)
        dict_of_int_vlans_authentication_2 = DUT2.rip.show_ip_rip_authentication()
        dict_of_int_vlans_authentication_1 = DUT1.rip.show_ip_rip_authentication()
        print(dict_of_int_vlans_authentication_2)
        print(dict_of_int_vlans_authentication_1)

        assert "15.0.0.0" in dict_rip_routes_1.keys()
        assert "20" in dict_of_int_vlans_authentication_2 and dict_of_int_vlans_authentication_2["20"]["Authentication Type"] == "md5"
        assert "20" in dict_of_int_vlans_authentication_1 and dict_of_int_vlans_authentication_1["20"][ "Authentication Type"] == "md5"
        assert dict_of_int_vlans_authentication_2["20"]['Authentication KeyId in use'] == dict_of_int_vlans_authentication_1["20"]['Authentication KeyId in use'] == "1"

        # Remove the authentication on both DUTs and check that the routes are installed

        DUT1.rip.remove_ip_rip_authentication_mode(int_vlan="20")
        DUT2.rip.remove_ip_rip_authentication_mode(int_vlan="20")

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(35)

        dict_rip_routes_1 = DUT1.rip.show_ip_route_rip()
        print(dict_rip_routes_1)
        dict_of_int_vlans_authentication_2 = DUT2.rip.show_ip_rip_authentication()
        dict_of_int_vlans_authentication_1 = DUT1.rip.show_ip_rip_authentication()
        print(dict_of_int_vlans_authentication_2)
        print(dict_of_int_vlans_authentication_1)

        assert "15.0.0.0" in dict_rip_routes_1.keys()
        assert "20" in dict_of_int_vlans_authentication_2 and dict_of_int_vlans_authentication_2["20"]["Authentication Type"] == "none"
        assert "20" in dict_of_int_vlans_authentication_1 and dict_of_int_vlans_authentication_1["20"]["Authentication Type"] == "none"

        print("########## Removing the config #############")

        DUT1.rip.disable_rip()
        DUT2.rip.disable_rip()

        DUT1.ip.remove_int_vlan(int_vlan="20")
        DUT2.ip.remove_vlan_interfaces("20", "15")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5")

        DUT1.vl.remove_vlan(vlan="20")
        DUT2.vl.remove_vlans("20", "15")

    def test_func_14(self):

        print("###### Test_func_14 ######")
        print("########## Check if we can advertise networks into RIP and it establish connection using int vlans #############")
        print("###### 3 DUTs ######")

        #       Topology
        #
        #         RIP
        #
        # -- DUT1 ---- DUT2
        #       \      /
        #        \    /
        #         DUT3
        #

        # No shutting the interfaces on DUTs

        DUT1.int.no_shut_interfaces("Gi 0/3", "Gi 0/4", "Ex 0/1", "Gi 0/9")
        DUT2.int.no_shut_interfaces("Gi 0/4", "Gi 0/5", "Gi 0/6", "Gi 0/9")
        DUT3.int.no_shut_interfaces("Gi 0/4", "Gi 0/9")

        # Creating the VLAN on all DUTs

        DUT1.vl.create_vlan(vlan="30")
        DUT1.vl.create_vlan(vlan="14")
        DUT1.vl.create_vlan(vlan="11")

        DUT2.vl.create_vlan(vlan="15")
        DUT2.vl.create_vlan(vlan="14")
        DUT2.vl.create_vlan(vlan="12")

        DUT3.vl.create_vlan(vlan="11")
        DUT3.vl.create_vlan(vlan="12")
        # DUT3.vl.create_vlan(vlan="20")

        # Adding the ports to the VLAN

        DUT1.vl.add_ports_to_vlan(ports="Gi 0/3", vlan="30")
        DUT1.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="11")
        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="14")

        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="14")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/4", vlan="12")

        # DUT3.vl.add_ports_to_vlan(ports="Gi 0/4", vlan="20")
        DUT3.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="11")
        DUT3.vl.add_ports_to_vlan(ports="Gi 0/4", vlan="12")

        # Create IP interfaces on all DUTs for the specific VLANs

        DUT1.ip.add_ip_interfaces("14", "30", "11", int_vlan14=["14.0.0.2", "255.255.255.0"],
                              int_vlan30=["30.0.0.1", "255.255.255.0"], int_vlan11=["11.0.0.2", "255.255.255.0"])
        DUT1.ip.no_shut_int_vlans("14", "30", "11")

        DUT2.ip.add_ip_interfaces("14", "15", "12", int_vlan14=["14.0.0.1", "255.255.255.0"],
                              int_vlan15=["15.0.0.1", "255.255.255.0"], int_vlan12=["12.0.0.1", "255.255.255.0"])
        DUT2.ip.no_shut_int_vlans("14", "15", "12")

        DUT3.ip.add_ip_interfaces("11", "12", int_vlan11=["11.0.0.1", "255.255.255.0"],
                              int_vlan12=["12.0.0.2", "255.255.255.0"])
        DUT3.ip.no_shut_int_vlans("11", "12")

        # Enable rip on all DUTs and advertise the IPs

        DUT1.rip.enable_rip()
        DUT1.rip.advertise_networks("14.0.0.2", "30.0.0.1", "11.0.0.2")

        DUT2.rip.enable_rip()
        DUT2.rip.advertise_networks("14.0.0.1", "15.0.0.1", "12.0.0.1")

        DUT3.rip.enable_rip()
        DUT3.rip.advertise_networks("11.0.0.1", "12.0.0.2")

        time.sleep(30)

        dict_rip_routes_1 = DUT1.rip.show_ip_route_rip()
        dict_rip_routes_2 = DUT2.rip.show_ip_route_rip()
        dict_rip_routes_3 = DUT3.rip.show_ip_route_rip()
        # print(dict_rip_routes_1["15.0.0.0"]["Learned From"])
        print(dict_rip_routes_1)

        # Check if the routes are learned and installed using RIP

        assert "15.0.0.0" in dict_rip_routes_1.keys() and "12.0.0.0" in dict_rip_routes_1.keys()
        assert "30.0.0.0" in dict_rip_routes_2.keys() and "11.0.0.0" in dict_rip_routes_2.keys()
        assert "30.0.0.0" in dict_rip_routes_3.keys() and "15.0.0.0" in dict_rip_routes_3.keys() and "14.0.0.0" in dict_rip_routes_3.keys()

        print("########## Removing the config #############")

        DUT1.rip.disable_rip()
        DUT2.rip.disable_rip()
        DUT3.rip.disable_rip()

        DUT1.ip.remove_vlan_interfaces("14", "30", "11")
        DUT2.ip.remove_vlan_interfaces("14", "15", "12")
        DUT3.ip.remove_vlan_interfaces("11", "12")

        DUT1.vl.remove_vlans("14", "30", "11")
        DUT2.vl.remove_vlans("14", "15", "12")
        DUT3.vl.remove_vlans("11", "12")

        DUT1.int.shut_interfaces("Gi 0/3", "Gi 0/4", "Ex 0/1", "Gi 0/9")
        DUT2.int.shut_interfaces("Gi 0/4", "Gi 0/5", "Gi 0/6", "Gi 0/9")
        DUT3.int.shut_interfaces("Gi 0/4", "Gi 0/9")

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
        #

        # Creating routed ports on all DUTs

        DUT1.int.add_routed_ports("Ex 0/2", "Gi 0/10")
        DUT2.int.add_routed_ports("Gi 0/3", "Gi 0/10")
        DUT3.int.add_routed_ports("Gi 0/3", "Gi 0/10")

        # No shutting the interfaces

        DUT1.int.no_shut_interfaces("Ex 0/2", "Gi 0/10")
        DUT2.int.no_shut_interfaces("Gi 0/3", "Gi 0/5", "Gi 0/10")
        DUT3.int.no_shut_interfaces("Gi 0/3", "Gi 0/10")

        # Creating the VLAN on DUT2

        DUT2.vl.create_vlan(vlan="15")

        # Adding the ports to the VLAN

        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")

        # Create IP Routed Ports on all DUTs

        DUT1.ip.add_ip_routed_ports("Ex 0/2", "Gi 0/10", Ex_0_2=["14.0.0.2", "255.255.255.0"], Gi_0_10=["13.0.0.2", "255.255.255.0"])

        DUT2.ip.add_ip_routed_ports("Gi 0/3", "Gi 0/10", Gi_0_3=["12.0.0.1", "255.255.255.0"], Gi_0_10=["14.0.0.1", "255.255.255.0"])
        DUT2.ip.add_ip_interface(int_vlan="15",ip="15.0.0.1",mask="255.255.255.0")
        DUT2.ip.no_shut_int_vlan(int_vlan="15")

        DUT3.ip.add_ip_routed_ports("Gi 0/3", "Gi 0/10", Gi_0_3=["12.0.0.2", "255.255.255.0"],Gi_0_10=["13.0.0.1", "255.255.255.0"])

        # Enable rip on all DUTs and advertise the IPs

        DUT1.rip.enable_rip()
        DUT1.rip.advertise_networks("13.0.0.2","14.0.0.2")

        DUT2.rip.enable_rip()
        DUT2.rip.advertise_networks("12.0.0.1", "14.0.0.1", "15.0.0.1")

        DUT3.rip.enable_rip()
        DUT3.rip.advertise_networks("12.0.0.2", "13.0.0.1")

        time.sleep(30)

        dict_rip_routes_1 = DUT1.rip.show_ip_route_rip()
        dict_rip_routes_2 = DUT2.rip.show_ip_route_rip()
        dict_rip_routes_3 = DUT3.rip.show_ip_route_rip()

        print(dict_rip_routes_1)
        print(dict_rip_routes_2)
        print(dict_rip_routes_3)

        # Check if the routes are learned and installed in RIP routes

        assert "15.0.0.0" in dict_rip_routes_1.keys() and "12.0.0.0" in dict_rip_routes_1.keys()
        assert "13.0.0.0" in dict_rip_routes_2.keys()
        assert "15.0.0.0" in dict_rip_routes_3.keys() and "14.0.0.0" in dict_rip_routes_3.keys()

        # Shut one port on DUT1 and check that RIP routes are not missing

        DUT1.int.shut_interface(interface="Ex 0/2")

        time.sleep(45)

        dict_rip_routes_1 = DUT1.rip.show_ip_route_rip()
        dict_rip_routes_2 = DUT2.rip.show_ip_route_rip()
        dict_rip_routes_3 = DUT3.rip.show_ip_route_rip()

        print(dict_rip_routes_1)
        print(dict_rip_routes_2)
        print(dict_rip_routes_3)

        assert "15.0.0.0" in dict_rip_routes_1.keys() and "12.0.0.0" in dict_rip_routes_1.keys() # Trb "in" in loc de "not in"
        assert "13.0.0.0" in dict_rip_routes_2.keys()
        assert "15.0.0.0" in dict_rip_routes_3.keys()

        # No shut the port on DUT1 and check that RIP routes are not missing

        DUT1.int.no_shut_interface(interface="Ex 0/2")

        time.sleep(45)

        dict_rip_routes_1 = DUT1.rip.show_ip_route_rip()
        dict_rip_routes_2 = DUT2.rip.show_ip_route_rip()
        dict_rip_routes_3 = DUT3.rip.show_ip_route_rip()

        print(dict_rip_routes_1)
        print(dict_rip_routes_2)
        print(dict_rip_routes_3)

        assert "15.0.0.0" in dict_rip_routes_1.keys() and "12.0.0.0" in dict_rip_routes_1.keys()
        assert "13.0.0.0" in dict_rip_routes_2.keys()
        assert "15.0.0.0" in dict_rip_routes_3.keys() and "14.0.0.0" in dict_rip_routes_3.keys()

        print("########## Removing the config #############")

        DUT1.rip.disable_rip()
        DUT2.rip.disable_rip()
        DUT3.rip.disable_rip()

        DUT2.ip.remove_vlan_interfaces("15")

        DUT2.vl.remove_vlans("15")

        DUT1.int.remove_routed_ports("Ex 0/2","Gi 0/10")
        DUT2.int.remove_routed_ports("Gi 0/3", "Gi 0/10")
        DUT3.int.remove_routed_ports("Gi 0/3", "Gi 0/10")

        DUT2.int.shut_interfaces("Gi 0/5")

    def test_func_16(self):

        print("###### Test_func_16 ######")
        print("########## Verify functionality for redistribute OSPF into RIP #############")
        print("###### 3 DUTs ######")

        #          Topology
        #
        #  DUT1 --RIP-- DUT2 --OSPF-- DUT3 -- OSPF
        #

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/9", "Gi 0/5", "Gi 0/4")
        DUT3.int.no_shut_interfaces("Gi 0/4")

        # Creating VLANs

        DUT1.vl.create_vlan(vlan="20")
        DUT2.vl.create_vlans("15", "12", "20")
        DUT3.vl.create_vlans("12", "100")

        # Adding the ports to the VLANs

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/4", vlan="12")
        DUT3.vl.add_ports_to_vlan(ports="Gi 0/4", vlan="12")
        DUT3.vl.add_ports_to_vlan(ports="Gi 0/4", vlan="100")

        # Adding IPs on the interfaces

        DUT1.ip.add_ip_interface(int_vlan="20", ip="20.0.0.2", mask="255.255.255.0")
        DUT2.ip.add_ip_interfaces("15", "12", "20", int_vlan15=["15.0.0.1", "255.255.255.0"],int_vlan12=["12.0.0.1", "255.255.255.0"], int_vlan20=["20.0.0.1", "255.255.255.0"])
        DUT3.ip.add_ip_interfaces("12", "100", int_vlan12=["12.0.0.2", "255.255.255.0"],int_vlan100=["100.0.0.2", "255.255.255.0"])

        DUT1.ip.no_shut_int_vlans("20")
        DUT2.ip.no_shut_int_vlans("20", "15", "12")
        DUT3.ip.no_shut_int_vlans("12", "100")

        # Enabling RIP and advertising the interfaces in RIP

        DUT1.rip.enable_rip()
        DUT2.rip.enable_rip()

        DUT1.rip.advertise_network(ip_network="20.0.0.2")
        DUT2.rip.advertise_networks("20.0.0.1", "15.0.0.1")

        # Enabling OSPF and advertising the network into OSPF

        DUT2.ospf.enable_ospf()
        DUT3.ospf.enable_ospf()

        DUT2.ospf.advertise_network(ip_network="12.0.0.1", area="0.0.0.0")
        DUT3.ospf.advertise_network(ip_network="12.0.0.2", area="0.0.0.0")
        DUT3.ospf.advertise_network(ip_network="100.0.0.2", area="0.0.0.0")

        # Redistributing OSPF into RIP on DUT2 and installing it on DUT1

        DUT2.rip.redistribute_ospf()

        # Checking if the routes are installed

        time.sleep(45)

        dict_rip_routes_1 = DUT1.rip.show_ip_route_rip()
        print(dict_rip_routes_1)

        assert "15.0.0.0" in dict_rip_routes_1.keys()
        assert "100.0.0.0" in dict_rip_routes_1.keys()

        # Remove the ospf route on DUT2 and check if the route is not anymore in the routing table of DUT1

        DUT2.rip.remove_redistribute_ospf()

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(30)

        dict_rip_routes_1 = DUT1.rip.show_ip_route_rip()
        print(dict_rip_routes_1)

        if len(dict_rip_routes_1.keys()) == 0:
            assert True
        else:
            assert "15.0.0.0" in dict_rip_routes_1.keys()
            assert "100.0.0.0" not in dict_rip_routes_1.keys()

        print("########## Removing the config #############")

        DUT1.rip.disable_rip()
        DUT2.rip.disable_rip()

        DUT2.ospf.remove_network(ip_network="12.0.0.1", area="0.0.0.0")
        DUT3.ospf.remove_network(ip_network="12.0.0.2", area="0.0.0.0")
        DUT3.ospf.remove_network(ip_network="100.0.0.2", area="0.0.0.0")

        DUT2.ospf.disable_ospf()
        DUT3.ospf.disable_ospf()

        DUT1.ip.remove_int_vlan(int_vlan="20")
        DUT2.ip.remove_vlan_interfaces("20", "15", "12")
        DUT3.ip.remove_vlan_interfaces("12", "100")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5", "Gi 0/4")
        DUT3.int.shut_interfaces("Gi 0/4")

        DUT1.vl.remove_vlan(vlan="20")
        DUT2.vl.remove_vlans("20", "15", "12")
        DUT3.vl.remove_vlans("12", "100")

    def test_func_17(self):

        print("###### Test_func_17 ######")
        print("########## Verify functionality for redistribute all into RIP #############")
        print("###### 3 DUTs ######")

        #          Topology
        #
        #  DUT1 --RIP-- DUT2 --OSPF-- DUT3 -- OSPF
        #

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/9", "Gi 0/5", "Gi 0/4")
        DUT3.int.no_shut_interfaces("Gi 0/4")

        # Creating VLANs

        DUT1.vl.create_vlan(vlan="20")
        DUT2.vl.create_vlans("15", "12", "20")
        DUT3.vl.create_vlans("12", "100")

        # Adding the ports to the VLANs

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/4", vlan="12")
        DUT3.vl.add_ports_to_vlan(ports="Gi 0/4", vlan="12")
        DUT3.vl.add_ports_to_vlan(ports="Gi 0/4", vlan="100")

        # Adding IPs on the interfaces

        DUT1.ip.add_ip_interface(int_vlan="20", ip="20.0.0.2", mask="255.255.255.0")
        DUT2.ip.add_ip_interfaces("15", "12", "20", int_vlan15=["15.0.0.1", "255.255.255.0"],
                              int_vlan12=["12.0.0.1", "255.255.255.0"], int_vlan20=["20.0.0.1", "255.255.255.0"])
        DUT3.ip.add_ip_interfaces("12", "100", int_vlan12=["12.0.0.2", "255.255.255.0"],
                              int_vlan100=["100.0.0.2", "255.255.255.0"])

        DUT1.ip.no_shut_int_vlans("20")
        DUT2.ip.no_shut_int_vlans("20", "15", "12")
        DUT3.ip.no_shut_int_vlans("12", "100")

        # Enabling RIP and advertising the interfaces in RIP

        DUT1.rip.enable_rip()
        DUT2.rip.enable_rip()

        DUT1.rip.advertise_network(ip_network="20.0.0.2")
        DUT2.rip.advertise_networks("20.0.0.1")

        # Enabling OSPF and advertising the networks into OSPF

        DUT2.ospf.enable_ospf()
        DUT3.ospf.enable_ospf()

        # You have to remove newtork and add it back because of the OSPF process that is not eliminated after disabling it

        DUT2.ospf.advertise_network(ip_network="12.0.0.1", area="0.0.0.0")
        DUT3.ospf.advertise_network(ip_network="12.0.0.2", area="0.0.0.0")
        DUT3.ospf.advertise_network(ip_network="100.0.0.2", area="0.0.0.0")

        # Creating a static route on DUT 2

        DUT2.ip.add_static_route(network_dest="88.0.0.0", mask_dest="255.255.255.0", next_hop="15.0.0.100")

        # Redistributing all into RIP on DUT2 and installing it on DUT1

        DUT2.rip.redistribute_all()

        # Checking if the routes are installed

        time.sleep(45)

        dict_rip_routes_1 = DUT1.rip.show_ip_route_rip()
        print(dict_rip_routes_1)

        assert "15.0.0.0" in dict_rip_routes_1.keys()
        assert "12.0.0.0" in dict_rip_routes_1.keys()
        assert "100.0.0.0" in dict_rip_routes_1.keys()
        assert "88.0.0.0" in dict_rip_routes_1.keys()

        # Remove the all redistribution on DUT2 and check if the routes are not anymore in the routing table of DUT1

        DUT2.rip.remove_redistribute_all()

        DUT1.ip.shut_int_vlan(int_vlan="20")
        DUT1.ip.no_shut_int_vlan(int_vlan="20")

        time.sleep(30)

        dict_rip_routes_1 = DUT1.rip.show_ip_route_rip()
        print(dict_rip_routes_1)

        if len(dict_rip_routes_1.keys()) == 0:
            assert True
        else:
            assert "15.0.0.0" not in dict_rip_routes_1.keys()
            assert "12.0.0.0" not in dict_rip_routes_1.keys()
            assert "100.0.0.0" not in dict_rip_routes_1.keys()
            assert "88.0.0.0" not in dict_rip_routes_1.keys()

        print("########## Removing the config #############")

        DUT1.rip.disable_rip()
        DUT2.rip.disable_rip()

        DUT2.ospf.remove_network(ip_network="12.0.0.1", area="0.0.0.0")
        DUT3.ospf.remove_network(ip_network="12.0.0.2", area="0.0.0.0")
        DUT3.ospf.remove_network(ip_network="100.0.0.2", area="0.0.0.0")

        DUT2.ospf.disable_ospf()
        DUT3.ospf.disable_ospf()

        DUT2.ip.remove_static_route(network_dest="88.0.0.0", mask_dest="255.255.255.0", next_hop="15.0.0.100")

        DUT1.ip.remove_int_vlan(int_vlan="20")
        DUT2.ip.remove_vlan_interfaces("20", "15", "12")
        DUT3.ip.remove_vlan_interfaces("12", "100")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5", "Gi 0/4")
        DUT3.int.shut_interfaces("Gi 0/4")

        DUT1.vl.remove_vlan(vlan="20")
        DUT2.vl.remove_vlans("20", "15", "12")
        DUT3.vl.remove_vlans("12", "100")

    def test_func_18(self):

        print("###### Test_func_18 ######")
        print("########## Verify that the DUT performs invalid timer correctly.#############")
        print("###### 2 DUTs ######")

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/9", "Gi 0/5")

        # Creating VLANs

        DUT1.vl.create_vlan(vlan="20")
        DUT2.vl.create_vlans("15", "20")

        # Adding the ports to the VLANs

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")

        # Adding IPs on the interfaces

        DUT1.ip.add_ip_interface(int_vlan="20", ip="20.0.0.2", mask="255.255.255.0")
        DUT2.ip.add_ip_interfaces("15", "20", int_vlan15=["15.0.0.1", "255.255.255.0"],
                              int_vlan20=["20.0.0.1", "255.255.255.0"])

        DUT1.ip.no_shut_int_vlans("20")
        DUT2.ip.no_shut_int_vlans("20", "15")

        # Enabling RIP and advertising the interfaces into RIP

        DUT1.rip.enable_rip()
        DUT2.rip.enable_rip()

        DUT1.rip.advertise_network(ip_network="20.0.0.2")
        DUT2.rip.advertise_networks("20.0.0.1", "15.0.0.1")

        # Shut the in vlan between the DUTs. Check the route is present in the Routing Table

        dict_rip_routes_1 = DUT1.rip.show_ip_route_rip()
        print(dict_rip_routes_1)
        assert "15.0.0.0" in dict_rip_routes_1.keys()

        DUT2.ip.shut_int_vlan(int_vlan="20")

        # Checking the routes are not installed in RIP routing table, but they are in RIP database. (After 180s)

        time.sleep(180)

        dict_rip_routes_1 = DUT1.rip.show_ip_route_rip()
        match_total_count, dict_of_auto_summary, dict_of_directly_connected, dict_of_via = DUT1.rip.show_rip_database()
        print(dict_rip_routes_1)
        print(dict_of_via)

        assert "15.0.0.0" not in dict_rip_routes_1.keys()
        assert "15.0.0.0" in dict_of_via.keys() and dict_of_via["15.0.0.0"]["Metric"] == "16"

        # Checking the routes are eliminated from RIP database. (After 120s)

        time.sleep(120)

        dict_rip_routes_1 = DUT1.rip.show_ip_route_rip()
        match_total_count, dict_of_auto_summary, dict_of_directly_connected, dict_of_via = DUT1.rip.show_rip_database()
        print(dict_rip_routes_1)
        print(dict_of_via)

        assert "15.0.0.0" not in dict_rip_routes_1.keys()
        assert "15.0.0.0" not in dict_of_via.keys()

        # No shut the interface to check that the routes are installing

        DUT2.ip.no_shut_int_vlan(int_vlan="20")

        # Configuring the timers

        DUT1.rip.configure_rip_timers(int_vlan="20",update_timer="10",routage_timer="30",garbage_timer="150")

        # Shut the in vlan between the DUTs. Check the route is present in the Routing Table

        time.sleep(20)

        dict_rip_routes_1 = DUT1.rip.show_ip_route_rip()
        print(dict_rip_routes_1)
        assert "15.0.0.0" in dict_rip_routes_1.keys()

        DUT2.ip.shut_int_vlan(int_vlan="20")

        # Checking the routes are not installed in RIP routing table, but they are in RIP database. (After 30s)

        time.sleep(30)

        dict_rip_routes_1 = DUT1.rip.show_ip_route_rip()
        match_total_count, dict_of_auto_summary, dict_of_directly_connected, dict_of_via = DUT1.rip.show_rip_database()
        print(dict_rip_routes_1)
        print(dict_of_via)

        assert "15.0.0.0" not in dict_rip_routes_1.keys()
        assert "15.0.0.0" in dict_of_via.keys() and dict_of_via["15.0.0.0"]["Metric"] == "16"

        # Checking the routes are eliminated from RIP database. (After 150s)

        time.sleep(150)

        dict_rip_routes_1 = DUT1.rip.show_ip_route_rip()
        match_total_count, dict_of_auto_summary, dict_of_directly_connected, dict_of_via = DUT1.rip.show_rip_database()
        print(dict_rip_routes_1)
        print(dict_of_via)

        assert "15.0.0.0" not in dict_rip_routes_1.keys()
        assert "15.0.0.0" not in dict_of_via.keys()

        print("########## Removing the config #############")

        DUT1.rip.remove_rip_timers(int_vlan="20")

        DUT1.rip.disable_rip()
        DUT2.rip.disable_rip()

        DUT1.ip.remove_int_vlan(int_vlan="20")
        DUT2.ip.remove_vlan_interfaces("20", "15")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5")

        DUT1.vl.remove_vlan(vlan="20")
        DUT2.vl.remove_vlans("20", "15")

    def test_func_19(self):

        print("###### Test_func_19 ######")
        print("########## Verify that the DUT sends updates at update timer value.#############")
        print("###### 2 DUTs ######")

        DUT1.int.no_shut_interfaces("Ex 0/1")
        DUT2.int.no_shut_interfaces("Gi 0/9", "Gi 0/5")

        # Creating VLANs

        DUT1.vl.create_vlan(vlan="20")
        DUT2.vl.create_vlans("15", "20")

        # Adding the ports to the VLANs

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")

        # Adding IPs on the interfaces

        DUT1.ip.add_ip_interface(int_vlan="20", ip="20.0.0.2", mask="255.255.255.0")
        DUT2.ip.add_ip_interfaces("15", "20", int_vlan15=["15.0.0.1", "255.255.255.0"],
                              int_vlan20=["20.0.0.1", "255.255.255.0"])

        DUT1.ip.no_shut_int_vlans("20")
        DUT2.ip.no_shut_int_vlans("20", "15")

        # Enabling RIP and advertising the interfaces into RIP

        DUT1.rip.enable_rip()
        DUT2.rip.enable_rip()

        DUT1.rip.advertise_network(ip_network="20.0.0.2")
        DUT2.rip.advertise_networks("20.0.0.1", "15.0.0.1")

        # Check the RIP statistics and verify the DUT is sending updates as expected (default is 30s)

        time.sleep(60)

        dict_rip_statistics = DUT1.rip.show_ip_rip_statistics()
        print(dict_rip_statistics)
        # The number should be 2 (30sx2)

        assert dict_rip_statistics["20.0.0.2"]["Updates Sent"] == "3"  # 2 in 60s + 1 that is sent after 60s

        # Modify the update timer for RIP

        DUT1.rip.remove_network(ip_network="20.0.0.2")
        DUT1.rip.advertise_network(ip_network="20.0.0.2")
        DUT1.rip.configure_rip_timers(int_vlan="20", update_timer="10", routage_timer="30", garbage_timer="150")

        # Check the RIP statistics and verify the DUT is sending updates as expected (now is 10s)

        time.sleep(53)

        dict_rip_statistics = DUT1.rip.show_ip_rip_statistics()
        print(dict_rip_statistics)
        # The number should be 6 (10sx6)

        assert dict_rip_statistics["20.0.0.2"]["Updates Sent"] == "7"  # 6 in 60s + 1 that is sent after 60s

        print("########## Removing the config #############")

        DUT1.rip.remove_rip_timers(int_vlan="20")

        DUT1.rip.disable_rip()
        DUT2.rip.disable_rip()

        DUT1.ip.remove_int_vlan(int_vlan="20")
        DUT2.ip.remove_vlan_interfaces("20", "15")

        DUT1.int.shut_interface(interface="Ex 0/1")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5")

        DUT1.vl.remove_vlan(vlan="20")
        DUT2.vl.remove_vlans("20", "15")
