import time
from Management import dut_objects
from flows import mstpflow

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

mstp_flow = mstpflow.MSTPFlow()


class TestMSTPSuite1:

    def test_func_1(self):

        print("###### Test_func_1 ######")
        print("########## Verify MSTP (802.1S) root election by setting priority #############")
        print("###### 3 DUTs ######")

        #   Topology
        #
        # DUT1 -- DUT2
        #   \     /
        #    \   /
        #     DUT3

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

        # Change the mode of STP to MSTP on all DUTs

        DUT1.stp.change_stp_mode(mode="mst")
        DUT2.stp.change_stp_mode(mode="mst")
        DUT3.stp.change_stp_mode(mode="mst")

        # Disable STP on the link towards Cambium LAB

        DUT2.stp.stp_disable(port="Gi 0/1")

        # Configure 2 MSTP Instances for all DUTs and assign VLANs to them

        DUT1.stp.add_mst_instances_with_vlans("1", "2", vlans_instance_1=["10,20"], vlans_instance_2=["30"])
        DUT2.stp.add_mst_instances_with_vlans("1", "2", vlans_instance_1=["10,20"], vlans_instance_2=["30"])
        DUT3.stp.add_mst_instances_with_vlans("1", "2", vlans_instance_1=["10,20"], vlans_instance_2=["30"])

        # Configure the same Region for all DUTs

        DUT1.stp.add_mst_region(region="Reg1")
        DUT2.stp.add_mst_region(region="Reg1")
        DUT3.stp.add_mst_region(region="Reg1")

        # Check the default Root Bridge for Instance 1 (the lowest MAC in the topology - DUT1)

        d_instance_zero1_1, d_instance1_1, dict_of_ports_instance1_1 = DUT1.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero1_2, d_instance1_2, dict_of_ports_instance1_2 = DUT2.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero1_3, d_instance1_3, dict_of_ports_instance1_3 = DUT3.stp.show_spanning_tree_mst(instance="1")

        print("######## Root ID and Bridge ID of DUT 1 ########")
        print(d_instance1_1)
        print("######## Root ID and Bridge ID of DUT 2 ########")
        print(d_instance1_2)
        print("######## Root ID and Bridge ID of DUT 3 ########")
        print(d_instance1_3)

        assert d_instance1_1["Root ID Address"] == d_instance1_2["Root ID Address"] == \
               d_instance1_3["Root ID Address"] == d_instance1_1["Bridge ID Address"]
        assert d_instance1_1["Root ID Priority"] == "32768" and d_instance1_2[
            "Root ID Priority"] == "32768" and d_instance1_3["Root ID Priority"] == "32768"

        print("######## Ports of DUT 1 ########")
        print(dict_of_ports_instance1_1)
        print("######## Ports of DUT 2 ########")
        print(dict_of_ports_instance1_2)
        print("######## Ports of DUT 3 ########")
        print(dict_of_ports_instance1_3)

        # Check the Port Role of each DUT

        assert dict_of_ports_instance1_1["Gi0/10"]["Role"] == "Designated" and \
               dict_of_ports_instance1_1["Ex0/1"]["Role"] == "Designated"
        assert dict_of_ports_instance1_2["Gi0/3"]["Role"] == "Designated" and \
               dict_of_ports_instance1_2["Gi0/9"]["Role"] == "Root"
        assert dict_of_ports_instance1_3["Gi0/3"]["Role"] == "Alternate" and \
               dict_of_ports_instance1_3["Gi0/10"]["Role"] == "Root"

        # Change the bridge priority on DUT3 for Instance 1

        DUT3.stp.add_mst_priority(instance="1", priority="4096")

        # Check the new Root Bridge for Instance 1 (the lowest priority in the topology - DUT3)

        d_instance_zero_1, d_instance1_1, dict_of_ports_instance1_1 = DUT1.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero_2, d_instance1_2, dict_of_ports_instance1_2 = DUT2.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero_3, d_instance1_3, dict_of_ports_instance1_3 = DUT3.stp.show_spanning_tree_mst(instance="1")

        print("######## Root ID and Bridge ID of DUT 1 ########")
        print(d_instance1_1)
        print("######## Root ID and Bridge ID of DUT 2 ########")
        print(d_instance1_2)
        print("######## Root ID and Bridge ID of DUT 3 ########")
        print(d_instance1_3)

        assert d_instance1_1["Root ID Address"] == d_instance1_2["Root ID Address"] == \
               d_instance1_3["Root ID Address"] == d_instance1_3["Bridge ID Address"]
        assert d_instance1_1["Root ID Priority"] == "4096" and d_instance1_2[
            "Root ID Priority"] == "4096" and d_instance1_3["Root ID Priority"] == "4096"

        print("######## Ports of DUT 1 ########")
        print(dict_of_ports_instance1_1)
        print("######## Ports of DUT 2 ########")
        print(dict_of_ports_instance1_2)
        print("######## Ports of DUT 3 ########")
        print(dict_of_ports_instance1_3)

        # Check the Port Role of each DUT for Instance 1

        assert dict_of_ports_instance1_1["Gi0/10"]["Role"] == "Root" and \
               dict_of_ports_instance1_1["Ex0/1"]["Role"] == "Designated"
        assert dict_of_ports_instance1_2["Gi0/3"]["Role"] == "Root" and \
               dict_of_ports_instance1_2["Gi0/9"]["Role"] == "Alternate"
        assert dict_of_ports_instance1_3["Gi0/3"]["Role"] == "Designated" and \
               dict_of_ports_instance1_3["Gi0/10"]["Role"] == "Designated"

        # Remove the bridge-priority for Instance 1 and check that DUT1 is the root for Instance 1

        DUT3.stp.remove_mst_priority(instance="1")

        # Check the default Root Bridge (the lowest MAC in the topology - DUT1)

        d_instance_zero_1, d_instance1_1, dict_of_ports_instance1_1 = DUT1.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero_2, d_instance1_2, dict_of_ports_instance1_2 = DUT2.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero_3, d_instance1_3, dict_of_ports_instance1_3 = DUT3.stp.show_spanning_tree_mst(instance="1")

        print("######## Root ID and Bridge ID of DUT 1 ########")
        print(d_instance1_1)
        print("######## Root ID and Bridge ID of DUT 2 ########")
        print(d_instance1_2)
        print("######## Root ID and Bridge ID of DUT 3 ########")
        print(d_instance1_3)

        assert d_instance1_1["Root ID Address"] == d_instance1_2["Root ID Address"] == \
               d_instance1_3["Root ID Address"] == d_instance1_1["Bridge ID Address"]
        assert d_instance1_1["Root ID Priority"] == "32768" and d_instance1_2[
            "Root ID Priority"] == "32768" and d_instance1_3["Root ID Priority"] == "32768"

        print("######## Ports of DUT 1 ########")
        print(dict_of_ports_instance1_1)
        print("######## Ports of DUT 2 ########")
        print(dict_of_ports_instance1_2)
        print("######## Ports of DUT 3 ########")
        print(dict_of_ports_instance1_3)

        # Check the Port Role of each DUT are back in place for Instance 1

        assert dict_of_ports_instance1_1["Gi0/10"]["Role"] == "Designated" and \
               dict_of_ports_instance1_1["Ex0/1"]["Role"] == "Designated"
        assert dict_of_ports_instance1_2["Gi0/3"]["Role"] == "Designated" and \
               dict_of_ports_instance1_2["Gi0/9"]["Role"] == "Root"
        assert dict_of_ports_instance1_3["Gi0/3"]["Role"] == "Alternate" and \
               dict_of_ports_instance1_3["Gi0/10"]["Role"] == "Root"

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
        print("########## Verify MSTP (802.1S) port cost functionality #############")
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

        # Change the mode of STP to MSTP on all DUTs

        DUT1.stp.change_stp_mode(mode="mst")
        DUT2.stp.change_stp_mode(mode="mst")
        DUT3.stp.change_stp_mode(mode="mst")

        # Disable STP on the link towards Cambium LAB

        DUT2.stp.stp_disable(port="Gi 0/1")

        # Configure 2 MSTP Instances for all DUTs and assign VLANs to them

        DUT1.stp.add_mst_instances_with_vlans("1", "2", vlans_instance_1=["10,20"], vlans_instance_2=["30"])
        DUT2.stp.add_mst_instances_with_vlans("1", "2", vlans_instance_1=["10,20"], vlans_instance_2=["30"])
        DUT3.stp.add_mst_instances_with_vlans("1", "2", vlans_instance_1=["10,20"], vlans_instance_2=["30"])

        # Configure the same Region for all DUTs

        DUT1.stp.add_mst_region(region="Reg1")
        DUT2.stp.add_mst_region(region="Reg1")
        DUT3.stp.add_mst_region(region="Reg1")

        # Check the default Root Bridge for Instance 1 (the lowest MAC in the topology - DUT1)

        d_instance_zero_1, d_instance1_1, dict_of_ports_instance1_1 = DUT1.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero_2, d_instance1_2, dict_of_ports_instance1_2 = DUT2.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero_3, d_instance1_3, dict_of_ports_instance1_3 = DUT3.stp.show_spanning_tree_mst(instance="1")

        print("######## Root ID and Bridge ID of DUT 1 ########")
        print(d_instance1_1)
        print("######## Root ID and Bridge ID of DUT 2 ########")
        print(d_instance1_2)
        print("######## Root ID and Bridge ID of DUT 3 ########")
        print(d_instance1_3)

        assert d_instance1_1["Root ID Address"] == d_instance1_2["Root ID Address"] == \
               d_instance1_3["Root ID Address"] == d_instance1_1["Bridge ID Address"]
        assert d_instance1_1["Root ID Priority"] == "32768" and d_instance1_2[
            "Root ID Priority"] == "32768" and d_instance1_3["Root ID Priority"] == "32768"

        print("######## Ports of DUT 1 ########")
        print(dict_of_ports_instance1_1)
        print("######## Ports of DUT 2 ########")
        print(dict_of_ports_instance1_2)
        print("######## Ports of DUT 3 ########")
        print(dict_of_ports_instance1_3)

        # # Check the Port Role/Cost of each DUT for Instance 1

        assert dict_of_ports_instance1_1["Gi0/10"]["Role"] == "Designated" and \
               dict_of_ports_instance1_1["Ex0/1"]["Role"] == "Designated"
        assert dict_of_ports_instance1_2["Gi0/3"]["Role"] == "Designated" and \
               dict_of_ports_instance1_2["Gi0/9"]["Role"] == "Root"
        assert dict_of_ports_instance1_3["Gi0/3"]["Role"] == "Alternate" and \
               dict_of_ports_instance1_3["Gi0/10"]["Role"] == "Root"
        assert dict_of_ports_instance1_3["Gi0/3"]["Cost"] == "20000" and \
               dict_of_ports_instance1_3["Gi0/10"]["Cost"] == "20000"

        # Change the cost of the Root port of DUT3 of Instance 1, so it becomes Alternate

        DUT3.stp.add_mst_port_cost(instance="1", port="Gi 0/10", cost="50000")

        # Check the Root Bridge for Instance 1 (the lowest priority in the topology - DUT1)

        d_instance_zero_1, d_instance1_1, dict_of_ports_instance1_1 = DUT1.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero_2, d_instance1_2, dict_of_ports_instance1_2 = DUT2.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero_3, d_instance1_3, dict_of_ports_instance1_3 = DUT3.stp.show_spanning_tree_mst(instance="1")

        print("######## Root ID and Bridge ID of DUT 1 ########")
        print(d_instance1_1)
        print("######## Root ID and Bridge ID of DUT 2 ########")
        print(d_instance1_2)
        print("######## Root ID and Bridge ID of DUT 3 ########")
        print(d_instance1_3)

        assert d_instance1_1["Root ID Address"] == d_instance1_2["Root ID Address"] == \
               d_instance1_3["Root ID Address"] == d_instance1_1["Bridge ID Address"]
        assert d_instance1_1["Root ID Priority"] == "32768" and d_instance1_2[
            "Root ID Priority"] == "32768" and d_instance1_3["Root ID Priority"] == "32768"

        print("######## Ports of DUT 1 ########")
        print(dict_of_ports_instance1_1)
        print("######## Ports of DUT 2 ########")
        print(dict_of_ports_instance1_2)
        print("######## Ports of DUT 3 ########")
        print(dict_of_ports_instance1_3)

        # Check the Port Role/Cost of each DUT for Instance 1

        assert dict_of_ports_instance1_1["Gi0/10"]["Role"] == "Designated" and \
               dict_of_ports_instance1_1["Ex0/1"]["Role"] == "Designated"
        assert dict_of_ports_instance1_2["Gi0/3"]["Role"] == "Designated" and \
               dict_of_ports_instance1_2["Gi0/9"]["Role"] == "Root"
        assert dict_of_ports_instance1_3["Gi0/3"]["Role"] == "Root" and \
               dict_of_ports_instance1_3["Gi0/10"]["Role"] == "Alternate"
        assert dict_of_ports_instance1_3["Gi0/3"]["Cost"] == "20000" and \
               dict_of_ports_instance1_3["Gi0/10"]["Cost"] == "50000"

        # Remove the cost for Instance 1 and check that DUT1 is the root for Instance 1

        DUT3.stp.remove_mst_port_cost(instance="1", port="Gi 0/10")

        # Check the default Root Bridge (the lowest MAC in the topology - DUT1)

        d_instance_zero_1, d_instance1_1, dict_of_ports_instance1_1 = DUT1.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero_2, d_instance1_2, dict_of_ports_instance1_2 = DUT2.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero_3, d_instance1_3, dict_of_ports_instance1_3 = DUT3.stp.show_spanning_tree_mst(instance="1")

        print("######## Root ID and Bridge ID of DUT 1 ########")
        print(d_instance1_1)
        print("######## Root ID and Bridge ID of DUT 2 ########")
        print(d_instance1_2)
        print("######## Root ID and Bridge ID of DUT 3 ########")
        print(d_instance1_3)

        assert d_instance1_1["Root ID Address"] == d_instance1_2["Root ID Address"] == \
               d_instance1_3["Root ID Address"] == d_instance1_1["Bridge ID Address"]
        assert d_instance1_1["Root ID Priority"] == "32768" and d_instance1_2[
            "Root ID Priority"] == "32768" and d_instance1_3["Root ID Priority"] == "32768"

        print("######## Ports of DUT 1 ########")
        print(dict_of_ports_instance1_1)
        print("######## Ports of DUT 2 ########")
        print(dict_of_ports_instance1_2)
        print("######## Ports of DUT 3 ########")
        print(dict_of_ports_instance1_3)

        # Check the Port Role/Cost of each DUT for Instance 1

        assert dict_of_ports_instance1_1["Gi0/10"]["Role"] == "Designated" and \
               dict_of_ports_instance1_1["Ex0/1"]["Role"] == "Designated"
        assert dict_of_ports_instance1_2["Gi0/3"]["Role"] == "Designated" and \
               dict_of_ports_instance1_2["Gi0/9"]["Role"] == "Root"
        assert dict_of_ports_instance1_3["Gi0/3"]["Role"] == "Alternate" and \
               dict_of_ports_instance1_3["Gi0/10"]["Role"] == "Root"
        assert dict_of_ports_instance1_3["Gi0/3"]["Cost"] == "20000" and \
               dict_of_ports_instance1_3["Gi0/10"]["Cost"] == "20000"

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
        print("########## Verify MSTP (802.1S) port priority functionality #############")
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

        # Change the mode of STP to MSTP on all DUTs

        DUT1.stp.change_stp_mode(mode="mst")
        DUT2.stp.change_stp_mode(mode="mst")

        # Disable STP on the link towards Cambium LAB

        DUT2.stp.stp_disable(port="Gi 0/1")

        # Configure 2 MSTP Instances for all DUTs and assign VLANs to them

        DUT1.stp.add_mst_instances_with_vlans("1", "2", vlans_instance_1=["10,20"], vlans_instance_2=["30"])
        DUT2.stp.add_mst_instances_with_vlans("1", "2", vlans_instance_1=["10,20"], vlans_instance_2=["30"])

        # Configure the same Region for all DUTs

        DUT1.stp.add_mst_region(region="Reg1")
        DUT2.stp.add_mst_region(region="Reg1")

        # Check the default Root Bridge for Instance 1 (the lowest MAC in the topology - DUT1)

        d_instance_zero_1, d_instance1_1, dict_of_ports_instance1_1 = DUT1.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero_2, d_instance1_2, dict_of_ports_instance1_2 = DUT2.stp.show_spanning_tree_mst(instance="1")

        print("######## Root ID and Bridge ID of DUT 1 ########")
        print(d_instance1_1)
        print("######## Root ID and Bridge ID of DUT 2 ########")
        print(d_instance1_2)

        assert d_instance1_1["Root ID Address"] == d_instance1_2["Root ID Address"] == d_instance1_1["Bridge ID Address"]
        assert d_instance1_1["Root ID Priority"] == "32768" and d_instance1_2["Root ID Priority"] == "32768"

        print("######## Ports of DUT 1 ########")
        print(dict_of_ports_instance1_1)
        print("######## Ports of DUT 2 ########")
        print(dict_of_ports_instance1_2)

        # Check the Port Role/Port-priority of each DUT for Instance 1

        assert dict_of_ports_instance1_1["Ex0/1"]["Role"] == "Designated" and dict_of_ports_instance1_1["Ex0/2"]["Role"] == "Designated"
        assert dict_of_ports_instance1_2["Gi0/9"]["Role"] == "Root" and dict_of_ports_instance1_2["Gi0/10"]["Role"] == "Alternate"
        assert dict_of_ports_instance1_1["Ex0/1"]["Prio"] == "128" and dict_of_ports_instance1_1["Ex0/2"]["Prio"] == "128"

        # Change the port-priority of the remote port of DUT1 (Ex 0/2), so the port Gi 0/10 from DUT2 becomes Root

        DUT1.stp.add_mst_port_priority(instance="1", port="Ex 0/2", port_priority="64")

        # Check the Root Bridge for Instance 1 (the lowest priority in the topology - DUT1)

        d_instance_zero_1, d_instance1_1, dict_of_ports_instance1_1 = DUT1.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero_2, d_instance1_2, dict_of_ports_instance1_2 = DUT2.stp.show_spanning_tree_mst(instance="1")

        print("######## Root ID and Bridge ID of DUT 1 ########")
        print(d_instance1_1)
        print("######## Root ID and Bridge ID of DUT 2 ########")
        print(d_instance1_2)

        assert d_instance1_1["Root ID Address"] == d_instance1_2["Root ID Address"] == d_instance1_1[
            "Bridge ID Address"]
        assert d_instance1_1["Root ID Priority"] == "32768" and d_instance1_2["Root ID Priority"] == "32768"

        print("######## Ports of DUT 1 ########")
        print(dict_of_ports_instance1_1)
        print("######## Ports of DUT 2 ########")
        print(dict_of_ports_instance1_2)

        # Check the Port Role/Port-priority of each DUT for Instance 1

        assert dict_of_ports_instance1_1["Ex0/1"]["Role"] == "Designated" and dict_of_ports_instance1_1["Ex0/2"][
            "Role"] == "Designated"
        assert dict_of_ports_instance1_2["Gi0/9"]["Role"] == "Alternate" and dict_of_ports_instance1_2["Gi0/10"][
            "Role"] == "Root"
        assert dict_of_ports_instance1_1["Ex0/1"]["Prio"] == "128" and dict_of_ports_instance1_1["Ex0/2"][
            "Prio"] == "64"

        # Remove the port-priority for Instance 1 and check that DUT1 is the root for Instance 1

        DUT1.stp.remove_mst_port_priority(instance="1", port="Ex 0/2")

        # Check the default Root Bridge (the lowest MAC in the topology - DUT1)

        d_instance_zero_1, d_instance1_1, dict_of_ports_instance1_1 = DUT1.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero_2, d_instance1_2, dict_of_ports_instance1_2 = DUT2.stp.show_spanning_tree_mst(instance="1")

        print("######## Root ID and Bridge ID of DUT 1 ########")
        print(d_instance1_1)
        print("######## Root ID and Bridge ID of DUT 2 ########")
        print(d_instance1_2)

        assert d_instance1_1["Root ID Address"] == d_instance1_2["Root ID Address"] == d_instance1_1["Bridge ID Address"]
        assert d_instance1_1["Root ID Priority"] == "32768" and d_instance1_2["Root ID Priority"] == "32768"

        print("######## Ports of DUT 1 ########")
        print(dict_of_ports_instance1_1)
        print("######## Ports of DUT 2 ########")
        print(dict_of_ports_instance1_2)

        # Check the Port Role/Port-priority of each DUT for Instance 1 are back in place

        assert dict_of_ports_instance1_1["Ex0/1"]["Role"] == "Designated" and dict_of_ports_instance1_1["Ex0/2"][
            "Role"] == "Designated"
        assert dict_of_ports_instance1_2["Gi0/9"]["Role"] == "Root" and dict_of_ports_instance1_2["Gi0/10"][
            "Role"] == "Alternate"
        assert dict_of_ports_instance1_1["Ex0/1"]["Prio"] == "128" and dict_of_ports_instance1_1["Ex0/2"][
            "Prio"] == "128"

        print("########## Removing the config #############")

        DUT2.stp.stp_enable(port="Gi 0/1")

        DUT1.stp.change_stp_mode(mode="rst")
        DUT2.stp.change_stp_mode(mode="rst")

        DUT1.vl.remove_vlans("10", "20", "30")
        DUT2.vl.remove_vlans("10", "20", "30")

        DUT1.int.shut_interfaces("Ex 0/1", "Ex 0/2")
        DUT2.int.shut_interfaces("Gi 0/9", "Gi 0/10")

    def test_func_4(self):

        print("###### Test_func_4 ######")
        print("########## Verify MSTP (802.1S) root election by setting root primary #############")
        print("###### 3 DUTs ######")

        #   Topology
        #
        # DUT1 -- DUT2
        #   \     /
        #    \   /
        #     DUT3

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

        # Change the mode of STP to MSTP on all DUTs

        DUT1.stp.change_stp_mode(mode="mst")
        DUT2.stp.change_stp_mode(mode="mst")
        DUT3.stp.change_stp_mode(mode="mst")

        # Disable STP on the link towards Cambium LAB

        DUT2.stp.stp_disable(port="Gi 0/1")

        # Configure 2 MSTP Instances for all DUTs and assign VLANs to them

        DUT1.stp.add_mst_instances_with_vlans("1", "2", vlans_instance_1=["10,20"], vlans_instance_2=["30"])
        DUT2.stp.add_mst_instances_with_vlans("1", "2", vlans_instance_1=["10,20"], vlans_instance_2=["30"])
        DUT3.stp.add_mst_instances_with_vlans("1", "2", vlans_instance_1=["10,20"], vlans_instance_2=["30"])

        # Configure the same Region for all DUTs

        DUT1.stp.add_mst_region(region="Reg1")
        DUT2.stp.add_mst_region(region="Reg1")
        DUT3.stp.add_mst_region(region="Reg1")

        # Check the default Root Bridge for Instance 1 (the lowest MAC in the topology - DUT1)

        d_instance_zero1_1, d_instance1_1, dict_of_ports_instance1_1 = DUT1.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero1_2, d_instance1_2, dict_of_ports_instance1_2 = DUT2.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero1_3, d_instance1_3, dict_of_ports_instance1_3 = DUT3.stp.show_spanning_tree_mst(instance="1")

        print("######## Root ID and Bridge ID of DUT 1 ########")
        print(d_instance1_1)
        print("######## Root ID and Bridge ID of DUT 2 ########")
        print(d_instance1_2)
        print("######## Root ID and Bridge ID of DUT 3 ########")
        print(d_instance1_3)

        assert d_instance1_1["Root ID Address"] == d_instance1_2["Root ID Address"] == \
               d_instance1_3["Root ID Address"] == d_instance1_1["Bridge ID Address"]
        assert d_instance1_1["Root ID Priority"] == "32768" and d_instance1_2[
            "Root ID Priority"] == "32768" and d_instance1_3["Root ID Priority"] == "32768"

        print("######## Ports of DUT 1 ########")
        print(dict_of_ports_instance1_1)
        print("######## Ports of DUT 2 ########")
        print(dict_of_ports_instance1_2)
        print("######## Ports of DUT 3 ########")
        print(dict_of_ports_instance1_3)

        # Check the Port Role of each DUT

        assert dict_of_ports_instance1_1["Gi0/10"]["Role"] == "Designated" and \
               dict_of_ports_instance1_1["Ex0/1"]["Role"] == "Designated"
        assert dict_of_ports_instance1_2["Gi0/3"]["Role"] == "Designated" and \
               dict_of_ports_instance1_2["Gi0/9"]["Role"] == "Root"
        assert dict_of_ports_instance1_3["Gi0/3"]["Role"] == "Alternate" and \
               dict_of_ports_instance1_3["Gi0/10"]["Role"] == "Root"

        # Change the bridge priority on DUT3 for Instance 1 using root primary

        DUT3.stp.add_mst_root_primary_secondary(instance="1", root="primary")

        # Check the new Root Bridge for Instance 1 (the lowest priority in the topology - DUT3)

        d_instance_zero_1, d_instance1_1, dict_of_ports_instance1_1 = DUT1.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero_2, d_instance1_2, dict_of_ports_instance1_2 = DUT2.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero_3, d_instance1_3, dict_of_ports_instance1_3 = DUT3.stp.show_spanning_tree_mst(instance="1")

        print("######## Root ID and Bridge ID of DUT 1 ########")
        print(d_instance1_1)
        print("######## Root ID and Bridge ID of DUT 2 ########")
        print(d_instance1_2)
        print("######## Root ID and Bridge ID of DUT 3 ########")
        print(d_instance1_3)

        assert d_instance1_1["Root ID Address"] == d_instance1_2["Root ID Address"] == \
               d_instance1_3["Root ID Address"] == d_instance1_3["Bridge ID Address"]
        assert d_instance1_1["Root ID Priority"] == "24576" and d_instance1_2[
            "Root ID Priority"] == "24576" and d_instance1_3["Root ID Priority"] == "24576"

        print("######## Ports of DUT 1 ########")
        print(dict_of_ports_instance1_1)
        print("######## Ports of DUT 2 ########")
        print(dict_of_ports_instance1_2)
        print("######## Ports of DUT 3 ########")
        print(dict_of_ports_instance1_3)

        # Check the Port Role of each DUT for Instance 1

        assert dict_of_ports_instance1_1["Gi0/10"]["Role"] == "Root" and \
               dict_of_ports_instance1_1["Ex0/1"]["Role"] == "Designated"
        assert dict_of_ports_instance1_2["Gi0/3"]["Role"] == "Root" and \
               dict_of_ports_instance1_2["Gi0/9"]["Role"] == "Alternate"
        assert dict_of_ports_instance1_3["Gi0/3"]["Role"] == "Designated" and \
               dict_of_ports_instance1_3["Gi0/10"]["Role"] == "Designated"

        # Remove the root priority for Instance 1 and check that DUT1 is the root for Instance 1

        DUT3.stp.remove_mst_root_primary_secondary(instance="1")

        # Check the default Root Bridge (the lowest MAC in the topology - DUT1)

        d_instance_zero_1, d_instance1_1, dict_of_ports_instance1_1 = DUT1.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero_2, d_instance1_2, dict_of_ports_instance1_2 = DUT2.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero_3, d_instance1_3, dict_of_ports_instance1_3 = DUT3.stp.show_spanning_tree_mst(instance="1")

        print("######## Root ID and Bridge ID of DUT 1 ########")
        print(d_instance1_1)
        print("######## Root ID and Bridge ID of DUT 2 ########")
        print(d_instance1_2)
        print("######## Root ID and Bridge ID of DUT 3 ########")
        print(d_instance1_3)

        assert d_instance1_1["Root ID Address"] == d_instance1_2["Root ID Address"] == \
               d_instance1_3["Root ID Address"] == d_instance1_1["Bridge ID Address"]
        assert d_instance1_1["Root ID Priority"] == "32768" and d_instance1_2[
            "Root ID Priority"] == "32768" and d_instance1_3["Root ID Priority"] == "32768"

        print("######## Ports of DUT 1 ########")
        print(dict_of_ports_instance1_1)
        print("######## Ports of DUT 2 ########")
        print(dict_of_ports_instance1_2)
        print("######## Ports of DUT 3 ########")
        print(dict_of_ports_instance1_3)

        # Check the Port Role of each DUT are back in place for Instance 1

        assert dict_of_ports_instance1_1["Gi0/10"]["Role"] == "Designated" and \
               dict_of_ports_instance1_1["Ex0/1"]["Role"] == "Designated"
        assert dict_of_ports_instance1_2["Gi0/3"]["Role"] == "Designated" and \
               dict_of_ports_instance1_2["Gi0/9"]["Role"] == "Root"
        assert dict_of_ports_instance1_3["Gi0/3"]["Role"] == "Alternate" and \
               dict_of_ports_instance1_3["Gi0/10"]["Role"] == "Root"

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


