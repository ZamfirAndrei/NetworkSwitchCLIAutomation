from Management import dut_objects


class RSTPFlow:

    def create_rstp_configuration(self, DUT, interfaces, vlans, mode, port_cambium_lab=None):

        # No shutting the interfaces

        for port in interfaces:
            DUT.int.no_shut_interface(interface=port)

        # Create VLANs on DUTs and assign ports to them

        for vlan in vlans:

            DUT.vl.create_vlan(vlan=vlan)

            for port in interfaces:
                DUT.vl.add_ports_to_vlan(vlan=vlan, ports=port)

        # Change the mode of STP to RSTP on all DUTs

        DUT.stp.change_stp_mode(mode=mode)

        # Disable STP on the link towards Cambium LAB

        if port_cambium_lab is not None:
            DUT.stp.stp_disable(port=port_cambium_lab)

    def remove_rstp_configuration(self, DUT, interfaces, vlans, mode, port_cambium_lab=None):

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
    def show_rstp_spanning_tree(self, DUT):

        d_root_id, d_bridge_id, ports, dict_of_ports = DUT.stp.show_spanning_tree_rstp()

        return d_root_id, d_bridge_id, ports, dict_of_ports


    def assert_rstp_port(self, DUT, dict_of_ports, port, role,  port_priority=None, cost=None):

        port = port.replace(" ","")
        # print(port)
        # print(dict_of_ports[port])

        if dict_of_ports[port]["Name"] == port:
            assert dict_of_ports[port]["Role"] == role

            if cost is not None:
                assert dict_of_ports[port]["Cost"] == cost

            if port_priority is not None:
                assert dict_of_ports[port]["Prio"] == port_priority

            print(f"#### Successfully asserting for port {port} of DUT {DUT.hostname}")


    def assert_rstp_ports(self, DUT, port1_dut, role1_dut, port_priority1_dut, cost1_dut,
                                     port2_dut, role2_dut, port_priority2_dut, cost2_dut):

        # Asserting the Root Bridge

        d_root_id, d_bridge_id, ports, dict_of_ports = self.show_rstp_spanning_tree(DUT)

        # print(d_root_id)
        # print(dict_of_ports)

        # Asserting for DUT for both ports

        self.assert_rstp_port(DUT, dict_of_ports, port1_dut, role1_dut, port_priority1_dut, cost1_dut)
        self.assert_rstp_port(DUT, dict_of_ports, port2_dut, role2_dut, port_priority2_dut, cost2_dut)

        print(f"######## Successfully asserting the RSTP Ports of DUT {DUT.hostname}")

    def assert_rstp_bridge_and_root_id(self, DUT, bridge_id, bridge_id_priority, root_id, root_priority, d_instance_vlan=None):

        # Asserting the Root Bridge and Bridge ID

        d_root_id, d_bridge_id, ports, dict_of_ports = self.show_rstp_spanning_tree(DUT)

        # print(d_root_id)
        # print(d_bridge_id)

        assert d_bridge_id["Bridge MAC-Address"] == bridge_id
        assert d_bridge_id["Bridge Priority"] == bridge_id_priority
        assert d_root_id["Root MAC-Address"] == root_id
        assert d_root_id["Root Priority"] == root_priority

        print(f"######## Successfully asserting the RSTP Root Bridge with priority {root_priority} and Bridge ID of DUT {DUT.hostname}")



