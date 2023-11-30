import time
from Management import dut_objects
from flows import rstpflow
from test_beds import test_bed_1

dut1 = test_bed_1.DUT1
dut2 = test_bed_1.DUT2
dut3 = test_bed_1.DUT3

DUT1 = dut_objects.DUT_Objects_TestBed(dut1)


# ip_session__1 = dut1["ip"]
# ip_session_2 = "10.2.109.83"
# ip_session_3 = "10.2.109.232"
# ip_session_4 = "10.2.109.100"
# ip_session_5 = "10.2.109.113"


class TestBed:

    def test_func_1(self):
        print("###### Test_func_1 ######")
        print("########## Test with Test Bed #############")
        print("###### 2 DUTs ######")

        #    Topology
        #
        #  DUT1 -- DUT2

        # print(ip_session__1)
        #
        # rstp_flow.create_rstp_configuration_1_LINK_2_DUTs(DUT1, dut1["ports"]["v1value"], "10", "20", "30", "rst")
        # rstp_flow.create_rstp_configuration_1_LINK_2_DUTs(DUT2, dut2["ports"]["v1value"], "10", "20", "30", "rst", dut2["ports"]["h3value"])

        # DUT1.vl.create_vlan(vlan="3000")
        print(DUT1.ip_session)
        print(DUT1.hostname)
