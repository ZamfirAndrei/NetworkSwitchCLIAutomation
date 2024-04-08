import re
import time

from Management import ssh, telnet


class OSPF:

    def __init__(self, ip_session="10.2.109.178"):

        print("Class OSPF")

        self.ip_session = ip_session
        self.session = ssh.SSH(ip_session)
        self.tn = telnet.Telnet(ip_session)

    def enable_ospf(self):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("router ospf")
        self.session.send_cmd("exit")
        print(f"The OSPF process has been enabled on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def disable_ospf(self):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("no router ospf")
        self.session.send_cmd("exit")
        print(f"The OSPF process has been disabled on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def advertise_network(self, ip_network=None, area=None):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("router ospf")
        self.session.send_cmd(f"network {ip_network} area {area}")
        self.session.send_cmd("exit")
        print(f"The network {ip_network} has been advertised in ospf in area {area} on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def advertise_networks(self, **kwargs):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("router ospf")
        for item in kwargs.values():
            self.session.send_cmd(f"network {item[0]} area {item[1]}")
            print(f"The network {item[0]} has been advertised in ospf on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def add_default_information_originate(self, nssa=None, metric=None, metric_type=None, area=None):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("router ospf")

        if nssa is not None:

            if metric is not None and metric_type is None:
                self.session.send_cmd(f"area {area} nssa default-information-originate metric {metric}")
                print(f"The default route has been redistributed with metric {metric} in nssa area {area} on DUT {self.ip_session}")

            elif metric_type is not None and metric is None:
                self.session.send_cmd(f"area {area} nssa default-information-originate metric-type {metric_type}")
                print(f"The default route has been redistributed with metric-type {metric_type} in nssa area {area} on DUT {self.ip_session}")

            elif metric is not None and metric_type is not None:
                self.session.send_cmd(f"area {area} nssa default-information-originate metric {metric} metric-type {metric_type}")
                print(f"The default route has been redistributed with metric {metric} and metric-type {metric_type} in nssa area {area} on DUT {self.ip_session}")
            else:
                self.session.send_cmd(f"area {area} nssa default-information-originate")
                print(f"The default route has been redistributed in nssa area {area} on DUT {self.ip_session}")

        if nssa is None:

            if metric is not None and metric_type is None:
                self.session.send_cmd(f"default-information originate always metric {metric}")
                print(f"The default route has been redistributed with metric {metric} on DUT {self.ip_session}")

            elif metric_type is not None and metric is None:
                self.session.send_cmd(f"default-information originate always metric-type {metric_type}")
                print(f"The default route has been redistributed with metric-type {metric_type} on DUT {self.ip_session}")

            elif metric is not None and metric_type is not None:
                self.session.send_cmd(f"default-information originate always metric {metric} metric-type {metric_type}")
                print(f"The default route has been redistributed with metric {metric} and metric-type {metric_type} on DUT {self.ip_session}")
            else:
                self.session.send_cmd(f"default-information originate always")
                print(f"The default route has been redistributed on DUT {self.ip_session}")

        output = self.session.read()
        # print(output)
        self.session.close()

    def remove_default_information_originate(self, nssa=None, area=None):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("router ospf")

        if nssa is not None:

            self.session.send_cmd(f"no area {area} nssa default-information-originate")
            print(f"The default route has been removed from nssa area {area} from DUT {self.ip_session}")

        else:

            self.session.send_cmd(f"no default-information originate always")
            print(f"The default route has been removed from DUT {self.ip_session}")

        output = self.session.read()
        # print(output)
        self.session.close()

    def remove_network(self, ip_network=None, area=None):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("router ospf")
        self.session.send_cmd(f"no network {ip_network} area {area}")
        self.session.send_cmd("exit")
        print(f"The network {ip_network} has been removed from ospf process on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def remove_networks(self, **kwargs):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("router ospf")
        for item in kwargs.values():
            self.session.send_cmd(f"no network {item[0]} area {item[1]}")
            print(f"The network {item[0]} has been removed from ospf on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def redistribute_connected(self, metric_type=None, metric=None):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("router ospf")

        if metric is None and metric_type is None:
            self.session.send_cmd("redistribute connected")
            print(f"The connected routes have been redistributed into ospf process on DUT {self.ip_session}")

        if metric is not None:

            if metric_type is not None:

                self.session.send_cmd(f"redistribute connected metric {metric} metric-type {metric_type}")
                print(f"The connected routes have been redistributed into ospf process on DUT {self.ip_session} with metric {metric} and metric_type {metric_type}")
            else:
                self.session.send_cmd(f"redistribute connected metric {metric}")
                print(f"The connected routes have been redistributed into ospf process on DUT {self.ip_session} with metric {metric}")

        if metric_type is not None and metric is None:
            self.session.send_cmd(f"redistribute connected metric-type {metric_type}")
            print(f"The connected routes have been redistributed into ospf process on DUT {self.ip_session} with metric_type {metric_type}")

        # time.sleep(2)
        output = self.session.read()
        # print(output)
        self.session.close()

    def redistribute_static(self, metric_type=None,metric=None):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("router ospf")

        if metric is None and metric_type is None:

            self.session.send_cmd("redistribute static")
            print(f"The static routes have been redistributed into ospf process on DUT {self.ip_session}")

        if metric is not None:

            if metric_type is not None:

                self.session.send_cmd(f"redistribute static metric {metric} metric-type {metric_type}")
                print(f"The static routes have been redistributed into ospf process on DUT {self.ip_session} with metric {metric} and metric_type {metric_type}")
            else:
                self.session.send_cmd(f"redistribute static metric {metric}")
                print(f"The static routes have been redistributed into ospf process on DUT {self.ip_session} with metric {metric}")

        if metric_type is not None and metric is None:

            self.session.send_cmd(f"redistribute static metric-type {metric_type}")
            print(f"The static routes have been redistributed into ospf process on DUT {self.ip_session} with metric_type {metric_type}")

        self.session.send_cmd("exit")
        output = self.session.read()
        # print(output)
        self.session.close()

    def redistribute_all(self, metric_type=None):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("router ospf")

        if metric_type is None:
            self.session.send_cmd("redistribute all")
        else:
            self.session.send_cmd(f"redistribute all metric-type {metric_type}")
        self.session.send_cmd("exit")
        print("All routes have been redistributed into ospf process")
        output = self.session.read()
        # print(output)
        self.session.close()

    def redistribute_rip(self, metric_type=None):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("router ospf")

        if metric_type is None:
            self.session.send_cmd("redistribute rip")
            print(f"RIP routes have been redistributed into ospf process on DUT {self.ip_session}")
        else:
            self.session.send_cmd(f"redistribute rip metric-type {metric_type}")
            print(f"RIP routes have been redistributed into ospf process with metric-type {metric_type} on DUT {self.ip_session}")

        self.session.send_cmd("exit")

        output = self.session.read()
        # print(output)
        self.session.close()

    def remove_redistribute_connected(self):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("router ospf")
        self.session.send_cmd("no redistribute connected")
        self.session.send_cmd("exit")
        print(f"The connected networks have been removed from ospf process on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def remove_redistribute_static(self):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("router ospf")
        self.session.send_cmd("no redistribute static")
        self.session.send_cmd("exit")
        print(f"The static routes have been removed from ospf process on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def remove_redistribute_all(self):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("router ospf")
        self.session.send_cmd("no redistribute all")
        self.session.send_cmd("exit")
        print(f"All routes have been removed from ospf process on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def remove_redistribute_rip(self):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("router ospf")
        self.session.send_cmd("no redistribute rip")
        self.session.send_cmd("exit")
        print(f"RIP routes have been removed from ospf process on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def add_router_id(self, router_id):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("router ospf")
        self.session.send_cmd(f"router-id {router_id}")
        self.session.send_cmd("exit")
        # time.sleep(2)
        print(f"Router-id {router_id} has been configured on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def remove_router_id(self):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("router ospf")
        self.session.send_cmd("no router-id")
        self.session.send_cmd("exit")
        print(f"Router-id has been removed from DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def configure_network_type(self, network_type, interface=None, int_vlan=None):

        self.session.connect()
        self.session.send_cmd("conf t")

        if int_vlan is not None:

            self.session.send_cmd(f"int vlan {int_vlan}")
            self.session.send_cmd(f"ip ospf network {network_type}")
            self.session.send_cmd("exit")
            print(f"The network type {network_type} has been configured on interface vlan {int_vlan} on DUT {self.ip_session}")

        if interface is not None:

            self.session.send_cmd(f"int {interface}")
            self.session.send_cmd(f"ip ospf network {network_type}")
            self.session.send_cmd("exit")
            print(f"The network type {network_type} has been configured on interface {interface} on DUT {self.ip_session}")

        output = self.session.read()
        # print(output)
        self.session.close()

    def remove_network_type(self, interface=None, int_vlan=None):

        self.session.connect()
        self.session.send_cmd("conf t")

        if int_vlan is not None:

            self.session.send_cmd(f"int vlan {int_vlan}")
            self.session.send_cmd(f"no ip ospf network")
            self.session.send_cmd("exit")
            print(f"The network type has been removed from interface vlan {int_vlan} on DUT {self.ip_session}")

        if interface is not None:

            self.session.send_cmd(f"int {interface}")
            self.session.send_cmd(f"no ip ospf network")
            self.session.send_cmd("exit")
            print(f"The network type has been removed from interface {interface} on DUT {self.ip_session}")

        output = self.session.read()
        # print(output)

        if "% Configured Neighbours present on this interface, If Type not set" in output:

            print("You have to remove the neighbors first")

        self.session.close()

    def configure_neighbor(self, neighbor):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("router ospf")
        self.session.send_cmd(f"neighbor {neighbor}")
        self.session.send_cmd("exit")
        # time.sleep(2)
        print(f"The neighbor {neighbor} has been configured on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def remove_neighbor(self, neighbor):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("router ospf")
        self.session.send_cmd(f"no neighbor {neighbor}")
        self.session.send_cmd("exit")
        # time.sleep(2)
        print(f"The neighbor {neighbor} has been removed on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def configure_neighbors(self, *args):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("router ospf")

        for neighbor in args:

            self.session.send_cmd(f"neighbor {neighbor}")
            print(f"The neighbor {neighbor} has been configured on DUT {self.ip_session}")

        self.session.send_cmd("exit")
        output = self.session.read()
        # print(output)
        self.session.close()

    def remove_neighbors(self, *args):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("router ospf")

        for neighbor in args:

            self.session.send_cmd(f"no neighbor {neighbor}")
            print(f"The neighbor {neighbor} has been removed on DUT {self.ip_session}")

        self.session.send_cmd("exit")
        output = self.session.read()
        # print(output)
        self.session.close()

    def show_ip_ospf_neighbors_detail(self):

        # Need to add this function

        self.session.connect()
        self.session.send_cmd("show ip ospf neighbor detail")
        output = self.session.read()
        # print(output)

        self.session.close()

    def show_ip_ospf_interface(self, interface=None, int_vlan=None):

        self.session.connect()

        if int_vlan is not None:

            self.session.send_cmd(f"show ip ospf interface vlan {int_vlan}")

        if interface is not None:
            self.session.send_cmd(f"show ip ospf interface {interface}")

        output = self.session.read()
        # print(output)

        network_type = re.findall(r"Network\s+Type\s+([NBMABROADCASTPointToMultiPointPointToPoint]+)", output)
        # print(network_type)

        self.session.close()

        return network_type

    def add_nssa_area(self, area):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("router ospf")
        self.session.send_cmd(f"area {area} nssa")
        self.session.send_cmd("exit")
        print(f"The nssa area {area} has been created on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def remove_nssa_area(self, area):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("router ospf")
        self.session.send_cmd(f"no area {area} nssa")
        self.session.send_cmd("exit")
        print(f"The nssa area has been removed from DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def add_network_summarize(self, network, mask, area):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("router ospf")
        self.session.send_cmd(f"summary-address {network} {mask} {area}")
        self.session.send_cmd("exit")
        print(f"The addresses have been summarized into {network} and mask {mask} on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def remove_network_summarize(self, network, mask, area):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("router ospf")
        self.session.send_cmd(f"no summary-address {network} {mask} {area}")
        self.session.send_cmd("exit")
        print(f"The summarization of {network} has been removed on DUT {self.ip_session}")
        output = self.session.read()
        # print(output)
        self.session.close()

    def add_passive_interface(self, vlan =None, interface=None):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("router ospf")

        if vlan is None:

            self.session.send_cmd(f"passive-interface {interface}")
            print(f"The passive-interface on interface {interface} has been configured on DUT {self.ip_session}")

        else:

            self.session.send_cmd(f"passive-interface vlan {vlan}")
            print(f"The passive-interface on vlan {vlan} has been configured on DUT {self.ip_session}")
        self.session.send_cmd("exit")

        output = self.session.read()
        # print(output)
        self.session.close()

    def remove_passive_interface(self, vlan=None, interface=None):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("router ospf")

        if vlan is None:

            self.session.send_cmd(f"no passive-interface {interface}")
            print(f"The passive-interface on interface {interface} has been removed from DUT {self.ip_session}")

        else:

            self.session.send_cmd(f"no passive-interface vlan {vlan}")
            print(f"The passive-interface on vlan {vlan} has been removed from DUT {self.ip_session}")
        self.session.send_cmd("exit")

        output = self.session.read()
        # print(output)
        self.session.close()

    def redist_config(self, network, network_mask, metric_type=None, metric_value=None, tag=None):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("router ospf")

        if metric_type is None and metric_value is None and tag is None:

            self.session.send_cmd(f"redist-config {network} {network_mask}")
            print(f"The network {network} has been redistributed")

        if metric_value is not None:

            self.session.send_cmd(f"redist-config {network} {network_mask} metric-value {metric_value}")
            print(f"The network {network} has been redistributed with the metric-value {metric_value}")

        if tag is not None:
            self.session.send_cmd(f"redist-config {network} {network_mask} tag {tag}")
            print(f"The network {network} has been redistributed with the tag {tag}")

        if metric_type is not None:
            self.session.send_cmd(f"redist-config {network} {network_mask} metric-type {metric_type}")
            print(f"The network {network} has been redistributed with the metric-type {metric_type}")

        self.session.send_cmd("exit")
        output = self.session.read()
        # print(output)
        self.session.close()

    def remove_redist_config(self, network, network_mask, metric_type=None, metric_value=None, tag=None):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("router ospf")
        self.session.send_cmd(f"no redist-config {network} {network_mask}")
        self.session.send_cmd("exit")
        print(f"The network {network} with the tag {tag} has been removed from redistribution")
        output = self.session.read()
        # print(output)
        self.session.close()

    def add_ip_ospf_authentication(self, int_vlan, authentication=None, authentication_key=None, message_digest_key=None, message_digest=None):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"int vlan {int_vlan}")

        if authentication == "simple" and message_digest_key is None:

            self.session.send_cmd(f"ip ospf authentication {authentication}")
            self.session.send_cmd(f"ip ospf authentication-key {authentication_key}")
            print(f"The mode {authentication} and key {authentication_key} have been configured on int_vlan {int_vlan} on DUT {self.ip_session}")

        if message_digest_key is not None:

            if message_digest is not None:

                self.session.send_cmd(f"ip ospf message-digest-key {message_digest_key} {authentication} {authentication_key}")
                self.session.send_cmd(f"ip ospf authentication message-digest")
                print(f"The mode message-digest, key {authentication_key} and message-digest-key {message_digest_key} have been configured on int_vlan {int_vlan} on DUT {self.ip_session}")

            else:

                self.session.send_cmd(f"ip ospf message-digest-key {message_digest_key} {authentication} {authentication_key}")
                self.session.send_cmd(f"ip ospf authentication {authentication}")
                print(f"The mode {authentication}, key {authentication_key} and message-digest-key {message_digest_key} have been configured on int_vlan {int_vlan} on DUT {self.ip_session}")

        self.session.send_cmd("exit")
        output = self.session.read()
        # print(output)

        self.session.close()

    def add_ip_ospf_authentication_key(self, int_vlan, authentication_key=None):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"int vlan {int_vlan}")
        self.session.send_cmd(f"ip ospf authentication-key {authentication_key}")
        print(f"The key {authentication_key} have been configured on int_vlan {int_vlan} on DUT {self.ip_session}")

        self.session.send_cmd("exit")
        output = self.session.read()
        # print(output)

        self.session.close()

    def remove_ip_ospf_authentication(self, int_vlan):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"int vlan {int_vlan}")
        self.session.send_cmd(f"no ip ospf authentication")
        print(f"The authentication has been removed from int_vlan {int_vlan} on DUT {self.ip_session}")

        self.session.send_cmd("exit")
        output = self.session.read()
        # print(output)

        self.session.close()

    def remove_ip_ospf_authentication_key(self, int_vlan, message_digest_key=None):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"int vlan {int_vlan}")

        if message_digest_key is None:

            self.session.send_cmd(f"no ip ospf authentication-key")
            print(f"The authentication key has been removed from int_vlan {int_vlan} on DUT {self.ip_session}")

        else:

            self.session.send_cmd(f"no ip ospf message-digest-key {message_digest_key}")
            print(f"The message-digest-key {message_digest_key} has been removed from int_vlan {int_vlan} on DUT {self.ip_session}")

        self.session.send_cmd("exit")
        output = self.session.read()
        # print(output)

        self.session.close()

    def add_ip_ospf_hello_interval(self, int_vlan, interval):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"int vlan {int_vlan}")
        self.session.send_cmd(f"ip ospf hello-interval {interval}")
        print(f"The hello-interval {interval} has been added on DUT {self.ip_session}")
        self.session.send_cmd("exit")
        output = self.session.read()
        # print(output)

        self.session.close()

    def remove_ip_ospf_hello_interval(self, int_vlan):

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd(f"int vlan {int_vlan}")
        self.session.send_cmd(f"no ip ospf hello-interval")
        print(f"The hello-interval has been removed from DUT {self.ip_session}")
        self.session.send_cmd("exit")
        output = self.session.read()
        # print(output)

        self.session.close()

    def show_ospf_neighbors(self):

        dict_of_ospf_neighbors = {}

        d_ospf_neighbors = {

            "Neighbor-ID": "",
            "Pri": "",
            "State": "",
            "DeadTime": "",
            "Address": "",
            "Interface": "",

        }

        list_ospf_neighbors = list()

        self.session.connect()
        self.session.send_cmd("show ip ospf neighbor")
        output = self.session.read()
        # print(output)

        match = re.findall(r"(\d+.\d+.\d+.\d+)\s+(\d+)\s+(\w+/\w+)\s+(\d+)\s+(\d+.\d+.\d+.\d+)\s+([\w\d/]+)", output)
        # print(match)

        for attribute in match:

            d = {}

            for key, value in zip(d_ospf_neighbors.keys(), attribute):

                d[key] = value

            list_ospf_neighbors.append(d)
            dict_of_ospf_neighbors[d["Neighbor-ID"]] = d
        # print(list_ospf_neighbors)

        self.session.close()

        return list_ospf_neighbors, dict_of_ospf_neighbors

    def show_run_ospf_key(self):

        dict_key = {}
        dict_of_keys = {}
        self.session.connect()
        self.session.send_cmd("show run ospf")
        output = self.session.read()
        # print(output)

        match = re.findall(r'ip ospf message-digest-key\s+(\d)+\s+([shamd5\S\d]+)([\s\w]+)', output)
        print(match)
        # print(len(match[0][2]))
        # key_text = match[0][2]

        for item in range(len(match)):

            dict_key[f"key {match[item][0]}"] = match[item][0]
            dict_key["Authentication"] = match[item][1]
            dict_key["key_Text"] = match[item][2]

            dict_of_keys[f"key {match[item][0]}"] = dict_key
            dict_key = {}

        # print(dict_of_keys)
        self.session.close()

        return dict_key, dict_of_keys

    def show_ip_ospf_database(self, database=None):

        # list_ospf_database = list()
        dict_ospf_database_router = dict()
        dict_ospf_database_network = dict()
        dict_ospf_database_summary = dict()
        dict_ospf_database_asbr = dict()
        dict_ospf_database_nssa = dict()
        dict_ospf_database_external = dict()

        self.session.connect()
        self.session.send_cmd("conf t")
        self.session.send_cmd("set cli pagination off")

        if database == "router":

            self.session.send_cmd(f"do show ip ospf database {database}")
            output = self.session.read()
            # print(output)

            area = re.findall(r"Router Link States\s\SArea\s+(\d+.\d+.\d+.\d+)", output)
            link_state_id = re.findall(r"Link State ID\s+:\s+(\d+.\d+.\d+.\d+)", output)
            adv_router = re.findall(r"Advertising Router\s+:\s+(\d+.\d+.\d+.\d+)", output)
            ls_type = re.findall(r"LS Type\s+:\s+(Router Links)", output)

            # print(area)
            # print(link_state_id)
            # print(adv_router)
            # print(ls_type)

            d = {}

            for attribute, id, adv, type in zip(area, link_state_id, adv_router, ls_type):

                d["Area"] = attribute
                d["Link State ID"] = id
                d["Advertising Router"] = adv
                d["LS Type"] = type
                # print(d)
                dict_ospf_database_router[id] = d
                d = {}

            # print(dict_ospf_database_router)

        elif database == "network":

            self.session.send_cmd(f"do show ip ospf database {database}")
            output = self.session.read()
            # print(output)

            area = re.findall(r"Network Link States\s\SArea\s+(\d+.\d+.\d+.\d+)", output)
            link_state_id = re.findall(r"Link State ID\s+:\s+(\d+.\d+.\d+.\d+)", output)
            adv_router = re.findall(r"Advertising Router\s+:\s+(\d+.\d+.\d+.\d+)", output)
            ls_type = re.findall(r"LS Type\s+:\s+(Network Links)", output)

            # print(area)
            # print(link_state_id)
            # print(adv_router)
            # print(ls_type)

            d = {}

            for attribute, id, adv, type in zip(area, link_state_id, adv_router, ls_type):

                d["Area"] = attribute
                d["Link State ID"] = id
                d["Advertising Router"] = adv
                d["LS Type"] = type
                # print(d)
                dict_ospf_database_network[id] = d
                d = {}

            # print(dict_ospf_database_network)

        elif database == "summary":

            self.session.send_cmd(f"do show ip ospf database {database}")
            output = self.session.read()
            # print(output)

            area = re.findall(r"Summary Link States\s\SArea\s+(\d+.\d+.\d+.\d+)", output)
            link_state_id = re.findall(r"Link State ID\s+:\s+(\d+.\d+.\d+.\d+)", output)
            adv_router = re.findall(r"Advertising Router\s+:\s+(\d+.\d+.\d+.\d+)", output)
            ls_type = re.findall(r"LS Type\s+:\s+(Summary Links\SNetwork\S)", output)

            # print(area)
            # print(link_state_id)
            # print(adv_router)
            # print(ls_type)

            d = {}

            for attribute, id, adv, type in zip(area, link_state_id, adv_router, ls_type):

                d["Area"] = attribute
                d["Link State ID"] = id
                d["Advertising Router"] = adv
                d["LS Type"] = type

                # print(d)
                dict_ospf_database_summary[id] = d
                d = {}

            # print(dict_ospf_database_summary)

        elif database == "asbr":

            self.session.send_cmd(f"do show ip ospf database {database}")
            output = self.session.read()
            # print(output)

            link_state_id = re.findall(r"Link State ID\s+:\s+(\d+.\d+.\d+.\d+)", output)
            adv_router = re.findall(r"Advertising Router\s+:\s+(\d+.\d+.\d+.\d+)", output)
            ls_type = re.findall(r"LS Type\s+:\s+(Summary Links\SAS Boundary Router\S)", output)

            # print(link_state_id)
            # print(adv_router)
            # print(ls_type)

            d = {}

            for id, adv, type in zip(link_state_id, adv_router, ls_type):

                d["Link State ID"] = id
                d["Advertising Router"] = adv
                d["LS Type"] = type
                # print(d)
                dict_ospf_database_asbr[id] = d
                d = {}

            # print(dict_ospf_database_asbr)

        elif database == "nssa":

            self.session.send_cmd(f"do show ip ospf database {database}")
            output = self.session.read()
            # print(output)

            area = re.findall(r"NSSA External Link States\s\SArea\s+(\d+.\d+.\d+.\d+)", output)
            link_state_id = re.findall(r"Link State ID\s+:\s+(\d+.\d+.\d+.\d+)", output)
            adv_router = re.findall(r"Advertising Router\s+:\s+(\d+.\d+.\d+.\d+)", output)
            ls_type = re.findall(r"LS Type\s+:\s+(NSSA\s+External\s+Link)", output) # Trb pus Regexul care trebuie

            # print(area)
            # print(link_state_id)
            # print(adv_router)
            print(ls_type)

            d = {}

            for attribute, id, adv, type in zip(area, link_state_id, adv_router, ls_type):

                d["Area"] = attribute
                d["Link State ID"] = id
                d["Advertising Router"] = adv
                d["LS Type"] = type

                # print(d)
                dict_ospf_database_nssa[id] = d
                d = {}

            # print(dict_ospf_database_nssa)

        elif database == "external":

            self.session.send_cmd(f"do show ip ospf database {database}")
            output = self.session.read()
            # print(output)

            link_state_id = re.findall(r"Link State ID\s+:\s+(\d+.\d+.\d+.\d+)", output)
            adv_router = re.findall(r"Advertising Router\s+:\s+(\d+.\d+.\d+.\d+)", output)
            ls_type = re.findall(r"LS Type\s+:\s+(AS\s+External\s+Link)", output)

            # print(link_state_id)
            # print(adv_router)
            # print(ls_type)

            d = {}

            for id, adv, type in zip(link_state_id, adv_router, ls_type):

                d["Link State ID"] = id
                d["Advertising Router"] = adv
                d["LS Type"] = type
                # print(d)
                dict_ospf_database_external[id] = d
                d = {}

            # print(dict_ospf_database_external)

        else:

            self.session.send_cmd(f"do show ip ospf database")
            output = self.session.read()
            # print(output)

        self.session.close()

        return dict_ospf_database_router, dict_ospf_database_network, \
               dict_ospf_database_summary, dict_ospf_database_asbr, \
               dict_ospf_database_nssa, dict_ospf_database_external

    def show_ip_route_ospf(self):

        dict_ospf_routes = {}

        self.session.connect()
        self.session.send_cmd(cmd="show ip route ospf")
        self.session.send_cmd(cmd="exit")
        output = self.session.read()
        # print(output)

        match = re.findall(r"(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})/(\d{1,2})\s+\S(\d{1,3})/(\d+)\S\s+via\s+(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})", output)
        # print(match)

        for item in match:

            dict_ospf_route = {}

            dict_ospf_route["Network"] = item[0]
            dict_ospf_route["Mask"] = item[1]
            dict_ospf_route["AD"] = item[2]
            dict_ospf_route["Metric"] = item[3]
            dict_ospf_route["Learned From"] = item[4]

            # print(dict_rip_route)
            dict_ospf_routes[item[0]] = dict_ospf_route

        # print(dict_ospf_routes)
        self.session.close()

        return dict_ospf_routes


ip = "10.2.109.238"

# ospf_obj = OSPF(ip_session=ip)
# ospf_obj.enable_ospf()
# ospf_obj.disable_ospf()
# ospf_obj.advertise_network(ip_network="4.0.0.1",area="0.0.0.0")
# ospf_obj.advertise_network(ip_network="14.0.0.2",area="0.0.0.1")
# ospf_obj.remove_network(ip_network="30.0.0.1",area="0.0.0.0")
# ospf_obj.redistribute_all()
# ospf_obj.redistribute_connected(metric_type="1")
# ospf_obj.redistribute_rip(metric_type="1")
# ospf_obj.redistribute_static(metric_type="1")
# ospf_obj.remove_redistribute_rip()
# ospf_obj.remove_redistribute_connected()
# ospf_obj.remove_redistribute_static()
# ospf_obj.add_router_id(router_id="1.1.1.1")
# ospf_obj.remove_router_id()
# ospf_obj.remove_passive_interface(vlan="30")
# ospf_obj.add_passive_interface(vlan="30")
# ospf_obj.add_passive_interface(interface="gi 0/3")
# ospf_obj.remove_passive_interface(interface="gi 0/3")
# ospf_obj.remove_nssa_area(area="0.0.0.1")
# ospf_obj.add_nssa_area(area="0.0.0.1")
# ospf_obj.redist_config(network="30.0.0.0",network_mask="255.255.255.0",tag="200")
# ospf_obj.remove_redist_config(network="30.0.0.0",network_mask="255.255.255.0")
# ospf_obj.show_ospf_neighbors()
# ospf_obj.show_ospf_database(database="summary")
