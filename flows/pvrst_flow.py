from Management import dut_objects
from config import vlan


class PVRSTFlow:

    def create_pvrst_configuration(self, DUT, interfaces, vlans, mode, port_cambium_lab=None):

        # No shutting the interfaces

        for port in interfaces:

            DUT.int.no_shut_interface(interface=port)

        # Create VLANs on DUTs and assign ports to them

        for vlan in vlans:

            DUT.vl.create_vlan(vlan=vlan)

            for port in interfaces:

                DUT.vl.add_ports_to_vlan(vlan=vlan, ports=port)

        # Change the mode of STP to PVRST on all DUTs

        DUT.stp.change_stp_mode(mode=mode)

        # Disable STP on the link towards Cambium LAB

        if port_cambium_lab is not None:

            DUT.stp.stp_disable(port=port_cambium_lab)


    def remove_pvrst_configuration(self, DUT, interfaces, vlans, mode, port_cambium_lab=None):

        # Enabling stp on the port towards Cambium LAB

        if port_cambium_lab is not None:

            DUT.stp.stp_enable(port=port_cambium_lab)

        # Changing to default STP mode on DUT

        DUT.stp.change_stp_mode(mode=mode)

        # Removing the VLANs from DUT

        for vlan in vlans:

            DUT.vl.remove_vlan(vlan=vlan)

        # Shutting the ports on DUT

        for port in interfaces:

            DUT.int.shut_interface(interface=port)

    def assert_pvrst_bridge_and_root_id(self, DUT, vlan, bridge_id, bridge_id_priority, root_id, root_priority, d_instance_vlan=None):

        # Asserting the Root Bridge and Bridge ID

        d_instance_vlan, dict_of_ports_instance_vlan, list_ports_instance_vlan = DUT.stp.show_spanning_tree_pvrst(vlan=vlan)

        # print(d_instance_vlan)
        assert d_instance_vlan["Bridge ID Address"] == bridge_id
        assert d_instance_vlan["Bridge ID Priority"] == bridge_id_priority
        assert d_instance_vlan["Root ID Address"] == root_id
        assert d_instance_vlan["Root ID Priority"] == root_priority

        print(f"######## Successfully asserting the PVRST Root Bridge with brg_priority {root_priority} and Bridge ID of DUT {DUT.hostname} in instance {vlan} ")

    def assert_pvrst_root_bridge(self, DUT, vlan, brg_priority, d_instance_vlan):

        # Asserting the Root Bridge

        # d_instance_vlan, dict_ports_instance_vlan, list_ports_instance_vlan = DUT.stp.show_spanning_tree_pvrst(vlan=vlan)

        # print(d_instance_vlan)
        assert d_instance_vlan["Root ID Address"] == d_instance_vlan["Bridge ID Address"]
        assert d_instance_vlan["Root ID Priority"] == brg_priority

        print(f"######## Successfully asserting the PVRST Root Bridge of DUT {DUT.hostname} in instance {vlan}")

    def show_pvrst_spanning_tree(self, DUT, vlan):

        d_instance_vlan_dut, dict_of_ports_instance_vlan_dut, list_ports_instance_dut = DUT.stp.show_spanning_tree_pvrst(
            vlan=vlan)

        return d_instance_vlan_dut, dict_of_ports_instance_vlan_dut, list_ports_instance_dut

    # def assert_pvrst_root_bridges_3_DUTs(self, DUT1, brg_priority_1, DUT2,  brg_priority_2, DUT3, brg_priority_3, vlan):
    #
    #     d_instance_vlan_dut1, dict_ports_instance_vlan_dut1, list_ports_instance_dut1 = self.show_pvrst_spanning_tree(DUT1, vlan=vlan)
    #     d_instance_vlan_dut2, dict_ports_instance_vlan_dut2, list_ports_instance_dut2 = self.show_pvrst_spanning_tree(DUT2, vlan=vlan)
    #     d_instance_vlan_dut3, dict_ports_instance_vlan_dut3, list_ports_instance_dut3 = self.show_pvrst_spanning_tree(DUT3, vlan=vlan)
    #
    #     print(d_instance_vlan_dut1)
    #     print(d_instance_vlan_dut2)
    #     print(d_instance_vlan_dut3)
    #
    #     assert d_instance_vlan_dut1["Root ID Address"] == d_instance_vlan_dut2["Root ID Address"] == d_instance_vlan_dut3["Root ID Address"]
    #     assert d_instance_vlan_dut1["Bridge ID Priority"] == brg_priority_1
    #     assert d_instance_vlan_dut2["Bridge ID Priority"] == brg_priority_2
    #     assert d_instance_vlan_dut3["Bridge ID Priority"] == brg_priority_3
    #
    #     print("Successfully asserting the PVRST Root Bridge")

    # def assert_pvrst_root_bridges_2_DUTs(self, DUT1, d_instance_vlan_1, priority_1
    #                             , DUT2, d_instance_vlan_2, priority_2):
    #
    #     print(d_instance_vlan_1)
    #     print(d_instance_vlan_2)
    #
    #     assert d_instance_vlan_1["Root ID Address"] == d_instance_vlan_2["Root ID Address"]
    #     assert d_instance_vlan_1["Root ID Priority"] == priority_1
    #     assert d_instance_vlan_2["Root ID Priority"] == priority_2
    #
    #     print("Successfully asserting")

    def assert_pvrst_port(self, DUT, dict_of_ports_instance, port, role, port_priority=None, cost=None):

        port = port.replace(" ", "")
        # print(port)
        # print(dict_of_ports_instance[port])

        if dict_of_ports_instance[port]["Name"] == port:
            # print(dict_of_ports_instance[port])
            assert dict_of_ports_instance[port]["Role"] == role

            if cost is not None:
                assert dict_of_ports_instance[port]["Cost"] == cost

            if port_priority is not None:
                assert dict_of_ports_instance[port]["Prio"] == port_priority

            print(f"#### Successfully asserting for port {port} of DUT {DUT.hostname}")

    # def assert_pvrst_ports_3_DUTs(self, DUT1, port1_dut1, port2_dut1, role1_dut1, role2_dut1, port_priority1_dut1, port_priority2_dut1, cost1_dut1, cost2_dut1,
    #                      DUT2, port1_dut2, port2_dut2, role1_dut2, role2_dut2, port_priority1_dut2, port_priority2_dut2, cost1_dut2,  cost2_dut2,
    #                      DUT3, port1_dut3, port2_dut3, role1_dut3, role2_dut3, port_priority1_dut3, port_priority2_dut3, cost1_dut3,  cost2_dut3, vlan):
    #
    #     d_instance_vlan_dut1, dict_ports_instance_vlan_dut1, list_ports_instance_dut1 = self.show_pvrst_spanning_tree(
    #         DUT1, vlan=vlan)
    #     d_instance_vlan_dut2, dict_ports_instance_vlan_dut2, list_ports_instance_dut2 = self.show_pvrst_spanning_tree(
    #         DUT2, vlan=vlan)
    #     d_instance_vlan_dut3, dict_ports_instance_vlan_dut3, list_ports_instance_dut3 = self.show_pvrst_spanning_tree(
    #         DUT3, vlan=vlan)
    #
    #     print(dict_ports_instance_vlan_dut1)
    #     print(dict_ports_instance_vlan_dut2)
    #     print(dict_ports_instance_vlan_dut3)
    #
    #     # Asserting for DUT1 for both ports
    #
    #     self.assert_pvrst_port(DUT1, dict_ports_instance_vlan_dut1, port1_dut1, role1_dut1, port_priority1_dut1, cost1_dut1)
    #     self.assert_pvrst_port(DUT1, dict_ports_instance_vlan_dut1, port2_dut1, role2_dut1, port_priority2_dut1, cost2_dut1)
    #
    #     print(f"######## Successfully asserting the PVRST Ports of DUT {DUT1.hostname} in instance {vlan}")
    #
    #     # Asserting for DUT2 for both ports
    #
    #     self.assert_pvrst_port(DUT2, dict_ports_instance_vlan_dut2, port1_dut2, role1_dut2, port_priority1_dut2, cost1_dut2)
    #     self.assert_pvrst_port(DUT2, dict_ports_instance_vlan_dut2, port2_dut2, role2_dut2, port_priority2_dut2, cost2_dut2)
    #
    #     print(f"######## Successfully asserting the PVRST Ports of  DUT {DUT2.hostname} in instance {vlan}")
    #
    #     # Asserting for DUT3 for both ports
    #
    #     self.assert_pvrst_port(DUT3, dict_ports_instance_vlan_dut3, port1_dut3, role1_dut3, port_priority1_dut3, cost1_dut3)
    #     self.assert_pvrst_port(DUT3, dict_ports_instance_vlan_dut3, port2_dut3, role2_dut3, port_priority2_dut3, cost2_dut3)
    #
    #     print(f"######## Successfully asserting the PVRST Ports of DUT {DUT3.hostname} in instance {vlan}")
    #
    # def assert_pvrst_ports_2_DUTs(self, DUT1, dict_ports_instance_vlan_1, port1_1, port2_1, role1_1, role2_1, port_priority1_1, cost1_1, port_priority2_1, cost2_1,
    #                      DUT2, dict_ports_instance_vlan_2, port1_2, port2_2, role1_2, role2_2, port_priority1_2, cost1_2, port_priority2_2, cost2_2):
    #
    #     # Asserting for DUT1 for both ports
    #
    #     self.assert_pvrst_port(DUT1, dict_ports_instance_vlan_1, port1_1, role1_1, port_priority1_1, cost1_1)
    #     self.assert_pvrst_port(DUT1, dict_ports_instance_vlan_1, port2_1, role2_1, port_priority2_1, cost2_1)
    #
    #     # Asserting for DUT2 for both ports
    #
    #     self.assert_pvrst_port(DUT2, dict_ports_instance_vlan_2, port1_2, role1_2, port_priority1_2, cost1_2)
    #     self.assert_pvrst_port(DUT2, dict_ports_instance_vlan_2, port2_2, role2_2, port_priority2_2, cost2_2)

    def assert_pvrst_root_bridge_and_ports(self, DUT, port1_dut, role1_dut, port_priority1_dut,
                               cost1_dut, port2_dut, role2_dut, port_priority2_dut, cost2_dut, vlan, bridge_id, bridge_id_priority, root_id, root_priority):

        # Asserting the Root Bridge

        d_instance_vlan_dut, dict_of_ports_instance_vlan_dut, list_ports_instance_dut = self.show_pvrst_spanning_tree(
            DUT, vlan=vlan)

        # print(d_instance_vlan_dut)
        # print(dict_of_ports_instance_vlan_dut)

        self.assert_pvrst_bridge_and_root_id(DUT, vlan=vlan, d_instance_vlan=d_instance_vlan_dut, bridge_id=bridge_id, bridge_id_priority=bridge_id_priority, root_id=root_id, root_priority=root_priority)

        # Asserting for DUT for both ports

        self.assert_pvrst_port(DUT, dict_of_ports_instance_vlan_dut, port1_dut, role1_dut, port_priority1_dut,
                               cost1_dut)
        self.assert_pvrst_port(DUT, dict_of_ports_instance_vlan_dut, port2_dut, role2_dut, port_priority2_dut,
                               cost2_dut)

        print(f"######## Successfully asserting the PVRST Ports of DUT {DUT.hostname} in instance {vlan}")

    def assert_pvrst_ports(self, DUT, port1_dut, role1_dut, port_priority1_dut, cost1_dut,
                                      port2_dut, role2_dut, port_priority2_dut, cost2_dut, vlan):

        # Asserting the Root Bridge

        d_instance_vlan_dut, dict_of_ports_instance_vlan_dut, list_ports_instance_dut = self.show_pvrst_spanning_tree(
            DUT, vlan=vlan)

        # print(d_instance_vlan_dut)
        # print(dict_of_ports_instance_vlan_dut)

        # Asserting for DUT for both ports

        self.assert_pvrst_port(DUT, dict_of_ports_instance_vlan_dut, port1_dut, role1_dut, port_priority1_dut,
                               cost1_dut)
        self.assert_pvrst_port(DUT, dict_of_ports_instance_vlan_dut, port2_dut, role2_dut, port_priority2_dut,
                               cost2_dut)

        print(f"######## Successfully asserting the PVRST Ports of DUT {DUT.hostname} in instance {vlan}")