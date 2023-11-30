import telnetlib
import time


class Telnet:

    def __init__(self, ip):

        self.ip_session = ip
        self.telnet = None
    def connect(self, username="admin", password="Admin1234!"):

        try:

            #Connect to the device

            self.telnet = telnetlib.Telnet(self.ip_session)
            self.telnet.read_until(b"login: ", timeout=5)
            self.telnet.write(username.encode('ascii') + b"\r\n")
            self.telnet.read_until(b"Password: ", timeout=5)
            self.telnet.write(password.encode('ascii') + b"\r\n")
            self.telnet = self.telnet

            time.sleep(1)
        except Exception as e:
            return e

    def close(self):

        self.telnet.close()

    def write_cmd(self, cmd):

        self.telnet.write(cmd.encode("ascii") + b"\r\n")
        time.sleep(2)

    def read(self):

        # Read the output

        output = str(self.telnet.read_very_eager())

        return output


# session = Telnet("10.2.109.178")
# session.connect("admin", "Admin1234!")
# session.write_cmd("show ip int")
# print(session.read())