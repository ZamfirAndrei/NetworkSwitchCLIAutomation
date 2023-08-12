import time
import pytest

from config import vlan, interfaces, stp
from Management import ssh

ip_session_1 = "10.2.109.206"
ip_session_2 = "10.2.109.83"

# DUT 1 Objects

int1 = interfaces.Interface(ip_session=ip_session_1)
vl1 = vlan.VLAN(ip_session=ip_session_1)
stp1 = stp.STP(ip_session=ip_session_1)

# DUT 2 Objects

int2 = interfaces.Interface(ip_session=ip_session_2)
vl2 = vlan.VLAN(ip_session=ip_session_2)
stp2 = stp.STP(ip_session=ip_session_2)


class TestRSTPSuite1:

    def test_func_1(self):

        print("###### Test_func_1 ######")
        print("########## Check if RSTP is enabled #############")

        x1 = stp1.check_stp_mode()
        x2 = stp2.check_stp_mode()

        # print(x1)
        # print(x1)

        assert "rstp" in x2["mode"]
        assert "rstp" == x1["mode"]

    def test_func_2(self):

        print("###### Test_func_2 ######")
        print("########## Check that you can change the stp mode to RSTP #############")

        stp1.changing_stp_mode(mode="pvrst")
        stp2.changing_stp_mode(mode="mst")

        x1 = stp1.check_stp_mode()
        x2 = stp2.check_stp_mode()

        print(x1)
        print(x2)

        assert "rstp" not in x1["mode"]
        assert "rstp" not in x2["mode"]

        print("##############################")

        stp1.changing_stp_mode(mode="rst")
        stp2.changing_stp_mode(mode="rst")

        x3 = stp1.check_stp_mode()
        x4 = stp2.check_stp_mode()

        assert "rstp" in x3["mode"]
        assert "rstp" in x4["mode"]

    def test_func_3(self):

        print("###### Test_func_3 ######")
        print("########## Check that you can change the RSTP brg-priority #############")

        brg_prio_1 = "4096"
        brg_prio_2 = "8192"

        stp1.add_rstp_bridge_priority(bridge_priority=brg_prio_1)
        stp2.add_rstp_bridge_priority(bridge_priority=brg_prio_2)

        x1, y1, z1 = stp1.show_spanning_tree_rstp()
        x2, y2, z2 = stp2.show_spanning_tree_rstp()

        print(y1)
        print(y2)

        assert brg_prio_1 in y1["Bridge Priority"]
        assert brg_prio_2 in y2["Bridge Priority"]

        print("########## Removing the config #############")

        stp1.remove_rstp_bridge_priority()
        stp2.remove_rstp_bridge_priority()

    def test_func_4(self):

        print("###### Test_func_4 ######")
        print("########## Check that you can change the RSTP Root Bridge #############")

        brg_prio_1 = "8192"

        int1.no_shut_interfaces("Gi 0/3", "Ex 0/1", "Ex 0/2")
        int2.no_shut_interfaces("Gi 0/5", "Gi 0/9", "Gi 0/10")

        x1, y1, z1 = stp1.show_spanning_tree_rstp()
        print(x1, y1)

        stp1.add_rstp_bridge_priority(bridge_priority=brg_prio_1)

        x1, y1, z1 = stp1.show_spanning_tree_rstp()
        print(x1, y1)

        assert x1["Root MAC-Address"] in y1["Bridge MAC-Address"]

        print("########## Removing the config #############")

        stp1.remove_rstp_bridge_priority()
        int1.shut_interfaces("Gi 0/3", "Ex 0/1", "Ex 0/2")
        int2.shut_interfaces("Gi 0/5", "Gi 0/9", "Gi 0/10")

    def test_func_5(self):

        print("###### Test_func_5 ######")
        print("########## Check that you can change the RSTP Root Bridge if the DUT is not the root #############")

        brg_prio_1 = "8192"

        int1.no_shut_interfaces("Gi 0/3", "Ex 0/1", "Ex 0/2")
        int2.no_shut_interfaces("Gi 0/5", "Gi 0/9", "Gi 0/10")

        x1, y1, z1 = stp1.show_spanning_tree_rstp()
        print(x1, y1)

        if x1["Root MAC-Address"] in y1["Bridge MAC-Address"]:

            print("This DUT is the root already")
            assert x1["Root MAC-Address"] in y1["Bridge MAC-Address"]

        else:

            stp1.add_rstp_bridge_priority(bridge_priority=brg_prio_1)

        x1, y1, z1 = stp1.show_spanning_tree_rstp()
        print(x1, y1)

        assert x1["Root MAC-Address"] in y1["Bridge MAC-Address"]

        print("########## Removing the config #############")

        stp1.remove_rstp_bridge_priority()
        int1.shut_interfaces("Gi 0/3", "Ex 0/1", "Ex 0/2")
        int2.shut_interfaces("Gi 0/5", "Gi 0/9", "Gi 0/10")



