import time
import pytest
import pytest_html
import sys

from flows import erpsflow
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

# Flows

erpsflow = erpsflow.ERPSFlow()


class TestERPSSuite1:

    def test_func_1(self):

        print("###### ERPS_G.8032_Functionality_01 ######")
        print("########## Verify a Port Based single ring ERPS configuration can be succesfully established in a minimum 3 switches topology. #############")

        # <<< ERPS CONFIGURATION >>>

        # STEPS 1-3: Creating ERPS configuration

        erpsflow.create_erps_configuration_for_rpl_owner(vl1, "3500", int1, "Ex 0/1", "Gi 0/9", erps1, "1", "port-based", "8", "88", "99", "9", "gi 0/9")
        erpsflow.create_erps_configuration_for_non_rpl_owner(vl2, "3500", int2, "Gi 0/4", "Gi 0/9", erps2, "1", "port-based", "77", "7", "88", "8")
        erpsflow.create_erps_configuration_for_non_rpl_owner(vl3, "3500", int3, "Gi 0/4", "Gi 0/9", erps3, "1", "port-based", "7", "77", "9", "99")

        # <<< ASSERTING >>>

        # STEP 4: Verify the ERPS mode is working properly, the RPL Port is the only Blocked port with Link Status: Not Failed, and the others ports are UnBlocked

        # Before ASSERTING we have to wait the Wait-to-restore (WTR) timer to expire, which is by default 300000 ms = 300 s

        time.sleep(400)

        # ----- Asserting for DUT1 -----

        d_ring_info_DUT1 = erps1.check_erps_ring_id_information("1")
        erpsflow.assert_ring_information(d_ring_info_DUT1)

        d_ports_DUT1 = erps1.check_erps_ports_status("1")
        erpsflow.assert_ports_status(d_ports_DUT1)

        rpl_port_DUT1 = erps1.check_rpl_port("1")
        erpsflow.assert_rpl_port("gi 0/9", rpl_port_DUT1)

        list_ports_DUT1 = erps1.check_erps_ports("1")
        erpsflow.assert_ports(rpl_port_DUT1, list_ports_DUT1)

        # ----- Asserting for DUT2 -----

        d_ring_info_DUT2 = erps2.check_erps_ring_id_information("1")
        erpsflow.assert_ring_information(d_ring_info_DUT2)

        d_ports_DUT2 = erps2.check_erps_ports_status("1")
        erpsflow.assert_ports_status(d_ports_DUT2)

        rpl_port_DUT2 = erps2.check_rpl_port("1")
        erpsflow.assert_rpl_port("There is no RPL Port", rpl_port_DUT2)

        list_ports_DUT2 = erps2.check_erps_ports("1")
        erpsflow.assert_ports(rpl_port_DUT2, list_ports_DUT2)

        # ----- Asserting for DUT3 -----

        d_ring_info_DUT3 = erps3.check_erps_ring_id_information("1")
        erpsflow.assert_ring_information(d_ring_info_DUT3)

        d_ports_DUT3 = erps3.check_erps_ports_status("1")
        erpsflow.assert_ports_status(d_ports_DUT3)

        rpl_port_DUT3 = erps3.check_rpl_port("1")
        erpsflow.assert_rpl_port("There is no RPL Port", rpl_port_DUT3)

        list_ports_DUT3 = erps3.check_erps_ports("1")
        erpsflow.assert_ports(rpl_port_DUT3, list_ports_DUT3)

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

        erpsflow.removing_the_configuration(int1, "Ex 0/1", "Gi 0/9", erps1, stp1, vl1, "3500")
        erpsflow.removing_the_configuration(int2, "Gi 0/4", "Gi 0/9", erps2, stp2, vl2, "3500")
        erpsflow.removing_the_configuration(int3, "Gi 0/4", "Gi 0/9", erps3, stp3, vl3, "3500")

    def test_func_2(self):

        print("###### ERPS_G.8032_Functionality_02 ######")
        print("########## Verify if the ERPS mode is working properly in the setup. #############")

        # <<< ERPS CONFIGURATION >>>

        # STEPS 1-3: Creating ERPS configuration

        erpsflow.create_erps_configuration_for_rpl_owner(vl1, "3500", int1, "Ex 0/1", "Gi 0/9", erps1, "1", "port-based", "8", "88", "99", "9", "gi 0/9")
        erpsflow.create_erps_configuration_for_non_rpl_owner(vl2, "3500", int2, "Gi 0/4", "Gi 0/9", erps2, "1", "port-based", "77", "7", "88", "8")
        erpsflow.create_erps_configuration_for_non_rpl_owner(vl3, "3500", int3, "Gi 0/4", "Gi 0/9", erps3, "1", "port-based", "7", "77", "9", "99")

        # <<< ASSERTING >>>

        # STEP 4: Verify the ERPS mode is working properly, the RPL Port is the only Blocked port with Link Status: Not Failed, and the others ports are UnBlocked

        # Before ASSERTING we have to wait the Wait-to-restore (WTR) timer to expire, which is by default 300000 ms = 300 s

        time.sleep(400)

        # ----- Asserting for DUT1 -----

        d_ring_info_DUT1 = erps1.check_erps_ring_id_information("1")
        erpsflow.assert_ring_information(d_ring_info_DUT1)

        d_ports_DUT1 = erps1.check_erps_ports_status("1")
        erpsflow.assert_ports_status(d_ports_DUT1)

        rpl_port_DUT1 = erps1.check_rpl_port("1")
        erpsflow.assert_rpl_port("gi 0/9", rpl_port_DUT1)

        list_ports_DUT1 = erps1.check_erps_ports("1")
        erpsflow.assert_ports(rpl_port_DUT1, list_ports_DUT1)

        # ----- Asserting for DUT2 -----

        d_ring_info_DUT2 = erps2.check_erps_ring_id_information("1")
        erpsflow.assert_ring_information(d_ring_info_DUT2)

        d_ports_DUT2 = erps2.check_erps_ports_status("1")
        erpsflow.assert_ports_status(d_ports_DUT2)

        rpl_port_DUT2 = erps2.check_rpl_port("1")
        erpsflow.assert_rpl_port("There is no RPL Port", rpl_port_DUT2)

        list_ports_DUT2 = erps2.check_erps_ports("1")
        erpsflow.assert_ports(rpl_port_DUT2, list_ports_DUT2)

        # ----- Asserting for DUT3 -----

        d_ring_info_DUT3 = erps3.check_erps_ring_id_information("1")
        erpsflow.assert_ring_information(d_ring_info_DUT3)

        d_ports_DUT3 = erps3.check_erps_ports_status("1")
        erpsflow.assert_ports_status(d_ports_DUT3)

        rpl_port_DUT3 = erps3.check_rpl_port("1")
        erpsflow.assert_rpl_port("There is no RPL Port", rpl_port_DUT3)

        list_ports_DUT3 = erps3.check_erps_ports("1")
        erpsflow.assert_ports(rpl_port_DUT3, list_ports_DUT3)

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
        erpsflow.assert_ring_information_after_shutting_down_a_ring_port(d_ring_info_DUT1_after_shut)

        d_ports_DUT1_after_shut = erps1.check_erps_ports_status("1")
        print(d_ports_DUT1_after_shut)
        assert d_ports_DUT1_after_shut['Port 1']['MEP Status'] == "Failed"
        assert d_ports_DUT1_after_shut['Port 2']['MEP Status'] == "Ok"

        rpl_port_DUT1_after_shut = erps1.check_rpl_port("1")
        erpsflow.assert_rpl_port_after_shutting_down_a_ring_port("gi 0/9", rpl_port_DUT1_after_shut)

        list_ports_DUT1_after_shut = erps1.check_erps_ports("1")
        erpsflow.assert_ports_after_shutting_down_a_ring_port(rpl_port_DUT1_after_shut, list_ports_DUT1_after_shut, final_int_to_shutdown_noshutdown, d_ports_DUT1_after_shut, is_rpl_owner_DUT1)

        # ----- Asserting for DUT2 -----
        d_ring_info_DUT2_after_shut = erps2.check_erps_ring_id_information("1")
        erpsflow.assert_ring_information_after_shutting_down_a_ring_port(d_ring_info_DUT2_after_shut)

        d_ports_DUT2_after_shut = erps2.check_erps_ports_status("1")
        print(d_ports_DUT2_after_shut)
        assert d_ports_DUT2_after_shut['Port 1']['MEP Status'] == "Ok"
        assert d_ports_DUT2_after_shut['Port 2']['MEP Status'] == "Failed"

        rpl_port_DUT2_after_shut = erps2.check_rpl_port("1")
        erpsflow.assert_rpl_port_after_shutting_down_a_ring_port("There is no RPL Port", rpl_port_DUT2_after_shut)

        list_ports_DUT2_after_shut = erps2.check_erps_ports("1")
        erpsflow.assert_ports_after_shutting_down_a_ring_port(rpl_port_DUT2_after_shut, list_ports_DUT2_after_shut, final_int_to_shutdown_noshutdown, d_ports_DUT2_after_shut, is_rpl_owner_DUT2)

        # ----- Asserting for DUT3 -----
        d_ring_info_DUT3_after_shut = erps3.check_erps_ring_id_information("1")
        erpsflow.assert_ring_information_after_shutting_down_a_ring_port(d_ring_info_DUT3_after_shut)

        d_ports_DUT3_after_shut = erps3.check_erps_ports_status("1")
        print(d_ports_DUT3_after_shut)
        assert d_ports_DUT3_after_shut['Port 1']['MEP Status'] == "Ok"
        assert d_ports_DUT3_after_shut['Port 2']['MEP Status'] == "Ok"

        rpl_port_DUT3_after_shut = erps3.check_rpl_port("1")
        erpsflow.assert_rpl_port_after_shutting_down_a_ring_port("There is no RPL Port", rpl_port_DUT3_after_shut)

        list_ports_DUT3_after_shut = erps3.check_erps_ports("1")
        erpsflow.assert_ports_after_shutting_down_a_ring_port(rpl_port_DUT3_after_shut, list_ports_DUT3_after_shut, final_int_to_shutdown_noshutdown, d_ports_DUT3_after_shut, is_rpl_owner_DUT3)

        # STEP 7:  No shutdown the port and verify that ERPS mode is still working properly
        int2.no_shut_interfaces(int_to_shutdown_noshutdown)

        # We need to wait for the Wait-to-restore (WTR) timer to expire, by default is 300 s
        time.sleep(350)
        # ASSERTING after the Wait-to-restore (WTR) timer expires

        # ----- Asserting for DUT1 -----

        d_ring_info_DUT1_after_noshut = erps1.check_erps_ring_id_information("1")
        erpsflow.assert_ring_information(d_ring_info_DUT1_after_noshut)

        d_ports_DUT1_after_noshut = erps1.check_erps_ports_status("1")
        erpsflow.assert_ports_status(d_ports_DUT1_after_noshut)

        rpl_port_DUT1_after_noshut = erps1.check_rpl_port("1")
        erpsflow.assert_rpl_port("gi 0/9", rpl_port_DUT1_after_noshut)

        list_ports_DUT1_after_noshut = erps1.check_erps_ports("1")
        erpsflow.assert_ports(rpl_port_DUT1_after_noshut, list_ports_DUT1_after_noshut)

        # ----- Asserting for DUT2 -----

        d_ring_info_DUT2_after_noshut = erps2.check_erps_ring_id_information("1")
        erpsflow.assert_ring_information(d_ring_info_DUT2_after_noshut)

        d_ports_DUT2_after_noshut = erps2.check_erps_ports_status("1")
        erpsflow.assert_ports_status(d_ports_DUT2_after_noshut)

        rpl_port_DUT2_after_noshut = erps2.check_rpl_port("1")
        erpsflow.assert_rpl_port("There is no RPL Port", rpl_port_DUT2_after_noshut)

        list_ports_DUT2_after_noshut = erps2.check_erps_ports("1")
        erpsflow.assert_ports(rpl_port_DUT2_after_noshut, list_ports_DUT2_after_noshut)

        # ----- Asserting for DUT3 -----

        d_ring_info_DUT3_after_noshut = erps3.check_erps_ring_id_information("1")
        erpsflow.assert_ring_information(d_ring_info_DUT3_after_noshut)

        d_ports_DUT3_after_noshut = erps3.check_erps_ports_status("1")
        erpsflow.assert_ports_status(d_ports_DUT3_after_noshut)

        rpl_port_DUT3_after_noshut = erps3.check_rpl_port("1")
        erpsflow.assert_rpl_port("There is no RPL Port", rpl_port_DUT3_after_noshut)

        list_ports_DUT3_after_noshut = erps3.check_erps_ports("1")
        erpsflow.assert_ports(rpl_port_DUT3_after_noshut, list_ports_DUT3_after_noshut)


        # <<< REMOVING THE CONFIGURATION >>>

        erpsflow.removing_the_configuration(int1, "Ex 0/1", "Gi 0/9", erps1, stp1, vl1, "3500")
        erpsflow.removing_the_configuration(int2, "Gi 0/4", "Gi 0/9", erps2, stp2, vl2, "3500")
        erpsflow.removing_the_configuration(int3, "Gi 0/4", "Gi 0/9", erps3, stp3, vl3, "3500")

