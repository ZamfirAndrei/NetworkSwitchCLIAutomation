from Management import dut_objects
from config import vlan


class PVRSTFlow:

    def create_pvrst_configuration(self, DUT, int1, int2, vlan1, vlan2, vlan3, mode, port_cambium_lab=None):

        # No shutting the interfaces

        DUT.int.no_shut_interfaces(int1, int2)

        # Create VLANs on DUTs and assign ports to them

        DUT.vl.create_vlans(vlan1, vlan2, vlan3)
        DUT.vl.add_more_ports_to_more_vlans(vlan1, vlan2, vlan3, port1=int1, port12=int2)

        # Change the mode of STP to PVRST on all DUTs

        DUT.stp.change_stp_mode(mode=mode)

        # Disable STP on the link towards Cambium LAB

        if port_cambium_lab is not None:

            DUT.stp.stp_disable(port=port_cambium_lab)


    def remove_pvrst_configuration(self, DUT, int1, int2, vlan1, vlan2, vlan3, mode, port_cambium_lab=None):

        # Enabling stp on the port towards Cambium LAB

        if port_cambium_lab is not None:

            DUT.stp.stp_enable(port=port_cambium_lab)

        # Changing to default STP mode on DUT

        DUT.stp.change_stp_mode(mode=mode)

        # Removing the VLANs from DUT

        DUT.vl.remove_vlans(vlan1, vlan2, vlan3)

        # Shutting the ports on DUT

        DUT.int.shut_interfaces(int1, int2)

    def assert_pvrst_root_bridge(self, DUT, vlan, d_instance_vlan, dict_ports_instance_vlan, priority):

        d_instance_vlan, dict_ports_instance_vlan, list_ports_instance_vlan = DUT.stp.show_spanning_tree_pvrst(vlan=vlan)

        print(d_instance_vlan)
        assert d_instance_vlan["Root ID Address"] == d_instance_vlan["Bridge ID Address"]
        assert d_instance_vlan["Root ID Priority"] == priority

        print("Successfully asserting")

    def assert_pvrst_root_bridges_3_DUTs(self, DUT1, d_instance_vlan_1, priority_1
                                , DUT2, d_instance_vlan_2, priority_2
                                , DUT3, d_instance_vlan_3, priority_3):

        print(d_instance_vlan_1)
        print(d_instance_vlan_2)
        print(d_instance_vlan_3)

        assert d_instance_vlan_1["Root ID Address"] == d_instance_vlan_2["Root ID Address"] == d_instance_vlan_3["Root ID Address"]
        assert d_instance_vlan_1["Bridge ID Priority"] == priority_1
        assert d_instance_vlan_2["Bridge ID Priority"] == priority_2
        assert d_instance_vlan_3["Bridge ID Priority"] == priority_3

        print("Successfully asserting")

    def assert_pvrst_root_bridges_2_DUTs(self, DUT1, d_instance_vlan_1, priority_1
                                , DUT2, d_instance_vlan_2, priority_2):

        print(d_instance_vlan_1)
        print(d_instance_vlan_2)

        assert d_instance_vlan_1["Root ID Address"] == d_instance_vlan_2["Root ID Address"]
        assert d_instance_vlan_1["Root ID Priority"] == priority_1
        assert d_instance_vlan_2["Root ID Priority"] == priority_2

        print("Successfully asserting")

    def assert_pvrst_port(self, DUT, dict_of_ports_instance, port, role, port_priority=None, cost=None):

        port = port.replace(" ", "")
        # print(port)
        print(dict_of_ports_instance[port])

        if dict_of_ports_instance[port]["Name"] == port:
            # print(dict_of_ports_instance[port])
            assert dict_of_ports_instance[port]["Role"] == role

            if cost is not None:
                assert dict_of_ports_instance[port]["Cost"] == cost

            if port_priority is not None:
                assert dict_of_ports_instance[port]["Prio"] == port_priority

        print("Successfully asserting")

    def assert_pvrst_ports_3_DUTs(self, DUT1, dict_ports_instance_vlan_1, port1_1, port2_1, role1_1, role2_1, port_priority1_1, cost1_1, port_priority2_1, cost2_1,
                         DUT2, dict_ports_instance_vlan_2, port1_2, port2_2, role1_2, role2_2, port_priority1_2, cost1_2, port_priority2_2, cost2_2,
                         DUT3, dict_ports_instance_vlan_3, port1_3, port2_3, role1_3, role2_3, port_priority1_3, cost1_3, port_priority2_3, cost2_3):

        # Asserting for DUT1 for both ports

        self.assert_pvrst_port(DUT1, dict_ports_instance_vlan_1, port1_1, role1_1, port_priority1_1, cost1_1)
        self.assert_pvrst_port(DUT1, dict_ports_instance_vlan_1, port2_1, role2_1, port_priority2_1, cost2_1)

        # Asserting for DUT2 for both ports

        self.assert_pvrst_port(DUT2, dict_ports_instance_vlan_2, port1_2, role1_2, port_priority1_2, cost1_2)
        self.assert_pvrst_port(DUT2, dict_ports_instance_vlan_2, port2_2, role2_2, port_priority2_2, cost2_2)

        # Asserting for DUT3 for both ports

        self.assert_pvrst_port(DUT3, dict_ports_instance_vlan_3, port1_3, role1_3, port_priority1_3, cost1_3)
        self.assert_pvrst_port(DUT3, dict_ports_instance_vlan_3, port2_3, role2_3, port_priority2_3, cost2_3)

    def assert_pvrst_ports_2_DUTs(self, DUT1, dict_ports_instance_vlan_1, port1_1, port2_1, role1_1, role2_1, port_priority1_1, cost1_1, port_priority2_1, cost2_1,
                         DUT2, dict_ports_instance_vlan_2, port1_2, port2_2, role1_2, role2_2, port_priority1_2, cost1_2, port_priority2_2, cost2_2):

        # Asserting for DUT1 for both ports

        self.assert_pvrst_port(DUT1, dict_ports_instance_vlan_1, port1_1, role1_1, port_priority1_1, cost1_1)
        self.assert_pvrst_port(DUT1, dict_ports_instance_vlan_1, port2_1, role2_1, port_priority2_1, cost2_1)

        # Asserting for DUT2 for both ports

        self.assert_pvrst_port(DUT2, dict_ports_instance_vlan_2, port1_2, role1_2, port_priority1_2, cost1_2)
        self.assert_pvrst_port(DUT2, dict_ports_instance_vlan_2, port2_2, role2_2, port_priority2_2, cost2_2)