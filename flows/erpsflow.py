import time
import pytest
import pytest_html
import sys


from config import vlan, interfaces, erps, fdb, stp
from Management import ssh

class ERPSFlow:

    def create_erps_configuration_for_non_rpl_owner(self, vl, vlanid, int, int1, int2, erps, group_id, protection_type, local_mep1, remote_mep1, local_mep2, remote_mep2):
        # < VLAN configuration >

        # Creating ERPS dedicated traffic VLAN
        vl.create_vlan(vlanid)

        # Adding the ports to the ERPS dedicated traffic VLAN
        vl.add_ports_to_vlan(int1, vlan=vlanid)
        vl.add_ports_to_vlan(int2, vlan=vlanid)

        # < Interfaces configuration >

        # No shutting the ports for the ERPS dedicated traffic VLAN
        int.no_shut_interfaces(int1, int2)

        # < ERPS configuration >

        # ERPS configuration for DUT 1, which will be the RPL Owner
        erps.enable_erps_mode()
        erps.create_erps_group(group_id)
        erps.configure_erps_protection_type(group_id, protection_type)
        erps.configure_erps_mapped_ports(group_id, int1, int2, vlanid, local_mep1, remote_mep1, local_mep2, remote_mep2)
        erps.activate_erps_group(group_id)

        print("ERPS configuration for Non RPL Owner has been done successfully")


    def create_erps_configuration_for_rpl_owner(self, vl, vlanid, int, int1, int2, erps, group_id, protection_type, local_mep1, remote_mep1, local_mep2, remote_mep2, configured_rpl_port):
        # < VLAN configuration >

        # Creating ERPS dedicated traffic VLAN
        vl.create_vlan(vlanid)

        # Adding the ports to the ERPS dedicated traffic VLAN
        vl.add_ports_to_vlan(int1, vlan=vlanid)
        vl.add_ports_to_vlan(int2, vlan=vlanid)

        # < Interfaces configuration >

        # No shutting the ports for the ERPS dedicated traffic VLAN
        int.no_shut_interfaces(int1, int2)

        # < ERPS configuration >

        # ERPS configuration for DUT 1, which will be the RPL Owner
        erps.enable_erps_mode()
        erps.create_erps_group(group_id)
        erps.configure_erps_protection_type(group_id, protection_type)
        erps.configure_erps_mapped_ports(group_id, int1, int2, vlanid, local_mep1, remote_mep1, local_mep2, remote_mep2)
        erps.configure_erps_protected_port(group_id, configured_rpl_port)
        erps.activate_erps_group(group_id)

        print("ERPS configuration for RPL Owner has been done successfully")

    def assert_ring_information(self, d_ring_info):

        print(d_ring_info)
        assert d_ring_info['Ring Name'] == "Ring1"
        assert d_ring_info['RAPS Vlan Id'] == "3500"
        assert d_ring_info['Operating Mode'] == "Revertive"
        assert d_ring_info['ERPS Compatible Version'] == "Version1"
        assert d_ring_info['Ring State'] == "Idle"
        assert d_ring_info['Status'] == "Active"

        print("Successfully asserting")

    def assert_ports_status(self, d_ports):
        print(d_ports)
        assert d_ports['Port 1']['MEP Status'] == "Ok"
        assert d_ports['Port 2']['MEP Status'] == "Ok"

        print("Successfully asserting")

    def assert_rpl_port(self, configured_rpl_port, rpl_port):
        print(rpl_port)
        if rpl_port != "There is no RPL Port":
            # Re-Modeling the Configured RPL Port from "gi 0/X" to be "Gi0/X"
            list_rpl_port = []
            list_rpl_port.append(configured_rpl_port[0].upper())
            for i in range(1, len(configured_rpl_port)):
                if configured_rpl_port[i] != ' ':
                    list_rpl_port.append(configured_rpl_port[i])
            final_configured_rpl_port_1 = ''.join(list_rpl_port)

            assert rpl_port == final_configured_rpl_port_1

        else:
            assert rpl_port == "There is no RPL Port"

        print("Successfully asserting")

    def assert_ports(self, rpl_port, list_ports):

        print(list_ports)
        for port in list_ports:
            if port['Ring Port'] == rpl_port:
                assert port['Link Status'] == 'Not Failed'
                assert port['Port Status'] == 'Blocked'
            else:
                assert port['Link Status'] == 'Not Failed'
                assert port['Port Status'] == 'UnBlocked'

        print("Successfully asserting")

    def removing_the_configuration(self, int, int1, int2, erps, stp, vl, vlanid):

        int.shut_interfaces(int1, int2)
        erps.disable_erps_mode()
        stp.stp_enable(port=int1)
        stp.stp_enable(port=int2)
        vl.remove_vlan(vlanid)

