import paramiko
import time

class SSH:


    def __init__(self, ip):

        # Create the ssh client

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ipSSH = ip
        self.shell = None

    def connect(self, username="admin", password="Admin1234!"):

        # Connect to the device
        try:

            self.ssh.connect(self.ipSSH, username=username, password=password, timeout=55)
            self.shell = self.ssh.invoke_shell()
            time.sleep(2)

        except Exception as e:
            print(e)

    def close(self):

        # Close the ssh connection

        self.ssh.close()

    def send_cmd(self, cmd):

        self.shell.send(cmd + "\r\n")
        # print(cmd)
        time.sleep(2)

    def read(self):

        # Read the prompt
        # time.sleep(1)
        output = str(self.shell.recv(65535))

        return output


ip_session = "10.2.109.238"

# session = SSH(ip=ip_session)
# session.connect()
# session.send_cmd(cmd="sh vlan")
# session.connect("admin", "Admin1234!")
# session.send_cmd(cmd="show ip int")
# session.send_cmd("ping 8.8.8.8")
# print(session.read())
# session.close()

