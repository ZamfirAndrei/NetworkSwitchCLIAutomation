import time
import pytest

from config import ip, vlan, interfaces, ping
from Management import ssh

ip_session_1 = "10.2.109.238"
# ip_session_2 = "10.2.109.239"

int1 = interfaces.Interface(ip_session=ip_session_1)
vlan1 = vlan.VLAN(ip_session=ip_session_1)
ip1 = ip.IP(ip_session=ip_session_1)
ping1 = ping.PING(ip_session=ip_session_1)


def test_1():

    vlan1.create_vlan(vlan="200")
    int1.no_shut_interface(interface="Gi 0/4")

