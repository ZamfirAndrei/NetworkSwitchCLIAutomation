from Management import dut_objects
from config import vlan


class MSTPFlow:

    def create_mst_configuration(self, DUT, int1, int2, vlan1, vlan2, vlan3, mode, instance1, instance2, vlans_instance_1, vlans_instance_2, region, port_cambium_lab=None):

        # No shutting the interfaces

        DUT.int.no_shut_interfaces(int1, int2)

        # Create VLANs on DUTs and assign ports to them

        DUT.vl.create_vlans(vlan1, vlan2, vlan3)
        DUT.vl.add_more_ports_to_more_vlans(vlan1, vlan2, vlan3, port1=int1, port12=int2)

        # Change the mode of STP to MSTP on all DUTs

        DUT.stp.change_stp_mode(mode=mode)

        # Disable STP on the link towards Cambium LAB

        if port_cambium_lab is not None:

            DUT.stp.stp_disable(port=port_cambium_lab)

        # Configure 2 MSTP Instances for all DUTs and assign VLANs to them

        DUT.stp.add_mst_instances_with_vlans(instance1, instance2, vlans_instance_1=[vlans_instance_1], vlans_instance_2=[vlans_instance_2])

        # Configure the same Region for all DUTs

        DUT.stp.add_mst_region(region=region)

    def remove_mst_configuration(self, DUT, int1, int2, vlan1, vlan2, vlan3, mode, port_cambium_lab=None):

        # Enabling stp on the port towards Cambium LAB

        if port_cambium_lab is not None:

            DUT.stp.stp_enable(port=port_cambium_lab)

        # Changing to default STP mode on DUT

        DUT.stp.change_stp_mode(mode=mode)

        # Removing the VLANs from DUT

        DUT.vl.remove_vlans(vlan1, vlan2, vlan3)

        # Shutting the ports on DUT

        DUT.int.shut_interfaces(int1, int2)

    def assert_mst_root_bridge(self, DUT, instance, d_instance, dict_of_ports_instance, priority):

        d_instance_zero, d_instance, dict_of_ports_instance = DUT.stp.show_spanning_tree_mst(instance=instance)

        print(d_instance)
        assert d_instance["Root ID Address"] == d_instance["Bridge ID Address"]
        assert d_instance["Root ID Priority"] == priority

        print("Successfully asserting")

    def assert_mst_root_bridges_3_DUTs(self, DUT1, d_instance_1, priority_1
                                , DUT2, d_instance_2, priority_2
                                , DUT3, d_instance_3, priority_3):

        print(d_instance_1)
        print(d_instance_2)
        print(d_instance_3)

        assert d_instance_1["Root ID Address"] == d_instance_2["Root ID Address"] == d_instance_3["Root ID Address"]
        assert d_instance_1["Bridge ID Priority"] == priority_1
        assert d_instance_2["Bridge ID Priority"] == priority_2
        assert d_instance_3["Bridge ID Priority"] == priority_3

        print("Successfully asserting")

    def assert_mst_root_bridges_2_DUTs(self, DUT1, d_instance_1, priority_1
                                , DUT2, d_instance_2, priority_2):

        print(d_instance_1)
        print(d_instance_2)

        assert d_instance_1["Root ID Address"] == d_instance_2["Root ID Address"]
        assert d_instance_1["Root ID Priority"] == priority_1 and d_instance_2[
            "Root ID Priority"] == priority_2

        print("Successfully asserting")

    def assert_mst_port(self, DUT, dict_of_ports_instance, port, role, port_priority=None, cost=None):

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

    def assert_mst_ports_3_DUTs(self, DUT1, dict_of_ports_instance_1, port1_1, port2_1, role1_1, role2_1, port_priority1_1, cost1_1, port_priority2_1, cost2_1,
                         DUT2, dict_of_ports_instance_2, port1_2, port2_2, role1_2, role2_2, port_priority1_2, cost1_2, port_priority2_2, cost2_2,
                         DUT3, dict_of_ports_instance_3, port1_3, port2_3, role1_3, role2_3, port_priority1_3, cost1_3, port_priority2_3, cost2_3):

        # Asserting for DUT1 for both ports

        self.assert_mst_port(DUT1, dict_of_ports_instance_1, port1_1, role1_1, port_priority1_1, cost1_1)
        self.assert_mst_port(DUT1, dict_of_ports_instance_1, port2_1, role2_1, port_priority2_1, cost2_1)

        # Asserting for DUT2 for both ports

        self.assert_mst_port(DUT2, dict_of_ports_instance_2, port1_2, role1_2, port_priority1_2, cost1_2)
        self.assert_mst_port(DUT2, dict_of_ports_instance_2, port2_2, role2_2, port_priority2_2, cost2_2)

        # Asserting for DUT3 for both ports

        self.assert_mst_port(DUT3, dict_of_ports_instance_3, port1_3, role1_3, port_priority1_3, cost1_3)
        self.assert_mst_port(DUT3, dict_of_ports_instance_3, port2_3, role2_3, port_priority2_3, cost2_3)

    def assert_mst_ports_2_DUTs(self, DUT1, dict_of_ports_instance_1, port1_1, port2_1, role1_1, role2_1, port_priority1_1, cost1_1, port_priority2_1, cost2_1,
                         DUT2, dict_of_ports_instance_2, port1_2, port2_2, role1_2, role2_2, port_priority1_2, cost1_2, port_priority2_2, cost2_2):

        # Asserting for DUT1 for both ports

        self.assert_mst_port(DUT1, dict_of_ports_instance_1, port1_1, role1_1, port_priority1_1, cost1_1)
        self.assert_mst_port(DUT1, dict_of_ports_instance_1, port2_1, role2_1, port_priority2_1, cost2_1)

        # Asserting for DUT2 for both ports

        self.assert_mst_port(DUT2, dict_of_ports_instance_2, port1_2, role1_2, port_priority1_2, cost1_2)
        self.assert_mst_port(DUT2, dict_of_ports_instance_2, port2_2, role2_2, port_priority2_2, cost2_2)




