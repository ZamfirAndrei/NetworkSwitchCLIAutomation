import time
import pytest

from config import sanity

from Management import dut_objects
from flows import sanity_flow
from test_beds import test_bed_1
from mocks import mock_1

path = mock_1.paths
images = mock_1.images_fiber
params = mock_1.mocks_sanity_fiber

dut6 = test_bed_1.DUT6
dut3 = test_bed_1.DUT3

DUT6 = dut_objects.DUT_Objects_TestBed(dut6)
DUT3 = dut_objects.DUT_Objects_TestBed(dut3)

sanity_flow_ = sanity_flow.SanityFlow()


class TestSanitySuiteFA:

    def test_func_1(self):

        print("###### Test_func_1 ######")
        print("########## Check you can download a software image on DUT using TFTP using SSH - FA #############")

        # Check that the new software version is downloaded successfully

        sanity_flow_.assert_download_image(DUT6, protocol=params["protocol"]["ssh"], mode=params["mode"]["tftp"],
                                           server_ip=params["server_ip"], img=params["image_version"]["image_to_upgrade"],
                                           path=params["path"]["DUT6"]["tftp"], platform=params["platform"] ,
                                           img_compression=params["image_compression"])

        # Make connection to the DUT, Reload it and check the new software version is loading successfully

        sanity_flow_.save_and_reload_DUT(DUT6, protocol=params["protocol"]["ssh"])

        # Check the new software version and model name of the DUT

        sanity_flow_.check_software_version_and_model(DUT6, img_to_be_checked=params["image_version_to_be_checked"]["image_to_upgrade"],
                                                      model=DUT6.model)

    def test_func_2(self):

        print("###### Test_func_2 ######")
        print("########## Check you can download a software image on DUT using SFTP using SSH - FA #############")

        # Check that the new software version is downloaded successfully

        sanity_flow_.assert_download_image(DUT6, protocol=params["protocol"]["ssh"], mode=params["mode"]["sftp"],
                                           server_ip=params["server_ip"], img=params["image_version"]["image_to_downgrade"],
                                           path=params["path"]["DUT6"]["sftp"], platform=params["platform"] ,
                                           img_compression=params["image_compression"], user=params["user"],
                                           password=params["password"])

        # Make connection to the DUT, Reload it and check the new software version is loading successfully

        sanity_flow_.reload_DUT(DUT6, protocol=params["protocol"]["ssh"])

        # Check the new software version and model name of the DUT

        sanity_flow_.check_software_version_and_model(DUT6, img_to_be_checked=params["image_version_to_be_checked"]["image_to_downgrade"],
                                                      model=DUT6.model)

    @pytest.mark.skip(reason="scp not working")
    def test_func_3(self):

        print("###### Test_func_3 ######")
        print("########## Check you can download a software image on DUT using SCP using SSH - FA #############")

        # Need to find a way to avoid that press "Enter" in the password prompt

        # DUT6.sanity.download_image_ssh(mode="scp",server_ip="10.2.109.24", img="5.0.1-r4",user="cambium",password="cambium123", path="/tftpboot")

    def test_func_4(self):

        # Getting back to the last image, so we can do the save/retrieve confing

        print("###### Test_func_4 ######")
        print("########## Check you can download a software image on DUT using TFTP using SSH - FA #############")

        # Check that the new software version is downloaded successfully

        sanity_flow_.assert_download_image(DUT6,  protocol=params["protocol"]["ssh"], mode=params["mode"]["tftp"],
                                           server_ip=params["server_ip"], img=params["image_version"]["image_to_upgrade"],
                                           path=params["path"]["DUT6"]["tftp"], platform=params["platform"] ,
                                           img_compression=params["image_compression"])

        # Make connection to the DUT, Reload it and check the new software version is loading successfully

        sanity_flow_.reload_DUT(DUT6, protocol=params["protocol"]["ssh"])

        # Check the new software version and model name of the DUT

        sanity_flow_.check_software_version_and_model(DUT6, img_to_be_checked=params["image_version_to_be_checked"]["image_to_upgrade"],
                                                      model=DUT6.model)

    def test_func_5(self):

        print("###### Test_func_5 ######")
        print("########## Check you can save/retrieve the startup-config on a remote server using TFTP using SSH - FA #############")

        sanity_flow_.assert_copy_startup_config(DUT6, protocol=params["protocol"]["ssh"], mode=params["mode"]["tftp"], server_ip=params["server_ip"], vlan="1000",
                                                path=params["path"]["DUT6"]["tftp"])

    def test_func_6(self):

        print("###### Test_func_6 ######")
        print("########## Check you can save/retrieve the startup-config on a remote server using SFTP using SSH - FA #############")

        sanity_flow_.assert_copy_startup_config(DUT6, protocol=params["protocol"]["ssh"], mode=params["mode"]["sftp"], server_ip=params["server_ip"], vlan="1000",
                                                path=params["path"]["DUT6"]["sftp"], user=params["user"], password=params["password"])

    # @pytest.mark.skip(reason="Telnet not working")
    def test_func_7(self):

        print("###### Test_func_7 ######")
        print("########## Check you can download a software image on DUT using TFTP using Telnet - FA #############")

        # Check that the new software version is downloaded successfully

        sanity_flow_.assert_download_image(DUT6, protocol=params["protocol"]["telnet"], mode=params["mode"]["tftp"],
                                           server_ip=params["server_ip"], img=params["image_version"]["image_to_downgrade"],
                                           path=params["path"]["DUT6"]["tftp"], platform=params["platform"] ,
                                           img_compression=params["image_compression"])

        # Make connection to the DUT, Reload it and check the new software version is loading successfully

        sanity_flow_.reload_DUT(DUT6, protocol=params["protocol"]["telnet"])

        # Check the new software version and model name of the DUT

        sanity_flow_.check_software_version_and_model(DUT6, img_to_be_checked=params["image_version_to_be_checked"][
            "image_to_downgrade"], model=DUT6.model)


    # @pytest.mark.skip(reason="Telnet not working")
    def test_func_8(self):

        print("###### Test_func_8 ######")
        print("########## Check you can download a software image on DUT using SFTP using Telnet - FA #############")

        # Check that the new software version is downloaded successfully

        sanity_flow_.assert_download_image(DUT6, protocol=params["protocol"]["telnet"], mode=params["mode"]["sftp"],
                                           server_ip=params["server_ip"],  img=params["image_version"]["image_to_upgrade"],
                                           path=params["path"]["DUT6"]["sftp"], user=params["user"], password=params["password"],
                                           platform=params["platform"], img_compression=params["image_compression"])

        # Make connection to the DUT, Reload it and check the new software version is loading successfully

        sanity_flow_.reload_DUT(DUT6, protocol=params["protocol"]["telnet"])

        # Check the new software version and model name of the DUT

        sanity_flow_.check_software_version_and_model(DUT6, img_to_be_checked=params["image_version_to_be_checked"][
            "image_to_upgrade"], model=DUT6.model)

    @pytest.mark.skip(reason="scp not working")
    def test_func_9(self):

        print("###### Test_func_9 ######")
        print("########## Check you can download a software image on DUT using SCP using telnet - FA #############")

        # Need to find a way to avoid that press "Enter" in the password prompt

        # DUT6.sanity.download_image_ssh(mode="scp",server_ip="10.2.109.24", img="5.0.1-r4",user="cambium",password="cambium123", path="/tftpboot")

    # @pytest.mark.skip(reason="Telnet not working")
    def test_func_10(self):

        print("###### Test_func_10 ######")
        print("########## Check you can save/retrieve the startup-config on a remote server using TFTP using Telnet - FA #############")

        sanity_flow_.assert_copy_startup_config(DUT6, protocol=params["protocol"]["telnet"],
                                                mode=params["mode"]["tftp"], server_ip=params["server_ip"],
                                                vlan="1000", path=params["path"]["DUT6"]["tftp"])

    # @pytest.mark.skip(reason="Telnet not working")
    def test_func_11(self):

        print("###### Test_func_11 ######")
        print("########## Check you can save/retrieve the startup-config on a remote server using SFTP using Telnet - FA #############")

        sanity_flow_.assert_copy_startup_config(DUT6, protocol=params["protocol"]["telnet"],
                                                mode=params["mode"]["sftp"], server_ip=params["server_ip"],
                                                vlan="1000", path=params["path"]["DUT6"]["sftp"], user=params["user"],
                                                password=params["password"])

    def test_func_12(self):

        print("###### Test_func_12 ######")
        print("########## Verify a configuration made on a port is available after downloading new image using SSH - FA #############")

        # Make the configuration for the port

        sanity_flow_.port_configuration(DUT6, port="Ex 0/4", port_mode="Trunk", pvid="15", acceptable_frame_type="tagged")

        # Check the port configuration BEFORE downloading the new software image

        sanity_flow_.assert_configuration_port(DUT6, port="Ex 0/4", port_mode="Trunk", pvid="15", acceptable_frame_type="tagged",
                                               img_to_be_checked=params["image_version_to_be_checked"]["image_to_upgrade"], model=DUT6.model)

        # Save the configuration and download the new image

        sanity_flow_.save_configuration(DUT6, protocol=params["protocol"]["ssh"])
        sanity_flow_.assert_download_image(DUT6, protocol=params["protocol"]["ssh"], mode=params["mode"]["tftp"],
                                           server_ip=params["server_ip"], img=params["image_version"]["image_to_downgrade"],
                                           path=params["path"]["DUT6"]["tftp"], platform=params["platform"] ,
                                           img_compression=params["image_compression"], user=params["user"],
                                           password=params["password"])

        # Reload the DUT

        sanity_flow_.reload_DUT(DUT6, protocol=params["protocol"]["ssh"])

        # Check the port configuration AFTER downloading the new software image

        sanity_flow_.assert_configuration_port(DUT6, port="Ex 0/4", port_mode="Trunk", pvid="15", acceptable_frame_type="tagged",
                                               img_to_be_checked=params["image_version_to_be_checked"]["image_to_downgrade"], model=DUT6.model)

        # Remove the port configuration and save

        sanity_flow_.remove_port_configuration(DUT6, port="Ex 0/4")
        sanity_flow_.save_configuration(DUT6, protocol=params["protocol"]["ssh"])

        # Check the port configuration

        sanity_flow_.assert_configuration_port(DUT6, port="Ex 0/4", port_mode="Hybrid", pvid="1", acceptable_frame_type="all", img_to_be_checked=params["image_version_to_be_checked"]["image_to_downgrade"],
                                              model=DUT6.model)

        # Remove the VLAN configured

        DUT6.vl.remove_vlan(vlan="15")


    # @pytest.mark.skip(reason="Telnet not working")
    def test_func_13(self):

        print("###### Test_func_13 ######")
        print("########## Verify a configuration made on a port is available after downloading new image using Telnet - FA #############")

        # Make the configuration for the port

        sanity_flow_.port_configuration(DUT6, port="Ex 0/4", port_mode="Hybrid", pvid="10",
                                        acceptable_frame_type="untagged")

        # Check the port configuration BEFORE downloading the new software image

        sanity_flow_.assert_configuration_port(DUT6, port="Ex 0/4", port_mode="Hybrid", pvid="10",
                                               acceptable_frame_type="untagged", img_to_be_checked=params["image_version_to_be_checked"]["image_to_downgrade"],
                                               model=DUT6.model)

        # Save the configuration and download the new image

        sanity_flow_.save_configuration(DUT6, protocol=params["protocol"]["telnet"])
        sanity_flow_.assert_download_image(DUT6, protocol=params["protocol"]["telnet"], mode=params["mode"]["tftp"],
                                           server_ip=params["server_ip"], img=params["image_version"]["image_to_upgrade"],
                                           path=params["path"]["DUT6"]["tftp"], platform=params["platform"],
                                           img_compression=params["image_compression"], user=params["user"],
                                           password=params["password"])

        # Reload the DUT

        sanity_flow_.reload_DUT(DUT6, protocol=params["protocol"]["telnet"])

        # Check the port configuration AFTER downloading the new software image

        sanity_flow_.assert_configuration_port(DUT6, port="Ex 0/4", port_mode="Hybrid", pvid="10",
                                               acceptable_frame_type="untagged",
                                               img_to_be_checked=params["image_version_to_be_checked"]["image_to_upgrade"],
                                               model=DUT6.model)

        # Remove the port configuration and save

        sanity_flow_.remove_port_configuration(DUT6, port="Ex 0/4")
        sanity_flow_.save_configuration(DUT6, protocol=params["protocol"]["telnet"])

        # Check the port configuration

        sanity_flow_.assert_configuration_port(DUT6, port="Ex 0/4", port_mode="Hybrid", pvid="1",
                                               acceptable_frame_type="all",
                                               img_to_be_checked=params["image_version_to_be_checked"]["image_to_upgrade"],
                                               model=DUT6.model)

        # Remove the VLAN configured

        DUT6.vl.remove_vlan(vlan="10")
