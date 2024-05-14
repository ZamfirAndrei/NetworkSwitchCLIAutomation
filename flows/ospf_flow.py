
class OSPFflow:


    def create_and_add_port_to_vlan(self, DUT, port, vlan):

        # Opening the port

        DUT.int.no_shut_interfaces(port)

        # Creating the VLAN on a DUT

        DUT.vl.create_vlan(vlan=vlan)

        # Adding the ports to the VLAN

        DUT.vl.add_ports_to_vlan(ports=port, vlan=vlan)

    def create_interfaces_vlan(self, DUT, vlan, ip, mask):

        # Create IP interfaces on DUT for the specific VLANs

        DUT.ip.add_ip_interfaces(vlan, int_vlan=[ip, mask])
        DUT.ip.no_shut_int_vlans(vlan)

    def create_ip_interface_vlan_no_shut_port_and_add_ports_to_the_vlan(self,  DUT, port, vlan, ip, mask):

        # Create IP interfaces on DUT for the specific VLANs

        DUT.ip.add_ip_interface(int_vlan=vlan, ip=ip, mask=mask)
        DUT.ip.no_shut_int_vlan(int_vlan=vlan)

        # Opening the port

        DUT.int.no_shut_interface(interface=port)

        # Adding the ports to the VLAN

        DUT.vl.add_ports_to_vlan(ports=port, vlan=vlan)

    def create_routed_port_and_add_ip(self, DUT, interface, ip, mask):

        # Creating routed port

        DUT.int.add_routed_port(interface=interface)

        # Opening the port

        DUT.int.no_shut_interface(interface=interface)

        # Create IP Routed Port

        DUT.ip.add_ip_routed_port(interface=interface, ip=ip, mask=mask)

    def remove_routed_port(self, DUT, *args):

        # Removing routed port

        for int in args:

            DUT.int.remove_routed_port(interface=int)


    def enable_and_advertise_networks(self, DUT, **kargs):

        # Enable OSPF on all DUTs and advertise the Network IPs

        DUT.ospf.enable_ospf()

        for item in kargs.values():

            DUT.ospf.advertise_network(ip_network=item[0],area=item[1])

    def confirm_network_details_in_the_routing_table(self, DUT, network, protocol=None, AD=None, metric=None, metric_type=None):

        # Check if the routes are learned and installed in OSPF routes

        ip_route, networks, networks_connected, dict_of_networks = DUT.ip.show_ip_route()
        print(f"The routing table of DUT {DUT.hostname} with the ip address {DUT.ip_session}")
        print(dict_of_networks)

        assert network in dict_of_networks.keys()

        if protocol is not None:

            if metric_type is not None:

                # print("----- 1 ------")
                # print(protocol + metric_type)
                assert dict_of_networks[network]["Protocol"] == protocol + metric_type

            else:

                # print("----- 2 ------")
                # print(protocol)
                assert dict_of_networks[network]["Protocol"] == protocol


        if AD is not None:

            assert dict_of_networks[network]["AD"] == AD

        if metric is not None:

            assert dict_of_networks[network]["Metric"] == metric


    def confirm_network_in_the_routing_table(self, DUT, network):

        # Check if the routes are learned and installed in OSPF routes

        ip_route, networks, networks_connected, dict_of_networks = DUT.ip.show_ip_route()
        print(f"The routing table of DUT {DUT.hostname} with the ip address {DUT.ip_session}")
        print(dict_of_networks)

        assert network in dict_of_networks.keys()

    def confirm_network_not_in_the_routing_table(self, DUT, network):

        # Check if the routes are learned and installed in OSPF routes

        ip_route, networks, networks_connected, dict_of_networks = DUT.ip.show_ip_route()
        print(f"The routing table of DUT {DUT.hostname} with the ip address {DUT.ip_session}")
        print(dict_of_networks)

        assert network not in dict_of_networks.keys()

    def disable_OSPF(self, DUT):

        DUT.ospf.disable_ospf()

    def remove_networks(self, DUT, **kwargs):

        # Remove the Network IPs from OSPF

        for item in kwargs.values():

            DUT.ospf.remove_network(ip_network=item[0], area=item[1])


    def remove_vlans_and_interfaces_vlan(self, DUT, *args):

        for vlan in args:

            DUT.ip.remove_vlan_interfaces(vlan)

            DUT.vl.remove_vlans(vlan)

    def shut_interfaces(self, DUT, *args):

        for interface in args:

            DUT.int.shut_interfaces(interface)