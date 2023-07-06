import paramiko
import time

#username = "admin"
#password = "Admin1234!"


# Creez o clasa SSH, iar in interiorul ei voi creea mai multe functii

class SSH:

    # Functia de initializare in care  initializez variabilele ssh si ip. Pe acestea le voi utilia in
    # functiile de mai jos

    def __init__(self, ip):

        # Create the ssh client

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ipSSH = ip
        self.shell = None

    def connect(self, username="admin", password="Admin1234!"):

        # Connect to the device
        try:

            self.ssh.connect(self.ipSSH, username=username, password=password, timeout=15)
            self.shell = self.ssh.invoke_shell()
            time.sleep(1)

        except Exception as e:
            return e

    def close(self):

        # Close the ssh connection

        self.ssh.close()

    def send_cmd(self, cmd):

        self.shell.send(cmd + "\r\n")
        time.sleep(2)

    def read(self):

        # Read the prompt
        # time.sleep(1)
        output = str(self.shell.recv(65535))

        return output


# session = SSH("10.2.109.178")
# session.connect("admin", "Admin1234!")
# session.send_cmd("show ip int")
# session.send_cmd("ping 8.8.8.8")
# print(session.read())
# session.close()

