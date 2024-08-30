import time
from Management import dut_objects
from flows import rstp_flow
from test_beds import test_bed_1

dut1 = test_bed_1.DUT1
dut2 = test_bed_1.DUT2
dut3 = test_bed_1.DUT3
dut4 = test_bed_1.DUT4
dut6 = test_bed_1.DUT6
dut7 = test_bed_1.DUTF

ip_session_FA_System = "10.2.109.213"


DUT1 = dut_objects.DUT_Objects_TestBed(dut1)
DUT2 = dut_objects.DUT_Objects_TestBed(dut2)
DUT3 = dut_objects.DUT_Objects_TestBed(dut3)
DUT_FA_system = dut_objects.DUT_Objects(ip_session=ip_session_FA_System)
DUT7 = dut_objects.DUT_Objects_TestBed(dut7)

rstp_flow = rstp_flow.RSTPFlow()


# ip_session__1 = dut1["ip"]
# ip_session_2 = "10.2.109.83"
# ip_session_3 = "10.2.109.232"
# ip_session_4 = "10.2.109.100"
ip_session_5 = "10.2.109.85"
ip_session_6 = "10.2.109.173"

# DUT6 = dut_objects.DUT_Objects(ip_session=ip_session_6)
DUT4 = dut_objects.DUT_Objects_TestBed(dut4)
DUT6 = dut_objects.DUT_Objects_TestBed(dut6)
DUT5 = dut_objects.DUT_Objects(ip_session=ip_session_5)



# class TestBed:
#
#     def test_func_1(self):
#
#         print("###### Test_func_1 ######")
#         print("########## Test with Test Bed #############")
#         print("###### 2 DUTs ######")
#
#         #    Topology
#         #
#         #  DUT1 -- DUT2
#
#         # print(ip_session__1)
#         #
#         # rstp_flow.create_rstp_configuration_1_LINK_2_DUTs(DUT1, dut1["ports"]["v1value"], "10", "20", "30", "rst")
#         # rstp_flow.create_rstp_configuration_1_LINK_2_DUTs(DUT2, dut2["ports"]["v1value"], "10", "20", "30", "rst", dut2["ports"]["h3value"])
#
#         # DUT1.vl.create_vlan(vlan="3000")
#         print(DUT1.ip_session)
#         print(DUT1.hostname)
#         print(DUT1.ports)
#         print(DUT1.ports["v1"])
#         print(DUT1.user)
#
#         rstp_flow.create_rstp_configuration_1_LINK_2_DUTs(DUT1, DUT1.ports['v1'],"10","20","30","rstp")
#         rstp_flow.create_rstp_configuration_1_LINK_2_DUTs(DUT2, DUT2.ports['v1'], "10", "20", "30", "rstp")
#
#         # Check the default Root Bridge (the lowest MAC in the topology - DUT1)
#
#         d_root_id_1, d_bridge_id_1, ports_1, dict_of_ports_1 = DUT1.stp.show_spanning_tree_rstp()
#         d_root_id_2, d_bridge_id_2, ports_2, dict_of_ports_2 = DUT2.stp.show_spanning_tree_rstp()
#
#         # Asserting the default root bridges of all DUTs using RSTP flow
#
#         rstp_flow.assert_root_2_DUTs(DUT1, d_root_id_1, d_bridge_id_1, "32768"
#                                      , DUT2, d_root_id_2, d_bridge_id_2, "32768")
#
#         print("########## Removing the config #############")
#
#         rstp_flow.remove_rstp_configuration_1_LINK_2_DUTs(DUT1, DUT1.ports['v1'], "10", "20", "30")
#         rstp_flow.remove_rstp_configuration_1_LINK_2_DUTs(DUT2, DUT2.ports['v1'], "10", "20", "30")
#
#     def test_func_2(self):
#
#         DUT1.tn.connect()
#         DUT1.tn.write_cmd(cmd="show ip int")
#         output = DUT1.tn.read()
#         print(output)
#         DUT1.tn.close()
#
#     def test_func_3(self, var=3):
#
#         if var == 1:
#             print("Block 1")
#
#         elif var == 2:
#             print("Block 2")
#
#         else:
#             print("Block 3")
#
#         print("-------- Final -----------")
#
#     def test_func_4(self):
#
#         DUT6.session.connect("admin", "Admin1234!")
#         DUT6.session.send_cmd(cmd="show ip route")
#         output = DUT6.session.read()
#         print(output)
#         DUT6.session.close()
#
#         print("########################")
#
#         DUT6.tn.connect("admin", "Admin1234!")
#         DUT6.tn.write_cmd(cmd="show ip route")
#         output1 = DUT6.tn.read()
#         print(output1)
#         DUT6.tn.close()
#
#         print("########################")
#
#         soft_ver = DUT6.sanity.show_software_version_device()
#         print(soft_ver)
#
#
#     def test_func_5(self):
#
#         print("########## Creating X interfaces VLAN and advertising them into OSPF in X areas for 2 DUTs #############")
#
#         int_vlan_1 = ".0.0.1"
#         int_vlan_2 = ".0.0.2"
#         port1 = "Ex 0/11"
#         port2 = "Ex 0/1"
#         mask = "255.255.255.0"
#         area = "0.0.0."
#         i = 1
#
#         DUT6.session.connect()
#         DUT4.session.connect()
#
#         for vlan in range(40,50):
#
#             # Creating the VLAN
#
#             DUT6.vl.add_ports_to_vlan(ports=port1,vlan=str(vlan))
#             DUT4.vl.add_ports_to_vlan(ports=port2, vlan=str(vlan))
#
#             # Creating the Interface VLAN
#
#             DUT6.ip.add_ip_interface(int_vlan=str(vlan),ip=(str(vlan) + int_vlan_1), mask=mask)
#             DUT6.ip.no_shut_int_vlan(int_vlan=vlan)
#
#             DUT4.ip.add_ip_interface(int_vlan=str(vlan), ip=(str(vlan) + int_vlan_2), mask=mask)
#             DUT4.ip.no_shut_int_vlan(int_vlan=vlan)
#
#             # Adding the network to ospf area
#
#             DUT6.ospf.advertise_network(ip_network=(str(vlan) + int_vlan_1), area= area + str(i))
#             DUT4.ospf.advertise_network(ip_network=(str(vlan) + int_vlan_2), area=area + str(i))
#
#             print(f"###### The i is {i} #######")
#             print(f"The area is {area}" + str(i))
#
#             i = i+1
#
#
#         DUT6.int.no_shut_interface(interface=port1)
#         DUT4.int.no_shut_interface(interface=port2)
#
#         DUT6.session.close()
#         DUT4.session.close()
#
#     def test_func_6(self):
#
#         print("########## Creating 500 interfaces VLAN and advertising them into OSPF #############")
#
#         int_vlan = ".0.0."
#         port = "Gi 0/25"
#         mask = "255.255.255.0"
#         area = "0.0.0.0"
#         # i = 1
#
#         DUT5.session.connect()
#
#         for vlan in range(40,254):
#
#             # Creating the VLAN
#
#             DUT5.vl.add_ports_to_vlan(ports=port,vlan=str(vlan))
#
#             # Creating the Interface VLAN
#
#             DUT5.ip.add_ip_interface(int_vlan=str(vlan),ip=(str(vlan)+int_vlan+str(vlan)), mask=mask)
#             DUT5.ip.no_shut_int_vlan(int_vlan=vlan)
#
#             # Adding the network to ospf area
#
#             DUT5.ospf.advertise_network(ip_network=(str(vlan)+int_vlan+str(vlan)), area= area)
#
#         DUT5.int.no_shut_interface(interface=port)
#
#         DUT5.session.close()
#
#     def test_func_7(self):
#
#         print("########## Creating 50 interfaces VLAN and advertising them into OSPF #############")
#
#         int_vlan = ".0.0.1"
#         port = "Ex 0/14"
#         mask = "255.255.255.0"
#         area = "0.0.0.0"
#         # i = 1
#
#         # DUT_FA_system.session.connect()
#         DUT7.session.connect()
#
#         for vlan in range(11,61):
#
#             # Creating the VLAN
#
#             # DUT_FA_system.vl.add_ports_to_vlan(ports=port,vlan=str(vlan))
#             DUT7.vl.add_ports_to_vlan(ports=port,vlan=str(vlan))
#             # Creating the Interface VLAN
#
#             # DUT_FA_system.ip.add_ip_interface(int_vlan=str(vlan),ip=(str(vlan)+int_vlan), mask=mask)
#             # DUT_FA_system.ip.no_shut_int_vlan(int_vlan=vlan)
#
#             DUT7.ip.add_ip_interface(int_vlan=str(vlan), ip=(str(vlan) + int_vlan), mask=mask)
#             DUT7.ip.no_shut_int_vlan(int_vlan=vlan)
#
#             # Adding the network to ospf area
#
#             # DUT_FA_system.ospf.advertise_network(ip_network=(str(vlan)+int_vlan), area=area)
#             DUT7.ospf.advertise_network(ip_network=(str(vlan) + int_vlan), area=area)
#
#         # DUT_FA_system.int.no_shut_interface(interface=port)
#         DUT7.int.no_shut_interface(interface=port)
#
#         # DUT_FA_system.session.close()
#         DUT7.session.close()






