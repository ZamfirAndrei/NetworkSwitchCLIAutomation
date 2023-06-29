import telnetlib
import time


class Telnet:

    def __init__(self,ip):

        self.telnet = telnetlib.Telnet(ip)

    def connect(self, username, password):

        try:

            #Connect to the device

            self.telnet.read_until(b"login: ", timeout=5)
            self.telnet.write(username.encode('ascii') + b"\r\n")
            self.telnet.read_until(b"Password: ", timeout=5)
            self.telnet.write(password.encode('ascii') + b"\r\n")
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