import time
import re

from Management import ssh, telnet

failed_messages_download = ["% Image Download Failed [[Unable to Reach Host]]","% Image Download Failed [[No Such File]]",
                            "% Image Download Failed [[INTERNAL ERROR]]", "Image Download Failed [File Transfer Failed]"]
passed_message_download = ["Image Download Successful"]

failed_message_copy_running_config = ["% TFTP failed", "% SFTP failed", "% TFTP Failed: startup-config file not found.", "% TFTP Failed", "% SFTP Failed"]
passed_message_copy_running_config =[]

class Sanity:

    def __init__(self, ip_session):

        self.session = ssh.SSH(ip=ip_session)
        self.tn = telnet.Telnet(ip=ip_session)

    def download_image_ssh(self, mode, server_ip, img, platform= "EXTX", img_compression = "img", user=None, password=None, path=None):

        self.session.connect()

        if mode == "tftp":

            self.session.send_cmd(cmd=f"download agent tftp://{server_ip}/cnMatrix-{platform}-{img}.{img_compression}.tar.gz")

        elif mode == "sftp":

            self.session.send_cmd(cmd=f"download agent sftp://{user}:{password}@{server_ip}/cnMatrix-{platform}-{img}.{img_compression}.tar.gz")

        elif mode == "scp":

            self.session.send_cmd(cmd=f"download agent scp://{user}@{server_ip}{path}/cnMatrix-{platform}-{img}.{img_compression}.tar.gz")
            self.session.send_cmd(cmd=f"{password}")

        else:

            print(f"The mode {mode} is not valid. Choose a valid mode")

        time.sleep(160)
        output = self.session.read()
        print(output)

        result = re.findall(r"(Image Download Successful)", output)
        print(result)

        for res in failed_messages_download:

            if res in output:

                print(f"There is a problem: {res}")
                # print(res)
                return res

        if (result):

            print(result[0])
            return result[0]

        self.session.close()


    def show_software_version_device(self):

        d_soft_version = dict()

        self.session.connect()
        self.session.send_cmd(cmd="conf t;set cli pagination off")
        self.session.send_cmd(cmd="do show system information")
        self.session.send_cmd(cmd="exit")

        output = self.session.read()
        # print(output)

        software_version = re.findall(r"CNS Software Version\s+:\s+([\w.-]+)", output)
        # print(software_version)

        d_soft_version["CNS Software Version"] = software_version[0]
        # print(d_soft_version)

        self.session.close()

        return d_soft_version

    def show_model_name_device(self):

        d_model_name = dict()

        self.session.connect()
        self.session.send_cmd(cmd="conf t;set cli pagination off")
        self.session.send_cmd(cmd="do show system information")
        self.session.send_cmd(cmd="exit")

        output = self.session.read()
        # print(output)

        model_name = re.findall(r"Model Name\s+:\s+([\w-]+)", output)
        # print(model_name)

        d_model_name["Model Name"] = model_name[0]
        # print(d_model_name)

        self.session.close()

        return d_model_name

    def copy_running_config_ssh(self, mode, server_ip, user=None, password=None, path=None):

        self.session.connect()

        if mode == "tftp":

            self.session.send_cmd(cmd=f"copy startup-config tftp://{server_ip}{path}")

        elif mode == "sftp":

            self.session.send_cmd(cmd=f"copy startup-config sftp://{user}:{password}@{server_ip}{path}")

        elif mode == "scp":

            self.session.send_cmd(cmd=f"copy startup scp://{user}@{server_ip}{path}")
            self.session.send_cmd(cmd=f"{password}")

        else:

            print(f"The mode {mode} is not valid. Choose a valid mode")

        time.sleep(60)
        output = self.session.read()
        print(output)
        ok = False

        for res in failed_message_copy_running_config:
            # print(res)
            if res in output:
                print(f"There is a problem: {res}")
                # print(res)
                ok = False
                return res

            else:
                ok = True

        if ok == True:
            print(f"The configuration has been copied successfully on the server {server_ip}")

        self.session.close()

    def retrieve_config_from_server_ssh(self, mode, server_ip, user=None, password=None, path=None):

        self.session.connect()

        if mode == "tftp":

            self.session.send_cmd(cmd=f"copy tftp://{server_ip}{path} startup-config")

        elif mode == "sftp":

            self.session.send_cmd(cmd=f"copy sftp://{user}:{password}@{server_ip}{path} startup-config ")

        elif mode == "scp":

            self.session.send_cmd(cmd=f"copy scp://{user}@{server_ip}{path} startup ")
            self.session.send_cmd(cmd=f"{password}")

        else:
            print(f"The mode {mode} is not valid. Choose a valid mode")

        time.sleep(60)
        output = self.session.read()
        print(output)

        result = re.findall(r"(File Copied Successfully)", output)
        print(result)

        for res in failed_message_copy_running_config:
            # print(res)
            if res in output:
                print(f"There is a problem: {res}")
                # print(res)
                return res

        if (result):
            print(result[0])
            return result[0]

        self.session.close()


    def copy_running_config_telnet(self, mode, server_ip, user=None, password=None, path=None):

        self.tn.connect()

        if mode == "tftp":

            self.tn.write_cmd(cmd=f"copy startup-config tftp://{server_ip}{path}")

        elif mode == "sftp":

            self.tn.write_cmd(cmd=f"copy startup-config sftp://{user}:{password}@{server_ip}{path}")

        elif mode == "scp":

            self.tn.write_cmd(cmd=f"copy startup scp://{user}@{server_ip}{path}")
            self.tn.write_cmd(cmd=f"{password}")

        else:

            print(f"The mode {mode} is not valid. Choose a valid mode")

        time.sleep(60)
        output = self.tn.read()
        # print(output)
        ok = False

        for res in failed_message_copy_running_config:
            # print(res)
            if res in output:
                print(f"There is a problem: {res}")
                # print(res)
                ok = False
                return res

            else:
                ok = True

        if ok == True:
            print(f"The configuration has been copied successfully on the server {server_ip}")

        self.tn.close()

    def retrieve_config_from_server_telnet(self, mode, server_ip, user=None, password=None, path=None):

        self.tn.connect()

        if mode == "tftp":

            self.tn.write_cmd(cmd=f"copy tftp://{server_ip}{path} startup-config")

        elif mode == "sftp":

            self.tn.write_cmd(cmd=f"copy sftp://{user}:{password}@{server_ip}{path} startup-config ")

        elif mode == "scp":

            self.tn.write_cmd(cmd=f"copy scp://{user}@{server_ip}{path} startup ")
            self.tn.write_cmd(cmd=f"{password}")

        else:

            print(f"The mode {mode} is not valid. Choose a valid mode")

        time.sleep(60)
        output = self.tn.read()
        # print(output)

        result = re.findall(r"(File Copied Successfully)", output)
        print(result)

        for res in failed_message_copy_running_config:
            # print(res)
            if res in output:
                print(f"There is a problem: {res}")
                # print(res)
                return res

        if (result):
            print(result[0])
            return result[0]

        self.tn.close()

    def download_image_telnet(self, mode, server_ip, img, platform= "EXTX", img_compression = "img", user=None, password=None, path=None):

        self.tn.connect()

        if mode == "tftp":

            self.tn.write_cmd(cmd=f"download agent tftp://{server_ip}/cnMatrix-{platform}-{img}.{img_compression}.tar.gz")

        elif mode == "sftp":

            self.tn.write_cmd(cmd=f"download agent sftp://{user}:{password}@{server_ip}/cnMatrix-{platform}-{img}.{img_compression}.tar.gz")

        elif mode == "scp":

            self.tn.write_cmd(cmd=f"download agent scp://{user}@{server_ip}{path}/cnMatrix-{platform}-{img}.{img_compression}.tar.gz")
            self.tn.write_cmd(cmd=f"{password}")

        else:

            print(f"The mode {mode} is not valid. Choose a valid mode")

        time.sleep(160)
        output = self.tn.read()
        print(output)

        result = re.findall(r"(Image Download Successful)", output)
        print(result)

        for res in failed_messages_download:
            # print(res)
            if res in output:
                print(f"There is a problem: {res}")
                # print(res)
                return res

        if (result):

            print(result[0])
            return result[0]

        self.tn.close()

# obj = Sanity(ip_session="10.2.109.206")
# img = obj.show_software_version_device()