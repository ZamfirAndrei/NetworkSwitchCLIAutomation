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

    def removing_the_erps_configuration(self, int, int1, int2, erps, stp, vl, vlanid):

        int.shut_interfaces(int1, int2)
        erps.disable_erps_mode()
        stp.stp_enable(port=int1)
        stp.stp_enable(port=int2)
        vl.remove_vlan(vlanid)

    def confirm_erps_configuration(self, erps, group_id, configured_rpl_port):

        d_ring_info_DUT = erps.check_erps_ring_id_information(group_id)
        self.assert_ring_information(d_ring_info_DUT)

        d_ports_DUT = erps.check_erps_ports_status(group_id)
        self.assert_ports_status(d_ports_DUT)

        rpl_port_DUT = erps.check_rpl_port(group_id)
        self.assert_rpl_port(configured_rpl_port, rpl_port_DUT)

        list_ports_DUT = erps.check_erps_ports(group_id)
        self.assert_ports(rpl_port_DUT, list_ports_DUT)

        is_rpl_owner_DUT = erps.check_rpl_owner(group_id)
        print(is_rpl_owner_DUT)

        if configured_rpl_port != "There is no RPL Port":
            assert is_rpl_owner_DUT == True
        else:
            assert is_rpl_owner_DUT == False

    def confirm_erps_configuration_for_3DUTs_after_one_interface_is_shutdown(self, erps1, erps2, erps3, group_id,
                                                                             configured_rpl_port_DUT1, configured_rpl_port_DUT2,
                                                                             configured_rpl_port_DUT3, final_int_to_shutdown_noshutdown):

        # ----- Asserting for DUT1 -----

        is_rpl_owner_DUT1 = erps1.check_rpl_owner(group_id)

        d_ring_info_DUT1_after_shut = erps1.check_erps_ring_id_information(group_id)
        self.assert_ring_information_after_shutting_down_a_ring_port(d_ring_info_DUT1_after_shut)

        d_ports_DUT1_after_shut = erps1.check_erps_ports_status(group_id)
        print(d_ports_DUT1_after_shut)
        assert d_ports_DUT1_after_shut['Port 1']['MEP Status'] == "Failed"
        assert d_ports_DUT1_after_shut['Port 2']['MEP Status'] == "Ok"

        rpl_port_DUT1_after_shut = erps1.check_rpl_port(group_id)
        self.assert_rpl_port_after_shutting_down_a_ring_port(configured_rpl_port_DUT1, rpl_port_DUT1_after_shut)

        list_ports_DUT1_after_shut = erps1.check_erps_ports(group_id)
        self.assert_ports_after_shutting_down_a_ring_port(rpl_port_DUT1_after_shut, list_ports_DUT1_after_shut, final_int_to_shutdown_noshutdown, d_ports_DUT1_after_shut, is_rpl_owner_DUT1)

        # ----- Asserting for DUT2 -----

        is_rpl_owner_DUT2 = erps2.check_rpl_owner(group_id)

        d_ring_info_DUT2_after_shut = erps2.check_erps_ring_id_information(group_id)
        self.assert_ring_information_after_shutting_down_a_ring_port(d_ring_info_DUT2_after_shut)

        d_ports_DUT2_after_shut = erps2.check_erps_ports_status(group_id)
        print(d_ports_DUT2_after_shut)
        assert d_ports_DUT2_after_shut['Port 1']['MEP Status'] == "Ok"
        assert d_ports_DUT2_after_shut['Port 2']['MEP Status'] == "Failed"

        rpl_port_DUT2_after_shut = erps2.check_rpl_port(group_id)
        self.assert_rpl_port_after_shutting_down_a_ring_port(configured_rpl_port_DUT2, rpl_port_DUT2_after_shut)

        list_ports_DUT2_after_shut = erps2.check_erps_ports(group_id)
        self.assert_ports_after_shutting_down_a_ring_port(rpl_port_DUT2_after_shut, list_ports_DUT2_after_shut, final_int_to_shutdown_noshutdown, d_ports_DUT2_after_shut, is_rpl_owner_DUT2)

        # ----- Asserting for DUT3 -----

        is_rpl_owner_DUT3 = erps3.check_rpl_owner(group_id)

        d_ring_info_DUT3_after_shut = erps3.check_erps_ring_id_information(group_id)
        self.assert_ring_information_after_shutting_down_a_ring_port(d_ring_info_DUT3_after_shut)

        d_ports_DUT3_after_shut = erps3.check_erps_ports_status(group_id)
        print(d_ports_DUT3_after_shut)
        assert d_ports_DUT3_after_shut['Port 1']['MEP Status'] == "Ok"
        assert d_ports_DUT3_after_shut['Port 2']['MEP Status'] == "Ok"

        rpl_port_DUT3_after_shut = erps3.check_rpl_port(group_id)
        self.assert_rpl_port_after_shutting_down_a_ring_port(configured_rpl_port_DUT3, rpl_port_DUT3_after_shut)

        list_ports_DUT3_after_shut = erps3.check_erps_ports(group_id)
        self.assert_ports_after_shutting_down_a_ring_port(rpl_port_DUT3_after_shut, list_ports_DUT3_after_shut, final_int_to_shutdown_noshutdown, d_ports_DUT3_after_shut, is_rpl_owner_DUT3)



