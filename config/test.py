import paramiko
import time
from config import vlan, interfaces, ip, ping
from Management import telnet


def connection(ip="10.2.109.238", username="admin", password="Admin1234!"):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to device

    ssh.connect(ip, username=username, password=password)
    shell = ssh.invoke_shell()
    time.sleep(1)
    shell.send("show ip int \r\n")
    shell.send("ping 8.8.8.8\r\n")
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
# show_vlan_pagination_enable_disable()

# ip_session = "10.2.109.238"
# vl = vlan.VLAN(ip_session=ip_session)
# int1 = interfaces.Interface(ip_session=ip_session)
#
#
# def exercitiu():
#
#
#     vl.create_vlan(vlan="150")
#     int1.no_shut_interface(interface="Gi 0/4")
#
#
# exercitiu()

d = {'15.0.0.0': {'Network': '15.0.0.0', 'Mask': '24', 'AD': '120', 'Metric': '2', 'Learned From': '20.0.0.1'},
      '88.0.0.0': {'Network': '88.0.0.0', 'Mask': '8', 'AD': '120', 'Metric': '4', 'Learned From': '20.0.0.1'}}

x = "Mask"
ip = "15.0.0.0"
# print(len(d))
# print(len(d.items()))
# print(len(d.keys()))
# print(d.values())
# print(d.keys())
# print(d["15.0.0.0"]["AD"])
# print(d[f'{ip}'][f'{x}'], "-----", ip,x)
#
# d1 = {}
#
# if "0.0.0.0" not in d1.keys():
#     print("Ok", d1)

def show_ip_route(ip="10.2.109.206", username="admin", password="Admin1234!"):

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to device

    ssh.connect(ip, username=username, password=password)
    shell = ssh.invoke_shell()
    time.sleep(1)
    shell.send("show ip route rip \r\n")
    time.sleep(1)
    output = shell.recv(65535)
    print(output)


# show_ip_route()
tn = telnet.Telnet(ip="10.2.109.206")
def show_ip_route_telnet(ip="10.2.109.206", username="admin", password="Admin1234!"):

    tn.connect(username=username, password=password)
    time.sleep(1)
    tn.write_cmd("conf t")
    tn.write_cmd("set cli pagination off")
    tn.write_cmd("do show ip route")
    time.sleep(2)
    output = tn.read()
    print(output)

show_ip_route_telnet()


d["Tete"] = "FULL/BACKUP"

if "FULLL" in d["Tete"]:
    print("Yes")
else:
    print("No")