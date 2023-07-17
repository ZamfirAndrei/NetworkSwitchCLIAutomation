import time
import re

from Management import ssh, telnet


class PING:

    def __init__(self, ip_session="10.2.109.178"):

        print("Clasa PING")

        self.ip_session = ip_session
        self.session = ssh.SSH(ip=ip_session)
        self.tn = telnet.Telnet(ip=ip_session)

    def ping(self, ip_dest):

        self.session.connect()
        self.session.send_cmd(f"ping {ip_dest}\r\n")
        output = self.session.read()
        # print(output)

        response = re.findall(r"Reply Received From :(\d+.\d+.\d+.\d+)", output)
        print(response)

        if response is not None:

            if ip_dest in response:

                print(f"Avem conexiune in {ip_dest}")

            else:

                print(f"Nu avem conexiune in {ip_dest}")

        else:

            print(f"Nu avem conexiune in {ip_dest}")

        self.session.close()

        return response


obj = PING(ip_session="10.2.109.136")
obj.ping(ip_dest="15.0.0.100")
obj.ping(ip_dest="15.0.0.88")
obj.ping(ip_dest="15.0.0.1")