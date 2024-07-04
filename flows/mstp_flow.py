from Management import dut_objects
from config import vlan


class MSTPFlow:

    def create_mstp_configuration(self, DUT, interfaces, vlans, instances, mode, region, port_cambium_lab=None):

        # No shutting the interfaces

        for port in interfaces:
            DUT.int.no_shut_interface(interface=port)

        # Create VLANs on DUTs and assign ports to them

        for vlan in vlans:

            DUT.vl.create_vlan(vlan=vlan)

            for port in interfaces:
                DUT.vl.add_ports_to_vlan(vlan=vlan, ports=port)

        # Change the mode of STP to MSTP on all DUTs

        DUT.stp.change_stp_mode(mode=mode)

        # Disable STP on the link towards Cambium LAB

        if port_cambium_lab is not None:
            DUT.stp.stp_disable(port=port_cambium_lab)

        # Create instances and add VLANs

        for instance in instances:
            for vlan in vlans:
                DUT.stp.add_mst_instance_with_vlan(instance=instance, vlan=vlan)

        # Configure the same Region for all DUTs

        DUT.stp.add_mst_region(region=region)
    def remove_mstp_configuration(self, DUT, interfaces, vlans, mode, port_cambium_lab=None):

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


    def show_mstp_spanning_tree(self, DUT, instance):

        d_instance_zero, d_instance, dict_of_ports_instance = DUT.stp.show_spanning_tree_mst(
            instance=instance)

        return d_instance_zero, d_instance, dict_of_ports_instance

    def assert_mstp_bridge_and_root_id(self, DUT, instance, bridge_id, bridge_id_priority, root_id, root_priority, d_instance=None):

        # Asserting the Root Bridge and Bridge ID

        d_instance_zero, d_instance, dict_of_ports_instance = DUT.stp.show_spanning_tree_mst(instance=instance)

        print(d_instance)

        assert d_instance["Bridge ID Address"] == bridge_id
        assert d_instance["Bridge ID Priority"] == bridge_id_priority
        assert d_instance["Root ID Address"] == root_id
        assert d_instance["Root ID Priority"] == root_priority

        print(f"######## Successfully asserting the MSTP Root Bridge with instance priority {root_priority} and Bridge ID of DUT {DUT.hostname} in instance {instance} ")


    def assert_mstp_root_bridge(self, DUT, instance, priority):

        d_instance_zero, d_instance, dict_of_ports_instance = DUT.stp.show_spanning_tree_mst(instance=instance)

        print(d_instance)
        assert d_instance["Root ID Address"] == d_instance["Bridge ID Address"]
        assert d_instance["Root ID Priority"] == priority

        print("Successfully asserting")


    def assert_mstp_port(self, DUT, dict_of_ports_instance, port, role, port_priority=None, cost=None):

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


    def assert_mstp_ports(self, DUT, port1_dut, role1_dut, port_priority1_dut, cost1_dut,
                                     port2_dut, role2_dut, port_priority2_dut, cost2_dut, instance):

        # Asserting the Root Bridge

        d_instance_zero_dut, d_instance_dut, dict_of_ports_instance_dut = self.show_mstp_spanning_tree(
            DUT, instance=instance)

        # print(d_instance_dut)
        # print(dict_of_ports_instance_dut)

        # Asserting for DUT for both ports

        self.assert_mstp_port(DUT, dict_of_ports_instance_dut, port1_dut, role1_dut, port_priority1_dut,
                               cost1_dut)
        self.assert_mstp_port(DUT, dict_of_ports_instance_dut, port2_dut, role2_dut, port_priority2_dut,
                               cost2_dut)

        print(f"######## Successfully asserting the MSTP Ports of DUT {DUT.hostname} in instance {instance}")



