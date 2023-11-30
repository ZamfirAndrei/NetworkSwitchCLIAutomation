import time
import pytest

from config import sanity
from Management import dut_objects


class SanityFlow:

    def assert_download_image(self, DUT, protocol, mode, server_ip, img, path, user=None, password=None):

        if protocol == "ssh":

            # Check that the new software version is downloaded succesfully

            result = DUT.sanity.download_image_ssh(mode=mode, server_ip=server_ip, img=img, user=user, password=password, path=path)

            assert result == "Image Download Successful"
            print("Successful asserting...")

        elif protocol == "telnet":

            # Check that the new software version is downloaded succesfully

            result = DUT.sanity.download_image_telnet(mode=mode, server_ip=server_ip, img=img)

            assert result == "Image Download Successful"
            print("Successful asserting...")

        else:

            print("Choose a valid protocol!")


    def reload_DUT(self, DUT, protocol):

        print(f"Reloading the DUT {DUT.ip_session}...")

        if protocol == "ssh":

            DUT.session.connect()
            DUT.session.send_cmd(cmd="reload --y")
            DUT.session.close()
            time.sleep(140)

        elif protocol == "telnet":

            DUT.tn.connect()
            DUT.tn.write_cmd(cmd="reload --y")
            DUT.tn.close()
            time.sleep(140)

        else:

            print("Choose a valid protocol!")


    def check_software_version_and_model(self, DUT, img_to_be_checked, model):

        # Check the new software version and model name of the DUT

        software_version = DUT.sanity.show_software_version_device()
        model_name = DUT.sanity.show_model_name_device()

        assert software_version["CNS Software Version"] == img_to_be_checked
        assert model_name["Model Name"] == model

    def assert_copy_startup_config(self, DUT, protocol, mode, server_ip, vlan, path, user=None, password=None):

        if protocol == "ssh":

            # Copy the startup-config on the Remove Server

            DUT.sanity.copy_running_config_ssh(mode=mode, server_ip=server_ip, user=user, password=password, path=path)

            # Make connection to the DUT, create VLAN and save the config

            DUT.vl.create_vlan(vlan=vlan)
            vl = DUT.vl.show_vlan(vlan=vlan)
            print(vl)

            DUT.session.connect()
            DUT.session.send_cmd(cmd="wr st")
            DUT.session.close()

            assert vl["VLAN ID"] == vlan

            # Retrieve the config, from the remote server, on the DUT

            result = DUT.sanity.retrieve_config_from_server_ssh(mode=mode, server_ip=server_ip, path=path, user=user, password=password)

            # Check the file is downloaded successfully

            assert result == "File Copied Successfully"
            print("Successful asserting before reloading the DUT...")

            # Make connection to the DUT and reload it

            self.reload_DUT(DUT, protocol=protocol)

            # Check after the reload that VLAN is no longer configured

            vl = DUT.vl.show_vlan(vlan=vlan)
            print(vl)

            assert vl["VLAN ID"] != vlan
            print("Successful asserting after reloading the DUT...")

        elif protocol == "telnet":

            # Copy the startup-config on the Remove Server

            DUT.sanity.copy_running_config_telnet(mode=mode, server_ip=server_ip, user=user, password=password,path=path)

            # Make connection to the DUT, create VLAN and save the config

            DUT.vl.create_vlan(vlan=vlan)
            vl = DUT.vl.show_vlan(vlan=vlan)
            print(vl)

            DUT.tn.connect()
            DUT.tn.write_cmd(cmd="wr st")
            DUT.tn.close()

            assert vl["VLAN ID"] == vlan

            # Retrieve the config, from the remote server, on the DUT

            time.sleep(2)

            result = DUT.sanity.retrieve_config_from_server_telnet(mode=mode, server_ip=server_ip, user=user, password=password, path=path)

            # Check the file is downloaded successfully

            assert result == "File Copied Successfully"

            print("Successful asserting before reloading the DUT...")

            # Make connection to the DUT and reload it

            self.reload_DUT(DUT, protocol=protocol)

            # Check after the reload that VLAN is no longer configured

            vl = DUT.vl.show_vlan(vlan=vlan)
            print(vlan)

            assert vl["VLAN ID"] != vlan
            print("Successful asserting after reloading the DUT...")

        else:

            print("Choose a valid protocol!")
