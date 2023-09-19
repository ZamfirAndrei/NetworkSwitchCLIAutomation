import time
import pytest

from config import ip, vlan, interfaces, ping, stp
from Management import ssh

ip_session_1 = "10.2.109.206"
ip_session_2 = "10.2.109.83"
ip_session_3 = "10.2.109.232"

# DUT 1 Objects

int1 = interfaces.Interface(ip_session=ip_session_1)
vl1 = vlan.VLAN(ip_session=ip_session_1)
ip1 = ip.IP(ip_session=ip_session_1)
ping1 = ping.PING(ip_session=ip_session_1)
stp1 = stp.STP(ip_session=ip_session_1)

# DUT 2 Objects

int2 = interfaces.Interface(ip_session=ip_session_2)
vl2 = vlan.VLAN(ip_session=ip_session_2)
ip2 = ip.IP(ip_session=ip_session_2)
ping2 = ping.PING(ip_session=ip_session_2)
stp2 = stp.STP(ip_session=ip_session_2)

# DUT 3 Objects

int3 = interfaces.Interface(ip_session=ip_session_3)
vl3 = vlan.VLAN(ip_session=ip_session_3)
stp3 = stp.STP(ip_session=ip_session_3)
# fdb3 = fdb.FDB(ip_session=ip_session_3)
ip3 = ip.IP(ip_session=ip_session_3)
# rip3 = rip.RIP(ip_session=ip_session_3)
ping3 = ping.PING(ip_session=ip_session_3)
# ospf3 = ospf.OSPF(ip_session=ip_session_3)


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
        vl1.create_vlan(vlan="14")
        vl1.create_vlan(vlan="30")
        vl1.create_vlan(vlan="60")
        vl1.add_ports_to_vlan(ports="Ex 0/1", vlan="14")
        vl1.add_ports_to_vlan(ports="Gi 0/3", vlan="30")
        vl1.add_ports_to_vlan(ports="Gi 0/4", vlan="60")
        ip1.create_int_vlan(int_vlan="14")
        ip1.create_int_vlan(int_vlan="30")
        ip1.create_int_vlan(int_vlan="60")
        ip1.add_ip_interface(int_vlan="14", ip="14.0.0.1", mask="255.255.255.0")
        ip1.add_ip_interface(int_vlan="30", ip="30.0.0.1", mask="255.255.255.0")
        ip1.add_ip_interface(int_vlan="60", ip="60.0.0.1", mask="255.255.0.0")

        print("#### Checking connectivity ####")

        resp = ping1.ping_more("60.0.0.100", "30.0.0.100", "14.0.0.2")
        print(resp)

        assert "60.0.0.100" in resp
        assert "30.0.0.100" in resp
        assert "14.0.0.2" not in resp

        print("########## Removing the config from DUT #############")

        vl1.remove_vlan(vlan="14")
        vl1.remove_vlan(vlan="30")
        vl1.remove_vlan(vlan="60")
        int1.shut_interfaces("Gi 0/3", "Gi 0/4", "Ex 0/1")
        ip1.remove_vlan_interfaces("14", "30", "60")

    def test_func_7(self):

        print("###### Test_func_7 ######")
        print("########## Check if interfaces VLAN are created and are Up Up/Up Down #############")

        print("#### Configuring DUT ####")

        vlan1 = "100"
        vlan2 = "110"
        vl1.create_vlan(vlan=vlan1)
        vl1.create_vlan(vlan=vlan2)
        vl1.add_ports_to_vlan(ports="Gi 0/3", vlan=vlan1)
        vl1.add_ports_to_vlan(ports="Gi 0/4", vlan=vlan2)
        int1.no_shut_interfaces("Gi 0/3", "Gi 0/4")
        ip1.add_ip_interfaces("100", "110", int_vlan1_ip=["100.0.0.1", "255.255.255.0"], int_vlan2_ip=["110.0.0.1", "255.255.255.0"])
        ip1.no_shut_int_vlans(vlan1, vlan2)

        a, b, c = int1.show_int_description()

        print(a)
        print(b)
        print(c)

        ok1 = False
        ok2 = False

        for item in c:

            if item["Interface"] == "vlan"+vlan1:

                if item["Status"] and item["Protocol"] == "Up":

                    print(f"The interface vlan {vlan1} was found and is Up Up")
                    ok1 = True

            if item["Interface"] == "vlan" + vlan2:

                if item["Status"] == "Up" and item["Protocol"] == "Up":

                    print(f"The interface vlan {vlan2} was found and is Up Up")
                    ok2 = True

        assert ok1 is True
        assert ok2 is True

        print("########## Removing the config from DUT #############")

        vl1.remove_vlan(vlan=vlan1)
        vl1.remove_vlan(vlan=vlan2)
        int1.shut_interfaces("Gi 0/3")
        ip1.remove_vlan_interfaces(vlan1, vlan2)

    def test_func_8(self):

        print("###### Test_func_8 ######")
        print("########## Check if connected interface are shown in the ip routing table #############")

        print("#### Configuring the variables ####")

        vlan1 = "40"
        vlan2 = "50"
        ip_1 = "40.0.0.1"
        ip_2 = "50.0.0.1"
        network_1 = "40.0.0.0"
        network_2 = "50.0.0.0"
        mask_1 = "255.255.255.0"
        mask_2 = "255.255.255.0"

        print("#### Configuring DUT ####")

        vl1.create_vlan(vlan=vlan1)
        vl1.create_vlan(vlan=vlan2)
        vl1.add_ports_to_vlan(ports="Gi 0/3", vlan=vlan1)
        vl1.add_ports_to_vlan(ports="Gi 0/4", vlan=vlan2)
        int1.no_shut_interfaces("Gi 0/3", "Gi 0/4")
        ip1.add_ip_interfaces(vlan1, vlan2, int_vlan1_ip=[ip_1, mask_1],
                                            int_vlan2_ip=[ip_2, mask_2])
        ip1.no_shut_int_vlans(vlan1, vlan2)

        ip_route_1, networks_1, networks_connected_1, dict_of_networks_1 = ip1.show_ip_route(network=ip_1)
        ip_route_2, networks_2, networks_connected_2, dict_of_networks_1 = ip1.show_ip_route(network=ip_2)

        print(ip_route_1)
        print(ip_route_2)

        assert ip_route_1["Protocol"] == "C" and ip_route_1["Network"] == network_1 and ip_route_1["Vlan/Port"] == "vlan" + vlan1
        assert ip_route_2["Protocol"] == "C" and ip_route_2["Network"] == network_2 and ip_route_2["Vlan/Port"] == "vlan" + vlan2

        print("########## Removing the config from DUT #############")

        vl1.remove_vlan(vlan=vlan1)
        vl1.remove_vlan(vlan=vlan2)
        int1.shut_interfaces("Gi 0/3", "Gi 0/4")
        ip1.remove_vlan_interfaces(vlan1, vlan2)

    def test_func_9(self):

        print("###### Test_func_9 ######")
        print("########## Check if static routes are shown in the ip routing table #############")

        print("#### Configuring the variables ####")

        vlan1 = "14"
        ip_1 = "14.0.0.2"
        mask_1 = "255.255.255.0"
        network_destination = "15.0.0.0"
        mask_destination = "255.255.255.0"
        next_hop = "14.0.0.1"

        print("#### Configuring DUT ####")

        vl1.create_vlan(vlan=vlan1)
        vl1.add_ports_to_vlan(ports="Gi 0/3", vlan=vlan1)
        int1.no_shut_interfaces("Gi 0/3")
        ip1.add_ip_interfaces(vlan1, int_vlan1_ip=[ip_1, mask_1])
        ip1.no_shut_int_vlans(vlan1)

        print(f"#### Configuring static route towards network {network_destination} ####")

        ip1.add_static_route(network_dest=network_destination, mask_dest=mask_destination, next_hop=next_hop)

        ip_route_1, networks_1, networks_connected_1, dict_of_networks_1 = ip1.show_ip_route(network=network_destination)

        print(ip_route_1)

        assert ip_route_1["Protocol"] == "S" and ip_route_1["Network"] == network_destination and ip_route_1["Next Hop"] == next_hop

        print("########## Removing the config from DUT #############")

        vl1.remove_vlan(vlan=vlan1)
        int1.shut_interfaces("Gi 0/3")
        ip1.remove_vlan_interfaces(vlan1)
        ip1.remove_static_route(network_dest=network_destination, mask_dest=mask_destination, next_hop=next_hop)

    # Mai e de facut un test cu show ip route (sa le vad pe alea connected si static in acelasi timp)

    def test_func_10(self):

        # LOKI-551

        print("###### Test_func_10 ######")
        print("########## Check if there is connectivity when the same static routes are configured with different outbounds #############")
        print("###### 3 DUTs ######")

        int1.no_shut_interfaces("Ex 0/1", "Gi 0/9")
        int2.no_shut_interfaces("Gi 0/9", "Gi 0/5", "Gi 0/4")
        int3.no_shut_interfaces("Gi 0/4", "Gi 0/9")

        # Creating VLANs

        vl1.create_vlans("20", "40")
        vl2.create_vlans("15", "30", "20")
        vl3.create_vlans("30", "40")

        # Adding the ports to the VLANs

        vl1.add_ports_to_vlan(ports="Ex 0/1", vlan="20")
        vl1.add_ports_to_vlan(ports="Gi 0/9", vlan="40")
        vl2.add_ports_to_vlan(ports="Gi 0/9", vlan="20")
        vl2.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
        vl2.add_ports_to_vlan(ports="Gi 0/4", vlan="30")
        vl3.add_ports_to_vlan(ports="Gi 0/4", vlan="30")
        vl3.add_ports_to_vlan(ports="Gi 0/9", vlan="40")

        # Creating INT VLANs on all DUTs

        ip1.add_ip_interfaces("20", "40", int_vlan20=["20.0.0.2", "255.255.255.0"],
                              int_vlan40=["40.0.0.2", "255.255.255.0"])
        ip2.add_ip_interfaces("15", "30", "20", int_vlan15=["15.0.0.1", "255.255.255.0"],
                              int_vlan30=["30.0.0.1", "255.255.255.0"], int_vlan20=["20.0.0.1", "255.255.255.0"])
        ip3.add_ip_interfaces("30", "40", int_vlan30=["30.0.0.2", "255.255.255.0"],
                              int_vlan40=["40.0.0.1", "255.255.255.0"])

        ip1.no_shut_int_vlans("20", "40")
        ip2.no_shut_int_vlans("20", "30", "15")
        ip3.no_shut_int_vlans("30", "40")

        # Configuring static routes on DUTs

        ip1.add_static_route(network_dest="15.0.0.0", mask_dest="255.255.255.0", next_hop="20.0.0.1")
        ip1.add_static_route(network_dest="15.0.0.0", mask_dest="255.255.255.0", next_hop="40.0.0.1",distance_metric="2")
        ip1.add_static_route(network_dest="30.0.0.0", mask_dest="255.255.255.0", next_hop="20.0.0.1")
        ip1.add_static_route(network_dest="30.0.0.0", mask_dest="255.255.255.0", next_hop="40.0.0.1",distance_metric="2")

        ip2.add_static_route(network_dest="40.0.0.0", mask_dest="255.255.255.0", next_hop="20.0.0.2")
        ip2.add_static_route(network_dest="40.0.0.0", mask_dest="255.255.255.0", next_hop="30.0.0.2",distance_metric="2")

        ip3.add_static_route(network_dest="15.0.0.0", mask_dest="255.255.255.0", next_hop="30.0.0.1")
        ip3.add_static_route(network_dest="15.0.0.0", mask_dest="255.255.255.0", next_hop="40.0.0.2",distance_metric="2")
        ip3.add_static_route(network_dest="20.0.0.0", mask_dest="255.255.255.0", next_hop="30.0.0.1")
        ip3.add_static_route(network_dest="20.0.0.0", mask_dest="255.255.255.0", next_hop="40.0.0.2",distance_metric="2")

        # Checking that the Static Routes are installed

        ip_route, networks, networks_connected, dict_of_networks = ip1.show_ip_route()
        print(dict_of_networks)

        d_root_id, d_bridge_id, ports, dict_of_ports = stp1.show_spanning_tree_rstp()
        print(dict_of_ports)

        assert "15.0.0.0" in dict_of_networks and "30.0.0.0" in dict_of_networks
        assert dict_of_networks["15.0.0.0"]["Protocol"] == "S" and dict_of_networks["15.0.0.0"]["Next Hop"] == "20.0.0.1"
        assert dict_of_networks["30.0.0.0"]["Protocol"] == "S" and dict_of_networks["30.0.0.0"]["Next Hop"] == "20.0.0.1"
        assert "Ex0/1" in dict_of_ports and dict_of_ports["Ex0/1"]["Role"] == "Root"

        response = ping1.ping_more("15.0.0.1", "30.0.0.1")

        assert "15.0.0.1" in response and "30.0.0.1" in response

        # Change the cost of the port Ex 0/1 (the stp will change the role of the port to ALTN) so that the traffic will be redirected trough int vlan 40.

        stp1.add_rstp_port_cost(port="Ex 0/1", cost="50000")

        ip_route, networks, networks_connected, dict_of_networks = ip1.show_ip_route()
        print(dict_of_networks)

        d_root_id, d_bridge_id, ports, dict_of_ports = stp1.show_spanning_tree_rstp()
        print(dict_of_ports)

        assert "15.0.0.0" in dict_of_networks and "30.0.0.0" in dict_of_networks
        assert dict_of_networks["15.0.0.0"]["Protocol"] == "S" and dict_of_networks["15.0.0.0"]["Next Hop"] == "40.0.0.1"
        assert dict_of_networks["30.0.0.0"]["Protocol"] == "S" and dict_of_networks["30.0.0.0"]["Next Hop"] == "40.0.0.1"
        assert "Ex0/1" in dict_of_ports and dict_of_ports["Ex0/1"]["Role"] == "Alternate"

        response = ping1.ping_more("15.0.0.1", "30.0.0.1")

        assert "15.0.0.1" in response and "30.0.0.1" in response

        print("########## Removing the config from DUT #############")

        stp1.remove_rstp_port_cost(port="Ex 0/1")

        ip1.remove_static_route(network_dest="15.0.0.0", mask_dest="255.255.255.0", next_hop="20.0.0.1")
        ip1.remove_static_route(network_dest="15.0.0.0", mask_dest="255.255.255.0", next_hop="40.0.0.1")
        ip1.remove_static_route(network_dest="30.0.0.0", mask_dest="255.255.255.0", next_hop="20.0.0.1")
        ip1.remove_static_route(network_dest="30.0.0.0", mask_dest="255.255.255.0", next_hop="40.0.0.1")

        ip2.remove_static_route(network_dest="40.0.0.0", mask_dest="255.255.255.0", next_hop="20.0.0.2")
        ip2.remove_static_route(network_dest="40.0.0.0", mask_dest="255.255.255.0", next_hop="30.0.0.2")

        ip3.remove_static_route(network_dest="15.0.0.0", mask_dest="255.255.255.0", next_hop="30.0.0.1")
        ip3.remove_static_route(network_dest="15.0.0.0", mask_dest="255.255.255.0", next_hop="40.0.0.2")
        ip3.remove_static_route(network_dest="20.0.0.0", mask_dest="255.255.255.0", next_hop="30.0.0.1")
        ip3.remove_static_route(network_dest="20.0.0.0", mask_dest="255.255.255.0", next_hop="40.0.0.2")

        ip1.remove_vlan_interfaces("20","40")
        ip2.remove_vlan_interfaces("15","20","30")
        ip3.remove_vlan_interfaces("30", "40")

        vl1.remove_vlans("20", "40")
        vl2.remove_vlans("15", "20", "30")
        vl3.remove_vlans("30", "40")

        int1.shut_interfaces("Ex 0/1", "Gi 0/9")
        int2.shut_interfaces("Gi 0/4", "Gi 0/5", "Gi 0/9")
        int3.shut_interfaces("Gi 0/4", "Gi 0/9")





