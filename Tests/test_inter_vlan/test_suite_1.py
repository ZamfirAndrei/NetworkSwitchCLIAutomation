import time
import pytest

from config import ip, vlan, interfaces, ping
from Management import ssh

ip_session_1 = "10.2.109.206"
ip_session_2 = "10.2.109.83"

# DUT 1 Objects

int1 = interfaces.Interface(ip_session=ip_session_1)
vl1 = vlan.VLAN(ip_session=ip_session_1)
ip1 = ip.IP(ip_session=ip_session_1)
ping1 = ping.PING(ip_session=ip_session_1)

# DUT 2 Objects

int2 = interfaces.Interface(ip_session=ip_session_2)
vl2 = vlan.VLAN(ip_session=ip_session_2)
ip2 = ip.IP(ip_session=ip_session_2)
ping2 = ping.PING(ip_session=ip_session_2)


class TestInterVlanRoutingSuite1:
    def test_func_1(self):

        print("###### Test_func_1 ######")
        print("########## Check if interface VLANs are created #############")

        vl1.create_vlan(vlan="200")
        int1.no_shut_interface(interface="Gi 0/3")
        vl1.add_ports_to_vlan(ports="Gi 0/3", vlan="200")
        ip1.create_int_vlan(int_vlan="200")
        ip1.add_ip_interface(int_vlan="200", ip="200.0.0.1", mask="255.255.255.0")

        vl1.create_vlan(vlan="30")
        int1.no_shut_interface(interface="Gi 0/3")
        vl1.add_ports_to_vlan(ports="Gi 0/3", vlan="30")
        ip1.create_int_vlan(int_vlan="30")
        ip1.add_ip_interface(int_vlan="30", ip="30.0.0.1", mask="255.255.255.0")

        a, b, c = ip1.show_ip_int(int_vlan="200")
        a1, b1, c1 = ip1.show_ip_int(int_vlan="30")

        print(a, a1)

        assert a["Interface Vlan"] == "vlan200"
        assert a1["Interface Vlan"] == "vlan30"

        print("########## Removing the config #############")

        vl1.remove_vlan(vlan="200")
        vl1.remove_vlan(vlan="30")
        int1.shut_interfaces("Gi 0/3", "Gi 0/4")
        ip1.remove_vlan_interfaces("200", "30")

    def test_func_2(self):

        print("###### Test_func_2 ######")
        print("########## Check if there is connectivity towards IXIA port #############")

        vl1.create_vlan(vlan="30")
        int1.no_shut_interface(interface="Gi 0/3")
        vl1.add_ports_to_vlan(ports="Gi 0/3", vlan="30")
        ip1.create_int_vlan(int_vlan="30")
        ip1.add_ip_interface(int_vlan="30", ip="30.0.0.1", mask="255.255.255.0")

        resp = ping1.ping(ip_dest="30.0.0.100")
        print(resp)

        assert "30.0.0.100" in resp

        print("########## Removing the config #############")

        vl1.remove_vlan(vlan="30")
        int1.shut_interfaces("Gi 0/3")
        ip1.remove_vlan_interfaces("30")

    def test_func_3(self):

        print("###### Test_func_3 ######")
        print("########## Check if there is connectivity towards IXIA port #############")

        vl1.create_vlan(vlan="60")
        int1.no_shut_interface(interface="Gi 0/4")
        vl1.add_ports_to_vlan(ports="Gi 0/4", vlan="60")
        ip1.create_int_vlan(int_vlan="60")
        ip1.add_ip_interface(int_vlan="60", ip="60.0.0.1", mask="255.255.0.0")

        resp = ping1.ping(ip_dest="60.0.0.100")
        print(resp)

        assert "60.0.0.100" in resp

        print("########## Removing the config #############")

        vl1.remove_vlan(vlan="60")
        int1.shut_interfaces("Gi 0/4")
        ip1.remove_vlan_interfaces("60")

    def test_func_4(self):

        print("###### Test_func_4 ######")
        print("########## Check if there is connectivity towards other DUT link #############")

        print("Configuring DUT 1")

        vl1.create_vlan(vlan="14")
        int1.no_shut_interface(interface="Ex 0/1")
        vl1.add_ports_to_vlan(ports="Ex 0/1", vlan="14")
        ip1.create_int_vlan(int_vlan="14")
        ip1.add_ip_interface(int_vlan="14", ip="14.0.0.2", mask="255.255.255.0")

        print("Configuring DUT 2")

        vl2.create_vlan(vlan="14")
        int2.no_shut_interface(interface="Gi 0/9")
        vl2.add_ports_to_vlan(ports="Gi 0/9", vlan="14")
        ip2.create_int_vlan(int_vlan="14")
        ip2.add_ip_interface(int_vlan="14", ip="14.0.0.1", mask="255.255.255.0")

        resp = ping1.ping(ip_dest="14.0.0.1")
        print(resp)

        assert "14.0.0.1" in resp

        print("########## Removing the config from DUT 1 #############")

        vl1.remove_vlan(vlan="14")
        int1.shut_interfaces("Ex 0/1")
        ip1.remove_vlan_interfaces("14")

        print("########## Removing the config from DUT 2 #############")

        vl2.remove_vlan(vlan="14")
        int2.shut_interfaces("Gi 0/9")
        ip2.remove_vlan_interfaces("14")

    def test_func_5(self):

        print("###### Test_func_5 ######")
        print("########## Check if there is connectivity towards other DUT IXIA #############")

        print("#### Configuring DUT 1 ####")

        int1.no_shut_interface(interface="Ex 0/1")
        int1.no_shut_interface(interface="Gi 0/3")
        vl1.create_vlan(vlan="30")
        vl1.create_vlan(vlan="14")
        vl1.add_ports_to_vlan(ports="Ex 0/1", vlan="14")
        vl1.add_ports_to_vlan(ports="Gi 0/3", vlan="30")
        ip1.create_int_vlan(int_vlan="30")
        ip1.create_int_vlan(int_vlan="14")
        ip1.add_ip_interface(int_vlan="30", ip="30.0.0.1", mask="255.255.255.0")
        ip1.add_ip_interface(int_vlan="14", ip="14.0.0.2", mask="255.255.255.0")

        print("#### Configuring DUT 2 ####")

        int2.no_shut_interface(interface="Gi 0/5")
        int2.no_shut_interface(interface="Gi 0/9")
        vl2.create_vlan(vlan="15")
        vl2.create_vlan(vlan="14")
        vl2.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
        vl2.add_ports_to_vlan(ports="Gi 0/9", vlan="14")
        ip2.create_int_vlan(int_vlan="15")
        ip2.create_int_vlan(int_vlan="14")
        ip2.add_ip_interface(int_vlan="15", ip="15.0.0.1", mask="255.255.255.0")
        ip2.add_ip_interface(int_vlan="14", ip="14.0.0.1", mask="255.255.255.0")

        print("#### Configuring the static routes towards IXIAs networks ####")

        ip1.add_static_route(network_dest="15.0.0.0", mask_dest="255.255.255.0", next_hop="14.0.0.1")
        ip2.add_static_route(network_dest="30.0.0.0", mask_dest="255.255.255.0", next_hop="14.0.0.2")

        print("#### Checking connectivity ####")

        resp1 = ping1.ping(ip_dest="15.0.0.100")
        print(resp1)
        resp2 = ping2.ping(ip_dest="30.0.0.100")
        print(resp2)

        assert "15.0.0.100" in resp1
        assert "30.0.0.100" in resp2

        print("########## Removing the config from DUT 1 #############")

        vl1.remove_vlan(vlan="14")
        vl1.remove_vlan(vlan="30")
        int1.shut_interfaces("Ex 0/1", "Gi 0/3")
        ip1.remove_vlan_interfaces("14", "30")
        ip1.remove_static_route(network_dest="15.0.0.0", mask_dest="255.255.255.0", next_hop="14.0.0.1")

        print("########## Removing the config from DUT 2 #############")

        vl2.remove_vlan(vlan="14")
        vl2.remove_vlan(vlan="15")
        int2.shut_interfaces("Gi 0/9", "Gi 0/5")
        ip2.remove_vlan_interfaces("14", "15")
        ip2.remove_static_route(network_dest="30.0.0.0", mask_dest="255.255.255.0", next_hop="14.0.0.2")

    def test_func_6(self):

        print("###### Test_func_6 ######")
        print("########## Check if there is connectivity towards other networks #############")

        print("#### Configuring DUT ####")

        int1.no_shut_interfaces("Gi 0/3", "Gi 0/4", "Ex 0/1")
        vl1.create_vlan(vlan="30")
        vl1.create_vlan(vlan="14")
        vl1.create_vlan(vlan="60")
        vl1.add_ports_to_vlan(ports="Ex 0/1", vlan="14")
        vl1.add_ports_to_vlan(ports="Gi 0/3", vlan="30")
        vl1.add_ports_to_vlan(ports="Gi 0/4", vlan="60")
        ip1.create_int_vlan(int_vlan="30")
        ip1.create_int_vlan(int_vlan="14")
        ip1.create_int_vlan(int_vlan="60")
        ip1.add_ip_interface(int_vlan="30", ip="30.0.0.1", mask="255.255.255.0")
        ip1.add_ip_interface(int_vlan="14", ip="14.0.0.2", mask="255.255.255.0")
        ip1.add_ip_interface(int_vlan="60", ip="60.0.0.1", mask="255.255.0.0")

        print("#### Checking connectivity ####")

        resp = ping1.ping_more("60.0.0.100", "30.0.0.100", "14.0.0.2")
        print(resp)

        assert "60.0.0.100" in resp
        assert "30.0.0.100" in resp
        assert "14.0.0.2" not in resp

        print("########## Removing the config from DUT #############")

        vl1.remove_vlan(vlan="14")
        vl1.remove_vlan(vlan="60")
        vl1.remove_vlan(vlan="30")
        int1.shut_interfaces("Gi 0/3", "Gi 0/4", "Ex 0/1")
        ip1.remove_vlan_interfaces("14", "15", "60")

