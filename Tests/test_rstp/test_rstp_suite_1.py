import time
import pytest
import pytest_html
import sys


from config import vlan, interfaces, stp, fdb
from Management import ssh

ip_session_1 = "10.2.109.206"
ip_session_2 = "10.2.109.83"
ip_session_3 = "10.2.109.232"

# DUT 1 Objects

int1 = interfaces.Interface(ip_session=ip_session_1)
vl1 = vlan.VLAN(ip_session=ip_session_1)
stp1 = stp.STP(ip_session=ip_session_1)
fdb1 = fdb.FDB(ip_session=ip_session_1)

# DUT 2 Objects

int2 = interfaces.Interface(ip_session=ip_session_2)
vl2 = vlan.VLAN(ip_session=ip_session_2)
stp2 = stp.STP(ip_session=ip_session_2)
fdb2 = fdb.FDB(ip_session=ip_session_2)

# DUT 3 Objects

int3 = interfaces.Interface(ip_session=ip_session_3)
vl3 = vlan.VLAN(ip_session=ip_session_3)
stp3 = stp.STP(ip_session=ip_session_3)
fdb3 = fdb.FDB(ip_session=ip_session_3)


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
        print("########### 2 DUTs ########### ")

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
        print("########### 2 DUTs ########### ")

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

    def test_func_6(self):

        print("###### Test_func_6 ######")
        print("########## Check that you can change the cost of a link when RSTP is enabled #############")

        cost1 = "10"
        cost2 = "20"

        port1 = "Gi 0/3"
        port2 = "Gi 0/5"

        ok1 = False
        ok2 = False

        int1.no_shut_interfaces("Gi 0/3", "Ex 0/1", "Ex 0/2")
        int2.no_shut_interfaces("Gi 0/5", "Gi 0/9", "Gi 0/10")

        stp1.add_rstp_port_cost(port=port1, cost=cost1)
        x1, y1, z1 = stp1.show_spanning_tree_rstp()
        print(z1)

        for port in z1:

            # print(port)
            # print("1")

            if port["Name"] == port1.replace(" ","") and port["Cost"] == cost1:

                # print("2")
                ok1 = True

        assert ok1 is True

        stp2.add_rstp_port_cost(port=port2, cost=cost2)
        x1, y1, z1 = stp2.show_spanning_tree_rstp()
        print(z1)

        for port in z1:

            # print("1")

            if port["Name"] == port2.replace(" ","") and port["Cost"] == cost2:

                # print("2")
                ok2 = True

        assert ok2 is True

        print("########## Removing the config #############")

        int1.shut_interfaces("Gi 0/3", "Ex 0/1", "Ex 0/2")
        int2.shut_interfaces("Gi 0/5", "Gi 0/9", "Gi 0/10")
        stp1.remove_rstp_port_cost(port=port1)
        stp2.remove_rstp_port_cost(port=port2)

    def test_func_7(self):

        print("###### Test_func_7 ######")
        print("########## Check that you can change the port-priority of a link when RSTP is enabled #############")

        port_prio_1 = "16"
        port_prio_2 = "32"

        port1 = "Gi 0/3"
        port2 = "Gi 0/5"

        ok1 = False
        ok2 = False

        int1.no_shut_interfaces("Gi 0/3", "Ex 0/1", "Ex 0/2")
        int2.no_shut_interfaces("Gi 0/5", "Gi 0/9", "Gi 0/10")

        stp1.add_rstp_port_priority(port=port1, port_priority=port_prio_1)
        x1, y1, z1 = stp1.show_spanning_tree_rstp()
        print(z1)

        for port in z1:

            # print(port)
            # print("1")

            if port["Name"] == port1.replace(" ","") and port["Prio"] == port_prio_1:

                # print("2")
                ok1 = True

        assert ok1 is True

        stp2.add_rstp_port_priority(port=port2, port_priority=port_prio_2)
        x1, y1, z1 = stp2.show_spanning_tree_rstp()
        print(z1)

        for port in z1:

            # print("1")

            if port["Name"] == port2.replace(" ","") and port["Prio"] == port_prio_2:

                # print("2")
                ok2 = True

        assert ok2 is True

        print("########## Removing the config #############")

        int1.shut_interfaces("Gi 0/3", "Ex 0/1", "Ex 0/2")
        int2.shut_interfaces("Gi 0/5", "Gi 0/9", "Gi 0/10")
        stp1.remove_rstp_port_priority(port=port1)
        stp2.remove_rstp_port_priority(port=port2)

    def test_func_8(self):

        print("###### Test_func_8 ######")
        print("########## Check that you can influence the path changing the cost of a link  #############")
        print("########### 2 DUTs ########### ")

        cost1 = "10"
        port1 = "Ex 0/2"

        ok1 = False

        int1.no_shut_interfaces("Gi 0/3", "Ex 0/1", "Ex 0/2")
        int2.no_shut_interfaces("Gi 0/5", "Gi 0/9", "Gi 0/10")

        x1, y1, z1 = stp1.show_spanning_tree_rstp()
        print(z1)

        for port in z1:

            # print(port)
            # print("1")

            if port["Name"] == port1.replace(" ","") and port["Role"] == "Alternate":

                # print("2")
                stp1.add_rstp_port_cost(port=port1, cost=cost1)
                break

        x1, y1, z1 = stp1.show_spanning_tree_rstp()
        print(z1)

        for port in z1:

            # print("1")

            if port["Name"] == port1.replace(" ","") and port["Role"] == "Root":

                # print("2")
                ok1 = True

        assert ok1 is True

        print("########## Removing the config #############")

        int1.shut_interfaces("Gi 0/3", "Ex 0/1", "Ex 0/2")
        int2.shut_interfaces("Gi 0/5", "Gi 0/9", "Gi 0/10")
        stp1.remove_rstp_port_cost(port=port1)

    def test_func_9(self):

        print("###### Test_func_9 ######")
        print("########## Check that you can influence the path changing the port-priority of a link on remote DUT #############")
        print("########### 2 DUTs ########### ")

        port_prio_2 = "16"
        port2 = "Gi 0/10"
        # port1_1 = "Ex 0/1"
        port1_2 = "Ex 0/2"

        ok1 = False

        int1.no_shut_interfaces("Gi 0/3", "Ex 0/1", "Ex 0/2")
        int2.no_shut_interfaces("Gi 0/5", "Gi 0/9", "Gi 0/10")

        x1, y1, z1 = stp1.show_spanning_tree_rstp()
        print(z1)

        for port in z1:

            # print(port)
            # print("1")

            if port["Name"] == port1_2.replace(" ","") and port["Role"] == "Alternate" :

                # print("2")
                stp2.add_rstp_port_priority(port=port2, port_priority=port_prio_2)
                print("We added port-priority on the link of the remote DUT")
                break

        x1, y1, z1 = stp1.show_spanning_tree_rstp()
        print(z1)

        for port in z1:

            # print("1")

            if port["Name"] == port1_2.replace(" ","") and port["Role"] == "Root":

                # print("2")
                ok1 = True

        assert ok1 is True

        print("########## Removing the config #############")

        int1.shut_interfaces("Gi 0/3", "Ex 0/1", "Ex 0/2")
        int2.shut_interfaces("Gi 0/5", "Gi 0/9", "Gi 0/10")
        stp2.remove_rstp_port_priority(port=port2)

    def test_func_10(self):

        print("###### Test_func_10 ######")
        print("########## Check that you can influence the Root Bridge in setup of more DUTs #############")
        print("########### 3 DUTs ########### ")

        brg_prio = "4096"

        int1.no_shut_interfaces("Gi 0/3", "Ex 0/1", "Gi 0/9")
        int2.no_shut_interfaces("Gi 0/4", "Gi 0/5", "Gi 0/9")
        int3.no_shut_interfaces("Gi 0/4", "Gi 0/9")
        stp2.stp_disable(port="Gi 0/1")  # Link towards CambiumLAB
        time.sleep(2)

        root1 = stp1.show_spanning_tree_root()
        root2 = stp1.show_spanning_tree_root()
        root3 = stp1.show_spanning_tree_root()

        print(root1)
        print(root2)
        print(root3)

        assert root1[0] == root2[0] == root3[0]

        stp2.add_rstp_bridge_priority(bridge_priority=brg_prio)
        time.sleep(2)

        root1_1 = stp1.show_spanning_tree_root()
        root2_1 = stp1.show_spanning_tree_root()
        root3_1 = stp1.show_spanning_tree_root()

        print(root1_1)
        print(root2_1)
        print(root3_1)

        assert root1_1[0] == root2_1[0] == root3_1[0] and root1_1[0] != root1
        stp2.remove_rstp_bridge_priority()

        stp3.add_rstp_bridge_priority(bridge_priority=brg_prio)
        time.sleep(2)

        root1_2 = stp1.show_spanning_tree_root()
        root2_2 = stp1.show_spanning_tree_root()
        root3_2 = stp1.show_spanning_tree_root()

        print(root1_2)
        print(root2_2)
        print(root3_2)

        assert root1_2[0] == root2_2[0] == root3_2[0] and (root1_2[0] != root1_1[0]) and (root1_2 != root1[0])
        stp3.remove_rstp_bridge_priority()
        time.sleep(2)

        # Going back to default settings and checking if the root is the default one

        root1_3 = stp1.show_spanning_tree_root()
        root2_3 = stp1.show_spanning_tree_root()
        root3_3 = stp1.show_spanning_tree_root()

        print(root1_3)
        print(root2_3)
        print(root3_3)

        assert root1_3[0] == root2_3[0] == root3_3[0] == root1[0]

        print("########## Removing the config #############")

        int1.shut_interfaces("Gi 0/3", "Ex 0/1", "Gi 0/9")
        int2.shut_interfaces("Gi 0/4", "Gi 0/5", "Gi 0/9")
        int3.shut_interfaces("Gi 0/4", "Gi 0/9")
        stp2.stp_enable(port="Gi 0/1")

    def test_func_11(self):

        print("###### Test_func_11 ######")
        print("########## Check that you can influence the path towards Root Bridge in setup of more DUTs #############")
        print("########### 3 DUTs ########### ")

        cost = "50000"
        input_string = ""
        output_string = ""
        ok = False

        alternate_ports = list()
        root_ports = list()

        d1 = dict()
        d2 = dict()
        d3 = dict()

        int1.no_shut_interfaces("Gi 0/3", "Ex 0/1", "Gi 0/9")
        int2.no_shut_interfaces("Gi 0/4", "Gi 0/5", "Gi 0/9")
        int3.no_shut_interfaces("Gi 0/4", "Gi 0/9")
        stp2.stp_disable(port="Gi 0/1")  # Link towards CambiumLAB
        time.sleep(2)

        x1, y1, z1 = stp1.show_spanning_tree_rstp()
        x2, y2, z2 = stp2.show_spanning_tree_rstp()
        x3, y3, z3 = stp3.show_spanning_tree_rstp()

        print(z1)
        print(z2)
        print(z3)

        for port in z1:

            if port["Role"] == "Alternate":

                print(port["Name"])
                d1["Alternate"] = port["Name"]
                d1["Alternate-Cost"] = port["Cost"]
                alternate_ports.append([port["Name"], "DUT1"])

            elif port["Role"] == "Root":

                print(port["Name"])
                d1["Root"] = port["Name"]
                d1["Root-Cost"] = port["Cost"]
                root_ports.append([port["Name"], "DUT1"])

        for port in z2:

            if port["Role"] == "Alternate":

                print(port["Name"])
                d2["Alternate"] = port["Name"]
                d2["Alternate-Cost"] = port["Cost"]
                alternate_ports.append([port["Name"], "DUT2"])

            elif port["Role"] == "Root":

                print(port["Name"])
                d2["Root"] = port["Name"]
                d2["Root-Cost"] = port["Cost"]
                root_ports.append([port["Name"], "DUT2"])

        for port in z3:

            if port["Role"] == "Alternate":

                print(port["Name"])
                d3["Alternate"] = port["Name"]
                d3["Alternate-Cost"] = port["Cost"]
                alternate_ports.append([port["Name"], "DUT3"])

            elif port["Role"] == "Root":

                print(port["Name"])
                d3["Root"] = port["Name"]
                d3["Root-Cost"] = port["Cost"]
                root_ports.append([port["Name"], "DUT3"])

        # print(d1)
        # print(d2)
        # print(d3)
        print("################")
        print(alternate_ports)
        print(root_ports)
        # print(root_ports[0][0])
        # print(d1.keys())
        # print(d2.keys())
        # print(d3.keys())

        if "Alternate" in d1.keys() and "Root" in d1.keys():

            # print(d1)
            # print("1")
            # Slicing the string and adding " " between the first 2 chars and the rest. Ex: Gi0/9 -> Gi 0/9

            input_string = d1["Root"]
            output_string = input_string[:2] + " " + input_string[2:]
            print(output_string)
            stp1.add_rstp_port_cost(port=output_string, cost=cost)

        if "Alternate" in d2.keys() and "Root" in d2.keys():

            # print(d2)
            # print("2")
            # Slicing the string and adding " " between the first 2 chars and the rest. Ex: Gi0/9 -> Gi 0/9

            input_string = d2["Root"]
            output_string = input_string[:2] + " " + input_string[2:]
            print(output_string)
            stp2.add_rstp_port_cost(port=output_string, cost=cost)

        if "Alternate" in d3.keys() and "Root" in d3.keys():

            # print(d3)
            # print("3")
            # Slicing the string and adding " " between the first 2 chars and the rest. Ex: Gi0/9 -> Gi 0/9

            input_string = d3["Root"]
            output_string = input_string[:2] + " " + input_string[2:]
            print(output_string)
            stp3.add_rstp_port_cost(port=output_string, cost=cost)

        x1, y1, z1 = stp1.show_spanning_tree_rstp()
        x2, y2, z2 = stp2.show_spanning_tree_rstp()
        x3, y3, z3 = stp3.show_spanning_tree_rstp()

        print(z1)
        print(z2)
        print(z3)

        # Checking that the port cost has been changed and the role transits from Root to Alternate

        for port in z1:

            if port["Name"] == output_string.replace(" ","") and port["Role"] == "Alternate" and port["Cost"] == cost:

                print(port["Name"])
                ok = True

        for port in z2:

            if port["Name"] == output_string.replace(" ","") and port["Role"] == "Alternate" and port["Cost"] == cost:

                print(port["Name"])
                ok = True

        for port in z3:

            if port["Name"] == output_string.replace(" ", "") and port["Role"] == "Alternate" and port["Cost"] == cost:
                print(port["Name"])
                ok = True

        assert ok is True

        print("########## Removing the config #############")

        int1.shut_interfaces("Gi 0/3", "Ex 0/1", "Gi 0/9")
        int2.shut_interfaces("Gi 0/4", "Gi 0/5", "Gi 0/9")
        int3.shut_interfaces("Gi 0/4", "Gi 0/9")
        stp2.stp_enable(port="Gi 0/1")
        stp3.remove_rstp_port_cost(port="Gi 0/9")

    def test_func_12(self):

        print("###### Test_func_12 ######")
        print("########## Check that you can influence the path towards Root Bridge in setup of more DUTs vers2 #############")
        print("########### 3 DUTs ########### ")

        cost = "50000"
        input_string = ""
        output_string = ""
        dut1 = False
        dut2 = False
        dut3 = False

        list_ports_DUT_1 = list()
        list_ports_DUT_2 = list()
        list_ports_DUT_3 = list()

        int1.no_shut_interfaces("Gi 0/3", "Ex 0/1", "Gi 0/9")
        int2.no_shut_interfaces("Gi 0/4", "Gi 0/5", "Gi 0/9")
        int3.no_shut_interfaces("Gi 0/4", "Gi 0/9")
        stp2.stp_disable(port="Gi 0/1")  # Link towards CambiumLAB
        time.sleep(2)

        x1, y1, z1 = stp1.show_spanning_tree_rstp()
        x2, y2, z2 = stp2.show_spanning_tree_rstp()
        x3, y3, z3 = stp3.show_spanning_tree_rstp()

        for port in z1:

            if port["Role"] == "Alternate":

                list_ports_DUT_1.append([port["Name"], port["Cost"], port["Role"]])

            elif port["Role"] == "Root":

                list_ports_DUT_1.append([port["Name"], port["Cost"], port["Role"]])

        for port in z2:

            if port["Role"] == "Alternate":

                list_ports_DUT_2.append([port["Name"], port["Cost"], port["Role"]])

            elif port["Role"] == "Root":

                list_ports_DUT_2.append([port["Name"], port["Cost"], port["Role"]])

        for port in z3:

            if port["Role"] == "Alternate":

                list_ports_DUT_3.append([port["Name"], port["Cost"], port["Role"]])

            elif port["Role"] == "Root":

                list_ports_DUT_3.append([port["Name"], port["Cost"], port["Role"]])

        print(list_ports_DUT_1)
        print(list_ports_DUT_2)
        print(list_ports_DUT_3)

        len_max = max(len(list_ports_DUT_1), len(list_ports_DUT_2), len(list_ports_DUT_3))
        print(len_max)

        if len(list_ports_DUT_1) > len(list_ports_DUT_2) and len(list_ports_DUT_1) > len(list_ports_DUT_3):

            for port in list_ports_DUT_1:

                if port[2] == "Root":

                    input_string = port[0]
                    output_string = input_string[:2] + " " + input_string[2:]
                    print(output_string)
                    stp1.add_rstp_port_cost(port=output_string, cost=cost)
                    dut1 = True

        if len(list_ports_DUT_2) > len(list_ports_DUT_1) and len(list_ports_DUT_2) > len(list_ports_DUT_3):

            for port in list_ports_DUT_2:

                if port[2] == "Root":

                    input_string = port[0]
                    output_string = input_string[:2] + " " + input_string[2:]
                    print(output_string)
                    stp2.add_rstp_port_cost(port=output_string, cost=cost)
                    dut2 = True

        if len(list_ports_DUT_3) > len(list_ports_DUT_1) and len(list_ports_DUT_3) > len(list_ports_DUT_2):

            for port in list_ports_DUT_3:

                if port[2] == "Root":

                    input_string = port[0]
                    output_string = input_string[:2] + " " + input_string[2:]
                    print(output_string)
                    stp3.add_rstp_port_cost(port=output_string, cost=cost)
                    dut3 = True

        # Checking that the port cost has been changed and the role transits from Root to Alternate

        if dut1 is True:

            x1, y1, z1 = stp1.show_spanning_tree_rstp()
            print(z1)

            for port in z1:

                if port["Name"] == output_string.replace(" ",""):

                    assert port["Role"] == "Alternate"
                    assert port["Cost"] == cost

        if dut2 is True:

            x2, y2, z2 = stp2.show_spanning_tree_rstp()
            print(z2)

            for port in z2:

                if port["Name"] == output_string.replace(" ",""):

                    assert port["Role"] == "Alternate"
                    assert port["Cost"] == cost

        if dut3 is True:

            x3, y3, z3 = stp3.show_spanning_tree_rstp()
            print(z3)

            for port in z3:

                if port["Name"] == output_string.replace(" ",""):

                    assert port["Role"] == "Alternate"
                    assert port["Cost"] == cost

        print("########## Removing the config #############")

        int1.shut_interfaces("Gi 0/3", "Ex 0/1", "Gi 0/9")
        int2.shut_interfaces("Gi 0/4", "Gi 0/5", "Gi 0/9")
        int3.shut_interfaces("Gi 0/4", "Gi 0/9")
        stp2.stp_enable(port="Gi 0/1")
        stp3.remove_rstp_port_cost(port="Gi 0/9")

    def test_func_13(self):

        print("###### Test_func_13 ######")
        print("########## Check that you can influence the path towards Root Bridge in setup of more DUTs vers3 #############")
        print("########### 3 DUTs ########### ")

        cost = "60000"
        default_cost = "20000"
        port_output = ""

        int1.no_shut_interfaces("Gi 0/3", "Ex 0/1", "Gi 0/9")
        int2.no_shut_interfaces("Gi 0/4", "Gi 0/5", "Gi 0/9")
        int3.no_shut_interfaces("Gi 0/4", "Gi 0/9")
        stp2.stp_disable(port="Gi 0/1")  # Link towards CambiumLAB
        time.sleep(2)

        d_root_id, d_bridge_id, ports = stp3.show_spanning_tree_rstp()
        print(ports)

        for port in ports:

            if port["Role"] == "Root":

                port_output = port["Name"][:2] + " " + port["Name"][2:]
                print(port_output)
                stp3.add_rstp_port_cost(port=port_output, cost=cost)

        d_root_id, d_bridge_id, ports = stp3.show_spanning_tree_rstp()
        print(ports)

        for port in ports:

            if port["Name"] == "Gi0/9":

                print("####### 1 ########")
                print(port["Name"])
                assert port["Role"] == "Alternate"
                assert port["Cost"] == cost

        # Going back to default and checking that everything is behaving as expected

        stp3.remove_rstp_port_cost(port=port_output)
        d_root_id, d_bridge_id, ports = stp3.show_spanning_tree_rstp()
        print(ports)

        for port in ports:

            if port["Name"] == "Gi0/9":

                print("####### 2 ########")
                print(port["Name"])
                assert port["Role"] == "Root"
                assert port["Cost"] == default_cost

        print("########## Removing the config #############")

        int1.shut_interfaces("Gi 0/3", "Ex 0/1", "Gi 0/9")
        int2.shut_interfaces("Gi 0/4", "Gi 0/5", "Gi 0/9")
        int3.shut_interfaces("Gi 0/4", "Gi 0/9")
        stp2.stp_enable(port="Gi 0/1")

    def test_func_14(self):

        print("###### Test_func_14 ######")
        print("########## Check that RSTP is still working after shutting down a link #############")
        print("########### 3 DUTs ########### ")

        port_output = ""
        ok = False

        int1.no_shut_interfaces("Gi 0/3", "Ex 0/1", "Gi 0/9")
        int2.no_shut_interfaces("Gi 0/4", "Gi 0/5", "Gi 0/9")
        int3.no_shut_interfaces("Gi 0/4", "Gi 0/9")
        stp2.stp_disable(port="Gi 0/1")  # Link towards CambiumLAB
        time.sleep(2)

        d_root_id, d_bridge_id, ports = stp3.show_spanning_tree_rstp()
        print(ports)
        len1 = len(ports)

        # Shut down the Root Port from the Non-Root DUT

        for port in ports:

            if port["Role"] == "Root":

                port_output = port["Name"][:2] + " " + port["Name"][2:]
                print(port_output)
                int3.shut_interface(interface=port_output)

        # Check the other port of Non-Root DUT. From Alternate --> Root and the shuted port is missing from the ports

        d_root_id, d_bridge_id, ports = stp3.show_spanning_tree_rstp()
        print(ports)
        len2 = len(ports)

        # for port in ports:
        #
        #     if port["Name"] == port_output.replace(" ",""):
        #
        #         print("We found the port")
        #         ok = False
        #
        #     else:
        #
        #         print("We did not find the port")
        #         ok = True

        # assert ok is true
        assert len1 - len2 == 1

        # Getting back to the default setup

        int3.no_shut_interface(interface=port_output)

        d_root_id, d_bridge_id, ports = stp3.show_spanning_tree_rstp()
        print(ports)
        len3 = len(ports)

        assert len3 == len1

        print("########## Removing the config #############")

        int1.shut_interfaces("Gi 0/3", "Ex 0/1", "Gi 0/9")
        int2.shut_interfaces("Gi 0/4", "Gi 0/5", "Gi 0/9")
        int3.shut_interfaces("Gi 0/4", "Gi 0/9")
        stp2.stp_enable(port="Gi 0/1")

    def test_func_15(self):

        print("###### Test_func_15 ######")
        print("########## Check that RSTP is still working after shutting down a link when is traffic from ixia #############")
        print("########### 3 DUTs ########### ")

        stream_mac_source = "00:00:00:00:aa:bb"
        stream_vlan = "88"
        vlan = "88"

        port_root = ""

        int1.no_shut_interfaces("Gi 0/3", "Ex 0/1", "Gi 0/9")
        int2.no_shut_interfaces("Gi 0/4", "Gi 0/5", "Gi 0/9")
        int3.no_shut_interfaces("Gi 0/4", "Gi 0/9")

        # Creating the VLAN on all DUTs

        vl1.create_vlan(vlan=vlan)
        vl2.create_vlan(vlan=vlan)
        vl3.create_vlan(vlan=vlan)

        # Adding the ports to the VLAN

        vl1.add_more_ports_to_vlan("Gi 0/3", "Ex 0/1", "Gi 0/9", vlan=vlan)
        vl2.add_more_ports_to_vlan("Gi 0/4", "Gi 0/5", "Gi 0/9", vlan=vlan)
        vl3.add_more_ports_to_vlan("Gi 0/4", "Gi 0/9", vlan=vlan)

        stp2.stp_disable(port="Gi 0/1")  # Link towards CambiumLAB
        time.sleep(2)

        d_root_id, d_bridge_id, ports = stp3.show_spanning_tree_rstp()
        print(ports)

        mac_addr = fdb3.show_mac_addr_table_vlan(vlan=stream_vlan)
        print(mac_addr)

        for port in ports:

            if port["Role"] == "Root":

                print("######## 1 ########")
                # print(port["Name"],"----", mac_addr[0]["Ports"])
                assert port["Name"] == mac_addr[0]["Ports"]
                assert mac_addr[0]["Mac Address"] == stream_mac_source
                port_root = port["Name"]

        print(port_root)
        # Shutting the Root Port and checking that the stream_mac_source is learned on the Alternate Port that is Root now

        int3.shut_interface(interface="Gi 0/9")

        d_root_id_1, d_bridge_id_1, ports_1 = stp3.show_spanning_tree_rstp()
        print(ports_1)

        mac_addr_1 = fdb3.show_mac_addr_table_vlan(vlan=stream_vlan)
        print(mac_addr_1)

        for port in ports_1:

            if port["Role"] == "Root":

                print("######## 2 ########")
                # print(port["Name"],"----", mac_addr[0]["Ports"])
                assert port["Name"] == mac_addr_1[0]["Ports"]
                assert mac_addr_1[0]["Mac Address"] == stream_mac_source
                assert port["Name"] != port_root

        # No shutting the port and checking that is learned on the first Root Port

        int3.no_shut_interface(interface="Gi 0/9")

        d_root_id_2, d_bridge_id_2, ports_2 = stp3.show_spanning_tree_rstp()
        print(ports_2)

        mac_addr_2 = fdb3.show_mac_addr_table_vlan(vlan=stream_vlan)
        print(mac_addr_2)

        for port in ports_2:

            if port["Role"] == "Root":

                print("######## 3 ########")
                # print(port["Name"],"----", mac_addr[0]["Ports"])
                assert port["Name"] == mac_addr_2[0]["Ports"]
                assert mac_addr_2[0]["Mac Address"] == stream_mac_source
                assert port["Name"] == port_root

        print("########## Removing the config #############")

        int1.shut_interfaces("Gi 0/3", "Ex 0/1", "Gi 0/9")
        int2.shut_interfaces("Gi 0/4", "Gi 0/5", "Gi 0/9")
        int3.shut_interfaces("Gi 0/4", "Gi 0/9")

        vl1.remove_vlan(vlan=vlan)
        vl2.remove_vlan(vlan=vlan)
        vl3.remove_vlan(vlan=vlan)

        stp2.stp_enable(port="Gi 0/1")














