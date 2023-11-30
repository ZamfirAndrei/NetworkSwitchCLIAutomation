import time
import pytest

from config import sanity

from Management import dut_objects
from flows import sanity_flow

ip_session_1 = "10.2.109.206"
ip_session_2 = "10.2.109.83"
ip_session_3 = "10.2.109.232"

DUT1 = dut_objects.DUT_Objects(ip_session=ip_session_1)
DUT2 = dut_objects.DUT_Objects(ip_session=ip_session_2)
DUT3 = dut_objects.DUT_Objects(ip_session=ip_session_3)

sanity_flow_ = sanity_flow.SanityFlow()

class TestSanitySuite2:

    def test_func_1(self):

        print("###### Test_func_1 ######")
        print("########## Check you can download a software image on DUT using TFTP using SSH #############")

        # Check that the new software version is downloaded succesfully

        sanity_flow_.assert_download_image(DUT1, "ssh", "tftp", "10.2.109.24", "5.0.2-r2","/AGZamfir/Andrei-2028.conf")

        # Make connection to the DUT, Reload it and check the new software version is loading successfully

        sanity_flow_.reload_DUT(DUT1, "ssh")

        # Check the new software version and model name of the DUT

        sanity_flow_.check_software_version_and_model(DUT1, "5.0.2-r2", "EX2028-P")

    def test_func_2(self):

        print("###### Test_func_2 ######")
        print("########## Check you can download a software image on DUT using SFTP using SSH #############")

        # Check that the new software version is downloaded succesfully

        sanity_flow_.assert_download_image(DUT1, "ssh", "sftp", "10.2.109.24", "5.1.0-e8", "/AGZamfir/Andrei-2028.conf", "cambium", "cambium123")

        # Make connection to the DUT, Reload it and check the new software version is loading successfully

        sanity_flow_.reload_DUT(DUT1, "ssh")

        # Check the new software version and model name of the DUT

        sanity_flow_.check_software_version_and_model(DUT1, "5.1.0-e8", "EX2028-P")

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

        sanity_flow_.assert_copy_startup_config(DUT1, "ssh", "tftp", "10.2.109.24", "3000", "/AGZamfir/Andrei-2028.conf", "cambium", "cambium123")

    # def test_func_5(self):
    #
    #     print("###### Test_func_5 ######")
    #     print("########## Check you can save/retrieve the startup-config on a remote server using SFTP using SSH #############")
    #
    #     # Copy the startup-config on the Remove Server
    #
    #     DUT1.sanity.copy_running_config_ssh(mode="sftp", server_ip="10.2.109.24", user="cambium", password="cambium123",
    #                                         path="/AGZamfir/Andrei-2028.conf")
    #
    #     # Make connection to the DUT, create VLAN 1000 and save the config
    #
    #     DUT1.vl.create_vlan(vlan="1000")
    #     vlan = DUT1.vl.show_vlan(vlan="1000")
    #     print(vlan)
    #
    #     DUT1.session.connect()
    #     DUT1.session.send_cmd(cmd="wr st")
    #     DUT1.session.close()
    #
    #     assert vlan["VLAN ID"] == "1000"
    #
    #     # Retrieve the config, from the remote server, on the DUT
    #
    #     result = DUT1.sanity.retrieve_config_from_server_ssh(mode="sftp", server_ip="10.2.109.24", user="cambium", password="cambium123",
    #                                         path="/AGZamfir/Andrei-2028.conf")
    #
    #     # Check the file is downloaded successfully
    #
    #     assert result == "File Copied Successfully"
    #
    #     # Make connection to the DUT and reload it.
    #
    #     DUT1.session.connect()
    #     DUT1.session.send_cmd(cmd="reload --y")
    #     DUT1.session.close()
    #     time.sleep(140)
    #
    #     # Check after the reload that VLAN 1000 is no longer configured
    #
    #     vlan = DUT1.vl.show_vlan(vlan="1000")
    #     print(vlan)
    #
    #     assert vlan["VLAN ID"] != "1000"
    #
    # def test_func_6(self):
    #
    #     print("###### Test_func_6 ######")
    #     print("########## Check you can download a software image on DUT using TFTP using Telnet #############")
    #
    #     # Check that the new software version is downloaded succesfully
    #
    #     result = DUT1.sanity.download_image_telnet(mode="tftp", server_ip="10.2.109.24", img="5.1.0-e18")
    #
    #     assert result == "Image Download Successful"
    #
    #     # Make connection to the DUT, Reload it and check the new software version is loading successfully
    #
    #     DUT1.tn.connect()
    #     DUT1.tn.write_cmd(cmd="reload --y")
    #     DUT1.tn.close()
    #     time.sleep(140)
    #
    #     # Check the new software version and model name of the DUT
    #
    #     software_version = DUT1.sanity.show_software_version_device()
    #     model_name = DUT1.sanity.show_model_name_device()
    #
    #     assert software_version["CNS Software Version"] == "5.1.0-e8"
    #     assert model_name["Model Name"] == "EX2028R-P"
    #
    # def test_func_7(self):
    #
    #     print("###### Test_func_7 ######")
    #     print("########## Check you can download a software image on DUT using SFTP using Telnet #############")
    #
    #     # Check that the new software version is downloaded succesfully
    #
    #     result = DUT1.sanity.download_image_telnet(mode="sftp", server_ip="10.2.109.24", img="5.1.0-e8", user="cambium",password="cambium123")
    #
    #     assert result == "Image Download Successful"
    #
    #     # Make connection to the DUT, Reload it and check the new software version is loading successfully
    #
    #     DUT1.tn.connect()
    #     DUT1.tn.write_cmd(cmd="reload --y")
    #     DUT1.tn.close()
    #     time.sleep(140)
    #
    #     # Check the new software version and model name of the DUT
    #
    #     software_version = DUT3.sanity.show_software_version_device()
    #     model_name = DUT3.sanity.show_model_name_device()
    #
    #     assert software_version["CNS Software Version"] == "5.1.0-e8"
    #     assert model_name["Model Name"] == "EX2028R-P"
    #
    # def test_func_8(self):
    #
    #     print("###### Test_func_8 ######")
    #     print("########## Check you can download a software image on DUT using SCP using telnet #############")
    #
    #     # Need to find a way to avoid that press "Enter" in the password prompt
    #
    #     # DUT1.sanity.download_image_ssh(mode="scp",server_ip="10.2.109.24", img="5.0.1-r4",user="cambium",password="cambium123", path="/tftpboot")
    #
    # def test_func_9(self):
    #
    #     print("###### Test_func_9 ######")
    #     print("########## Check you can save/retrieve the startup-config on a remote server using TFTP using Telnet #############")
    #
    #     # Copy the startup-config on the Remove Server
    #
    #     DUT1.sanity.copy_running_config_telnet(mode="tftp", server_ip="10.2.109.24", path="/AGZamfir/Andrei-2028.conf")
    #
    #     # Make connection to the DUT, create VLAN 1000 and save the config
    #
    #     DUT1.vl.create_vlan(vlan="1000")
    #     vlan = DUT1.vl.show_vlan(vlan="1000")
    #     print(vlan)
    #
    #     DUT1.tn.connect()
    #     DUT1.tn.write_cmd(cmd="wr st")
    #     DUT1.tn.close()
    #
    #     assert vlan["VLAN ID"] == "1000"
    #
    #     # Retrieve the config, from the remote server, on the DUT
    #
    #     time.sleep(2)
    #
    #     result = DUT1.sanity.retrieve_config_from_server_telnet(mode="tftp", server_ip="10.2.109.24", path="/AGZamfir/Andrei-2028.conf")
    #
    #     # Check the file is downloaded successfully
    #
    #     assert result == "File Copied Successfully"
    #
    #     # Make connection to the DUT and reload it.
    #
    #     DUT1.tn.connect()
    #     DUT1.tn.write_cmd(cmd="reload --y")
    #     DUT1.tn.close()
    #     time.sleep(140)
    #
    #     # Check after the reload that VLAN 1000 is no longer configured
    #
    #     vlan = DUT1.vl.show_vlan(vlan="1000")
    #     print(vlan)
    #
    #     assert vlan["VLAN ID"] != "1000"
    #
    # def test_func_10(self):
    #
    #     print("###### Test_func_10 ######")
    #     print("########## Check you can save/retrieve the startup-config on a remote server using SFTP using Telnet #############")
    #
    #     # Copy the startup-config on the Remove Server
    #
    #     DUT1.sanity.copy_running_config_telnet(mode="sftp", server_ip="10.2.109.24", user="cambium", password="cambium123",
    #                                         path="/AGZamfir/Andrei-2028.conf")
    #
    #     # Make connection to the DUT, create VLAN 1000 and save the config
    #
    #     DUT1.vl.create_vlan(vlan="1000")
    #     vlan = DUT1.vl.show_vlan(vlan="1000")
    #     print(vlan)
    #
    #     DUT1.tn.connect()
    #     DUT1.tn.write_cmd(cmd="wr st")
    #     DUT1.tn.close()
    #
    #     assert vlan["VLAN ID"] == "1000"
    #
    #     # Retrieve the config, from the remote server, on the DUT
    #
    #     time.sleep(2)
    #
    #     result = DUT1.sanity.retrieve_config_from_server_telnet(mode="sftp", server_ip="10.2.109.24", user="cambium", password="cambium123", path="/AGZamfir/Andrei-2028.conf")
    #
    #     # Check the file is downloaded successfully
    #
    #     assert result == "File Copied Successfully"
    #
    #     # Make connection to the DUT and reload it.
    #
    #     DUT1.tn.connect()
    #     DUT1.tn.write_cmd(cmd="reload --y")
    #     DUT1.tn.close()
    #     time.sleep(140)
    #
    #     # Check after the reload that VLAN 1000 is no longer configured
    #
    #     vlan = DUT1.vl.show_vlan(vlan="1000")
    #     print(vlan)
    #
    #     assert vlan["VLAN ID"] != "1000"
