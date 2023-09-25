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
ip_session_3 = "10.2.109.232"

# dut_obj_1 = dut_objects.DUT_Objects(ip_session=ip_session_1)
# dut_obj_1.rip.disable_rip()


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

# DUT 1 Objects

int1 = interfaces.Interface(ip_session=ip_session_1)
vl1 = vlan.VLAN(ip_session=ip_session_1)
stp1 = stp.STP(ip_session=ip_session_1)
fdb1 = fdb.FDB(ip_session=ip_session_1)
ip1 = ip.IP(ip_session=ip_session_1)
rip1 = rip.RIP(ip_session=ip_session_1)
ping1 = ping.PING(ip_session=ip_session_1)
ospf1 = ospf.OSPF(ip_session=ip_session_1)

# DUT 2 Objects

int2 = interfaces.Interface(ip_session=ip_session_2)
vl2 = vlan.VLAN(ip_session=ip_session_2)
stp2 = stp.STP(ip_session=ip_session_2)
fdb2 = fdb.FDB(ip_session=ip_session_2)
ip2 = ip.IP(ip_session=ip_session_2)
rip2 = rip.RIP(ip_session=ip_session_2)
ping2 = ping.PING(ip_session=ip_session_2)
ospf2 = ospf.OSPF(ip_session=ip_session_2)

# DUT 3 Objects

int3 = interfaces.Interface(ip_session=ip_session_3)
vl3 = vlan.VLAN(ip_session=ip_session_3)
stp3 = stp.STP(ip_session=ip_session_3)
fdb3 = fdb.FDB(ip_session=ip_session_3)
ip3 = ip.IP(ip_session=ip_session_3)
rip3 = rip.RIP(ip_session=ip_session_3)
ping3 = ping.PING(ip_session=ip_session_3)
ospf3 = ospf.OSPF(ip_session=ip_session_3)


class TestRIPSuite1:

    def test_func_1(self):

        print("###### Test_func_1 ######")
        print( "########## Check if we can advertise networks into RIP and it establish connection using int vlans #############")
        print("###### 2 DUTs ######")

        int1.no_shut_interfaces("Gi 0/3", "Gi 0/4", "Ex 0/1")
        int2.no_shut_interfaces("Gi 0/5", "Gi 0/6", "Gi 0/9")

        # Creating the VLAN on all DUTs

        vl1.create_vlan(vlan="30")
        vl1.create_vlan(vlan="14")

        vl2.create_vlan(vlan="15")
        vl2.create_vlan(vlan="14")

        # Adding the ports to the VLAN

        vl1.add_ports_to_vlan(ports="Gi 0/3", vlan="30")
        vl1.add_ports_to_vlan(ports="Ex 0/1", vlan="14")

        vl2.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
        vl2.add_ports_to_vlan(ports="Gi 0/9", vlan="14")

        # Create IP interfaces on all DUTs for the specific VLANs

        ip1.add_ip_interfaces("14", "30", int_vlan14=["14.0.0.2", "255.255.255.0"],
                              int_vlan30=["30.0.0.1", "255.255.255.0"])
        ip1.no_shut_int_vlans("14", "30")

        ip2.add_ip_interfaces("14", "15", int_vlan14=["14.0.0.1", "255.255.255.0"],
                              int_vlan15=["15.0.0.1", "255.255.255.0"])
        ip2.no_shut_int_vlans("14", "15")

        # Enable rip on all DUTs and advertise the IPs

        rip1.enable_rip()
        rip1.advertise_networks("14.0.0.2", "30.0.0.1")

        rip2.enable_rip()
        rip2.advertise_networks("14.0.0.1", "15.0.0.1")

        time.sleep(30)

        dict_rip_routes_1 = rip1.show_ip_route_rip()
        dict_rip_routes_2 = rip2.show_ip_route_rip()
        # print(dict_rip_routes_1["15.0.0.0"]["Learned From"])

        # Check if the routes are learned and instaled in RIP routes

        assert "15.0.0.0" in dict_rip_routes_1.keys()
        assert "30.0.0.0" in dict_rip_routes_2.keys()

        print("########## Removing the config #############")

        rip1.disable_rip()
        rip2.disable_rip()

        ip1.remove_vlan_interfaces("14", "30")
        ip2.remove_vlan_interfaces("14", "15")

        vl1.remove_vlans("14", "30")
        vl2.remove_vlans("14", "15")

        int1.shut_interfaces("Gi 0/3", "Gi 0/4", "Ex 0/1", "Gi 0/9")
        int2.shut_interfaces("Gi 0/4", "Gi 0/5", "Gi 0/6", "Gi 0/9")

    def test_func_2(self):

        print("###### Test_func_2 ######")
        print(
            "########## Verify a DUT sends a default route if the default-information originate is configured on a RIP enabled interface.#############")
        print("###### 2 DUTs ######")

        int1.no_shut_interfaces("Ex 0/1")
        int2.no_shut_interfaces("Gi 0/9", "Gi 0/5")

        # Creating VLANs

        vl1.create_vlan(vlan="20")
        vl2.create_vlan(vlan="20")
        vl2.create_vlan(vlan="15")

        # Adding the ports to the VLANs

        vl1.add_ports_to_vlan(ports="Ex 0/1", vlan="20")
        vl2.add_ports_to_vlan(ports="Gi 0/9", vlan="20")
        vl2.add_ports_to_vlan(ports="Gi 0/5", vlan="15")

        # Adding IPs on the interfaces

        ip1.add_ip_interface(int_vlan="20", ip="20.0.0.2", mask="255.255.255.0")
        ip2.add_ip_interface(int_vlan="20", ip="20.0.0.1", mask="255.255.255.0")
        ip2.add_ip_interface(int_vlan="15", ip="15.0.0.1", mask="255.255.255.0")

        ip1.no_shut_int_vlans("20")
        ip2.no_shut_int_vlans("20", "15")

        # Enabling RIP and advertising the interfaces in RIP

        rip1.enable_rip()
        rip2.enable_rip()

        rip1.advertise_network(ip_network="20.0.0.2")
        rip2.advertise_networks("20.0.0.1", "15.0.0.1")

        # Advertising the default route on DUT2 and installing the route on DUT1

        rip2.add_default_information_originate(int_vlan="20")
        rip1.add_ip_default_route_install(int_vlan="20")

        # Checking if the route is installed

        time.sleep(30)

        dict_rip_routes_1 = rip1.show_ip_route_rip()
        # print(dict_rip_routes_1)

        assert "0.0.0.0" in dict_rip_routes_1.keys()

        # Remove the route install and check if the default route is not in the routing table

        rip1.remove_ip_default_route_install(int_vlan="20")

        ip1.shut_int_vlan(int_vlan="20")
        ip1.no_shut_int_vlan(int_vlan="20")

        time.sleep(30)

        dict_rip_routes_1 = rip1.show_ip_route_rip()
        print(dict_rip_routes_1)

        assert "0.0.0.0" not in dict_rip_routes_1.keys()

        print("########## Removing the config #############")

        rip2.remove_default_information_originate(int_vlan="20")

        rip1.disable_rip()
        rip2.disable_rip()

        ip1.remove_int_vlan(int_vlan="20")
        ip2.remove_vlan_interfaces("20", "15")

        int1.shut_interface(interface="Ex 0/1")
        int2.shut_interfaces("Gi 0/9", "Gi 0/5")

        vl1.remove_vlan(vlan="20")
        vl2.remove_vlans("20", "15")

    def test_func_3(self):

        print("###### Test_func_3 ######")
        print("########## Verify functionality for redistribute connected #############")
        print("###### 2 DUTs ######")

        int1.no_shut_interfaces("Ex 0/1")
        int2.no_shut_interfaces("Gi 0/9", "Gi 0/5", "Gi 0/6")

        # Creating VLANs

        vl1.create_vlan(vlan="20")
        vl2.create_vlans("15", "20", "16", "100")

        # Adding the ports to the VLANs

        vl1.add_ports_to_vlan(ports="Ex 0/1", vlan="20")
        vl2.add_ports_to_vlan(ports="Gi 0/9", vlan="20")
        vl2.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
        vl2.add_ports_to_vlan(ports="Gi 0/6", vlan="16")
        vl2.add_ports_to_vlan(ports="Gi 0/5", vlan="100")

        # Adding IPs on the interfaces

        ip1.add_ip_interface(int_vlan="20", ip="20.0.0.2", mask="255.255.255.0")
        ip2.add_ip_interfaces("16", "15", "20", "100", int_vlan16=["16.0.0.1", "255.255.255.0"],
                              int_vlan15=["15.0.0.1", "255.255.255.0"], int_vlan20=["20.0.0.1", "255.255.255.0"],
                              int_vlan100=["100.0.0.1", "255.255.255.0"])

        ip1.no_shut_int_vlans("20")
        ip2.no_shut_int_vlans("20", "15", "16", "100")

        # Enabling RIP and advertising the interfaces in RIP

        rip1.enable_rip()
        rip2.enable_rip()

        rip1.advertise_network(ip_network="20.0.0.2")
        rip2.advertise_networks("20.0.0.1", "100.0.0.1")

        # Redistributing the connected networks on DUT2 and installing them on DUT1

        rip2.redistribute_connected()

        # Checking if the routes are installed

        time.sleep(30)

        dict_rip_routes_1 = rip1.show_ip_route_rip()
        # print(dict_rip_routes_1)

        assert "15.0.0.0" in dict_rip_routes_1.keys()
        assert "16.0.0.0" in dict_rip_routes_1.keys()
        assert "100.0.0.0" in dict_rip_routes_1.keys()

        # Remove redistribution on DUT2 and check if the connected routes are not anymore in the routing table of DUT1

        rip2.remove_redistribute_connected()

        ip1.shut_int_vlan(int_vlan="20")
        ip1.no_shut_int_vlan(int_vlan="20")

        time.sleep(30)

        dict_rip_routes_1 = rip1.show_ip_route_rip()
        # print(dict_rip_routes_1)

        assert "15.0.0.0" not in dict_rip_routes_1.keys()
        assert "16.0.0.0" not in dict_rip_routes_1.keys()
        assert "100.0.0.0" in dict_rip_routes_1.keys()

        print("########## Removing the config #############")

        rip1.disable_rip()
        rip2.disable_rip()

        ip1.remove_int_vlan(int_vlan="20")
        ip2.remove_vlan_interfaces("20", "15", "16", "100")

        int1.shut_interface(interface="Ex 0/1")
        int2.shut_interfaces("Gi 0/9", "Gi 0/5", "Gi 0/6")

        vl1.remove_vlan(vlan="20")
        vl2.remove_vlans("20", "15", "16", "100")

    def test_func_4(self):

        print("###### Test_func_4 ######")
        print("########## Verify functionality for redistribute static #############")
        print("###### 2 DUTs ######")

        int1.no_shut_interfaces("Ex 0/1")
        int2.no_shut_interfaces("Gi 0/9", "Gi 0/5")

        # Creating VLANs

        vl1.create_vlan(vlan="20")
        vl2.create_vlans("15", "20")

        # Adding the ports to the VLANs

        vl1.add_ports_to_vlan(ports="Ex 0/1", vlan="20")
        vl2.add_ports_to_vlan(ports="Gi 0/9", vlan="20")
        vl2.add_ports_to_vlan(ports="Gi 0/5", vlan="15")

        # Adding IPs on the interfaces

        ip1.add_ip_interface(int_vlan="20", ip="20.0.0.2", mask="255.255.255.0")
        ip2.add_ip_interfaces("15", "20", int_vlan15=["15.0.0.1", "255.255.255.0"],
                              int_vlan20=["20.0.0.1", "255.255.255.0"])

        ip1.no_shut_int_vlans("20")
        ip2.no_shut_int_vlans("20", "15")

        # Enabling RIP and advertising the interfaces in RIP

        rip1.enable_rip()
        rip2.enable_rip()

        rip1.advertise_network(ip_network="20.0.0.2")
        rip2.advertise_networks("20.0.0.1", "15.0.0.1")

        # Creating a static route

        ip2.add_static_route(network_dest="100.0.0.0", mask_dest="255.255.0.0", next_hop="15.0.0.100")

        # Redistributing the static network on DUT2 and installing it on DUT1

        rip2.redistribute_static()

        # Checking if the routes are installed

        time.sleep(30)

        dict_rip_routes_1 = rip1.show_ip_route_rip()
        # print(dict_rip_routes_1)

        assert "15.0.0.0" in dict_rip_routes_1.keys()
        assert "100.0.0.0" in dict_rip_routes_1.keys()

        # Remove the static route on DUT2 and check if the route is not anymore in the routing table of DUT1

        rip2.remove_redistribute_static()

        ip1.shut_int_vlan(int_vlan="20")
        ip1.no_shut_int_vlan(int_vlan="20")

        time.sleep(30)

        dict_rip_routes_1 = rip1.show_ip_route_rip()
        # print(dict_rip_routes_1)

        assert "15.0.0.0" in dict_rip_routes_1.keys()
        assert "100.0.0.0" not in dict_rip_routes_1.keys()

        print("########## Removing the config #############")

        rip1.disable_rip()
        rip2.disable_rip()

        ip2.remove_static_route(network_dest="100.0.0.0", mask_dest="255.255.0.0", next_hop="15.0.0.100")

        ip1.remove_int_vlan(int_vlan="20")
        ip2.remove_vlan_interfaces("20", "15")

        int1.shut_interface(interface="Ex 0/1")
        int2.shut_interfaces("Gi 0/9", "Gi 0/5")

        vl1.remove_vlan(vlan="20")
        vl2.remove_vlans("20", "15")

    def test_func_5(self):

        print("###### Test_func_5 ######")
        print("########## Verify auto-summary #############")
        print("###### 2 DUTs ######")

        int1.no_shut_interfaces("Ex 0/1")
        int2.no_shut_interfaces("Gi 0/9", "Gi 0/5")

        # Creating VLANs

        vl1.create_vlan(vlan="20")
        vl2.create_vlans("15", "20")

        # Adding the ports to the VLANs

        vl1.add_ports_to_vlan(ports="Ex 0/1", vlan="20")
        vl2.add_ports_to_vlan(ports="Gi 0/9", vlan="20")
        vl2.add_ports_to_vlan(ports="Gi 0/5", vlan="15")

        # Adding IPs on the interfaces

        ip1.add_ip_interface(int_vlan="20", ip="20.0.0.2", mask="255.255.255.0")
        ip2.add_ip_interfaces("15", "20", int_vlan15=["15.0.0.1", "255.255.255.0"],
                              int_vlan20=["20.0.0.1", "255.255.255.0"])

        ip1.no_shut_int_vlans("20")
        ip2.no_shut_int_vlans("20", "15")

        # Enabling RIP and advertising the interfaces into RIP

        rip1.enable_rip()
        rip2.enable_rip()

        rip1.advertise_network(ip_network="20.0.0.2")
        rip2.advertise_networks("20.0.0.1", "15.0.0.1")

        # Creating a static route

        ip2.add_static_route(network_dest="88.88.88.0", mask_dest="255.255.255.128", next_hop="15.0.0.100")

        # Disabling no-autosummary on DUT2 so it will redistribute classless subnets

        rip2.remove_auto_summary()

        # Redistributing the static network on DUT2 and installing it on DUT1

        rip2.redistribute_static()

        # Checking if the routes are installed and that are classless

        time.sleep(30)

        dict_rip_routes_1 = rip1.show_ip_route_rip()
        # print(dict_rip_routes_1)

        assert "88.88.88.0" in dict_rip_routes_1.keys() and dict_rip_routes_1["88.88.88.0"]["Mask"] == "25"

        # Enable the auto-summary on DUT2 and check if the route is classfull and is present in the routing table of DUT1

        rip2.auto_summary()

        ip1.shut_int_vlan(int_vlan="20")
        ip1.no_shut_int_vlan(int_vlan="20")

        time.sleep(45)

        dict_rip_routes_1 = rip1.show_ip_route_rip()
        # print(dict_rip_routes_1)

        assert "88.88.88.0" not in dict_rip_routes_1.keys()
        assert "88.0.0.0" in dict_rip_routes_1.keys()

        print("########## Removing the config #############")

        rip1.disable_rip()
        rip2.disable_rip()

        ip2.remove_static_route(network_dest="88.88.88.0", mask_dest="255.255.255.128", next_hop="15.0.0.100")

        ip1.remove_int_vlan(int_vlan="20")
        ip2.remove_vlan_interfaces("20", "15")

        int1.shut_interface(interface="Ex 0/1")
        int2.shut_interfaces("Gi 0/9", "Gi 0/5")

        vl1.remove_vlan(vlan="20")
        vl2.remove_vlans("20", "15")

    def test_func_6(self):

        print("###### Test_func_6 ######")
        print("########## Verify that administrative RIP distance can be changed to other value #############")
        print("###### 2 DUTs ######")

        int1.no_shut_interfaces("Ex 0/1")
        int2.no_shut_interfaces("Gi 0/9", "Gi 0/5")

        # Creating VLANs

        vl1.create_vlan(vlan="20")
        vl2.create_vlans("15", "20")

        # Adding the ports to the VLANs

        vl1.add_ports_to_vlan(ports="Ex 0/1", vlan="20")
        vl2.add_ports_to_vlan(ports="Gi 0/9", vlan="20")
        vl2.add_ports_to_vlan(ports="Gi 0/5", vlan="15")

        # Adding IPs on the interfaces

        ip1.add_ip_interface(int_vlan="20", ip="20.0.0.2", mask="255.255.255.0")
        ip2.add_ip_interfaces("15", "20", int_vlan15=["15.0.0.1", "255.255.255.0"],
                              int_vlan20=["20.0.0.1", "255.255.255.0"])

        ip1.no_shut_int_vlans("20")
        ip2.no_shut_int_vlans("20", "15")

        # Enabling RIP and advertising the interfaces into RIP

        rip1.enable_rip()
        rip2.enable_rip()

        rip1.advertise_network(ip_network="20.0.0.2")
        rip2.advertise_networks("20.0.0.1", "15.0.0.1")

        # Enabling OSPF and advertising the interfaces into OSPF

        ospf1.enable_ospf()
        ospf2.enable_ospf()

        ospf1.advertise_network(ip_network="20.0.0.2", area="0.0.0.0")
        ospf2.advertise_network(ip_network="15.0.0.1", area="0.0.0.0")
        ospf2.advertise_network(ip_network="20.0.0.1", area="0.0.0.0")

        # Disabling no-autosummary on DUT2 so it will redistribute classless subnets

        rip2.remove_auto_summary()

        # Configuring the Distance on DUT1 so to routes are learned using RIP

        rip1.add_distance(distance="99")

        # Checking if the routes are installed and that are learned via RIP

        time.sleep(30)

        ip_route, networks, networks_connected, dict_of_networks = ip1.show_ip_route()
        print(dict_of_networks)

        assert "15.0.0.0" in dict_of_networks and dict_of_networks["15.0.0.0"]["Protocol"] == "R"

        # Remove the distance and check that the routes are learned via OSPF

        rip1.remove_distance()

        ip1.shut_int_vlan(int_vlan="20")
        ip1.no_shut_int_vlan(int_vlan="20")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = ip1.show_ip_route()
        print(dict_of_networks)

        assert "15.0.0.0" in dict_of_networks and dict_of_networks["15.0.0.0"]["Protocol"] == "O"

        print("########## Removing the config #############")

        rip1.disable_rip()
        rip2.disable_rip()

        ospf1.remove_network(ip_network="20.0.0.2", area="0.0.0.0")
        ospf2.remove_network(ip_network="15.0.0.1", area="0.0.0.0")
        ospf2.remove_network(ip_network="20.0.0.1", area="0.0.0.0")

        ospf1.disable_ospf()
        ospf2.disable_ospf()

        ip1.remove_int_vlan(int_vlan="20")
        ip2.remove_vlan_interfaces("20", "15")

        int1.shut_interface(interface="Ex 0/1")
        int2.shut_interfaces("Gi 0/9", "Gi 0/5")

        vl1.remove_vlan(vlan="20")
        vl2.remove_vlans("20", "15")

    def test_func_7(self):

        print("###### Test_func_7 ######")
        print("########## Verify functionality for passive-interface #############")
        print("###### 2 DUTs ######")

        int1.no_shut_interfaces("Ex 0/1")
        int2.no_shut_interfaces("Gi 0/9", "Gi 0/5")

        # Creating VLANs

        vl1.create_vlan(vlan="20")
        vl2.create_vlans("15", "20")

        # Adding the ports to the VLANs

        vl1.add_ports_to_vlan(ports="Ex 0/1", vlan="20")
        vl2.add_ports_to_vlan(ports="Gi 0/9", vlan="20")
        vl2.add_ports_to_vlan(ports="Gi 0/5", vlan="15")

        # Adding IPs on the interfaces

        ip1.add_ip_interface(int_vlan="20", ip="20.0.0.2", mask="255.255.255.0")
        ip2.add_ip_interfaces("15", "20", int_vlan15=["15.0.0.1", "255.255.255.0"],
                              int_vlan20=["20.0.0.1", "255.255.255.0"])

        ip1.no_shut_int_vlans("20")
        ip2.no_shut_int_vlans("20", "15")

        # Enabling RIP and advertising the interfaces into RIP

        rip1.enable_rip()
        rip2.enable_rip()

        rip1.advertise_network(ip_network="20.0.0.2")
        rip2.advertise_networks("20.0.0.1", "15.0.0.1")

        # Enable passive interface on the int VLAN between the DUTs and shut/no shut the int VLAN between them

        rip2.add_passive_interface(vlan="20")

        ip1.shut_int_vlan(int_vlan="20")
        ip1.no_shut_int_vlan(int_vlan="20")

        # Checking if the routes are not installed on DUT1 and that are classless

        time.sleep(45)

        dict_rip_routes_1 = rip1.show_ip_route_rip()
        # print(dict_rip_routes_1)

        assert "15.0.0.0" not in dict_rip_routes_1.keys()

        # Disable the passive interface and check that the routes are installed on DUT1

        rip2.remove_passive_interface(vlan="20")

        ip1.shut_int_vlan(int_vlan="20")
        ip1.no_shut_int_vlan(int_vlan="20")

        time.sleep(45)

        dict_rip_routes_1 = rip1.show_ip_route_rip()
        # print(dict_rip_routes_1)

        assert "15.0.0.0" in dict_rip_routes_1.keys()

        print("########## Removing the config #############")

        rip1.disable_rip()
        rip2.disable_rip()

        ip1.remove_int_vlan(int_vlan="20")
        ip2.remove_vlan_interfaces("20", "15")

        int1.shut_interface(interface="Ex 0/1")
        int2.shut_interfaces("Gi 0/9", "Gi 0/5")

        vl1.remove_vlan(vlan="20")
        vl2.remove_vlans("20", "15")

    def test_func_8(self):

        print("###### Test_func_8 ######")
        print("########## Verify functionality for default-metric #############")
        print("###### 2 DUTs ######")

        default_metric = 3
        metric = 5
        metric_high = 16

        int1.no_shut_interfaces("Ex 0/1")
        int2.no_shut_interfaces("Gi 0/9", "Gi 0/5")

        # Creating VLANs

        vl1.create_vlan(vlan="20")
        vl2.create_vlans("15", "20")

        # Adding the ports to the VLANs

        vl1.add_ports_to_vlan(ports="Ex 0/1", vlan="20")
        vl2.add_ports_to_vlan(ports="Gi 0/9", vlan="20")
        vl2.add_ports_to_vlan(ports="Gi 0/5", vlan="15")

        # Adding IPs on the interfaces

        ip1.add_ip_interface(int_vlan="20", ip="20.0.0.2", mask="255.255.255.0")
        ip2.add_ip_interfaces("15", "20", int_vlan15=["15.0.0.1", "255.255.255.0"],
                              int_vlan20=["20.0.0.1", "255.255.255.0"])

        ip1.no_shut_int_vlans("20")
        ip2.no_shut_int_vlans("20", "15")

        # Enabling RIP and advertising the interfaces into RIP

        rip1.enable_rip()
        rip2.enable_rip()

        rip1.advertise_network(ip_network="20.0.0.2")
        rip2.advertise_networks("20.0.0.1")

        # Changing the metric for redistributed routes

        rip2.default_metric(metric=metric)

        # Configuring static routes, redistribute static and redistribute connected on DUT2 towards DUT1

        ip2.add_static_route(network_dest="88.0.0.0", mask_dest="255.255.255.0", next_hop="15.0.0.100")

        rip2.redistribute_static()
        rip2.redistribute_connected()

        # Checking if the routes are installed and that are learned via RIP

        time.sleep(30)

        ip_route, networks, networks_connected, dict_of_networks = ip1.show_ip_route()
        print(dict_of_networks)

        assert "15.0.0.0" in dict_of_networks and dict_of_networks["15.0.0.0"]["Metric"] == str(metric + 1)
        assert "88.0.0.0" in dict_of_networks and dict_of_networks["88.0.0.0"]["Metric"] == str(metric + 1)

        # Changing the metric for redistributed routes

        rip2.default_metric(metric=metric_high)

        # Remove the redistribution of static/connected and add them back

        rip2.remove_redistribute_static()
        rip2.remove_redistribute_connected()

        rip2.redistribute_static()
        rip2.redistribute_connected()

        ip1.shut_int_vlan(int_vlan="20")
        ip1.no_shut_int_vlan(int_vlan="20")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = ip1.show_ip_route()
        print(dict_of_networks)

        # Checking that the routes are not installed because they have a metric higher than 15

        assert "15.0.0.0" not in dict_of_networks
        assert "88.0.0.0" not in dict_of_networks

        # Remove the default metric

        rip2.remove_default_metric()

        # Remove the redistribution of static/connected and add them back

        rip2.remove_redistribute_static()
        rip2.remove_redistribute_connected()

        rip2.redistribute_static()
        rip2.redistribute_connected()

        ip1.shut_int_vlan(int_vlan="20")
        ip1.no_shut_int_vlan(int_vlan="20")

        time.sleep(45)

        ip_route, networks, networks_connected, dict_of_networks = ip1.show_ip_route()
        print(dict_of_networks)

        assert "15.0.0.0" in dict_of_networks and dict_of_networks["15.0.0.0"]["Metric"] == str(default_metric + 1)
        assert "88.0.0.0" in dict_of_networks and dict_of_networks["88.0.0.0"]["Metric"] == str(default_metric + 1)

        print("########## Removing the config #############")

        rip1.disable_rip()
        rip2.disable_rip()

        ip1.remove_int_vlan(int_vlan="20")
        ip2.remove_vlan_interfaces("20", "15")

        ip2.remove_static_route(network_dest="88.0.0.0", mask_dest="255.255.255.0", next_hop="15.0.0.100")

        int1.shut_interface(interface="Ex 0/1")
        int2.shut_interfaces("Gi 0/9", "Gi 0/5")

        vl1.remove_vlan(vlan="20")
        vl2.remove_vlans("20", "15")

    def test_func_9(self):

        print("###### Test_func_9 ######")
        print("########## Verify that the text mode authentication option works as expected. #############")
        print("###### 2 DUTs ######")

        int1.no_shut_interfaces("Ex 0/1")
        int2.no_shut_interfaces("Gi 0/9", "Gi 0/5")

        # Creating VLANs

        vl1.create_vlan(vlan="20")
        vl2.create_vlans("15", "20")

        # Adding the ports to the VLANs

        vl1.add_ports_to_vlan(ports="Ex 0/1", vlan="20")
        vl2.add_ports_to_vlan(ports="Gi 0/9", vlan="20")
        vl2.add_ports_to_vlan(ports="Gi 0/5", vlan="15")

        # Adding IPs on the interfaces

        ip1.add_ip_interface(int_vlan="20", ip="20.0.0.2", mask="255.255.255.0")
        ip2.add_ip_interfaces("15", "20", int_vlan15=["15.0.0.1", "255.255.255.0"],
                              int_vlan20=["20.0.0.1", "255.255.255.0"])

        ip1.no_shut_int_vlans("20")
        ip2.no_shut_int_vlans("20", "15")

        # Enabling RIP and advertising the interfaces into RIP

        rip1.enable_rip()
        rip2.enable_rip()

        rip1.advertise_network(ip_network="20.0.0.2")
        rip2.advertise_networks("20.0.0.1", "15.0.0.1")

        # Enable authentication key on the int VLAN between the DUTs on DUT2 and shut/no shut the int VLAN between them

        rip2.add_ip_rip_authentication_mode(int_vlan="20", mode="text", key_chain="12345")

        ip1.shut_int_vlan(int_vlan="20")
        ip1.no_shut_int_vlan(int_vlan="20")

        # Checking if the routes are not installed

        time.sleep(45)

        dict_rip_routes_1 = rip1.show_ip_route_rip()
        # print(dict_rip_routes_1)
        dict_of_int_vlans_authentication_2 = rip2.show_ip_rip_authentication()
        dict_of_int_vlans_authentication_1 = rip1.show_ip_rip_authentication()
        print(dict_of_int_vlans_authentication_2)
        print(dict_of_int_vlans_authentication_1)

        assert "15.0.0.0" not in dict_rip_routes_1.keys()
        assert "20" in dict_of_int_vlans_authentication_2 and dict_of_int_vlans_authentication_2["20"]["Authentication Type"] == "simple text"
        assert "20" in dict_of_int_vlans_authentication_1 and dict_of_int_vlans_authentication_1["20"]["Authentication Type"] == "none"

        # Enable the same authentication key on DUT1 and check that routes are installed

        rip1.add_ip_rip_authentication_mode(int_vlan="20", mode="text", key_chain="12345")

        ip1.shut_int_vlan(int_vlan="20")
        ip1.no_shut_int_vlan(int_vlan="20")

        time.sleep(30)

        dict_rip_routes_1 = rip1.show_ip_route_rip()
        # print(dict_rip_routes_1)
        dict_of_int_vlans_authentication_2 = rip2.show_ip_rip_authentication()
        dict_of_int_vlans_authentication_1 = rip1.show_ip_rip_authentication()
        print(dict_of_int_vlans_authentication_2)
        print(dict_of_int_vlans_authentication_1)

        assert "15.0.0.0" in dict_rip_routes_1.keys()
        assert "20" in dict_of_int_vlans_authentication_2 and dict_of_int_vlans_authentication_2["20"]["Authentication Type"] == "simple text"
        assert "20" in dict_of_int_vlans_authentication_1 and dict_of_int_vlans_authentication_1["20"]["Authentication Type"] == "simple text"

        # Disable the authentication and check that the routes are installed on DUT1

        rip1.remove_ip_rip_authentication_mode(int_vlan="20")
        rip2.remove_ip_rip_authentication_mode(int_vlan="20")

        ip1.shut_int_vlan(int_vlan="20")
        ip1.no_shut_int_vlan(int_vlan="20")

        time.sleep(35)

        dict_rip_routes_1 = rip1.show_ip_route_rip()
        # print(dict_rip_routes_1)
        dict_of_int_vlans_authentication_2 = rip2.show_ip_rip_authentication()
        dict_of_int_vlans_authentication_1 = rip1.show_ip_rip_authentication()
        print(dict_of_int_vlans_authentication_2)
        print(dict_of_int_vlans_authentication_1)

        assert "15.0.0.0" in dict_rip_routes_1.keys()
        assert "20" in dict_of_int_vlans_authentication_2 and dict_of_int_vlans_authentication_2["20"]["Authentication Type"] == "none"
        assert "20" in dict_of_int_vlans_authentication_1 and dict_of_int_vlans_authentication_1["20"]["Authentication Type"] == "none"

        print("########## Removing the config #############")

        rip1.disable_rip()
        rip2.disable_rip()

        ip1.remove_int_vlan(int_vlan="20")
        ip2.remove_vlan_interfaces("20", "15")

        int1.shut_interface(interface="Ex 0/1")
        int2.shut_interfaces("Gi 0/9", "Gi 0/5")

        vl1.remove_vlan(vlan="20")
        vl2.remove_vlans("20", "15")

    def test_func_10(self):

        print("###### Test_func_10 ######")
        print("########## Verify that md5 Authentication with the authentication type for crypto authentication md5 | sha-1 | sha-256 works as expected.#############")
        print("###### 2 DUTs ######")

        int1.no_shut_interfaces("Ex 0/1")
        int2.no_shut_interfaces("Gi 0/9", "Gi 0/5")

        # Creating VLANs

        vl1.create_vlan(vlan="20")
        vl2.create_vlans("15", "20")

        # Adding the ports to the VLANs

        vl1.add_ports_to_vlan(ports="Ex 0/1", vlan="20")
        vl2.add_ports_to_vlan(ports="Gi 0/9", vlan="20")
        vl2.add_ports_to_vlan(ports="Gi 0/5", vlan="15")

        # Adding IPs on the interfaces

        ip1.add_ip_interface(int_vlan="20", ip="20.0.0.2", mask="255.255.255.0")
        ip2.add_ip_interfaces("15", "20", int_vlan15=["15.0.0.1", "255.255.255.0"],
                              int_vlan20=["20.0.0.1", "255.255.255.0"])

        ip1.no_shut_int_vlans("20")
        ip2.no_shut_int_vlans("20", "15")

        # Enabling RIP and advertising the interfaces into RIP

        rip1.enable_rip()
        rip2.enable_rip()

        rip1.advertise_network(ip_network="20.0.0.2")
        rip2.advertise_networks("20.0.0.1", "15.0.0.1")

        # Enable authentication key on the int VLAN between the DUTs on DUT2 and shut/no shut the int VLAN between them

        rip2.add_ip_rip_authentication_mode(int_vlan="20", mode="md5", key_chain="12345")
        rip2.add_ip_rip_auth_type_mode(int_vlan="20", mode="md5", key_id="1", key="12345")

        ip1.shut_int_vlan(int_vlan="20")
        ip1.no_shut_int_vlan(int_vlan="20")

        # Checking if the routes are not installed

        time.sleep(45)

        dict_rip_routes_1 = rip1.show_ip_route_rip()
        # print(dict_rip_routes_1)
        dict_of_int_vlans_authentication_2 = rip2.show_ip_rip_authentication()
        dict_of_int_vlans_authentication_1 = rip1.show_ip_rip_authentication()
        print(dict_of_int_vlans_authentication_2)
        print(dict_of_int_vlans_authentication_1)

        assert "15.0.0.0" not in dict_rip_routes_1.keys()
        assert "20" in dict_of_int_vlans_authentication_2 and dict_of_int_vlans_authentication_2["20"]["Authentication Type"] == "md5"
        assert "20" in dict_of_int_vlans_authentication_1 and dict_of_int_vlans_authentication_1["20"]["Authentication Type"] == "none"

        # Enable the same authentication key on DUT1 and check that routes are installed

        rip1.add_ip_rip_authentication_mode(int_vlan="20", mode="md5", key_chain="12345")
        rip1.add_ip_rip_auth_type_mode(int_vlan="20", mode="md5", key_id="1", key="12345")

        ip1.shut_int_vlan(int_vlan="20")
        ip1.no_shut_int_vlan(int_vlan="20")

        time.sleep(30)

        dict_rip_routes_1 = rip1.show_ip_route_rip()
        # print(dict_rip_routes_1)
        dict_of_int_vlans_authentication_2 = rip2.show_ip_rip_authentication()
        dict_of_int_vlans_authentication_1 = rip1.show_ip_rip_authentication()
        print(dict_of_int_vlans_authentication_2)
        print(dict_of_int_vlans_authentication_1)

        assert "15.0.0.0" in dict_rip_routes_1.keys()
        assert "20" in dict_of_int_vlans_authentication_2 and dict_of_int_vlans_authentication_2["20"]["Authentication Type"] == "md5"
        assert "20" in dict_of_int_vlans_authentication_1 and dict_of_int_vlans_authentication_1["20"]["Authentication Type"] == "md5"
        assert dict_of_int_vlans_authentication_2["20"]['Authentication KeyId in use'] == dict_of_int_vlans_authentication_1["20"]['Authentication KeyId in use'] == "1"

        # Disable the authentication and check that the routes are installed on DUT1

        rip1.remove_ip_rip_authentication_mode(int_vlan="20")
        rip2.remove_ip_rip_authentication_mode(int_vlan="20")

        ip1.shut_int_vlan(int_vlan="20")
        ip1.no_shut_int_vlan(int_vlan="20")

        time.sleep(35)

        dict_rip_routes_1 = rip1.show_ip_route_rip()
        # print(dict_rip_routes_1)
        dict_of_int_vlans_authentication_2 = rip2.show_ip_rip_authentication()
        dict_of_int_vlans_authentication_1 = rip1.show_ip_rip_authentication()
        print(dict_of_int_vlans_authentication_2)
        print(dict_of_int_vlans_authentication_1)

        assert "15.0.0.0" in dict_rip_routes_1.keys()
        assert "20" in dict_of_int_vlans_authentication_2 and dict_of_int_vlans_authentication_2["20"]["Authentication Type"] == "none"
        assert "20" in dict_of_int_vlans_authentication_1 and dict_of_int_vlans_authentication_1["20"]["Authentication Type"] == "none"

        print("########## Removing the config #############")

        rip1.disable_rip()
        rip2.disable_rip()

        ip1.remove_int_vlan(int_vlan="20")
        ip2.remove_vlan_interfaces("20", "15")

        int1.shut_interface(interface="Ex 0/1")
        int2.shut_interfaces("Gi 0/9", "Gi 0/5")

        vl1.remove_vlan(vlan="20")
        vl2.remove_vlans("20", "15")

    def test_func_11(self):

        print("###### Test_func_11 ######")
        print("########## Verify that sha-1 Authentication with the authentication type for crypto authentication sha-1 works as expected.#############")
        print("###### 2 DUTs ######")

        int1.no_shut_interfaces("Ex 0/1")
        int2.no_shut_interfaces("Gi 0/9", "Gi 0/5")

        # Creating VLANs

        vl1.create_vlan(vlan="20")
        vl2.create_vlans("15", "20")

        # Adding the ports to the VLANs

        vl1.add_ports_to_vlan(ports="Ex 0/1", vlan="20")
        vl2.add_ports_to_vlan(ports="Gi 0/9", vlan="20")
        vl2.add_ports_to_vlan(ports="Gi 0/5", vlan="15")

        # Adding IPs on the interfaces

        ip1.add_ip_interface(int_vlan="20", ip="20.0.0.2", mask="255.255.255.0")
        ip2.add_ip_interfaces("15", "20", int_vlan15=["15.0.0.1", "255.255.255.0"],
                              int_vlan20=["20.0.0.1", "255.255.255.0"])

        ip1.no_shut_int_vlans("20")
        ip2.no_shut_int_vlans("20", "15")

        # Enabling RIP and advertising the interfaces into RIP

        rip1.enable_rip()
        rip2.enable_rip()

        rip1.advertise_network(ip_network="20.0.0.2")
        rip2.advertise_networks("20.0.0.1", "15.0.0.1")

        # Enable authentication key on the int VLAN between the DUTs on DUT2 and shut/no shut the int VLAN between them

        rip2.add_ip_rip_auth_type_mode(int_vlan="20", mode="sha-1", key_id="1", key="12345")

        ip1.shut_int_vlan(int_vlan="20")
        ip1.no_shut_int_vlan(int_vlan="20")

        # Checking if the routes are not installed

        time.sleep(45)

        dict_rip_routes_1 = rip1.show_ip_route_rip()
        # print(dict_rip_routes_1)
        dict_of_int_vlans_authentication_2 = rip2.show_ip_rip_authentication()
        dict_of_int_vlans_authentication_1 = rip1.show_ip_rip_authentication()
        print(dict_of_int_vlans_authentication_2)
        print(dict_of_int_vlans_authentication_1)

        assert "15.0.0.0" not in dict_rip_routes_1.keys()
        assert "20" in dict_of_int_vlans_authentication_2 and dict_of_int_vlans_authentication_2["20"]["Authentication Type"] == "sha1"
        assert "20" in dict_of_int_vlans_authentication_1 and dict_of_int_vlans_authentication_1["20"]["Authentication Type"] == "none"

        # Enable the same authentication key on DUT1 and check that routes are installed

        rip1.add_ip_rip_auth_type_mode(int_vlan="20", mode="sha-1", key_id="1", key="12345")

        ip1.shut_int_vlan(int_vlan="20")
        ip1.no_shut_int_vlan(int_vlan="20")

        time.sleep(30)

        dict_rip_routes_1 = rip1.show_ip_route_rip()
        # print(dict_rip_routes_1)
        dict_of_int_vlans_authentication_2 = rip2.show_ip_rip_authentication()
        dict_of_int_vlans_authentication_1 = rip1.show_ip_rip_authentication()
        print(dict_of_int_vlans_authentication_2)
        print(dict_of_int_vlans_authentication_1)

        assert "15.0.0.0" in dict_rip_routes_1.keys()
        assert "20" in dict_of_int_vlans_authentication_2 and dict_of_int_vlans_authentication_2["20"]["Authentication Type"] == "sha1"
        assert "20" in dict_of_int_vlans_authentication_1 and dict_of_int_vlans_authentication_1["20"]["Authentication Type"] == "sha1"
        assert dict_of_int_vlans_authentication_2["20"]['Authentication KeyId in use'] == dict_of_int_vlans_authentication_1["20"]['Authentication KeyId in use'] == "1"

        # Disable the authentication and check that the routes are installed on DUT1

        rip1.remove_ip_rip_authentication_mode(int_vlan="20")
        rip2.remove_ip_rip_authentication_mode(int_vlan="20")

        ip1.shut_int_vlan(int_vlan="20")
        ip1.no_shut_int_vlan(int_vlan="20")

        time.sleep(35)

        dict_rip_routes_1 = rip1.show_ip_route_rip()
        # print(dict_rip_routes_1)
        dict_of_int_vlans_authentication_2 = rip2.show_ip_rip_authentication()
        dict_of_int_vlans_authentication_1 = rip1.show_ip_rip_authentication()
        print(dict_of_int_vlans_authentication_2)
        print(dict_of_int_vlans_authentication_1)

        assert "15.0.0.0" in dict_rip_routes_1.keys()
        assert "20" in dict_of_int_vlans_authentication_2 and dict_of_int_vlans_authentication_2["20"]["Authentication Type"] == "none"
        assert "20" in dict_of_int_vlans_authentication_1 and dict_of_int_vlans_authentication_1["20"]["Authentication Type"] == "none"

        print("########## Removing the config #############")

        rip1.disable_rip()
        rip2.disable_rip()

        ip1.remove_int_vlan(int_vlan="20")
        ip2.remove_vlan_interfaces("20", "15")

        int1.shut_interface(interface="Ex 0/1")
        int2.shut_interfaces("Gi 0/9", "Gi 0/5")

        vl1.remove_vlan(vlan="20")
        vl2.remove_vlans("20", "15")

    def test_func_12(self):

        print("###### Test_func_12 ######")
        print("########## Verify that sha-256 Authentication with the authentication type for crypto authentication sha-256 works as expected.#############")
        print("###### 2 DUTs ######")

        int1.no_shut_interfaces("Ex 0/1")
        int2.no_shut_interfaces("Gi 0/9", "Gi 0/5")

        # Creating VLANs

        vl1.create_vlan(vlan="20")
        vl2.create_vlans("15", "20")

        # Adding the ports to the VLANs

        vl1.add_ports_to_vlan(ports="Ex 0/1", vlan="20")
        vl2.add_ports_to_vlan(ports="Gi 0/9", vlan="20")
        vl2.add_ports_to_vlan(ports="Gi 0/5", vlan="15")

        # Adding IPs on the interfaces

        ip1.add_ip_interface(int_vlan="20", ip="20.0.0.2", mask="255.255.255.0")
        ip2.add_ip_interfaces("15", "20", int_vlan15=["15.0.0.1", "255.255.255.0"],
                              int_vlan20=["20.0.0.1", "255.255.255.0"])

        ip1.no_shut_int_vlans("20")
        ip2.no_shut_int_vlans("20", "15")

        # Enabling RIP and advertising the interfaces into RIP

        rip1.enable_rip()
        rip2.enable_rip()

        rip1.advertise_network(ip_network="20.0.0.2")
        rip2.advertise_networks("20.0.0.1", "15.0.0.1")

        # Enable authentication key on the int VLAN between the DUTs on DUT2 and shut/no shut the int VLAN between them

        rip2.add_ip_rip_auth_type_mode(int_vlan="20", mode="sha-256", key_id="1", key="12345")

        ip1.shut_int_vlan(int_vlan="20")
        ip1.no_shut_int_vlan(int_vlan="20")

        # Checking if the routes are not installed

        time.sleep(45)

        dict_rip_routes_1 = rip1.show_ip_route_rip()
        # print(dict_rip_routes_1)
        dict_of_int_vlans_authentication_2 = rip2.show_ip_rip_authentication()
        dict_of_int_vlans_authentication_1 = rip1.show_ip_rip_authentication()
        print(dict_of_int_vlans_authentication_2)
        print(dict_of_int_vlans_authentication_1)

        assert "15.0.0.0" not in dict_rip_routes_1.keys()
        assert "20" in dict_of_int_vlans_authentication_2 and dict_of_int_vlans_authentication_2["20"]["Authentication Type"] == "sha256"
        assert "20" in dict_of_int_vlans_authentication_1 and dict_of_int_vlans_authentication_1["20"]["Authentication Type"] == "none"

        # Enable the same authentication key on DUT1 and check that routes are installed

        rip1.add_ip_rip_auth_type_mode(int_vlan="20", mode="sha-256", key_id="1", key="12345")

        ip1.shut_int_vlan(int_vlan="20")
        ip1.no_shut_int_vlan(int_vlan="20")

        time.sleep(30)

        dict_rip_routes_1 = rip1.show_ip_route_rip()
        # print(dict_rip_routes_1)
        dict_of_int_vlans_authentication_2 = rip2.show_ip_rip_authentication()
        dict_of_int_vlans_authentication_1 = rip1.show_ip_rip_authentication()
        print(dict_of_int_vlans_authentication_2)
        print(dict_of_int_vlans_authentication_1)

        assert "15.0.0.0" in dict_rip_routes_1.keys()
        assert "20" in dict_of_int_vlans_authentication_2 and dict_of_int_vlans_authentication_2["20"]["Authentication Type"] == "sha256"
        assert "20" in dict_of_int_vlans_authentication_1 and dict_of_int_vlans_authentication_1["20"]["Authentication Type"] == "sha256"
        assert dict_of_int_vlans_authentication_2["20"]['Authentication KeyId in use'] == dict_of_int_vlans_authentication_1["20"]['Authentication KeyId in use'] == "1"

        # Disable the authentication and check that the routes are installed on DUT1

        rip1.remove_ip_rip_authentication_mode(int_vlan="20")
        rip2.remove_ip_rip_authentication_mode(int_vlan="20")

        ip1.shut_int_vlan(int_vlan="20")
        ip1.no_shut_int_vlan(int_vlan="20")

        time.sleep(35)

        dict_rip_routes_1 = rip1.show_ip_route_rip()
        # print(dict_rip_routes_1)
        dict_of_int_vlans_authentication_2 = rip2.show_ip_rip_authentication()
        dict_of_int_vlans_authentication_1 = rip1.show_ip_rip_authentication()
        print(dict_of_int_vlans_authentication_2)
        print(dict_of_int_vlans_authentication_1)

        assert "15.0.0.0" in dict_rip_routes_1.keys()
        assert "20" in dict_of_int_vlans_authentication_2 and dict_of_int_vlans_authentication_2["20"]["Authentication Type"] == "none"
        assert "20" in dict_of_int_vlans_authentication_1 and dict_of_int_vlans_authentication_1["20"]["Authentication Type"] == "none"

        print("########## Removing the config #############")

        rip1.disable_rip()
        rip2.disable_rip()

        ip1.remove_int_vlan(int_vlan="20")
        ip2.remove_vlan_interfaces("20", "15")

        int1.shut_interface(interface="Ex 0/1")
        int2.shut_interfaces("Gi 0/9", "Gi 0/5")

        vl1.remove_vlan(vlan="20")
        vl2.remove_vlans("20", "15")

    def test_func_13(self):

        print("###### Test_func_13 ######")
        print("########## Verify that multiple authentication keys can be configured on a DUT.#############")
        print("###### 2 DUTs ######")

        int1.no_shut_interfaces("Ex 0/1")
        int2.no_shut_interfaces("Gi 0/9", "Gi 0/5")

        # Creating VLANs

        vl1.create_vlan(vlan="20")
        vl2.create_vlans("15", "20")

        # Adding the ports to the VLANs

        vl1.add_ports_to_vlan(ports="Ex 0/1", vlan="20")
        vl2.add_ports_to_vlan(ports="Gi 0/9", vlan="20")
        vl2.add_ports_to_vlan(ports="Gi 0/5", vlan="15")

        # Adding IPs on the interfaces

        ip1.add_ip_interface(int_vlan="20", ip="20.0.0.2", mask="255.255.255.0")
        ip2.add_ip_interfaces("15", "20", int_vlan15=["15.0.0.1", "255.255.255.0"],
                              int_vlan20=["20.0.0.1", "255.255.255.0"])

        ip1.no_shut_int_vlans("20")
        ip2.no_shut_int_vlans("20", "15")

        # Enabling RIP and advertising the interfaces into RIP

        rip1.enable_rip()
        rip2.enable_rip()

        rip1.advertise_network(ip_network="20.0.0.2")
        rip2.advertise_networks("20.0.0.1", "15.0.0.1")

        # Enable authentication key on the int VLAN between the DUTs on DUT2 and shut/no shut the int VLAN between them

        rip2.add_ip_rip_auth_type_mode(int_vlan="20", mode="md5", key_id="1", key="12345")
        rip2.add_ip_rip_auth_type_mode(int_vlan="20", mode="md5", key_id="2", key="123456")

        ip1.shut_int_vlan(int_vlan="20")
        ip1.no_shut_int_vlan(int_vlan="20")

        # Checking if the routes are not installed

        time.sleep(35)

        dict_rip_routes_1 = rip1.show_ip_route_rip()
        # print(dict_rip_routes_1)
        dict_of_int_vlans_authentication_2 = rip2.show_ip_rip_authentication()
        dict_of_int_vlans_authentication_1 = rip1.show_ip_rip_authentication()
        print(dict_of_int_vlans_authentication_2)
        print(dict_of_int_vlans_authentication_1)

        assert "15.0.0.0" not in dict_rip_routes_1.keys()
        assert "20" in dict_of_int_vlans_authentication_2 and dict_of_int_vlans_authentication_2["20"]["Authentication Type"] == "md5"
        assert "20" in dict_of_int_vlans_authentication_1 and dict_of_int_vlans_authentication_1["20"]["Authentication Type"] == "none"

        # Enable the same authentication key on DUT1 and check that routes are installed

        rip1.add_ip_rip_auth_type_mode(int_vlan="20", mode="md5", key_id="1", key="12345")
        rip1.add_ip_rip_auth_type_mode(int_vlan="20", mode="md5", key_id="2", key="123456")

        ip1.shut_int_vlan(int_vlan="20")
        ip1.no_shut_int_vlan(int_vlan="20")

        time.sleep(30)

        dict_rip_routes_1 = rip1.show_ip_route_rip()
        # print(dict_rip_routes_1)
        dict_of_int_vlans_authentication_2 = rip2.show_ip_rip_authentication()
        dict_of_int_vlans_authentication_1 = rip1.show_ip_rip_authentication()
        print(dict_of_int_vlans_authentication_2)
        print(dict_of_int_vlans_authentication_1)

        assert "15.0.0.0" in dict_rip_routes_1.keys()
        assert "20" in dict_of_int_vlans_authentication_2 and dict_of_int_vlans_authentication_2["20"]["Authentication Type"] == "md5"
        assert "20" in dict_of_int_vlans_authentication_1 and dict_of_int_vlans_authentication_1["20"]["Authentication Type"] == "md5"
        assert dict_of_int_vlans_authentication_2["20"]['Authentication KeyId in use'] == dict_of_int_vlans_authentication_1["20"]['Authentication KeyId in use'] == "2"

        # Disable the last authentication key on both DUTs and check that the routes are installed on DUT1 with key-id 1

        rip1.remove_ip_rip_authentication_key(int_vlan="20",key_id="2")
        rip2.remove_ip_rip_authentication_key(int_vlan="20",key_id="2")

        ip1.shut_int_vlan(int_vlan="20")
        ip1.no_shut_int_vlan(int_vlan="20")

        time.sleep(35)

        dict_rip_routes_1 = rip1.show_ip_route_rip()
        # print(dict_rip_routes_1)
        dict_of_int_vlans_authentication_2 = rip2.show_ip_rip_authentication()
        dict_of_int_vlans_authentication_1 = rip1.show_ip_rip_authentication()
        print(dict_of_int_vlans_authentication_2)
        print(dict_of_int_vlans_authentication_1)

        assert "15.0.0.0" in dict_rip_routes_1.keys()
        assert "20" in dict_of_int_vlans_authentication_2 and dict_of_int_vlans_authentication_2["20"]["Authentication Type"] == "md5"
        assert "20" in dict_of_int_vlans_authentication_1 and dict_of_int_vlans_authentication_1["20"][ "Authentication Type"] == "md5"
        assert dict_of_int_vlans_authentication_2["20"]['Authentication KeyId in use'] == dict_of_int_vlans_authentication_1["20"]['Authentication KeyId in use'] == "1"

        # Remove the authentication on both DUTs and check that the routes are installed

        rip1.remove_ip_rip_authentication_mode(int_vlan="20")
        rip2.remove_ip_rip_authentication_mode(int_vlan="20")

        ip1.shut_int_vlan(int_vlan="20")
        ip1.no_shut_int_vlan(int_vlan="20")

        time.sleep(35)

        dict_rip_routes_1 = rip1.show_ip_route_rip()
        # print(dict_rip_routes_1)
        dict_of_int_vlans_authentication_2 = rip2.show_ip_rip_authentication()
        dict_of_int_vlans_authentication_1 = rip1.show_ip_rip_authentication()
        print(dict_of_int_vlans_authentication_2)
        print(dict_of_int_vlans_authentication_1)

        assert "15.0.0.0" in dict_rip_routes_1.keys()
        assert "20" in dict_of_int_vlans_authentication_2 and dict_of_int_vlans_authentication_2["20"]["Authentication Type"] == "none"
        assert "20" in dict_of_int_vlans_authentication_1 and dict_of_int_vlans_authentication_1["20"]["Authentication Type"] == "none"

        print("########## Removing the config #############")

        rip1.disable_rip()
        rip2.disable_rip()

        ip1.remove_int_vlan(int_vlan="20")
        ip2.remove_vlan_interfaces("20", "15")

        int1.shut_interface(interface="Ex 0/1")
        int2.shut_interfaces("Gi 0/9", "Gi 0/5")

        vl1.remove_vlan(vlan="20")
        vl2.remove_vlans("20", "15")

    def test_func_14(self):

        print("###### Test_func_14 ######")
        print("########## Check if we can advertise networks into RIP and it establish connection using int vlans #############")
        print("###### 3 DUTs ######")

        # No shutting the interfaces on DUTs

        int1.no_shut_interfaces("Gi 0/3", "Gi 0/4", "Ex 0/1", "Gi 0/9")
        int2.no_shut_interfaces("Gi 0/4", "Gi 0/5", "Gi 0/6", "Gi 0/9")
        int3.no_shut_interfaces("Gi 0/4", "Gi 0/9")

        # Creating the VLAN on all DUTs

        vl1.create_vlan(vlan="30")
        vl1.create_vlan(vlan="14")
        vl1.create_vlan(vlan="11")

        vl2.create_vlan(vlan="15")
        vl2.create_vlan(vlan="14")
        vl2.create_vlan(vlan="12")

        vl3.create_vlan(vlan="11")
        vl3.create_vlan(vlan="12")
        vl3.create_vlan(vlan="20")

        # Adding the ports to the VLAN

        vl1.add_ports_to_vlan(ports="Gi 0/3", vlan="30")
        vl1.add_ports_to_vlan(ports="Gi 0/9", vlan="11")
        vl1.add_ports_to_vlan(ports="Ex 0/1", vlan="14")

        vl2.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
        vl2.add_ports_to_vlan(ports="Gi 0/9", vlan="14")
        vl2.add_ports_to_vlan(ports="Gi 0/4", vlan="12")

        vl3.add_ports_to_vlan(ports="Gi 0/4", vlan="20")
        vl3.add_ports_to_vlan(ports="Gi 0/9", vlan="11")
        vl3.add_ports_to_vlan(ports="Gi 0/4", vlan="12")

        # Create IP interfaces on all DUTs for the specific VLANs

        ip1.add_ip_interfaces("14", "30", "11", int_vlan14=["14.0.0.2", "255.255.255.0"],
                              int_vlan30=["30.0.0.1", "255.255.255.0"], int_vlan11=["11.0.0.2", "255.255.255.0"])
        ip1.no_shut_int_vlans("14", "30", "11")

        ip2.add_ip_interfaces("14", "15", "12", int_vlan14=["14.0.0.1", "255.255.255.0"],
                              int_vlan15=["15.0.0.1", "255.255.255.0"], int_vlan12=["12.0.0.1", "255.255.255.0"])
        ip2.no_shut_int_vlans("14", "15", "12")

        ip3.add_ip_interfaces("11", "12", int_vlan11=["11.0.0.1", "255.255.255.0"],
                              int_vlan12=["12.0.0.2", "255.255.255.0"])
        ip3.no_shut_int_vlans("11", "12")

        # Enable rip on all DUTs and advertise the IPs

        rip1.enable_rip()
        rip1.advertise_networks("14.0.0.2", "30.0.0.1", "11.0.0.2")

        rip2.enable_rip()
        rip2.advertise_networks("14.0.0.1", "15.0.0.1", "12.0.0.1")

        rip3.enable_rip()
        rip3.advertise_networks("11.0.0.1", "12.0.0.2")

        time.sleep(30)

        dict_rip_routes_1 = rip1.show_ip_route_rip()
        dict_rip_routes_2 = rip2.show_ip_route_rip()
        dict_rip_routes_3 = rip3.show_ip_route_rip()
        # print(dict_rip_routes_1["15.0.0.0"]["Learned From"])

        # Check if the routes are learned and instaled in RIP routes

        assert "15.0.0.0" in dict_rip_routes_1.keys() and "12.0.0.0" in dict_rip_routes_1.keys()
        assert "30.0.0.0" in dict_rip_routes_2.keys() and "11.0.0.0" in dict_rip_routes_2.keys()
        assert "30.0.0.0" in dict_rip_routes_3.keys() and "15.0.0.0" in dict_rip_routes_3.keys()

        print("########## Removing the config #############")

        rip1.disable_rip()
        rip2.disable_rip()
        rip3.disable_rip()

        ip1.remove_vlan_interfaces("14", "30", "11")
        ip2.remove_vlan_interfaces("14", "15", "12")
        ip3.remove_vlan_interfaces("11", "12")

        vl1.remove_vlans("14", "30", "11")
        vl2.remove_vlans("14", "15", "12")
        vl3.remove_vlans("11", "12")

        int1.shut_interfaces("Gi 0/3", "Gi 0/4", "Ex 0/1", "Gi 0/9")
        int2.shut_interfaces("Gi 0/4", "Gi 0/5", "Gi 0/6", "Gi 0/9")
        int3.shut_interfaces("Gi 0/4", "Gi 0/9")

    def test_func_15(self):

        # LOKI-4876 - Missing routes with Routed Ports

        print("###### Test_func_15 ######")
        print("########## Check if we can advertise networks into RIP and it establish connection using routed ports #############")
        print("###### 3 DUTs ######")

        # Creating routed ports on all DUTs

        int1.add_routed_ports("Ex 0/2","Gi 0/10")
        int2.add_routed_ports("Gi 0/3", "Gi 0/10")
        int3.add_routed_ports("Gi 0/3", "Gi 0/10")

        # No shutting the interfaces

        int1.no_shut_interfaces("Ex 0/2", "Gi 0/10")
        int2.no_shut_interfaces("Gi 0/3", "Gi 0/5", "Gi 0/10")
        int3.no_shut_interfaces("Gi 0/3", "Gi 0/10")

        # Creating the VLAN on DUT2

        vl2.create_vlan(vlan="15")

        # Adding the ports to the VLAN

        vl2.add_ports_to_vlan(ports="Gi 0/5", vlan="15")

        # Create IP Routed Ports on all DUTs

        ip1.add_ip_routed_ports("Ex 0/2", "Gi 0/10", Ex_0_2=["14.0.0.2", "255.255.255.0"], Gi_0_10=["13.0.0.2", "255.255.255.0"])

        ip2.add_ip_routed_ports("Gi 0/3", "Gi 0/10", Gi_0_3=["12.0.0.1", "255.255.255.0"], Gi_0_10=["14.0.0.1", "255.255.255.0"])
        ip2.add_ip_interface(int_vlan="15",ip="15.0.0.1",mask="255.255.255.0")
        ip2.no_shut_int_vlan(int_vlan="15")

        ip3.add_ip_routed_ports("Gi 0/3", "Gi 0/10", Gi_0_3=["12.0.0.2", "255.255.255.0"],Gi_0_10=["13.0.0.1", "255.255.255.0"])

        # Enable rip on all DUTs and advertise the IPs

        rip1.enable_rip()
        rip1.advertise_networks("13.0.0.2","14.0.0.2")

        rip2.enable_rip()
        rip2.advertise_networks("12.0.0.1", "14.0.0.1", "15.0.0.1")

        rip3.enable_rip()
        rip3.advertise_networks("12.0.0.2", "13.0.0.1")

        # time.sleep(30)

        dict_rip_routes_1 = rip1.show_ip_route_rip()
        dict_rip_routes_2 = rip2.show_ip_route_rip()
        dict_rip_routes_3 = rip3.show_ip_route_rip()

        # Check if the routes are learned and installed in RIP routes

        assert "15.0.0.0" in dict_rip_routes_1.keys() and "12.0.0.0" in dict_rip_routes_1.keys()
        assert "13.0.0.0" in dict_rip_routes_2.keys()
        assert "14.0.0.0" in dict_rip_routes_3.keys() and "15.0.0.0" in dict_rip_routes_3.keys()

        # Shut one port on DUT1 and check that RIP routes are not missing

        int1.shut_interface(interface="Ex 0/2")

        time.sleep(45)

        dict_rip_routes_1 = rip1.show_ip_route_rip()

        assert "15.0.0.0" in dict_rip_routes_1.keys() and "12.0.0.0" not in dict_rip_routes_1.keys() # Trb "in" in loc de "not in"

        # No shut the port on DUT1 and check that RIP routes are not missing

        int1.no_shut_interface(interface="Ex 0/2")

        time.sleep(45)

        dict_rip_routes_1 = rip1.show_ip_route_rip()

        assert "15.0.0.0" in dict_rip_routes_1.keys() and "12.0.0.0" in dict_rip_routes_1.keys()

        print("########## Removing the config #############")

        rip1.disable_rip()
        rip2.disable_rip()
        rip3.disable_rip()

        ip2.remove_vlan_interfaces("15")

        vl2.remove_vlans("15")

        int1.remove_routed_ports("Ex 0/2","Gi 0/10")
        int2.remove_routed_ports("Gi 0/3", "Gi 0/10")
        int3.remove_routed_ports("Gi 0/3", "Gi 0/10")

        int2.shut_interfaces("Gi 0/5")

    def test_func_16(self):

        print("###### Test_func_16 ######")
        print("########## Verify functionality for redistribute OSPF into RIP #############")
        print("###### 3 DUTs ######")

        int1.no_shut_interfaces("Ex 0/1")
        int2.no_shut_interfaces("Gi 0/9", "Gi 0/5", "Gi 0/4")
        int3.no_shut_interfaces("Gi 0/4")

        # Creating VLANs

        vl1.create_vlan(vlan="20")
        vl2.create_vlans("15", "12", "20")
        vl3.create_vlans("12", "100")

        # Adding the ports to the VLANs

        vl1.add_ports_to_vlan(ports="Ex 0/1", vlan="20")
        vl2.add_ports_to_vlan(ports="Gi 0/9", vlan="20")
        vl2.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
        vl2.add_ports_to_vlan(ports="Gi 0/4", vlan="12")
        vl3.add_ports_to_vlan(ports="Gi 0/4", vlan="12")
        vl3.add_ports_to_vlan(ports="Gi 0/4", vlan="100")

        # Adding IPs on the interfaces

        ip1.add_ip_interface(int_vlan="20", ip="20.0.0.2", mask="255.255.255.0")
        ip2.add_ip_interfaces("15", "12", "20", int_vlan15=["15.0.0.1", "255.255.255.0"],int_vlan12=["12.0.0.1", "255.255.255.0"], int_vlan20=["20.0.0.1", "255.255.255.0"])
        ip3.add_ip_interfaces("12", "100", int_vlan12=["12.0.0.2", "255.255.255.0"],int_vlan100=["100.0.0.2", "255.255.255.0"])

        ip1.no_shut_int_vlans("20")
        ip2.no_shut_int_vlans("20", "15", "12")
        ip3.no_shut_int_vlans("12", "100")

        # Enabling RIP and advertising the interfaces in RIP

        rip1.enable_rip()
        rip2.enable_rip()

        rip1.advertise_network(ip_network="20.0.0.2")
        rip2.advertise_networks("20.0.0.1", "15.0.0.1")

        # Enabling OSPF and advertising the network into OSPF

        ospf2.enable_ospf()
        ospf3.enable_ospf()

        ospf2.advertise_network(ip_network="12.0.0.1", area="0.0.0.0")
        ospf3.advertise_network(ip_network="12.0.0.2", area="0.0.0.0")
        ospf3.advertise_network(ip_network="100.0.0.2", area="0.0.0.0")

        # Redistributing OSPF into RIP on DUT2 and installing it on DUT1

        rip2.redistribute_ospf()

        # Checking if the routes are installed

        time.sleep(45)

        dict_rip_routes_1 = rip1.show_ip_route_rip()
        # print(dict_rip_routes_1)

        assert "15.0.0.0" in dict_rip_routes_1.keys()
        assert "100.0.0.0" in dict_rip_routes_1.keys()

        # Remove the ospf route on DUT2 and check if the route is not anymore in the routing table of DUT1

        rip2.remove_redistribute_ospf()

        ip1.shut_int_vlan(int_vlan="20")
        ip1.no_shut_int_vlan(int_vlan="20")

        time.sleep(30)

        dict_rip_routes_1 = rip1.show_ip_route_rip()
        # print(dict_rip_routes_1)

        if len(dict_rip_routes_1.keys()) == 0:
            assert True
        else:
            assert "15.0.0.0" in dict_rip_routes_1.keys()
            assert "100.0.0.0" not in dict_rip_routes_1.keys()

        print("########## Removing the config #############")

        rip1.disable_rip()
        rip2.disable_rip()

        ospf2.remove_network(ip_network="12.0.0.1", area="0.0.0.0")
        ospf3.remove_network(ip_network="12.0.0.2", area="0.0.0.0")
        ospf3.remove_network(ip_network="100.0.0.2", area="0.0.0.0")

        ospf2.disable_ospf()
        ospf3.disable_ospf()

        ip1.remove_int_vlan(int_vlan="20")
        ip2.remove_vlan_interfaces("20", "15", "12")
        ip3.remove_vlan_interfaces("12", "100")

        int1.shut_interface(interface="Ex 0/1")
        int2.shut_interfaces("Gi 0/9", "Gi 0/5", "Gi 0/4")
        int3.shut_interfaces("Gi 0/4")

        vl1.remove_vlan(vlan="20")
        vl2.remove_vlans("20", "15", "12")
        vl3.remove_vlans("12", "100")

    def test_func_17(self):

        print("###### Test_func_17 ######")
        print("########## Verify functionality for redistribute all into RIP #############")
        print("###### 3 DUTs ######")

        int1.no_shut_interfaces("Ex 0/1")
        int2.no_shut_interfaces("Gi 0/9", "Gi 0/5", "Gi 0/4")
        int3.no_shut_interfaces("Gi 0/4")

        # Creating VLANs

        vl1.create_vlan(vlan="20")
        vl2.create_vlans("15", "12", "20")
        vl3.create_vlans("12", "100")

        # Adding the ports to the VLANs

        vl1.add_ports_to_vlan(ports="Ex 0/1", vlan="20")
        vl2.add_ports_to_vlan(ports="Gi 0/9", vlan="20")
        vl2.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
        vl2.add_ports_to_vlan(ports="Gi 0/4", vlan="12")
        vl3.add_ports_to_vlan(ports="Gi 0/4", vlan="12")
        vl3.add_ports_to_vlan(ports="Gi 0/4", vlan="100")

        # Adding IPs on the interfaces

        ip1.add_ip_interface(int_vlan="20", ip="20.0.0.2", mask="255.255.255.0")
        ip2.add_ip_interfaces("15", "12", "20", int_vlan15=["15.0.0.1", "255.255.255.0"],
                              int_vlan12=["12.0.0.1", "255.255.255.0"], int_vlan20=["20.0.0.1", "255.255.255.0"])
        ip3.add_ip_interfaces("12", "100", int_vlan12=["12.0.0.2", "255.255.255.0"],
                              int_vlan100=["100.0.0.2", "255.255.255.0"])

        ip1.no_shut_int_vlans("20")
        ip2.no_shut_int_vlans("20", "15", "12")
        ip3.no_shut_int_vlans("12", "100")

        # Enabling RIP and advertising the interfaces in RIP

        rip1.enable_rip()
        rip2.enable_rip()

        rip1.advertise_network(ip_network="20.0.0.2")
        rip2.advertise_networks("20.0.0.1")

        # Enabling OSPF and advertising the networks into OSPF

        ospf2.enable_ospf()
        ospf3.enable_ospf()

        # You have to remove newtork and add it back because of the OSPF process that is not eliminated after disabling it

        ospf2.advertise_network(ip_network="12.0.0.1", area="0.0.0.0")
        ospf3.advertise_network(ip_network="12.0.0.2", area="0.0.0.0")
        ospf3.advertise_network(ip_network="100.0.0.2", area="0.0.0.0")

        # Creating a static route on DUT 2

        ip2.add_static_route(network_dest="88.0.0.0", mask_dest="255.255.255.0", next_hop="15.0.0.100")

        # Redistributing all into RIP on DUT2 and installing it on DUT1

        rip2.redistribute_all()

        # Checking if the routes are installed

        time.sleep(45)

        dict_rip_routes_1 = rip1.show_ip_route_rip()
        # print(dict_rip_routes_1)

        assert "15.0.0.0" in dict_rip_routes_1.keys()
        assert "12.0.0.0" in dict_rip_routes_1.keys()
        assert "100.0.0.0" in dict_rip_routes_1.keys()
        assert "88.0.0.0" in dict_rip_routes_1.keys()

        # Remove the all redistribution on DUT2 and check if the routes are not anymore in the routing table of DUT1

        rip2.remove_redistribute_all()

        ip1.shut_int_vlan(int_vlan="20")
        ip1.no_shut_int_vlan(int_vlan="20")

        time.sleep(30)

        dict_rip_routes_1 = rip1.show_ip_route_rip()
        # print(dict_rip_routes_1)

        if len(dict_rip_routes_1.keys()) == 0:
            assert True
        else:
            assert "15.0.0.0" not in dict_rip_routes_1.keys()
            assert "12.0.0.0" not in dict_rip_routes_1.keys()
            assert "100.0.0.0" not in dict_rip_routes_1.keys()
            assert "88.0.0.0" not in dict_rip_routes_1.keys()

        print("########## Removing the config #############")

        rip1.disable_rip()
        rip2.disable_rip()

        ospf2.remove_network(ip_network="12.0.0.1", area="0.0.0.0")
        ospf3.remove_network(ip_network="12.0.0.2", area="0.0.0.0")
        ospf3.remove_network(ip_network="100.0.0.2", area="0.0.0.0")

        ospf2.disable_ospf()
        ospf3.disable_ospf()

        ip2.remove_static_route(network_dest="88.0.0.0", mask_dest="255.255.255.0", next_hop="15.0.0.100")

        ip1.remove_int_vlan(int_vlan="20")
        ip2.remove_vlan_interfaces("20", "15", "12")
        ip3.remove_vlan_interfaces("12", "100")

        int1.shut_interface(interface="Ex 0/1")
        int2.shut_interfaces("Gi 0/9", "Gi 0/5", "Gi 0/4")
        int3.shut_interfaces("Gi 0/4")

        vl1.remove_vlan(vlan="20")
        vl2.remove_vlans("20", "15", "12")
        vl3.remove_vlans("12", "100")

    def test_func_18(self):

        print("###### Test_func_18 ######")
        print("########## Verify that the DUT performs invalid timer correctly.#############")
        print("###### 2 DUTs ######")

        int1.no_shut_interfaces("Ex 0/1")
        int2.no_shut_interfaces("Gi 0/9", "Gi 0/5")

        # Creating VLANs

        vl1.create_vlan(vlan="20")
        vl2.create_vlans("15", "20")

        # Adding the ports to the VLANs

        vl1.add_ports_to_vlan(ports="Ex 0/1", vlan="20")
        vl2.add_ports_to_vlan(ports="Gi 0/9", vlan="20")
        vl2.add_ports_to_vlan(ports="Gi 0/5", vlan="15")

        # Adding IPs on the interfaces

        ip1.add_ip_interface(int_vlan="20", ip="20.0.0.2", mask="255.255.255.0")
        ip2.add_ip_interfaces("15", "20", int_vlan15=["15.0.0.1", "255.255.255.0"],
                              int_vlan20=["20.0.0.1", "255.255.255.0"])

        ip1.no_shut_int_vlans("20")
        ip2.no_shut_int_vlans("20", "15")

        # Enabling RIP and advertising the interfaces into RIP

        rip1.enable_rip()
        rip2.enable_rip()

        rip1.advertise_network(ip_network="20.0.0.2")
        rip2.advertise_networks("20.0.0.1", "15.0.0.1")

        # Shut the in vlan between the DUTs. Check the route is present in the Routing Table

        dict_rip_routes_1 = rip1.show_ip_route_rip()
        assert "15.0.0.0" in dict_rip_routes_1.keys()

        ip2.shut_int_vlan(int_vlan="20")

        # Checking the routes are not installed in RIP routing table, but they are in RIP database. (After 180s)

        time.sleep(180)

        dict_rip_routes_1 = rip1.show_ip_route_rip()
        match_total_count, dict_of_auto_summary, dict_of_directly_connected, dict_of_via = rip1.show_rip_database()

        assert "15.0.0.0" not in dict_rip_routes_1.keys()
        assert "15.0.0.0" in dict_of_via.keys() and dict_of_via["15.0.0.0"]["Metric"] == "16"

        # Checking the routes are eliminated from RIP database. (After 120s)

        time.sleep(120)

        dict_rip_routes_1 = rip1.show_ip_route_rip()
        match_total_count, dict_of_auto_summary, dict_of_directly_connected, dict_of_via = rip1.show_rip_database()

        assert "15.0.0.0" not in dict_rip_routes_1.keys()
        assert "15.0.0.0" not in dict_of_via.keys()

        # No shut the interface to check that the routes are installing

        ip2.no_shut_int_vlan(int_vlan="20")

        # Configuring the timers

        rip1.configure_rip_timers(int_vlan="20",update_timer="10",routage_timer="30",garbage_timer="150")

        # Shut the in vlan between the DUTs. Check the route is present in the Routing Table

        time.sleep(20)

        dict_rip_routes_1 = rip1.show_ip_route_rip()
        assert "15.0.0.0" in dict_rip_routes_1.keys()

        ip2.shut_int_vlan(int_vlan="20")

        # Checking the routes are not installed in RIP routing table, but they are in RIP database. (After 30s)

        time.sleep(30)

        dict_rip_routes_1 = rip1.show_ip_route_rip()
        match_total_count, dict_of_auto_summary, dict_of_directly_connected, dict_of_via = rip1.show_rip_database()

        assert "15.0.0.0" not in dict_rip_routes_1.keys()
        assert "15.0.0.0" in dict_of_via.keys() and dict_of_via["15.0.0.0"]["Metric"] == "16"

        # Checking the routes are eliminated from RIP database. (After 150s)

        time.sleep(150)

        dict_rip_routes_1 = rip1.show_ip_route_rip()
        match_total_count, dict_of_auto_summary, dict_of_directly_connected, dict_of_via = rip1.show_rip_database()

        assert "15.0.0.0" not in dict_rip_routes_1.keys()
        assert "15.0.0.0" not in dict_of_via.keys()

        print("########## Removing the config #############")

        rip1.remove_rip_timers(int_vlan="20")

        rip1.disable_rip()
        rip2.disable_rip()

        ip1.remove_int_vlan(int_vlan="20")
        ip2.remove_vlan_interfaces("20", "15")

        int1.shut_interface(interface="Ex 0/1")
        int2.shut_interfaces("Gi 0/9", "Gi 0/5")

        vl1.remove_vlan(vlan="20")
        vl2.remove_vlans("20", "15")

    def test_func_19(self):

        print("###### Test_func_19 ######")
        print("########## Verify that the DUT sends updates at update timer value.#############")
        print("###### 2 DUTs ######")

        int1.no_shut_interfaces("Ex 0/1")
        int2.no_shut_interfaces("Gi 0/9", "Gi 0/5")

        # Creating VLANs

        vl1.create_vlan(vlan="20")
        vl2.create_vlans("15", "20")

        # Adding the ports to the VLANs

        vl1.add_ports_to_vlan(ports="Ex 0/1", vlan="20")
        vl2.add_ports_to_vlan(ports="Gi 0/9", vlan="20")
        vl2.add_ports_to_vlan(ports="Gi 0/5", vlan="15")

        # Adding IPs on the interfaces

        ip1.add_ip_interface(int_vlan="20", ip="20.0.0.2", mask="255.255.255.0")
        ip2.add_ip_interfaces("15", "20", int_vlan15=["15.0.0.1", "255.255.255.0"],
                              int_vlan20=["20.0.0.1", "255.255.255.0"])

        ip1.no_shut_int_vlans("20")
        ip2.no_shut_int_vlans("20", "15")

        # Enabling RIP and advertising the interfaces into RIP

        rip1.enable_rip()
        rip2.enable_rip()

        rip1.advertise_network(ip_network="20.0.0.2")
        rip2.advertise_networks("20.0.0.1", "15.0.0.1")

        # Check the RIP statistics and verify the DUT is sending updates as expected (default is 30s)

        time.sleep(60)

        dict_rip_statistics = rip1.show_ip_rip_statistics()

        # The number should be 2 (30sx2)

        assert dict_rip_statistics["20.0.0.2"]["Updates Sent"] == "3"  # 2 in 60s + 1 that is sent after 60s

        # Modify the update timer for RIP

        rip1.remove_network(ip_network="20.0.0.2")
        rip1.advertise_network(ip_network="20.0.0.2")
        rip1.configure_rip_timers(int_vlan="20", update_timer="10", routage_timer="30", garbage_timer="150")

        # Check the RIP statistics and verify the DUT is sending updates as expected (now is 10s)

        time.sleep(53)

        dict_rip_statistics = rip1.show_ip_rip_statistics()

        # The number should be 6 (10sx6)

        assert dict_rip_statistics["20.0.0.2"]["Updates Sent"] == "7"  # 6 in 60s + 1 that is sent after 60s

        print("########## Removing the config #############")

        rip1.remove_rip_timers(int_vlan="20")

        rip1.disable_rip()
        rip2.disable_rip()

        ip1.remove_int_vlan(int_vlan="20")
        ip2.remove_vlan_interfaces("20", "15")

        int1.shut_interface(interface="Ex 0/1")
        int2.shut_interfaces("Gi 0/9", "Gi 0/5")

        vl1.remove_vlan(vlan="20")
        vl2.remove_vlans("20", "15")
