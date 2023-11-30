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
        print("########## Verify a Port Based single ring ERPS configuration can be succesfully established in a minimum 3 switches topology #############")

        # <<< ERPS CONFIGURATION >>>

        # STEPS 1-3: Creating ERPS configuration

        erpsflow.create_erps_configuration_for_rpl_owner(vl1, "3500", int1, "Ex 0/1", "Gi 0/9", erps1, "1", "port-based", "8", "88", "99", "9", "gi 0/9")
        erpsflow.create_erps_configuration_for_non_rpl_owner(vl2, "3500", int2, "Gi 0/4", "Gi 0/9", erps2, "1", "port-based", "77", "7", "88", "8")
        erpsflow.create_erps_configuration_for_non_rpl_owner(vl3, "3500", int3, "Gi 0/4", "Gi 0/9", erps3, "1", "port-based", "7", "77", "9", "99")

        # <<< ASSERTING >>>

        # STEP 4: Verify the ERPS mode is working properly, the RPL Port is the only Blocked port
        # with Link Status: Not Failed, and the others ports are UnBlocked
        # STEP 5: Verify that only one DUT is the RPL Owner

        # Before ASSERTING we have to wait the Wait-to-restore (WTR) timer to expire,
        # which is by default 300000 ms = 300 s

        time.sleep(400)

        # ----- Asserting for DUT1 -----

        erpsflow.confirm_erps_configuration(erps1, group_id="1", configured_rpl_port="gi 0/9")

        # ----- Asserting for DUT2 -----

        erpsflow.confirm_erps_configuration(erps2, group_id="1", configured_rpl_port="There is no RPL Port")

        # ----- Asserting for DUT3 -----

        erpsflow.confirm_erps_configuration(erps3, group_id="1", configured_rpl_port="There is no RPL Port")

        # <<< REMOVING THE CONFIGURATION >>>

        erpsflow.removing_the_erps_configuration(int1, "Ex 0/1", "Gi 0/9", erps1, stp1, vl1, "3500")
        erpsflow.removing_the_erps_configuration(int2, "Gi 0/4", "Gi 0/9", erps2, stp2, vl2, "3500")
        erpsflow.removing_the_erps_configuration(int3, "Gi 0/4", "Gi 0/9", erps3, stp3, vl3, "3500")

    def test_func_2(self):

        print("###### ERPS_G.8032_Functionality_02 ######")
        print("########## Verify if the ERPS mode is working properly in the setup #############")

        # <<< ERPS CONFIGURATION >>>

        # STEPS 1-3: Creating ERPS configuration

        erpsflow.create_erps_configuration_for_rpl_owner(vl1, "3500", int1, "Ex 0/1", "Gi 0/9", erps1, "1", "port-based", "8", "88", "99", "9", "gi 0/9")
        erpsflow.create_erps_configuration_for_non_rpl_owner(vl2, "3500", int2, "Gi 0/4", "Gi 0/9", erps2, "1", "port-based", "77", "7", "88", "8")
        erpsflow.create_erps_configuration_for_non_rpl_owner(vl3, "3500", int3, "Gi 0/4", "Gi 0/9", erps3, "1", "port-based", "7", "77", "9", "99")

        # Change the WTR Timer for the RPL Owner to 60000 ms = 60 s

        erps1.configure_erps_revertive_mode("1", "60000")

        # <<< ASSERTING >>>

        # STEP 4: Verify the ERPS mode is working properly, the RPL Port is the only Blocked port
        # with Link Status: Not Failed, and the others ports are UnBlocked
        # STEP 5: Verify that only one DUT is the RPL Owner

        # Before ASSERTING we have to wait the configured Wait-to-restore (WTR) timer to expire:
        # 60000 ms = 60 s, which is by default 300000 ms = 300 s

        time.sleep(65)

        # ----- Asserting for DUT1 -----

        erpsflow.confirm_erps_configuration(erps1, group_id="1", configured_rpl_port="gi 0/9")

        # ----- Asserting for DUT2 -----

        erpsflow.confirm_erps_configuration(erps2, group_id="1", configured_rpl_port="There is no RPL Port")

        # ----- Asserting for DUT3 -----

        erpsflow.confirm_erps_configuration(erps3, group_id="1", configured_rpl_port="There is no RPL Port")

        # STEP 6:  Shutdown one of the ring member ports and verify that ERPS mode is working properly

        # Shutting down interface Gi 0/9 of DUT2
        int_to_shutdown_noshutdown = "Gi 0/9"
        int2.shut_interfaces(int_to_shutdown_noshutdown)

        int_to_shutdown_noshutdown_split = int_to_shutdown_noshutdown.split(" ")
        final_int_to_shutdown_noshutdown = ''.join(int_to_shutdown_noshutdown_split)
        print(final_int_to_shutdown_noshutdown)

        # ----- Asserting for DUT1, DUT2, DUT3 -----

        erpsflow.confirm_erps_configuration_for_3DUTs_after_one_interface_is_shutdown(erps1, erps2, erps3,
                                                                                       final_int_to_shutdown_noshutdown, group_id="1",
                                                                                       configured_rpl_port_DUT1="gi 0/9", configured_rpl_port_DUT2="There is no RPL Port",
                                                                                       configured_rpl_port_DUT3="There is no RPL Port")

        # STEP 7:  No shutdown the port and verify that ERPS mode is still working properly
        int2.no_shut_interfaces(int_to_shutdown_noshutdown)

        # We need to wait for the configured Wait-to-restore (WTR) timer to expire: 60 s
        time.sleep(65)
        # ASSERTING after the Wait-to-restore (WTR) timer expires

        # ----- Asserting for DUT1 -----

        erpsflow.confirm_erps_configuration(erps1, group_id="1", configured_rpl_port="gi 0/9")

        # ----- Asserting for DUT2 -----

        erpsflow.confirm_erps_configuration(erps2, group_id="1", configured_rpl_port="There is no RPL Port")

        # ----- Asserting for DUT3 -----

        erpsflow.confirm_erps_configuration(erps3, group_id="1", configured_rpl_port="There is no RPL Port")

        # <<< REMOVING THE CONFIGURATION >>>

        erpsflow.removing_the_erps_configuration(int1, "Ex 0/1", "Gi 0/9", erps1, stp1, vl1, "3500")
        erpsflow.removing_the_erps_configuration(int2, "Gi 0/4", "Gi 0/9", erps2, stp2, vl2, "3500")
        erpsflow.removing_the_erps_configuration (int3, "Gi 0/4", "Gi 0/9", erps3, stp3, vl3, "3500")

    def test_func_4(self):

        print("###### ERPS_G.8032_Functionality_04 ######")
        print("########## Verify the process of changing the RPL owner #############")

        # # <<< ERPS CONFIGURATION >>>
        #
        # # STEPS 1-3: Creating ERPS configuration
        #
        # erpsflow.create_erps_configuration_for_rpl_owner(vl1, "3500", int1, "Ex 0/1", "Gi 0/9", erps1, "1",
        #                                                  "port-based", "8", "88", "99", "9", "gi 0/9")
        # erpsflow.create_erps_configuration_for_non_rpl_owner(vl2, "3500", int2, "Gi 0/4", "Gi 0/9", erps2, "1",
        #                                                      "port-based", "77", "7", "88", "8")
        # erpsflow.create_erps_configuration_for_non_rpl_owner(vl3, "3500", int3, "Gi 0/4", "Gi 0/9", erps3, "1",
        #                                                      "port-based", "7", "77", "9", "99")
        #
        # # Change the WTR Timer for the RPL Owner to 60000 ms = 60 s
        #
        # erps1.configure_erps_revertive_mode("1", "60000")
        #
        # # <<< ASSERTING >>>
        #
        # # STEP 4: Verify the ERPS mode is working properly, the RPL Port is the only Blocked port
        # # with Link Status: Not Failed, and the others ports are UnBlocked
        # # STEP 5: Verify that only one DUT is the RPL Owner
        #
        # # Before ASSERTING we have to wait the configured Wait-to-restore (WTR) timer to expire:
        # # 60000 ms = 60 s, which is by default 300000 ms = 300 s
        #
        # time.sleep(65)

        # ----- Asserting for DUT1 -----

        erpsflow.confirm_erps_configuration(erps1, group_id="1", configured_rpl_port="gi 0/9")

        # ----- Asserting for DUT2 -----

        erpsflow.confirm_erps_configuration(erps2, group_id="1", configured_rpl_port="There is no RPL Port")

        # ----- Asserting for DUT3 -----

        erpsflow.confirm_erps_configuration(erps3, group_id="1", configured_rpl_port="There is no RPL Port")

        # STEP 6: Attempt to change the protected port, RPL Link, on the DUT that is the RPL Owner
        # and verify that after that the DUT is still the RPL Owner

        erpsflow.change_the_rpl_port_on_the_rpl_owner(erps1, group_id="1", new_rpl_port="ex 0/1")

        time.sleep(65)

        # ----- Asserting for DUT1 -----

        erpsflow.confirm_erps_configuration(erps1, group_id="1", configured_rpl_port="ex 0/1")

        # ----- Asserting for DUT2 -----

        erpsflow.confirm_erps_configuration(erps2, group_id="1", configured_rpl_port="There is no RPL Port")

        # ----- Asserting for DUT3 -----

        erpsflow.confirm_erps_configuration(erps3, group_id="1", configured_rpl_port="There is no RPL Port")

        # STEP 7: Remove the RPL Owner configuration from the DUT you configured at the beginning
        # and reconfigure another DUT as RPL Owner

        erpsflow.change_the_rpl_owner(erps1, erps2, group_id="1", new_rpl_port="gi 0/4")

        time.sleep(65)

        # ----- Asserting for DUT1 -----

        erpsflow.confirm_erps_configuration(erps1, group_id="1", configured_rpl_port="There is no RPL Port")

        # ----- Asserting for DUT2 -----

        erpsflow.confirm_erps_configuration(erps2, group_id="1", configured_rpl_port="gi 0/4")

        # ----- Asserting for DUT3 -----

        erpsflow.confirm_erps_configuration(erps3, group_id="1", configured_rpl_port="There is no RPL Port")

        #  STEP 8: Repeat STEP 7 for another DUT

        erpsflow.change_the_rpl_owner(erps2, erps3, group_id="1", new_rpl_port="gi 0/9")

        time.sleep(65)

        # ----- Asserting for DUT1 -----

        erpsflow.confirm_erps_configuration(erps1, group_id="1", configured_rpl_port="There is no RPL Port")

        # ----- Asserting for DUT2 -----

        erpsflow.confirm_erps_configuration(erps2, group_id="1", configured_rpl_port="There is no RPL Port")

        # ----- Asserting for DUT3 -----

        erpsflow.confirm_erps_configuration(erps3, group_id="1", configured_rpl_port="gi 0/9")

        # <<< REMOVING THE CONFIGURATION >>>

        erpsflow.removing_the_erps_configuration(int1, "Ex 0/1", "Gi 0/9", erps1, stp1, vl1, "3500")
        erpsflow.removing_the_erps_configuration(int2, "Gi 0/4", "Gi 0/9", erps2, stp2, vl2, "3500")
        erpsflow.removing_the_erps_configuration(int3, "Gi 0/4", "Gi 0/9", erps3, stp3, vl3, "3500")


