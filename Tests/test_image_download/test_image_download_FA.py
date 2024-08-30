import time
import pytest

from config import sanity

from Management import dut_objects
from flows import sanity_flow
from test_beds import test_bed_1
from mocks import mock_1

# mock_1 = mock_1.mocks_sanity
path = mock_1.paths
params = mock_1.mocks_sanity_fiber

dut1 = test_bed_1.DUT1
dut2 = test_bed_1.DUT2
dut3 = test_bed_1.DUT3
dut4 = test_bed_1.DUT4
dut5 = test_bed_1.DUT5
dut6 = test_bed_1.DUT6

DUT1 = dut_objects.DUT_Objects_TestBed(dut1)
DUT2 = dut_objects.DUT_Objects_TestBed(dut2)
DUT3 = dut_objects.DUT_Objects_TestBed(dut3)
DUT4 = dut_objects.DUT_Objects_TestBed(dut4)
DUT5 = dut_objects.DUT_Objects_TestBed(dut5)
DUT6 = dut_objects.DUT_Objects_TestBed(dut6)

sanity_flow_ = sanity_flow.SanityFlow()

class TestImageDownloadFA:

    def test_func_1(self):

        print("###### Test_func_1 ######")
        print("########## Check you can download a software image on DUT using TFTP using SSH #############")

        # Check that the new software version is downloaded successfully

        sanity_flow_.assert_download_image(DUT6,
                                           protocol=params["protocol"]["ssh"],
                                           mode=params["mode"]["tftp"],
                                           server_ip=params["server_ip"],
                                           img=params["image_version"]["image_to_upgrade"],
                                           path=params["path"]["DUT6"]["tftp"],
                                           platform=params["platform"],
                                           img_compression=params["image_compression"])

        # Make connection to the DUT, Reload it and check the new software version is loading successfully

        sanity_flow_.reload_DUT(DUT6, protocol=params["protocol"]["ssh"])

        # Check the new software version and model name of the DUT

        sanity_flow_.check_software_version_and_model(DUT6, img_to_be_checked=params["image_version_to_be_checked"]["image_to_upgrade"],
                                                            model=DUT6.model)

    def test_func_2(self):

        print("###### Test_func_2 ######")
        print("########## Check you can download a software image on DUT using SFTP using SSH #############")

        # Check that the new software version is downloaded successfully

        sanity_flow_.assert_download_image(DUT6,
                                           protocol=params["protocol"]["ssh"],
                                           mode=params["mode"]["sftp"],
                                           server_ip=params["server_ip"],
                                           img=params["image_version"]["image_to_downgrade"],
                                           path=params["path"]["DUT6"]["sftp"],
                                           platform=params["platform"],
                                           img_compression=params["image_compression"],
                                           user=params["user"],
                                           password=params["password"])

        # Make connection to the DUT, Reload it and check the new software version is loading successfully

        sanity_flow_.reload_DUT(DUT6, protocol=params["protocol"]["ssh"])

        # Check the new software version and model name of the DUT

        sanity_flow_.check_software_version_and_model(DUT6, img_to_be_checked=params["image_version_to_be_checked"]["image_to_downgrade"],
                                                            model=DUT6.model)

    def test_func_3(self):

        print("###### Test_func_3 ######")
        print("########## Check you can download a software image on DUT using TFTP using SSH #############")

        # Getting back to the last image so we can do the save/retrieve confing

        # Check that the new software version is downloaded successfully

        sanity_flow_.assert_download_image(DUT6,
                                           protocol=params["protocol"]["ssh"],
                                           mode=params["mode"]["tftp"],
                                           server_ip=params["server_ip"],
                                           img=params["image_version"]["image_to_upgrade"],
                                           path=params["path"]["DUT6"]["tftp"],
                                           platform=params["platform"],
                                           img_compression=params["image_compression"])

        # Make connection to the DUT, Reload it and check the new software version is loading successfully

        sanity_flow_.reload_DUT(DUT6, protocol=params["protocol"]["ssh"])

        # Check the new software version and model name of the DUT

        sanity_flow_.check_software_version_and_model(DUT6, img_to_be_checked=params["image_version_to_be_checked"]["image_to_upgrade"],
                                                            model=DUT6.model)

    def test_func_4(self):

        print("###### Test_func_4 ######")
        print("########## Check you can save/retrieve the startup-config on a remote server using TFTP using SSH #############")

        sanity_flow_.assert_copy_startup_config(DUT6,
                                                protocol=params["protocol"]["ssh"],
                                                mode=params["mode"]["tftp"],
                                                server_ip=params["server_ip"],
                                                vlan="3000",
                                                path=params["path"]["DUT6"]["tftp"])

    def test_func_5(self):

        print("###### Test_func_5 ######")
        print("########## Check you can save/retrieve the startup-config on a remote server using SFTP using SSH #############")

        sanity_flow_.assert_copy_startup_config(DUT6,
                                                protocol=params["protocol"]["ssh"],
                                                mode=params["mode"]["sftp"],
                                                server_ip=params["server_ip"],
                                                vlan="3000", path=params["path"]["DUT6"]["sftp"],
                                                user=params["user"],
                                                password=params["password"])