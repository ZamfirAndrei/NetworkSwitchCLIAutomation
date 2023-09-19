import time
import re

from Management import ssh, telnet


class PING:

    def __init__(self, ip_session="10.2.109.178"):

        print("Class PING")

        self.ip_session = ip_session
        self.session = ssh.SSH(ip=ip_session)
        self.tn = telnet.Telnet(ip=ip_session)

    def ping(self, ip_dest):

        self.session.connect()
        self.session.send_cmd(f"ping {ip_dest}")
        output = self.session.read()
        # print(output)

        response = re.findall(r"Reply Received From :(\d+.\d+.\d+.\d+)", output)
        print(response)

        if response is not None:

            if ip_dest in response:

                print(f"We have connection in {ip_dest}")

            else:

                print(f"We don't have connection in {ip_dest}")

        else:

            print(f"We don't have connection {ip_dest}")

        self.session.close()

        return response

    def ping_more(self, *args):

        self.session.connect()

        for ip_dest in args:
            self.session.send_cmd(f"ping {ip_dest}\r\n")
        output = self.session.read()
        # print(output)

        response = re.findall(r"Reply Received From :(\d+.\d+.\d+.\d+)", output)
        print(response)

        if response is not None:

            for ip_dest in args:

                if ip_dest in response:

                    print(f"We have connection in {ip_dest}")

                else:

                    print(f"We don't have connection in {ip_dest}")

        else:

            print(f"We don't have connection")

        self.session.close()

        return response


ip_session = "10.2.109.238"

# obj = PING(ip_session=ip_session)
# obj.ping(ip_dest="15.0.0.100")
# obj.ping(ip_dest="15.0.0.88")
# obj.ping(ip_dest="15.0.0.1")
# obj.ping_more("15.0.0.1","15.0.0.100","15.0.0.88", "6.0.0.1")