import time
from Management import dut_objects
from flows import rstpflow
from test_beds import test_bed_1

dut1 = test_bed_1.DUT1
dut2 = test_bed_1.DUT2
dut3 = test_bed_1.DUT3

DUT1 = dut_objects.DUT_Objects_TestBed(dut1)
DUT2 = dut_objects.DUT_Objects_TestBed(dut2)
DUT3 = dut_objects.DUT_Objects_TestBed(dut3)

rstp_flow = rstpflow.RSTPFlow()


# ip_session__1 = dut1["ip"]
# ip_session_2 = "10.2.109.83"
# ip_session_3 = "10.2.109.232"
# ip_session_4 = "10.2.109.100"
# ip_session_5 = "10.2.109.113"
ip_session_6 = "10.2.109.173"

DUT6 = dut_objects.DUT_Objects(ip_session=ip_session_6)


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
        print(DUT1.ports)
        print(DUT1.ports["v1"])
        print(DUT1.user)

        rstp_flow.create_rstp_configuration_1_LINK_2_DUTs(DUT1, DUT1.ports['v1'],"10","20","30","rstp")
        rstp_flow.create_rstp_configuration_1_LINK_2_DUTs(DUT2, DUT2.ports['v1'], "10", "20", "30", "rstp")

        # Check the default Root Bridge (the lowest MAC in the topology - DUT1)

        d_root_id_1, d_bridge_id_1, ports_1, dict_of_ports_1 = DUT1.stp.show_spanning_tree_rstp()
        d_root_id_2, d_bridge_id_2, ports_2, dict_of_ports_2 = DUT2.stp.show_spanning_tree_rstp()

        # Asserting the default root bridges of all DUTs using RSTP flow

        rstp_flow.assert_root_2_DUTs(DUT1, d_root_id_1, d_bridge_id_1, "32768"
                                     , DUT2, d_root_id_2, d_bridge_id_2, "32768")

        print("########## Removing the config #############")

        rstp_flow.remove_rstp_configuration_1_LINK_2_DUTs(DUT1, DUT1.ports['v1'], "10", "20", "30")
        rstp_flow.remove_rstp_configuration_1_LINK_2_DUTs(DUT2, DUT2.ports['v1'], "10", "20", "30")

    def test_func_2(self):

        DUT1.tn.connect()
        DUT1.tn.write_cmd(cmd="show ip int")
        output = DUT1.tn.read()
        print(output)
        DUT1.tn.close()

    def test_func_3(self, var=3):

        if var == 1:
            print("Block 1")

        elif var == 2:
            print("Block 2")

        else:
            print("Block 3")

        print("-------- Final -----------")

    def test_func_4(self):

        DUT6.session.connect("admin", "Admin1234!")
        DUT6.session.send_cmd(cmd="show ip route")
        output = DUT6.session.read()
        print(output)
        DUT6.session.close()

        print("########################")

        DUT6.tn.connect("admin", "Admin1234!")
        DUT6.tn.write_cmd(cmd="show ip route")
        output1 = DUT6.tn.read()
        print(output1)
        DUT6.tn.close()

        print("########################")

        soft_ver = DUT6.sanity.show_software_version_device()
        print(soft_ver)