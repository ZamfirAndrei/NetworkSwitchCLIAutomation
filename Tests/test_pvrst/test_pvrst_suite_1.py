import time
from Management import dut_objects

ip_session_1 = "10.2.109.206"
ip_session_2 = "10.2.109.83"
ip_session_3 = "10.2.109.232"
ip_session_4 = "10.2.109.100"
ip_session_5 = "10.2.109.113"

DUT1 = dut_objects.DUT_Objects(ip_session=ip_session_1)
DUT2 = dut_objects.DUT_Objects(ip_session=ip_session_2)
DUT3 = dut_objects.DUT_Objects(ip_session=ip_session_3)
DUT4 = dut_objects.DUT_Objects(ip_session=ip_session_4)
DUT5 = dut_objects.DUT_Objects(ip_session=ip_session_5)


class TestPVRSTSuite1:

    def test_func_1(self):

        print("###### Test_func_1 ######")
        print("########## Verify PVRST root election by setting priority #############")
        print("###### 3 DUTs ######")

        #    Topology
        #
        #  DUT1 -- DUT2
        #    \     /
        #     \   /
        #      DUT3

        # No shutting the interfaces

        DUT1.int.no_shut_interfaces("Ex 0/1", "Gi 0/10")
        DUT2.int.no_shut_interfaces("Gi 0/3", "Gi 0/9")
        DUT3.int.no_shut_interfaces("Gi 0/3", "Gi 0/10")

        # Create VLANs on DUTs and assign ports to them

        DUT1.vl.create_vlans("10", "20", "30")
        DUT2.vl.create_vlans("10", "20", "30")
        DUT3.vl.create_vlans("10", "20", "30")

        DUT1.vl.add_more_ports_to_more_vlans("Ex 0/1", "Gi 0/10", vlan10="10", vlan20="20", vlan30="30")
        DUT2.vl.add_more_ports_to_more_vlans("Gi 0/3", "Gi 0/9", vlan10="10", vlan20="20", vlan30="30")
        DUT3.vl.add_more_ports_to_more_vlans("Gi 0/3", "Gi 0/10", vlan10="10", vlan20="20", vlan30="30")

        # Change the mode of STP to PVRST on all DUTs

        DUT1.stp.change_stp_mode(mode="pvrst")
        DUT2.stp.change_stp_mode(mode="pvrst")
        DUT3.stp.change_stp_mode(mode="pvrst")

        # Disable STP on the link towards Cambium LAB

        DUT2.stp.stp_disable(port="Gi 0/1")

        # Check the default Root Bridge for VLAN 10 (the lowest MAC in the topology - DUT1)

        d_instance_vlan_vl10_1,  dict_ports_instance_vlan_vl10_1, list_ports_instance_vl10_1 = DUT1.stp.show_spanning_tree_pvrst(vlan="10")
        d_instance_vlan_vl10_2, dict_ports_instance_vlan_vl10_2, list_ports_instance_vl10_2 = DUT2.stp.show_spanning_tree_pvrst(vlan="10")
        d_instance_vlan_vl10_3, dict_ports_instance_vlan_vl10_3, list_ports_instance_vl10_3 = DUT3.stp.show_spanning_tree_pvrst(vlan="10")

        print("######## Root ID and Bridge ID of DUT 1 ########")
        print(d_instance_vlan_vl10_1)
        print("######## Root ID and Bridge ID of DUT 2 ########")
        print(d_instance_vlan_vl10_2)
        print("######## Root ID and Bridge ID of DUT 3 ########")
        print(d_instance_vlan_vl10_3)

        assert d_instance_vlan_vl10_1["Root ID Address"] == d_instance_vlan_vl10_2["Root ID Address"] == d_instance_vlan_vl10_3["Root ID Address"] == d_instance_vlan_vl10_1["Bridge ID Address"]
        assert d_instance_vlan_vl10_1["Root ID Priority"] == "32778" and d_instance_vlan_vl10_2["Root ID Priority"] == "32778" and d_instance_vlan_vl10_3["Root ID Priority"] == "32778"

        print("######## Ports of DUT 1 ########")
        print(dict_ports_instance_vlan_vl10_1)
        print("######## Ports of DUT 2 ########")
        print(dict_ports_instance_vlan_vl10_2)
        print("######## Ports of DUT 3 ########")
        print(dict_ports_instance_vlan_vl10_3)

        # Check the Port Role of each DUT

        assert dict_ports_instance_vlan_vl10_1["Gi0/10"]["Role"] == "Designated" and dict_ports_instance_vlan_vl10_1["Ex0/1"]["Role"] == "Designated"
        assert dict_ports_instance_vlan_vl10_2["Gi0/3"]["Role"] == "Designated" and dict_ports_instance_vlan_vl10_2["Gi0/9"]["Role"] == "Root"
        assert dict_ports_instance_vlan_vl10_3["Gi0/3"]["Role"] == "Alternate" and dict_ports_instance_vlan_vl10_3["Gi0/10"]["Role"] == "Root"

        # Change the bridge priority on DUT3 for VLAN 10

        DUT3.stp.add_pvrst_bridge_priority(vlan="10", brg_priority="4096")

        # Check the new Root Bridge for VLAN 10(the lowest priority in the topology - DUT3)

        d_instance_vlan_vl10_1, dict_ports_instance_vlan_vl10_1, list_ports_instance_vl10_1 = DUT1.stp.show_spanning_tree_pvrst(
            vlan="10")
        d_instance_vlan_vl10_2, dict_ports_instance_vlan_vl10_2, list_ports_instance_vl10_2 = DUT2.stp.show_spanning_tree_pvrst(
            vlan="10")
        d_instance_vlan_vl10_3, dict_ports_instance_vlan_vl10_3, list_ports_instance_vl10_3 = DUT3.stp.show_spanning_tree_pvrst(
            vlan="10")

        print("######## Root ID and Bridge ID of DUT 1 ########")
        print(d_instance_vlan_vl10_1)
        print("######## Root ID and Bridge ID of DUT 2 ########")
        print(d_instance_vlan_vl10_2)
        print("######## Root ID and Bridge ID of DUT 3 ########")
        print(d_instance_vlan_vl10_3)

        assert d_instance_vlan_vl10_1["Root ID Address"] == d_instance_vlan_vl10_2["Root ID Address"] == \
               d_instance_vlan_vl10_3["Root ID Address"] == d_instance_vlan_vl10_3["Bridge ID Address"]
        assert d_instance_vlan_vl10_1["Root ID Priority"] == "4106" and d_instance_vlan_vl10_2[
            "Root ID Priority"] == "4106" and d_instance_vlan_vl10_3["Root ID Priority"] == "4106"

        print("######## Ports of DUT 1 ########")
        print(dict_ports_instance_vlan_vl10_1)
        print("######## Ports of DUT 2 ########")
        print(dict_ports_instance_vlan_vl10_2)
        print("######## Ports of DUT 3 ########")
        print(dict_ports_instance_vlan_vl10_3)

        # Check the Port Role of each DUT

        assert dict_ports_instance_vlan_vl10_1["Gi0/10"]["Role"] == "Root" and \
               dict_ports_instance_vlan_vl10_1["Ex0/1"]["Role"] == "Designated"
        assert dict_ports_instance_vlan_vl10_2["Gi0/3"]["Role"] == "Root" and \
               dict_ports_instance_vlan_vl10_2["Gi0/9"]["Role"] == "Alternate"
        assert dict_ports_instance_vlan_vl10_3["Gi0/3"]["Role"] == "Designated" and \
               dict_ports_instance_vlan_vl10_3["Gi0/10"]["Role"] == "Designated"

        # Remove the bridge-priority for VLAN 10 and check that DUT1 is the root for VLAN 10

        DUT3.stp.remove_pvrst_bridge_priority(vlan="10")

        # Check the default Root Bridge (the lowest MAC in the topology - DUT1)

        d_instance_vlan_vl10_1, dict_ports_instance_vlan_vl10_1, list_ports_instance_vl10_1 = DUT1.stp.show_spanning_tree_pvrst(
            vlan="10")
        d_instance_vlan_vl10_2, dict_ports_instance_vlan_vl10_2, list_ports_instance_vl10_2 = DUT2.stp.show_spanning_tree_pvrst(
            vlan="10")
        d_instance_vlan_vl10_3, dict_ports_instance_vlan_vl10_3, list_ports_instance_vl10_3 = DUT3.stp.show_spanning_tree_pvrst(
            vlan="10")

        print("######## Root ID and Bridge ID of DUT 1 ########")
        print(d_instance_vlan_vl10_1)
        print("######## Root ID and Bridge ID of DUT 2 ########")
        print(d_instance_vlan_vl10_2)
        print("######## Root ID and Bridge ID of DUT 3 ########")
        print(d_instance_vlan_vl10_3)

        assert d_instance_vlan_vl10_1["Root ID Address"] == d_instance_vlan_vl10_2["Root ID Address"] == \
               d_instance_vlan_vl10_3["Root ID Address"] == d_instance_vlan_vl10_1["Bridge ID Address"]
        assert d_instance_vlan_vl10_1["Root ID Priority"] == "32778" and d_instance_vlan_vl10_2[
            "Root ID Priority"] == "32778" and d_instance_vlan_vl10_3["Root ID Priority"] == "32778"

        print("######## Ports of DUT 1 ########")
        print(dict_ports_instance_vlan_vl10_1)
        print("######## Ports of DUT 2 ########")
        print(dict_ports_instance_vlan_vl10_2)
        print("######## Ports of DUT 3 ########")
        print(dict_ports_instance_vlan_vl10_3)

        # Check the Port Role of each DUT

        assert dict_ports_instance_vlan_vl10_1["Gi0/10"]["Role"] == "Designated" and \
               dict_ports_instance_vlan_vl10_1["Ex0/1"]["Role"] == "Designated"
        assert dict_ports_instance_vlan_vl10_2["Gi0/3"]["Role"] == "Designated" and \
               dict_ports_instance_vlan_vl10_2["Gi0/9"]["Role"] == "Root"
        assert dict_ports_instance_vlan_vl10_3["Gi0/3"]["Role"] == "Alternate" and \
               dict_ports_instance_vlan_vl10_3["Gi0/10"]["Role"] == "Root"

        print("########## Removing the config #############")

        DUT2.stp.stp_enable(port="Gi 0/1")

        DUT1.stp.change_stp_mode(mode="rst")
        DUT2.stp.change_stp_mode(mode="rst")
        DUT3.stp.change_stp_mode(mode="rst")

        DUT1.vl.remove_vlans("10", "20", "30")
        DUT2.vl.remove_vlans("10", "20", "30")
        DUT3.vl.remove_vlans("10", "20", "30")

        DUT1.int.shut_interfaces("Ex 0/1", "Gi 0/10")
        DUT2.int.shut_interfaces("Gi 0/3", "Gi 0/9")
        DUT3.int.shut_interfaces("Gi 0/3", "Gi 0/10")

    def test_func_2(self):

        print("###### Test_func_2 ######")
        print("########## Verify PVRST port cost functionality #############")
        print("###### 3 DUTs ######")

        #    Topology
        #
        #  DUT1 -- DUT2
        #    \     /
        #     \   /
        #      DUT3

        # No shutting the interfaces

        DUT1.int.no_shut_interfaces("Ex 0/1", "Gi 0/10")
        DUT2.int.no_shut_interfaces("Gi 0/3", "Gi 0/9")
        DUT3.int.no_shut_interfaces("Gi 0/3", "Gi 0/10")

        # Create VLANs on DUTs and assign ports to them

        DUT1.vl.create_vlans("10", "20", "30")
        DUT2.vl.create_vlans("10", "20", "30")
        DUT3.vl.create_vlans("10", "20", "30")

        DUT1.vl.add_more_ports_to_more_vlans("Ex 0/1", "Gi 0/10", vlan10="10", vlan20="20", vlan30="30")
        DUT2.vl.add_more_ports_to_more_vlans("Gi 0/3", "Gi 0/9", vlan10="10", vlan20="20", vlan30="30")
        DUT3.vl.add_more_ports_to_more_vlans("Gi 0/3", "Gi 0/10", vlan10="10", vlan20="20", vlan30="30")

        # Change the mode of STP to PVRST on all DUTs

        DUT1.stp.change_stp_mode(mode="pvrst")
        DUT2.stp.change_stp_mode(mode="pvrst")
        DUT3.stp.change_stp_mode(mode="pvrst")

        # Disable STP on the link towards Cambium LAB

        DUT2.stp.stp_disable(port="Gi 0/1")

        # Check the default Root Bridge for VLAN 10 (the lowest MAC in the topology - DUT1)

        d_instance_vlan_vl10_1,  dict_ports_instance_vlan_vl10_1, list_ports_instance_vl10_1 = DUT1.stp.show_spanning_tree_pvrst(vlan="10")
        d_instance_vlan_vl10_2, dict_ports_instance_vlan_vl10_2, list_ports_instance_vl10_2 = DUT2.stp.show_spanning_tree_pvrst(vlan="10")
        d_instance_vlan_vl10_3, dict_ports_instance_vlan_vl10_3, list_ports_instance_vl10_3 = DUT3.stp.show_spanning_tree_pvrst(vlan="10")

        print("######## Root ID and Bridge ID of DUT 1 ########")
        print(d_instance_vlan_vl10_1)
        print("######## Root ID and Bridge ID of DUT 2 ########")
        print(d_instance_vlan_vl10_2)
        print("######## Root ID and Bridge ID of DUT 3 ########")
        print(d_instance_vlan_vl10_3)

        assert d_instance_vlan_vl10_1["Root ID Address"] == d_instance_vlan_vl10_2["Root ID Address"] == d_instance_vlan_vl10_3["Root ID Address"] == d_instance_vlan_vl10_1["Bridge ID Address"]
        assert d_instance_vlan_vl10_1["Root ID Priority"] == "32778" and d_instance_vlan_vl10_2["Root ID Priority"] == "32778" and d_instance_vlan_vl10_3["Root ID Priority"] == "32778"

        print("######## Ports of DUT 1 ########")
        print(dict_ports_instance_vlan_vl10_1)
        print("######## Ports of DUT 2 ########")
        print(dict_ports_instance_vlan_vl10_2)
        print("######## Ports of DUT 3 ########")
        print(dict_ports_instance_vlan_vl10_3)

        # Check the Port Role/Cost of each DUT

        assert dict_ports_instance_vlan_vl10_1["Gi0/10"]["Role"] == "Designated" and dict_ports_instance_vlan_vl10_1["Ex0/1"]["Role"] == "Designated"
        assert dict_ports_instance_vlan_vl10_2["Gi0/3"]["Role"] == "Designated" and dict_ports_instance_vlan_vl10_2["Gi0/9"]["Role"] == "Root"
        assert dict_ports_instance_vlan_vl10_3["Gi0/3"]["Role"] == "Alternate" and dict_ports_instance_vlan_vl10_3["Gi0/10"]["Role"] == "Root"
        assert dict_ports_instance_vlan_vl10_3["Gi0/3"]["Cost"] == "20000" and dict_ports_instance_vlan_vl10_3["Gi0/10"]["Cost"] == "20000"

        # Change the cost of the Root port of DUT3, so it becomes Alternate

        DUT3.stp.add_pvrst_port_cost(vlan="10", port="Gi 0/10", cost="50000")

        # Check the default Root Bridge for VLAN 10 (the lowest MAC in the topology - DUT1)

        d_instance_vlan_vl10_1, dict_ports_instance_vlan_vl10_1, list_ports_instance_vl10_1 = DUT1.stp.show_spanning_tree_pvrst(
            vlan="10")
        d_instance_vlan_vl10_2, dict_ports_instance_vlan_vl10_2, list_ports_instance_vl10_2 = DUT2.stp.show_spanning_tree_pvrst(
            vlan="10")
        d_instance_vlan_vl10_3, dict_ports_instance_vlan_vl10_3, list_ports_instance_vl10_3 = DUT3.stp.show_spanning_tree_pvrst(
            vlan="10")

        print("######## Root ID and Bridge ID of DUT 1 ########")
        print(d_instance_vlan_vl10_1)
        print("######## Root ID and Bridge ID of DUT 2 ########")
        print(d_instance_vlan_vl10_2)
        print("######## Root ID and Bridge ID of DUT 3 ########")
        print(d_instance_vlan_vl10_3)

        assert d_instance_vlan_vl10_1["Root ID Address"] == d_instance_vlan_vl10_2["Root ID Address"] == \
               d_instance_vlan_vl10_3["Root ID Address"] == d_instance_vlan_vl10_1["Bridge ID Address"]
        assert d_instance_vlan_vl10_1["Root ID Priority"] == "32778" and d_instance_vlan_vl10_2[
            "Root ID Priority"] == "32778" and d_instance_vlan_vl10_3["Root ID Priority"] == "32778"

        print("######## Ports of DUT 1 ########")
        print(dict_ports_instance_vlan_vl10_1)
        print("######## Ports of DUT 2 ########")
        print(dict_ports_instance_vlan_vl10_2)
        print("######## Ports of DUT 3 ########")
        print(dict_ports_instance_vlan_vl10_3)

        # Check the Port Role/Cost of each DUT

        assert dict_ports_instance_vlan_vl10_1["Gi0/10"]["Role"] == "Designated" and \
               dict_ports_instance_vlan_vl10_1["Ex0/1"]["Role"] == "Designated"
        assert dict_ports_instance_vlan_vl10_2["Gi0/3"]["Role"] == "Designated" and \
               dict_ports_instance_vlan_vl10_2["Gi0/9"]["Role"] == "Root"
        assert dict_ports_instance_vlan_vl10_3["Gi0/3"]["Role"] == "Root" and \
               dict_ports_instance_vlan_vl10_3["Gi0/10"]["Role"] == "Alternate"
        assert dict_ports_instance_vlan_vl10_3["Gi0/3"]["Cost"] == "20000" and dict_ports_instance_vlan_vl10_3["Gi0/10"]["Cost"] == "50000"

        # Remove the cost for VLAN 10 and check that DUT3 ports are back in place

        DUT3.stp.remove_pvrst_port_cost(vlan="10", port="Gi 0/10")

        # Check the default Root Bridge (the lowest MAC in the topology - DUT1)

        d_instance_vlan_vl10_1, dict_ports_instance_vlan_vl10_1, list_ports_instance_vl10_1 = DUT1.stp.show_spanning_tree_pvrst(
            vlan="10")
        d_instance_vlan_vl10_2, dict_ports_instance_vlan_vl10_2, list_ports_instance_vl10_2 = DUT2.stp.show_spanning_tree_pvrst(
            vlan="10")
        d_instance_vlan_vl10_3, dict_ports_instance_vlan_vl10_3, list_ports_instance_vl10_3 = DUT3.stp.show_spanning_tree_pvrst(
            vlan="10")

        print("######## Root ID and Bridge ID of DUT 1 ########")
        print(d_instance_vlan_vl10_1)
        print("######## Root ID and Bridge ID of DUT 2 ########")
        print(d_instance_vlan_vl10_2)
        print("######## Root ID and Bridge ID of DUT 3 ########")
        print(d_instance_vlan_vl10_3)

        assert d_instance_vlan_vl10_1["Root ID Address"] == d_instance_vlan_vl10_2["Root ID Address"] == \
               d_instance_vlan_vl10_3["Root ID Address"] == d_instance_vlan_vl10_1["Bridge ID Address"]
        assert d_instance_vlan_vl10_1["Root ID Priority"] == "32778" and d_instance_vlan_vl10_2[
            "Root ID Priority"] == "32778" and d_instance_vlan_vl10_3["Root ID Priority"] == "32778"

        print("######## Ports of DUT 1 ########")
        print(dict_ports_instance_vlan_vl10_1)
        print("######## Ports of DUT 2 ########")
        print(dict_ports_instance_vlan_vl10_2)
        print("######## Ports of DUT 3 ########")
        print(dict_ports_instance_vlan_vl10_3)

        # Check the Port Role/Cost of each DUT

        assert dict_ports_instance_vlan_vl10_1["Gi0/10"]["Role"] == "Designated" and \
               dict_ports_instance_vlan_vl10_1["Ex0/1"]["Role"] == "Designated"
        assert dict_ports_instance_vlan_vl10_2["Gi0/3"]["Role"] == "Designated" and \
               dict_ports_instance_vlan_vl10_2["Gi0/9"]["Role"] == "Root"
        assert dict_ports_instance_vlan_vl10_3["Gi0/3"]["Role"] == "Alternate" and \
               dict_ports_instance_vlan_vl10_3["Gi0/10"]["Role"] == "Root"
        assert dict_ports_instance_vlan_vl10_3["Gi0/3"]["Cost"] == "20000" and dict_ports_instance_vlan_vl10_3["Gi0/10"]["Cost"] == "20000"

        print("########## Removing the config #############")

        DUT2.stp.stp_enable(port="Gi 0/1")

        DUT1.stp.change_stp_mode(mode="rst")
        DUT2.stp.change_stp_mode(mode="rst")
        DUT3.stp.change_stp_mode(mode="rst")

        DUT1.vl.remove_vlans("10", "20", "30")
        DUT2.vl.remove_vlans("10", "20", "30")
        DUT3.vl.remove_vlans("10", "20", "30")

        DUT1.int.shut_interfaces("Ex 0/1", "Gi 0/10")
        DUT2.int.shut_interfaces("Gi 0/3", "Gi 0/9")
        DUT3.int.shut_interfaces("Gi 0/3", "Gi 0/10")

    def test_func_3(self):

        print("###### Test_func_3 ######")
        print("########## Verify PVRST port priority functionality #############")
        print("###### 2 DUTs ######")

        #    Topology
        #
        #  DUT1 == DUT2

        # No shutting the interfaces

        DUT1.int.no_shut_interfaces("Ex 0/1", "Ex 0/2")
        DUT2.int.no_shut_interfaces("Gi 0/9", "Gi 0/10")

        # Create VLANs on DUTs and assign ports to them

        DUT1.vl.create_vlans("10", "20", "30")
        DUT2.vl.create_vlans("10", "20", "30")

        DUT1.vl.add_more_ports_to_more_vlans("Ex 0/1", "Ex 0/2", vlan10="10", vlan20="20", vlan30="30")
        DUT2.vl.add_more_ports_to_more_vlans("Gi 0/9", "Gi 0/10", vlan10="10", vlan20="20", vlan30="30")

        # Change the mode of STP to PVRST on all DUTs

        DUT1.stp.change_stp_mode(mode="pvrst")
        DUT2.stp.change_stp_mode(mode="pvrst")

        # Disable STP on the link towards Cambium LAB

        DUT2.stp.stp_disable(port="Gi 0/1")

        # Check the default Root Bridge for VLAN 10 (the lowest MAC in the topology - DUT1)

        d_instance_vlan_vl10_1, dict_ports_instance_vlan_vl10_1, list_ports_instance_vl10_1 = DUT1.stp.show_spanning_tree_pvrst(
            vlan="10")
        d_instance_vlan_vl10_2, dict_ports_instance_vlan_vl10_2, list_ports_instance_vl10_2 = DUT2.stp.show_spanning_tree_pvrst(
            vlan="10")

        print("######## Root ID and Bridge ID of DUT 1 ########")
        print(d_instance_vlan_vl10_1)
        print("######## Root ID and Bridge ID of DUT 2 ########")
        print(d_instance_vlan_vl10_2)

        assert d_instance_vlan_vl10_1["Root ID Address"] == d_instance_vlan_vl10_2["Root ID Address"] == d_instance_vlan_vl10_1["Bridge ID Address"]
        assert d_instance_vlan_vl10_1["Root ID Priority"] == "32778" and d_instance_vlan_vl10_2["Root ID Priority"] == "32778"

        print("######## Ports of DUT 1 ########")
        print(dict_ports_instance_vlan_vl10_1)
        print("######## Ports of DUT 2 ########")
        print(dict_ports_instance_vlan_vl10_2)

        # Check the Port Role/Port-priority of each DUT

        assert dict_ports_instance_vlan_vl10_1["Ex0/1"]["Role"] == "Designated" and dict_ports_instance_vlan_vl10_1["Ex0/2"]["Role"] == "Designated"
        assert dict_ports_instance_vlan_vl10_2["Gi0/9"]["Role"] == "Root" and dict_ports_instance_vlan_vl10_2["Gi0/10"]["Role"] == "Alternate"
        assert dict_ports_instance_vlan_vl10_1["Ex0/1"]["Prio"] == "128" and dict_ports_instance_vlan_vl10_1["Ex0/2"]["Prio"] == "128"

        # Change the port-priority of the remote port of DUT1 (Ex 0/2), so the port Gi 0/10 from DUT2 becomes Root

        DUT1.stp.add_pvrst_port_priority(vlan="10", port="Ex 0/2", port_priority="64")

        # Check the default Root Bridge for VLAN 10 (the lowest MAC in the topology - DUT1)

        d_instance_vlan_vl10_1, dict_ports_instance_vlan_vl10_1, list_ports_instance_vl10_1 = DUT1.stp.show_spanning_tree_pvrst(
            vlan="10")
        d_instance_vlan_vl10_2, dict_ports_instance_vlan_vl10_2, list_ports_instance_vl10_2 = DUT2.stp.show_spanning_tree_pvrst(
            vlan="10")

        print("######## Root ID and Bridge ID of DUT 1 ########")
        print(d_instance_vlan_vl10_1)
        print("######## Root ID and Bridge ID of DUT 2 ########")
        print(d_instance_vlan_vl10_2)

        assert d_instance_vlan_vl10_1["Root ID Address"] == d_instance_vlan_vl10_2["Root ID Address"] == d_instance_vlan_vl10_1["Bridge ID Address"]
        assert d_instance_vlan_vl10_1["Root ID Priority"] == "32778" and d_instance_vlan_vl10_2["Root ID Priority"] == "32778"

        # Check the ports of DUT2 (The Root port -> Alternate port, The Alternate port -> Root port)
        print("######## Ports of DUT 1 ########")
        print(dict_ports_instance_vlan_vl10_1)
        print("######## Ports of DUT 2 ########")
        print(dict_ports_instance_vlan_vl10_2)

        # Check the Port Role/Port-priority of each DUT

        assert dict_ports_instance_vlan_vl10_1["Ex0/1"]["Role"] == "Designated" and dict_ports_instance_vlan_vl10_1["Ex0/2"]["Role"] == "Designated"
        assert dict_ports_instance_vlan_vl10_2["Gi0/9"]["Role"] == "Alternate" and dict_ports_instance_vlan_vl10_2["Gi0/10"]["Role"] == "Root"
        assert dict_ports_instance_vlan_vl10_1["Ex0/1"]["Prio"] == "128" and dict_ports_instance_vlan_vl10_1["Ex0/2"]["Prio"] == "64"

        # Remove the port-priority from DUT1 and check that DUT2 ports are back in place

        DUT1.stp.remove_pvrst_port_priority(vlan="10", port="Ex 0/2")

        d_instance_vlan_vl10_1, dict_ports_instance_vlan_vl10_1, list_ports_instance_vl10_1 = DUT1.stp.show_spanning_tree_pvrst(
            vlan="10")
        d_instance_vlan_vl10_2, dict_ports_instance_vlan_vl10_2, list_ports_instance_vl10_2 = DUT2.stp.show_spanning_tree_pvrst(
            vlan="10")

        print("######## Root ID and Bridge ID of DUT 1 ########")
        print(d_instance_vlan_vl10_1)
        print("######## Root ID and Bridge ID of DUT 2 ########")
        print(d_instance_vlan_vl10_2)

        assert d_instance_vlan_vl10_1["Root ID Address"] == d_instance_vlan_vl10_2["Root ID Address"] == d_instance_vlan_vl10_1["Bridge ID Address"]
        assert d_instance_vlan_vl10_1["Root ID Priority"] == "32778" and d_instance_vlan_vl10_2["Root ID Priority"] == "32778"

        print("######## Ports of DUT 1 ########")
        print(dict_ports_instance_vlan_vl10_1)
        print("######## Ports of DUT 2 ########")
        print(dict_ports_instance_vlan_vl10_2)

        # Check the Port Role/Port-priority of each DUT

        assert dict_ports_instance_vlan_vl10_1["Ex0/1"]["Role"] == "Designated" and dict_ports_instance_vlan_vl10_1["Ex0/2"]["Role"] == "Designated"
        assert dict_ports_instance_vlan_vl10_2["Gi0/9"]["Role"] == "Root" and dict_ports_instance_vlan_vl10_2["Gi0/10"]["Role"] == "Alternate"
        assert dict_ports_instance_vlan_vl10_1["Ex0/1"]["Prio"] == "128" and dict_ports_instance_vlan_vl10_1["Ex0/2"]["Prio"] == "128"

        print("########## Removing the config #############")

        DUT2.stp.stp_enable(port="Gi 0/1")

        DUT1.stp.change_stp_mode(mode="rst")
        DUT2.stp.change_stp_mode(mode="rst")

        DUT1.vl.remove_vlans("10", "20", "30")
        DUT2.vl.remove_vlans("10", "20", "30")

        DUT1.int.shut_interfaces("Ex 0/1", "Ex 0/2")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/10")