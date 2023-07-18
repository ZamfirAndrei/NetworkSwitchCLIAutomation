import pytest

from Management import ssh, telnet
from config import ping

session = ssh.SSH(ip="10.2.109.136")
obj_ping = ping.PING(ip_session="10.2.109.136")


def test_func_1():

    ip_dest = "15.0.0.1"
    resp = obj_ping.ping(ip_dest)
    print(resp)

    assert ip_dest in resp


def test_func_2():

    ip_dest = "15.0.0.88"
    resp = obj_ping.ping(ip_dest)
    print(resp)

    assert ip_dest not in resp


def test_func_3():

    ip_dest = ["15.0.0.88","16.0.0.100","6.0.0.16"]
    list_of_resp = list()
    for ip in ip_dest:
        resp = obj_ping.ping(ip)
        print(resp)
        for i in resp:
            list_of_resp.append(i)
    print(list_of_resp)

    for ip in ip_dest:
        assert ip not in list_of_resp


def test_func_4():

    ip_dest = ["15.0.0.1","6.0.0.1","14.0.0.1"]
    list_of_resp = list()
    for ip in ip_dest:
        resp = obj_ping.ping(ip)
        print(resp)
        for i in resp:
            list_of_resp.append(i)
    print(list_of_resp)

    for ip in ip_dest:
        assert ip in list_of_resp