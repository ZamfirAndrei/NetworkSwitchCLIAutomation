import time
import pytest

from config import ip, vlan, interfaces, ping, stp
from Management import dut_objects

ip_session_1 = "10.2.109.206"
ip_session_2 = "10.2.109.83"
ip_session_3 = "10.2.109.232"

DUT1 = dut_objects.DUT_Objects(ip_session=ip_session_1)
DUT2 = dut_objects.DUT_Objects(ip_session=ip_session_2)
DUT3 = dut_objects.DUT_Objects(ip_session=ip_session_3)


class TestInterVlanRoutingSuite1:
    def test_func_1(self):

        print("###### Test_func_1 ######")
        print("########## Check if interface VLANs are created #############")

        DUT1.vl.create_vlan(vlan="200")
        DUT1.int.no_shut_interface(interface="Gi 0/3")
        DUT1.vl.add_ports_to_vlan(ports="Gi 0/3", vlan="200")
        DUT1.ip.create_int_vlan(int_vlan="200")
        DUT1.ip.add_ip_interface(int_vlan="200", ip="200.0.0.1", mask="255.255.255.0")

        DUT1.vl.create_vlan(vlan="30")
        DUT1.int.no_shut_interface(interface="Gi 0/3")
        DUT1.vl.add_ports_to_vlan(ports="Gi 0/3", vlan="30")
        DUT1.ip.create_int_vlan(int_vlan="30")
        DUT1.ip.add_ip_interface(int_vlan="30", ip="30.0.0.1", mask="255.255.255.0")

        a, b, c = DUT1.ip.show_ip_int(int_vlan="200")
        a1, b1, c1 = DUT1.ip.show_ip_int(int_vlan="30")

        print(a, a1)

        assert a["Interface Vlan"] == "vlan200"
        assert a1["Interface Vlan"] == "vlan30"

        print("########## Removing the config #############")

        DUT1.vl.remove_vlan(vlan="200")
        DUT1.vl.remove_vlan(vlan="30")
        DUT1.int.shut_interfaces("Gi 0/3", "Gi 0/4")
        DUT1.ip.remove_vlan_interfaces("200", "30")

    def test_func_2(self):

        print("###### Test_func_2 ######")
        print("########## Check if there is connectivity towards IXIA port #############")

        DUT1.vl.create_vlan(vlan="30")
        DUT1.int.no_shut_interface(interface="Gi 0/3")
        DUT1.vl.add_ports_to_vlan(ports="Gi 0/3", vlan="30")
        DUT1.ip.create_int_vlan(int_vlan="30")
        DUT1.ip.add_ip_interface(int_vlan="30", ip="30.0.0.1", mask="255.255.255.0")

        resp = DUT1.ping.ping(ip_dest="30.0.0.100")
        print(resp)

        assert "30.0.0.100" in resp

        print("########## Removing the config #############")

        DUT1.vl.remove_vlan(vlan="30")
        DUT1.int.shut_interfaces("Gi 0/3")
        DUT1.ip.remove_vlan_interfaces("30")

    def test_func_3(self):

        print("###### Test_func_3 ######")
        print("########## Check if there is connectivity towards IXIA port #############")

        DUT1.vl.create_vlan(vlan="60")
        DUT1.int.no_shut_interface(interface="Gi 0/4")
        DUT1.vl.add_ports_to_vlan(ports="Gi 0/4", vlan="60")
        DUT1.ip.create_int_vlan(int_vlan="60")
        DUT1.ip.add_ip_interface(int_vlan="60", ip="60.0.0.1", mask="255.255.0.0")

        resp = DUT1.ping.ping(ip_dest="60.0.0.100")
        print(resp)

        assert "60.0.0.100" in resp

        print("########## Removing the config #############")

        DUT1.vl.remove_vlan(vlan="60")
        DUT1.int.shut_interfaces("Gi 0/4")
        DUT1.ip.remove_vlan_interfaces("60")

    def test_func_4(self):

        print("###### Test_func_4 ######")
        print("########## Check if there is connectivity towards other DUT link #############")

        print("Configuring DUT 1")

        DUT1.vl.create_vlan(vlan="14")
        DUT1.int.no_shut_interface(interface="Ex 0/1")
        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="14")
        DUT1.ip.create_int_vlan(int_vlan="14")
        DUT1.ip.add_ip_interface(int_vlan="14", ip="14.0.0.2", mask="255.255.255.0")

        print("Configuring DUT 2")

        DUT2.vl.create_vlan(vlan="14")
        DUT2.int.no_shut_interface(interface="Gi 0/9")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="14")
        DUT2.ip.create_int_vlan(int_vlan="14")
        DUT2.ip.add_ip_interface(int_vlan="14", ip="14.0.0.1", mask="255.255.255.0")

        resp = DUT1.ping.ping(ip_dest="14.0.0.1")
        print(resp)

        assert "14.0.0.1" in resp

        print("########## Removing the config from DUT 1 #############")

        DUT1.vl.remove_vlan(vlan="14")
        DUT1.int.shut_interfaces("Ex 0/1")
        DUT1.ip.remove_vlan_interfaces("14")

        print("########## Removing the config from DUT 2 #############")

        DUT2.vl.remove_vlan(vlan="14")
        DUT2.int.shut_interfaces("Gi 0/9")
        DUT2.ip.remove_vlan_interfaces("14")

    def test_func_5(self):

        print("###### Test_func_5 ######")
        print("########## Check if there is connectivity towards other DUT IXIA #############")

        print("#### Configuring DUT 1 ####")

        DUT1.int.no_shut_interface(interface="Ex 0/1")
        DUT1.int.no_shut_interface(interface="Gi 0/3")
        DUT1.vl.create_vlan(vlan="30")
        DUT1.vl.create_vlan(vlan="14")
        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="14")
        DUT1.vl.add_ports_to_vlan(ports="Gi 0/3", vlan="30")
        DUT1.ip.create_int_vlan(int_vlan="30")
        DUT1.ip.create_int_vlan(int_vlan="14")
        DUT1.ip.add_ip_interface(int_vlan="30", ip="30.0.0.1", mask="255.255.255.0")
        DUT1.ip.add_ip_interface(int_vlan="14", ip="14.0.0.2", mask="255.255.255.0")

        print("#### Configuring DUT 2 ####")

        DUT2.int.no_shut_interface(interface="Gi 0/5")
        DUT2.int.no_shut_interface(interface="Gi 0/9")
        DUT2.vl.create_vlan(vlan="15")
        DUT2.vl.create_vlan(vlan="14")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="14")
        DUT2.ip.create_int_vlan(int_vlan="15")
        DUT2.ip.create_int_vlan(int_vlan="14")
        DUT2.ip.add_ip_interface(int_vlan="15", ip="15.0.0.1", mask="255.255.255.0")
        DUT2.ip.add_ip_interface(int_vlan="14", ip="14.0.0.1", mask="255.255.255.0")

        print("#### Configuring the static routes towards IXIAs networks ####")

        DUT1.ip.add_static_route(network_dest="15.0.0.0", mask_dest="255.255.255.0", next_hop="14.0.0.1")
        DUT2.ip.add_static_route(network_dest="30.0.0.0", mask_dest="255.255.255.0", next_hop="14.0.0.2")

        print("#### Checking connectivity ####")

        resp1 = DUT1.ping.ping(ip_dest="15.0.0.100")
        print(resp1)
        resp2 = DUT2.ping.ping(ip_dest="30.0.0.100")
        print(resp2)

        assert "15.0.0.100" in resp1
        assert "30.0.0.100" in resp2

        print("########## Removing the config from DUT 1 #############")

        DUT1.vl.remove_vlan(vlan="14")
        DUT1.vl.remove_vlan(vlan="30")
        DUT1.int.shut_interfaces("Ex 0/1", "Gi 0/3")
        DUT1.ip.remove_vlan_interfaces("14", "30")
        DUT1.ip.remove_static_route(network_dest="15.0.0.0", mask_dest="255.255.255.0", next_hop="14.0.0.1")

        print("########## Removing the config from DUT 2 #############")

        DUT2.vl.remove_vlan(vlan="14")
        DUT2.vl.remove_vlan(vlan="15")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/5")
        DUT2.ip.remove_vlan_interfaces("14", "15")
        DUT2.ip.remove_static_route(network_dest="30.0.0.0", mask_dest="255.255.255.0", next_hop="14.0.0.2")

    def test_func_6(self):

        print("###### Test_func_6 ######")
        print("########## Check if there is connectivity towards other networks #############")

        print("#### Configuring DUT ####")

        DUT1.int.no_shut_interfaces("Gi 0/3", "Gi 0/4", "Ex 0/1")
        DUT1.vl.create_vlan(vlan="14")
        DUT1.vl.create_vlan(vlan="30")
        DUT1.vl.create_vlan(vlan="60")
        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="14")
        DUT1.vl.add_ports_to_vlan(ports="Gi 0/3", vlan="30")
        DUT1.vl.add_ports_to_vlan(ports="Gi 0/4", vlan="60")
        DUT1.ip.create_int_vlan(int_vlan="14")
        DUT1.ip.create_int_vlan(int_vlan="30")
        DUT1.ip.create_int_vlan(int_vlan="60")
        DUT1.ip.add_ip_interface(int_vlan="14", ip="14.0.0.1", mask="255.255.255.0")
        DUT1.ip.add_ip_interface(int_vlan="30", ip="30.0.0.1", mask="255.255.255.0")
        DUT1.ip.add_ip_interface(int_vlan="60", ip="60.0.0.1", mask="255.255.0.0")

        print("#### Checking connectivity ####")

        resp = DUT1.ping.ping_more("60.0.0.100", "30.0.0.100", "14.0.0.2")
        print(resp)

        assert "60.0.0.100" in resp
        assert "30.0.0.100" in resp
        assert "14.0.0.2" not in resp

        print("########## Removing the config from DUT #############")

        DUT1.vl.remove_vlan(vlan="14")
        DUT1.vl.remove_vlan(vlan="30")
        DUT1.vl.remove_vlan(vlan="60")
        DUT1.int.shut_interfaces("Gi 0/3", "Gi 0/4", "Ex 0/1")
        DUT1.ip.remove_vlan_interfaces("14", "30", "60")

    def test_func_7(self):

        print("###### Test_func_7 ######")
        print("########## Check if interfaces VLAN are created and are Up Up/Up Down #############")

        print("#### Configuring DUT ####")

        vlan1 = "100"
        vlan2 = "110"
        DUT1.vl.create_vlan(vlan=vlan1)
        DUT1.vl.create_vlan(vlan=vlan2)
        DUT1.vl.add_ports_to_vlan(ports="Gi 0/3", vlan=vlan1)
        DUT1.vl.add_ports_to_vlan(ports="Gi 0/4", vlan=vlan2)
        DUT1.int.no_shut_interfaces("Gi 0/3", "Gi 0/4")
        DUT1.ip.add_ip_interfaces("100", "110", int_vlan1_ip=["100.0.0.1", "255.255.255.0"], int_vlan2_ip=["110.0.0.1", "255.255.255.0"])
        DUT1.ip.no_shut_int_vlans(vlan1, vlan2)

        a, b, c = DUT1.int.show_int_description()

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

        DUT1.vl.remove_vlan(vlan=vlan1)
        DUT1.vl.remove_vlan(vlan=vlan2)
        DUT1.int.shut_interfaces("Gi 0/3")
        DUT1.ip.remove_vlan_interfaces(vlan1, vlan2)

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

        DUT1.vl.create_vlan(vlan=vlan1)
        DUT1.vl.create_vlan(vlan=vlan2)
        DUT1.vl.add_ports_to_vlan(ports="Gi 0/3", vlan=vlan1)
        DUT1.vl.add_ports_to_vlan(ports="Gi 0/4", vlan=vlan2)
        DUT1.int.no_shut_interfaces("Gi 0/3", "Gi 0/4")
        DUT1.ip.add_ip_interfaces(vlan1, vlan2, int_vlan1_ip=[ip_1, mask_1],
                                            int_vlan2_ip=[ip_2, mask_2])
        DUT1.ip.no_shut_int_vlans(vlan1, vlan2)

        ip_route_1, networks_1, networks_connected_1, dict_of_networks_1 = DUT1.ip.show_ip_route(network=ip_1)
        ip_route_2, networks_2, networks_connected_2, dict_of_networks_1 = DUT1.ip.show_ip_route(network=ip_2)

        print(ip_route_1)
        print(ip_route_2)

        assert ip_route_1["Protocol"] == "C" and ip_route_1["Network"] == network_1 and ip_route_1["Vlan/Port"] == "vlan" + vlan1
        assert ip_route_2["Protocol"] == "C" and ip_route_2["Network"] == network_2 and ip_route_2["Vlan/Port"] == "vlan" + vlan2

        print("########## Removing the config from DUT #############")

        DUT1.vl.remove_vlan(vlan=vlan1)
        DUT1.vl.remove_vlan(vlan=vlan2)
        DUT1.int.shut_interfaces("Gi 0/3", "Gi 0/4")
        DUT1.ip.remove_vlan_interfaces(vlan1, vlan2)

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

        DUT1.vl.create_vlan(vlan=vlan1)
        DUT1.vl.add_ports_to_vlan(ports="Gi 0/3", vlan=vlan1)
        DUT1.int.no_shut_interfaces("Gi 0/3")
        DUT1.ip.add_ip_interfaces(vlan1, int_vlan1_ip=[ip_1, mask_1])
        DUT1.ip.no_shut_int_vlans(vlan1)

        print(f"#### Configuring static route towards network {network_destination} ####")

        DUT1.ip.add_static_route(network_dest=network_destination, mask_dest=mask_destination, next_hop=next_hop)

        ip_route_1, networks_1, networks_connected_1, dict_of_networks_1 = DUT1.ip.show_ip_route(network=network_destination)

        print(ip_route_1)

        assert ip_route_1["Protocol"] == "S" and ip_route_1["Network"] == network_destination and ip_route_1["Next Hop"] == next_hop

        print("########## Removing the config from DUT #############")

        DUT1.vl.remove_vlan(vlan=vlan1)
        DUT1.int.shut_interfaces("Gi 0/3")
        DUT1.ip.remove_vlan_interfaces(vlan1)
        DUT1.ip.remove_static_route(network_dest=network_destination, mask_dest=mask_destination, next_hop=next_hop)

    # Mai e de facut un test cu show ip route (sa le vad pe alea connected si static in acelasi timp)

    def test_func_10(self):

        # LOKI-551

        print("###### Test_func_10 ######")
        print("########## Check if there is connectivity when the same static routes are configured with different outbounds #############")
        print("###### 3 DUTs ######")

        DUT1.int.no_shut_interfaces("Ex 0/1", "Gi 0/9")
        DUT2.int.no_shut_interfaces("Gi 0/9", "Gi 0/5", "Gi 0/4")
        DUT3.int.no_shut_interfaces("Gi 0/4", "Gi 0/9")

        # Creating VLANs

        DUT1.vl.create_vlans("20", "40")
        DUT2.vl.create_vlans("15", "30", "20")
        DUT3.vl.create_vlans("30", "40")

        # Adding the ports to the VLANs

        DUT1.vl.add_ports_to_vlan(ports="Ex 0/1", vlan="20")
        DUT1.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="40")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="20")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
        DUT2.vl.add_ports_to_vlan(ports="Gi 0/4", vlan="30")
        DUT3.vl.add_ports_to_vlan(ports="Gi 0/4", vlan="30")
        DUT3.vl.add_ports_to_vlan(ports="Gi 0/9", vlan="40")

        # Creating INT VLANs on all DUTs

        DUT1.ip.add_ip_interfaces("20", "40", int_vlan20=["20.0.0.2", "255.255.255.0"], int_vlan40=["40.0.0.2", "255.255.255.0"])
        DUT2.ip.add_ip_interfaces("15", "30", "20", int_vlan15=["15.0.0.1", "255.255.255.0"], int_vlan30=["30.0.0.1", "255.255.255.0"], int_vlan20=["20.0.0.1", "255.255.255.0"])
        DUT3.ip.add_ip_interfaces("30", "40", int_vlan30=["30.0.0.2", "255.255.255.0"], int_vlan40=["40.0.0.1", "255.255.255.0"])

        DUT1.ip.no_shut_int_vlans("20", "40")
        DUT2.ip.no_shut_int_vlans("20", "30", "15")
        DUT3.ip.no_shut_int_vlans("30", "40")

        # Configuring static routes on DUTs

        DUT1.ip.add_static_route(network_dest="15.0.0.0", mask_dest="255.255.255.0", next_hop="20.0.0.1")
        DUT1.ip.add_static_route(network_dest="15.0.0.0", mask_dest="255.255.255.0", next_hop="40.0.0.1",distance_metric="2")
        DUT1.ip.add_static_route(network_dest="30.0.0.0", mask_dest="255.255.255.0", next_hop="20.0.0.1")
        DUT1.ip.add_static_route(network_dest="30.0.0.0", mask_dest="255.255.255.0", next_hop="40.0.0.1",distance_metric="2")

        DUT2.ip.add_static_route(network_dest="40.0.0.0", mask_dest="255.255.255.0", next_hop="20.0.0.2")
        DUT2.ip.add_static_route(network_dest="40.0.0.0", mask_dest="255.255.255.0", next_hop="30.0.0.2",distance_metric="2")

        DUT3.ip.add_static_route(network_dest="15.0.0.0", mask_dest="255.255.255.0", next_hop="30.0.0.1")
        DUT3.ip.add_static_route(network_dest="15.0.0.0", mask_dest="255.255.255.0", next_hop="40.0.0.2",distance_metric="2")
        DUT3.ip.add_static_route(network_dest="20.0.0.0", mask_dest="255.255.255.0", next_hop="30.0.0.1")
        DUT3.ip.add_static_route(network_dest="20.0.0.0", mask_dest="255.255.255.0", next_hop="40.0.0.2",distance_metric="2")

        # Checking that the Static Routes are installed

        time.sleep(15)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        d_root_id, d_bridge_id, ports, dict_of_ports = DUT1.stp.show_spanning_tree_rstp()
        print(dict_of_ports)

        assert "15.0.0.0" in dict_of_networks and "30.0.0.0" in dict_of_networks
        assert dict_of_networks["15.0.0.0"]["Protocol"] == "S" and dict_of_networks["15.0.0.0"]["Next Hop"] == "20.0.0.1"
        assert dict_of_networks["30.0.0.0"]["Protocol"] == "S" and dict_of_networks["30.0.0.0"]["Next Hop"] == "20.0.0.1"
        assert "Ex0/1" in dict_of_ports and dict_of_ports["Ex0/1"]["Role"] == "Root"

        response = DUT1.ping.ping_more("15.0.0.1", "30.0.0.1")

        assert "15.0.0.1" in response and "30.0.0.1" in response

        # Change the cost of the port Ex 0/1 (the stp will change the role of the port to ALTN) so that the traffic will be redirected trough int vlan 40.

        DUT1.stp.add_rstp_port_cost(port="Ex 0/1", cost="50000")

        time.sleep(60)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        d_root_id, d_bridge_id, ports, dict_of_ports = DUT1.stp.show_spanning_tree_rstp()
        print(dict_of_ports)

        assert "15.0.0.0" in dict_of_networks and "30.0.0.0" in dict_of_networks
        assert dict_of_networks["15.0.0.0"]["Protocol"] == "S" and dict_of_networks["15.0.0.0"]["Next Hop"] == "40.0.0.1"
        assert dict_of_networks["30.0.0.0"]["Protocol"] == "S" and dict_of_networks["30.0.0.0"]["Next Hop"] == "40.0.0.1"
        assert "Ex0/1" in dict_of_ports and dict_of_ports["Ex0/1"]["Role"] == "Alternate"

        response = DUT1.ping.ping_more("15.0.0.1", "30.0.0.1")

        assert "15.0.0.1" in response and "30.0.0.1" in response

        # Remove to cost and check that the routes are back in the initial state

        DUT1.stp.remove_rstp_port_cost(port="Ex 0/1")

        time.sleep(60)

        ip_route, networks, networks_connected, dict_of_networks = DUT1.ip.show_ip_route()
        print(dict_of_networks)

        d_root_id, d_bridge_id, ports, dict_of_ports = DUT1.stp.show_spanning_tree_rstp()
        print(dict_of_ports)

        assert "15.0.0.0" in dict_of_networks and "30.0.0.0" in dict_of_networks
        assert dict_of_networks["15.0.0.0"]["Protocol"] == "S" and dict_of_networks["15.0.0.0"]["Next Hop"] == "20.0.0.1"
        assert dict_of_networks["30.0.0.0"]["Protocol"] == "S" and dict_of_networks["30.0.0.0"]["Next Hop"] == "20.0.0.1"
        assert "Ex0/1" in dict_of_ports and dict_of_ports["Ex0/1"]["Role"] == "Root"

        response = DUT1.ping.ping_more("15.0.0.1", "30.0.0.1")

        assert "15.0.0.1" in response and "30.0.0.1" in response

        print("########## Removing the config from DUT #############")

        DUT1.ip.remove_static_route(network_dest="15.0.0.0", mask_dest="255.255.255.0", next_hop="20.0.0.1")
        DUT1.ip.remove_static_route(network_dest="15.0.0.0", mask_dest="255.255.255.0", next_hop="40.0.0.1")
        DUT1.ip.remove_static_route(network_dest="30.0.0.0", mask_dest="255.255.255.0", next_hop="20.0.0.1")
        DUT1.ip.remove_static_route(network_dest="30.0.0.0", mask_dest="255.255.255.0", next_hop="40.0.0.1")

        DUT2.ip.remove_static_route(network_dest="40.0.0.0", mask_dest="255.255.255.0", next_hop="20.0.0.2")
        DUT2.ip.remove_static_route(network_dest="40.0.0.0", mask_dest="255.255.255.0", next_hop="30.0.0.2")

        DUT3.ip.remove_static_route(network_dest="15.0.0.0", mask_dest="255.255.255.0", next_hop="30.0.0.1")
        DUT3.ip.remove_static_route(network_dest="15.0.0.0", mask_dest="255.255.255.0", next_hop="40.0.0.2")
        DUT3.ip.remove_static_route(network_dest="20.0.0.0", mask_dest="255.255.255.0", next_hop="30.0.0.1")
        DUT3.ip.remove_static_route(network_dest="20.0.0.0", mask_dest="255.255.255.0", next_hop="40.0.0.2")

        DUT1.ip.remove_vlan_interfaces("20","40")
        DUT2.ip.remove_vlan_interfaces("15","20","30")
        DUT3.ip.remove_vlan_interfaces("30", "40")

        DUT1.vl.remove_vlans("20", "40")
        DUT2.vl.remove_vlans("15", "20", "30")
        DUT3.vl.remove_vlans("30", "40")

        DUT1.int.shut_interfaces("Ex 0/1", "Gi 0/9")
        DUT2.int.shut_interfaces("Gi 0/4", "Gi 0/5", "Gi 0/9")
        DUT3.int.shut_interfaces("Gi 0/4", "Gi 0/9")





