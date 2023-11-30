import re
from Management import ssh, telnet



'''The pattern `r"VLAN ID\s+:\s+(\d+)\S+Member Ports\s+:\s+([\w/,\s]+)\S+Untagged Ports\s+:\s+([\w/,\s]+)\S+
PBA Ports\s+:\s+([\w/,\s]+)\S+Name\s+:([\s\w]+)\S+Status\s+:\s+(\w+)\S+
Egress Ethertype\s+:\s+([\dx]+)\S"` is a regular expression pattern that is designed to match and extract 
specific information from a multiline string that follows a specific format. Let's break down the pattern:

- `VLAN ID\s+:\s+`: Matches the literal text "VLAN ID" followed by one or more whitespace characters, followed by a colon and one or more whitespace characters.
- `(\d+)`: Matches and captures one or more digits (numeric VLAN ID).
- `\S+`: Matches one or more non-whitespace characters (any characters except whitespace).
- `Member Ports\s+:\s+`: Matches the literal text "Member Ports" followed by one or more whitespace characters, followed by a colon and one or more whitespace characters.
- `([\w/,\s]+)`: Matches and captures a sequence of word characters, forward slashes, commas, and whitespace characters (member ports).
- `\S+`: Matches one or more non-whitespace characters.
- `Untagged Ports\s+:\s+`: Matches the literal text "Untagged Ports" followed by one or more whitespace characters, followed by a colon and one or more whitespace characters.
- `([\w/,\s]+)`: Matches and captures a sequence of word characters, forward slashes, commas, and whitespace characters (untagged ports).
- `\S+`: Matches one or more non-whitespace characters.
- `PBA Ports\s+:\s+`: Matches the literal text "PBA Ports" followed by one or more whitespace characters, followed by a colon and one or more whitespace characters.
- `([\w/,\s]+)`: Matches and captures a sequence of word characters, forward slashes, commas, and whitespace characters (PBA ports).
- `\S+`: Matches one or more non-whitespace characters.
- `Name\s+:([\s\w]+)`: Matches the literal text "Name" followed by a colon, and captures one or more word characters and whitespace characters (name).
- `\S+`: Matches one or more non-whitespace characters.
- `Status\s+:\s+(\w+)`: Matches the literal text "Status" followed by one or more whitespace characters, a colon, and captures one or more word characters (status).
- `\S+`: Matches one or more non-whitespace characters.
- `Egress Ethertype\s+:\s+([\dx]+)`: Matches the literal text "Egress Ethertype" followed by one or more whitespace characters, a colon, and captures one or more hexadecimal digits and 'x' character (egress ethertype).

In summary, this pattern is used to extract specific information related to VLAN configuration, including VLAN ID, member ports, untagged ports, PBA ports, name, status, and egress ethertype, from a multiline string that adheres to a specific format.'''


class VLAN:

    #session = ssh.SSH("10.2.109.178") # Creez obiectul session prin care ma conectez la DUT. Apoi il utiliez in functiile de VLAN

    def __init__(self, ip_session="10.2.109.178"):

        print("Class VLAN")

        self.ip_session = ip_session
        self.session = ssh.SSH(ip_session)  # Creez obiectul session prin care ma conectez la DUT. Apoi il utiliez in functiile de VLAN
                                    # ssh --> folderul unde am creat functiile de ssh,
                                    # .SSH --> apelez clasa din interiorul folderului ssh
        self.tn = telnet.Telnet(ip_session)

    def create_vlan(self, vlan):

        self.session.connect()
        output = self.session.read()
        conf = re.findall(r"config", output)
        #print(conf)
        if int(vlan) >= 4094:
            print("The limit is 4094")

        else:
            if "config" not in conf:
                self.session.send_cmd("!")
                self.session.send_cmd("conf t")
                self.session.send_cmd(f"vlan {vlan}")
                self.session.send_cmd("!")
                # print("1")
            else:
                self.session.send_cmd("!")
                self.session.send_cmd(f"vlan {vlan}")
                # print("2")
            print(f"The VLAN {vlan} was created on DUT {self.ip_session}")
        self.session.send_cmd("exit")
        # print(output)
        self.session.close()


    def create_vlans(self, *args):

        self.session.connect()
        output = self.session.read()
        conf = re.findall(r"config", output)
        # print(conf)

        for vlan in args:

            if int(vlan) >= 4094:
                print("The limit is 4094")

            else:
                if "config" not in conf:
                    self.session.send_cmd("!")
                    self.session.send_cmd("conf t")
                    self.session.send_cmd(f"vlan {vlan}")
                    self.session.send_cmd("!")
                    # print("1")
                else:
                    self.session.send_cmd("!")
                    self.session.send_cmd(f"vlan {vlan}")
                    # print("2")
                print(f"The VLAN {vlan} was created on DUT {self.ip_session}")
        self.session.send_cmd("exit")
        # print(output)
        self.session.close()

    def remove_vlan(self, vlan):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"no vlan {vlan}")
        self.session.send_cmd("exit")
        output = self.session.read()
        error = re.findall("% Vlan does not exist", output)
        # print(error)
        if "% Vlan does not exist" in error:
            print("The VLAN does not exist")
        else:
            print(f"The VLAN {vlan} has been removed succesfully from DUT {self.ip_session}")
        self.session.send_cmd("exit")
        # print(output)
        self.session.close()

    def remove_vlans(self, *args):

        self.session.connect()
        self.session.send_cmd("conf t")
        output = ""

        for vlan in args:

            self.session.send_cmd(f"no vlan {vlan}")
            output = self.session.read()
            error = re.findall("% Vlan does not exist", output)
            # print(error)
            if "% Vlan does not exist" in error:
                print("The VLAN does not exist")
            else:
                print(f"The VLAN {vlan} has been removed succesfully from DUT {self.ip_session}")
        self.session.send_cmd("exit")
        # print(output)
        self.session.close()

    def add_ports_to_vlan(self, ports, vlan):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"vlan {vlan}")
        self.session.send_cmd(f"port add {ports}")
        self.session.send_cmd("!")
        output = self.session.read()
        error = re.findall(r"% Invalid interface type", output)
        #print(error)
        if "% Invalid interface type" in error:
            print("The interface does not exist")
        else:
            print(f"The port {ports} is added succesfully on DUT {self.ip_session} for vlan {vlan}")
        # print(output)
        self.session.send_cmd("exit")
        # print(output)
        self.session.close()

    def remove_ports_from_vlan(self, ports, vlan):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"vlan {vlan}")
        self.session.send_cmd(f"no port {ports}")
        output = self.session.read()
        print(output)
        error1 = re.findall("Invalid portlist", output)
        error2 = re.findall("Port list has a port configured as trunk port", output)
        error3 = re.findall("One of the egress ports is also a member of the untagged port list", output)
        print(error1)
        print(error2)
        print(error3)

        if "Invalid portlist" in error1:
            if "Port list has a port configured as trunk port" in error2:
                print("We have to configure the port to be hybrid")
                self.session.send_cmd("!")
                self.session.send_cmd(f"int {ports}")
                self.session.send_cmd("sw mo hybrid")
                self.session.send_cmd("!")

            else:
                print("The port is not part of the VLAN membership")

        elif "One of the egress ports is also a member of the untagged port list" in error3:
            print("We have to remove the port from the untagged list too")
            self.session.send_cmd(f"no port {ports} untagged {ports}")
            self.session.send_cmd("!")

        else:
            print(f"The port {ports} has been removed from the VLAN {vlan}")
        self.session.send_cmd("exit")
        # print(output)
        self.session.close()

    def show_vlan(self, vlan=None):

        self.session.connect()
        d = {
            "VLAN ID" : "",
            "Member Ports" : "",
            "Untagged Ports": "" ,
            "PBA Ports" : "",
            "Name" : "",
            "Status": "",
            "Egress Ethertype": ""
        }
        all_out = ""

        if vlan is not None:
            self.session.send_cmd(f"show vlan id {vlan}")
            output = self.session.read()
            match = re.findall(r"VLAN ID\s+:\s+(\d+)\S+Member Ports\s+:\s+([\w/,\s]+)[\S\s]+Untagged Ports\s+:\s+([\w/,\s]+)\S+"
                               r"PBA Ports\s+:\s+([\w/,\s]+)\S+Name\s+:([\s\w]+)\S+Status\s+:\s+(\w+)\S+"
                               r"Egress Ethertype\s+:\s+([\dx]+)\S", output)

            # match = re.findall(r"VLAN ID\s+:\s+(\d+)\S+Member Ports\s+:\s+([\w/,\s]+)[\S\s]+Untagged Ports\s+:\s+([\w/,\s]+)\S+", output)
            # print(output)
            # print(match)
            # print(len(match))

            # Creez o lista cu cheile din dictionar

            # lista_keys = list()
            # for key in d.keys():
            #     lista_keys.append(key)
            #
            # print(lista_keys)

            # Varianta mai frumoasa

            for attribute in range(len(match)):
                # print(match[attribute])

                for key, value in zip(d.keys(), match[attribute]):
                    # print(key ,value)
                    d[key] = value.replace(" ","")

            # Variantele mai de la tara

            # for attribute in range(len(match)):
            #     for j in range(len(lista_keys)):
            #         d[lista_keys[j]] = match[attribute][j].replace(" ","")

            # i = 0
            # for key in d.keys():
            #     print(i)
            #     if i < len(d.keys()):
            #         d[key] = match[0][i]
            #         i += 1

            # print(d)

        else:

            self.session.send_cmd("conf t")
            self.session.send_cmd("set cli pagination off")
            self.session.send_cmd("do show vlan")
            output = self.session.read()
            # print(output)

        self.session.close()

        return d

    def show_vlan_port(self, port):

        self.session.connect()
        d = {
            "Port ":"",
            "Port VLAN ID":"",
            "Port Acceptable Frame Type":"",
            "Port Mode": "",
            "Port-and-Protocol Based Support":"",
            "Default Priority":"",
            "Port Protected Status ":"",
        }
        self.session.send_cmd(f"show vlan port {port}")
        output = self.session.read()
        # print(output)

        match = re.findall(r"Port\s+(\w+\d/\d+)\S+\s+Port\s+VLAN\s+ID\s+:\s+(\d+)\S+"
                           r"\s+Port\s+Acceptable\s+Frame\s+Type\s+:\s+([\w\s]+)\S+"
                           r"\s+Port\s+Mode\s+:\s+(\w+)\S+"
                           r"\s+Port-and-Protocol\s+Based\s+Support\s+:\s+(\w+)\S+"
                           r"\s+Default\s+Priority\s+:\s+(\d+)\S+"
                           r"\s+Port\s+Protected\s+Status\s+:\s+(\w+)", output)
        # match1 = re.findall(r"Port\s+(\w+\d/\d+).*?Port\sVLAN\sID\s+:\s+(\d+)", output) # E buna si varianta asta cu .*?
        # print(match)

        for key, value in zip(d.keys(), match[0]):
            # print(key, value)
            d[key] = value

        print(d)
        self.session.close()

        return d

    def add_more_ports_to_vlan(self, *args, vlan):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"vlan {vlan}")

        for arg in args:
            self.session.send_cmd(f"port add {arg}")

        self.session.send_cmd("!")
        output = self.session.read()
        error = re.findall(r"% Invalid interface type", output)
        #print(error)
        if "% Invalid interface type" in error:
            print("The interface does not exist")
        else:
            print(f"The port is added succesfully on DUT {self.ip_session}")
        # print(output)
        self.session.close()

    def add_more_ports_to_more_vlans(self, *args, **kwargs):

        self.session.connect()
        self.session.send_cmd("conf t")

        for vlan in args:

            # print(vlan)
            self.session.send_cmd(f"vlan {vlan}")
            # print(kwargs.items())
            # print(kwargs.values())
            # print(kwargs.keys())
            for port in kwargs.values():
                self.session.send_cmd(f"port add {port}")
                print(f"The port {port} is added successfully to vlan {vlan} on DUT {self.ip_session}")
            self.session.send_cmd("!")

        output = self.session.read()
        error = re.findall(r"% Invalid interface type", output)
        # print(error)
        if "% Invalid interface type" in error:
            print("The interface does not exist")

        # print(output)
        self.session.close()

    def add_more_ports_to_different_vlans(self, *args, **kwargs):

        self.session.connect()
        self.session.send_cmd("conf t")

        for vlan, port in zip(args, kwargs.values()):

            self.session.send_cmd(f"vlan {vlan}")
            self.session.send_cmd(f"port add {port}")
            self.session.send_cmd(f"!")

        output = self.session.read()
        error = re.findall(r"% Invalid interface type", output)
        # print(error)
        if "% Invalid interface type" in error:
            print("The interface does not exist")

        # print(output)
        self.session.close()


ip = "10.2.109.238"

# vlan = VLAN(ip_session=ip)
# vlan.create_vlan(vlan="430")
# vlan.remove_vlan(vlan="330")
# vlan.add_ports_to_vlan(ports="ex 0/5",vlan="330")
# vlan.remove_ports_from_vlan(ports="gi 0/4", vlan="2000")
# vlan.show_vlan_port(port="gi 0/13")
# print("###########################")
# vlan.show_vlan(vlan="2000")
# vlan.create_vlan(vlan="100")
# vlan.show_vlan(vlan="2")
# vlan.add_more_ports_to_vlan("Gi 0/4","Gi 0/3","Gi 0/5",vlan="14")
# vlan.add_more_ports_to_more_vlans("Gi 0/4","Gi 0/3","Gi 0/5", vlan1="23", vlan2="24",vlan3="25")

