import time
import pytest

from config import sanity

from Management import dut_objects
from flows import sanity_flow
from test_beds import test_bed_1
from mocks import mock_1

mock_1 = mock_1.mocks_sanity

ip_session_1 = "10.2.109.206"
ip_session_2 = "10.2.109.83"
ip_session_3 = "10.2.109.98"

dut1 = test_bed_1.DUT1
dut2 = test_bed_1.DUT2
dut3 = test_bed_1.DUT3

DUT1 = dut_objects.DUT_Objects(ip_session=ip_session_1)
DUT2 = dut_objects.DUT_Objects(ip_session=ip_session_2)
DUT3 = dut_objects.DUT_Objects(ip_session=ip_session_3)

_DUT1 = dut_objects.DUT_Objects_TestBed(dut1)
_DUT2 = dut_objects.DUT_Objects_TestBed(dut2)
_DUT3 = dut_objects.DUT_Objects_TestBed(dut3)


sanity_flow_ = sanity_flow.SanityFlow()

class TestSanitySuite2:

    def test_func_1(self):

        print("###### Test_func_1 ######")
        print("########## Check you can download a software image on DUT using TFTP using SSH #############")

        # Check that the new software version is downloaded successfully

        sanity_flow_.assert_download_image(DUT1, "ssh", "tftp", "10.2.109.24", "5.0.2-r3","/AGZamfir/Andrei-2028.conf")

        # Make connection to the DUT, Reload it and check the new software version is loading successfully

        sanity_flow_.reload_DUT(DUT1, "ssh")

        # Check the new software version and model name of the DUT

        sanity_flow_.check_software_version_and_model(DUT1, "5.0.2-r3", dut1['model'])

    def test_func_2(self):

        print("###### Test_func_2 ######")
        print("########## Check you can download a software image on DUT using SFTP using SSH #############")

        # Check that the new software version is downloaded successfully

        sanity_flow_.assert_download_image(_DUT1, "ssh", "sftp", "10.2.109.24", "5.0.2-r2", "/AGZamfir/Andrei-2028.conf", "cambium", "cambium123")

        # Make connection to the DUT, Reload it and check the new software version is loading successfully

        sanity_flow_.reload_DUT(_DUT1, "ssh")

        # Check the new software version and model name of the DUT

        sanity_flow_.check_software_version_and_model(_DUT1, "5.0.2-r2", _DUT1.model)

    # def test_func_3(self):
    #
    #     print("###### Test_func_3 ######")
    #     print("########## Check you can download a software image on DUT using SCP using SSH #############")
    #
    #     # Need to find a way to avoid that press "Enter" in the password prompt
    #
    #     # DUT1.sanity.download_image_ssh(mode="scp",server_ip="10.2.109.24", img="5.0.1-r4",user="cambium",password="cambium123", path="/tftpboot")
    #
    def test_func_4(self):

        print("###### Test_func_4 ######")
        print("########## Check you can save/retrieve the startup-config on a remote server using TFTP using SSH #############")

        sanity_flow_.assert_copy_startup_config(DUT1, "ssh", "tftp", "10.2.109.24", "3000", "/AGZamfir/Andrei-2028.conf")

    def test_func_5(self):

        print("###### Test_func_5 ######")
        print("########## Check you can save/retrieve the startup-config on a remote server using SFTP using SSH #############")

        sanity_flow_.assert_copy_startup_config(DUT1, "ssh", "sftp", "10.2.109.24", "3000", "/AGZamfir/Andrei-2028.conf", "cambium", "cambium123")

    def test_func_6(self):

        print("###### Test_func_6 ######")
        print("########## Check you can download a software image on DUT using TFTP using Telnet #############")

        # Check that the new software version is downloaded successfully

        sanity_flow_.assert_download_image(DUT1, "telnet", "tftp", "10.2.109.24", "5.0.2-r3", "/AGZamfir/Andrei-2028.conf")

        # Make connection to the DUT, Reload it and check the new software version is loading successfully

        sanity_flow_.reload_DUT(DUT1, "telnet")

        # Check the new software version and model name of the DUT

        sanity_flow_.check_software_version_and_model(DUT1, "5.0.2-r3", "EX2028-P")

    def test_func_7(self):

        print("###### Test_func_7 ######")
        print("########## Check you can download a software image on DUT using SFTP using Telnet #############")

        # Check that the new software version is downloaded succesfully

        sanity_flow_.assert_download_image(DUT1, "telnet", "sftp", "10.2.109.24", "5.1.0-e8", "/AGZamfir/Andrei-2028.conf",
                                           "cambium", "cambium123")

        # Make connection to the DUT, Reload it and check the new software version is loading successfully

        sanity_flow_.reload_DUT(DUT1, "telnet")

        # Check the new software version and model name of the DUT

        sanity_flow_.check_software_version_and_model(DUT1, "5.1.0-e8", "EX2028-P")

    # def test_func_8(self):
    #
    #     print("###### Test_func_8 ######")
    #     print("########## Check you can download a software image on DUT using SCP using telnet #############")
    #
    #     # Need to find a way to avoid that press "Enter" in the password prompt
    #
    #     # DUT1.sanity.download_image_ssh(mode="scp",server_ip="10.2.109.24", img="5.0.1-r4",user="cambium",password="cambium123", path="/tftpboot")

    def test_func_9(self):

        print("###### Test_func_9 ######")
        print("########## Check you can save/retrieve the startup-config on a remote server using TFTP using Telnet #############")

        sanity_flow_.assert_copy_startup_config(DUT1, "telnet", "tftp", "10.2.109.24", "3000",
                                                "/AGZamfir/Andrei-2028.conf")

    def test_func_10(self):

        print("###### Test_func_10 ######")
        print("########## Check you can save/retrieve the startup-config on a remote server using SFTP using Telnet #############")

        sanity_flow_.assert_copy_startup_config(DUT1, "telnet", "sftp", "10.2.109.24", "3000", "/AGZamfir/Andrei-2028.conf", "cambium", "cambium123")

    def test_func_11(self):

        print("###### Test_func_11 ######")
        print("########## Verify a configuration made on a port is available after downloading new image using SSH #############")

        # Make the configuration for the port

        sanity_flow_.port_configuration(DUT1, "Gi 0/4", "Trunk", "15","tagged")

        # Check the port configuration BEFORE downloading the new software image

        sanity_flow_.assert_configuration_port(DUT1, "Gi 0/4", "Trunk", "15","tagged","5.1.0-e8", "EX2028-P")

        # Save the configuration and download the new image

        sanity_flow_.save_configuration(DUT1, "ssh")
        sanity_flow_.assert_download_image(DUT1, "ssh", "tftp", "10.2.109.24", "5.0.2-r3","/AGZamfir/Andrei-2028.conf")

        # Reload the DUT

        sanity_flow_.reload_DUT(DUT1, "ssh")

        # Check the port configuration AFTER downloading the new software image

        sanity_flow_.assert_configuration_port(DUT1, "Gi 0/4", "Trunk", "15", "tagged", "5.0.2-r3", "EX2028-P")

    def test_func_12(self):

        print("###### Test_func_12 ######")
        print("########## Verify a configuration made on a port is available after downloading new image using Telnet #############")

        # Make the configuration for the port

        sanity_flow_.port_configuration(DUT1, "Gi 0/4", "Hybrid", "10","untagged")

        # Check the port configuration BEFORE downloading the new software image

        sanity_flow_.assert_configuration_port(DUT1, "Gi 0/4", "Hybrid", "10","untagged","5.0.2-r3", "EX2028-P")

        # Save the configuration and download the new image

        sanity_flow_.save_configuration(DUT1, "telnet")
        sanity_flow_.assert_download_image(DUT1, "telnet", "tftp", "10.2.109.24", "5.1.0-e8","/AGZamfir/Andrei-2028.conf")

        # Reload the DUT

        sanity_flow_.reload_DUT(DUT1, "telnet")

        # Check the port configuration AFTER downloading the new software image

        sanity_flow_.assert_configuration_port(DUT1, "Gi 0/4", "Hybrid", "10", "untagged", "5.1.0-e8", "EX2028-P")