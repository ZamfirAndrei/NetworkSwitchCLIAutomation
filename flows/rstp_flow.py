from Management import dut_objects


class RSTPFlow:

    def assert_root_bridge(self, d_root_id, d_bridge_id):

        if d_root_id["Root MAC-Address"] == d_bridge_id["Bridge MAC-Address"]:

            print(f"The Bridge MAC-Address {d_bridge_id['Bridge MAC-Address']} is the root")
            assert d_root_id["Root MAC-Address"] == d_bridge_id["Bridge MAC-Address"]

        else:

            assert d_root_id["Root MAC-Address"] != d_bridge_id["Bridge MAC-Address"]
            print(f"The Bridge MAC-Address {d_bridge_id['Bridge MAC-Address']} is not the root")

        print("Successfully asserting the Root Bridge")

    def assert_root_bridge_priority(self, d_bridge_id, bridge_priority):

        assert d_bridge_id["Bridge Priority"] == bridge_priority
        # print(f"The bridge priority was configured on the DUT {d_bridge_id['Bridge MAC-Address']}")

        print("Successfully asserting the Bridge Priority")

    def assert_root(self, DUT, d_root_id, d_bridge_id, bridge_priority):

        assert d_root_id["Root MAC-Address"] == d_bridge_id["Bridge MAC-Address"]
        assert d_bridge_id["Bridge Priority"] == bridge_priority
        # print(f"The bridge priority was configured on the DUT {d_bridge_id['Bridge MAC-Address']}")

        print(d_root_id, d_bridge_id)
        print("Successfully asserting the Root Bridge")

    def assert_root_3_DUTs(self, DUT1, d_root_id_1, d_bridge_id_1, bridge_priority_1,
                                 DUT2, d_root_id_2, d_bridge_id_2, bridge_priority_2,
                                 DUT3, d_root_id_3, d_bridge_id_3, bridge_priority_3):

        print(d_root_id_1, d_bridge_id_1)
        print(d_root_id_2, d_bridge_id_2)
        print(d_root_id_3, d_bridge_id_3)

        assert d_root_id_1["Root MAC-Address"] == d_root_id_2["Root MAC-Address"] == d_root_id_3["Root MAC-Address"]
        assert d_bridge_id_1["Bridge Priority"] == bridge_priority_1
        assert d_bridge_id_2["Bridge Priority"] == bridge_priority_2
        assert d_bridge_id_3["Bridge Priority"] == bridge_priority_3

        print("Successfully asserting the Root Bridges for 3 DUTs")

    def assert_root_2_DUTs(self, DUT1, d_root_id_1, d_bridge_id_1, bridge_priority_1,
                                 DUT2, d_root_id_2, d_bridge_id_2, bridge_priority_2):

        print(d_root_id_1, d_bridge_id_1)
        print(d_root_id_2, d_bridge_id_2)

        assert d_root_id_1["Root MAC-Address"] == d_root_id_2["Root MAC-Address"]
        assert d_bridge_id_1["Bridge Priority"] == bridge_priority_1
        assert d_bridge_id_2["Bridge Priority"] == bridge_priority_2

        print("Successfully asserting the Root Bridges for 2 DUTs")

    def assert_rstp_ports(self, DUT, dict_of_ports, port, role, cost=None, port_priority=None):

        port = port.replace(" ","")
        print(port)
        print(dict_of_ports[port])

        if dict_of_ports[port]["Name"] == port:
            assert dict_of_ports[port]["Role"] == role

            if cost is not None:
                assert dict_of_ports[port]["Cost"] == cost

            if port_priority is not None:
                assert dict_of_ports[port]["Prio"] == port_priority

        print(f"Successfully asserting the Port {port}")

    def assert_rstp_ports_3_DUTs(self, DUT1, dict_of_ports_1, port1_1, port2_1, role1_1, role2_1, port_priority1_1, cost1_1, port_priority2_1, cost2_1,
                                       DUT2, dict_of_ports_2, port1_2, port2_2, role1_2, role2_2,  port_priority1_2, cost1_2, port_priority2_2, cost2_2,
                                       DUT3, dict_of_ports_3, port1_3, port2_3, role1_3, role2_3, port_priority1_3, cost1_3, port_priority2_3, cost2_3):

        # Asserting the port1 and port2 of DUT1

        self.assert_rstp_ports(DUT1, dict_of_ports_1, port1_1, role1_1, cost1_1, port_priority1_1)
        self.assert_rstp_ports(DUT1, dict_of_ports_1, port2_1, role2_1, cost2_1, port_priority2_1)

        # Asserting the port1 and port2 of DUT2

        self.assert_rstp_ports(DUT2, dict_of_ports_2, port1_2, role1_2, cost1_2, port_priority1_2)
        self.assert_rstp_ports(DUT2, dict_of_ports_2, port2_2, role2_2, cost2_2, port_priority2_2)

        # Asserting the port1 and port2 of DUT3

        self.assert_rstp_ports(DUT3, dict_of_ports_3, port1_3, role1_3, cost1_3, port_priority1_3)
        self.assert_rstp_ports(DUT3, dict_of_ports_3, port2_3, role2_3, cost2_3, port_priority2_3)


    def assert_rstp_ports_2_DUTs(self, DUT1, dict_of_ports_1, port1_1, port2_1, role1_1, role2_1, port_priority1_1, cost1_1, port_priority2_1, cost2_1,
                                       DUT2, dict_of_ports_2, port1_2, port2_2, role1_2, role2_2,  port_priority1_2, cost1_2, port_priority2_2, cost2_2):

        # Asserting the port1 and port2 of DUT1

        self.assert_rstp_ports(DUT1, dict_of_ports_1, port1_1, role1_1, cost1_1, port_priority1_1)
        self.assert_rstp_ports(DUT1, dict_of_ports_1, port2_1, role2_1, cost2_1, port_priority2_1)

        # Asserting the port1 and port2 of DUT2

        self.assert_rstp_ports(DUT2, dict_of_ports_2, port1_2, role1_2, cost1_2, port_priority1_2)
        self.assert_rstp_ports(DUT2, dict_of_ports_2, port2_2, role2_2, cost2_2, port_priority2_2)


    def create_rstp_configuration(self, DUT, int1, int2, vlan1, vlan2, vlan3, mode, port_cambium_lab=None):

        # No shutting the interfaces from DUT

        DUT.int.no_shut_interfaces(int1, int2)

        # Create VLANs on DUT and assign ports to them

        DUT.vl.create_vlans(vlan1, vlan2, vlan3)
        DUT.vl.add_more_ports_to_more_vlans(vlan1, vlan2, vlan3, port1=int1, port12=int2)

        # Change the mode of STP to RSTP

        DUT.stp.change_stp_mode(mode=mode)

        # Disable STP on the link towards Cambium LAB

        if port_cambium_lab is not None:
            DUT.stp.stp_disable(port=port_cambium_lab)

    def remove_rstp_configuration(self, DUT, int1, int2, vlan1, vlan2, vlan3, port_cambium_lab=None):

        # Enable STP on the link towards Cambium LAB

        if port_cambium_lab is not None:
            DUT.stp.stp_enable(port=port_cambium_lab)

        # Remove VLANs from DUT

        DUT.vl.remove_vlans(vlan1, vlan2, vlan3)

        # Shut interfaces from DUT

        DUT.int.shut_interfaces(int1, int2)

    def create_rstp_configuration_1_LINK_2_DUTs(self, DUT, int1, vlan1, vlan2, vlan3, mode, port_cambium_lab=None):

        # No shutting the interface from DUT

        DUT.int.no_shut_interfaces(int1)

        # Create VLANs on DUT and assign ports to them

        DUT.vl.create_vlans(vlan1, vlan2, vlan3)
        DUT.vl.add_more_ports_to_more_vlans(vlan1, vlan2, vlan3, port1=int1)

        # Change the mode of STP to RSTP

        DUT.stp.change_stp_mode(mode=mode)

        # Disable STP on the link towards Cambium LAB

        if port_cambium_lab is not None:
            DUT.stp.stp_disable(port=port_cambium_lab)

    def remove_rstp_configuration_1_LINK_2_DUTs(self, DUT, int1, vlan1, vlan2, vlan3, port_cambium_lab=None):

        # Enable STP on the link towards Cambium LAB

        if port_cambium_lab is not None:
            DUT.stp.stp_enable(port=port_cambium_lab)

        # Remove VLANs from DUT

        DUT.vl.remove_vlans(vlan1, vlan2, vlan3)

        # Shut interfaces from DUT

        DUT.int.shut_interfaces(int1)

    def assert_rstp_ports_1_LINK_2_DUTs(self, DUT1, dict_of_ports_1, port1_1, role1_1, port_priority1_1, cost1_1,
                                              DUT2, dict_of_ports_2, port1_2, role1_2,  port_priority1_2, cost1_2):

        # Asserting the port1 of DUT1

        self.assert_rstp_ports(DUT1, dict_of_ports_1, port1_1, role1_1, cost1_1, port_priority1_1)

        # Asserting the port1 of DUT2

        self.assert_rstp_ports(DUT2, dict_of_ports_2, port1_2, role1_2, cost1_2, port_priority1_2)



