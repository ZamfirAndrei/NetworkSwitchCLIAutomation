import pytest
from config import qinq

qinq1 = qinq.QinQ(ip_session="10.2.109.203")


class TestQinQSuite1:

    def test_func_1(self):

        bridge_mode = qinq1.show_bridge_mode()
        assert "provider-edge" in bridge_mode["Bridge Mode"]

    def test_func_2(self):

        # Verify that the ingress ethertype of a port is different than the default one

        interface = "gi 0/4"
        default_ingress_ethertype = "x88a8"
        ingress_ethertype = qinq1.show_ingress_ethertype(interface)
        assert ingress_ethertype != default_ingress_ethertype

    def test_func_3(self):

        # Verify that the egress ethertype of a port is different from the default one

        interface = "gi 0/3"
        default_egress_ethertype = "x88a8"
        egress_ethertype = qinq1.show_egress_ethertype(interface)
        assert egress_ethertype != default_egress_ethertype