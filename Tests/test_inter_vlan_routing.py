import time

import pytest
from config import ip, vlan, interfaces, ping
from Management import ssh

ip1 = ip.IP(ip_session="10.2.109.136")
vlan1 = vlan.VLAN(ip_session="10.2.109.136")
session1 = ssh.SSH(ip="10.2.109.136")
int1 = interfaces.Interface(ip_session="10.2.109.136")
ping1 = ping.PING(ip_session="10.2.109.136")

ip2 = ip.IP(ip_session="10.2.109.88")
vlan2 = vlan.VLAN(ip_session="10.2.109.88")
session3 = ssh.SSH(ip="10.2.109.88")
int2 = interfaces.Interface(ip_session="10.2.109.88")
ping2 = ping.PING(ip_session="10.2.109.88")


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


    assert "ok" == "ok"


