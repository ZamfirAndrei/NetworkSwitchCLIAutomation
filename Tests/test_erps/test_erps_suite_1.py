import time
import pytest
import pytest_html
import sys


from config import vlan, interfaces, erps, fdb, stp
from Management import ssh

ip_session_1 = "10.2.109.206"
ip_session_2 = "10.2.109.83"
ip_session_3 = "10.2.109.232"

# DUT 1 Objects

int1 = interfaces.Interface(ip_session=ip_session_1)
vl1 = vlan.VLAN(ip_session=ip_session_1)
erps1 = erps.ERPS(ip_session=ip_session_1)
fdb1 = fdb.FDB(ip_session=ip_session_1)
stp1 = stp.STP(ip_session=ip_session_1)

# DUT 2 Objects

int2 = interfaces.Interface(ip_session=ip_session_2)
vl2 = vlan.VLAN(ip_session=ip_session_2)
erps2 = erps.ERPS(ip_session=ip_session_2)
fdb2 = fdb.FDB(ip_session=ip_session_2)
stp2 = stp.STP(ip_session=ip_session_2)


# DUT 3 Objects

int3 = interfaces.Interface(ip_session=ip_session_3)
vl3 = vlan.VLAN(ip_session=ip_session_3)
erps3 = erps.ERPS(ip_session=ip_session_3)
fdb3 = fdb.FDB(ip_session=ip_session_3)
stp3 = stp.STP(ip_session=ip_session_3)



class TestERPSSuite1:

    def test_func_1(self):

        print("###### ERPS_G.8032_Functionality_01 ######")
        print("########## Verify a Port Based single ring ERPS configuration can be succesfully established in a minimum 3 switches topology. #############")

        # <<< CONFIGURATION >>>
        # STEPS 1-3

        # # < VLAN configuration >
        #
        # # Creating ERPS dedicated traffic VLAN on each DUT
        # vl1.create_vlan("3500")
        # vl2.create_vlan("3500")
        # vl3.create_vlan("3500")
        #
        # # Adding the ports to the ERPS dedicated traffic VLAN on each DUT
        # vl1.add_ports_to_vlan("Ex 0/1", vlan="3500")
        # vl1.add_ports_to_vlan("Gi 0/9", vlan="3500")
        #
        # vl2.add_ports_to_vlan("Gi 0/4", vlan="3500")
        # vl2.add_ports_to_vlan("Gi 0/9", vlan="3500")
        #
        # vl3.add_ports_to_vlan("Gi 0/4", vlan="3500")
        # vl3.add_ports_to_vlan("Gi 0/9", vlan="3500")
        #
        # # < Interfaces configuration >
        #
        # # No shutting the ports for the ERPS dedicated traffic VLAN on each DUT
        # int1.no_shut_interfaces("Ex 0/1", "Gi 0/9")
        # int2.no_shut_interfaces("Gi 0/4", "Gi 0/9")
        # int3.no_shut_interfaces("Gi 0/4", "Gi 0/9")
        #
        # # < ERPS configuration >
        #
        # # ERPS configuration for DUT 1, which will be the RPL Owner
        # erps1.enable_erps_mode()
        # erps1.create_erps_group("1")
        # erps1.configure_erps_protection_type("1", "port-based")
        # erps1.configure_erps_mapped_ports("1", "ex 0/1", "gi 0/9", "3500", "8", "88", "99", "9")
        configured_rpl_port = "gi 0/9"
        # erps1.configure_erps_protected_port("1", configured_rpl_port)
        # erps1.activate_erps_group("1")
        #
        # # ERPS configuration for DUT 2
        # erps2.enable_erps_mode()
        # erps2.create_erps_group("1")
        # erps2.configure_erps_protection_type("1", "port-based")
        # erps2.configure_erps_mapped_ports("1", "gi 0/4", "gi 0/9", "3500", "77", "7", "88", "8")
        # erps2.activate_erps_group("1")
        #
        # # ERPS configuration for DUT 3
        # erps3.enable_erps_mode()
        # erps3.create_erps_group("1")
        # erps3.configure_erps_protection_type("1", "port-based")
        # erps3.configure_erps_mapped_ports("1", "gi 0/4", "gi 0/9", "3500", "7", "77", "9", "99")
        # erps3.activate_erps_group("1")

        # <<< ASSERTING >>>
        # STEP 4: Verify the ERPS mode is working properly, the RPL Port is the only Blocked port with Link Status: Not Failed, and the others ports are UnBlocked

        # Before ASSERTING we have to wait the Wait-to-restore (WTR) timer to expire, which is by default 300000 ms = 300 s
        # time.sleep(400)

        # ----- Asserting for DUT1 -----
        d_ring_info_DUT1 = erps1.check_erps_ring_id_information("1")
        print(d_ring_info_DUT1)
        assert d_ring_info_DUT1['Ring Name'] == "Ring1"
        assert d_ring_info_DUT1['RAPS Vlan Id'] == "3500"
        assert d_ring_info_DUT1['Operating Mode'] == "Revertive"
        assert d_ring_info_DUT1['ERPS Compatible Version'] == "Version1"
        assert d_ring_info_DUT1['Ring State'] == "Idle"
        assert d_ring_info_DUT1['Status'] == "Active"

        d_ports_DUT1 = erps1.check_erps_ports_status("1")
        print(d_ports_DUT1)
        assert d_ports_DUT1['Port 1']['MEP Status'] == "Ok"
        assert d_ports_DUT1['Port 2']['MEP Status'] == "Ok"

        rpl_port_DUT1 = erps1.check_rpl_port("1")
        print(rpl_port_DUT1)
        # Re-Modeling the Configured RPL Port from "gi 0/X" to be "Gi0/X"
        list_rpl_port = []
        list_rpl_port.append(configured_rpl_port[0].upper())
        for i in range(1, len(configured_rpl_port)):
            if configured_rpl_port[i] != ' ':
                list_rpl_port.append(configured_rpl_port[i])
        final_configured_rpl_port_1 = ''.join(list_rpl_port)
        assert rpl_port_DUT1 == final_configured_rpl_port_1

        list_ports_DUT1 = erps1.check_erps_ports("1")
        print(list_ports_DUT1)
        for port in list_ports_DUT1:
            if port['Ring Port'] == rpl_port_DUT1:
                assert port['Link Status'] == 'Not Failed'
                assert port['Port Status'] == 'Blocked'
            else:
                assert port['Link Status'] == 'Not Failed'
                assert port['Port Status'] == 'UnBlocked'

        # ----- Asserting for DUT2 -----
        d_ring_info_DUT2 = erps2.check_erps_ring_id_information("1")
        print(d_ring_info_DUT2)
        assert d_ring_info_DUT2['Ring Name'] == "Ring1"
        assert d_ring_info_DUT2['RAPS Vlan Id'] == "3500"
        assert d_ring_info_DUT2['Operating Mode'] == "Revertive"
        assert d_ring_info_DUT2['ERPS Compatible Version'] == "Version1"
        assert d_ring_info_DUT2['Ring State'] == "Idle"
        assert d_ring_info_DUT2['Status'] == "Active"

        d_ports_DUT2 = erps2.check_erps_ports_status("1")
        print(d_ports_DUT2)
        assert d_ports_DUT2['Port 1']['MEP Status'] == "Ok"
        assert d_ports_DUT2['Port 2']['MEP Status'] == "Ok"

        rpl_port_DUT2 = erps2.check_rpl_port("1")
        print(rpl_port_DUT2)
        assert rpl_port_DUT2 == "There is no RPL Port"

        list_ports_DUT2 = erps2.check_erps_ports("1")
        print(list_ports_DUT2)
        for port in list_ports_DUT2:
            if port['Ring Port'] == rpl_port_DUT2:
                assert port['Link Status'] == 'Not Failed'
                assert port['Port Status'] == 'Blocked'
            else:
                assert port['Link Status'] == 'Not Failed'
                assert port['Port Status'] == 'UnBlocked'

        # ----- Asserting for DUT3 -----
        d_ring_info_DUT3 = erps3.check_erps_ring_id_information("1")
        print(d_ring_info_DUT3)
        assert d_ring_info_DUT3['Ring Name'] == "Ring1"
        assert d_ring_info_DUT3['RAPS Vlan Id'] == "3500"
        assert d_ring_info_DUT3['Operating Mode'] == "Revertive"
        assert d_ring_info_DUT3['ERPS Compatible Version'] == "Version1"
        assert d_ring_info_DUT3['Ring State'] == "Idle"
        assert d_ring_info_DUT3['Status'] == "Active"

        d_ports_DUT3 = erps3.check_erps_ports_status("1")
        print(d_ring_info_DUT3)
        assert d_ports_DUT3['Port 1']['MEP Status'] == "Ok"
        assert d_ports_DUT3['Port 2']['MEP Status'] == "Ok"

        rpl_port_DUT3 = erps3.check_rpl_port("1")
        print(rpl_port_DUT3)
        assert rpl_port_DUT3 == "There is no RPL Port"

        list_ports_DUT3 = erps3.check_erps_ports("1")
        print(list_ports_DUT3)
        for port in list_ports_DUT3:
            if port['Ring Port'] == rpl_port_DUT3:
                assert port['Link Status'] == 'Not Failed'
                assert port['Port Status'] == 'Blocked'
            else:
                assert port['Link Status'] == 'Not Failed'
                assert port['Port Status'] == 'UnBlocked'

        # STEP 5: Verify that only one DUT is the RPL Owner
        is_rpl_owner_DUT1 = erps1.check_rpl_owner("1")
        print(is_rpl_owner_DUT1)
        assert is_rpl_owner_DUT1 == True;

        is_rpl_owner_DUT2 = erps2.check_rpl_owner("1")
        print(is_rpl_owner_DUT2)
        assert is_rpl_owner_DUT2 == False;

        is_rpl_owner_DUT3 = erps3.check_rpl_owner("1")
        print(is_rpl_owner_DUT3)
        assert is_rpl_owner_DUT3 == False;

        # <<< REMOVING THE CONFIGURATION >>>

        int1.shut_interfaces("Ex 0/1", "Gi 0/9")
        erps1.disable_erps_mode()
        stp1.stp_enable(port="Ex 0/1")
        stp1.stp_enable(port="Gi 0/9")
        vl1.remove_vlan("3500")

        int2.shut_interfaces("Gi 0/4", "Gi 0/9")
        erps2.disable_erps_mode()
        stp2.stp_enable(port="Gi 0/4")
        stp2.stp_enable(port="Gi 0/9")
        vl2.remove_vlan("3500")


        int3.shut_interfaces("Gi 0/4", "Gi 0/9")
        erps3.disable_erps_mode()
        stp3.stp_enable(port="Gi 0/4")
        stp3.stp_enable(port="Gi 0/9")
        vl3.remove_vlan("3500")


        int1.no_shut_interfaces("Ex 0/1", "Gi 0/9")
        int2.no_shut_interfaces("Gi 0/4", "Gi 0/9")
        int3.no_shut_interfaces("Gi 0/4", "Gi 0/9")

    def test_func_2(self):

        print("###### ERPS_G.8032_Functionality_02 ######")
        print("########## Verify if the ERPS mode is working properly in the setup. #############")

        # <<< CONFIGURATION >>>
        # STEPS 1-3

        # < VLAN configuration >

        # Creating ERPS dedicated traffic VLAN on each DUT
        vl1.create_vlan("3500")
        vl2.create_vlan("3500")
        vl3.create_vlan("3500")

        # Adding the ports to the ERPS dedicated traffic VLAN on each DUT
        vl1.add_ports_to_vlan("Ex 0/1", vlan="3500")
        vl1.add_ports_to_vlan("Gi 0/9", vlan="3500")

        vl2.add_ports_to_vlan("Gi 0/4", vlan="3500")
        vl2.add_ports_to_vlan("Gi 0/9", vlan="3500")

        vl3.add_ports_to_vlan("Gi 0/4", vlan="3500")
        vl3.add_ports_to_vlan("Gi 0/9", vlan="3500")

        # < Interfaces configuration >

        # No shutting the ports for the ERPS dedicated traffic VLAN on each DUT
        int1.no_shut_interfaces("Ex 0/1", "Gi 0/9")
        int2.no_shut_interfaces("Gi 0/4", "Gi 0/9")
        int3.no_shut_interfaces("Gi 0/4", "Gi 0/9")

        # < ERPS configuration >

        # ERPS configuration for DUT 1, which will be the RPL Owner
        erps1.enable_erps_mode()
        erps1.create_erps_group("1")
        erps1.configure_erps_protection_type("1", "port-based")
        erps1.configure_erps_mapped_ports("1", "ex 0/1", "gi 0/9", "3500", "8", "88", "99", "9")
        configured_rpl_port = "gi 0/9"
        erps1.configure_erps_protected_port("1", configured_rpl_port)
        erps1.activate_erps_group("1")

        # ERPS configuration for DUT 2
        erps2.enable_erps_mode()
        erps2.create_erps_group("1")
        erps2.configure_erps_protection_type("1", "port-based")
        erps2.configure_erps_mapped_ports("1", "gi 0/4", "gi 0/9", "3500", "77", "7", "88", "8")
        erps2.activate_erps_group("1")

        # ERPS configuration for DUT 3
        erps3.enable_erps_mode()
        erps3.create_erps_group("1")
        erps3.configure_erps_protection_type("1", "port-based")
        erps3.configure_erps_mapped_ports("1", "gi 0/4", "gi 0/9", "3500", "7", "77", "9", "99")
        erps3.activate_erps_group("1")

        # <<< ASSERTING >>>
        # STEP 4: Verify the ERPS mode is working properly, the RPL Port is the only Blocked port with Link Status: Not Failed, and the others ports are UnBlocked

        # Before ASSERTING we have to wait the Wait-to-restore (WTR) timer to expire, which is by default 300000 ms = 300 s
        time.sleep(350)

        # ----- Asserting for DUT1 -----
        d_ring_info_DUT1 = erps1.check_erps_ring_id_information("1")
        print(d_ring_info_DUT1)
        assert d_ring_info_DUT1['Ring Name'] == "Ring1"
        assert d_ring_info_DUT1['RAPS Vlan Id'] == "3500"
        assert d_ring_info_DUT1['Operating Mode'] == "Revertive"
        assert d_ring_info_DUT1['ERPS Compatible Version'] == "Version1"
        assert d_ring_info_DUT1['Ring State'] == "Idle"
        assert d_ring_info_DUT1['Status'] == "Active"

        d_ports_DUT1 = erps1.check_erps_ports_status("1")
        print(d_ports_DUT1)
        assert d_ports_DUT1['Port 1']['MEP Status'] == "Ok"
        assert d_ports_DUT1['Port 2']['MEP Status'] == "Ok"

        rpl_port_DUT1 = erps1.check_rpl_port("1")
        print(rpl_port_DUT1)
        # Re-Modeling the Configured RPL Port from "gi 0/X" to be "Gi0/X"
        list_rpl_port = []
        list_rpl_port.append(configured_rpl_port[0].upper())
        for i in range(1, len(configured_rpl_port)):
            if configured_rpl_port[i] != ' ':
                list_rpl_port.append(configured_rpl_port[i])
        final_configured_rpl_port_1 = ''.join(list_rpl_port)
        assert rpl_port_DUT1 == final_configured_rpl_port_1

        list_ports_DUT1 = erps1.check_erps_ports("1")
        print(list_ports_DUT1)
        for port in list_ports_DUT1:
            if port['Ring Port'] == rpl_port_DUT1:
                assert port['Link Status'] == 'Not Failed'
                assert port['Port Status'] == 'Blocked'
            else:
                assert port['Link Status'] == 'Not Failed'
                assert port['Port Status'] == 'UnBlocked'

        # ----- Asserting for DUT2 -----
        d_ring_info_DUT2 = erps2.check_erps_ring_id_information("1")
        print(d_ring_info_DUT2)
        assert d_ring_info_DUT2['Ring Name'] == "Ring1"
        assert d_ring_info_DUT2['RAPS Vlan Id'] == "3500"
        assert d_ring_info_DUT2['Operating Mode'] == "Revertive"
        assert d_ring_info_DUT2['ERPS Compatible Version'] == "Version1"
        assert d_ring_info_DUT2['Ring State'] == "Idle"
        assert d_ring_info_DUT2['Status'] == "Active"

        d_ports_DUT2 = erps2.check_erps_ports_status("1")
        print(d_ports_DUT2)
        assert d_ports_DUT2['Port 1']['MEP Status'] == "Ok"
        assert d_ports_DUT2['Port 2']['MEP Status'] == "Ok"

        rpl_port_DUT2 = erps2.check_rpl_port("1")
        print(rpl_port_DUT2)
        assert rpl_port_DUT2 == "There is no RPL Port"

        list_ports_DUT2 = erps2.check_erps_ports("1")
        print(list_ports_DUT2)
        for port in list_ports_DUT2:
            if port['Ring Port'] == rpl_port_DUT2:
                assert port['Link Status'] == 'Not Failed'
                assert port['Port Status'] == 'Blocked'
            else:
                assert port['Link Status'] == 'Not Failed'
                assert port['Port Status'] == 'UnBlocked'

        # ----- Asserting for DUT3 -----
        d_ring_info_DUT3 = erps3.check_erps_ring_id_information("1")
        print(d_ring_info_DUT3)
        assert d_ring_info_DUT3['Ring Name'] == "Ring1"
        assert d_ring_info_DUT3['RAPS Vlan Id'] == "3500"
        assert d_ring_info_DUT3['Operating Mode'] == "Revertive"
        assert d_ring_info_DUT3['ERPS Compatible Version'] == "Version1"
        assert d_ring_info_DUT3['Ring State'] == "Idle"
        assert d_ring_info_DUT3['Status'] == "Active"

        d_ports_DUT3 = erps3.check_erps_ports_status("1")
        print(d_ring_info_DUT3)
        assert d_ports_DUT3['Port 1']['MEP Status'] == "Ok"
        assert d_ports_DUT3['Port 2']['MEP Status'] == "Ok"

        rpl_port_DUT3 = erps3.check_rpl_port("1")
        print(rpl_port_DUT3)
        assert rpl_port_DUT3 == "There is no RPL Port"

        list_ports_DUT3 = erps3.check_erps_ports("1")
        print(list_ports_DUT3)
        for port in list_ports_DUT3:
            if port['Ring Port'] == rpl_port_DUT3:
                assert port['Link Status'] == 'Not Failed'
                assert port['Port Status'] == 'Blocked'
            else:
                assert port['Link Status'] == 'Not Failed'
                assert port['Port Status'] == 'UnBlocked'

        # STEP 5: Verify that only one DUT is the RPL Owner
        is_rpl_owner_DUT1 = erps1.check_rpl_owner("1")
        print(is_rpl_owner_DUT1)
        assert is_rpl_owner_DUT1 == True;

        is_rpl_owner_DUT2 = erps2.check_rpl_owner("1")
        print(is_rpl_owner_DUT2)
        assert is_rpl_owner_DUT2 == False;

        is_rpl_owner_DUT3 = erps3.check_rpl_owner("1")
        print(is_rpl_owner_DUT3)
        assert is_rpl_owner_DUT3 == False;

        # STEP 6:  Shutdown one of the ring member ports and verify that ERPS mode is working properly
        int_to_shutdown_noshutdown = "Gi 0/9"
        int2.shut_interfaces(int_to_shutdown_noshutdown)

        int_to_shutdown_noshutdown_split = int_to_shutdown_noshutdown.split(" ")
        final_int_to_shutdown_noshutdown = ''.join(int_to_shutdown_noshutdown_split)
        print(final_int_to_shutdown_noshutdown)

        # ----- Asserting for DUT1 -----
        d_ring_info_DUT1_after_shut = erps1.check_erps_ring_id_information("1")
        print(d_ring_info_DUT1_after_shut)
        assert d_ring_info_DUT1_after_shut['Ring Name'] == "Ring1"
        assert d_ring_info_DUT1_after_shut['RAPS Vlan Id'] == "3500"
        assert d_ring_info_DUT1_after_shut['Operating Mode'] == "Revertive"
        assert d_ring_info_DUT1_after_shut['ERPS Compatible Version'] == "Version1"
        assert d_ring_info_DUT1_after_shut['Ring State'] == "Protection"
        assert d_ring_info_DUT1_after_shut['Status'] == "Active"

        d_ports_DUT1_after_shut = erps1.check_erps_ports_status("1")
        print(d_ports_DUT1_after_shut)
        assert d_ports_DUT1_after_shut['Port 1']['MEP Status'] == "Failed"
        assert d_ports_DUT1_after_shut['Port 2']['MEP Status'] == "Ok"

        rpl_port_DUT1_after_shut = erps1.check_rpl_port("1")
        print(rpl_port_DUT1_after_shut)
        # Re-Modeling the Configured RPL Port from "gi 0/X" to be "Gi0/X"
        list_rpl_port_after_shut = []
        list_rpl_port_after_shut.append(configured_rpl_port[0].upper())
        for i in range(1, len(configured_rpl_port)):
            if configured_rpl_port[i] != ' ':
                list_rpl_port_after_shut.append(configured_rpl_port[i])
        final_configured_rpl_port_1_after_shut = ''.join(list_rpl_port_after_shut)
        assert rpl_port_DUT1_after_shut == final_configured_rpl_port_1_after_shut

        list_ports_DUT1_after_shut = erps1.check_erps_ports("1")
        print(list_ports_DUT1_after_shut)
        for port in list_ports_DUT1_after_shut:
            if port['Ring Port'] == rpl_port_DUT1_after_shut:
                assert port['Link Status'] == 'Not Failed'
                assert port['Port Status'] == 'UnBlocked'
            elif port['Ring Port'] == final_int_to_shutdown_noshutdown and (d_ports_DUT1_after_shut['Port 1']['MEP Status'] == "Failed" or d_ports_DUT1_after_shut['Port 2']['MEP Status'] == "Failed"):
                assert port['Link Status'] == 'Failed'
                assert port['Port Status'] == 'Blocked'
            else:
                if d_ports_DUT1_after_shut['Port 1']['MEP Status'] == "Ok" and d_ports_DUT1_after_shut['Port 2']['MEP Status'] == "Ok":
                    assert port['Link Status'] == 'Remote Failure'
                    assert port['Port Status'] == 'UnBlocked'
                elif is_rpl_owner_DUT1:
                    assert port['Link Status'] == 'Failed'
                    assert port['Port Status'] == 'Blocked'
                else:
                    assert port['Link Status'] == 'Not Failed'
                    assert port['Port Status'] == 'UnBlocked'

        # ----- Asserting for DUT2 -----
        d_ring_info_DUT2_after_shut = erps2.check_erps_ring_id_information("1")
        print(d_ring_info_DUT2_after_shut)
        assert d_ring_info_DUT2_after_shut['Ring Name'] == "Ring1"
        assert d_ring_info_DUT2_after_shut['RAPS Vlan Id'] == "3500"
        assert d_ring_info_DUT2_after_shut['Operating Mode'] == "Revertive"
        assert d_ring_info_DUT2_after_shut['ERPS Compatible Version'] == "Version1"
        assert d_ring_info_DUT2_after_shut['Ring State'] == "Protection"
        assert d_ring_info_DUT2_after_shut['Status'] == "Active"

        d_ports_DUT2_after_shut = erps2.check_erps_ports_status("1")
        print(d_ports_DUT2_after_shut)
        assert d_ports_DUT2_after_shut['Port 1']['MEP Status'] == "Ok"
        assert d_ports_DUT2_after_shut['Port 2']['MEP Status'] == "Failed"

        rpl_port_DUT2_after_shut = erps2.check_rpl_port("1")
        print(rpl_port_DUT2_after_shut)
        assert rpl_port_DUT2_after_shut == "There is no RPL Port"

        list_ports_DUT2_after_shut = erps2.check_erps_ports("1")
        print(list_ports_DUT2_after_shut)
        for port in list_ports_DUT2_after_shut:
            if port['Ring Port'] == rpl_port_DUT2_after_shut:
                assert port['Link Status'] == 'Not Failed'
                assert port['Port Status'] == 'UnBlocked'
            elif port['Ring Port'] == final_int_to_shutdown_noshutdown and (d_ports_DUT2_after_shut['Port 1']['MEP Status'] == "Failed" or d_ports_DUT2_after_shut['Port 2']['MEP Status'] == "Failed"):
                assert port['Link Status'] == 'Failed'
                assert port['Port Status'] == 'Blocked'
            else:
                if d_ports_DUT2_after_shut['Port 1']['MEP Status'] == "Ok" and d_ports_DUT2_after_shut['Port 2']['MEP Status'] == "Ok":
                    assert port['Link Status'] == 'Remote Failure'
                    assert port['Port Status'] == 'UnBlocked'
                elif is_rpl_owner_DUT2:
                    assert port['Link Status'] == 'Failed'
                    assert port['Port Status'] == 'Blocked'
                else:
                    assert port['Link Status'] == 'Not Failed'
                    assert port['Port Status'] == 'UnBlocked'

        # ----- Asserting for DUT3 -----
        d_ring_info_DUT3_after_shut = erps3.check_erps_ring_id_information("1")
        print(d_ring_info_DUT3_after_shut)
        assert d_ring_info_DUT3_after_shut['Ring Name'] == "Ring1"
        assert d_ring_info_DUT3_after_shut['RAPS Vlan Id'] == "3500"
        assert d_ring_info_DUT3_after_shut['Operating Mode'] == "Revertive"
        assert d_ring_info_DUT3_after_shut['ERPS Compatible Version'] == "Version1"
        assert d_ring_info_DUT3_after_shut['Ring State'] == "Protection"
        assert d_ring_info_DUT3_after_shut['Status'] == "Active"

        d_ports_DUT3_after_shut = erps3.check_erps_ports_status("1")
        print(d_ring_info_DUT3_after_shut)
        assert d_ports_DUT3_after_shut['Port 1']['MEP Status'] == "Ok"
        assert d_ports_DUT3_after_shut['Port 2']['MEP Status'] == "Ok"

        rpl_port_DUT3_after_shut = erps3.check_rpl_port("1")
        print(rpl_port_DUT3_after_shut)
        assert rpl_port_DUT3_after_shut == "There is no RPL Port"

        list_ports_DUT3_after_shut = erps3.check_erps_ports("1")
        print(list_ports_DUT3_after_shut)
        for port in list_ports_DUT3_after_shut:
            if port['Ring Port'] == rpl_port_DUT3_after_shut:
                assert port['Link Status'] == 'Not Failed'
                assert port['Port Status'] == 'UnBlocked'
            elif port['Ring Port'] == final_int_to_shutdown_noshutdown and (d_ports_DUT3_after_shut['Port 1']['MEP Status'] == "Failed" or d_ports_DUT3_after_shut['Port 2']['MEP Status'] == "Failed"):
                assert port['Link Status'] == 'Failed'
                assert port['Port Status'] == 'Blocked'
            else:
                if d_ports_DUT3_after_shut['Port 1']['MEP Status'] == "Ok" and d_ports_DUT3_after_shut['Port 2']['MEP Status'] == "Ok":
                    assert port['Link Status'] == 'Remote Failure'
                    assert port['Port Status'] == 'UnBlocked'
                elif is_rpl_owner_DUT3:
                    assert port['Link Status'] == 'Failed'
                    assert port['Port Status'] == 'Blocked'
                else:
                    assert port['Link Status'] == 'Not Failed'
                    assert port['Port Status'] == 'UnBlocked'

        # STEP 7:  No shutdown the port and verify that ERPS mode is still working properly
        int2.no_shut_interfaces(int_to_shutdown_noshutdown)

        # We need to wait for the Wait-to-restore (WTR) timer to expire, by default is 300 s
        time.sleep(350)
        # ASSERTING after the Wait-to-restore (WTR) timer expires

        # ----- Asserting for DUT1 -----
        d_ring_info_DUT1_after_noshut = erps1.check_erps_ring_id_information("1")
        print(d_ring_info_DUT1_after_noshut)
        assert d_ring_info_DUT1_after_noshut['Ring Name'] == "Ring1"
        assert d_ring_info_DUT1_after_noshut['RAPS Vlan Id'] == "3500"
        assert d_ring_info_DUT1_after_noshut['Operating Mode'] == "Revertive"
        assert d_ring_info_DUT1_after_noshut['ERPS Compatible Version'] == "Version1"
        assert d_ring_info_DUT1_after_noshut['Ring State'] == "Idle"
        assert d_ring_info_DUT1_after_noshut['Status'] == "Active"

        d_ports_DUT1_after_noshut = erps1.check_erps_ports_status("1")
        print(d_ports_DUT1_after_noshut)
        assert d_ports_DUT1_after_noshut['Port 1']['MEP Status'] == "Ok"
        assert d_ports_DUT1_after_noshut['Port 2']['MEP Status'] == "Ok"

        rpl_port_DUT1_after_noshut = erps1.check_rpl_port("1")
        print(rpl_port_DUT1_after_noshut)
        # Re-Modeling the Configured RPL Port from "gi 0/X" to be "Gi0/X"
        list_rpl_port_after_noshut = []
        list_rpl_port_after_noshut.append(configured_rpl_port[0].upper())
        for i in range(1, len(configured_rpl_port)):
            if configured_rpl_port[i] != ' ':
                list_rpl_port_after_noshut.append(configured_rpl_port[i])
        final_configured_rpl_port_1_after_noshut = ''.join(list_rpl_port_after_noshut)
        assert rpl_port_DUT1_after_noshut == final_configured_rpl_port_1_after_noshut

        list_ports_DUT1_after_noshut = erps1.check_erps_ports("1")
        print(list_ports_DUT1_after_noshut)
        for port in list_ports_DUT1_after_noshut:
            if port['Ring Port'] == rpl_port_DUT1_after_noshut:
                assert port['Link Status'] == 'Not Failed'
                assert port['Port Status'] == 'Blocked'
            else:
                assert port['Link Status'] == 'Not Failed'
                assert port['Port Status'] == 'UnBlocked'

        # ----- Asserting for DUT2 -----
        d_ring_info_DUT2_after_noshut = erps2.check_erps_ring_id_information("1")
        print(d_ring_info_DUT2_after_noshut)
        assert d_ring_info_DUT2_after_noshut['Ring Name'] == "Ring1"
        assert d_ring_info_DUT2_after_noshut['RAPS Vlan Id'] == "3500"
        assert d_ring_info_DUT2_after_noshut['Operating Mode'] == "Revertive"
        assert d_ring_info_DUT2_after_noshut['ERPS Compatible Version'] == "Version1"
        assert d_ring_info_DUT2_after_noshut['Ring State'] == "Idle"
        assert d_ring_info_DUT2_after_noshut['Status'] == "Active"

        d_ports_DUT2_after_noshut = erps2.check_erps_ports_status("1")
        print(d_ports_DUT2_after_noshut)
        assert d_ports_DUT2_after_noshut['Port 1']['MEP Status'] == "Ok"
        assert d_ports_DUT2_after_noshut['Port 2']['MEP Status'] == "Ok"

        rpl_port_DUT2_after_noshut = erps2.check_rpl_port("1")
        print(rpl_port_DUT2_after_noshut)
        assert rpl_port_DUT2_after_noshut == "There is no RPL Port"

        list_ports_DUT2_after_noshut = erps2.check_erps_ports("1")
        print(list_ports_DUT2_after_noshut)
        for port in list_ports_DUT2_after_noshut:
            if port['Ring Port'] == rpl_port_DUT2_after_noshut:
                assert port['Link Status'] == 'Not Failed'
                assert port['Port Status'] == 'Blocked'
            else:
                assert port['Link Status'] == 'Not Failed'
                assert port['Port Status'] == 'UnBlocked'

        # ----- Asserting for DUT3 -----
        d_ring_info_DUT3_after_noshut = erps3.check_erps_ring_id_information("1")
        print(d_ring_info_DUT3_after_noshut)
        assert d_ring_info_DUT3_after_noshut['Ring Name'] == "Ring1"
        assert d_ring_info_DUT3_after_noshut['RAPS Vlan Id'] == "3500"
        assert d_ring_info_DUT3_after_noshut['Operating Mode'] == "Revertive"
        assert d_ring_info_DUT3_after_noshut['ERPS Compatible Version'] == "Version1"
        assert d_ring_info_DUT3_after_noshut['Ring State'] == "Idle"
        assert d_ring_info_DUT3_after_noshut['Status'] == "Active"

        d_ports_DUT3_after_noshut = erps3.check_erps_ports_status("1")
        print(d_ring_info_DUT3_after_noshut)
        assert d_ports_DUT3_after_noshut['Port 1']['MEP Status'] == "Ok"
        assert d_ports_DUT3_after_noshut['Port 2']['MEP Status'] == "Ok"

        rpl_port_DUT3_after_noshut = erps3.check_rpl_port("1")
        print(rpl_port_DUT3_after_noshut)
        assert rpl_port_DUT3_after_noshut == "There is no RPL Port"

        list_ports_DUT3_after_noshut = erps3.check_erps_ports("1")
        print(list_ports_DUT3_after_noshut)
        for port in list_ports_DUT3_after_noshut:
            if port['Ring Port'] == rpl_port_DUT3_after_noshut:
                assert port['Link Status'] == 'Not Failed'
                assert port['Port Status'] == 'Blocked'
            else:
                assert port['Link Status'] == 'Not Failed'
                assert port['Port Status'] == 'UnBlocked'

        # <<< REMOVING THE CONFIGURATION >>>

        int1.shut_interfaces("Ex 0/1", "Gi 0/9")
        erps1.disable_erps_mode()
        stp1.stp_enable(port="Ex 0/1")
        stp1.stp_enable(port="Gi 0/9")
        vl1.remove_vlan("3500")

        int2.shut_interfaces("Gi 0/4", "Gi 0/9")
        erps2.disable_erps_mode()
        stp2.stp_enable(port="Gi 0/4")
        stp2.stp_enable(port="Gi 0/9")
        vl2.remove_vlan("3500")

        int3.shut_interfaces("Gi 0/4", "Gi 0/9")
        erps3.disable_erps_mode()
        stp3.stp_enable(port="Gi 0/4")
        stp3.stp_enable(port="Gi 0/9")
        vl3.remove_vlan("3500")

        int1.no_shut_interfaces("Ex 0/1", "Gi 0/9")
        int2.no_shut_interfaces("Gi 0/4", "Gi 0/9")
        int3.no_shut_interfaces("Gi 0/4", "Gi 0/9")
