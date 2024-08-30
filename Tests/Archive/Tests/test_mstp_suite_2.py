import time
from Management import dut_objects
from flows import mstp_flow

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

mstp_flow = mstp_flow.MSTPFlow()


class TestMSTPSuite2:

    def test_func_1(self):

        print("###### Test_func_1 ######")
        print("########## Verify MSTP (802.1S) root election by setting priority #############")
        print("###### 3 DUTs ######")

        #    Topology
        #
        #  DUT1 -- DUT2
        #    \     /
        #     \   /
        #      DUT3
        #

        mstp_flow.create_mst_configuration(DUT1, "Ex 0/1", "Gi 0/10", "10", "20", "30", "mst", "1", "2", "10,20", "30", "Reg1")
        mstp_flow.create_mst_configuration(DUT2, "Gi 0/3", "Gi 0/9", "10", "20", "30", "mst", "1", "2", "10,20", "30", "Reg1", "Gi 0/1")
        mstp_flow.create_mst_configuration(DUT3, "Gi 0/3", "Gi 0/10", "10", "20", "30", "mst", "1", "2", "10,20", "30","Reg1")

        # Check the default Root Bridge for Instance 1 (the lowest MAC in the topology - DUT1)

        d_instance_zero_1, d_instance_1, dict_of_ports_instance_1 = DUT1.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero_2, d_instance_2, dict_of_ports_instance_2 = DUT2.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero_3, d_instance_3, dict_of_ports_instance_3 = DUT3.stp.show_spanning_tree_mst(instance="1")

        # Asserting the default root bridges of all DUTs using MSTP flow

        mstp_flow.assert_mst_root_bridges_3_DUTs( DUT1, d_instance_1, "32768"
                                , DUT2, d_instance_2,  "32768"
                                , DUT3, d_instance_3,  "32768")

        # Asserting the default ports of Instance 1 of all DUTs using MSTP flow

        mstp_flow.assert_mst_ports_3_DUTs(DUT1, dict_of_ports_instance_1, "Ex 0/1", "Gi 0/10", "Designated", "Designated", "128", "20000", "128", "20000",
                         DUT2, dict_of_ports_instance_2, "Gi 0/3", "Gi 0/9", "Designated", "Root",  "128", "20000", "128", "20000",
                         DUT3, dict_of_ports_instance_3, "Gi 0/3", "Gi 0/10", "Alternate", "Root", "128", "20000", "128", "20000")

        # Change the bridge priority on DUT3 for Instance 1

        DUT3.stp.add_mst_priority(instance="1", priority="4096")

        # Check the new Root Bridge for Instance 1 (the lowest priority in the topology - DUT3)

        d_instance_zero_1, d_instance_1, dict_of_ports_instance_1 = DUT1.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero_2, d_instance_2, dict_of_ports_instance_2 = DUT2.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero_3, d_instance_3, dict_of_ports_instance_3 = DUT3.stp.show_spanning_tree_mst(instance="1")

        # Asserting the root bridges of all DUTs using MSTP flow (after adding bridge priority)

        mstp_flow.assert_mst_root_bridges_3_DUTs(DUT1, d_instance_1, "32768"
                                          , DUT2, d_instance_2, "32768"
                                          , DUT3, d_instance_3, "4096")

        # Asserting the ports of Instance 1 of all DUTs using MSTP flow (after adding bridge priority)

        mstp_flow.assert_mst_ports_3_DUTs(DUT1, dict_of_ports_instance_1, "Ex 0/1", "Gi 0/10", "Designated", "Root",
                                   "128", "20000", "128", "20000",
                                   DUT2, dict_of_ports_instance_2, "Gi 0/3", "Gi 0/9", "Root", "Alternate", "128",
                                   "20000", "128", "20000",
                                   DUT3, dict_of_ports_instance_3, "Gi 0/3", "Gi 0/10", "Designated", "Designated", "128",
                                   "20000", "128", "20000")

        # Remove the bridge-priority for Instance 1 and check that DUT1 is the root for Instance 1

        DUT3.stp.remove_mst_priority(instance="1")

        # Check the default Root Bridge (the lowest MAC in the topology - DUT1)

        d_instance_zero_1, d_instance_1, dict_of_ports_instance_1 = DUT1.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero_2, d_instance_2, dict_of_ports_instance_2 = DUT2.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero_3, d_instance_3, dict_of_ports_instance_3 = DUT3.stp.show_spanning_tree_mst(instance="1")

        # Asserting the default root bridges of all DUTs using MSTP flow (after removing the bridge priority)

        mstp_flow.assert_mst_root_bridges_3_DUTs( DUT1, d_instance_1, "32768"
                                , DUT2, d_instance_2,  "32768"
                                , DUT3, d_instance_3,  "32768")

        # Asserting the default ports of Instance 1 of all DUTs using MSTP flow (after removing the bridge priority)

        mstp_flow.assert_mst_ports_3_DUTs(DUT1, dict_of_ports_instance_1, "Ex 0/1", "Gi 0/10", "Designated", "Designated", "128", "20000", "128", "20000",
                         DUT2, dict_of_ports_instance_2, "Gi 0/3", "Gi 0/9", "Designated", "Root",  "128", "20000", "128", "20000",
                         DUT3, dict_of_ports_instance_3, "Gi 0/3", "Gi 0/10", "Alternate", "Root", "128", "20000", "128", "20000")

        print("########## Removing the config #############")

        mstp_flow.remove_mst_configuration(DUT1, "Ex 0/1", "Gi 0/10", "10", "20", "30", "rst")
        mstp_flow.remove_mst_configuration(DUT2, "Gi 0/3", "Gi 0/9", "10", "20", "30", "rst", "Gi 0/1")
        mstp_flow.remove_mst_configuration(DUT3, "Gi 0/3", "Gi 0/10", "10", "20", "30", "rst")

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
        #

        mstp_flow.create_mst_configuration(DUT1, "Ex 0/1", "Gi 0/10", "10", "20", "30", "mst", "1", "2", "10,20",
                                                "30", "Reg1")
        mstp_flow.create_mst_configuration(DUT2, "Gi 0/3", "Gi 0/9", "10", "20", "30", "mst", "1", "2", "10,20",
                                                "30", "Reg1", "Gi 0/1")
        mstp_flow.create_mst_configuration(DUT3, "Gi 0/3", "Gi 0/10", "10", "20", "30", "mst", "1", "2", "10,20",
                                                "30", "Reg1")

        # Check the default Root Bridge for Instance 1 (the lowest MAC in the topology - DUT1)

        d_instance_zero_1, d_instance_1, dict_of_ports_instance_1 = DUT1.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero_2, d_instance_2, dict_of_ports_instance_2 = DUT2.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero_3, d_instance_3, dict_of_ports_instance_3 = DUT3.stp.show_spanning_tree_mst(instance="1")

        # Asserting the default root bridges of all DUTs using MSTP flow

        mstp_flow.assert_mst_root_bridges_3_DUTs(DUT1, d_instance_1, "32768"
                                        , DUT2, d_instance_2, "32768"
                                        , DUT3, d_instance_3, "32768")

        # Asserting the default ports of Instance 1 of all DUTs using MSTP flow

        mstp_flow.assert_mst_ports_3_DUTs(DUT1, dict_of_ports_instance_1, "Ex 0/1", "Gi 0/10", "Designated", "Designated",
                                       "128", "20000", "128", "20000",
                                   DUT2, dict_of_ports_instance_2, "Gi 0/3", "Gi 0/9", "Designated", "Root", "128",
                                       "20000", "128", "20000",
                                   DUT3, dict_of_ports_instance_3, "Gi 0/3", "Gi 0/10", "Alternate", "Root", "128",
                                       "20000", "128", "20000")

        # Change the cost of the Root port of DUT3 of Instance 1, so it becomes Alternate

        DUT3.stp.add_mst_port_cost(instance="1", port="Gi 0/10", cost="50000")

        # Check the Root Bridge for Instance 1 (the lowest priority in the topology - DUT1)

        d_instance_zero_1, d_instance_1, dict_of_ports_instance_1 = DUT1.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero_2, d_instance_2, dict_of_ports_instance_2 = DUT2.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero_3, d_instance_3, dict_of_ports_instance_3 = DUT3.stp.show_spanning_tree_mst(instance="1")

        # Asserting the root bridges of all DUTs using MSTP flow

        mstp_flow.assert_mst_root_bridges_3_DUTs(DUT1, d_instance_1, "32768"
                                        , DUT2, d_instance_2, "32768"
                                        , DUT3, d_instance_3, "32768")

        # Asserting the ports of Instance 1 of all DUTs using MSTP flow (after adding the cost)

        mstp_flow.assert_mst_ports_3_DUTs(DUT1, dict_of_ports_instance_1, "Ex 0/1", "Gi 0/10", "Designated", "Designated",
                                       "128", "20000", "128", "20000",
                                   DUT2, dict_of_ports_instance_2, "Gi 0/3", "Gi 0/9", "Designated", "Root", "128",
                                       "20000", "128", "20000",
                                   DUT3, dict_of_ports_instance_3, "Gi 0/3", "Gi 0/10", "Root", "Alternate",
                                       "128", "20000", "128", "50000")

        # Remove the cost for Instance 1 and check that DUT1 is the root for Instance 1

        DUT3.stp.remove_mst_port_cost(instance="1", port="Gi 0/10")

        # Check the default Root Bridge (the lowest MAC in the topology - DUT1)

        d_instance_zero_1, d_instance_1, dict_of_ports_instance_1 = DUT1.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero_2, d_instance_2, dict_of_ports_instance_2 = DUT2.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero_3, d_instance_3, dict_of_ports_instance_3 = DUT3.stp.show_spanning_tree_mst(instance="1")

        # Asserting the default root bridges of all DUTs using MSTP flow (after removing the bridge priority)

        mstp_flow.assert_mst_root_bridges_3_DUTs(DUT1, d_instance_1, "32768"
                                        , DUT2, d_instance_2, "32768"
                                        , DUT3, d_instance_3, "32768")

        # Asserting the default ports of Instance 1 of all DUTs using MSTP flow (after removing the cost)

        mstp_flow.assert_mst_ports_3_DUTs(DUT1, dict_of_ports_instance_1, "Ex 0/1", "Gi 0/10", "Designated", "Designated",
                                       "128", "20000", "128", "20000",
                                   DUT2, dict_of_ports_instance_2, "Gi 0/3", "Gi 0/9", "Designated", "Root", "128",
                                       "20000", "128", "20000",
                                   DUT3, dict_of_ports_instance_3, "Gi 0/3", "Gi 0/10", "Alternate", "Root", "128",
                                       "20000", "128", "20000")

        print("########## Removing the config #############")

        mstp_flow.remove_mst_configuration(DUT1, "Ex 0/1", "Gi 0/10", "10", "20", "30", "rst")
        mstp_flow.remove_mst_configuration(DUT2, "Gi 0/3", "Gi 0/9", "10", "20", "30", "rst", "Gi 0/1")
        mstp_flow.remove_mst_configuration(DUT3, "Gi 0/3", "Gi 0/10", "10", "20", "30", "rst")

    def test_func_3(self):

        print("###### Test_func_3 ######")
        print("########## Verify MSTP (802.1S) port priority functionality #############")
        print("###### 2 DUTs ######")

        #    Topology
        #
        #  DUT1 == DUT2

        mstp_flow.create_mst_configuration(DUT1, "Ex 0/1", "Ex 0/2", "10", "20", "30", "mst", "1", "2", "10,20",
                                            "30", "Reg1")
        mstp_flow.create_mst_configuration(DUT2, "Gi 0/9", "Gi 0/10", "10", "20", "30", "mst", "1", "2", "10,20",
                                            "30", "Reg1", "Gi 0/1")

        # Check the default Root Bridge for Instance 1 (the lowest MAC in the topology - DUT1)

        d_instance_zero_1, d_instance_1, dict_of_ports_instance_1 = DUT1.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero_2, d_instance_2, dict_of_ports_instance_2 = DUT2.stp.show_spanning_tree_mst(instance="1")

        # Asserting the default root bridges of all DUTs using MSTP flow

        mstp_flow.assert_mst_root_bridges_2_DUTs(DUT1, d_instance_1, "32768"
                                          , DUT2, d_instance_2, "32768")

        # Asserting the default ports of Instance 1 of all DUTs using MSTP flow

        mstp_flow.assert_mst_ports_2_DUTs(DUT1, dict_of_ports_instance_1, "Ex 0/1", "Ex 0/2", "Designated", "Designated",
                                   "128", "20000", "128", "20000",
                                   DUT2, dict_of_ports_instance_2, "Gi 0/9", "Gi 0/10", "Root", "Alternate", "128",
                                   "20000", "128", "20000")

        # Change the port-priority of the remote port of DUT1 (Ex 0/2), so the port Gi 0/10 from DUT2 becomes Root

        DUT1.stp.add_mst_port_priority(instance="1", port="Ex 0/2", port_priority="64")

        # Check the Root Bridge for Instance 1 (the lowest priority in the topology - DUT1)

        d_instance_zero_1, d_instance_1, dict_of_ports_instance_1 = DUT1.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero_2, d_instance_2, dict_of_ports_instance_2 = DUT2.stp.show_spanning_tree_mst(instance="1")

        # Asserting the root bridges of all DUTs using MSTP flow

        mstp_flow.assert_mst_root_bridges_2_DUTs(DUT1, d_instance_1, "32768"
                                          , DUT2, d_instance_2, "32768")

        # Asserting the ports of Instance 1 of all DUTs using MSTP flow (after adding the port-priority)

        mstp_flow.assert_mst_ports_2_DUTs(DUT1, dict_of_ports_instance_1, "Ex 0/1", "Ex 0/2", "Designated", "Designated",
                                   "128", "20000", "64", "20000",
                                   DUT2, dict_of_ports_instance_2, "Gi 0/9", "Gi 0/10", "Alternate", "Root", "128",
                                   "20000", "128", "20000")

        # Remove the cost for Instance 1 and check that DUT1 is the root for Instance 1

        DUT1.stp.remove_mst_port_priority(instance="1", port="Ex 0/2")

        # Check the default Root Bridge (the lowest MAC in the topology - DUT1)

        d_instance_zero_1, d_instance_1, dict_of_ports_instance_1 = DUT1.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero_2, d_instance_2, dict_of_ports_instance_2 = DUT2.stp.show_spanning_tree_mst(instance="1")

        # Asserting the default root bridges of all DUTs using MSTP flow (after removing the port-priority)

        mstp_flow.assert_mst_root_bridges_2_DUTs(DUT1, d_instance_1, "32768"
                                          , DUT2, d_instance_2, "32768")

        # Asserting the default ports of Instance 1 of all DUTs using MSTP flow (after removing the port-priority)

        mstp_flow.assert_mst_ports_2_DUTs(DUT1, dict_of_ports_instance_1, "Ex 0/1", "Ex 0/2", "Designated", "Designated",
                                   "128", "20000", "128", "20000",
                                   DUT2, dict_of_ports_instance_2, "Gi 0/9", "Gi 0/10", "Root", "Alternate", "128",
                                   "20000", "128", "20000")

        print("########## Removing the config #############")

        mstp_flow.remove_mst_configuration(DUT1, "Ex 0/1", "Ex 0/2", "10", "20", "30", "rst")
        mstp_flow.remove_mst_configuration(DUT2, "Gi 0/9", "Gi 0/10", "10", "20", "30", "rst", "Gi 0/1")

    def test_func_4(self):

        print("###### Test_func_4 ######")
        print("########## Verify MSTP (802.1S) root election by setting root primary #############")
        print("###### 3 DUTs ######")

        #    Topology
        #
        #  DUT1 -- DUT2
        #    \     /
        #     \   /
        #      DUT3
        #

        mstp_flow.create_mst_configuration(DUT1, "Ex 0/1", "Gi 0/10", "10", "20", "30", "mst", "1", "2", "10,20", "30",
                                            "Reg1")
        mstp_flow.create_mst_configuration(DUT2, "Gi 0/3", "Gi 0/9", "10", "20", "30", "mst", "1", "2", "10,20", "30",
                                            "Reg1", "Gi 0/1")
        mstp_flow.create_mst_configuration(DUT3, "Gi 0/3", "Gi 0/10", "10", "20", "30", "mst", "1", "2", "10,20", "30",
                                            "Reg1")

        # Check the default Root Bridge for Instance 1 (the lowest MAC in the topology - DUT1)

        d_instance_zero_1, d_instance_1, dict_of_ports_instance_1 = DUT1.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero_2, d_instance_2, dict_of_ports_instance_2 = DUT2.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero_3, d_instance_3, dict_of_ports_instance_3 = DUT3.stp.show_spanning_tree_mst(instance="1")

        # Asserting the default root bridges of all DUTs using MSTP flow

        mstp_flow.assert_mst_root_bridges_3_DUTs(DUT1, d_instance_1, "32768"
                                                 , DUT2, d_instance_2, "32768"
                                                 , DUT3, d_instance_3, "32768")

        # Asserting the default ports of Instance 1 of all DUTs using MSTP flow

        mstp_flow.assert_mst_ports_3_DUTs(DUT1, dict_of_ports_instance_1, "Ex 0/1", "Gi 0/10", "Designated",
                                          "Designated", "128", "20000", "128", "20000",
                                          DUT2, dict_of_ports_instance_2, "Gi 0/3", "Gi 0/9", "Designated", "Root",
                                          "128", "20000", "128", "20000",
                                          DUT3, dict_of_ports_instance_3, "Gi 0/3", "Gi 0/10", "Alternate", "Root",
                                          "128", "20000", "128", "20000")

        # Change the bridge priority on DUT3 for Instance 1 using root primary

        DUT3.stp.add_mst_root_primary_secondary(instance="1", root="primary")

        # Check the new Root Bridge for Instance 1 (the lowest priority in the topology - DUT3)

        d_instance_zero_1, d_instance_1, dict_of_ports_instance_1 = DUT1.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero_2, d_instance_2, dict_of_ports_instance_2 = DUT2.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero_3, d_instance_3, dict_of_ports_instance_3 = DUT3.stp.show_spanning_tree_mst(instance="1")

        # Asserting the root bridges of all DUTs using MSTP flow (after adding root priority)

        mstp_flow.assert_mst_root_bridges_3_DUTs(DUT1, d_instance_1, "32768"
                                                 , DUT2, d_instance_2, "32768"
                                                 , DUT3, d_instance_3, "24576")

        # Asserting the ports of Instance 1 of all DUTs using MSTP flow (after adding root priority)

        mstp_flow.assert_mst_ports_3_DUTs(DUT1, dict_of_ports_instance_1, "Ex 0/1", "Gi 0/10", "Designated", "Root",
                                          "128", "20000", "128", "20000",
                                          DUT2, dict_of_ports_instance_2, "Gi 0/3", "Gi 0/9", "Root", "Alternate",
                                          "128",
                                          "20000", "128", "20000",
                                          DUT3, dict_of_ports_instance_3, "Gi 0/3", "Gi 0/10", "Designated",
                                          "Designated", "128",
                                          "20000", "128", "20000")

        # Remove the root priority for Instance 1 and check that DUT1 is the root for Instance 1

        DUT3.stp.remove_mst_root_primary_secondary(instance="1")

        # Check the default Root Bridge (the lowest MAC in the topology - DUT1)

        d_instance_zero_1, d_instance_1, dict_of_ports_instance_1 = DUT1.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero_2, d_instance_2, dict_of_ports_instance_2 = DUT2.stp.show_spanning_tree_mst(instance="1")
        d_instance_zero_3, d_instance_3, dict_of_ports_instance_3 = DUT3.stp.show_spanning_tree_mst(instance="1")

        # Asserting the default root bridges of all DUTs using MSTP flow (after removing the root priority)

        mstp_flow.assert_mst_root_bridges_3_DUTs(DUT1, d_instance_1, "32768"
                                                 , DUT2, d_instance_2, "32768"
                                                 , DUT3, d_instance_3, "32768")

        # Asserting the default ports of Instance 1 of all DUTs using MSTP flow (after removing the root priority)

        mstp_flow.assert_mst_ports_3_DUTs(DUT1, dict_of_ports_instance_1, "Ex 0/1", "Gi 0/10", "Designated",
                                          "Designated", "128", "20000", "128", "20000",
                                          DUT2, dict_of_ports_instance_2, "Gi 0/3", "Gi 0/9", "Designated", "Root",
                                          "128", "20000", "128", "20000",
                                          DUT3, dict_of_ports_instance_3, "Gi 0/3", "Gi 0/10", "Alternate", "Root",
                                          "128", "20000", "128", "20000")

        print("########## Removing the config #############")

        mstp_flow.remove_mst_configuration(DUT1, "Ex 0/1", "Gi 0/10", "10", "20", "30", "rst")
        mstp_flow.remove_mst_configuration(DUT2, "Gi 0/3", "Gi 0/9", "10", "20", "30", "rst", "Gi 0/1")
        mstp_flow.remove_mst_configuration(DUT3, "Gi 0/3", "Gi 0/10", "10", "20", "30", "rst")

