import re
import time
import pytest

from config import sanity
from Management import dut_objects


class SanityFlow:

    def assert_download_image(self, DUT, protocol, mode, server_ip, img, path, platform= "EXTX", img_compression = "img", user=None, password=None):

        if protocol == "ssh":

            # Check that the new software version is downloaded successfully

            result = DUT.sanity.download_image_ssh(mode=mode,
                                                   server_ip=server_ip,
                                                   img=img,
                                                   user=user,
                                                   password=password,
                                                   path=path,
                                                   platform=platform,
                                                   img_compression=img_compression)

            assert result == "Image Download Successful"
            print("Successful asserting...")

        elif protocol == "telnet":

            # Check that the new software version is downloaded successfully

            result = DUT.sanity.download_image_telnet(mode=mode,
                                                      server_ip=server_ip,
                                                      img=img,
                                                      user=user,
                                                      password=password,
                                                      platform=platform,
                                                      img_compression=img_compression)

            assert result == "Image Download Successful"
            print("Successful asserting...")

        else:

            print("Choose a valid protocol!")


    def reload_DUT(self, DUT, protocol):

        print(f"Reloading the {DUT.hostname} switch with the ip address {DUT.ip_session}...")

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

    def save_and_reload_DUT(self, DUT, protocol):

        print(f"Reloading the {DUT.hostname} switch with the ip address {DUT.ip_session}...")

        if protocol == "ssh":

            DUT.session.connect()
            DUT.session.send_cmd(cmd="wr st")
            time.sleep(3)
            output = DUT.session.read()
            # print(output)

            result = re.findall(r"OK", output)
            # print(result)

            if result[0] == "OK":
                print(f"The configuration of {DUT.hostname} has been saved successfully in the startup-config")
            else:
                print(f"The configuration of {DUT.hostname} has not been saved successfully in the startup-config")

            DUT.session.send_cmd(cmd="reload --y")
            DUT.session.close()
            time.sleep(140)

        elif protocol == "telnet":

            DUT.tn.connect()
            DUT.tn.write_cmd(cmd="wr st")
            time.sleep(3)
            output = DUT.tn.read()
            # print(output)

            result = re.findall(r"OK", output)
            # print(result)

            if result[0] == "OK":
                print(f"The configuration of {DUT.hostname} has been saved successfully in the startup-config")
            else:
                print(f"The configuration of {DUT.hostname} has not been saved successfully in the startup-config")

            DUT.tn.write_cmd(cmd="reload --y")
            DUT.tn.close()
            time.sleep(140)

        else:

            print("Choose a valid protocol!")

    def save_configuration(self, DUT, protocol):

        print(f"Saving the configuration on the {DUT.hostname} with the ip address {DUT.ip_session}...")

        if protocol == "ssh":

            DUT.session.connect()
            DUT.session.send_cmd(cmd="wr st")
            time.sleep(3)
            output = DUT.session.read()
            # print(output)

            result = re.findall(r"OK", output)
            # print(result)

            if result[0] == "OK":
                print(f"The configuration of {DUT.hostname} has been saved successfully in the startup-config")
            else:
                print(f"The configuration of {DUT.hostname} has not been saved successfully in the startup-config")


        elif protocol == "telnet":

            DUT.tn.connect()
            DUT.tn.write_cmd(cmd="wr st")
            time.sleep(3)
            output = DUT.tn.read()
            # print(output)

            result = re.findall(r"OK", output)
            # print(result)

            if result[0] == "OK":
                print(f"The configuration of {DUT.hostname} has been saved successfully in the startup-config")
            else:
                print(f"The configuration of {DUT.hostname} has not been saved successfully in the startup-config")


        else:

            print("Choose a valid protocol!")

        time.sleep(5)

    def check_software_version_and_model(self, DUT, img_to_be_checked, model):

        # Check the new software version and model name of the DUT

        software_version = DUT.sanity.show_software_version_device()
        model_name = DUT.sanity.show_model_name_device()

        assert software_version["CNS Software Version"] == img_to_be_checked
        assert model_name["Model Name"] == model

        print(f"The software version {software_version['CNS Software Version']} and the model name {model_name['Model Name']} have been asserted successfully")

    def assert_copy_startup_config(self, DUT, protocol, mode, server_ip, vlan, path, user=None, password=None):

        if protocol == "ssh":

            # Save the configuration

            DUT.session.connect()
            DUT.session.send_cmd(cmd="wr st")
            DUT.session.close()

            print("The configuration has been saved")

            # Copy the startup-config on the Remove Server

            DUT.sanity.copy_running_config_ssh(mode=mode, server_ip=server_ip, user=user, password=password, path=path)

            # Make connection to the DUT, create VLAN and save the config

            DUT.vl.create_vlan(vlan=vlan)
            vl = DUT.vl.show_vlan(vlan=vlan)
            print(vl)

            DUT.session.connect()
            DUT.session.send_cmd(cmd="wr st")
            DUT.session.close()

            time.sleep(5)

            print("The configuration has been saved to startup-config...")

            assert vl["VLAN ID"] == vlan

            # Retrieve the config, from the remote server, on the DUT

            time.sleep(5)

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

            # Save the configuration

            DUT.tn.connect()
            DUT.tn.write_cmd(cmd="wr st")
            DUT.tn.close()

            print("The configuration has been saved")

            # Copy the startup-config on the Remove Server

            DUT.sanity.copy_running_config_telnet(mode=mode, server_ip=server_ip, user=user, password=password,path=path)

            # Make connection to the DUT, create VLAN and save the config

            DUT.vl.create_vlan(vlan=vlan)
            vl = DUT.vl.show_vlan(vlan=vlan)
            print(vl)

            DUT.tn.connect()
            DUT.tn.write_cmd(cmd="wr st")
            DUT.tn.close()
            print("The configuration has been saved to startup-config...")

            assert vl["VLAN ID"] == vlan

            # Retrieve the config, from the remote server, on the DUT

            time.sleep(5)

            result = DUT.sanity.retrieve_config_from_server_telnet(mode=mode, server_ip=server_ip, user=user, password=password, path=path)

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

        else:

            print("Choose a valid protocol!")

    def port_configuration(self,  DUT, port, port_mode, pvid, acceptable_frame_type):

        # Create vlan

        DUT.vl.create_vlan(vlan=pvid)

        # Make the configuration for the port

        DUT.int.add_port_configuration(port=port, mode=port_mode, pvid=pvid,
                                       acceptable_frame_type=acceptable_frame_type)

    def remove_port_configuration(self, DUT, port):

        # Remove port configurations

        DUT.int.remove_port_configuration(port=port)

    def assert_configuration_port(self, DUT, port, port_mode, pvid, acceptable_frame_type, img_to_be_checked, model):

        # Check the Port Configuration BEFORE downloading the new image

        port_ = DUT.vl.show_vlan_port(port=port)
        print(port_)

        assert port_["Port"] == port.replace(" ","")
        assert port_["Port VLAN ID"] == pvid
        assert port_["Port Mode"] == port_mode

        if acceptable_frame_type == "all":
            assert port_["Port Acceptable Frame Type"] == "Admit All"

        elif acceptable_frame_type == "tagged":
            assert port_["Port Acceptable Frame Type"] == "Admit Only VLAN Tagged"

        elif acceptable_frame_type == "untagged":
            assert port_["Port Acceptable Frame Type"] == "Admit Only Untagged and Priority Tagged"

        else:
            print(f"Chose a valid acceptable_frame_type for the port {port}")

        # Check the model and software version

        self.check_software_version_and_model(DUT, img_to_be_checked=img_to_be_checked, model=model)

    def assert_configuration_port_before_after_download_image(self, DUT, port, port_mode, pvid, acceptable_frame_type,
                                                              protocol, mode, srv_ip, user, password , path, img_to_be_checked,
                                                            model):

        # Make the configuration for the port

        DUT.int.add_port_configuration(port=port, mode=port_mode, pvid=pvid, acceptable_frame_type=acceptable_frame_type)

        # Check the Port Configuration BEFORE downloading the new image

        port_ = DUT.vl.show_vlan_port(port=port)
        print(port_)

        assert port_["Port"] == port.replace(" ","")
        assert port_["Port VLAN ID"] == pvid
        assert port_["Port Mode"] == port_mode

        if acceptable_frame_type == "all":
            assert port_["Port Acceptable Frame Type"] == "Admit All"

        elif acceptable_frame_type == "tagged":
            assert port_["Port Acceptable Frame Type"] == "Admit Only VLAN Tagged"

        elif acceptable_frame_type == "untagged":
            assert port_["Port Acceptable Frame Type"] == "Admit Only Untagged and Priority Tagged"

        else:
            print(f"Chose a valid acceptable_frame_type for the port {port}")

        # Save the configuration and download the new image

        self.save_configuration(DUT, protocol)
        self.assert_download_image(DUT, protocol, mode, srv_ip, img_to_be_checked, path, user, password)

        # Reload the DUT

        self.reload_DUT(DUT, protocol)

        # Check the Port Configuration AFTER downloading the new image

        port_ = DUT.vl.show_vlan_port(port=port)
        print(port_)

        assert port_["Port"] == port.replace(" ", "")
        assert port_["Port VLAN ID"] == pvid
        assert port_["Port Mode"] == port_mode

        if acceptable_frame_type == "all":
            assert port_["Port Acceptable Frame Type"] == "Admit All"

        elif acceptable_frame_type == "tagged":
            assert port_["Port Acceptable Frame Type"] == "Admit Only VLAN Tagged"

        elif acceptable_frame_type == "untagged":
            assert port_["Port Acceptable Frame Type"] == "Admit Only Untagged and Priority Tagged"

        else:
            print(f"Chose a valid acceptable_frame_type for the port {port}")

        # Check the model and software version

        self.check_software_version_and_model(DUT, img_to_be_checked=img_to_be_checked, model=model)








