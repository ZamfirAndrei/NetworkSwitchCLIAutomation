import time
import pytest

from config import ip, vlan, interfaces, ping
from Management import ssh

ip_session_1 = "10.2.109.203"
ip_session_2 = "10.2.109.83"


ip1 = ip.IP(ip_session=ip_session_1)
vlan1 = vlan.VLAN(ip_session=ip_session_1)
int1 = interfaces.Interface(ip_session=ip_session_1)
ping1 = ping.PING(ip_session=ip_session_1)


ip2 = ip.IP(ip_session=ip_session_2)
vlan2 = vlan.VLAN(ip_session=ip_session_2)
int2 = interfaces.Interface(ip_session=ip_session_2)
ping2 = ping.PING(ip_session=ip_session_2)


def test_1():

    int1.no_shut_interface(interface="Gi 0/5")
    vlan1.create_vlan(vlan="111")


def test_inter_vlan_routing_func_1():

    # Configure DUT 1
    int1.no_shut_interface(interface="Ex 0/1")
    int1.no_shut_interface(interface="Gi 0/3")
    vlan1.create_vlan(vlan="30")
    vlan1.create_vlan(vlan="14")
    vlan1.add_ports_to_vlan(ports="Ex 0/1", vlan="14")
    vlan1.add_ports_to_vlan(ports="Gi 0/3", vlan="30")
    ip1.create_int_vlan(int_vlan="30")
    ip1.create_int_vlan(int_vlan="14")
    ip1.add_ip_interface(int_vlan="30", ip="30.0.0.1", mask="255.255.255.0")
    ip1.add_ip_interface(int_vlan="14", ip="14.0.0.2", mask="255.255.255.0")
    ip1.add_static_route(network_dest="15.0.0.0", mask_dest="255.255.255.0", next_hop="14.0.0.1")

    print("####################################")

    # Configure DUT 2

    int2.no_shut_interface(interface="Gi 0/5")
    int2.no_shut_interface(interface="Gi 0/9")
    vlan2.create_vlan(vlan="15")
    vlan2.create_vlan(vlan="14")
    vlan2.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
    vlan2.add_ports_to_vlan(ports="Gi 0/9", vlan="14")
    ip2.create_int_vlan(int_vlan="15")
    ip2.create_int_vlan(int_vlan="14")
    ip2.add_ip_interface(int_vlan="15", ip="15.0.0.1", mask="255.255.255.0")
    ip2.add_ip_interface(int_vlan="14", ip="14.0.0.1", mask="255.255.255.0")
    ip2.add_static_route(network_dest="30.0.0.0", mask_dest="255.255.255.0", next_hop="14.0.0.2")

    print("####################################")

    resp = ping1.ping(ip_dest="15.0.0.100")
    time.sleep(2)
    print(resp)

    assert "15.0.0.100" in resp


def test_inter_vlan_routing_func_2():

    int1.no_shut_interface(interface="Ex 0/1")
    int1.no_shut_interface(interface="Gi 0/4")
    vlan1.create_vlan(vlan="66")
    vlan1.create_vlan(vlan="14")
    vlan1.add_ports_to_vlan(ports="Ex 0/1", vlan="14")
    vlan1.add_ports_to_vlan(ports="Gi 0/4", vlan="66")
    ip1.create_int_vlan(int_vlan="66")
    ip1.create_int_vlan(int_vlan="14")
    ip1.add_ip_interface(int_vlan="66", ip="66.0.0.1", mask="255.255.255.0")
    ip1.add_ip_interface(int_vlan="14", ip="14.0.0.2", mask="255.255.255.0")
    ip1.add_static_route(network_dest="16.0.0.0", mask_dest="255.255.255.0", next_hop="14.0.0.1")

    print("####################################")

    int2.no_shut_interface(interface="Gi 0/6")
    int2.no_shut_interface(interface="Gi 0/9")
    vlan2.create_vlan(vlan="16")
    vlan2.create_vlan(vlan="14")
    vlan2.add_ports_to_vlan(ports="Gi 0/6", vlan="16")
    vlan2.add_ports_to_vlan(ports="Gi 0/9", vlan="14")
    ip2.create_int_vlan(int_vlan="16")
    ip2.create_int_vlan(int_vlan="14")
    ip2.add_ip_interface(int_vlan="16", ip="16.0.0.1", mask="255.255.255.0")
    ip2.add_ip_interface(int_vlan="14", ip="14.0.0.1", mask="255.255.255.0")
    ip2.add_static_route(network_dest="66.0.0.0", mask_dest="255.255.255.0", next_hop="14.0.0.2")

    print("####################################")

    resp = ping1.ping(ip_dest="16.0.0.100")
    time.sleep(2)
    print(resp)

    assert "16.0.0.100" in resp


def test_inter_vlan_routing_func_3():

    int1.no_shut_interface(interface="Gi 0/3")
    vlan1.create_vlan(vlan="50")
    vlan1.add_more_ports_to_vlan("Gi 0/3", "Gi 0/4", vlan="50")
    ip1.create_int_vlan(int_vlan="50")
    ip1.add_ip_interface(int_vlan="50", ip="50.0.0.1", mask="255.255.0.0")

    a, b, c = int1.show_int_description()
    # print(a, b, c)
    list_of_int_vlans = list()
    x, y, z = "", "", ""

    for i in c:
        print(i)
        print(i["Interface"], i["Status"], i["Protocol"])
        list_of_int_vlans.append([i["Interface"], i["Status"], i["Protocol"]])

    print(list_of_int_vlans)

    for inter in list_of_int_vlans:

        print(inter)

        if "vlan50" in inter:

            print(inter[0], inter[1], inter[2])
            x, y, z = inter[0], inter[1], inter[2]
            break

    assert x == "vlan50" and y == "Up" and z == "Up"


def test_inter_vlan_routing_func_4():

    int1.no_shut_interface(interface="Gi 0/3")
    vlan1.create_vlan(vlan="30")
    vlan1.add_more_ports_to_vlan("Gi 0/3", "Gi 0/4", vlan="30")
    ip1.create_int_vlan(int_vlan="30")
    ip1.add_ip_interface(int_vlan="30", ip="30.0.0.1", mask="255.255.0.0")

    a, b, c = int1.show_int_description()
    ok = False

    for elem in c:
        if "vlan1" in elem.values():
            print(f"Found in {elem}")
            ok = True

    assert ok is True


def test_inter_vlan_routing_func_5():

    int1.no_shut_interface(interface="Gi 0/3")
    vlan1.create_vlan(vlan="20")
    vlan1.add_more_ports_to_vlan("Gi 0/3", "Gi 0/4", vlan="20")
    ip1.create_int_vlan(int_vlan="20")
    ip1.add_ip_interface(int_vlan="20", ip="20.0.0.1", mask="255.255.0.0")

    vlan = "vlan1"
    a, b, c = int1.show_int_description()
    ok = False

    for elem in c:
        if vlan in elem.values():
            print(elem["Status"], elem["Protocol"])

            if elem["Status"] == "Down":

                print(f"Found in {elem}")
                ok = True

    assert ok is True


def test_inter_vlan_routing_func_6():

    vl = "60"
    ip1.create_int_vlan(int_vlan=vl)
    ip1.add_ip_interface(int_vlan=vl, ip="60.0.0.1", mask="255.255.0.0")
    a, b, c = ip1.show_ip_int(int_vlan=vl)
    print(a,b,c)

    assert "vlan50" not in a.values()


def test_inter_vlan_routing_func_7():

    vl = "60"
    ip1.create_int_vlan(int_vlan=vl)
    ip1.add_ip_interface(int_vlan=vl, ip="60.0.0.1", mask="255.255.0.0")
    a, b, c = ip1.show_ip_int(int_vlan=vl)
    print(a,b,c)

    assert "vlan"+vl in a.values()


def test_inter_vlan_routing_func_8():

    vl = "50"
    ip1.create_int_vlan(int_vlan=vl)
    ip1.add_ip_interface(int_vlan=vl, ip="50.0.0.1", mask="255.255.255.0")
    vlan1.add_more_ports_to_vlan("Gi 0/3", "Gi 0/4", vlan=vl)
    int1.no_shut_interface(interface="Gi 0/3")
    int1.no_shut_interface(interface="Gi 0/4")

    a, b, c = ip1.show_ip_int(int_vlan=vl)
    print(a,b,c)

    assert a["Interface Vlan"] == "vlan"+vl
    assert a["The Interface is"] == "up"
    assert a["Line Protocol is"] == "up"


def test_inter_vlan_routing_func_9():

    vl = "14"
    # Configuring DUT1

    vlan1.create_vlan(vlan=vl)
    vlan1.add_ports_to_vlan(ports="Ex 0/1", vlan=vl)
    int1.no_shut_interface(interface="Ex 0/1")
    ip1.create_int_vlan(int_vlan=vl)
    ip1.add_ip_interface(int_vlan=vl, ip="14.0.0.2", mask="255.255.255.0")

    # Configuring DUT2

    vlan2.create_vlan(vlan=vl)
    vlan2.add_ports_to_vlan(ports="Gi 0/9", vlan=vl)
    int2.no_shut_interface(interface="Gi 0/9")
    ip2.create_int_vlan(int_vlan=vl)
    ip2.add_ip_interface(int_vlan=vl, ip="14.0.0.1", mask="255.255.255.0")

    # Checking connectivity

    resp = ping1.ping(ip_dest="14.0.0.2")
    # print(resp)

    assert "14.0.0.2" in resp


def test_inter_vlan_routing_func_10():

    vl = "30"
    # Configuring DUT1

    vlan1.create_vlan(vlan=vl)
    vlan1.add_ports_to_vlan(ports="Gi 0/3", vlan=vl)
    int1.no_shut_interface(interface="Gi 0/3")
    ip1.create_int_vlan(int_vlan=vl)
    ip1.add_ip_interface(int_vlan=vl, ip="30.0.0.1", mask="255.255.255.0")

    # Checking connectivity

    resp1 = ping1.ping(ip_dest="30.0.0.100")
    # print(resp)
    resp2 = ping1.ping(ip_dest="30.0.0.77")
    # print(resp)

    assert "30.0.0.100" in resp1
    assert "30.0.0.88" not in resp2


def test_inter_vlan_routing_func_11():

    ip1.add_ip_interfaces("100", "110", int_vlan1_ip=["100.0.0.1","255.255.255.0"], int_vlan2_ip=["110.0.0.1","255.255.255.0"])
    ip1.no_shut_int_vlans("100", "110")
    ok = False
    a, b, c = int1.show_int_description()
    print(c)

    for item in c:
        # print(item)
        if item["Interface"] == "vlan100" and item["Status"] == "Up":
            print(item)
            ok = True

    assert ok is True

    x, y, z = ip1.show_ip_int(int_vlan="100")
    print(x, y, z)
    assert x["Interface Vlan"] == "vlan100"
    assert x["The Interface is"] == "up"
    assert x["IP Address"] == "100.0.0.1"
    assert x["Mask"] == "24"

    x1, y1, z1 = ip1.show_ip_int(int_vlan="110")
    print(x1, y1, z1)
    assert x1["Interface Vlan"] == "vlan110"
    assert x1["The Interface is"] == "up"
    assert x1["IP Address"] == "110.0.0.1"
    assert x1["Mask"] == "24"


def test_inter_vlan_routing_func_12():

    # Checking routing between routed ports

    # Configuring DUT 1

    int1.add_routed_port(interface="Ex 0/2")
    ip1.add_ip_routed_port(interface="Ex 0/2", ip="20.0.0.2", mask="255.255.0.0")
    int1.no_shut_interface(interface="Ex 0/2")

    int1.add_routed_port(interface="Gi 0/4")
    ip1.add_ip_routed_port(interface="Gi 0/4", ip="60.0.0.1", mask="255.255.0.0")
    int1.no_shut_interface(interface="Gi 0/4")

    # Configuring DUT 2

    int2.add_routed_port(interface="Gi 0/10")
    ip2.add_ip_routed_port(interface="Gi 0/10", ip="20.0.0.1", mask="255.255.0.0")
    int2.no_shut_interface(interface="Gi 0/10")

    int2.add_routed_port(interface="Gi 0/6")
    ip2.add_ip_routed_port(interface="Gi 0/6", ip="6.0.0.1", mask="255.255.0.0")
    int2.no_shut_interface(interface="Gi 0/6")

    vlan2.create_vlan(vlan="15")
    vlan2.add_ports_to_vlan(ports="Gi 0/5", vlan="15")
    ip2.create_int_vlan(int_vlan="15")
    ip2.add_ip_interface(int_vlan="15", ip="15.0.0.1", mask="255.255.255.0")

    # Configuring the static routes

    ip1.add_static_route(network_dest="6.0.0.0", next_hop="20.0.0.1", mask_dest="255.255.0.0")
    ip2.add_static_route(network_dest="60.0.0.0", next_hop="20.0.0.2", mask_dest="255.255.0.0")

    ip1.add_static_route(network_dest="15.0.0.0", next_hop="20.0.0.1", mask_dest="255.255.255.0")

    # Checking connectivity

    resp1 = ping1.ping(ip_dest="6.0.0.100")
    resp2 = ping2.ping(ip_dest="60.0.0.100")
    resp3 = ping1.ping(ip_dest="15.0.0.100")

    print(resp1)
    print(resp2)
    print(resp3)

    assert "6.0.0.100" in resp1
    assert "60.0.0.100" in resp2
    assert "15.0.0.100" in resp3


def test_inter_vlan_routing_func_13():

    # int1.add_routed_ports("Gi 0/3", "Gi 0/4")
    # ip1.add_ip_routed_ports("Gi 0/3", "Gi 0/4", routed_port_1=["100.0.0.1","255.255.0.0"], routed_port_2=["110.0.0.1","255.255.0.0"])
    # ip1.remove_ip_routed_ports("Gi 0/3", "Gi 0/4")
    # int1.remove_routed_ports("Gi 0/3", "Gi 0/4")