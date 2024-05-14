import re
import time
import pytest
import pytest_html
import sys


from config import vlan, interfaces, erps, fdb, stp
from Management import ssh, dut_objects
from mocks import mock_erps
from flows import rstp_flow

rstpflow = rstpflow.RSTPFlow()

class ERPSFlow:

    def create_erps_configuration_for_non_rpl_owner(self, DUT, mock_erps_DUT):
        # < VLAN configuration >

        # Creating ERPS dedicated traffic VLAN
        DUT.vl.create_vlan(mock_erps_DUT['vlanid'])

        # Adding the ports to the ERPS dedicated traffic VLAN
        DUT.vl.add_ports_to_vlan(mock_erps_DUT['int1'], vlan=mock_erps_DUT['vlanid'])
        DUT.vl.add_ports_to_vlan(mock_erps_DUT['int2'], vlan=mock_erps_DUT['vlanid'])

        # < Interfaces configuration >

        # No shutting the ports for the ERPS dedicated traffic VLAN
        DUT.int.no_shut_interfaces(mock_erps_DUT['int1'], mock_erps_DUT['int2'])

        # < ERPS configuration >

        # ERPS configuration for DUT 1, which will be the RPL Owner
        DUT.erps.enable_erps_mode()
        DUT.erps.create_erps_group(mock_erps_DUT['group_id'])
        DUT.erps.configure_erps_protection_type(mock_erps_DUT['group_id'], mock_erps_DUT['protection_type'])
        DUT.erps.configure_erps_mapped_ports(mock_erps_DUT['group_id'], mock_erps_DUT['int1'], mock_erps_DUT['int2'], mock_erps_DUT['vlanid'], mock_erps_DUT['local_mep1'], mock_erps_DUT['remote_mep1'], mock_erps_DUT['local_mep2'], mock_erps_DUT['remote_mep2'])
        DUT.erps.activate_erps_group(mock_erps_DUT['group_id'])

        print("ERPS configuration for Non RPL Owner has been done successfully")


    def create_erps_configuration_for_rpl_owner(self, DUT, mock_erps_DUT):
        # < VLAN configuration >

        # Creating ERPS dedicated traffic VLAN
        # vl.create_vlan(vlanid)
        DUT.vl.create_vlan(mock_erps_DUT['vlanid'])

        # Adding the ports to the ERPS dedicated traffic VLAN
        DUT.vl.add_ports_to_vlan(mock_erps_DUT['int1'], vlan=mock_erps_DUT['vlanid'])
        DUT.vl.add_ports_to_vlan(mock_erps_DUT['int2'], vlan=mock_erps_DUT['vlanid'])

        # < Interfaces configuration >

        # No shutting the ports for the ERPS dedicated traffic VLAN
        DUT.int.no_shut_interfaces(mock_erps_DUT['int1'], mock_erps_DUT['int2'])

        # < ERPS configuration >

        # ERPS configuration for DUT 1, which will be the RPL Owner
        DUT.erps.enable_erps_mode()
        DUT.erps.create_erps_group(mock_erps_DUT['group_id'])
        DUT.erps.configure_erps_protection_type(mock_erps_DUT['group_id'], mock_erps_DUT['protection_type'])
        DUT.erps.configure_erps_mapped_ports(mock_erps_DUT['group_id'], mock_erps_DUT['int1'], mock_erps_DUT['int2'], mock_erps_DUT['vlanid'], mock_erps_DUT['local_mep1'], mock_erps_DUT['remote_mep1'], mock_erps_DUT['local_mep2'], mock_erps_DUT['remote_mep2'])
        DUT.erps.configure_erps_protected_port(mock_erps_DUT['group_id'], mock_erps_DUT['configured_rpl_port'])
        DUT.erps.activate_erps_group(mock_erps_DUT['group_id'])

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

    def assert_ring_information_after_shutting_down_a_ring_port(self, d_ring_info_after_shut):

        print(d_ring_info_after_shut)
        assert d_ring_info_after_shut['Ring Name'] == "Ring1"
        assert d_ring_info_after_shut['RAPS Vlan Id'] == "3500"
        assert d_ring_info_after_shut['Operating Mode'] == "Revertive"
        assert d_ring_info_after_shut['ERPS Compatible Version'] == "Version1"
        assert d_ring_info_after_shut['Ring State'] == "Protection"
        assert d_ring_info_after_shut['Status'] == "Active"

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
            assert rpl_port == configured_rpl_port

        print("Successfully asserting")

    def assert_rpl_port_after_shutting_down_a_ring_port(self, configured_rpl_port, rpl_port_after_shut):

        print(rpl_port_after_shut)
        if rpl_port_after_shut != "There is no RPL Port":
            # Re-Modeling the Configured RPL Port from "gi 0/X" to be "Gi0/X"
            list_rpl_port_after_shut = []
            list_rpl_port_after_shut.append(configured_rpl_port[0].upper())
            for i in range(1, len(configured_rpl_port)):
                if configured_rpl_port[i] != ' ':
                    list_rpl_port_after_shut.append(configured_rpl_port[i])
            final_configured_rpl_port_1_after_shut = ''.join(list_rpl_port_after_shut)
            assert rpl_port_after_shut == final_configured_rpl_port_1_after_shut

        else:
            assert rpl_port_after_shut == configured_rpl_port

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

    def assert_ports_after_shutting_down_a_ring_port(self, rpl_port_after_shut, list_ports_after_shut, int_to_shutdown_noshutdown, d_ports_after_shut, is_rpl_owner):

        print(list_ports_after_shut)
        for port in list_ports_after_shut:
            if port['Ring Port'] == rpl_port_after_shut:
                assert port['Link Status'] == 'Not Failed'
                assert port['Port Status'] == 'UnBlocked'
            elif port['Ring Port'] == int_to_shutdown_noshutdown and (d_ports_after_shut['Port 1']['MEP Status'] == "Failed" or d_ports_after_shut['Port 2']['MEP Status'] == "Failed"):
                assert port['Link Status'] == 'Failed'
                assert port['Port Status'] == 'Blocked'
            else:
                if d_ports_after_shut['Port 1']['MEP Status'] == "Ok" and d_ports_after_shut['Port 2']['MEP Status'] == "Ok":
                    assert port['Link Status'] == 'Remote Failure'
                    assert port['Port Status'] == 'UnBlocked'
                elif is_rpl_owner:
                    assert port['Link Status'] == 'Failed'
                    assert port['Port Status'] == 'Blocked'
                else:
                    assert port['Link Status'] == 'Not Failed'
                    assert port['Port Status'] == 'UnBlocked'

        print("Successfully asserting")


    def assert_erps_ports_after_attempting_to_enable_stp(self, DUT, port1, port2):

        DUT.session.connect()
        DUT.session.send_cmd("conf t ")
        DUT.session.send_cmd(f"int {port1}")
        DUT.session.send_cmd(f"spanning-tree enable")
        DUT.session.send_cmd(f"int {port2}")
        DUT.session.send_cmd(f"spanning-tree enable")
        output = DUT.session.read()
        ports_match = re.findall(r"% Port is configured as part of a ERPS ring", output)
        DUT.session.close()

        print(ports_match)

        assert ports_match[0] == "% Port is configured as part of a ERPS ring"
        assert ports_match[1] == "% Port is configured as part of a ERPS ring"


    def assert_rstp_ports_for_erps_ports(self, DUT, port1, port2, role1, role2):

        d_root_id, d_bridge_id, ports, dict_of_ports = DUT.stp.show_spanning_tree_rstp()
        rstpflow.assert_rstp_ports(DUT, dict_of_ports, port1, role1)
        rstpflow.assert_rstp_ports(DUT, dict_of_ports, port2, role2)


    def removing_the_erps_configuration(self, DUT, int1, int2, vlanid):

        DUT.int.shut_interfaces(int1, int2)
        DUT.erps.disable_erps_mode()
        DUT.stp.stp_enable(port=int1)
        DUT.stp.stp_enable(port=int2)
        DUT.vl.remove_vlan(vlanid)

    def confirm_erps_configuration(self, DUT, group_id, configured_rpl_port):

        d_ring_info_DUT = DUT.erps.check_erps_ring_id_information(group_id)
        self.assert_ring_information(d_ring_info_DUT)

        d_ports_DUT = DUT.erps.check_erps_ports_status(group_id)
        self.assert_ports_status(d_ports_DUT)

        rpl_port_DUT = DUT.erps.check_rpl_port(group_id)
        self.assert_rpl_port(configured_rpl_port, rpl_port_DUT)

        list_ports_DUT = DUT.erps.check_erps_ports(group_id)
        self.assert_ports(rpl_port_DUT, list_ports_DUT)

        is_rpl_owner_DUT = DUT.erps.check_rpl_owner(group_id)
        print(is_rpl_owner_DUT)

        if configured_rpl_port != "There is no RPL Port":
            assert is_rpl_owner_DUT == True
        else:
            assert is_rpl_owner_DUT == False

    def confirm_erps_configuration_for_3DUTs_after_one_interface_is_shutdown(self, DUT1, DUT2, DUT3, final_int_to_shutdown_noshutdown, group_id,
                                                                             configured_rpl_port_DUT1, configured_rpl_port_DUT2,
                                                                             configured_rpl_port_DUT3):

        # ----- Asserting for DUT1 -----

        is_rpl_owner_DUT1 = DUT1.erps.check_rpl_owner(group_id)

        d_ring_info_DUT1_after_shut = DUT1.erps.check_erps_ring_id_information(group_id)
        self.assert_ring_information_after_shutting_down_a_ring_port(d_ring_info_DUT1_after_shut)

        d_ports_DUT1_after_shut = DUT1.erps.check_erps_ports_status(group_id)
        print(d_ports_DUT1_after_shut)
        assert d_ports_DUT1_after_shut['Port 1']['MEP Status'] == "Failed"
        assert d_ports_DUT1_after_shut['Port 2']['MEP Status'] == "Ok"

        rpl_port_DUT1_after_shut = DUT1.erps.check_rpl_port(group_id)
        self.assert_rpl_port_after_shutting_down_a_ring_port(configured_rpl_port_DUT1, rpl_port_DUT1_after_shut)

        list_ports_DUT1_after_shut = DUT1.erps.check_erps_ports(group_id)
        self.assert_ports_after_shutting_down_a_ring_port(rpl_port_DUT1_after_shut, list_ports_DUT1_after_shut, final_int_to_shutdown_noshutdown, d_ports_DUT1_after_shut, is_rpl_owner_DUT1)

        # ----- Asserting for DUT2 -----

        is_rpl_owner_DUT2 = DUT2.erps.check_rpl_owner(group_id)

        d_ring_info_DUT2_after_shut = DUT2.erps.check_erps_ring_id_information(group_id)
        self.assert_ring_information_after_shutting_down_a_ring_port(d_ring_info_DUT2_after_shut)

        d_ports_DUT2_after_shut = DUT2.erps.check_erps_ports_status(group_id)
        print(d_ports_DUT2_after_shut)
        assert d_ports_DUT2_after_shut['Port 1']['MEP Status'] == "Ok"
        assert d_ports_DUT2_after_shut['Port 2']['MEP Status'] == "Failed"

        rpl_port_DUT2_after_shut = DUT2.erps.check_rpl_port(group_id)
        self.assert_rpl_port_after_shutting_down_a_ring_port(configured_rpl_port_DUT2, rpl_port_DUT2_after_shut)

        list_ports_DUT2_after_shut = DUT2.erps.check_erps_ports(group_id)
        self.assert_ports_after_shutting_down_a_ring_port(rpl_port_DUT2_after_shut, list_ports_DUT2_after_shut, final_int_to_shutdown_noshutdown, d_ports_DUT2_after_shut, is_rpl_owner_DUT2)

        # ----- Asserting for DUT3 -----

        is_rpl_owner_DUT3 = DUT3.erps.check_rpl_owner(group_id)

        d_ring_info_DUT3_after_shut = DUT3.erps.check_erps_ring_id_information(group_id)
        self.assert_ring_information_after_shutting_down_a_ring_port(d_ring_info_DUT3_after_shut)

        d_ports_DUT3_after_shut = DUT3.erps.check_erps_ports_status(group_id)
        print(d_ports_DUT3_after_shut)
        assert d_ports_DUT3_after_shut['Port 1']['MEP Status'] == "Ok"
        assert d_ports_DUT3_after_shut['Port 2']['MEP Status'] == "Ok"

        rpl_port_DUT3_after_shut = DUT3.erps.check_rpl_port(group_id)
        self.assert_rpl_port_after_shutting_down_a_ring_port(configured_rpl_port_DUT3, rpl_port_DUT3_after_shut)

        list_ports_DUT3_after_shut = DUT3.erps.check_erps_ports(group_id)
        self.assert_ports_after_shutting_down_a_ring_port(rpl_port_DUT3_after_shut, list_ports_DUT3_after_shut, final_int_to_shutdown_noshutdown, d_ports_DUT3_after_shut, is_rpl_owner_DUT3)

    def change_the_rpl_port_on_the_rpl_owner(self, erps, group_id, new_rpl_port):

        # De-activating the ERPS Group
        erps.deactivate_erps_group(group_id)

        # Removing and re-configuring the ERPS Protected Port
        erps.delete_erps_protected_port(group_id)
        erps.configure_erps_protected_port(group_id, new_rpl_port)

        # Activating the ERPS Group
        erps.activate_erps_group(group_id)

    def change_the_rpl_owner(self, erps1, erps2, group_id, new_rpl_port):

        # De-activating the ERPS Group
        erps1.deactivate_erps_group(group_id)

        # Removing the ERPS Protected Port of the actual RPL Owner
        erps1.delete_erps_protected_port(group_id)

        # De-activating the ERPS Group on another DUT and configuring ERPS Protected Port, making it the new RPL Owner
        erps2.deactivate_erps_group(group_id)
        erps2.configure_erps_protected_port(group_id, new_rpl_port)

        # Activating the ERPS Group on the new and old RPL Owner
        erps1.activate_erps_group(group_id)
        erps2.activate_erps_group(group_id)


