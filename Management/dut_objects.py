from config import erps, fdb, infos, interfaces, ip, ospf, pch, ping, qinq, rip, stp, vlan, sanity
from test_beds import test_bed_1
from Management import ssh, telnet

# dut1 = test_bed_1.DUT1
# dut2 = test_bed_1.DUT2
# dut3 = test_bed_1.DUT3


class DUT_Objects:

    def __init__(self, ip_session):

        # Storing the IP of the session
        self.ip_session = ip_session

        # Creating the objects

        self.fdb = fdb.FDB(ip_session=self.ip_session)
        self.erps = erps.ERPS(ip_session=self.ip_session)
        self.int = interfaces.Interface(ip_session=self.ip_session)
        self.vl = vlan.VLAN(ip_session=self.ip_session)
        self.stp = stp.STP(ip_session=self.ip_session)
        self.ip = ip.IP(ip_session=self.ip_session)
        self.rip = rip.RIP(ip_session=self.ip_session)
        self.ping = ping.PING(ip_session=self.ip_session)
        self.ospf = ospf.OSPF(ip_session=self.ip_session)
        self.pch = pch.PCH(ip_session=self.ip_session)
        self.inf = infos.INFOs(ip_session=self.ip_session)
        self.qinq = qinq.QinQ(ip_session=self.ip_session)
        self.sanity = sanity.Sanity(ip_session=self.ip_session)
        self.session = ssh.SSH(ip=self.ip_session)
        self.tn = telnet.Telnet(ip=self.ip_session)


class DUT_Objects_TestBed:

    def __init__(self, parameters):

        # Initialization of parameters

        self.ip_session = parameters["ip"]
        self.user = parameters["user"]
        self.password = parameters["password"]
        self.port = parameters["ports"]["h1value"][:2] + " " + parameters["ports"]["h1value"][2:]
        self.hostname = parameters["hostname"]

        # Creating the objects

        self.fdb = fdb.FDB(ip_session=self.ip_session)
        self.erps = erps.ERPS(ip_session=self.ip_session)
        self.int = interfaces.Interface(ip_session=self.ip_session)
        self.vl = vlan.VLAN(ip_session=self.ip_session)
        self.stp = stp.STP(ip_session=self.ip_session)
        self.ip = ip.IP(ip_session=self.ip_session)
        self.rip = rip.RIP(ip_session=self.ip_session)
        self.ping = ping.PING(ip_session=self.ip_session)
        self.ospf = ospf.OSPF(ip_session=self.ip_session)
        self.pch = pch.PCH(ip_session=self.ip_session)
        self.inf = infos.INFOs(ip_session=self.ip_session)
        self.qinq = qinq.QinQ(ip_session=self.ip_session)
        self.sanity = sanity.Sanity(ip_session=self.ip_session)
        self.session = ssh.SSH(ip=self.ip_session)
        self.tn = telnet.Telnet(ip=self.ip_session)