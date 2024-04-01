import time
import re

from Management import ssh, telnet

session = ssh.SSH(ip="10.2.109.83")
username = "admin"
password = "Admin1234!"

img_soft = '''CNS Software Version : 5.1.0-e329, CNS Software Version : 5.0-r5, CNS Software Version : 5.0.1-r4, 
CNS Software Version : 5.0.1-r3, CNS Software Version : 4.3.1-r4, CNS Software Version : 4.4-r3 '''


def show_system_info():

    session.connect(username=username, password=password)
    session.send_cmd(cmd="conf t")
    session.send_cmd(cmd="set cli pagination off")
    session.send_cmd(cmd="do show system info")
    output = session.read()
    # print(output)

    software_version = re.findall(r"CNS Software Version\s+:\s+([\w.-]+)", output)
    model_name = re.findall(r"Model Name\s+:\s+([\w-]+)", output)

    return software_version, model_name


sw1, mn1 = show_system_info()
# sw1 = show_system_info()
print(sw1)
print(mn1)


