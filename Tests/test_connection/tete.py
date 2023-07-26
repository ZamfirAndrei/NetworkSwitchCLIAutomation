import paramiko
import time
import telnetlib
import re


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

# x = ssh_session("10.2.109.178", "admin", "Admin1234!")
# print(x)


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

# y = telnet("10.2.109.178", "admin", "Admin1234!")
# print(y)


output = '''   Router Link States (Area 0.0.0.0)
                  ---------------------------------------
Link ID          ADV Router       Age        Seq#          Checksum  Link count
-------          ----------       ---        ----          --------  ----------
2.2.2.2          2.2.2.2          825        0x80000005    0x36c6    1

                  Summary Link States (Area 0.0.0.0)
                  ---------------------------------------
Link ID          ADV Router       Age        Seq#          Checksum
-------          ----------       ---        ----          --------
14.0.0.0         2.2.2.2          1316       0x80000002    0x9e86

16.0.0.0         2.2.2.2          1271       0x80000002    0x8e93

                  Router Link States (Area 0.0.0.1)
                  ---------------------------------------
Link ID          ADV Router       Age        Seq#          Checksum  Link count
-------          ----------       ---        ----          --------  ----------
1.1.1.1          1.1.1.1          1270       0x80000008    0x756c    2

2.2.2.2          2.2.2.2          825        0x80000006    0x7f7b    1

                  Network Link States (Area 0.0.0.1)
                  ---------------------------------------
Link ID          ADV Router       Age        Seq#          Checksum
-------          ----------       ---        ----          --------
14.0.0.2         2.2.2.2          1220       0x80000003    0xfb17

                  Summary Link States (Area 0.0.0.1)
                  ---------------------------------------
Link ID          ADV Router       Age        Seq#          Checksum
-------          ----------       ---        ----          --------
30.0.0.0         2.2.2.2          1311       0x80000003    0xcb48

                  NSSA External Link States (Area 0.0.0.1)
                  ----------------------------------------------
Link ID          ADV Router       Age        Seq#          Checksum
-------          ----------       ---        ----          --------
10.2.109.0       1.1.1.1          1270       0x80000005    0x39d4

15.0.0.0         1.1.1.1          1270       0x80000005    0xc3b4

18.0.0.0         1.1.1.1          1270       0x80000005    0x9cd8

35.35.35.0       1.1.1.1          1270       0x80000005    0x9687

100.0.0.0        2.2.2.2          824        0x80000002    0xc664

                  AS External Link States
                  -----------------------
Link ID          ADV Router       Age        Seq#          Checksum
-------          ----------       ---        ----          --------
10.2.109.0       2.2.2.2          825        0x80000004    0x75bd

15.0.0.0         2.2.2.2          825        0x80000004    0xff9d

18.0.0.0         2.2.2.2          825        0x80000004    0xd8c1

35.35.35.0       2.2.2.2          825        0x80000004    0xd270

100.0.0.0        2.2.2.2          824        0x80000002    0xef6b

'''


# match1 = re.findall(r"(\d+.\d+.\d+.\d+)\s+(\d+.\d+.\d+.\d+)\s+(\d+)", output)
# print(match1)
# print(len(match1))


lis = [{'Interface': 'vlan1', 'Status': 'Down', 'Protocol': 'Down'},
     {'Interface': 'vlan50', 'Status': 'Up', 'Protocol': 'Up'},
     {'Interface': 'vlan30', 'Status': 'Up', 'Protocol': 'Up'}]
# print(lis)
#
# for i in lis:
#     print(i)
#     # for j in i:
#     #     print(j)
#     if "vlan30" in i.values():
#         print("Da")
#     else:
#         print("Nu")
#
# for i in lis:
#     print(i)
#     for j in i.values():
#         print(j)
#         if "vlan30" == j:
#             print("Da")
#         else:
#             print("Nu")


def con(ip,username,password):

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
    print(output)
    return output


# con("10.2.109.239",username="admin",password="Admin1234!")

def add_ip_interfaces(*args, **kwargs):
    ok = 0
    for int_vlan in args:
        print(int_vlan)
        l = list(kwargs.values())
        print(l)
        print(l[ok])
        ok += 1





add_ip_interfaces("100", "110","120", int_vlan1_ip=["100.0.0.1", "255.255.0.0"], int_vlan2_ip=["110.0.0.1", "255.255.0.0"], int_vlan3_ip=["120.0.0.1", "255.255.0.0"])
# add_ip_interfaces("100","110","120")