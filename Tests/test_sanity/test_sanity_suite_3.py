import time
import pytest

from config import sanity

from Management import dut_objects
from flows import sanity_flow
from test_beds import test_bed_1
from mocks import mock_1

# mock_1 = mock_1.mocks_sanity
path = mock_1.paths
params = mock_1.mocks_sanity_legacy

dut1 = test_bed_1.DUT1
dut2 = test_bed_1.DUT2
dut3 = test_bed_1.DUT3

DUT1 = dut_objects.DUT_Objects_TestBed(dut1)
DUT2 = dut_objects.DUT_Objects_TestBed(dut2)
DUT3 = dut_objects.DUT_Objects_TestBed(dut3)


sanity_flow_ = sanity_flow.SanityFlow()


class TestSanitySuite3:

    def test_func_1(self):

        print("###### Test_func_1 ######")
        print("########## Check you can download a software image on DUT using TFTP using SSH #############")

        # Check that the new software version is downloaded successfully

        sanity_flow_.assert_download_image(DUT1,
                                           protocol=params["protocol"]["ssh"],
                                           mode=params["mode"]["tftp"],
                                           server_ip=params["server_ip"],
                                           img=params["image_version"]["image_to_upgrade"],
                                           path=params["path"]["DUT1"]["tftp"])

        # Make connection to the DUT, Reload it and check the new software version is loading successfully

        sanity_flow_.reload_DUT(DUT1, protocol=params["protocol"]["ssh"])

        # Check the new software version and model name of the DUT

        sanity_flow_.check_software_version_and_model(DUT1, img_to_be_checked=params["image_version_to_be_checked"]["image_to_upgrade"],
                                                            model=DUT1.model)

    def test_func_2(self):

        print("###### Test_func_2 ######")
        print("########## Check you can download a software image on DUT using SFTP using SSH #############")

        # Check that the new software version is downloaded successfully

        sanity_flow_.assert_download_image(DUT1,
                                           protocol=params["protocol"]["ssh"],
                                           mode=params["mode"]["sftp"],
                                           server_ip=params["server_ip"],
                                           img=params["image_version"]["image_to_downgrade"],
                                           path=params["path"]["DUT1"]["sftp"],
                                           user=params["user"],
                                           password=params["password"])

        # Make connection to the DUT, Reload it and check the new software version is loading successfully

        sanity_flow_.reload_DUT(DUT1, protocol=params["protocol"]["ssh"])

        # Check the new software version and model name of the DUT

        sanity_flow_.check_software_version_and_model(DUT1, img_to_be_checked=params["image_version_to_be_checked"]["image_to_downgrade"],
                                                            model=DUT1.model)

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
        print("########## Check you can download a software image on DUT using TFTP using SSH #############")

        # Getting back to the last image so we can do the save/retrieve confing

        # Check that the new software version is downloaded successfully

        sanity_flow_.assert_download_image(DUT1,
                                           protocol=params["protocol"]["ssh"],
                                           mode=params["mode"]["tftp"],
                                           server_ip=params["server_ip"],
                                           img=params["image_version"]["image_to_upgrade"],
                                           path=params["path"]["DUT1"]["tftp"])

        # Make connection to the DUT, Reload it and check the new software version is loading successfully

        sanity_flow_.reload_DUT(DUT1, protocol=params["protocol"]["ssh"])

        # Check the new software version and model name of the DUT

        sanity_flow_.check_software_version_and_model(DUT1, img_to_be_checked=params["image_version_to_be_checked"]["image_to_upgrade"],
                                                            model=DUT1.model)

    def test_func_5(self):

        print("###### Test_func_5 ######")
        print("########## Check you can save/retrieve the startup-config on a remote server using TFTP using SSH #############")

        sanity_flow_.assert_copy_startup_config(DUT1,
                                                protocol=params["protocol"]["ssh"],
                                                mode=params["mode"]["tftp"],
                                                server_ip=params["server_ip"],
                                                vlan="3000",
                                                path=params["path"]["DUT1"]["tftp"])

    def test_func_6(self):

        print("###### Test_func_6 ######")
        print("########## Check you can save/retrieve the startup-config on a remote server using SFTP using SSH #############")

        sanity_flow_.assert_copy_startup_config(DUT1,
                                                protocol=params["protocol"]["ssh"],
                                                mode=params["mode"]["sftp"],
                                                server_ip=params["server_ip"],
                                                vlan="3000", path=params["path"]["DUT1"]["sftp"],
                                                user=params["user"],
                                                password=params["password"])

    def test_func_7(self):

        print("###### Test_func_7 ######")
        print("########## Check you can download a software image on DUT using TFTP using Telnet #############")

        # Check that the new software version is downloaded successfully

        sanity_flow_.assert_download_image(DUT1,
                                           protocol=params["protocol"]["telnet"],
                                           mode=params["mode"]["tftp"],
                                           server_ip=params["server_ip"],
                                           img=params["image_version"]["image_to_downgrade"],
                                           path=params["path"]["DUT1"]["tftp"])

        # Make connection to the DUT, Reload it and check the new software version is loading successfully

        sanity_flow_.reload_DUT(DUT1, protocol=params["protocol"]["telnet"])

        # Check the new software version and model name of the DUT

        sanity_flow_.check_software_version_and_model(DUT1, img_to_be_checked=params["image_version_to_be_checked"]["image_to_downgrade"], model=DUT1.model)

    def test_func_8(self):

        print("###### Test_func_8 ######")
        print("########## Check you can download a software image on DUT using SFTP using Telnet #############")

        # Check that the new software version is downloaded successfully

        sanity_flow_.assert_download_image(DUT1,
                                           protocol=params["protocol"]["telnet"],
                                           mode=params["mode"]["sftp"],
                                           server_ip=params["server_ip"],
                                           img=params["image_version"]["image_to_upgrade"],
                                           path=params["path"]["DUT1"]["sftp"],
                                           user=params["user"],
                                           password=params["password"])

        # Make connection to the DUT, Reload it and check the new software version is loading successfully

        sanity_flow_.reload_DUT(DUT1, protocol=params["protocol"]["telnet"])

        # Check the new software version and model name of the DUT

        sanity_flow_.check_software_version_and_model(DUT1, img_to_be_checked=params["image_version_to_be_checked"]["image_to_upgrade"],
                                                            model=DUT1.model)

    @pytest.mark.skip(reason="scp not working")
    def test_func_9(self):

        print("###### Test_func_9 ######")
        print("########## Check you can download a software image on DUT using SCP using telnet #############")

        # Need to find a way to avoid that press "Enter" in the password prompt

        # DUT1.sanity.download_image_ssh(mode="scp",server_ip="10.2.109.24", img="5.0.1-r4",user="cambium",password="cambium123", path="/tftpboot")

    def test_func_10(self):

        print("###### Test_func_10 ######")
        print("########## Check you can save/retrieve the startup-config on a remote server using TFTP using Telnet #############")

        sanity_flow_.assert_copy_startup_config(DUT1,
                                                protocol=params["protocol"]["telnet"],
                                                mode=params["mode"]["tftp"],
                                                server_ip=params["server_ip"],
                                                vlan="3000",
                                                path=params["path"]["DUT1"]["tftp"])

    def test_func_11(self):

        print("###### Test_func_11 ######")
        print("########## Check you can save/retrieve the startup-config on a remote server using SFTP using Telnet #############")

        sanity_flow_.assert_copy_startup_config(DUT1,
                                                protocol=params["protocol"]["telnet"],
                                                mode=params["mode"]["sftp"],
                                                server_ip=params["server_ip"],
                                                vlan="3000",
                                                path=params["path"]["DUT1"]["sftp"],
                                                user=params["user"],
                                                password=params["password"])

    def test_func_12(self):

        print("###### Test_func_12 ######")
        print("########## Verify a configuration made on a port is available after downloading new image using SSH #############")

        # Make the configuration for the port

        sanity_flow_.port_configuration(DUT1,
                                        port="Gi 0/4",
                                        port_mode="Trunk",
                                        pvid="15",
                                        acceptable_frame_type="tagged")

        # Check the port configuration BEFORE downloading the new software image

        sanity_flow_.assert_configuration_port(DUT1,
                                               port="Gi 0/4",
                                               port_mode="Trunk",
                                               pvid="15",
                                               acceptable_frame_type="tagged",
                                               img_to_be_checked=params["image_version_to_be_checked"]["image_to_upgrade"],
                                               model=DUT1.model)

        # Save the configuration and download the new image

        sanity_flow_.save_configuration(DUT1, protocol=params["protocol"]["ssh"])
        sanity_flow_.assert_download_image(DUT1,
                                           protocol=params["protocol"]["ssh"],
                                           mode=params["mode"]["tftp"],
                                           server_ip=params["server_ip"],
                                           img=params["image_version"]["image_to_downgrade"],
                                           path=params["path"]["DUT1"]["tftp"],
                                           platform=params["platform"],
                                           img_compression=params["image_compression"],
                                           user=params["user"],
                                           password=params["password"])

        # Reload the DUT

        sanity_flow_.reload_DUT(DUT1, protocol=params["protocol"]["ssh"])

        # Check the port configuration AFTER downloading the new software image

        sanity_flow_.assert_configuration_port(DUT1,
                                               port="Gi 0/4",
                                               port_mode="Trunk",
                                               pvid="15",
                                               acceptable_frame_type="tagged",
                                               img_to_be_checked=params["image_version_to_be_checked"]["image_to_downgrade"],
                                               model=DUT1.model)

        # Remove the port configuration and save

        sanity_flow_.remove_port_configuration(DUT1, port="Gi 0/4")
        sanity_flow_.save_configuration(DUT1, protocol=params["protocol"]["ssh"])

        # Check the port configuration

        sanity_flow_.assert_configuration_port(DUT1,
                                               port="Gi 0/4",
                                               port_mode="Hybrid",
                                               pvid="1",
                                               acceptable_frame_type="all",
                                               img_to_be_checked=params["image_version_to_be_checked"]["image_to_downgrade"],
                                               model=DUT1.model)

        # Remove the VLAN configured

        DUT1.vl.remove_vlan(vlan="15")

    def test_func_13(self):

        print("###### Test_func_13 ######")
        print("########## Verify a configuration made on a port is available after downloading new image using Telnet #############")

        # Make the configuration for the port

        sanity_flow_.port_configuration(DUT1,
                                        port="Gi 0/4",
                                        port_mode="Hybrid",
                                        pvid="10",
                                        acceptable_frame_type="untagged")

        # Check the port configuration BEFORE downloading the new software image

        sanity_flow_.assert_configuration_port(DUT1,
                                               port="Gi 0/4",
                                               port_mode="Hybrid",
                                               pvid="10",
                                               acceptable_frame_type="untagged",
                                               img_to_be_checked=params["image_version_to_be_checked"]["image_to_downgrade"],
                                               model=DUT1.model)

        # Save the configuration and download the new image

        sanity_flow_.save_configuration(DUT1, protocol=params["protocol"]["telnet"])
        sanity_flow_.assert_download_image(DUT1,
                                           protocol=params["protocol"]["telnet"],
                                           mode=params["mode"]["tftp"],
                                           server_ip=params["server_ip"],
                                           img=params["image_version"]["image_to_upgrade"],
                                           path=params["path"]["DUT1"]["tftp"],
                                           platform=params["platform"],
                                           img_compression=params["image_compression"],
                                           user=params["user"],
                                           password=params["password"])

        # Reload the DUT

        sanity_flow_.reload_DUT(DUT1, protocol=params["protocol"]["telnet"])

        # Check the port configuration AFTER downloading the new software image

        sanity_flow_.assert_configuration_port(DUT1,
                                               port="Gi 0/4",
                                               port_mode="Hybrid",
                                               pvid="10",
                                               acceptable_frame_type="untagged",
                                               img_to_be_checked=params["image_version_to_be_checked"]["image_to_upgrade"],
                                               model=DUT1.model)

        # Remove the port configuration and save

        sanity_flow_.remove_port_configuration(DUT1, port="Gi 0/4")
        sanity_flow_.save_configuration(DUT1, protocol=params["protocol"]["telnet"])

        # Check the port configuration

        sanity_flow_.assert_configuration_port(DUT1,
                                               port="Gi 0/4",
                                               port_mode="Hybrid",
                                               pvid="1",
                                               acceptable_frame_type="all",
                                               img_to_be_checked=params["image_version_to_be_checked"]["image_to_upgrade"],
                                               model=DUT1.model)

        # Remove the VLAN configured

        DUT1.vl.remove_vlan(vlan="10")


    def test_func_14(self):

        print("###### Test_func_14 ######")
        print("########## Check you can download a software image on DUT using TFTP using SSH - EX2010-P #############")

        # Check that the new software version is downloaded successfully

        sanity_flow_.assert_download_image(DUT2,
                                           protocol=params["protocol"]["ssh"],
                                           mode=params["mode"]["tftp"],
                                           server_ip=params["server_ip"],
                                           img=params["image_version"]["image_to_upgrade"],
                                           path=params["path"]["DUT2"]["tftp"])

        # Make connection to the DUT, Reload it and check the new software version is loading successfully

        sanity_flow_.reload_DUT(DUT2, protocol=params["protocol"]["ssh"])

        # Check the new software version and model name of the DUT

        sanity_flow_.check_software_version_and_model(DUT2,
                                                      img_to_be_checked=params["image_version_to_be_checked"]["image_to_upgrade"],
                                                      model=DUT2.model)


    def test_func_15(self):

        print("###### Test_func_15 ######")
        print("########## Check you can download a software image on DUT using SFTP using SSH - EX2010-P #############")

        # Check that the new software version is downloaded successfully

        sanity_flow_.assert_download_image(DUT2,
                                           protocol=params["protocol"]["ssh"],
                                           mode=params["mode"]["sftp"],
                                           server_ip=params["server_ip"],
                                           img=params["image_version"]["image_to_downgrade"],
                                           path=params["path"]["DUT2"]["sftp"],
                                           user=params["user"],
                                           password=params["password"])

        # Make connection to the DUT, Reload it and check the new software version is loading successfully

        sanity_flow_.reload_DUT(DUT2, protocol=params["protocol"]["ssh"])

        # Check the new software version and model name of the DUT

        sanity_flow_.check_software_version_and_model(DUT2,
                                                      img_to_be_checked=params["image_version_to_be_checked"]["image_to_downgrade"],
                                                      model=DUT2.model)

    @pytest.mark.skip(reason="scp not working")
    def test_func_16(self):

        print("###### Test_func_16 ######")
        print("########## Check you can download a software image on DUT using SCP using SSH - EX2010-P #############")

        # Need to find a way to avoid that press "Enter" in the password prompt

        # DUT2.sanity.download_image_ssh(mode="scp",server_ip="10.2.109.24", img="5.0.1-r4",user="cambium",password="cambium123", path="/tftpboot")


    def test_func_17(self):

        # Getting back to the last image so we can do the save/retrieve confing

        # Check that the new software version is downloaded successfully

        sanity_flow_.assert_download_image(DUT2,
                                           protocol=params["protocol"]["ssh"],
                                           mode=params["mode"]["tftp"],
                                           server_ip=params["server_ip"],
                                           img=params["image_version"]["image_to_upgrade"],
                                           path=params["path"]["DUT2"]["tftp"])

        # Make connection to the DUT, Reload it and check the new software version is loading successfully

        sanity_flow_.reload_DUT(DUT2, protocol=params["protocol"]["ssh"])

        # Check the new software version and model name of the DUT

        sanity_flow_.check_software_version_and_model(DUT2,
                                                      img_to_be_checked=params["image_version_to_be_checked"]["image_to_upgrade"],
                                                      model=DUT2.model)

    def test_func_18(self):

        print("###### Test_func_18 ######")
        print("########## Check you can save/retrieve the startup-config on a remote server using TFTP using SSH - EX2010-P #############")

        sanity_flow_.assert_copy_startup_config(DUT2,
                                                protocol=params["protocol"]["ssh"],
                                                mode=params["mode"]["tftp"],
                                                server_ip=params["server_ip"],
                                                vlan="2000",
                                                path=params["path"]["DUT2"]["tftp"])

    def test_func_19(self):

        print("###### Test_func_19 ######")
        print("########## Check you can save/retrieve the startup-config on a remote server using SFTP using SSH - EX2010-P #############")

        sanity_flow_.assert_copy_startup_config(DUT2,
                                                protocol=params["protocol"]["ssh"],
                                                mode=params["mode"]["sftp"],
                                                server_ip=params["server_ip"],
                                                vlan="2000",
                                                path=params["path"]["DUT2"]["sftp"],
                                                user=params["user"],
                                                password=params["password"])

    def test_func_20(self):

        print("###### Test_func_20 ######")
        print("########## Check you can download a software image on DUT using TFTP using Telnet - EX2010-P #############")

        # Check that the new software version is downloaded successfully

        sanity_flow_.assert_download_image(DUT2,
                                           protocol=params["protocol"]["telnet"],
                                           mode=params["mode"]["tftp"],
                                           server_ip=params["server_ip"],
                                           img=params["image_version"]["image_to_downgrade"],
                                           path=params["path"]["DUT2"]["tftp"])

        # Make connection to the DUT, Reload it and check the new software version is loading successfully

        sanity_flow_.reload_DUT(DUT2, protocol=params["protocol"]["telnet"])

        # Check the new software version and model name of the DUT

        sanity_flow_.check_software_version_and_model(DUT2, img_to_be_checked=params["image_version_to_be_checked"]["image_to_downgrade"], model=DUT2.model)


    def test_func_21(self):

        print("###### Test_func_21 ######")
        print("########## Check you can download a software image on DUT using SFTP using Telnet - EX2010-P #############")

        # Check that the new software version is downloaded successfully

        sanity_flow_.assert_download_image(DUT2,
                                           protocol=params["protocol"]["telnet"],
                                           mode=params["mode"]["sftp"],
                                           server_ip=params["server_ip"],
                                           img=params["image_version"]["image_to_upgrade"],
                                           path=params["path"]["DUT2"]["sftp"],
                                           user=params["user"],
                                           password=params["password"])

        # Make connection to the DUT, Reload it and check the new software version is loading successfully

        sanity_flow_.reload_DUT(DUT2, protocol=params["protocol"]["telnet"])

        # Check the new software version and model name of the DUT

        sanity_flow_.check_software_version_and_model(DUT2,
                                                      img_to_be_checked=params["image_version_to_be_checked"]["image_to_upgrade"],
                                                      model=DUT2.model)

    @pytest.mark.skip(reason="scp not working")
    def test_func_22(self):

        print("###### Test_func_22 ######")
        print("########## Check you can download a software image on DUT using SCP using telnet - EX2010-P #############")

        # Need to find a way to avoid that press "Enter" in the password prompt

        # DUT2.sanity.download_image_ssh(mode="scp",server_ip="10.2.109.24", img="5.0.1-r4",user="cambium",password="cambium123", path="/tftpboot")

    def test_func_23(self):

        print("###### Test_func_23 ######")
        print("########## Check you can save/retrieve the startup-config on a remote server using TFTP using Telnet - EX2010-P #############")

        sanity_flow_.assert_copy_startup_config(DUT2,
                                                protocol=params["protocol"]["telnet"],
                                                mode=params["mode"]["tftp"],
                                                server_ip=params["server_ip"],
                                                vlan="2000",
                                                path=params["path"]["DUT2"]["tftp"])

    def test_func_24(self):

        print("###### Test_func_24 ######")
        print("########## Check you can save/retrieve the startup-config on a remote server using SFTP using Telnet - EX2010-P #############")

        sanity_flow_.assert_copy_startup_config(DUT2,
                                                protocol=params["protocol"]["telnet"],
                                                mode=params["mode"]["sftp"],
                                                server_ip=params["server_ip"],
                                                vlan="2000",
                                                path=params["path"]["DUT2"]["sftp"],
                                                user=params["user"],
                                                password=params["password"])

    def test_func_25(self):

        print("###### Test_func_25 ######")
        print("########## Verify a configuration made on a port is available after downloading new image using SSH - EX2010-P #############")

        # Make the configuration for the port

        sanity_flow_.port_configuration(DUT2,
                                        port="Gi 0/4",
                                        port_mode="Trunk",
                                        pvid="15",
                                        acceptable_frame_type="tagged")

        # Check the port configuration BEFORE downloading the new software image

        sanity_flow_.assert_configuration_port(DUT2,
                                               port="Gi 0/4",
                                               port_mode="Trunk",
                                               pvid="15",
                                               acceptable_frame_type="tagged",
                                               img_to_be_checked=params["image_version_to_be_checked"]["image_to_upgrade"],
                                               model=DUT2.model)

        # Save the configuration and download the new image

        sanity_flow_.save_configuration(DUT2, protocol=params["protocol"]["ssh"])
        sanity_flow_.assert_download_image(DUT2,
                                           protocol=params["protocol"]["ssh"],
                                           mode=params["mode"]["tftp"],
                                           server_ip=params["server_ip"],
                                           img=params["image_version"]["image_to_downgrade"],
                                           path=params["path"]["DUT2"]["tftp"],
                                           platform=params["platform"],
                                           img_compression=params["image_compression"],
                                           user=params["user"],
                                           password=params["password"])

        # Reload the DUT

        sanity_flow_.reload_DUT(DUT2, protocol=params["protocol"]["ssh"])

        # Check the port configuration AFTER downloading the new software image

        sanity_flow_.assert_configuration_port(DUT2,
                                               port="Gi 0/4",
                                               port_mode="Trunk",
                                               pvid="15",
                                               acceptable_frame_type="tagged",
                                               img_to_be_checked=params["image_version_to_be_checked"]["image_to_downgrade"],
                                               model=DUT2.model)

        # Remove the port configuration and save

        sanity_flow_.remove_port_configuration(DUT2, port="Gi 0/4")
        sanity_flow_.save_configuration(DUT2, protocol=params["protocol"]["ssh"])

        # Check the port configuration

        sanity_flow_.assert_configuration_port(DUT2,
                                               port="Gi 0/4",
                                               port_mode="Hybrid",
                                               pvid="1",
                                               acceptable_frame_type="all",
                                               img_to_be_checked=params["image_version_to_be_checked"]["image_to_downgrade"],
                                               model=DUT2.model)

        # Remove the VLAN configured

        DUT2.vl.remove_vlan(vlan="15")


    def test_func_26(self):

        print("###### Test_func_26 ######")
        print("########## Verify a configuration made on a port is available after downloading new image using Telnet - EX2010-P #############")

        # Make the configuration for the port

        sanity_flow_.port_configuration(DUT2,
                                        port="Gi 0/4",
                                        port_mode="Hybrid",
                                        pvid="10",
                                        acceptable_frame_type="untagged")

        # Check the port configuration BEFORE downloading the new software image

        sanity_flow_.assert_configuration_port(DUT2,
                                               port="Gi 0/4",
                                               port_mode="Hybrid",
                                               pvid="10",
                                               acceptable_frame_type="untagged",
                                               img_to_be_checked=params["image_version_to_be_checked"]["image_to_downgrade"],
                                               model=DUT2.model)

        # Save the configuration and download the new image

        sanity_flow_.save_configuration(DUT2, protocol=params["protocol"]["telnet"])
        sanity_flow_.assert_download_image(DUT2,
                                           protocol=params["protocol"]["telnet"],
                                           mode=params["mode"]["tftp"],
                                           server_ip=params["server_ip"],
                                           img=params["image_version"]["image_to_upgrade"],
                                           path=params["path"]["DUT2"]["tftp"],
                                           platform=params["platform"],
                                           img_compression=params["image_compression"],
                                           user=params["user"],
                                           password=params["password"])

        # Reload the DUT

        sanity_flow_.reload_DUT(DUT2, protocol=params["protocol"]["telnet"])

        # Check the port configuration AFTER downloading the new software image

        sanity_flow_.assert_configuration_port(DUT2,
                                               port="Gi 0/4",
                                               port_mode="Hybrid",
                                               pvid="10",
                                               acceptable_frame_type="untagged",
                                               img_to_be_checked=params["image_version_to_be_checked"]["image_to_upgrade"],
                                               model=DUT2.model)

        # Remove the port configuration and save

        sanity_flow_.remove_port_configuration(DUT2, port="Gi 0/4")
        sanity_flow_.save_configuration(DUT2, protocol=params["protocol"]["telnet"])

        # Check the port configuration

        sanity_flow_.assert_configuration_port(DUT2,
                                               port="Gi 0/4",
                                               port_mode="Hybrid",
                                               pvid="1",
                                               acceptable_frame_type="all",
                                               img_to_be_checked=params["image_version_to_be_checked"]["image_to_upgrade"],
                                               model=DUT2.model)
        # Remove the VLAN configured

        DUT2.vl.remove_vlan(vlan="10")


    def test_func_27(self):

        print("###### Test_func_27 ######")
        print("########## Check you can download a software image on DUT using TFTP using SSH - EX3052R-P #############")

        # Check that the new software version is downloaded successfully

        sanity_flow_.assert_download_image(DUT3,
                                           protocol=params["protocol"]["ssh"],
                                           mode=params["mode"]["tftp"],
                                           server_ip=params["server_ip"],
                                           img=params["image_version"]["image_to_upgrade"],
                                           path=params["path"]["DUT3"]["tftp"])

        # Make connection to the DUT, Reload it and check the new software version is loading successfully

        sanity_flow_.reload_DUT(DUT3, protocol=params["protocol"]["ssh"])

        # Check the new software version and model name of the DUT

        sanity_flow_.check_software_version_and_model(DUT3,
                                                      img_to_be_checked=params["image_version_to_be_checked"]["image_to_upgrade"],
                                                      model=DUT3.model)


    def test_func_28(self):

        print("###### Test_func_28 ######")
        print("########## Check you can download a software image on DUT using SFTP using SSH - EX3052R-P #############")

        # Check that the new software version is downloaded successfully

        sanity_flow_.assert_download_image(DUT3,
                                           protocol=params["protocol"]["ssh"],
                                           mode=params["mode"]["sftp"],
                                           server_ip=params["server_ip"],
                                           img=params["image_version"]["image_to_downgrade"],
                                           path=params["path"]["DUT3"]["sftp"],
                                           user=params["user"],
                                           password=params["password"])

        # Make connection to the DUT, Reload it and check the new software version is loading successfully

        sanity_flow_.reload_DUT(DUT3, protocol=params["protocol"]["ssh"])

        # Check the new software version and model name of the DUT

        sanity_flow_.check_software_version_and_model(DUT3, img_to_be_checked=params["image_version_to_be_checked"][
            "image_to_downgrade"], model=DUT3.model)

    @pytest.mark.skip(reason="scp not working")
    def test_func_29(self):

        print("###### Test_func_29 ######")
        print("########## Check you can download a software image on DUT using SCP using SSH - EX3052R-P #############")

        # Need to find a way to avoid that press "Enter" in the password prompt

        # DUT3.sanity.download_image_ssh(mode="scp",server_ip="10.2.109.24", img="5.0.1-r4",user="cambium",password="cambium123", path="/tftpboot")


    def test_func_30(self):

        # Getting back to the last image so we can do the save/retrieve confing

        print("###### Test_func_30 ######")
        print("########## Check you can download a software image on DUT using TFTP using SSH - EX3052R-P #############")

        # Check that the new software version is downloaded successfully

        sanity_flow_.assert_download_image(DUT3,
                                           protocol=params["protocol"]["ssh"],
                                           mode=params["mode"]["tftp"],
                                           server_ip=params["server_ip"],
                                           img=params["image_version"]["image_to_upgrade"],
                                           path=params["path"]["DUT3"]["tftp"])

        # Make connection to the DUT, Reload it and check the new software version is loading successfully

        sanity_flow_.reload_DUT(DUT3, protocol=params["protocol"]["ssh"])

        # Check the new software version and model name of the DUT

        sanity_flow_.check_software_version_and_model(DUT3,
                                                      img_to_be_checked=params["image_version_to_be_checked"][ "image_to_upgrade"],
                                                      model=DUT3.model)

    def test_func_31(self):

        print("###### Test_func_31 ######")
        print("########## Check you can save/retrieve the startup-config on a remote server using TFTP using SSH - EX3052R-P #############")

        sanity_flow_.assert_copy_startup_config(DUT3,
                                                protocol=params["protocol"]["ssh"],
                                                mode=params["mode"]["tftp"],
                                                server_ip=params["server_ip"],
                                                vlan="1000",
                                                path=params["path"]["DUT3"]["tftp"])

    def test_func_32(self):

        print("###### Test_func_32 ######")
        print("########## Check you can save/retrieve the startup-config on a remote server using SFTP using SSH - EX3052R-P #############")

        sanity_flow_.assert_copy_startup_config(DUT3,
                                                protocol=params["protocol"]["ssh"],
                                                mode=params["mode"]["sftp"],
                                                server_ip=params["server_ip"],
                                                vlan="1000",
                                                path=params["path"]["DUT3"]["sftp"],
                                                user=params["user"],
                                                password=params["password"])

    def test_func_33(self):

        print("###### Test_func_33 ######")
        print("########## Check you can download a software image on DUT using TFTP using Telnet - EX3052R-P #############")

        # Check that the new software version is downloaded successfully

        sanity_flow_.assert_download_image(DUT3,
                                           protocol=params["protocol"]["telnet"],
                                           mode=params["mode"]["tftp"],
                                           server_ip=params["server_ip"],
                                           img=params["image_version"]["image_to_downgrade"],
                                           path=params["path"]["DUT3"]["tftp"])

        # Make connection to the DUT, Reload it and check the new software version is loading successfully

        sanity_flow_.reload_DUT(DUT3, protocol=params["protocol"]["telnet"])

        # Check the new software version and model name of the DUT

        sanity_flow_.check_software_version_and_model(DUT3,
                                                      img_to_be_checked=params["image_version_to_be_checked"]["image_to_downgrade"],
                                                      model=DUT3.model)

    def test_func_34(self):

        print("###### Test_func_34 ######")
        print("########## Check you can download a software image on DUT using SFTP using Telnet - EX3052R-P #############")

        # Check that the new software version is downloaded successfully

        sanity_flow_.assert_download_image(DUT3,
                                           protocol=params["protocol"]["telnet"],
                                           mode=params["mode"]["sftp"],
                                           server_ip=params["server_ip"],
                                           img=params["image_version"]["image_to_upgrade"],
                                           path=params["path"]["DUT3"]["sftp"],
                                           user=params["user"],
                                           password=params["password"])

        # Make connection to the DUT, Reload it and check the new software version is loading successfully

        sanity_flow_.reload_DUT(DUT3, protocol=params["protocol"]["telnet"])

        # Check the new software version and model name of the DUT

        sanity_flow_.check_software_version_and_model(DUT3,
                                                      img_to_be_checked=params["image_version_to_be_checked"]["image_to_upgrade"],
                                                      model=DUT3.model)

    @pytest.mark.skip(reason="scp not working")
    def test_func_35(self):

        print("###### Test_func_35 ######")
        print("########## Check you can download a software image on DUT using SCP using telnet - EX3052R-P #############")

        # Need to find a way to avoid that press "Enter" in the password prompt

        # DUT3.sanity.download_image_ssh(mode="scp",server_ip="10.2.109.24", img="5.0.1-r4",user="cambium",password="cambium123", path="/tftpboot")

    def test_func_36(self):

        print("###### Test_func_36 ######")
        print("########## Check you can save/retrieve the startup-config on a remote server using TFTP using Telnet - EX3052R-P #############")

        sanity_flow_.assert_copy_startup_config(DUT3,
                                                protocol=params["protocol"]["telnet"],
                                                mode=params["mode"]["tftp"],
                                                server_ip=params["server_ip"],
                                                vlan="1000",
                                                path=params["path"]["DUT3"]["tftp"])

    def test_func_37(self):

        print("###### Test_func_37 ######")
        print("########## Check you can save/retrieve the startup-config on a remote server using SFTP using Telnet - EX3052R-P #############")

        sanity_flow_.assert_copy_startup_config(DUT3,
                                                protocol=params["protocol"]["telnet"],
                                                mode=params["mode"]["sftp"],
                                                server_ip=params["server_ip"],
                                                vlan="1000",
                                                path=params["path"]["DUT3"]["sftp"],
                                                user=params["user"],
                                                password=params["password"])

    def test_func_38(self):

        print("###### Test_func_38 ######")
        print("########## Verify a configuration made on a port is available after downloading new image using SSH - EX3052R-P #############")

        # Make the configuration for the port

        sanity_flow_.port_configuration(DUT3,
                                        port="Gi 0/4",
                                        port_mode="Trunk",
                                        pvid="15",
                                        acceptable_frame_type="tagged")

        # Check the port configuration BEFORE downloading the new software image

        sanity_flow_.assert_configuration_port(DUT3,
                                               port="Gi 0/4",
                                               port_mode="Trunk",
                                               pvid="15",
                                               acceptable_frame_type="tagged",
                                               img_to_be_checked=params["image_version_to_be_checked"]["image_to_upgrade"],
                                               model=DUT3.model)

        # Save the configuration and download the new image

        sanity_flow_.save_configuration(DUT3, protocol=params["protocol"]["ssh"])
        sanity_flow_.assert_download_image(DUT3,
                                           protocol=params["protocol"]["ssh"],
                                           mode=params["mode"]["tftp"],
                                           server_ip=params["server_ip"],
                                           img=params["image_version"]["image_to_downgrade"],
                                           path=params["path"]["DUT3"]["tftp"],
                                           platform=params["platform"],
                                           img_compression=params["image_compression"],
                                           user=params["user"],
                                           password=params["password"])

        # Reload the DUT

        sanity_flow_.reload_DUT(DUT3, protocol=params["protocol"]["ssh"])

        # Check the port configuration AFTER downloading the new software image

        sanity_flow_.assert_configuration_port(DUT3,
                                               port="Gi 0/4",
                                               port_mode="Trunk",
                                               pvid="15",
                                               acceptable_frame_type="tagged",
                                               img_to_be_checked=params["image_version_to_be_checked"]["image_to_downgrade"],
                                               model=DUT3.model)

        # Remove the port configuration and save

        sanity_flow_.remove_port_configuration(DUT3, port="Gi 0/4")
        sanity_flow_.save_configuration(DUT3, protocol=params["protocol"]["ssh"])

        # Check the port configuration

        sanity_flow_.assert_configuration_port(DUT3,
                                               port="Gi 0/4",
                                               port_mode="Hybrid",
                                               pvid="1",
                                               acceptable_frame_type="all",
                                               img_to_be_checked=params["image_version_to_be_checked"]["image_to_downgrade"],
                                               model=DUT3.model)

        # Remove the VLAN configured

        DUT3.vl.remove_vlan(vlan="15")


    def test_func_39(self):

        print("###### Test_func_39 ######")
        print("########## Verify a configuration made on a port is available after downloading new image using Telnet - EX3052R-P #############")

        # Make the configuration for the port

        sanity_flow_.port_configuration(DUT3,
                                        port="Gi 0/4",
                                        port_mode="Hybrid",
                                        pvid="10",
                                        acceptable_frame_type="untagged")

        # Check the port configuration BEFORE downloading the new software image

        sanity_flow_.assert_configuration_port(DUT3,
                                               port="Gi 0/4",
                                               port_mode="Hybrid",
                                               pvid="10",
                                               acceptable_frame_type="untagged",
                                               img_to_be_checked=params["image_version_to_be_checked"]["image_to_downgrade"],
                                               model=DUT3.model)

        # Save the configuration and download the new image

        sanity_flow_.save_configuration(DUT3, protocol=params["protocol"]["telnet"])
        sanity_flow_.assert_download_image(DUT3,
                                           protocol=params["protocol"]["telnet"],
                                           mode=params["mode"]["tftp"],
                                           server_ip=params["server_ip"],
                                           img=params["image_version"]["image_to_upgrade"],
                                           path=params["path"]["DUT3"]["tftp"],
                                           platform=params["platform"],
                                           img_compression=params["image_compression"],
                                           user=params["user"],
                                           password=params["password"])

        # Reload the DUT

        sanity_flow_.reload_DUT(DUT3, protocol=params["protocol"]["telnet"])

        # Check the port configuration AFTER downloading the new software image

        sanity_flow_.assert_configuration_port(DUT3,
                                               port="Gi 0/4",
                                               port_mode="Hybrid",
                                               pvid="10",
                                               acceptable_frame_type="untagged",
                                               img_to_be_checked=params["image_version_to_be_checked"]["image_to_upgrade"],
                                               model=DUT3.model)

        # Remove the port configuration and save

        sanity_flow_.remove_port_configuration(DUT3, port="Gi 0/4")
        sanity_flow_.save_configuration(DUT3, protocol=params["protocol"]["telnet"])

        # Check the port configuration

        sanity_flow_.assert_configuration_port(DUT3,
                                               port="Gi 0/4",
                                               port_mode="Hybrid",
                                               pvid="1",
                                               acceptable_frame_type="all",
                                               img_to_be_checked=params["image_version_to_be_checked"]["image_to_upgrade"],
                                               model=DUT3.model)

        # Remove the VLAN configured

        DUT3.vl.remove_vlan(vlan="10")


    # def test_func_40(self):
    #
    #     print(path)
    #     print(path["DUT1"]["sftp"])
    #     print(path["DUT1"]["tftp"])
    #     print(path["DUT2"]["sftp"])
    #     print(path["DUT2"]["tftp"])
    #     print(path["DUT3"]["sftp"])
    #     print(path["DUT3"]["tftp"])




