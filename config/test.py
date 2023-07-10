import paramiko
import time


def connection(ip="10.2.109.178", username="admin", password="Admin1234!"):
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

def show_vlan_pagination_enable_disable(ip="10.2.109.198",username="admin", password = "Admin1234!"):

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to device

    ssh.connect(ip, username=username, password=password)
    shell = ssh.invoke_shell()
    time.sleep(1)
    shell.send("conf t\r\n")
    shell.send("set cli pagination off\r\n")
    shell.send("do show vlan\r\n")
    time.sleep(2)
    output = shell.recv(65535)
    print(output)



# connection()
show_vlan_pagination_enable_disable()