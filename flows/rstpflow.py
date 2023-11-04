from Management import dut_objects


class RSTPFlow:

    def assert_root_bridge(self, d_root_id, d_bridge_id):

        if d_root_id["Root MAC-Address"] == d_bridge_id["Bridge MAC-Address"]:

            print(f"The Bridge MAC-Address {d_bridge_id['Bridge MAC-Address']} is the root")
            assert d_root_id["Root MAC-Address"] == d_bridge_id["Bridge MAC-Address"]

        else:

            assert d_root_id["Root MAC-Address"] != d_bridge_id["Bridge MAC-Address"]
            print(f"The Bridge MAC-Address {d_bridge_id['Bridge MAC-Address']} is not the root")

        print("Successfully asserting")

    def assert_root_bridge_priority(self, d_bridge_id, bridge_priority):

        assert d_bridge_id["Bridge Priority"] == bridge_priority
        # print(f"The bridge priority was configured on the DUT {d_bridge_id['Bridge MAC-Address']}")

        print("Successfully asserting")

    def assert_rstp_ports(self, dict_of_ports, port, role, cost=None, port_priority=None):

        port = port.replace(" ","")

        if dict_of_ports[port] == port:
            assert dict_of_ports[port]["Role"] == role

            if cost is not None:
                assert dict_of_ports[port]["Cost"] == cost

                if port_priority is not None:
                    assert dict_of_ports[port]["Prio"] == port_priority

        print("Successfully asserting")

    def confirm_rstp_root_bridge_bridge_priority_and_ports(self, d_root_id, d_bridge_id, bridge_priority, dict_of_ports, port, role, cost=None, port_priority=None):

        self.assert_root_bridge(d_root_id, d_bridge_id)
        self.assert_root_bridge_priority(d_bridge_id, bridge_priority)
        self.assert_rstp_ports(dict_of_ports, port, role, cost, port_priority)



