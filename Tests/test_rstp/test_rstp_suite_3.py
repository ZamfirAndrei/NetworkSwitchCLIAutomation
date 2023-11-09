import time
from Management import dut_objects
from flows import rstpflow

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

rstp_flow = rstpflow.RSTPFlow()


class TestRSTPSuite3:

    def test_func_1(self):

        print("###### Test_func_1 ######")
        print("########## Verify RSTP (802.1W) root election #############")
        print("###### 3 DUTs ######")

        #    Topology
        #
        #  DUT1 -- DUT2
        #    \     /
        #     \   /
        #      DUT3

        rstp_flow.create_rstp_configuration(DUT1, "Ex 0/1", "Gi 0/10", "10", "20", "30", "rst")
        rstp_flow.create_rstp_configuration(DUT2, "Gi 0/3", "Gi 0/9", "10", "20", "30", "rst", "Gi 0/1")
        rstp_flow.create_rstp_configuration(DUT3, "Gi 0/3", "Gi 0/10", "10", "20", "30", "rst")

        # Check the default Root Bridge (the lowest MAC in the topology - DUT1)

        d_root_id_1, d_bridge_id_1, ports_1, dict_of_ports_1 = DUT1.stp.show_spanning_tree_rstp()
        d_root_id_2, d_bridge_id_2, ports_2, dict_of_ports_2 = DUT2.stp.show_spanning_tree_rstp()
        d_root_id_3, d_bridge_id_3, ports_3, dict_of_ports_3 = DUT3.stp.show_spanning_tree_rstp()

        # Asserting the default root bridges of all DUTs using RSTP flow

        rstp_flow.assert_root_3_DUTs(DUT1,  d_root_id_1, d_bridge_id_1, "32768"
                                , DUT2,  d_root_id_2, d_bridge_id_2,  "32768"
                                , DUT3,  d_root_id_3, d_bridge_id_3,  "32768")

        # Check the Port Role of each DUT

        rstp_flow.assert_rstp_ports_3_DUTs(DUT1, dict_of_ports_1, "Ex 0/1", "Gi 0/10", "Designated", "Designated", "128", "20000", "128", "20000",
                         DUT2, dict_of_ports_2, "Gi 0/3", "Gi 0/9", "Designated", "Root",  "128", "20000", "128", "20000",
                         DUT3, dict_of_ports_3, "Gi 0/3", "Gi 0/10", "Alternate", "Root", "128", "20000", "128", "20000")

        # Change the bridge priority on DUT3 using RSTP flow

        DUT3.stp.add_rstp_bridge_priority(bridge_priority="4096")

        # Check the new Root Bridge (the lowest priority in the topology - DUT3)

        d_root_id_1, d_bridge_id_1, ports_1, dict_of_ports_1 = DUT1.stp.show_spanning_tree_rstp()
        d_root_id_2, d_bridge_id_2, ports_2, dict_of_ports_2 = DUT2.stp.show_spanning_tree_rstp()
        d_root_id_3, d_bridge_id_3, ports_3, dict_of_ports_3 = DUT3.stp.show_spanning_tree_rstp()

        # Asserting the default root bridges of all DUTs using RSTP flow (after adding bridge priority)

        rstp_flow.assert_root_3_DUTs(DUT1, d_root_id_1, d_bridge_id_1, "32768"
                                     , DUT2, d_root_id_2, d_bridge_id_2, "32768"
                                     , DUT3, d_root_id_3, d_bridge_id_3, "4096")

        # Check the Port Role of each DUT using RSTP flow (after adding bridge priority)

        rstp_flow.assert_rstp_ports_3_DUTs(DUT1, dict_of_ports_1, "Ex 0/1", "Gi 0/10", "Designated", "Root",
                                   "128", "20000", "128", "20000",
                                   DUT2, dict_of_ports_2, "Gi 0/3", "Gi 0/9", "Root", "Alternate", "128",
                                   "20000", "128", "20000",
                                   DUT3, dict_of_ports_3, "Gi 0/3", "Gi 0/10", "Designated", "Designated", "128",
                                   "20000", "128", "20000")

        # Remove the bridge-priority and check that DUT1 is the root

        DUT3.stp.remove_rstp_bridge_priority()

        # Check the Root Bridge (the lowest MAC in the topology - DUT1)

        d_root_id_1, d_bridge_id_1, ports_1, dict_of_ports_1 = DUT1.stp.show_spanning_tree_rstp()
        d_root_id_2, d_bridge_id_2, ports_2, dict_of_ports_2 = DUT2.stp.show_spanning_tree_rstp()
        d_root_id_3, d_bridge_id_3, ports_3, dict_of_ports_3 = DUT3.stp.show_spanning_tree_rstp()

        # Asserting the default root bridges of all DUTs using RSTP flow

        rstp_flow.assert_root_3_DUTs(DUT1, d_root_id_1, d_bridge_id_1, "32768"
                                     , DUT2, d_root_id_2, d_bridge_id_2, "32768"
                                     , DUT3, d_root_id_3, d_bridge_id_3, "32768")

        # Check the Port Role of each DUT

        rstp_flow.assert_rstp_ports_3_DUTs(DUT1, dict_of_ports_1, "Ex 0/1", "Gi 0/10", "Designated", "Designated",
                                           "128", "20000", "128", "20000",
                                           DUT2, dict_of_ports_2, "Gi 0/3", "Gi 0/9", "Designated", "Root", "128",
                                           "20000", "128", "20000",
                                           DUT3, dict_of_ports_3, "Gi 0/3", "Gi 0/10", "Alternate", "Root", "128",
                                           "20000", "128", "20000")

        print("########## Removing the config #############")

        rstp_flow.remove_rstp_configuration(DUT1, "Ex 0/1", "Gi 0/10", "10", "20", "30")
        rstp_flow.remove_rstp_configuration(DUT2, "Gi 0/3", "Gi 0/9", "10", "20", "30", "Gi 0/1")
        rstp_flow.remove_rstp_configuration(DUT3, "Gi 0/3", "Gi 0/10", "10", "20", "30")

    def test_func_2(self):

        print("###### Test_func_2 ######")
        print("########## Verify RSTP (802.1W) port cost functionality #############")
        print("###### 3 DUTs ######")

        #    Topology
        #
        #  DUT1 -- DUT2
        #    \     /
        #     \   /
        #      DUT3

        rstp_flow.create_rstp_configuration(DUT1, "Ex 0/1", "Gi 0/10", "10", "20", "30", "rst")
        rstp_flow.create_rstp_configuration(DUT2, "Gi 0/3", "Gi 0/9", "10", "20", "30", "rst", "Gi 0/1")
        rstp_flow.create_rstp_configuration(DUT3, "Gi 0/3", "Gi 0/10", "10", "20", "30", "rst")

        # Check the default Root Bridge (the lowest MAC in the topology - DUT1)

        d_root_id_1, d_bridge_id_1, ports_1, dict_of_ports_1 = DUT1.stp.show_spanning_tree_rstp()
        d_root_id_2, d_bridge_id_2, ports_2, dict_of_ports_2 = DUT2.stp.show_spanning_tree_rstp()
        d_root_id_3, d_bridge_id_3, ports_3, dict_of_ports_3 = DUT3.stp.show_spanning_tree_rstp()

        # Asserting the default root bridges of all DUTs using RSTP flow

        rstp_flow.assert_root_3_DUTs(DUT1,  d_root_id_1, d_bridge_id_1, "32768"
                                , DUT2,  d_root_id_2, d_bridge_id_2,  "32768"
                                , DUT3,  d_root_id_3, d_bridge_id_3,  "32768")

        # Check the Port Role of each DUT

        rstp_flow.assert_rstp_ports_3_DUTs(DUT1, dict_of_ports_1, "Ex 0/1", "Gi 0/10", "Designated", "Designated", "128", "20000", "128", "20000",
                         DUT2, dict_of_ports_2, "Gi 0/3", "Gi 0/9", "Designated", "Root",  "128", "20000", "128", "20000",
                         DUT3, dict_of_ports_3, "Gi 0/3", "Gi 0/10", "Alternate", "Root", "128", "20000", "128", "20000")

        # Change the cost of the Root port of DUT3, so it becomes Alternate

        DUT3.stp.add_rstp_port_cost(port="Gi 0/10", cost="50000")

        # Check the new Root Bridge (the lowest priority in the topology - DUT3)

        d_root_id_1, d_bridge_id_1, ports_1, dict_of_ports_1 = DUT1.stp.show_spanning_tree_rstp()
        d_root_id_2, d_bridge_id_2, ports_2, dict_of_ports_2 = DUT2.stp.show_spanning_tree_rstp()
        d_root_id_3, d_bridge_id_3, ports_3, dict_of_ports_3 = DUT3.stp.show_spanning_tree_rstp()

        # Asserting the default root bridges of all DUTs using RSTP flow (after adding bridge priority)

        rstp_flow.assert_root_3_DUTs(DUT1, d_root_id_1, d_bridge_id_1, "32768"
                                     , DUT2, d_root_id_2, d_bridge_id_2, "32768"
                                     , DUT3, d_root_id_3, d_bridge_id_3, "32768")

        # Check the Port Role of each DUT using RSTP flow (after adding cost)

        rstp_flow.assert_rstp_ports_3_DUTs(DUT1, dict_of_ports_1, "Ex 0/1", "Gi 0/10", "Designated", "Designated",
                                           "128", "20000", "128", "20000",
                                           DUT2, dict_of_ports_2, "Gi 0/3", "Gi 0/9", "Designated", "Root", "128",
                                           "20000", "128", "20000",
                                           DUT3, dict_of_ports_3, "Gi 0/3", "Gi 0/10", "Root", "Alternate", "128",
                                           "20000", "128", "50000")

        # Remove the cost and check that DUT3 ports are back in place

        DUT3.stp.remove_rstp_port_cost(port="Gi 0/10")

        # Check the Root Bridge (the lowest MAC in the topology - DUT1)

        d_root_id_1, d_bridge_id_1, ports_1, dict_of_ports_1 = DUT1.stp.show_spanning_tree_rstp()
        d_root_id_2, d_bridge_id_2, ports_2, dict_of_ports_2 = DUT2.stp.show_spanning_tree_rstp()
        d_root_id_3, d_bridge_id_3, ports_3, dict_of_ports_3 = DUT3.stp.show_spanning_tree_rstp()

        # Asserting the default root bridges of all DUTs using RSTP flow

        rstp_flow.assert_root_3_DUTs(DUT1, d_root_id_1, d_bridge_id_1, "32768"
                                     , DUT2, d_root_id_2, d_bridge_id_2, "32768"
                                     , DUT3, d_root_id_3, d_bridge_id_3, "32768")

        # Check the Port Role of each DUT

        rstp_flow.assert_rstp_ports_3_DUTs(DUT1, dict_of_ports_1, "Ex 0/1", "Gi 0/10", "Designated", "Designated",
                                           "128", "20000", "128", "20000",
                                           DUT2, dict_of_ports_2, "Gi 0/3", "Gi 0/9", "Designated", "Root", "128",
                                           "20000", "128", "20000",
                                           DUT3, dict_of_ports_3, "Gi 0/3", "Gi 0/10", "Alternate", "Root", "128",
                                           "20000", "128", "20000")

        print("########## Removing the config #############")

        rstp_flow.remove_rstp_configuration(DUT1, "Ex 0/1", "Gi 0/10", "10", "20", "30")
        rstp_flow.remove_rstp_configuration(DUT2, "Gi 0/3", "Gi 0/9", "10", "20", "30", "Gi 0/1")
        rstp_flow.remove_rstp_configuration(DUT3, "Gi 0/3", "Gi 0/10", "10", "20", "30")

    def test_func_3(self):

        print("###### Test_func_3 ######")
        print("########## Verify RSTP (802.1W) port-priority functionality #############")
        print("###### 2 DUTs ######")

        #    Topology
        #
        #  DUT1 == DUT2

        rstp_flow.create_rstp_configuration(DUT1, "Ex 0/1", "Ex 0/2", "10", "20", "30", "rst")
        rstp_flow.create_rstp_configuration(DUT2, "Gi 0/9", "Gi 0/10", "10", "20", "30", "rst", "Gi 0/1")

        # Check the default Root Bridge (the lowest MAC in the topology - DUT1)

        d_root_id_1, d_bridge_id_1, ports_1, dict_of_ports_1 = DUT1.stp.show_spanning_tree_rstp()
        d_root_id_2, d_bridge_id_2, ports_2, dict_of_ports_2 = DUT2.stp.show_spanning_tree_rstp()

        # Asserting the default root bridges of all DUTs using RSTP flow

        rstp_flow.assert_root_2_DUTs(DUT1, d_root_id_1, d_bridge_id_1, "32768"
                                     , DUT2, d_root_id_2, d_bridge_id_2, "32768")

        # Check the Port Role of each DUT

        rstp_flow.assert_rstp_ports_2_DUTs(DUT1, dict_of_ports_1, "Ex 0/1", "Ex 0/2", "Designated", "Designated",
                                           "128", "20000", "128", "20000",
                                           DUT2, dict_of_ports_2, "Gi 0/9", "Gi 0/10", "Root", "Alternate", "128",
                                           "20000", "128", "20000")

        # Change the port-priority of the remote port of DUT1 (Ex 0/2), so the port Gi 0/10 from DUT2 becomes Root

        DUT1.stp.add_rstp_port_priority(port="Ex 0/2", port_priority="64")

        # Check the default Root Bridge (the lowest MAC in the topology - DUT1)

        d_root_id_1, d_bridge_id_1, ports_1, dict_of_ports_1 = DUT1.stp.show_spanning_tree_rstp()
        d_root_id_2, d_bridge_id_2, ports_2, dict_of_ports_2 = DUT2.stp.show_spanning_tree_rstp()

        # Asserting the default root bridges of all DUTs using RSTP flow

        rstp_flow.assert_root_2_DUTs(DUT1, d_root_id_1, d_bridge_id_1, "32768"
                                     , DUT2, d_root_id_2, d_bridge_id_2, "32768")

        # Check the Port Role of each DUT

        rstp_flow.assert_rstp_ports_2_DUTs(DUT1, dict_of_ports_1, "Ex 0/1", "Ex 0/2", "Designated", "Designated",
                                           "128", "20000", "64", "20000",
                                           DUT2, dict_of_ports_2, "Gi 0/9", "Gi 0/10",  "Alternate", "Root", "128",
                                           "20000", "128", "20000")

        # Remove the port-priority from DUT1 and check that DUT2 ports are back in place

        DUT1.stp.remove_rstp_port_priority(port="Ex 0/2")

        # Check the default Root Bridge (the lowest MAC in the topology - DUT1)

        d_root_id_1, d_bridge_id_1, ports_1, dict_of_ports_1 = DUT1.stp.show_spanning_tree_rstp()
        d_root_id_2, d_bridge_id_2, ports_2, dict_of_ports_2 = DUT2.stp.show_spanning_tree_rstp()

        # Asserting the default root bridges of all DUTs using RSTP flow

        rstp_flow.assert_root_2_DUTs(DUT1, d_root_id_1, d_bridge_id_1, "32768"
                                     , DUT2, d_root_id_2, d_bridge_id_2, "32768")

        # Check the Port Role of each DUT

        rstp_flow.assert_rstp_ports_2_DUTs(DUT1, dict_of_ports_1, "Ex 0/1", "Ex 0/2", "Designated", "Designated",
                                           "128", "20000", "128", "20000",
                                           DUT2, dict_of_ports_2, "Gi 0/9", "Gi 0/10", "Root", "Alternate", "128",
                                           "20000", "128", "20000")

        print("########## Removing the config #############")

        rstp_flow.remove_rstp_configuration(DUT1, "Ex 0/1", "Ex 0/2", "10", "20", "30")
        rstp_flow.remove_rstp_configuration(DUT2, "Gi 0/9", "Gi 0/10", "10", "20", "30", "Gi 0/1")
