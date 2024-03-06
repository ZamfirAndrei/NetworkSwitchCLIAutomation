import time
import pytest

from config import sanity

from Management import dut_objects
from flows import sanity_flow
from test_beds import test_bed_1
from mocks import mock_1

path = mock_1.paths

dut6 = test_bed_1.DUT6
dut3 = test_bed_1.DUT3

DUT6 = dut_objects.DUT_Objects_TestBed(dut6)
DUT3 = dut_objects.DUT_Objects_TestBed(dut3)

sanity_flow_ = sanity_flow.SanityFlow()

image_to_update = "6.0.0-e56"
image_to_downgrade = "6.0.0-e54"

image_to_be_checked_1 = "6.0.0-e56"
image_to_be_checked_2 = "6.0.0-e54"

server_ip = "10.2.109.24"
user = "cambium"
password = "cambium123"


paths_dut6 = {
    "tftp": "/AGZamfir/3024F.conf",
    "sftp": "/AGZamfir/sftp_3024F.conf"
}

paths = {
    "DUT6": paths_dut6
}

class TestSanitySuiteFA:

    def test_func_123(self):

        print(paths)
        print(DUT6.model)
        print(paths['DUT6']['tftp'])
        print(paths['DUT6']['sftp'])
    def test_func_1(self):

        print("###### Test_func_1 ######")
        print("########## Check you can download a software image on DUT using TFTP using SSH - FA #############")

        # Check that the new software version is downloaded successfully

        sanity_flow_.assert_download_image(DUT6, "ssh", "tftp", server_ip, image_to_update, paths['DUT6']['tftp'],"EX3Kext", "itb")

        # Make connection to the DUT, Reload it and check the new software version is loading successfully

        sanity_flow_.reload_DUT(DUT6, "ssh")

        # Check the new software version and model name of the DUT

        sanity_flow_.check_software_version_and_model(DUT6, image_to_be_checked_1, DUT6.model)

    def test_func_2(self):

        print("###### Test_func_2 ######")
        print("########## Check you can download a software image on DUT using SFTP using SSH - FA #############")

        # Check that the new software version is downloaded successfully

        sanity_flow_.assert_download_image(DUT6, "ssh", "sftp", server_ip, image_to_downgrade,
                                           paths['DUT6']['sftp'], "EX3Kext" , "itb", user=user, password=password)

        # Make connection to the DUT, Reload it and check the new software version is loading successfully

        sanity_flow_.reload_DUT(DUT6, "ssh")

        # Check the new software version and model name of the DUT

        sanity_flow_.check_software_version_and_model(DUT6, image_to_be_checked_2, DUT6.model)

    # def test_func_3(self):
    #
    #     print("###### Test_func_3 ######")
    #     print("########## Check you can download a software image on DUT using SCP using SSH - FA #############")
    #
    #     # Need to find a way to avoid that press "Enter" in the password prompt
    #
    #     # DUT6.sanity.download_image_ssh(mode="scp",server_ip="10.2.109.24", img="5.0.1-r4",user="cambium",password="cambium123", path="/tftpboot")
    #
    def test_func_4(self):

        # Getting back to the last image so we can do the save/retrieve confing

        print("###### Test_func_4 ######")
        print("########## Check you can download a software image on DUT using TFTP using SSH - FA #############")

        # Check that the new software version is downloaded successfully

        sanity_flow_.assert_download_image(DUT6, "ssh", "tftp", server_ip, image_to_update, paths["DUT6"]["tftp"],"EX3Kext", "itb")

        # Make connection to the DUT, Reload it and check the new software version is loading successfully

        sanity_flow_.reload_DUT(DUT6, "ssh")

        # Check the new software version and model name of the DUT

        sanity_flow_.check_software_version_and_model(DUT6, image_to_be_checked_1, DUT6.model)

    def test_func_5(self):

        print("###### Test_func_5 ######")
        print("########## Check you can save/retrieve the startup-config on a remote server using TFTP using SSH - FA #############")

        sanity_flow_.assert_copy_startup_config(DUT6, "ssh", "tftp", server_ip, "1000",
                                                paths["DUT6"]["tftp"])

    def test_func_6(self):

        print("###### Test_func_6 ######")
        print("########## Check you can save/retrieve the startup-config on a remote server using SFTP using SSH - FA #############")

        sanity_flow_.assert_copy_startup_config(DUT6, "ssh", "sftp", server_ip, "1000",
                                                paths["DUT6"]["sftp"], user, password)
    def test_func_7(self):

        print("###### Test_func_7 ######")
        print("########## Check you can download a software image on DUT using TFTP using Telnet - FA #############")

        # Check that the new software version is downloaded successfully

        sanity_flow_.assert_download_image(DUT6, "telnet", "tftp", server_ip, image_to_downgrade, paths['DUT6']['tftp'], "EX3Kext", "itb")

        # Make connection to the DUT, Reload it and check the new software version is loading successfully

        sanity_flow_.reload_DUT(DUT6, "telnet")

        # Check the new software version and model name of the DUT

        sanity_flow_.check_software_version_and_model(DUT6, image_to_be_checked_2, DUT6.model)

    def test_func_34(self):

        print("###### Test_func_34 ######")
        print("########## Check you can download a software image on DUT using SFTP using Telnet - FA #############")

        # Check that the new software version is downloaded successfully

        sanity_flow_.assert_download_image(DUT6, "telnet", "sftp", server_ip, image_to_update, paths['DUT6']['sftp'], "EX3Kext" , "itb",
                                           user=user, password=password)

        # Make connection to the DUT, Reload it and check the new software version is loading successfully

        sanity_flow_.reload_DUT(DUT6, "telnet")

        # Check the new software version and model name of the DUT

        sanity_flow_.check_software_version_and_model(DUT6, image_to_be_checked_1, DUT6.model)