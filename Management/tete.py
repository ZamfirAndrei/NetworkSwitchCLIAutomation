import paramiko
import time
import telnetlib

def ssh_session(ip,username,password):

    # Create a new SSH client

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to device

    ssh.connect(ip, username=username, password=password)
    shell = ssh.invoke_shell()
    time.sleep(1)

    shell.send("show ip int\r\n")
    time.sleep(1)
    output = shell.recv(65535)


    # Storing the variables ssh, shell
    return output

x = ssh_session("10.2.109.178", "admin", "Admin1234!")
#print(x)

def telnet(ip, username , password):

    tn = telnetlib.Telnet(ip)
    tn.read_until(b"login: ",timeout=10)
    tn.write(username.encode('ascii') + b"\r\n")
    tn.read_until(b"Password: ",timeout=10)
    tn.write(password.encode('ascii') + b"\r\n")
    time.sleep(1)
    tn.write(b"show ip int\r\n")
    time.sleep(2)
    output = tn.read_very_eager()#.decode("ascii")
    return output

y = telnet("10.2.109.178", "admin", "Admin1234!")
print(y)
