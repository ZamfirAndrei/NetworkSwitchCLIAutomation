from config import erps, fdb, infos, interfaces, ip, ospf, pch, ping, qinq, rip, stp, vlan


class DUT_Objects:

    def __init__(self, ip_session):

        # Storing the IP of the session
        self.ip_session = ip_session

        # Creating the objects

        self.fdb = fdb.FDB(ip_session=ip_session)
        self.erps = erps.ERPS(ip_session=ip_session)
        self.int = interfaces.Interface(ip_session=ip_session)
        self.vl = vlan.VLAN(ip_session=ip_session)
        self.stp = stp.STP(ip_session=ip_session)
        self.ip = ip.IP(ip_session=ip_session)
        self.rip = rip.RIP(ip_session=ip_session)
        self.ping = ping.PING(ip_session=ip_session)
        self.ospf = ospf.OSPF(ip_session=ip_session)
        self.pch = pch.PCH(ip_session=ip_session)
        self.inf = infos.INFOs(ip_session=ip_session)
        self.qinq = qinq.QinQ(ip_session=ip_session)
