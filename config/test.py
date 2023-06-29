import paramiko
import time


def connection(ip="10.2.109.198", username="admin", password="Admin1234!"):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to device

    ssh.connect(ip, username=username, password=password)
    shell = ssh.invoke_shell()
    time.sleep(1)
    shell.send("show ip int \r\n")
    time.sleep(1)
    output = shell.recv(65535)
    print(output)



connection()
