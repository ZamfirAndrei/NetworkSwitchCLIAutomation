import pytest
from Management import ssh, telnet
from config import vlan

ip = "10.2.109.238"

vl = vlan.VLAN(ip_session=ip)
session = ssh.SSH(ip=ip)


def test_connection():

    a = 10
    print(a)
    assert a == 10


def test_create_vlan():

    x = "100"
    vl.create_vlan(vlan="100")
    a, b = vl.show_vlan(vlan="100")
    print(a["VLAN ID"])

    assert x == a["VLAN ID"]


def test_remove_vlan():

    x = ""
    vl.remove_vlan(vlan="100")
    a, b = vl.show_vlan(vlan="100")
    print(a)

    assert  x == a["VLAN ID"]


def test_port_add_vlan():

    ok = False
    port = "Gi 0/5"
    vl.create_vlan(vlan="100")
    vl.add_ports_to_vlan(ports=port,vlan="100")
    a,b = vl.show_vlan(vlan="100")
    print(a)
    if port.replace(" ","") in a["Member Ports"]:
        ok = True

    assert True == ok


def test_remove_port_from_vlan():

    ok = False
    port = "Gi 0/5"
    vl.remove_ports_from_vlan(ports=port,vlan="100")
    a,b = vl.show_vlan(vlan="100")
    print(a)

    if port.replace(" ","") not in a["Member Ports"]:
        ok = True

    assert True == ok
