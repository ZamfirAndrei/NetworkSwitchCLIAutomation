import time
from Management import dut_objects
from flows import pvrst_flow

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

pvrst_flow = pvrst_flow.PVRSTFlow()


class TestPVRSTSuite2:

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

        pvrst_flow.create_pvrst_configuration(DUT1, "Ex 0/1", "Gi 0/10", "10", "20", "30", "pvrst")
        pvrst_flow.create_pvrst_configuration(DUT2, "Gi 0/3", "Gi 0/9", "10", "20", "30", "pvrst", "Gi 0/1")
        pvrst_flow.create_pvrst_configuration(DUT3, "Gi 0/3", "Gi 0/10", "10", "20", "30", "pvrst")

        # Check the default Root Bridge for VLAN 10 (the lowest MAC in the topology - DUT1)

        d_instance_vlan_10_1, dict_ports_instance_vlan_10_1, list_ports_instance_10_1 = DUT1.stp.show_spanning_tree_pvrst(vlan="10")
        d_instance_vlan_10_2, dict_ports_instance_vlan_10_2, list_ports_instance_10_2 = DUT2.stp.show_spanning_tree_pvrst(vlan="10")
        d_instance_vlan_10_3, dict_ports_instance_vlan_10_3, list_ports_instance_10_3 = DUT3.stp.show_spanning_tree_pvrst(vlan="10")

        # Asserting the default root bridges of all DUTs using PVRST flow

        pvrst_flow.assert_pvrst_root_bridges_3_DUTs(DUT1,  d_instance_vlan_10_1, "32778"
                                                 , DUT2,  d_instance_vlan_10_2, "32778"
                                                 , DUT3,  d_instance_vlan_10_3, "32778")

        # Check the Port Role of each DUT using PVRST flow

        pvrst_flow.assert_pvrst_ports_3_DUTs(DUT1, dict_ports_instance_vlan_10_1, "Ex 0/1", "Gi 0/10", "Designated",
                                          "Designated", "128", "20000", "128", "20000",
                                          DUT2, dict_ports_instance_vlan_10_2, "Gi 0/3", "Gi 0/9", "Designated", "Root",
                                          "128", "20000", "128", "20000",
                                          DUT3, dict_ports_instance_vlan_10_3, "Gi 0/3", "Gi 0/10", "Alternate", "Root",
                                          "128", "20000", "128", "20000")

        # Change the bridge priority on DUT3 for VLAN 10

        DUT3.stp.add_pvrst_bridge_priority(vlan="10", brg_priority="4096")

        # Check the new Root Bridge for VLAN 10(the lowest priority in the topology - DUT3)

        d_instance_vlan_10_1, dict_ports_instance_vlan_10_1, list_ports_instance_10_1 = DUT1.stp.show_spanning_tree_pvrst(
            vlan="10")
        d_instance_vlan_10_2, dict_ports_instance_vlan_10_2, list_ports_instance_10_2 = DUT2.stp.show_spanning_tree_pvrst(
            vlan="10")
        d_instance_vlan_10_3, dict_ports_instance_vlan_10_3, list_ports_instance_10_3 = DUT3.stp.show_spanning_tree_pvrst(
            vlan="10")

        # Asserting the new root bridges of all DUTs using PVRST flow

        pvrst_flow.assert_pvrst_root_bridges_3_DUTs(DUT1, d_instance_vlan_10_1, "32778"
                                                    , DUT2, d_instance_vlan_10_2, "32778"
                                                    , DUT3, d_instance_vlan_10_3, "4106")

        # Check the Port Role of each DUT using PVRST flow (after changing bridge priority)

        pvrst_flow.assert_pvrst_ports_3_DUTs(DUT1, dict_ports_instance_vlan_10_1, "Ex 0/1", "Gi 0/10", "Designated", "Root",
                                   "128", "20000", "128", "20000",
                                   DUT2, dict_ports_instance_vlan_10_2, "Gi 0/3", "Gi 0/9", "Root", "Alternate", "128",
                                   "20000", "128", "20000",
                                   DUT3, dict_ports_instance_vlan_10_3, "Gi 0/3", "Gi 0/10", "Designated", "Designated", "128",
                                   "20000", "128", "20000")

        # Remove the bridge-priority for VLAN 10 and check that DUT1 is the root for VLAN 10

        DUT3.stp.remove_pvrst_bridge_priority(vlan="10")

        # Check the default Root Bridge for VLAN 10 (the lowest MAC in the topology - DUT1)

        d_instance_vlan_10_1, dict_ports_instance_vlan_10_1, list_ports_instance_10_1 = DUT1.stp.show_spanning_tree_pvrst(
            vlan="10")
        d_instance_vlan_10_2, dict_ports_instance_vlan_10_2, list_ports_instance_10_2 = DUT2.stp.show_spanning_tree_pvrst(
            vlan="10")
        d_instance_vlan_10_3, dict_ports_instance_vlan_10_3, list_ports_instance_10_3 = DUT3.stp.show_spanning_tree_pvrst(
            vlan="10")

        # Asserting the default root bridges of all DUTs using PVRST flow

        pvrst_flow.assert_pvrst_root_bridges_3_DUTs(DUT1, d_instance_vlan_10_1, "32778"
                                                    , DUT2, d_instance_vlan_10_2, "32778"
                                                    , DUT3, d_instance_vlan_10_3, "32778")

        # Check the Port Role of each DUT using PVRST flow

        pvrst_flow.assert_pvrst_ports_3_DUTs(DUT1, dict_ports_instance_vlan_10_1, "Ex 0/1", "Gi 0/10", "Designated",
                                             "Designated", "128", "20000", "128", "20000",
                                             DUT2, dict_ports_instance_vlan_10_2, "Gi 0/3", "Gi 0/9", "Designated",
                                             "Root","128", "20000", "128", "20000",
                                             DUT3, dict_ports_instance_vlan_10_3, "Gi 0/3", "Gi 0/10", "Alternate",
                                             "Root","128", "20000", "128", "20000")

        print("########## Removing the config #############")

        pvrst_flow.remove_pvrst_configuration(DUT1, "Ex 0/1", "Gi 0/10", "10", "20", "30", "rst")
        pvrst_flow.remove_pvrst_configuration(DUT2, "Gi 0/3", "Gi 0/9", "10", "20", "30", "rst", "Gi 0/1")
        pvrst_flow.remove_pvrst_configuration(DUT3, "Gi 0/3", "Gi 0/10", "10", "20", "30", "rst")

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

        pvrst_flow.create_pvrst_configuration(DUT1, "Ex 0/1", "Gi 0/10", "10", "20", "30", "pvrst")
        pvrst_flow.create_pvrst_configuration(DUT2, "Gi 0/3", "Gi 0/9", "10", "20", "30", "pvrst", "Gi 0/1")
        pvrst_flow.create_pvrst_configuration(DUT3, "Gi 0/3", "Gi 0/10", "10", "20", "30", "pvrst")

        # Check the default Root Bridge for VLAN 10 (the lowest MAC in the topology - DUT1)

        d_instance_vlan_10_1, dict_ports_instance_vlan_10_1, list_ports_instance_10_1 = DUT1.stp.show_spanning_tree_pvrst(vlan="10")
        d_instance_vlan_10_2, dict_ports_instance_vlan_10_2, list_ports_instance_10_2 = DUT2.stp.show_spanning_tree_pvrst(vlan="10")
        d_instance_vlan_10_3, dict_ports_instance_vlan_10_3, list_ports_instance_10_3 = DUT3.stp.show_spanning_tree_pvrst(vlan="10")

        # Asserting the default root bridges of all DUTs using PVRST flow

        pvrst_flow.assert_pvrst_root_bridges_3_DUTs(DUT1,  d_instance_vlan_10_1, "32778"
                                                 , DUT2,  d_instance_vlan_10_2, "32778"
                                                 , DUT3,  d_instance_vlan_10_3, "32778")

        # Check the Port Role/Cost of each DUT using PVRST flow

        pvrst_flow.assert_pvrst_ports_3_DUTs(DUT1, dict_ports_instance_vlan_10_1, "Ex 0/1", "Gi 0/10", "Designated",
                                          "Designated", "128", "20000", "128", "20000",
                                          DUT2, dict_ports_instance_vlan_10_2, "Gi 0/3", "Gi 0/9", "Designated", "Root",
                                          "128", "20000", "128", "20000",
                                          DUT3, dict_ports_instance_vlan_10_3, "Gi 0/3", "Gi 0/10", "Alternate", "Root",
                                          "128", "20000", "128", "20000")

        #  Change the cost of the Root port of DUT3 of VLAN 10, so it becomes Alternate

        DUT3.stp.add_pvrst_port_cost(vlan="10", port="Gi 0/10", cost="50000")

        # Check the new Root Bridge for VLAN 10(the lowest priority in the topology - DUT3)

        d_instance_vlan_10_1, dict_ports_instance_vlan_10_1, list_ports_instance_10_1 = DUT1.stp.show_spanning_tree_pvrst(
            vlan="10")
        d_instance_vlan_10_2, dict_ports_instance_vlan_10_2, list_ports_instance_10_2 = DUT2.stp.show_spanning_tree_pvrst(
            vlan="10")
        d_instance_vlan_10_3, dict_ports_instance_vlan_10_3, list_ports_instance_10_3 = DUT3.stp.show_spanning_tree_pvrst(
            vlan="10")

        # Asserting root bridges of all DUTs using PVRST flow

        pvrst_flow.assert_pvrst_root_bridges_3_DUTs(DUT1, d_instance_vlan_10_1, "32778"
                                                    , DUT2, d_instance_vlan_10_2, "32778"
                                                    , DUT3, d_instance_vlan_10_3, "32778")

        # Check the Port Role/Cost of each DUT using PVRST flow (after changing the cost)

        pvrst_flow.assert_pvrst_ports_3_DUTs(DUT1, dict_ports_instance_vlan_10_1, "Ex 0/1", "Gi 0/10", "Designated", "Designated",
                                   "128", "20000", "128", "20000",
                                   DUT2, dict_ports_instance_vlan_10_2, "Gi 0/3", "Gi 0/9", "Designated", "Root", "128",
                                   "20000", "128", "20000",
                                   DUT3, dict_ports_instance_vlan_10_3, "Gi 0/3", "Gi 0/10", "Root", "Alternate",
                                   "128", "20000", "128", "50000")

        # Remove the cost for VLAN 10 and check that DUT3 ports are back in place

        DUT3.stp.remove_pvrst_port_cost(vlan="10", port="Gi 0/10")

        # Check the default Root Bridge for VLAN 10 (the lowest MAC in the topology - DUT1)

        d_instance_vlan_10_1, dict_ports_instance_vlan_10_1, list_ports_instance_10_1 = DUT1.stp.show_spanning_tree_pvrst(
            vlan="10")
        d_instance_vlan_10_2, dict_ports_instance_vlan_10_2, list_ports_instance_10_2 = DUT2.stp.show_spanning_tree_pvrst(
            vlan="10")
        d_instance_vlan_10_3, dict_ports_instance_vlan_10_3, list_ports_instance_10_3 = DUT3.stp.show_spanning_tree_pvrst(
            vlan="10")

        # Asserting the default root bridges of all DUTs using PVRST flow

        pvrst_flow.assert_pvrst_root_bridges_3_DUTs(DUT1, d_instance_vlan_10_1, "32778"
                                                    , DUT2, d_instance_vlan_10_2, "32778"
                                                    , DUT3, d_instance_vlan_10_3, "32778")

        # Check the Port Role of each DUT using PVRST flow

        pvrst_flow.assert_pvrst_ports_3_DUTs(DUT1, dict_ports_instance_vlan_10_1, "Ex 0/1", "Gi 0/10", "Designated",
                                             "Designated", "128", "20000", "128", "20000",
                                             DUT2, dict_ports_instance_vlan_10_2, "Gi 0/3", "Gi 0/9", "Designated",
                                             "Root","128", "20000", "128", "20000",
                                             DUT3, dict_ports_instance_vlan_10_3, "Gi 0/3", "Gi 0/10", "Alternate",
                                             "Root","128", "20000", "128", "20000")

        print("########## Removing the config #############")

        pvrst_flow.remove_pvrst_configuration(DUT1, "Ex 0/1", "Gi 0/10", "10", "20", "30", "rst")
        pvrst_flow.remove_pvrst_configuration(DUT2, "Gi 0/3", "Gi 0/9", "10", "20", "30", "rst", "Gi 0/1")
        pvrst_flow.remove_pvrst_configuration(DUT3, "Gi 0/3", "Gi 0/10", "10", "20", "30", "rst")

    def test_func_3(self):

        print("###### Test_func_3 ######")
        print("########## Verify PVRST port priority functionality #############")
        print("###### 2 DUTs ######")

        #    Topology
        #
        #  DUT1 == DUT2

        pvrst_flow.create_pvrst_configuration(DUT1, "Ex 0/1", "Ex 0/2", "10", "20", "30", "pvrst")
        pvrst_flow.create_pvrst_configuration(DUT2, "Gi 0/9", "Gi 0/10", "10", "20", "30", "pvrst", "Gi 0/1")

        # Check the default Root Bridge for VLAN 10 (the lowest MAC in the topology - DUT1)

        d_instance_vlan_10_1, dict_ports_instance_vlan_10_1, list_ports_instance_10_1 = DUT1.stp.show_spanning_tree_pvrst(
            vlan="10")
        d_instance_vlan_10_2, dict_ports_instance_vlan_10_2, list_ports_instance_10_2 = DUT2.stp.show_spanning_tree_pvrst(
            vlan="10")
        # Asserting the default root bridges of all DUTs using PVRST flow

        pvrst_flow.assert_pvrst_root_bridges_2_DUTs(DUT1, d_instance_vlan_10_1, "32778"
                                                    , DUT2, d_instance_vlan_10_2, "32778")

        # Check the Port Role/Cost of each DUT using PVRST flow

        pvrst_flow.assert_pvrst_ports_2_DUTs(DUT1, dict_ports_instance_vlan_10_1, "Ex 0/1", "Ex 0/2", "Designated",
                                             "Designated", "128", "20000", "128", "20000",
                                             DUT2, dict_ports_instance_vlan_10_2, "Gi 0/9", "Gi 0/10", "Root",
                                             "Alternate", "128", "20000", "128", "20000")

        # Change the port-priority of the remote port of DUT1 (Ex 0/2), so the port Gi 0/10 from DUT2 becomes Root

        DUT1.stp.add_pvrst_port_priority(vlan="10", port="Ex 0/2", port_priority="64")

        # Check the new Root Bridge for VLAN 10(the lowest priority in the topology - DUT3)

        d_instance_vlan_10_1, dict_ports_instance_vlan_10_1, list_ports_instance_10_1 = DUT1.stp.show_spanning_tree_pvrst(
            vlan="10")
        d_instance_vlan_10_2, dict_ports_instance_vlan_10_2, list_ports_instance_10_2 = DUT2.stp.show_spanning_tree_pvrst(
            vlan="10")

        # Asserting root bridges of all DUTs using PVRST flow

        pvrst_flow.assert_pvrst_root_bridges_2_DUTs(DUT1, d_instance_vlan_10_1, "32778"
                                                    , DUT2, d_instance_vlan_10_2, "32778")

        # Check the Port Role/Port-priority of each DUT using PVRST flow (after changing the port-priority)

        pvrst_flow.assert_pvrst_ports_2_DUTs(DUT1, dict_ports_instance_vlan_10_1, "Ex 0/1", "Ex 0/2", "Designated",
                                             "Designated", "128", "20000", "64", "20000",
                                             DUT2, dict_ports_instance_vlan_10_2, "Gi 0/9", "Gi 0/10", "Alternate",
                                             "Root", "128", "20000", "128", "20000")

        # Remove the port-priority from DUT1 and check that DUT2 ports are back in place

        DUT1.stp.remove_pvrst_port_priority(vlan="10", port="Ex 0/2")

        # Check the default Root Bridge for VLAN 10 (the lowest MAC in the topology - DUT1)

        d_instance_vlan_10_1, dict_ports_instance_vlan_10_1, list_ports_instance_10_1 = DUT1.stp.show_spanning_tree_pvrst(
            vlan="10")
        d_instance_vlan_10_2, dict_ports_instance_vlan_10_2, list_ports_instance_10_2 = DUT2.stp.show_spanning_tree_pvrst(
            vlan="10")

        # Asserting the default root bridges of all DUTs using PVRST flow

        pvrst_flow.assert_pvrst_root_bridges_2_DUTs(DUT1, d_instance_vlan_10_1, "32778"
                                                    , DUT2, d_instance_vlan_10_2, "32778")

        # Check the Port Role/Port-priority of each DUT using PVRST flow

        pvrst_flow.assert_pvrst_ports_2_DUTs(DUT1, dict_ports_instance_vlan_10_1, "Ex 0/1", "Ex 0/2", "Designated",
                                             "Designated", "128", "20000", "128", "20000",
                                             DUT2, dict_ports_instance_vlan_10_2, "Gi 0/9", "Gi 0/10", "Root",
                                             "Alternate", "128", "20000", "128", "20000")

        print("########## Removing the config #############")

        pvrst_flow.remove_pvrst_configuration(DUT1, "Ex 0/1", "Ex 0/2", "10", "20", "30", "rst")
        pvrst_flow.remove_pvrst_configuration(DUT2, "Gi 0/9", "Gi 0/10", "10", "20", "30", "rst", "Gi 0/1")

    def test_func_4(self):

        print("###### Test_func_4 ######")
        print("########## Verify PVRST root election by setting root primary #############")
        print("###### 3 DUTs ######")
        #    Topology
        #
        #  DUT1 -- DUT2
        #    \     /
        #     \   /
        #      DUT3

        pvrst_flow.create_pvrst_configuration(DUT1, "Ex 0/1", "Gi 0/10", "10", "20", "30", "pvrst")
        pvrst_flow.create_pvrst_configuration(DUT2, "Gi 0/3", "Gi 0/9", "10", "20", "30", "pvrst", "Gi 0/1")
        pvrst_flow.create_pvrst_configuration(DUT3, "Gi 0/3", "Gi 0/10", "10", "20", "30", "pvrst")

        # Check the default Root Bridge for VLAN 10 (the lowest MAC in the topology - DUT1)

        d_instance_vlan_10_1, dict_ports_instance_vlan_10_1, list_ports_instance_10_1 = DUT1.stp.show_spanning_tree_pvrst(vlan="10")
        d_instance_vlan_10_2, dict_ports_instance_vlan_10_2, list_ports_instance_10_2 = DUT2.stp.show_spanning_tree_pvrst(vlan="10")
        d_instance_vlan_10_3, dict_ports_instance_vlan_10_3, list_ports_instance_10_3 = DUT3.stp.show_spanning_tree_pvrst(vlan="10")

        # Asserting the default root bridges of all DUTs using PVRST flow

        pvrst_flow.assert_pvrst_root_bridges_3_DUTs(DUT1,  d_instance_vlan_10_1, "32778"
                                                 , DUT2,  d_instance_vlan_10_2, "32778"
                                                 , DUT3,  d_instance_vlan_10_3, "32778")

        # Check the Port Role of each DUT using PVRST flow

        pvrst_flow.assert_pvrst_ports_3_DUTs(DUT1, dict_ports_instance_vlan_10_1, "Ex 0/1", "Gi 0/10", "Designated",
                                          "Designated", "128", "20000", "128", "20000",
                                          DUT2, dict_ports_instance_vlan_10_2, "Gi 0/3", "Gi 0/9", "Designated", "Root",
                                          "128", "20000", "128", "20000",
                                          DUT3, dict_ports_instance_vlan_10_3, "Gi 0/3", "Gi 0/10", "Alternate", "Root",
                                          "128", "20000", "128", "20000")

        # Change the root priority on DUT3 for VLAN 10

        DUT3.stp.add_prvst_root_primary_secondary(vlan="10", root="primary")

        # Check the new Root Bridge for VLAN 10(the lowest priority in the topology - DUT3)

        d_instance_vlan_10_1, dict_ports_instance_vlan_10_1, list_ports_instance_10_1 = DUT1.stp.show_spanning_tree_pvrst(
            vlan="10")
        d_instance_vlan_10_2, dict_ports_instance_vlan_10_2, list_ports_instance_10_2 = DUT2.stp.show_spanning_tree_pvrst(
            vlan="10")
        d_instance_vlan_10_3, dict_ports_instance_vlan_10_3, list_ports_instance_10_3 = DUT3.stp.show_spanning_tree_pvrst(
            vlan="10")

        # Asserting the new root bridges of all DUTs using PVRST flow

        pvrst_flow.assert_pvrst_root_bridges_3_DUTs(DUT1, d_instance_vlan_10_1, "32778"
                                                    , DUT2, d_instance_vlan_10_2, "32778"
                                                    , DUT3, d_instance_vlan_10_3, "28682")

        # Check the Port Role of each DUT using PVRST flow (after changing bridge priority)

        pvrst_flow.assert_pvrst_ports_3_DUTs(DUT1, dict_ports_instance_vlan_10_1, "Ex 0/1", "Gi 0/10", "Designated", "Root",
                                   "128", "20000", "128", "20000",
                                   DUT2, dict_ports_instance_vlan_10_2, "Gi 0/3", "Gi 0/9", "Root", "Alternate", "128",
                                   "20000", "128", "20000",
                                   DUT3, dict_ports_instance_vlan_10_3, "Gi 0/3", "Gi 0/10", "Designated", "Designated", "128",
                                   "20000", "128", "20000")

        # Remove the root priority for VLAN 10 and check that DUT1 is the root for VLAN 10

        DUT3.stp.remove_pvrst_root_primary_secondary(vlan="10")

        # Check the default Root Bridge for VLAN 10 (the lowest MAC in the topology - DUT1)

        d_instance_vlan_10_1, dict_ports_instance_vlan_10_1, list_ports_instance_10_1 = DUT1.stp.show_spanning_tree_pvrst(
            vlan="10")
        d_instance_vlan_10_2, dict_ports_instance_vlan_10_2, list_ports_instance_10_2 = DUT2.stp.show_spanning_tree_pvrst(
            vlan="10")
        d_instance_vlan_10_3, dict_ports_instance_vlan_10_3, list_ports_instance_10_3 = DUT3.stp.show_spanning_tree_pvrst(
            vlan="10")

        # Asserting the default root bridges of all DUTs using PVRST flow

        pvrst_flow.assert_pvrst_root_bridges_3_DUTs(DUT1, d_instance_vlan_10_1, "32778"
                                                    , DUT2, d_instance_vlan_10_2, "32778"
                                                    , DUT3, d_instance_vlan_10_3, "32778")

        # Check the Port Role of each DUT using PVRST flow

        pvrst_flow.assert_pvrst_ports_3_DUTs(DUT1, dict_ports_instance_vlan_10_1, "Ex 0/1", "Gi 0/10", "Designated",
                                             "Designated", "128", "20000", "128", "20000",
                                             DUT2, dict_ports_instance_vlan_10_2, "Gi 0/3", "Gi 0/9", "Designated",
                                             "Root","128", "20000", "128", "20000",
                                             DUT3, dict_ports_instance_vlan_10_3, "Gi 0/3", "Gi 0/10", "Alternate",
                                             "Root","128", "20000", "128", "20000")

        print("########## Removing the config #############")

        pvrst_flow.remove_pvrst_configuration(DUT1, "Ex 0/1", "Gi 0/10", "10", "20", "30", "rst")
        pvrst_flow.remove_pvrst_configuration(DUT2, "Gi 0/3", "Gi 0/9", "10", "20", "30", "rst", "Gi 0/1")
        pvrst_flow.remove_pvrst_configuration(DUT3, "Gi 0/3", "Gi 0/10", "10", "20", "30", "rst")