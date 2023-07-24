import time
import pytest

from config import ip, vlan, interfaces, ping
from Management import ssh

ip_session_1 = "10.2.109.238"
ip_session_2 = "10.2.109.239"

ip1 = ip.IP(ip_session=ip_session_1)
vlan1 = vlan.VLAN(ip_session=ip_session_1)
session1 = ssh.SSH(ip=ip_session_1)
int1 = interfaces.Interface(ip_session=ip_session_1)
ping1 = ping.PING(ip_session=ip_session_1)

ip2 = ip.IP(ip_session=ip_session_2)
vlan2 = vlan.VLAN(ip_session=ip_session_2)
session2 = ssh.SSH(ip=ip_session_2)
int2 = interfaces.Interface(ip_session=ip_session_2)
ping2 = ping.PING(ip_session=ip_session_2)


def test_1():

    # session1.connect()
    int1.no_shut_interface(interface="Gi 0/4")
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

    # int1.no_shut_interface(interface="Gi 0/3")
    # vlan1.create_vlan(vlan="50")
    # vlan1.add_more_ports_to_vlan("Gi 0/3", "Gi 0/4", vlan="50")
    # ip1.create_int_vlan(int_vlan="50")
    # ip1.add_ip_interface(int_vlan="50",ip="50.0.0.1",mask="255.255.0.0")

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
    ip1.add_ip_interface(int_vlan="30",ip="30.0.0.1",mask="255.255.0.0")

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
    ip1.add_ip_interface(int_vlan="20",ip="20.0.0.1",mask="255.255.0.0")

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





