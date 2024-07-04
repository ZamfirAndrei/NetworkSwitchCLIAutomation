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


    def assert_pvrst_root_bridge_and_ports(self, DUT, port1_dut, role1_dut, port_priority1_dut,
                               cost1_dut, port2_dut, role2_dut, port_priority2_dut, cost2_dut, vlan, bridge_id, bridge_id_priority, root_id, root_priority):

        # Asserting the Root Bridge

        d_instance_vlan_dut, dict_of_ports_instance_vlan_dut, list_ports_instance_dut = self.show_pvrst_spanning_tree(
            DUT, vlan=vlan)

        # print(d_instance_vlan_dut)
        # print(dict_of_ports_instance_vlan_dut)

        self.assert_pvrst_bridge_and_root_id(DUT, vlan=vlan,
                                             d_instance_vlan=d_instance_vlan_dut,
                                             bridge_id=bridge_id,
                                             bridge_id_priority=bridge_id_priority,
                                             root_id=root_id,
                                             root_priority=root_priority)

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